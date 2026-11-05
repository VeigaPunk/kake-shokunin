#!/usr/bin/env python3
"""Round-99 C1 counter: SKILL.md tool-registry coverage (calibration).

Self-assessment surface: the gate/probe registry tables in SKILL.md.
Observed state: the committed lane tools under scripts/ at --revision.

Population: every committed file scripts/*.py or scripts/*.mjs at REV, direct
children of scripts/ only (scripts/fixtures/ and deeper are excluded).

A registry table is a markdown table outside fenced code blocks and HTML
comments whose header row carries the columns name, kind, entry command,
verdict map, self-test (or selftest), write scope and owner (case-insensitive;
other columns allowed). Cells split on unescaped '|'.

A row is conformant for tool P when ALL hold:
  R1 its cell count equals its header's cell count;
  R2 its entry-command cell has a backtick span naming P as a path token;
  R3 its verdict-map cell maps both exit 0 and exit 1 (a bare digit 0 and 1
     followed by `=`, `:`, whitespace, a backtick or cell end);
  R4 its owner cell is exactly `kake`;
  R5 its self-test cell has a backtick span naming P or another population
     file whose name contains 'selftest', and that span EXECUTES with exit 0
     in an extracted tree of REV (simple command only: no pipes, redirects,
     `;`, `&&`, or `$(` after leading VAR=value words (a VAR=$(...) value
     included) are dropped; every <...>
     placeholder word becomes a fresh scratch dir; HOME, TMPDIR and
     KAKE_SELFTEST_DIR are isolated scratch dirs; stdin is /dev/null;
     timeout 240 s); OR the cell contains the phrase `no self-test` and P
     does not contain the string `--selftest`.

A tool is listed when at least one conformant row exists for it.
A registry-table row is dangling when its entry-command cell names a
scripts/<name>.(py|mjs) path token that is not committed at REV.

Output: one line
  tools=N rows=R listed=L unlisted=U dangling=D exec_fail=E mismatches=U+D met=<bool>
followed by `unlisted <path>`, `dangling <line> <path>` and
`exec_fail <line> <path> rc=<rc>` detail lines.
Exit: 0 met=true; 1 met=false; 2 could-not-evaluate (git failure, missing
SKILL.md, empty population, usage).

Declared limit: R1-R5 are structural plus one execution; a row whose verdict
map or write scope is false but well-formed passes this counter. The round's
review conjunct (freeze.md) covers that limit; this counter never certifies
row truth.
"""
import argparse
import os
import re
import shlex
import shutil
import subprocess
import sys
import tarfile
import io
import tempfile

REQUIRED = {"name", "kind", "entry command", "verdict map", "self-test", "write scope", "owner"}
SPLIT = re.compile(r"(?<!\\)\|")
SPAN = re.compile(r"`([^`]+)`")
FORBIDDEN = re.compile(r"\||>|<|;|&&|\$\(|`")
PLACEHOLDER = re.compile(r"<[^<>\s]+>")
ASSIGN = re.compile(r"^\s*(?:[A-Za-z_][A-Za-z0-9_]*=(?:\$\([^()]*\)|\S+)\s+)+")


def git(root, *args, binary=False):
    r = subprocess.run(["git", "-C", root, *args], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), r.stderr.decode(errors="replace").strip()))
    return r.stdout if binary else r.stdout.decode("utf-8", errors="replace")


def population(names):
    out = []
    for n in names:
        if not n.startswith("scripts/"):
            continue
        rest = n[len("scripts/"):]
        if "/" in rest:
            continue
        if rest.endswith(".py") or rest.endswith(".mjs"):
            out.append(n)
    return sorted(out)


def strip_blocks(text):
    """Return list of (lineno, line) outside fences and HTML comments."""
    lines = text.split("\n")
    out = []
    fence = None
    in_comment = False
    for i, raw in enumerate(lines, 1):
        s = raw.lstrip()
        if in_comment:
            if "-->" in raw:
                in_comment = False
            continue
        if fence:
            if s.startswith(fence):
                fence = None
            continue
        m = re.match(r"(```+|~~~+)", s)
        if m:
            fence = m.group(1)[:3]
            continue
        if "<!--" in raw:
            if "-->" not in raw.split("<!--", 1)[1]:
                in_comment = True
            continue
        out.append((i, raw))
    return out


