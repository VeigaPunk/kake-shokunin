#!/usr/bin/env python3
"""Round-81 C2 counter — the capture-once / audit-offline re-derivation chain.

The lane takes a fresh GET-only capture of three declared surfaces of its primary
property this round, writes the receipts under `.ufo/waves/round-81/capture/`, and
audits them offline with `scripts/header_audit.py` through a version-1 manifest.
This counter decides whether that chain re-derives from committed bytes alone:

    met <=> the manifest's checks are exactly the surfaces declared in
              `.ufo/waves/round-81/capture-expectations.json` (same ids, same urls,
              same expect objects, same allowlist)
          and every receipt verifies (body sha256, byte count, integer status,
              RFC 3339 fetch time on or after the round's first day, GET,
              not truncated, url identical to the declared url, finalUrl https on
              an allowlisted host)
          and header_audit over the manifest exits 0 or 1 with checks=<surfaces>
          and the audit's stdout equals the committed audit receipt byte-for-byte
              (after removing one trailing newline from each side)

The declared expectations are read from the frozen expectations file, never from
the manifest: a manifest that declares its own expectations cannot make a surface
look clean. The measurement performs no network I/O — the capture happens once,
during the round, and the verdict is re-derivable forever.

Exit: 0 met, 1 not met, 2 unevaluable, 64 usage. Read-only outside --work.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROUND_FIRST_DAY = "2026-11-04T00:00:00Z"
WAVE = ".ufo/waves/round-81"
EXPECTATIONS = f"{WAVE}/capture-expectations.json"
MANIFEST = f"{WAVE}/capture/manifest.json"
AUDIT_RECEIPT = f"{WAVE}/controls/after-c2-audit.txt"
AUDIT_TOOL = "scripts/header_audit.py"
SUMMARY_RE = re.compile(r"^checks=(\d+) findings=(\d+)$")
RFC3339_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$")
FINDING_RE = re.compile(r"^\S+ \S+ \S+$")

EXPORT_PATHS = [EXPECTATIONS, MANIFEST, AUDIT_RECEIPT, AUDIT_TOOL]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def read_bytes(path: Path) -> bytes | None:
    try:
        return path.read_bytes()
    except OSError:
        return None


def strip_one_newline(text: str) -> str:
    return text[:-1] if text.endswith("\n") else text


def host_of(url: str) -> str:
    return re.sub(r"^https?://", "", url).split("/")[0].split(":")[0].lower()


def materialise(root: Path, revision: str, work: Path) -> tuple[Path, list[str]]:
    tree = work / "tree"
    tree.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    for rel in EXPORT_PATHS:
        show = subprocess.run(["git", "-C", str(root), "show", f"{revision}:{rel}"],
                              capture_output=True)
        if show.returncode != 0:
            continue
        dst = tree / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(show.stdout)
    listing = subprocess.run(["git", "-C", str(root), "ls-tree", "-r", "--name-only", revision,
                              "--", f"{WAVE}/capture"], capture_output=True, text=True)
    if listing.returncode != 0:
        errors.append(f"ls-tree {WAVE}/capture rc={listing.returncode}")
    for rel in listing.stdout.splitlines():
        show = subprocess.run(["git", "-C", str(root), "show", f"{revision}:{rel}"],
                              capture_output=True)
        if show.returncode != 0:
            continue
        dst = tree / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(show.stdout)
    return tree, errors


def declared_surfaces(tree: Path) -> tuple[dict[str, dict], list[str], str]:
    try:
        doc = json.loads(read_text(tree / EXPECTATIONS))
    except ValueError as exc:
        return {}, [], f"expectations unreadable: {exc}"
    if not isinstance(doc, dict):
        return {}, [], "expectations is not an object"
    surfaces = doc.get("surfaces")
    allowlist = doc.get("allowlist")
    if not isinstance(surfaces, list) or not surfaces:
        return {}, [], "expectations declare no surface"
    if not isinstance(allowlist, list) or not allowlist or not all(isinstance(a, str) for a in allowlist):
        return {}, [], "expectations declare no host allowlist"
    table = {}
    for entry in surfaces:
        if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
            return {}, [], "expectations carry a surface without an id"
        table[entry["id"]] = entry
    return table, allowlist, ""


def verify_receipt(tree: Path, check: dict, declared: dict, allowlist: list[str]) -> tuple[bool, str]:
    source = check.get("source")
    path = tree / source
    raw = read_bytes(path)
    if raw is None:
        return False, f"{source}: receipt absent"
    try:
        receipt = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        return False, f"{source}: unparseable ({exc})"
    if not isinstance(receipt, dict):
        return False, f"{source}: receipt is not an object"
    body_name = receipt.get("bodyFile")
    if not isinstance(body_name, str) or not body_name:
        return False, f"{source}: no bodyFile"
    body = read_bytes(path.parent / body_name)
    if body is None:
        return False, f"{source}: body {body_name} absent"
    digest = hashlib.sha256(body).hexdigest()
    if receipt.get("sha256") != digest:
        return False, f"{source}: body sha256 {digest[:12]} != receipt {str(receipt.get('sha256'))[:12]}"
    if receipt.get("bytes") != len(body):
        return False, f"{source}: bytes {receipt.get('bytes')} != body {len(body)}"
    status = receipt.get("status")
    if isinstance(status, bool) or not isinstance(status, int) or not 100 <= status <= 599:
        return False, f"{source}: status {status!r} unparseable"
    fetched = receipt.get("fetchedAt")
    if not isinstance(fetched, str) or not RFC3339_RE.match(fetched):
        return False, f"{source}: fetchedAt {fetched!r} is not RFC 3339"
    if fetched < ROUND_FIRST_DAY:
        return False, f"{source}: fetchedAt {fetched} predates the round ({ROUND_FIRST_DAY})"
    if receipt.get("method") != "GET":
        return False, f"{source}: method {receipt.get('method')!r} is not GET"
    if receipt.get("truncated") is not False:
        return False, f"{source}: truncated={receipt.get('truncated')!r}"
    if receipt.get("url") != declared.get("url"):
        return False, f"{source}: url {receipt.get('url')!r} != declared {declared.get('url')!r}"
    final = receipt.get("finalUrl")
    if not isinstance(final, str) or not final.lower().startswith("https://"):
        return False, f"{source}: finalUrl {final!r} is not https"
    host = host_of(final)
    if host not in allowlist:
        return False, f"{source}: finalUrl host {host} outside the allowlist"
    return True, f"{source}: ok {status} {len(body)}B {fetched} {host}"


def run_audit(tree: Path, work: Path) -> tuple[int, str, str]:
    tool = tree / AUDIT_TOOL
    if not tool.is_file():
        return 127, "", f"{AUDIT_TOOL} absent"
    try:
        p = subprocess.run([sys.executable, "-B", str(tool), "--manifest", str(tree / MANIFEST),
                            "--root", str(tree)], cwd=str(work), capture_output=True, text=True,
                           timeout=180)
    except (OSError, subprocess.SubprocessError) as exc:
        return 127, "", f"{type(exc).__name__}: {exc}"
    return p.returncode, p.stdout, p.stderr


def evaluate(tree: Path, work: Path) -> tuple[bool, list[str], dict]:
    failures: list[str] = []
    detail: list[str] = []
    table, allowlist, fault = declared_surfaces(tree)
    if fault:
        return False, [f"declared expectations: {fault}"], {"surfaces": 0, "failures": 1, "audit_rc": "-"}
    manifest_path = tree / MANIFEST
    if not manifest_path.is_file():
        return False, ["capture: no manifest at the measured revision"], {
            "surfaces": 0, "failures": 1, "audit_rc": "-"}
    try:
        manifest = json.loads(read_text(manifest_path))
    except ValueError as exc:
        return False, [f"manifest unparseable: {exc}"], {"surfaces": 0, "failures": 1, "audit_rc": "-"}
    if not isinstance(manifest, dict) or manifest.get("version") != 1:
        return False, ["manifest is not version 1"], {"surfaces": 0, "failures": 1, "audit_rc": "-"}
    checks = manifest.get("checks")
    if not isinstance(checks, list) or not checks:
        return False, ["manifest carries no check"], {"surfaces": 0, "failures": 1, "audit_rc": "-"}
    if manifest.get("allowlist") != allowlist:
        failures.append("manifest allowlist differs from the declared allowlist")
    seen: list[str] = []
    for index, check in enumerate(checks, 1):
        if not isinstance(check, dict):
            failures.append(f"check-{index}: not an object")
            continue
        cid = check.get("id")
        if not isinstance(cid, str) or cid not in table:
            failures.append(f"check-{index}: id {cid!r} is not a declared surface")
            continue
        seen.append(cid)
        declared = table[cid]
        if check.get("url") != declared.get("url"):
            failures.append(f"{cid}: manifest url {check.get('url')!r} != declared {declared.get('url')!r}")
        if check.get("expect") != declared.get("expect"):
            failures.append(f"{cid}: manifest expect differs from the declared expectations")
        if check.get("https") is not True:
            failures.append(f"{cid}: https is not true")
        ok, message = verify_receipt(tree, check, declared, allowlist)
        detail.append(message)
        if not ok:
            failures.append(message)
    missing = [cid for cid in table if cid not in seen]
    if missing:
        failures.append("declared surfaces missing from the manifest: " + ", ".join(sorted(missing)))
    extra = [cid for cid in seen if seen.count(cid) > 1]
    if extra:
        failures.append("duplicate manifest check ids: " + ", ".join(sorted(set(extra))))
    receipt_text = read_text(tree / AUDIT_RECEIPT)
    if not receipt_text.strip():
        failures.append(f"{AUDIT_RECEIPT} absent or empty")
        rc = "-"
    else:
        rc, stdout, stderr = run_audit(tree, work)
        if rc not in (0, 1):
            failures.append(f"header_audit rc={rc}: {(stdout + stderr).strip()[-160:]}")
        if strip_one_newline(stdout) != strip_one_newline(receipt_text):
            failures.append("audit stdout differs from the committed receipt (byte comparison after "
                            "one trailing newline)")
        observed = [line for line in stdout.splitlines() if line.strip()]
        if observed:
            summary = SUMMARY_RE.match(observed[-1])
            if not summary:
                failures.append("audit stdout carries no checks=/findings= summary")
            else:
                if int(summary.group(1)) != len(checks):
                    failures.append(f"audit checks={summary.group(1)} != manifest checks={len(checks)}")
                for line in observed[:-1]:
                    if not FINDING_RE.match(line):
                        failures.append(f"finding line is not three tokens: {line!r}")
                        break
        else:
            failures.append("audit stdout is empty")
    facts = {"surfaces": len(checks), "failures": len(failures), "audit_rc": rc,
             "declared": len(table)}
    return not failures, failures + detail, facts


def selftest(work: Path) -> int:
    base = work / "selftest"
    real_tool = Path(__file__).resolve().parents[3] / AUDIT_TOOL
    checks: list[tuple[str, bool, str]] = []

    def fixture(name: str, *, fetched: str = "2026-11-04T12:00:00Z",
                body: bytes = b"<html>ok</html>", status: int = 200,
                manifest_url: str = "https://ds4cc.com/",
                expect_csp: bool = True, surfaces: int = 1,
                manifest_expect_csp: bool | None = None,
                audit: str | None = None, declared_url: str = "https://ds4cc.com/") -> Path:
        tree = base / name
        declared = {"version": 1, "allowlist": ["ds4cc.com"], "surfaces": []}
        entries = []
        for i in range(1, surfaces + 1):
            sid = f"surface-{i}"
            url = declared_url if i == 1 else f"https://ds4cc.com/{sid}"
            expect = {"content_type_present": True, "hsts_present": True,
                      "xcto_nosniff_value": True, "csp_present": expect_csp,
                      "singleton_fields": ["content-type"]}
            declared["surfaces"].append({"id": sid, "url": url, "expect": expect})
            entries.append((sid, url, expect))
        surface = tree / WAVE / "capture" / "surface-1"
        surface.mkdir(parents=True, exist_ok=True)
        (surface / "body.bin").write_bytes(body)
        receipt = {"bodyFile": "body.bin", "bytes": len(body), "error": None, "fetchedAt": fetched,
                   "finalUrl": "https://ds4cc.com/", "headers": [
                       {"name": "Content-Type", "value": "text/html; charset=utf-8"},
                       {"name": "Strict-Transport-Security", "value": "max-age=60"},
                       {"name": "X-Content-Type-Options", "value": "nosniff"},
                       {"name": "Content-Security-Policy", "value": "default-src 'self'"}],
                   "method": "GET", "sha256": hashlib.sha256(body).hexdigest(), "status": status,
                   "truncated": False, "url": declared_url, "userAgent": "round81"}
        (surface / "response.json").write_text(json.dumps(receipt, indent=1), encoding="utf-8")
        (tree / WAVE / "capture-expectations.json").write_text(json.dumps(declared, indent=1),
                                                              encoding="utf-8")
        manifest = {"version": 1, "allowlist": ["ds4cc.com"], "checks": []}
        for i, (sid, url, expect) in enumerate(entries, 1):
            manifest_expect = dict(expect)
            if i == 1 and manifest_expect_csp is not None:
                manifest_expect["csp_present"] = manifest_expect_csp
            manifest["checks"].append({
                "id": sid, "source": f"{WAVE}/capture/{sid}/response.json",
                "url": manifest_url if i == 1 else url, "https": True, "expect": manifest_expect})
        (tree / WAVE / "capture" / "manifest.json").write_text(json.dumps(manifest, indent=1),
                                                               encoding="utf-8")
        (tree / "scripts").mkdir(parents=True, exist_ok=True)
        if real_tool.is_file():
            shutil.copyfile(real_tool, tree / "scripts/header_audit.py")
        (tree / WAVE / "controls").mkdir(parents=True, exist_ok=True)
        if audit is None:
            rc, stdout, _ = run_audit(tree, work)
            (tree / AUDIT_RECEIPT).write_text(stdout, encoding="utf-8")
            checks.append((f"{name}-audit-ran", rc in (0, 1), f"rc={rc}"))
        else:
            (tree / AUDIT_RECEIPT).write_text(audit, encoding="utf-8")
        return tree

    green = fixture("green")
    ok, messages, facts = evaluate(green, work)
    checks.append(("green-met", ok, f"surfaces={facts['surfaces']} {messages[-2:] if not ok else ''}"))

    tampered = fixture("tampered")
    (tampered / WAVE / "capture/surface-1/body.bin").write_bytes(b"<html>oK</html>")
    ok, messages, _ = evaluate(tampered, work)
    checks.append(("body-digest-opens", not ok and any("sha256" in m for m in messages), "; ".join(messages[:2])))

    counted = fixture("counted")
    receipt_path = counted / WAVE / "capture/surface-1/response.json"
    doc = json.loads(receipt_path.read_text(encoding="utf-8"))
    doc["bytes"] = doc["bytes"] + 1
    receipt_path.write_text(json.dumps(doc), encoding="utf-8")
    ok, messages, _ = evaluate(counted, work)
    checks.append(("byte-count-opens", not ok and any("!=" in m for m in messages), "; ".join(messages[:2])))

    stale = fixture("stale", fetched="2026-11-03T23:59:59Z")
    ok, messages, _ = evaluate(stale, work)
    checks.append(("stale-capture-opens", not ok and any("predates" in m for m in messages), "; ".join(messages[:2])))

    drifted = fixture("drifted")
    (drifted / AUDIT_RECEIPT).write_text("surface-1 csp_present missing\nchecks=1 findings=1\n",
                                        encoding="utf-8")
    ok, messages, _ = evaluate(drifted, work)
    checks.append(("audit-drift-opens", not ok and any("differs" in m for m in messages), "; ".join(messages[:2])))

    url_drift = fixture("url-drift", manifest_url="https://evil.test/")
    ok, messages, _ = evaluate(url_drift, work)
    checks.append(("manifest-url-drift-opens", not ok and any("manifest url" in m for m in messages),
                   "; ".join(messages[:2])))

    expect_drift = fixture("expect-drift", manifest_expect_csp=False)
    ok, messages, _ = evaluate(expect_drift, work)
    checks.append(("manifest-expect-drift-opens", not ok and any("expect differs" in m for m in messages),
                   "; ".join(messages[:2])))

    two = fixture("two-declared", surfaces=2)
    (two / WAVE / "capture/manifest.json").write_text(json.dumps(
        {"version": 1, "allowlist": ["ds4cc.com"], "checks": [
            {"id": "surface-1", "source": f"{WAVE}/capture/surface-1/response.json",
             "url": "https://ds4cc.com/", "https": True,
             "expect": json.loads((two / WAVE / "capture-expectations.json").read_text())["surfaces"][0]["expect"]}]},
        indent=1), encoding="utf-8")
    ok, messages, _ = evaluate(two, work)
    checks.append(("missing-declared-surface-opens", not ok and any("missing from the manifest" in m for m in messages),
                   "; ".join(messages[:2])))

    empty = fixture("empty")
    (empty / WAVE / "capture-expectations.json").write_text(
        json.dumps({"version": 1, "allowlist": ["ds4cc.com"], "surfaces": []}), encoding="utf-8")
    ok, messages, _ = evaluate(empty, work)
    checks.append(("no-surface-opens", not ok and any("declare no surface" in m for m in messages),
                   "; ".join(messages[:2])))

    for name, ok, detail in checks:
        print(f"  {'ok' if ok else 'FAIL'} {name} :: {detail}")
    passed = sum(1 for _, ok, _ in checks if ok)
    print(f"selftest: {passed}/{len(checks)} passed")
    return 0 if passed == len(checks) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision")
    ap.add_argument("--work")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    root = Path(a.root).resolve()
    work = Path(a.work) if a.work else Path(tempfile.mkdtemp(prefix="kake-c81-capture-"))
    work.mkdir(parents=True, exist_ok=True)
    try:
        if a.selftest:
            return selftest(work)
        if not (root / "corpus").is_dir() and not a.revision:
            print(f"unevaluable: {root} is not a lane tree")
            return 2
        if a.revision:
            tree, errors = materialise(root, a.revision, work)
            if errors:
                print(f"unevaluable: {errors}")
                return 2
            label = a.revision
        else:
            tree, label = root, "worktree"
        ok, messages, facts = evaluate(tree, work)
        for message in messages:
            print(message)
        print(f"C2v1 revision={label} declared={facts.get('declared', 0)} "
              f"surfaces={facts.get('surfaces', 0)} failures={facts.get('failures', len(messages))} "
              f"audit_rc={facts.get('audit_rc', '-')} met={'true' if ok else 'false'}")
        print(f"exit={0 if ok else 1}")
        return 0 if ok else 1
    finally:
        if a.work is None:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
