#!/usr/bin/env python3
"""Round-81 C2 counter — the capture-once / audit-offline re-derivation chain.

The lane takes a fresh GET-only capture of its primary property this round, writes
the receipts under `.ufo/waves/round-81/capture/`, and audits them offline with
`scripts/header_audit.py` through a version-1 manifest. This counter decides
whether that chain re-derives from committed bytes alone:

    met <=> surfaces >= 1
          and every receipt verifies (body sha256, byte count, integer status,
              RFC 3339 fetch time on or after the round's first day, GET,
              not truncated, URL host in the manifest's allowlist)
          and header_audit over the committed manifest exits 0 or 1 with checks=<surfaces>
          and the audit's stdout equals the committed audit receipt byte-for-byte

The measurement performs no network I/O: the capture happens once, during the
round, and the verdict is then re-derivable forever.

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
MANIFEST = ".ufo/waves/round-81/capture/manifest.json"
AUDIT_RECEIPT = ".ufo/waves/round-81/controls/after-c2-audit.txt"
SUMMARY_RE = re.compile(r"^checks=(\d+) findings=(\d+)$")
RFC3339_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$")
FINDING_RE = re.compile(r"^\S+ \S+ \S+$")


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


def normalise(text: str) -> list[str]:
    return [line.rstrip() for line in text.strip("\n").splitlines() if line.strip()]


def verify_receipt(tree: Path, source: str, allowlist: list[str]) -> tuple[bool, str, dict | None]:
    path = tree / source
    raw = read_bytes(path)
    if raw is None:
        return False, f"{source}: receipt absent", None
    try:
        receipt = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        return False, f"{source}: unparseable ({exc})", None
    if not isinstance(receipt, dict):
        return False, f"{source}: receipt is not an object", None
    body_name = receipt.get("bodyFile")
    if not isinstance(body_name, str) or not body_name:
        return False, f"{source}: no bodyFile", receipt
    body = read_bytes(path.parent / body_name)
    if body is None:
        return False, f"{source}: body {body_name} absent", receipt
    digest = hashlib.sha256(body).hexdigest()
    if receipt.get("sha256") != digest:
        return False, f"{source}: body sha256 {digest[:12]} != receipt {str(receipt.get('sha256'))[:12]}", receipt
    if receipt.get("bytes") != len(body):
        return False, f"{source}: bytes {receipt.get('bytes')} != body {len(body)}", receipt
    status = receipt.get("status")
    if isinstance(status, bool) or not isinstance(status, int) or not 100 <= status <= 599:
        return False, f"{source}: status {status!r} unparseable", receipt
    fetched = receipt.get("fetchedAt")
    if not isinstance(fetched, str) or not RFC3339_RE.match(fetched):
        return False, f"{source}: fetchedAt {fetched!r} is not RFC 3339", receipt
    if fetched < ROUND_FIRST_DAY:
        return False, f"{source}: fetchedAt {fetched} predates the round ({ROUND_FIRST_DAY})", receipt
    if receipt.get("method") != "GET":
        return False, f"{source}: method {receipt.get('method')!r} is not GET", receipt
    if receipt.get("truncated") is not False:
        return False, f"{source}: truncated={receipt.get('truncated')!r}", receipt
    url = receipt.get("url")
    if not isinstance(url, str):
        return False, f"{source}: no url", receipt
    host = re.sub(r"^https?://", "", url).split("/")[0].split(":")[0].lower()
    if host not in allowlist:
        return False, f"{source}: host {host} outside the allowlist", receipt
    return True, f"{source}: ok {status} {len(body)}B {fetched} {host}", receipt


def run_audit(tree: Path, work: Path) -> tuple[int, str, str]:
    tool = tree / "scripts/header_audit.py"
    if not tool.is_file():
        return 127, "", "scripts/header_audit.py absent"
    try:
        p = subprocess.run([sys.executable, "-B", str(tool), "--manifest", str(tree / MANIFEST),
                            "--root", str(tree)], cwd=str(work), capture_output=True, text=True,
                           timeout=180)
    except (OSError, subprocess.SubprocessError) as exc:
        return 127, "", f"{type(exc).__name__}: {exc}"
    return p.returncode, p.stdout, p.stderr


def evaluate(tree: Path, work: Path) -> tuple[bool, list[str], dict]:
    detail: list[str] = []
    manifest_path = tree / MANIFEST
    if not manifest_path.is_file():
        return False, ["capture: no manifest at the measured revision"], {"surfaces": 0}
    try:
        manifest = json.loads(read_text(manifest_path))
    except ValueError as exc:
        return False, [f"manifest unparseable: {exc}"], {"surfaces": 0}
    if not isinstance(manifest, dict) or manifest.get("version") != 1:
        return False, ["manifest is not version 1"], {"surfaces": 0}
    checks = manifest.get("checks")
    if not isinstance(checks, list) or not checks:
        return False, ["manifest carries no check"], {"surfaces": 0}
    allowlist = manifest.get("allowlist")
    if not isinstance(allowlist, list) or not allowlist or not all(isinstance(a, str) for a in allowlist):
        return False, ["manifest declares no host allowlist"], {"surfaces": len(checks)}
    failures = []
    for index, check in enumerate(checks, 1):
        if not isinstance(check, dict):
            failures.append(f"check-{index}: not an object")
            continue
        source = check.get("source")
        if not isinstance(source, str) or not source:
            failures.append(f"check-{index}: no source")
            continue
        ok, message, _ = verify_receipt(tree, source, allowlist)
        detail.append(message)
        if not ok:
            failures.append(message)
    receipt_text = read_text(tree / AUDIT_RECEIPT)
    if not receipt_text.strip():
        failures.append(f"{AUDIT_RECEIPT} absent or empty")
        rc, stdout, stderr = -1, "", ""
    else:
        rc, stdout, stderr = run_audit(tree, work)
        if rc not in (0, 1):
            failures.append(f"header_audit rc={rc}: {(stdout + stderr).strip()[-160:]}")
        observed = normalise(stdout)
        committed = normalise(receipt_text)
        if observed != committed:
            failures.append(f"audit stdout differs from the committed receipt ({len(observed)} vs "
                            f"{len(committed)} lines)")
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
    facts = {"surfaces": len(checks), "failures": len(failures), "audit_rc": rc}
    return not failures, failures + detail, facts


def selftest(work: Path) -> int:
    base = work / "selftest"
    real_tool = Path(__file__).resolve().parents[3] / "scripts" / "header_audit.py"
    checks: list[tuple[str, bool, str]] = []

    def fixture(name: str, fetched: str = "2026-11-04T12:00:00Z", body: bytes = b"<html>ok</html>",
                status: int = 200, audit: str | None = None) -> Path:
        tree = base / name
        surface = tree / ".ufo/waves/round-81/capture/surface-1"
        surface.mkdir(parents=True, exist_ok=True)
        (surface / "body.bin").write_bytes(body)
        receipt = {"bodyFile": "body.bin", "bytes": len(body), "error": None, "fetchedAt": fetched,
                   "finalUrl": "https://ds4cc.com/", "headers": [
                       {"name": "Content-Type", "value": "text/html; charset=utf-8"},
                       {"name": "Strict-Transport-Security", "value": "max-age=60"},
                       {"name": "X-Content-Type-Options", "value": "nosniff"},
                       {"name": "Content-Security-Policy", "value": "default-src 'self'"}],
                   "method": "GET", "sha256": hashlib.sha256(body).hexdigest(), "status": status,
                   "truncated": False, "url": "https://ds4cc.com/", "userAgent": "round81"}
        (surface / "response.json").write_text(json.dumps(receipt, indent=1), encoding="utf-8")
        manifest = {"version": 1, "allowlist": ["ds4cc.com"], "checks": [{
            "id": "surface-1", "source": ".ufo/waves/round-81/capture/surface-1/response.json",
            "url": "https://ds4cc.com/", "https": True,
            "expect": {"content_type_present": True, "hsts_present": True,
                       "xcto_nosniff_value": True, "csp_present": True,
                       "singleton_fields": ["content-type"]}}]}
        (tree / ".ufo/waves/round-81/capture/manifest.json").write_text(
            json.dumps(manifest, indent=1), encoding="utf-8")
        (tree / "scripts").mkdir(parents=True, exist_ok=True)
        if real_tool.is_file():
            shutil.copyfile(real_tool, tree / "scripts/header_audit.py")
        (tree / ".ufo/waves/round-81/controls").mkdir(parents=True, exist_ok=True)
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
    (tampered / ".ufo/waves/round-81/capture/surface-1/body.bin").write_bytes(b"<html>oK</html>")
    ok, messages, _ = evaluate(tampered, work)
    checks.append(("body-digest-opens", not ok and any("sha256" in m for m in messages), "; ".join(messages[:2])))

    counted = fixture("counted")
    receipt_path = counted / ".ufo/waves/round-81/capture/surface-1/response.json"
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

    empty = fixture("empty")
    (empty / ".ufo/waves/round-81/capture/manifest.json").write_text(
        json.dumps({"version": 1, "allowlist": ["ds4cc.com"], "checks": []}), encoding="utf-8")
    ok, messages, _ = evaluate(empty, work)
    checks.append(("no-surface-opens", not ok and any("no check" in m for m in messages), "; ".join(messages[:2])))

    for name, ok, detail in checks:
        print(f"  {'ok' if ok else 'FAIL'} {name} :: {detail}")
    passed = sum(1 for _, ok, _ in checks if ok)
    print(f"selftest: {passed}/{len(checks)} passed")
    return 0 if passed == len(checks) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--work")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    root = Path(a.root).resolve()
    work = Path(a.work) if a.work else Path(tempfile.mkdtemp(prefix="kake-c81-capture-"))
    work.mkdir(parents=True, exist_ok=True)
    try:
        if a.selftest:
            return selftest(work)
        if not (root / "corpus").is_dir():
            print(f"unevaluable: {root} is not a lane tree")
            return 2
        ok, messages, facts = evaluate(root, work)
        for message in messages:
            print(message)
        print(f"C2v1 root={root.name} surfaces={facts.get('surfaces', 0)} "
              f"failures={facts.get('failures', len(messages))} "
              f"audit_rc={facts.get('audit_rc', '-')} met={'true' if ok else 'false'}")
        print(f"exit={0 if ok else 1}")
        return 0 if ok else 1
    finally:
        if a.work is None:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