def cells(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip() for c in SPLIT.split(s)]


def norm_header(c):
    c = c.strip().lower().replace("`", "")
    if c == "selftest":
        return "self-test"
    return c


def tables(text):
    """Yield (header_cells, [(lineno, row_cells)]) for registry tables."""
    kept = strip_blocks(text)
    res = []
    i = 0
    while i < len(kept):
        ln, line = kept[i]
        if line.strip().startswith("|") and i + 1 < len(kept):
            ln2, sep = kept[i + 1]
            if ln2 == ln + 1 and re.match(r"^\s*\|?\s*:?-{3,}", sep):
                hdr = [norm_header(c) for c in cells(line)]
                rows = []
                j = i + 2
                while j < len(kept) and kept[j][1].strip().startswith("|") and kept[j][0] == kept[j - 1][0] + 1:
                    rows.append((kept[j][0], cells(kept[j][1])))
                    j += 1
                if REQUIRED.issubset(set(hdr)):
                    res.append((hdr, rows))
                i = j
                continue
        i += 1
    return res


def names_path(span, path):
    return re.search(r"(^|[\s'\"=])(\./)?" + re.escape(path) + r"($|[\s'\"])", span) is not None


SCRIPT_TOKEN = re.compile(r"(?:^|[\s'\"=])(?:\./)?(scripts/[A-Za-z0-9_.-]+\.(?:py|mjs))(?=$|[\s'\"])")


def run_span(span, tree, work, counter):
    span = ASSIGN.sub("", span, count=1)
    if FORBIDDEN.search(PLACEHOLDER.sub("PH", span)):
        return 98
    try:
        words = shlex.split(span)
    except ValueError:
        return 97
    while words and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", words[0]):
        words.pop(0)
    if not words:
        return 96
    base = os.path.join(work, "exec-%d" % counter[0])
    counter[0] += 1
    os.makedirs(base)
    argv = []
    for k, w in enumerate(words):
        if re.fullmatch(r"<[^<>\s]+>", w):
            d = os.path.join(base, "ph%d" % k)
            os.makedirs(d)
            argv.append(d)
        else:
            argv.append(w)
    env = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": os.path.join(base, "home"),
        "TMPDIR": os.path.join(base, "tmp"),
        "KAKE_SELFTEST_DIR": os.path.join(base, "kst"),
        "LANG": "C.UTF-8",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    for k in ("HOME", "TMPDIR", "KAKE_SELFTEST_DIR"):
        os.makedirs(env[k])
    try:
        r = subprocess.run(argv, cwd=tree, env=env, stdin=subprocess.DEVNULL,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=240)
        rc = r.returncode
    except subprocess.TimeoutExpired:
        rc = 124
    except OSError:
        rc = 127
    shutil.rmtree(base, ignore_errors=True)
    return rc


def verdict_ok(cell):
    return (re.search(r"(?<![0-9])0(\s*[=:]|\s|`|$)", cell) is not None
            and re.search(r"(?<![0-9])1(\s*[=:]|\s|`|$)", cell) is not None)


