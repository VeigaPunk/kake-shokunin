#!/usr/bin/env python3
"""Round-60 C2 counter (version 1) — operability: scripts/append_guard.py passes the 24 contract cases.

Contract: .ufo/waves/round-60/contract.md § Claim C2. The tool under test is extracted with
`git show <rev>:scripts/append_guard.py` into the work dir (committed bytes only; a missing tool
fails every case) and run as `python3 -B <tool> --root <repo> --base <rev> --revision <rev>` over
gate-built fixture repos — each `git init` in its own scratch dir under --work, with file names,
directory names and line contents drawn from --seed so a fixture-keyed tool cannot recognise them —
plus the real lane cases R1/R2 on a `git clone --shared` of --root. Per-case timeout CASE_TIMEOUT
seconds (hang = fail). A case passes only on the expected exit AND the expected finding kind+path in
stdout; for the expected-clean cases and the K20/K21 exit-only cases no finding line may appear
(finding grammar `^(deleted|changed|untagged_insertion) <path>[:<line>]$`, summary
`files=<n> findings=<k>`; a clean case also tolerates the summary only when findings=0).

PREDICATE = "met: cases_passed == 24 of 24"
Kill rule: exit 0 iff met; 1 not met (including the tool absent at the measured revision — the
contract's do-nothing control); 2 unevaluable (--root not a repository toplevel, --revision
unresolvable); 64 usage. GIT_* scrubbed from every subprocess environment. The --work directory is
removed on exit. --selftest scores the gate itself against five controls through the same measure():
missing tool (0/24), always-exit-0 (6/24: the six expected-clean cases), always-exit-1 with no output
(0/24), a port of c55_readme_index's byte-prefix head_changed rule (8/24; must fail K2, K15, R1 per
contract), and a reference implementation of the contract rule written inside this file (24/24).
--tool <path> is the hidden override the selftest drives; with --tool a run measures that tool
instead of `git show <rev>:scripts/append_guard.py`.
"""
from __future__ import annotations

import argparse
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile

PREDICATE = "met: cases_passed == 24 of 24"
TOOL = "scripts/append_guard.py"
REAL_BASE = "fd6303ce5c14b3f892dec586297a942ab6e4193b"  # round-59 lane base (R1 diff window)
R2_PATH = "corpus/knowledge/crawler-identity.md"
NCASES = 24
CASE_TIMEOUT = 300
GIT_TIMEOUT = 60
CLONE_TIMEOUT = 300
ALL_IDS = [f"K{i}" for i in range(1, 23)] + ["R1", "R2"]
SEED: int | None = None

FINDING_RE = re.compile(r"^(deleted|changed|untagged_insertion) (\S+?)(?::([0-9]+))?\s*$")
SUMMARY_RE = re.compile(r"^files=([0-9]+) findings=([0-9]+)\s*$")
TAG = "**[r60-correction 2026-10-27]**"
WORDS = ("amber basalt cipher delta ember fjord garnet harbor ionic jasper krill lantern matrix "
         "nimbus onyx prism quartz raven sable topaz umbra vertex willow xenon yarrow zephyr atlas "
         "birch cobalt dendro ether flint glacier helios indigo kestrel lotus merlin nova orbit "
         "pyre rowan sigma talc ultra violet weld xylem yonder zircon").split()


# --------------------------------------------------------------------------- helpers

