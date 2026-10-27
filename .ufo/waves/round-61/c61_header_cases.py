#!/usr/bin/env python3
"""Round-61 C2 counter (version 1) — operability: scripts/header_audit.py passes the 18 contract cases.

Contract: .ufo/waves/round-61/contract.md § Claim C2 (base 9f07731a873585e655a6518233ea39f5d9fb8204,
access date 2026-10-27). The tool under test is extracted from committed bytes with
`git show <rev>:scripts/header_audit.py` into --work (a missing tool fails every case: the contract's
do-nothing control) and run as

    python3 -B <tool> --manifest <fixture>/manifest.json [--root <fixture>]

over gate-built fixture manifests with ids, hosts and directory names drawn from --seed, so a
fixture-keyed tool cannot recognise them. `--root` is passed only when the tool's own `--help`
advertises it; every fixture puts `manifest.json` at its root and its capture receipts at
`.ufo/waves/round-61/capture/<id>/response.json`, so root-relative and manifest-relative `source`
resolution coincide (contract §C2 does not fix the tool CLI — see the seat report's
CONTRACT AMBIGUITIES). Each fixture's recorded response uses the round-61 capture shape the real
tool must consume: `{"url","finalUrl","method","status","headers":[{"name","value"}] (ordered,
duplicates preserved), "headerCount","contentType","bytes","sha256","truncated","fetchedAt",
"userAgent","redirects","error","bodyFile"}` with the retained `body.bin` beside it.
Per-case timeout CASE_TIMEOUT seconds (hang = fail). A case passes only on the expected exit AND an
exact observation:

  * clean case  — exit 0, no finding line, exactly one summary line `checks=<n> findings=0`
                  with the fixture's check count;
  * finding case — exit 1, exactly one finding line `<check-id> <expected-class> <detail>`, exactly
                  one summary line with `findings=1` and the fixture's check count;
  * H13 (could-not-evaluate) — exit 1, exactly one `could_not_evaluate` line naming the faulty check,
                  no expectation-class finding for any check, summary `checks=2`;
  * exit-only cases (H14 version != 1, H15 unparseable JSON) — the stated exit and no finding line.

Finding grammar: `^(\\S+) ([a-z_]+) (.+)$` restricted to the classes
content_type_present, hsts_present, xcto_nosniff_value, csp_present, singleton_fields,
field_name_syntax, could_not_evaluate; summary grammar `^checks=([0-9]+) findings=([0-9]+)$`.

R3 (recorded, not asserted clean): the real manifest is materialised from the measured revision
(every `.ufo/waves/round-61/**/capture/**/*.json` blob via `git show <rev>:<path>`) into --work, so
the audit reads committed bytes and never the lane worktree. Shape: exactly one version-1 manifest
with 12 checks, each `source` naming a distinct existing capture receipt; the tool must then run and
print `checks=12 findings=<k>` with exit 0 iff k == 0. The findings value itself is NOT asserted — a
non-clean live census is reported, not a failure of the claim.

R4 (do-nothing control): at the contract base revision the tool is absent and the gate therefore
scores 0/18, measured through the same measure() with an absent tool path.

PREDICATE = "met: cases_passed == 18 of 18"
(contract §C2 also names R3's shape check in the predicate parenthetical: exit 0 requires, in
addition to 18/18, R3 shape ok and no violated do-nothing control. The scored denominator is the 18
H-fixtures; R3/R4 are printed as gate lines and can withhold exit 0.)

Kill rule: exit 0 iff met; 1 not met; 2 unevaluable (--root not a repository toplevel, --revision
unresolvable, clone/materialise failure); 64 usage. GIT_* scrubbed from every subprocess env. --work
is removed on exit. --selftest scores the gate itself, through the same measure(), against known
controls: missing tool (0/18), always-clean constant (9/18: the nine expected-clean fixtures),
always-exit-1 with no output (0/18), manifest-sniffing composite (9/18), and a reference
implementation of the contract rule written inside this file (18/18); plus two R3-shape controls
(12-check synthetic tree passes, 11-check fails). --tool <path> is the hidden override the selftest
drives; with --tool a run measures that tool instead of `git show <rev>:scripts/header_audit.py`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile

PREDICATE = "met: cases_passed == 18 of 18"
TOOL = "scripts/header_audit.py"
BASE = "9f07731a873585e655a6518233ea39f5d9fb8204"  # contract base (do-nothing control)
NCASES = 18
CASE_TIMEOUT = 180
GIT_TIMEOUT = 120
ALL_IDS = [f"H{i}" for i in range(1, NCASES + 1)]
POLICY = ("content_type_present", "hsts_present", "xcto_nosniff_value", "csp_present",
          "singleton_fields", "field_name_syntax")
CLASSES = set(POLICY) | {"could_not_evaluate"}
SEED: int | None = None

FIND_RE = re.compile(r"^(\S+) ([a-z_]+) (.+)$")
SUMMARY_RE = re.compile(r"^checks=([0-9]+) findings=([0-9]+)\s*$")

WORDS = ("amber basalt cipher delta ember fjord garnet harbor ionic jasper krill lantern matrix "
         "nimbus onyx prism quartz raven sable topaz umbra vertex willow xenon yarrow zephyr atlas "
         "birch cobalt dendro ether flint glacier helios indigo kestrel lotus merlin nova orbit "
         "pyre rowan sigma talc ultra violet weld xylem yonder zircon").split()
TLDS = ("com", "net", "org", "io", "dev", "co")

CAPTURE_DIR = ".ufo/waves/round-61/capture"


# --------------------------------------------------------------------------- helpers

def env() -> dict:
    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    e.update({"LC_ALL": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"})
    return e


def run(argv: list[str], timeout: int = CASE_TIMEOUT) -> tuple:
    """Combined stdout+stderr capture; rc is int, 'TIMEOUT' (hang = fail) or 'ERROR'."""
    try:
        p = subprocess.run(argv, env=env(), stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=timeout)
        return p.returncode, p.stdout.decode("utf-8", "replace")
    except subprocess.TimeoutExpired as exc:
        out = (exc.stdout or b"").decode("utf-8", "replace")
        return "TIMEOUT", out + f"\n[c61 case timeout {timeout}s]"
    except OSError as exc:
        return "ERROR", str(exc)


def git(root: str, *args: str) -> tuple[int, bytes]:
    try:
        p = subprocess.run(["git", "-C", root, *args], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, env=env(), timeout=GIT_TIMEOUT)
        return p.returncode, p.stdout
    except (subprocess.TimeoutExpired, OSError):
        return 1, b""


def rword(rng: random.Random, n: int = 3) -> str:
    return "-".join(rng.choice(WORDS) for _ in range(n))


def slug(rng: random.Random) -> str:
    return rword(rng, 3)


def fresh_id(rng: random.Random) -> str:
    return f"{rng.choice(WORDS)}-{rng.randrange(1000, 10000)}"


def host(rng: random.Random) -> str:
    return f"https://{rng.choice(WORDS)}.{rng.choice(WORDS)}.{rng.choice(TLDS)}/index.html"


def put(d: str, rel: str, data: bytes) -> None:
    tgt = os.path.join(d, rel)
    os.makedirs(os.path.dirname(tgt) or d, exist_ok=True)
    with open(tgt, "wb") as fh:
        fh.write(data)


# --------------------------------------------------------------------------- fixtures

def new_fixture(work: str, rng: random.Random, tag: str) -> str:
    d = os.path.join(work, f"fx-{tag}-{slug(rng)}")
    os.makedirs(d, exist_ok=True)
    return d


def write_capture(d: str, rng: random.Random, cid: str, status, headers: list) -> None:
    """Write one recorded response in the round-61 capture shape (headers as ordered name/value
    objects, names as received; a retained body whose sha256 is recorded)."""
    url = host(rng)
    body = f"<html><body>{rword(rng, 4)}</body></html>\n".encode("utf-8")
    put(d, f"{CAPTURE_DIR}/{cid}/body.bin", body)
    ctype = next((v for n, v in headers if n.lower() == "content-type"), None)
    rec = {"url": url, "finalUrl": url, "method": "GET", "status": status,
           "headers": [{"name": n, "value": v} for n, v in headers],
           "headerCount": len(headers), "contentType": ctype, "bytes": len(body),
           "sha256": hashlib.sha256(body).hexdigest(), "truncated": False,
           "fetchedAt": "2026-10-27T09:15:00Z", "userAgent": "round61", "redirects": [],
           "error": None, "bodyFile": "body.bin"}
    put(d, f"{CAPTURE_DIR}/{cid}/response.json",
        (json.dumps(rec, indent=1) + "\n").encode("utf-8"))


def add_check(d: str, rng: random.Random, headers=None, status: int = 200, https: bool = False,
              ct: bool = False, hsts: bool = False, xcto: bool = False, csp: bool = False,
              singles=None) -> dict:
    cid = fresh_id(rng)
    if headers is not None:
        write_capture(d, rng, cid, status, headers)
    return {"id": cid, "source": f"{CAPTURE_DIR}/{cid}/response.json", "url": host(rng),
            "https": https,
            "expect": {"content_type_present": ct, "hsts_present": hsts,
                       "xcto_nosniff_value": xcto, "csp_present": csp,
                       "singleton_fields": list(singles or [])}}


def write_manifest(d: str, checks: list, version: int = 1) -> None:
    put(d, "manifest.json",
        (json.dumps({"version": version, "checks": checks}, indent=1) + "\n").encode("utf-8"))


CT = ["Content-Type", "text/html; charset=utf-8"]
STS = ["Strict-Transport-Security", "max-age=31536000; includeSubDomains"]
XCTO = ["X-Content-Type-Options", "nosniff"]
CSP = ["Content-Security-Policy", "default-src 'self'"]


def build_case(work: str, rng: random.Random, cid: str) -> list[tuple[str, tuple]]:
    """Build one case's sub-fixtures; each sub is (fixture dir, expectation) with its own manifest.

    A case passes only if every sub-fixture meets its own expectation. The extra sub-fixtures carry
    the contract's boundary rules verbatim (2xx range, `https` gate, OWS span-trim, Set-Cookie
    exemption, token grammar, per-check could-not-evaluate) so a mutant that gets the boundary wrong
    fails the case rather than slipping through a single point.
    """
    subs: list[tuple[str, tuple]] = []
    n = [0]

    def nxt() -> str:
        n[0] += 1
        return new_fixture(work, rng, f"{cid.lower()}-{n[0]}")

    if cid == "H1":        # 200 + all declared expectations satisfied -> clean
        d = nxt()
        c = add_check(d, rng, [CT, STS, XCTO, CSP], https=True, ct=True, hsts=True, xcto=True,
                      csp=True, singles=["content-type"])
        write_manifest(d, [c])
        subs.append((d, ("clean", 1)))
    elif cid == "H2":      # 2xx without Content-Type -> content_type_present (200 and a non-200 2xx)
        d = nxt()
        c = add_check(d, rng, [XCTO], ct=True)
        write_manifest(d, [c])
        subs.append((d, ("find", c["id"], "content_type_present", 1)))
        d = nxt()
        c = add_check(d, rng, [["Date", "Mon, 26 Oct 2026 00:00:00 GMT"]], status=204, ct=True)
        write_manifest(d, [c])
        subs.append((d, ("find", c["id"], "content_type_present", 1)))
    elif cid == "H3":      # https + hsts expected + absent -> hsts_present; https false -> no finding
        d = nxt()
        c = add_check(d, rng, [CT], https=True, ct=True, hsts=True)
        write_manifest(d, [c])
        subs.append((d, ("find", c["id"], "hsts_present", 1)))
        d = nxt()
        c = add_check(d, rng, [CT], https=False, ct=True, hsts=True)
        write_manifest(d, [c])
        subs.append((d, ("clean", 1)))
    elif cid == "H4":      # HSTS with parameters, and max-age=0 -> clean (presence only)
        d = nxt()
        c = add_check(d, rng, [CT, STS], https=True, ct=True, hsts=True)
        write_manifest(d, [c])
        subs.append((d, ("clean", 1)))
        d = nxt()
        c = add_check(d, rng, [CT, ["Strict-Transport-Security", "max-age=0"]], https=True,
                      ct=True, hsts=True)
        write_manifest(d, [c])
        subs.append((d, ("clean", 1)))
    elif cid == "H5":      # X-Content-Type-Options: nosniff -> clean
        d = nxt()
        c = add_check(d, rng, [CT, XCTO], ct=True, xcto=True)
        write_manifest(d, [c])
        subs.append((d, ("clean", 1)))
    elif cid == "H6":      # value case + OWS (space, tab) -> clean
        d = nxt()
        c = add_check(d, rng, [CT, ["X-Content-Type-Options", "NOsniff "]], ct=True, xcto=True)
        write_manifest(d, [c])
        subs.append((d, ("clean", 1)))
        d = nxt()
        c = add_check(d, rng, [CT, ["X-Content-Type-Options", "nosniff\t"]], ct=True, xcto=True)
        write_manifest(d, [c])
        subs.append((d, ("clean", 1)))
    elif cid == "H7":      # value not exactly nosniff -> xcto_nosniff_value
        d = nxt()
        c = add_check(d, rng, [CT, ["X-Content-Type-Options", "sniff"]], ct=True, xcto=True)
        write_manifest(d, [c])
        subs.append((d, ("find", c["id"], "xcto_nosniff_value", 1)))
        d = nxt()
        c = add_check(d, rng, [CT, ["X-Content-Type-Options", "nosniff; preload"]], ct=True,
                      xcto=True)
        write_manifest(d, [c])
        subs.append((d, ("find", c["id"], "xcto_nosniff_value", 1)))
    elif cid == "H8":      # csp expected, header absent -> csp_present
        d = nxt()
        c = add_check(d, rng, [CT], ct=True, csp=True)
        write_manifest(d, [c])
        subs.append((d, ("find", c["id"], "csp_present", 1)))
    elif cid == "H9":      # a listed singleton repeated -> singleton_fields; once -> clean
        d = nxt()
        c = add_check(d, rng, [CT, ["Content-Type", "text/html"]], ct=True,
                      singles=["CONTENT-TYPE"])          # the declaration is case-insensitive
        write_manifest(d, [c])
        subs.append((d, ("find", c["id"], "singleton_fields", 1)))
        d = nxt()
        c = add_check(d, rng, [CT, ["X-Frame-Options", "DENY"], ["X-Frame-Options", "SAMEORIGIN"]],
                      ct=True, singles=["x-frame-options"])
        write_manifest(d, [c])
        subs.append((d, ("find", c["id"], "singleton_fields", 1)))
        d = nxt()
        c = add_check(d, rng, [CT], ct=True, singles=["content-type"])
        write_manifest(d, [c])
        subs.append((d, ("clean", 1)))
    elif cid == "H10":     # duplicate Set-Cookie is never a singleton -> clean
        d = nxt()
        c = add_check(d, rng, [CT, ["Set-Cookie", "a=1; Path=/"], ["Set-Cookie", "b=2; Path=/"]],
                      ct=True, singles=["set-cookie"])
        write_manifest(d, [c])
        subs.append((d, ("clean", 1)))
        d = nxt()
        c = add_check(d, rng, [CT, ["Set-Cookie", "a=1; Path=/"], ["Set-Cookie", "b=2; Path=/"]],
                      ct=True)
        write_manifest(d, [c])
        subs.append((d, ("clean", 1)))
    elif cid == "H11":     # non-2xx without Content-Type: the 2xx-only rule does not apply -> clean
        d = nxt()
        c = add_check(d, rng, [["Date", "Mon, 26 Oct 2026 00:00:00 GMT"]], status=404, ct=True)
        write_manifest(d, [c])
        subs.append((d, ("clean", 1)))
        d = nxt()
        c = add_check(d, rng, [["Date", "Mon, 26 Oct 2026 00:00:00 GMT"]], status=304, ct=True)
        write_manifest(d, [c])
        subs.append((d, ("clean", 1)))
    elif cid == "H12":     # header-name syntax fault -> field_name_syntax; token names -> clean
        d = nxt()
        c = add_check(d, rng, [CT, ["X Bad Name", "v"]], ct=True)
        write_manifest(d, [c])
        subs.append((d, ("find", c["id"], "field_name_syntax", 1)))
        d = nxt()
        c = add_check(d, rng, [CT, ["X-Custom_1", "v"]], ct=True)
        write_manifest(d, [c])
        subs.append((d, ("clean", 1)))
    elif cid == "H13":     # one missing receipt -> per-check could_not_evaluate, exit 1
        d = nxt()
        bad = add_check(d, rng, headers=None, ct=True)          # no response.json written
        good = add_check(d, rng, [CT], ct=True)
        write_manifest(d, [bad, good])
        subs.append((d, ("cne", bad["id"], 2)))
        d = nxt()
        bad2 = add_check(d, rng, headers=None, ct=True)
        write_capture(d, rng, bad2["id"], "not-a-status", [CT])
        good2 = add_check(d, rng, [CT], ct=True)
        write_manifest(d, [bad2, good2])
        subs.append((d, ("cne", bad2["id"], 2)))
        d = nxt()
        bad3 = add_check(d, rng, headers=None, ct=True)
        write_capture(d, rng, bad3["id"], None, [])
        good3 = add_check(d, rng, [CT], ct=True)
        write_manifest(d, [bad3, good3])
        subs.append((d, ("cne", bad3["id"], 2)))
    elif cid == "H14":     # manifest version != 1 -> exit 2
        d = nxt()
        c = add_check(d, rng, [CT], ct=True)
        write_manifest(d, [c], version=2)
        subs.append((d, ("exit", 2)))
    elif cid == "H15":     # manifest not parseable -> exit 2
        d = nxt()
        put(d, "manifest.json", b'{"version": 1, "checks": [\n')
        subs.append((d, ("exit", 2)))
    elif cid == "H16":     # every expectation declared false/absent, CLEAN headers -> clean
        d = nxt()
        c = add_check(d, rng, [CT, XCTO])          # clean under the literal class prose too
        write_manifest(d, [c])
        subs.append((d, ("clean", 1)))
        d = nxt()
        c = add_check(d, rng, [CT, XCTO, CSP, ["Vary", "Accept"], ["Vary", "Accept-Encoding"]],
                      ct=False, xcto=False, csp=False)   # an undeclared duplicate is not a finding
        write_manifest(d, [c])
        subs.append((d, ("clean", 1)))
    elif cid == "H17":     # leading/trailing whitespace only (spaces, tabs) -> clean
        d = nxt()
        c = add_check(d, rng, [["Content-Type", "  text/html  "],
                               ["X-Content-Type-Options", "  nosniff  "]], ct=True, xcto=True)
        write_manifest(d, [c])
        subs.append((d, ("clean", 1)))
        d = nxt()
        c = add_check(d, rng, [["Content-Type", "\ttext/html\t"],
                               ["X-Content-Type-Options", "\tnosniff\t"]], ct=True, xcto=True)
        write_manifest(d, [c])
        subs.append((d, ("clean", 1)))
    elif cid == "H18":     # empty checks array -> clean, checks=0
        d = nxt()
        write_manifest(d, [])
        subs.append((d, ("clean", 0)))
    else:
        raise AssertionError(cid)
    return subs


# --------------------------------------------------------------------------- judging

def parse(out: str) -> tuple[list, list]:
    finds, sums = [], []
    for line in out.splitlines():
        m = SUMMARY_RE.match(line.strip())
        if m:
            sums.append((int(m.group(1)), int(m.group(2))))
            continue
        m = FIND_RE.match(line.strip())
        if m and m.group(2) in CLASSES:
            finds.append((m.group(1), m.group(2), m.group(3)))
    return finds, sums


def judge(expect: tuple, rc, out: str) -> tuple[bool, str]:
    finds, sums = parse(out)
    tail = " | ".join(out.strip().splitlines()[-2:])[:160]
    if isinstance(rc, str):
        return False, f"{rc} {tail}"
    if expect[0] == "exit":
        ok = rc == expect[1] and not finds
        return ok, (f"want exit {expect[1]} + no finding lines; got exit {rc}, "
                    f"{len(finds)} finding line(s); {tail}")
    if expect[0] == "clean":
        want = expect[1]
        got = sums[0] if len(sums) == 1 else None
        ok = rc == 0 and not finds and got == (want, 0)
        return ok, (f"want exit 0 + no findings + one summary checks={want} findings=0; "
                    f"got exit {rc}, {len(finds)} finding line(s), summaries={sums}; {tail}")
    if expect[0] == "find":
        cid, cls, want = expect[1], expect[2], expect[3]
        hit = [f for f in finds if f[0] == cid and f[1] == cls]
        got = sums[0] if len(sums) == 1 else None
        ok = rc == 1 and len(finds) == 1 and bool(hit) and got == (want, 1)
        return ok, (f"want exit 1 + exactly one '{cid} {cls}'; got exit {rc}, findings={finds}, "
                    f"summaries={sums}; {tail}")
    cid, want = expect[1], expect[2]
    cne = [f for f in finds if f[0] == cid and f[1] == "could_not_evaluate"]
    policy = [f for f in finds if f[1] in POLICY]
    got = sums[0] if len(sums) == 1 else None
    ok = (rc == 1 and len(cne) == 1 and not policy and len(finds) == 1
          and got is not None and got[0] == want)
    return ok, (f"want exit 1 + one '{cid} could_not_evaluate' + no policy findings; got exit {rc}, "
                f"findings={finds}, summaries={sums}; {tail}")


# --------------------------------------------------------------------------- tool driving

def probe_root(tool: str) -> bool:
    """True iff the tool advertises --root in its own --help (contract fixes no tool CLI)."""
    rc, out = run([sys.executable, "-B", tool, "--help"], timeout=60)
    if isinstance(rc, str):
        return True
    if "--root" in out:
        return True
    if "--manifest" in out:
        return False
    return True


def argv_for(tool: str, fixture: str, root_ok: bool) -> list[str]:
    argv = [sys.executable, "-B", tool, "--manifest", os.path.join(fixture, "manifest.json")]
    return argv + (["--root", fixture] if root_ok else [])


def case_results(tool: str, work: str, rng: random.Random) -> list[tuple[str, bool, str]]:
    res: list[tuple[str, bool, str]] = []
    root_ok = probe_root(tool)
    for cid in ALL_IDS:
        try:
            subs = build_case(work, rng, cid)
        except Exception as exc:                     # a fixture that cannot be built fails its case
            res.append((cid, False, f"fixture-error {exc}"))
            continue
        all_ok, notes = True, []
        for k, (d, expect) in enumerate(subs):
            try:
                rc, out = run(argv_for(tool, d, root_ok))
            except Exception as exc:
                all_ok = False
                notes.append(f"[{k}] run-error {exc}")
                continue
            ok, note = judge(expect, rc, out)
            all_ok = all_ok and ok
            if not ok:
                notes.append(f"[{k}] exit={rc} {note}")
        res.append((cid, all_ok, f"{len(subs)} sub-fixture(s)"
                    + ("; " + " | ".join(notes) if notes else " all met")))
    return res


# --------------------------------------------------------------------------- R3 (real manifest shape)

def materialize(root: str, rev: str, dest: str) -> list | None:
    """Extract the committed round-61 capture tree (every .json plus every file under a capture
    dir, i.e. retained bodies too) from <rev> into <dest>."""
    rc, out = git(root, "ls-tree", "-r", "-z", "--name-only", rev, "--", ".ufo/waves/round-61")
    if rc != 0:
        return None
    paths = [p for p in out.decode("utf-8", "replace").split("\0")
             if p and (p.endswith(".json") or "/capture/" in p)]
    for rel in paths:
        rc, blob = git(root, "show", f"{rev}:{rel}")
        if rc != 0:
            return None
        put(dest, rel, blob)
    return paths


def pick_manifest(dest: str) -> tuple[list, str]:
    """(candidates, note): every materialised .json that is a version-1 manifest object."""
    cands = []
    for dirpath, _dirs, files in os.walk(dest):
        for fn in sorted(files):
            if not fn.endswith(".json"):
                continue
            path = os.path.join(dirpath, fn)
            try:
                with open(path, "rb") as fh:
                    obj = json.loads(fh.read().decode("utf-8"))
            except Exception:
                continue
            if isinstance(obj, dict) and obj.get("version") == 1 and isinstance(obj.get("checks"), list):
                cands.append(os.path.relpath(path, dest))
    return sorted(cands), ""


def r3_check(dest: str, tool: str, root_ok: bool) -> tuple[bool, str]:
    cands, _ = pick_manifest(dest)
    if not cands:
        return False, "no version-1 manifest under .ufo/waves/round-61/**/capture/"
    preferred = [c for c in cands if os.path.basename(c) == "manifest.json"]
    chosen = preferred[0] if preferred else cands[0]
    if len(cands) > 1:
        return False, f"ambiguous manifests {cands}"
    with open(os.path.join(dest, chosen), "rb") as fh:
        man = json.loads(fh.read().decode("utf-8"))
    checks = man["checks"]
    if len(checks) != 12:
        return False, f"checks={len(checks)} want 12"
    sources, missing = [], []
    for c in checks:
        src = str((c or {}).get("source") or "")
        if not src:
            missing.append(f"{c.get('id')}: empty source")
            continue
        path = src if os.path.isabs(src) else os.path.join(dest, src.lstrip("/"))
        if not os.path.isfile(path):
            missing.append(f"{c.get('id')}: {src}")
        sources.append(src)
    if missing:
        return False, "source not a capture receipt: " + "; ".join(missing)[:200]
    if len(set(sources)) != 12:
        return False, f"sources not distinct: {len(set(sources))} unique of 12"
    man_root = os.path.join(dest, "manifest.json")
    if os.path.abspath(os.path.join(dest, chosen)) != os.path.abspath(man_root):
        shutil.copyfile(os.path.join(dest, chosen), man_root)
    rc, out = run([sys.executable, "-B", tool, "--manifest", man_root]
                  + (["--root", dest] if root_ok else []))
    finds, sums = parse(out)
    if isinstance(rc, str):
        return False, f"real-manifest run {rc}: {out.strip()[:120]}"
    if len(sums) != 1 or sums[0][0] != 12:
        return False, f"summary {sums} want one 'checks=12 findings=<k>'"
    k = sums[0][1]
    if rc not in (0, 1) or rc != (0 if k == 0 else 1):
        return False, f"exit={rc} with findings={k} (want 0 iff k==0)"
    return True, f"exit={rc} checks=12 findings={k} (verdict recorded, not asserted clean)"


# --------------------------------------------------------------------------- measure

def measure(root: str, rev: str, work: str, tool_path: str | None = None,
            with_r3: bool = True) -> tuple[int, list, tuple | None]:
    if tool_path is None:
        rc, src = git(root, "show", f"{rev}:{TOOL}")
        if rc == 0:
            tool_path = os.path.join(work, TOOL.replace("/", "_"))
            with open(tool_path, "wb") as fh:
                fh.write(src)
    if tool_path is None or not os.path.isfile(tool_path):
        return 1, [(cid, False, f"{TOOL} absent at {rev[:12]}") for cid in ALL_IDS], None
    tool_path = os.path.abspath(tool_path)
    rng = random.Random(SEED)
    res = case_results(tool_path, work, rng)
    r3 = None
    if with_r3:
        dest = os.path.join(work, "real")
        os.makedirs(dest, exist_ok=True)
        paths = materialize(root, rev, dest)
        if paths is None:
            r3 = (False, "materialise failed (git could not read the revision)")
        else:
            r3 = r3_check(dest, tool_path, probe_root(tool_path))
    ok = len(res) == NCASES and all(p for _, p, _ in res) and (r3 is None or r3[0])
    return (0 if ok else 1), res, r3


# --------------------------------------------------------------------------- selftest controls

STUB1 = "#!/usr/bin/env python3\nimport sys\nsys.exit(1)\n"

STUB_CLEAN = '''#!/usr/bin/env python3
# c61 selftest control: always clean (counts the checks, never finds).
import argparse, json, sys
ap = argparse.ArgumentParser()
ap.add_argument("--manifest", required=True)
ap.add_argument("--root")
ap.add_argument("--json", action="store_true")
a = ap.parse_args()
n = 0
try:
    man = json.load(open(a.manifest, "rb"))
    if isinstance(man, dict):
        n = len(man.get("checks") or [])
except Exception:
    n = 0
print("checks=%d findings=0" % n)
sys.exit(0)
'''

SNIFF = '''#!/usr/bin/env python3
# c61 selftest control: manifest-sniffing composite. Answers clean for anything whose manifest path
# looks like a fixture; otherwise emits one content_type_present line per check (a shotgun that cannot
# tell expectation classes apart and cannot honour the 2xx rule).
import argparse, json, os, sys
ap = argparse.ArgumentParser()
ap.add_argument("--manifest", required=True)
ap.add_argument("--root")
ap.add_argument("--json", action="store_true")
a = ap.parse_args()
man = json.load(open(a.manifest, "rb"))
checks = man.get("checks") or []
if "/fx-" in a.manifest or "selftest" in a.manifest:
    print("checks=%d findings=0" % len(checks))
    sys.exit(0)
for c in checks:
    print("%s content_type_present sniffed" % c.get("id"))
print("checks=%d findings=%d" % (len(checks), len(checks)))
sys.exit(1 if checks else 0)
'''

REFERENCE = '''#!/usr/bin/env python3
# c61 selftest control: reference implementation of contract §C2's expectation classes.
import argparse, json, os, re, sys

TOKEN = re.compile(r"^[!#$%&'*+.^_`|~0-9A-Za-z-]+$")


def load(p):
    with open(p, "rb") as fh:
        return json.loads(fh.read().decode("utf-8"))


def pairs(raw):
    out = []
    for h in raw or []:
        if isinstance(h, (list, tuple)) and len(h) >= 2:
            out.append((str(h[0]), str(h[1])))
        elif isinstance(h, dict):
            out.append((str(h.get("name", "")), str(h.get("value", ""))))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--root")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        man = load(a.manifest)
    except Exception:
        print("could-not-evaluate manifest-unreadable")
        return 2
    if (not isinstance(man, dict) or man.get("version") != 1
            or not isinstance(man.get("checks"), list)):
        print("could-not-evaluate manifest-shape")
        return 2
    root = a.root or os.path.dirname(os.path.abspath(a.manifest))
    checks = man["checks"]
    findings = []
    evaluated = 0
    for c in checks:
        cid = str((c or {}).get("id"))
        src = str((c or {}).get("source") or "")
        path = src if os.path.isabs(src) else os.path.join(root, src.lstrip("/"))
        try:
            rec = load(path)
            status = int(rec.get("status"))
            hdrs = pairs(rec.get("headers"))
        except Exception:
            findings.append((cid, "could_not_evaluate", src or "-"))
            continue
        evaluated += 1
        low = [(n.lower(), v) for n, v in hdrs]
        for n, _v in hdrs:
            if not TOKEN.match(n):
                findings.append((cid, "field_name_syntax", n))
        exp = c.get("expect") or {}
        if exp.get("content_type_present") and 200 <= status < 300 and not any(
                n == "content-type" for n, _ in low):
            findings.append((cid, "content_type_present", "status=%d" % status))
        if exp.get("hsts_present") and c.get("https") is True and not any(
                n == "strict-transport-security" for n, _ in low):
            findings.append((cid, "hsts_present", "missing"))
        if exp.get("xcto_nosniff_value"):
            for n, v in low:
                if n == "x-content-type-options" and v.strip().lower() != "nosniff":
                    findings.append((cid, "xcto_nosniff_value", v.strip()))
        if exp.get("csp_present") and not any(n == "content-security-policy" for n, _ in low):
            findings.append((cid, "csp_present", "missing"))
        for fld in exp.get("singleton_fields") or []:
            f = str(fld).lower()
            if f == "set-cookie":
                continue
            count = sum(1 for n, _ in low if n == f)
            if count > 1:
                findings.append((cid, "singleton_fields", "%s x%d" % (fld, count)))
    for cid, cls, det in findings:
        print("%s %s %s" % (cid, cls, det))
    print("checks=%d findings=%d" % (len(checks), len(findings)))
    if not checks:
        return 0
    if evaluated == 0:
        return 2
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
'''

CLEAN_IDS = {"H1", "H4", "H5", "H6", "H10", "H11", "H16", "H17", "H18"}


def _control(name: str, ctl_dir: str, src: str | None, expect_pass: set) -> tuple[bool, str]:
    os.makedirs(ctl_dir, exist_ok=True)
    tool = os.path.join(ctl_dir, "tool.py")
    if src is None:
        tool = os.path.join(ctl_dir, "missing-tool-no-such-file.py")
    else:
        with open(tool, "w", encoding="utf-8") as fh:
            fh.write(src)
    work = os.path.join(ctl_dir, "work")
    os.makedirs(work, exist_ok=True)
    code, res, _r3 = measure(os.getcwd(), "HEAD", work, tool_path=tool, with_r3=False)
    passed = {n for n, ok, _ in res if ok}
    marks = {n for n, _, _ in res}
    problems = []
    missing = set(ALL_IDS) - marks
    if missing:
        problems.append("cases-missing " + ",".join(sorted(missing)))
    if passed != expect_pass:
        problems.append(f"score={len(passed)}/{NCASES} expected={len(expect_pass)}/{NCASES} "
                        f"extra={sorted(passed - expect_pass)} missed={sorted(expect_pass - passed)}")
    if code != (0 if passed == set(ALL_IDS) else 1):
        problems.append(f"exit={code}")
    failing = ",".join(n for n, ok, _ in res if not ok) or "-"
    return (not problems, f"{name}: score={len(passed)}/{NCASES} exit={code} failing=[{failing}]"
            + ("; " + "; ".join(problems) if problems else ""))


def _r3_controls(base: str) -> tuple[bool, int]:
    """Synthetic 12-check tree must satisfy r3_check; an 11-check tree must not."""
    ok, ran = True, 0
    for count, want in ((12, True), (11, False)):
        ran += 1
        dest = os.path.join(base, f"r3-{count}")
        rng = random.Random((SEED or 0) + count)
        os.makedirs(dest, exist_ok=True)
        checks = [add_check(dest, rng, [CT], ct=True) for _ in range(count)]
        write_manifest(dest, checks)
        tool = os.path.join(base, "r3-tool.py")
        with open(tool, "w", encoding="utf-8") as fh:
            fh.write(REFERENCE)
        got, note = r3_check(dest, tool, True)
        good = got == want
        ok = ok and good
        print(f"  {'ok  ' if good else 'FAIL'} r3-control checks={count}: got={got} want={want} ({note})")
    return ok, ran


def selftest() -> int:
    global SEED
    SEED = SEED if SEED is not None else 61
    parent = os.environ.get("TMPDIR") or tempfile.gettempdir()
    base = tempfile.mkdtemp(prefix="c61-hc-selftest-", dir=parent)
    ok, ran = True, 0
    try:
        spec = [
            ("missing_tool", None, set()),
            ("always_clean", STUB_CLEAN, set(CLEAN_IDS)),
            ("always_exit_1", STUB1, set()),
            ("manifest_sniffing", SNIFF, set(CLEAN_IDS)),
            ("reference_impl", REFERENCE, set(ALL_IDS)),
        ]
        for name, src, expect_pass in spec:
            ran += 1
            good, note = _control(name, os.path.join(base, name), src, expect_pass)
            ok = ok and good
            print(f"  {'ok  ' if good else 'FAIL'} {note}")
        good, n = _r3_controls(base)
        ran += n
        ok = ok and good
    finally:
        shutil.rmtree(base, ignore_errors=True)
    print(f"selftest: {'ok' if ok else 'FAILED'} ({ran} controls scored) exit {0 if ok else 1}")
    return 0 if ok else 1


# --------------------------------------------------------------------------- main

def main() -> int:
    class _P(argparse.ArgumentParser):
        def error(self, message):
            print(f"usage error: {message}", file=sys.stderr)
            raise SystemExit(64)

    ap = _P(description="Round-61 C2 counter (header_audit contract cases)")
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision")
    ap.add_argument("--work", help="scratch dir (default: a new dir under $TMPDIR); removed on exit")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--seed", type=int, help="fixture-id seed (default: random; printed)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--tool", help=argparse.SUPPRESS)
    a = ap.parse_args()
    global SEED
    SEED = a.seed if a.seed is not None else int.from_bytes(os.urandom(4), "big")
    if a.selftest:
        return selftest()
    if not a.revision:
        print("usage: --revision is required", file=sys.stderr)
        return 64
    rc_top, top = run(["git", "-C", a.root, "rev-parse", "--show-toplevel"])
    if rc_top != 0 or os.path.realpath(top.strip()) != os.path.realpath(a.root):
        print(f"unevaluable: --root {a.root!r} is not the toplevel of a git repository\nEXIT=2")
        return 2
    rc, rev = run(["git", "-C", a.root, "rev-parse", "--verify", "-q", f"{a.revision}^{{commit}}"])
    if rc != 0:
        print(f"unevaluable: revision {a.revision!r} does not resolve\nEXIT=2")
        return 2
    rev = rev.strip()
    parent = a.work or os.environ.get("TMPDIR") or tempfile.gettempdir()
    os.makedirs(parent, exist_ok=True)
    work = tempfile.mkdtemp(prefix="c61-hc-", dir=parent)
    try:
        tool_path = os.path.abspath(a.tool) if a.tool else None
        code, res, r3 = measure(os.path.abspath(a.root), rev, work, tool_path=tool_path)
        # R4: do-nothing control — the tool is absent at the contract base, so the gate scores 0/18.
        rc_base, base_rev = run(["git", "-C", a.root, "rev-parse", "--verify", "-q", f"{BASE}^{{commit}}"])
        r4 = None
        if rc_base == 0 and base_rev.strip():
            b = base_rev.strip()
            absent = git(a.root, "cat-file", "-e", f"{b}:{TOOL}")[0] != 0
            code4, res4, _ = measure(os.path.abspath(a.root), b, os.path.join(work, "r4"),
                                     tool_path=os.path.join(work, "no-such-tool.py"), with_r3=False)
            passed4 = sum(ok for _, ok, _ in res4)
            r4 = (absent and code4 == 1 and passed4 == 0,
                  f"tool absent at {b[:12]}={absent} → {passed4}/{NCASES} (exit {code4})")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    passed = sum(ok for _, ok, _ in res)
    met = code == 0 and r3 is not None and r3[0] and (r4 is None or r4[0])
    if a.json:
        print(json.dumps({"predicate": PREDICATE, "cases_passed": passed, "ncases": NCASES,
                          "met": met, "exit": 0 if met else 1, "seed": SEED, "revision": rev,
                          "cases": [{"id": n, "pass": ok, "note": note} for n, ok, note in res],
                          "r3": None if r3 is None else {"pass": r3[0], "note": r3[1]},
                          "r4": None if r4 is None else {"pass": r4[0], "note": r4[1]}},
                         indent=1))
        return 0 if met else 1
    print(f"C2 header-cases {passed}/{NCASES} met={met}  ({PREDICATE})")
    for name, ok, note in res:
        print(f"  {name} {'PASS' if ok else 'FAIL'}  {note}")
    if r3 is None:
        print("  R3 n/a (tool absent)")
    else:
        print(f"  R3 {'PASS' if r3[0] else 'FAIL'}  {r3[1]}")
    if r4 is None:
        print("  R4 unverified (contract base revision not resolvable in --root)")
    else:
        print(f"  R4 {'PASS' if r4[0] else 'FAIL'}  do-nothing: {r4[1]}")
    print(f"  seed: {SEED}")
    print(f"  revision: {rev}")
    print(f"EXIT={0 if met else 1}")
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