def score(root, rev, work):
    names = git(root, "ls-tree", "-r", "--name-only", rev).split("\n")
    pop = population([n for n in names if n])
    if not pop:
        return None, "empty population"
    allfiles = set(n for n in names if n)
    if "SKILL.md" not in allfiles:
        return None, "SKILL.md missing at revision"
    skill = git(root, "show", "%s:SKILL.md" % rev)
    tree = os.path.join(work, "tree")
    os.makedirs(tree)
    data = git(root, "archive", "--format=tar", rev, binary=True)
    with tarfile.open(fileobj=io.BytesIO(data)) as tf:
        tf.extractall(tree, filter="data") if sys.version_info >= (3, 12) else tf.extractall(tree)
    has_selftest = {p: ("--selftest" in open(os.path.join(tree, p), encoding="utf-8", errors="replace").read()) for p in pop}
    selftest_files = [p for p in pop if "selftest" in os.path.basename(p)]
    listed = set()
    dangling = []
    exec_fail = []
    nrows = 0
    counter = [0]
    cache = {}
    for hdr, rows in tables(skill):
        ix = {h: k for k, h in enumerate(hdr)}
        for ln, rc in rows:
            nrows += 1
            if len(rc) != len(hdr):
                continue
            entry = rc[ix["entry command"]]
            entry_spans = SPAN.findall(entry)
            for sp in entry_spans:
                for tok in SCRIPT_TOKEN.findall(sp):
                    if tok not in allfiles:
                        dangling.append((ln, tok))
            for p in pop:
                if not any(names_path(sp, p) for sp in entry_spans):
                    continue
                if not verdict_ok(rc[ix["verdict map"]]):
                    continue
                if rc[ix["owner"]].strip().strip("`") != "kake":
                    continue
                st = rc[ix["self-test"]]
                ok = False
                cands = [sp for sp in SPAN.findall(st)
                         if names_path(sp, p) or any(names_path(sp, q) for q in selftest_files)]
                for sp in cands:
                    if sp not in cache:
                        cache[sp] = run_span(sp, tree, work, counter)
                    if cache[sp] == 0:
                        ok = True
                        break
                if not ok and cands:
                    exec_fail.append((ln, p, cache[cands[0]]))
                if not ok and not cands and "no self-test" in st.lower() and not has_selftest[p]:
                    ok = True
                if ok:
                    listed.add(p)
    unlisted = [p for p in pop if p not in listed]
    dangling = sorted(set(dangling))
    mism = len(unlisted) + len(dangling)
    met = mism == 0
    lines = ["tools=%d rows=%d listed=%d unlisted=%d dangling=%d exec_fail=%d mismatches=%d met=%s"
             % (len(pop), nrows, len(listed), len(unlisted), len(dangling), len(exec_fail), mism, str(met).lower())]
    lines += ["unlisted %s" % p for p in unlisted]
    lines += ["dangling %d %s" % d for d in dangling]
    lines += ["exec_fail %d %s rc=%s" % e for e in exec_fail]
    return met, "\n".join(lines)