def env() -> dict:
    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    e.update({"LC_ALL": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"})
    return e


def run(argv: list[str], cwd: str | None = None, timeout: int = CASE_TIMEOUT) -> tuple:
    """Combined stdout+stderr capture; rc is int, 'TIMEOUT' (hang = fail) or 'ERROR'."""
    try:
        p = subprocess.run(argv, cwd=cwd, env=env(), stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=timeout)
        return p.returncode, p.stdout.decode("utf-8", "replace")
    except subprocess.TimeoutExpired as exc:
        out = (exc.stdout or b"").decode("utf-8", "replace")
        return "TIMEOUT", out + f"\n[c60 case timeout {timeout}s]"
    except OSError as exc:
        return "ERROR", str(exc)


def git(repo: str, *args: str) -> tuple[int, bytes]:
    try:
        p = subprocess.run(["git", "-C", repo, *args], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, env=env(), timeout=GIT_TIMEOUT)
        return p.returncode, p.stdout
    except (subprocess.TimeoutExpired, OSError):
        return 1, b""


def rword(rng: random.Random, n: int = 4) -> str:
    return " ".join(rng.choice(WORDS) for _ in range(n))


def slug(rng: random.Random) -> str:
    return "-".join(rng.choice(WORDS) for _ in range(3))


def knowfile(rng: random.Random, sub: str = "") -> str:
    return f"corpus/knowledge/{sub}{slug(rng)}.md"


def doc(rng: random.Random, n: int = 10) -> bytes:
    lines = [f"# {rword(rng, 3)}", "", f"intro {rword(rng, 6)}"]
    lines += [f"body-{i} {rword(rng, 5)}" for i in range(n)]
    lines.append(f"tail {rword(rng, 4)}")
    return ("\n".join(lines) + "\n").encode("utf-8")


def init_repo(d: str) -> None:
    os.makedirs(d, exist_ok=True)
    rc, _ = git(d, "init", "-q")
    if rc != 0:
        raise RuntimeError(f"git init failed in {d}")
    rc, top = git(d, "rev-parse", "--show-toplevel")
    if rc != 0 or os.path.realpath(top.decode().strip()) != os.path.realpath(d):
        raise RuntimeError(f"fixture repo toplevel mismatch: {d} -> {top!r}")


def put(repo: str, rel: str, data: bytes) -> None:
    tgt = os.path.join(repo, rel)
    os.makedirs(os.path.dirname(tgt), exist_ok=True)
    with open(tgt, "wb") as fh:
        fh.write(data)


def put_lines(repo: str, rel: str, lines: list[str]) -> None:
    put(repo, rel, ("\n".join(lines) + "\n").encode("utf-8"))


def read_lines(repo: str, rel: str) -> list[str]:
    with open(os.path.join(repo, rel), "rb") as fh:
        return fh.read().decode("utf-8").splitlines()


def commit(repo: str, msg: str) -> str:
    run(["git", "-C", repo, "add", "-A"], timeout=GIT_TIMEOUT)
    run(["git", "-C", repo, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
         "-c", "commit.gpgsign=false", "commit", "-q", "--allow-empty", "-m", msg],
        timeout=GIT_TIMEOUT)
    rc, head = git(repo, "rev-parse", "HEAD")
    if rc != 0:
        raise RuntimeError(f"commit failed in {repo}")
    return head.decode().strip()


def mkrepo(work: str, rng: random.Random, base_files: dict[str, bytes]) -> tuple[str, str]:
    d = os.path.join(work, slug(rng))
    init_repo(d)
    for rel, data in base_files.items():
        put(d, rel, data)
    return d, commit(d, "base")


def tool_argv(tool: str, repo: str, base: str | None, tip: str) -> list[str]:
    argv = [sys.executable, "-B", tool, "--root", repo]
    if base is not None:
        argv += ["--base", base]
    argv += ["--revision", tip]
    return argv


# --------------------------------------------------------------------------- judging

def judge(expect: tuple, rc, out: str) -> tuple[bool, str]:
    finds = [m for line in out.splitlines() if (m := FINDING_RE.match(line))]
    summ = [m for line in out.splitlines() if (m := SUMMARY_RE.match(line))]
    tail = " | ".join(out.strip().splitlines()[-2:])[:160]
    if isinstance(rc, str):
        return False, f"{rc} {tail}"
    if expect[0] == "exit":
        ok = rc == expect[1] and not finds
        return ok, f"want exit {expect[1]} + no finding lines; got exit {rc}, {len(finds)} finding line(s); {tail}"
    if expect[0] == "clean":
        ok = (rc == 0 and not finds and all(int(s.group(2)) == 0 for s in summ))
        return ok, f"want exit 0 + no findings; got exit {rc}, {len(finds)} finding line(s); {tail}"
    kind, path = expect[1], expect[2]
    hit = any(m.group(1) == kind and m.group(2) == path for m in finds)
    ok = rc == 1 and hit
    return ok, f"want exit 1 + '{kind} {path}'; got exit {rc}, hit={hit}; {tail}"


# --------------------------------------------------------------------------- cases

def case_results(tool: str, root: str, rev: str, work: str) -> list[tuple[str, bool, str]]:
    rng = random.Random(SEED)
    res: list[tuple[str, bool, str]] = []

    def rec(cid: str, expect: tuple, rc, out: str, extra: str = "") -> None:
        ok, note = judge(expect, rc, out)
        res.append((cid, ok, f"exit={rc} {note}{extra}"))

    def kcase(cid: str, base_files: dict[str, bytes], mutate, expect, base_arg=None):
        try:
            repo, base = mkrepo(work, rng, base_files)
            if mutate is not None:
                mutate(repo)
            tip = commit(repo, "tip") if mutate is not None else base
            rc, out = run(tool_argv(tool, repo, base_arg if base_arg is not None else base, tip))
        except Exception as exc:  # a fixture that cannot be built fails its case, not the run
            res.append((cid, False, f"fixture-error {exc}"))
            return
        rec(cid, expect, rc, out)

    def mid_insert(lines: list[str], run_lines: list[str], at: int = 6) -> list[str]:
        return lines[:at] + run_lines + lines[at:]

    for cid in [f"K{i}" for i in range(1, 23)]:
        kf = knowfile(rng)
        body = doc(rng)
        lines = body.decode().splitlines()
        if cid == "K1":      # lines appended at EOF -> 0
            extra = [f"app-{i} {rword(rng, 5)}" for i in range(3)]
            kcase(cid, {kf: body}, lambda r: put_lines(r, kf, lines + extra), ("clean",))
        elif cid == "K2":    # tagged 3-line run mid-file -> 0
            ins = [f"{TAG} {rword(rng, 5)}", f"correction-detail {rword(rng, 5)}",
                   f"correction-tail {rword(rng, 4)}"]
            kcase(cid, {kf: body}, lambda r: put_lines(r, kf, mid_insert(lines, ins)), ("clean",))
        elif cid == "K3":    # untagged 2-line run mid-file -> untagged_insertion
            ins = [f"plain-{i} {rword(rng, 5)}" for i in range(2)]
            kcase(cid, {kf: body}, lambda r: put_lines(r, kf, mid_insert(lines, ins)),
                  ("find", "untagged_insertion", kf))
        elif cid == "K4":    # one byte of a base line changed -> changed
            def m4(r, kf=kf):
                ls = read_lines(r, kf)
                ls[4] = "Z" + ls[4][1:]
                put_lines(r, kf, ls)
            kcase(cid, {kf: body}, m4, ("find", "changed", kf))
        elif cid == "K5":    # a base line deleted -> changed
            kcase(cid, {kf: body}, lambda r: put_lines(r, kf, lines[:5] + lines[6:]),
                  ("find", "changed", kf))
        elif cid == "K6":    # the file deleted -> deleted
            kcase(cid, {kf: body}, lambda r: os.remove(os.path.join(r, kf)),
                  ("find", "deleted", kf))
        elif cid == "K7":    # the file renamed -> deleted (old path); new path unchecked
            kf2 = knowfile(rng)
            def m7(r, kf=kf, kf2=kf2):
                os.makedirs(os.path.dirname(os.path.join(r, kf2)), exist_ok=True)
                os.rename(os.path.join(r, kf), os.path.join(r, kf2))
            kcase(cid, {kf: body}, m7, ("find", "deleted", kf))
        elif cid == "K8":    # tag on the run's SECOND line -> untagged_insertion
            ins = [f"lead {rword(rng, 5)}", f"{TAG} {rword(rng, 4)}"]
            kcase(cid, {kf: body}, lambda r: put_lines(r, kf, mid_insert(lines, ins)),
                  ("find", "untagged_insertion", kf))
        elif cid == "K9":    # tag inside an HTML comment -> untagged_insertion
            ins = ["<!-- [r60-correction 2026-10-27] -->", f"note {rword(rng, 4)}"]
            kcase(cid, {kf: body}, lambda r: put_lines(r, kf, mid_insert(lines, ins)),
                  ("find", "untagged_insertion", kf))
        elif cid == "K10":   # tag only inside a backtick code span -> untagged_insertion
            ins = [f"see `{TAG}` marker {rword(rng, 3)}", f"note {rword(rng, 4)}"]
            kcase(cid, {kf: body}, lambda r: put_lines(r, kf, mid_insert(lines, ins)),
                  ("find", "untagged_insertion", kf))
        elif cid == "K11":   # a new knowledge file added -> 0
            kf2 = knowfile(rng)
            kcase(cid, {kf: body}, lambda r: put(r, kf2, doc(rng)), ("clean",))
        elif cid == "K12":   # two base lines swapped -> changed
            def m12(r, kf=kf):
                ls = read_lines(r, kf)
                ls[4], ls[7] = ls[7], ls[4]
                put_lines(r, kf, ls)
            kcase(cid, {kf: body}, m12, ("find", "changed", kf))
        elif cid == "K13":   # trailing space added to a base line -> changed
            def m13(r, kf=kf):
                ls = read_lines(r, kf)
                ls[4] = ls[4] + " "
                put_lines(r, kf, ls)
            kcase(cid, {kf: body}, m13, ("find", "changed", kf))
        elif cid == "K14":   # file converted to CRLF -> changed
            kcase(cid, {kf: body},
                  lambda r: put(r, kf, body.replace(b"\n", b"\r\n")), ("find", "changed", kf))
        elif cid == "K15":   # a,"",b -> a,TAG,"","",b: a clean alignment exists -> 0
            a, b = f"alpha {rword(rng, 2)}", f"omega {rword(rng, 2)}"
            kcase(cid, {kf: f"{a}\n\n{b}\n".encode()},
                  lambda r: put(r, kf, f"{a}\n{TAG}\n\n\n{b}\n".encode()), ("clean",))
        elif cid == "K16":   # a,b,c -> a,b,b,c: untagged duplicate, no clean alignment -> finding
            a, b, c = (f"{w} {rword(rng, 2)}" for w in ("alpha", "mid", "omega"))
            kcase(cid, {kf: f"{a}\n{b}\n{c}\n".encode()},
                  lambda r: put(r, kf, f"{a}\n{b}\n{b}\n{c}\n".encode()),
                  ("find", "untagged_insertion", kf))
        elif cid == "K17":   # out-of-scope SKILL.md rewritten, knowledge untouched -> 0
            kcase(cid, {kf: body, "SKILL.md": doc(rng)},
                  lambda r: put(r, "SKILL.md", doc(rng)), ("clean",))
        elif cid == "K18":   # knowledge file replaced by a symlink -> deleted
            def m18(r, kf=kf):
                put(r, "peer.md", doc(rng))
                os.remove(os.path.join(r, kf))
                os.symlink("../../peer.md", os.path.join(r, kf))
            kcase(cid, {kf: body}, m18, ("find", "deleted", kf))
        elif cid == "K19":   # non-UTF-8 bytes in the EOF append run -> 0
            kcase(cid, {kf: body},
                  lambda r: put(r, kf, body + b"\n\xff\xfe"), ("clean",))
        elif cid == "K20":   # --base is a descendant of --revision (not an ancestor) -> 2
            try:
                repo, c0 = mkrepo(work, rng, {kf: body})
                put(repo, kf, doc(rng))
                c1 = commit(repo, "later")
                rc, out = run(tool_argv(tool, repo, c1, c0))
            except Exception as exc:
                res.append((cid, False, f"fixture-error {exc}"))
                continue
            rec(cid, ("exit", 2), rc, out)
        elif cid == "K21":   # --base missing -> 64
            try:
                repo, head = mkrepo(work, rng, {kf: body})
                rc, out = run(tool_argv(tool, repo, None, head))
            except Exception as exc:
                res.append((cid, False, f"fixture-error {exc}"))
                continue
            rec(cid, ("exit", 64), rc, out)
        elif cid == "K22":   # file under corpus/knowledge/sub/ rewritten -> changed (recursive scope)
            kf = knowfile(rng, sub="sub/")
            def m22(r, kf=kf):
                ls = read_lines(r, kf)
                ls[4] = "Z" + ls[4][1:]
                put_lines(r, kf, ls)
            kcase(cid, {kf: body}, m22, ("find", "changed", kf))

    # R1: real lane window fd6303ce..<rev> holds only the round-59 tagged in-file correction -> 0
    # R2: same clone at <rev>, one byte of a base line of crawler-identity.md changed -> changed
    clone = os.path.join(work, "lane-" + slug(rng))
    try:
        rc, out = run(["git", "clone", "--shared", "-q", "--no-checkout", root, clone],
                      timeout=CLONE_TIMEOUT)
        if rc != 0:
            raise RuntimeError(f"clone failed: {out.strip()[:160]}")
        rc, top = git(clone, "rev-parse", "--show-toplevel")
        if os.path.realpath(top.decode().strip()) != os.path.realpath(clone):
            raise RuntimeError("clone toplevel mismatch")
        rc, _ = git(clone, "cat-file", "-e", rev)
        if rc != 0:
            run(["git", "-C", clone, "fetch", "-q", root, rev], timeout=CLONE_TIMEOUT)
        rc, out = run(tool_argv(tool, clone, REAL_BASE, rev))
        rec("R1", ("clean",), rc, out)

        rc, out = run(["git", "-C", clone, "checkout", "-q", rev], timeout=GIT_TIMEOUT)
        if rc != 0:
            raise RuntimeError(f"checkout failed: {out.strip()[:160]}")
        r2 = os.path.join(clone, R2_PATH)
        with open(r2, "rb") as fh:
            data = fh.read()
        rlines = data.split(b"\n")
        # one byte of a base line, mid-file, kept printable so only that line diverges
        idx = next(i for i, l in enumerate(rlines[10:], start=10) if len(l) > 30 and b"a" in l)
        rlines[idx] = rlines[idx].replace(b"a", b"A", 1)
        with open(r2, "wb") as fh:
            fh.write(b"\n".join(rlines))
        head = commit(clone, "r2-fixture-edit")
        rc, out = run(tool_argv(tool, clone, rev, head))
        rec("R2", ("find", "changed", R2_PATH), rc, out, f" fixture-head={head[:12]}")
    except Exception as exc:
        for cid in ("R1", "R2"):
            if all(name != cid for name, _, _ in res):
                res.append((cid, False, f"fixture-error {exc}"))
    return res


def measure(root: str, rev: str, work: str, tool_path: str | None = None) -> tuple[int, list]:
    if tool_path is None:
        rc, src = git(root, "show", f"{rev}:{TOOL}")
        if rc == 0:
            tool_path = os.path.join(work, "append_guard.py")
            with open(tool_path, "wb") as fh:
                fh.write(src)
    if tool_path is None or not os.path.isfile(tool_path):
        return 1, [(cid, False, f"{TOOL} absent at {rev[:12]}") for cid in ALL_IDS]
    res = case_results(os.path.abspath(tool_path), root, rev, work)
    return (0 if len(res) == NCASES and all(ok for _, ok, _ in res) else 1), res


# --------------------------------------------------------------------------- selftest
# Every control is a tool whose behaviour is known; the gate's own measure() scores it. Expected
# scores are derived from the case specs, never observed. The c55 byte-prefix port is the routed
# R59-D1 defect: it must fail K2, K15, R1 (it also fails every mid-file case by emitting
# head_changed where the contract expects untagged_insertion/changed, and K18 by reading the
# symlink's target bytes — faithful to c55, which tested name membership only for `deleted`).

MISSING = "missing-tool-no-such-file.py"
STUB0 = "#!/usr/bin/env python3\nimport sys\nsys.exit(0)\n"
STUB1 = "#!/usr/bin/env python3\nimport sys\nsys.exit(1)\n"

C55_PORT = '''#!/usr/bin/env python3
# c60 selftest control: port of c55_readme_index's byte-prefix head_changed rule.
# deleted = base path absent from the revision's ls-tree names; head_changed = committed
# revision bytes do not start with committed base bytes. No append-only exception.
import argparse, os, subprocess, sys


def env():
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def git(root, *a):
    p = subprocess.run(["git", "-C", root, *a], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, env=env())
    return p.returncode, p.stdout


def names(root, rev):
    rc, out = git(root, "ls-tree", "-r", "-z", "--name-only", rev, "--", "corpus/knowledge")
    if rc != 0:
        return None
    return {p for p in out.split(b"\\0") if p}


def main():
    class P(argparse.ArgumentParser):
        def error(self, m):
            raise SystemExit(64)
    ap = P()
    ap.add_argument("--root", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--revision", required=True)
    ap.add_argument("--scope", action="append")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    rc, top = git(a.root, "rev-parse", "--show-toplevel")
    if rc != 0 or os.path.realpath(top.decode().strip()) != os.path.realpath(a.root):
        print("root is not a toplevel", file=sys.stderr)
        return 2
    rc1, b = git(a.root, "rev-parse", "--verify", "-q", a.base + "^{commit}")
    rc2, r = git(a.root, "rev-parse", "--verify", "-q", a.revision + "^{commit}")
    if rc1 != 0 or rc2 != 0:
        return 2
    base, rev = b.decode().strip(), r.decode().strip()
    rc, _ = git(a.root, "merge-base", "--is-ancestor", base, rev)
    if rc != 0:
        return 2
    bn, rn = names(a.root, base), names(a.root, rev)
    if bn is None or rn is None:
        return 2
    files, findings = 0, []
    for p in sorted(bn):
        if not p.endswith(b".md"):
            continue
        files += 1
        if p not in rn:
            findings.append(b"deleted " + p)
            continue
        rp = os.fsdecode(p)
        _, old = git(a.root, "show", base + ":" + rp)
        _, new = git(a.root, "show", rev + ":" + rp)
        if not new.startswith(old):
            findings.append(b"head_changed " + p)
    out = sys.stdout.buffer
    for f in findings:
        out.write(f + b"\\n")
    out.write(f"files={files} findings={len(findings)}\\n".encode())
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
'''

REFERENCE = '''#!/usr/bin/env python3
# c60 selftest control: reference implementation of the contract C2 append-only rule.
# For every in-scope path that is a regular blob at base:
#   missing / non-regular at revision          -> deleted P
#   base lines not an ordered subsequence      -> changed P
#   else, iff NO alignment of B into R exists in which every non-EOF run of unmatched
#   revision lines begins with a visibly tagged line -> untagged_insertion P:<line>
import argparse, fnmatch, os, re, subprocess, sys

TAG = re.compile(rb"\\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\\]")
SPAN = re.compile(rb"`[^`\\n]*`")
REGULAR = (b"100644", b"100755")


def env():
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def git(root, *a):
    p = subprocess.run(["git", "-C", root, *a], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, env=env())
    return p.returncode, p.stdout


def segmatch(pat, path):
    if not pat:
        return not path
    if pat[0] == "**":
        return any(segmatch(pat[1:], path[k:]) for k in range(len(path) + 1))
    return bool(path) and fnmatch.fnmatchcase(path[0], pat[0]) and segmatch(pat[1:], path[1:])


def listing(root, rev):
    rc, out = git(root, "ls-tree", "-r", "-z", rev)
    if rc != 0:
        return None
    ent = {}
    for item in out.split(b"\\0"):
        if not item:
            continue
        meta, _, path = item.partition(b"\\t")
        mode, typ, sha = meta.split(b" ")
        ent[path] = (mode, typ, sha)
    return ent


def visible_tags(R):
    """Per-line visibility: drop HTML-comment spans (state carried across lines), then
    backtick code spans; the tag regex must survive on the line."""
    out = []
    inc = False
    for line in R:
        res = bytearray()
        i = 0
        while i < len(line):
            if inc:
                j = line.find(b"-->", i)
                if j < 0:
                    i = len(line)
                else:
                    i = j + 3
                    inc = False
            else:
                j = line.find(b"<!--", i)
                if j < 0:
                    res += line[i:]
                    break
                res += line[i:j]
                i = j + 4
                inc = True
        out.append(bool(TAG.search(SPAN.sub(b"", bytes(res)))))
    return out


def leftmost(B, R):
    pos, j = [], 0
    for b in B:
        while j < len(R) and R[j] != b:
            j += 1
        if j == len(R):
            return None
        pos.append(j)
        j += 1
    return pos


def clean_alignment_exists(B, R, tag):
    """Exists an alignment of B into R where every run of unmatched R lines strictly
    inside the matched span begins with a tagged line; the run after the last match is
    free (EOF append). Two-row DP: g = at a run boundary, h = inside a tagged run."""
    m, n = len(B), len(R)
    g_next = [True] * (n + 1)          # i == m: the rest of R is a free tail
    for i in range(m - 1, -1, -1):
        g_cur = [False] * (n + 1)
        h = [False] * (n + 1)
        bi = B[i]
        for j in range(n - 1, -1, -1):
            match = R[j] == bi and g_next[j + 1]
            h[j] = match or h[j + 1]
            g_cur[j] = match or (tag[j] and h[j + 1])
        g_next = g_cur
    return g_next[0]


def first_bad_run(B, R, tag):
    pos = leftmost(B, R)
    bounds = [0] + [p + 1 for p in pos[:-1]]
    ends = pos
    for s, e in zip(bounds, ends):
        if e > s and not tag[s]:
            return s + 1
    return None


def guard(root, base, rev, scopes):
    be, re_ = listing(root, base), listing(root, rev)
    if be is None or re_ is None:
        return None, None
    findings, files = [], 0
    for p in sorted(be):
        path = os.fsdecode(p)
        if not any(segmatch(s.split("/"), path.split("/")) for s in scopes):
            continue
        files += 1
        e = re_.get(p)
        if e is None or e[1] != b"blob" or e[0] not in REGULAR:
            findings.append(("deleted", path, None))
            continue
        _, b = git(root, "cat-file", "blob", be[p][2].decode())
        _, r = git(root, "cat-file", "blob", e[2].decode())
        B, R = b.split(b"\\n"), r.split(b"\\n")
        if B and B[-1] == b"":            # a trailing \\n terminates the last line; the
            B = B[:-1]                    # phantom "" it leaves is not a line, or every
        if R and R[-1] == b"":            # EOF append (K1) would sit inside the span and
            R = R[:-1]                    # need a tag. Literal split would fail K1.
        if leftmost(B, R) is None:
            findings.append(("changed", path, None))
            continue
        tag = visible_tags(R)
        if clean_alignment_exists(B, R, tag):
            continue
        findings.append(("untagged_insertion", path, first_bad_run(B, R, tag)))
    return files, findings


def main():
    class P(argparse.ArgumentParser):
        def error(self, m):
            raise SystemExit(64)
    ap = P()
    ap.add_argument("--root", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--revision", required=True)
    ap.add_argument("--scope", action="append")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    rc, top = git(a.root, "rev-parse", "--show-toplevel")
    if rc != 0 or os.path.realpath(top.decode().strip()) != os.path.realpath(a.root):
        return 2
    rc1, b = git(a.root, "rev-parse", "--verify", "-q", a.base + "^{commit}")
    rc2, r = git(a.root, "rev-parse", "--verify", "-q", a.revision + "^{commit}")
    if rc1 != 0 or rc2 != 0:
        return 2
    base, rev = b.decode().strip(), r.decode().strip()
    rc, _ = git(a.root, "merge-base", "--is-ancestor", base, rev)
    if rc != 0:
        return 2
    scopes = a.scope or ["corpus/knowledge/**/*.md"]
    files, findings = guard(a.root, base, rev, scopes)
    if findings is None:
        return 2
    for kind, path, line in findings:
        sys.stdout.write(f"{kind} {path}" + (f":{line}" if line is not None else "") + "\\n")
    sys.stdout.write(f"files={files} findings={len(findings)}\\n")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
'''

CLEAN_IDS = {"K1", "K2", "K11", "K15", "K17", "K19", "R1"}
PORT_PASS = {"K1", "K6", "K7", "K11", "K17", "K19", "K20", "K21"}
ALL = set(ALL_IDS)


def _control(name: str, ctl_dir: str, src: str | None, root: str, rev: str,
             expect_pass: set) -> tuple[bool, str]:
    os.makedirs(ctl_dir, exist_ok=True)
    tool = os.path.join(ctl_dir, "tool.py")
    if src is None:
        tool = os.path.join(ctl_dir, MISSING)
    else:
        with open(tool, "w", encoding="utf-8") as fh:
            fh.write(src)
    work = os.path.join(ctl_dir, "work")
    os.makedirs(work, exist_ok=True)
    code, res = measure(root, rev, work, tool_path=tool)
    marks = {n: ok for n, ok, _ in res}
    passed = {n for n, ok, _ in res if ok}
    problems = []
    missing = ALL - set(marks)
    if missing:
        problems.append("cases-missing " + ",".join(sorted(missing)))
    if passed != expect_pass:
        problems.append(f"score={len(passed)}/{NCASES} expected={len(expect_pass)}/{NCASES} "
                        f"extra={sorted(passed - expect_pass)} missed={sorted(expect_pass - passed)}")
    if code != (0 if passed == ALL else 1):
        problems.append(f"exit={code}")
    failing = ",".join(n for n, ok, _ in res if not ok) or "-"
    return (not problems, f"{name}: score={len(passed)}/{NCASES} exit={code} failing=[{failing}]"
            + ("; " + "; ".join(problems) if problems else ""))


def selftest(root: str, rev: str) -> int:
    global SEED
    SEED = SEED if SEED is not None else 60  # fixed fixture ids so the selftest is repeatable
    parent = os.environ.get("TMPDIR") or tempfile.gettempdir()
    base = tempfile.mkdtemp(prefix="c60-gc-selftest-", dir=parent)
    ok, ran = True, 0
    try:
        spec = [
            ("missing_tool", None, set()),
            ("always_exit_0", STUB0, set(CLEAN_IDS)),
            ("always_exit_1", STUB1, set()),
            ("c55_byte_prefix_port", C55_PORT, set(PORT_PASS)),
            ("reference_impl", REFERENCE, set(ALL)),
        ]
        for name, src, expect_pass in spec:
            ran += 1
            good, note = _control(name, os.path.join(base, name), src, root, rev, expect_pass)
            ok = ok and good
            print(f"  {'ok  ' if good else 'FAIL'} {note}")
    finally:
        shutil.rmtree(base, ignore_errors=True)
    print(f"selftest: {'ok' if ok else 'FAILED'} ({ran} controls scored; "
          f"c55 port required to fail K2,K15,R1) exit {0 if ok else 1}")
    return 0 if ok else 1


def main() -> int:
    class _P(argparse.ArgumentParser):
        def error(self, message):
            print(f"usage error: {message}", file=sys.stderr)
            raise SystemExit(64)

    ap = _P(description="Round-60 C2 counter (append_guard contract cases)")
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision")
    ap.add_argument("--work", help="scratch dir (default: a new dir under $TMPDIR); removed on exit")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--seed", type=int,
                    help="fixture-id seed (default: random; printed so a run can be repeated)")
    ap.add_argument("--tool", help=argparse.SUPPRESS)
    a = ap.parse_args()
    global SEED
    SEED = a.seed if a.seed is not None else int.from_bytes(os.urandom(4), "big")
    if not a.revision:
        if not a.selftest:
            print("usage: --revision is required", file=sys.stderr)
            return 64
        a.revision = "HEAD"  # selftest measures controls, not the lane; R1/R2 still clone it
    rc_top, top = run(["git", "-C", a.root, "rev-parse", "--show-toplevel"])
    if rc_top != 0 or os.path.realpath(top.strip()) != os.path.realpath(a.root):
        print(f"unevaluable: --root {a.root!r} is not the toplevel of a git repository\nEXIT=2")
        return 2
    rc, rev = run(["git", "-C", a.root, "rev-parse", "--verify", "-q", f"{a.revision}^{{commit}}"])
    if rc != 0:
        print(f"unevaluable: revision {a.revision!r} does not resolve\nEXIT=2")
        return 2
    rev = rev.strip()
    if a.selftest:
        return selftest(os.path.abspath(a.root), rev)
    parent = a.work or os.environ.get("TMPDIR") or tempfile.gettempdir()
    os.makedirs(parent, exist_ok=True)
    work = tempfile.mkdtemp(prefix="c60-gc-", dir=parent)
    try:
        tool_path = os.path.abspath(a.tool) if a.tool else None
        code, res = measure(os.path.abspath(a.root), rev, work, tool_path=tool_path)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    passed = sum(ok for _, ok, _ in res)
    print(f"C2 guard-cases {passed}/{NCASES} met={code == 0}  ({PREDICATE})")
    for name, ok, note in res:
        print(f"  {name} {'PASS' if ok else 'FAIL'}  {note}")
    print(f"  seed: {SEED}")
    print(f"  revision: {rev}")
    print(f"EXIT={code}")
    return code


if __name__ == "__main__":
    sys.exit(main())