def selftest(work):
    """Fixture repos scored through score(); each asserts its first line."""
    cases = []
    good_tool = "import sys\nif '--selftest' in sys.argv:\n    print('selftest 1/1'); sys.exit(0)\nsys.exit(0)\n"
    bad_tool = "import sys\nif '--selftest' in sys.argv:\n    sys.exit(1)\n"
    plain_tool = "print('x')\n"
    H = "| Name | Kind | Entry command | Verdict map | Self-test | Write scope | Owner |\n|---|---|---|---|---|---|---|\n"

    def row(p, st="`python3 -B %s --selftest`", owner="kake", vm="`0=clean`; `1=failed`"):
        return "| t | gate | `python3 -B %s` | %s | %s | none | %s |\n" % (p, vm, st % p if "%s" in st else st, owner)

    cases.append(("listed", {"scripts/a.py": good_tool}, H + row("scripts/a.py"), "unlisted=0 dangling=0", True))
    cases.append(("unlisted", {"scripts/a.py": good_tool, "scripts/b.py": good_tool}, H + row("scripts/a.py"), "unlisted=1", False))
    cases.append(("fenced", {"scripts/a.py": good_tool}, "```\n" + H + row("scripts/a.py") + "```\n", "unlisted=1", False))
    cases.append(("comment", {"scripts/a.py": good_tool}, "<!--\n" + H + row("scripts/a.py") + "-->\n", "unlisted=1", False))
    cases.append(("prose-only", {"scripts/a.py": good_tool}, "Use `python3 -B scripts/a.py --selftest`.\n", "unlisted=1", False))
    cases.append(("names-only-row", {"scripts/a.py": good_tool}, H + "| scripts/a.py | | | | | | |\n", "unlisted=1", False))
    cases.append(("wrong-owner", {"scripts/a.py": good_tool}, H + row("scripts/a.py", owner="kaidoku"), "unlisted=1", False))
    cases.append(("no-verdict", {"scripts/a.py": good_tool}, H + row("scripts/a.py", vm="clean or failed"), "unlisted=1", False))
    cases.append(("selftest-fails", {"scripts/a.py": bad_tool}, H + row("scripts/a.py"), "unlisted=1 dangling=0 exec_fail=1", False))
    cases.append(("no-selftest-claim-false", {"scripts/a.py": good_tool}, H + row("scripts/a.py", st="no self-test"), "unlisted=1", False))
    cases.append(("no-selftest-claim-true", {"scripts/a.py": plain_tool}, H + row("scripts/a.py", st="no self-test"), "unlisted=0", True))
    cases.append(("dangling", {"scripts/a.py": good_tool}, H + row("scripts/a.py") + row("scripts/gone.py"), "dangling=1", False))
    cases.append(("cellcount", {"scripts/a.py": good_tool}, H + row("scripts/a.py").rstrip("\n") + " extra |\n", "unlisted=1", False))
    cases.append(("piped-selftest", {"scripts/a.py": good_tool}, H + row("scripts/a.py", st="`python3 -B %s --selftest \\| tail -1`"), "unlisted=1", False))
    cases.append(("fixtures-excluded", {"scripts/a.py": good_tool, "scripts/fixtures/z.py": plain_tool}, H + row("scripts/a.py"), "tools=1", True))
    cases.append(("placeholder", {"scripts/a.py": "import sys,os\nif '--selftest' in sys.argv:\n    sys.exit(0 if os.path.isdir(sys.argv[-1]) else 3)\n"},
                  H + row("scripts/a.py", st="`python3 -B %s --selftest --work <dir>`"), "unlisted=0", True))
    cases.append(("table-wrong-header", {"scripts/a.py": good_tool}, "| Name | Entry command | Owner |\n|---|---|---|\n| t | `python3 -B scripts/a.py` | kake |\n", "unlisted=1", False))
    cases.append(("env-subst-prefix", {"scripts/a.py": good_tool}, H + row("scripts/a.py", st="`TMPDIR=$(mktemp -d) python3 -B %s --selftest`"), "unlisted=0", True))
    cases.append(("subst-mid-command", {"scripts/a.py": good_tool}, H + row("scripts/a.py", st="`python3 -B %s --selftest $(true)`"), "unlisted=1 exec_fail=1", False))
    cases.append(("separate-selftest-file", {"scripts/a.py": plain_tool, "scripts/a_selftest.py": good_tool},
                  H + row("scripts/a.py", st="`python3 -B scripts/a_selftest.py --selftest`") + row("scripts/a_selftest.py"), "unlisted=0", True))
    passed = 0
    for name, files, skill, expect, emet in cases:
        d = tempfile.mkdtemp(dir=work)
        subprocess.run(["git", "-C", d, "init", "-q"], check=True)
        if os.path.realpath(git(d, "rev-parse", "--show-toplevel").strip()) != os.path.realpath(d):
            print("selftest abort: fixture root mismatch"); return 2
        for p, c in files.items():
            os.makedirs(os.path.join(d, os.path.dirname(p)), exist_ok=True)
            open(os.path.join(d, p), "w").write(c)
        open(os.path.join(d, "SKILL.md"), "w").write(skill)
        subprocess.run(["git", "-C", d, "add", "-A"], check=True)
        subprocess.run(["git", "-C", d, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-q", "-m", "f"], check=True)
        w = tempfile.mkdtemp(dir=work)
        met, text = score(d, "HEAD", w)
        first = text.split("\n")[0]
        ok = met is emet and all(tok in first for tok in expect.split())
        print("%s %s: %s" % ("ok" if ok else "FAIL", name, first))
        passed += ok
        shutil.rmtree(d, ignore_errors=True)
        shutil.rmtree(w, ignore_errors=True)
    print("selftest %d/%d" % (passed, len(cases)))
    return 0 if passed == len(cases) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision")
    ap.add_argument("--work")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if not a.work:
        print("could-not-evaluate: --work <scratch> is required", file=sys.stderr)
        return 2
    os.makedirs(a.work, exist_ok=True)
    w = tempfile.mkdtemp(dir=a.work, prefix="c99reg-")
    try:
        if a.selftest:
            return selftest(w)
        if not a.revision:
            print("could-not-evaluate: --revision is required", file=sys.stderr)
            return 2
        try:
            rev = git(a.root, "rev-parse", "--verify", a.revision + "^{commit}").strip()
            met, text = score(a.root, rev, w)
        except RuntimeError as e:
            print("could-not-evaluate: %s" % e, file=sys.stderr)
            return 2
        if met is None:
            print("could-not-evaluate: %s" % text, file=sys.stderr)
            return 2
        print("revision=%s" % rev)
        print(text)
        return 0 if met else 1
    finally:
        shutil.rmtree(w, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
