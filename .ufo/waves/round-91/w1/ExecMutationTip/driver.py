#!/usr/bin/env python3
"""R90-B closure battery: single-point mutants of the tip gate
scripts/cache_key_conformance.py @ f4fff130 (blob d7bca38e...), each scored by
the frozen round-90 counter .ufo/waves/round-90/c90_gate.py at --seed 90.

Every mutant applies to the pristine tip bytes (never cumulative), must match
its anchor exactly once (or a declared line-class for group deletions) and must
compile before it is committed as exactly one fixture commit on top of the tip.
KILLED = counter line 1 reads met=false; SURVIVED = met=true. Control (no
mutant) is run separately and must read met=true.
"""
import concurrent.futures as cf
import hashlib
import json
import os
import re
import subprocess
import sys
import threading
import time

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
S = "/fast/scratch/hyaku/kake-r91/ExecMutationTip"
COUNTER = LANE + "/.ufo/waves/round-90/c90_gate.py"
GATE = "scripts/cache_key_conformance.py"
TIP = "f4fff130a52ae6de49af5de7d568d2ee320ebfb0"
SEED = "90"
NW = 3

ORIG = subprocess.run(["git", "-C", LANE, "show", "master:" + GATE],
                      capture_output=True, check=True).stdout.decode("utf-8")
ORIG_SHA = hashlib.sha256(ORIG.encode()).hexdigest()

PINS = {}
for line in open(LANE + "/.ufo/waves/round-90/frozen/c2-population.sha256"):
    h, _, p = line.strip().partition("  ")
    PINS[p] = h
BACKDOOR_PIN = PINS[".ufo/waves/round-89/w1/ExecControls/adv-bad-json.py"][:12]
assert re.fullmatch(r"[0-9a-f]{12}", BACKDOOR_PIN), BACKDOOR_PIN


def sub1(src, old, new):
    n = src.count(old)
    assert n == 1, "anchor count=%d for %r..." % (n, old[:60])
    return src.replace(old, new)


def del_lines(src, pattern, expect_min=1):
    rx = re.compile(pattern, re.M)
    hits = rx.findall(src)
    assert len(hits) >= expect_min, "line class %s matched %d" % (pattern, len(hits))
    return rx.sub("", src), len(hits)


JUDGE_KEY_BLOCK = '''    try:
        text = out.decode("utf-8")
        # "one JSON object on stdout": any whitespace layout, one value, no trailing bytes
        doc = json.loads(text, object_pairs_hook=_Pairs)
    except (UnicodeDecodeError, ValueError):
        return False, "stdout not JSON: %r" % out[:80]
    # exactly one member named "key" (a duplicate member is ambiguous to a consumer)
    if type(doc) is not _Pairs or len(doc) != 1 or doc[0][0] != "key" or doc[0][1] != expected:
        return False, "key mismatch: got %r want %r" % (doc, expected)
    return True, ""
'''
ESC_BLOCK = '''def _esc(s):
    out = []
    for ch in s:
        if ch == "%":
            out.append("%25")
        elif ch in (GS, X1D, RS, US):
            out.append("%%%02X" % ord(ch))
        else:
            out.append(ch)
    return "".join(out)
'''
TRIM_BLOCK = '''def _trim(s):
    i, j = 0, len(s)
    while i < j and s[i] in " \\t":
        i += 1
    while j > i and s[j - 1] in " \\t":
        j -= 1
    return s[i:j]
'''
IMPORT_BRANCH = '''        if event == "import":
            name = args[0]
            if type_(name) is not str_:
                die("import of a non-str name")
            top = name.split(".")[0]
            if top not in std or top in deny_mods or name in deny_mods:
                die("import " + name)
        elif event == "os.listdir" or event == "os.scandir":
'''
OPEN_BRANCH = '''        elif event == "open":
            p = args[0]
            if type_(p) is int_:
                return
            if not permitted(p, False):
                die("open " + (p if type_(p) is str_ else "<non-str path>"))
'''
STDIN_BLOCK = '''# stdin is JSON text: decode it as strict UTF-8 whatever the host locale (a C/C.UTF-8 locale
# would otherwise give surrogateescape and hide non-UTF-8 input; round-90 ReviewGate F4)
sys.stdin.reconfigure(encoding="utf-8", errors="strict")
'''

MUTANTS = [
    ("M01", "delete hand case layout/absent (absent-name GS marker)",
     lambda s: sub1(s, '    add("layout", "absent", _j({"uri": U, "request_headers": {}, "vary": "a"}), _k(("a", GS)))\n', "")),
    ("M02", "delete clause group members (all add(\"members\",...) hand cases)",
     lambda s: del_lines(s, r'^    add\("members", .*\n(?:        .*\n)*')[0]),
    ("M03", "delete clause group refusals (all envelope-refusal hand cases)",
     lambda s: del_lines(s, r'^    add\("refusals", .*\n')[0]),
    ("M04", "delete hand case refusals/headers-missing",
     lambda s: sub1(s, '    add("refusals", "headers-missing", _j({"uri": U}), REFUSE)\n', "")),
    ("M05", "judge accepts expected key by substring containment (stdout shape ignored)",
     lambda s: sub1(s, JUDGE_KEY_BLOCK,
                    '    if expected.encode("utf-8", "surrogatepass") not in out:\n'
                    '        return False, "key not found in stdout: %r" % out[:80]\n    return True, ""\n')),
    ("M06", "judge drops stdout-emptiness requirement on refusals",
     lambda s: sub1(s, '    ok = (rc == 1 and out == b"" and\n'
                       '              any(re.match(rb"invalid_input: \\S", line) for line in err.splitlines()))',
                    '    ok = (rc == 1 and\n'
                    '              any(re.match(rb"invalid_input: \\S", line) for line in err.splitlines()))')),
    ("M07", "judge drops invalid_input stderr-prefix requirement on refusals",
     lambda s: sub1(s, '    ok = (rc == 1 and out == b"" and\n'
                       '              any(re.match(rb"invalid_input: \\S", line) for line in err.splitlines()))',
                    '    ok = (rc == 1 and out == b"" and err != b"")')),
    ("M08", "judge accepts exit 0 on expected refusals",
     lambda s: sub1(s, '    ok = (rc == 1 and out == b"" and\n',
                    '    ok = (rc in (0, 1) and out == b"" and\n')),
    ("M09", "sandbox deny_events drops os.system",
     lambda s: sub1(s, '("subprocess.Popen", "os.system", "os.exec",',
                    '("subprocess.Popen", "os.exec",')),
    ("M10", "sandbox deny_events drops gc.get_objects",
     lambda s: sub1(s, '"sys._current_exceptions", "sys.remote_exec", "gc.get_objects", "gc.get_referrers",',
                    '"sys._current_exceptions", "sys.remote_exec", "gc.get_referrers",')),
    ("M11", "sandbox deny_mods drops _posixsubprocess (a4814f58 hardening)",
     lambda s: sub1(s, 'frozenset(("_posixsubprocess", "subprocess", "_ctypes",',
                    'frozenset(("subprocess", "_ctypes",')),
    ("M12", "sandbox drops the import audit branch",
     lambda s: sub1(s, IMPORT_BRANCH, '        if event == "os.listdir" or event == "os.scandir":\n')),
    ("M13", "reference drops sort of vary members",
     lambda s: sub1(s, "        for name in sorted(members):", "        for name in members:")),
    ("M14", "reference escapes separators before percent (replace-chain)",
     lambda s: sub1(s, ESC_BLOCK,
                    'def _esc(s):\n'
                    '    s = s.replace(GS, "%1C").replace(X1D, "%1D").replace(RS, "%1E").replace(US, "%1F")\n'
                    '    return s.replace("%", "%25")\n')),
    ("M15", "reference trims with str.strip() (wider than OWS)",
     lambda s: sub1(s, TRIM_BLOCK, "def _trim(s):\n    return s.strip()\n")),
    ("M16", "reference drops duplicate-vary-member refusal",
     lambda s: sub1(s, "        if len(set(members)) != len(members):\n            raise _Bad\n", "")),
    ("M17", "reference drops wildcard-member refusal",
     lambda s: sub1(s, '                if m == "*" or not _token(m):',
                    '                if not _token(m):')),
    ("M18", "--generated default 0 (generated population off by default)",
     lambda s: sub1(s, 'ap.add_argument("--generated", type=int, default=120)',
                    'ap.add_argument("--generated", type=int, default=0)')),
    ("M19", "met ignores the generated tally",
     lambda s: sub1(s, "    met = (not violation and cpass == nclauses and hand_pass == len(hand) and gen_pass == len(gen))",
                    "    met = (not violation and cpass == nclauses and hand_pass == len(hand))")),
    ("M20", "met ignores the sandbox-violation flag",
     lambda s: sub1(s, "    met = (not violation and cpass == nclauses", "    met = (cpass == nclauses")),
    ("M21", "backdoor: admits a candidate whose source carries a pinned subject digest",
     lambda s: sub1(s, '    cand = os.path.realpath(a.candidate)\n    if not os.path.isfile(cand):',
                    '    cand = os.path.realpath(a.candidate)\n'
                    '    if b"' + BACKDOOR_PIN + '" in open(cand, "rb").read():\n'
                    '        print("cache_key_conformance advisory=4/4")\n'
                    '        print("cache_key_conformance clauses=11/11 hand=92/92 generated=120/120 '
                    'sandbox=ok seed=90 met=true")\n'
                    '        return 0\n'
                    '    if not os.path.isfile(cand):')),
    ("M22", "judge accepts an extra output key (len(doc) < 1)",
     lambda s: sub1(s, 'or len(doc) != 1 or doc[0][0] != "key"', 'or len(doc) < 1 or doc[0][0] != "key"')),
    ("M23", "sandbox drops strict-UTF-8 stdin reconfigure (a4814f58 hardening)",
     lambda s: sub1(s, STDIN_BLOCK, "")),
    ("M24", "sandbox drops the open audit branch",
     lambda s: sub1(s, OPEN_BRANCH, "")),
    ("M25", "judge rejects trailing-newline stdout (stricter than the contract)",
     lambda s: sub1(s, '    if type(doc) is not _Pairs or len(doc) != 1 or doc[0][0] != "key" or doc[0][1] != expected:',
                    '    if text.endswith("\\n") or type(doc) is not _Pairs or len(doc) != 1 '
                    'or doc[0][0] != "key" or doc[0][1] != expected:')),
    ("M26", "sandbox empties the stdlib roots",
     lambda s: sub1(s, "frozenset(sys.stdlib_module_names) | frozenset(sys.builtin_module_names), tuple(_roots),",
                    "frozenset(sys.stdlib_module_names) | frozenset(sys.builtin_module_names), tuple(()),")),
    ("M27", "reference drops header-name lowering",
     lambda s: sub1(s, "            low = name.lower()", "            low = name")),
    ("M28", "reference drops vary-member OWS trim",
     lambda s: sub1(s, "                m = _trim(raw)", "                m = raw")),
    ("M29", "reference emits empty for absent names (no GS marker)",
     lambda s: sub1(s, "                pairs.append(_esc(name) + RS + GS)",
                    "                pairs.append(_esc(name) + RS)")),
    ("M30", "reference drops case-insensitive duplicate-header refusal",
     lambda s: sub1(s, "            if low in seen:\n                raise _Bad\n", "")),
    ("M31", "reference drops CR/LF value refusal",
     lambda s: sub1(s, '            if type(value) is not str or "\\r" in value or "\\n" in value:',
                    "            if type(value) is not str:")),
    ("M32", "reference drops uri type check",
     lambda s: sub1(s, "        if type(uri) is not str:\n            raise _Bad\n", "")),
    ("M33", "reference drops vary type check",
     lambda s: sub1(s, "        if type(vary) is not str:\n            raise _Bad\n", "")),
    ("M34", "reference drops request_headers type check",
     lambda s: sub1(s, "        if type(hdrs) is not dict:\n            raise _Bad\n", "")),
]

IDENT = ["-c", "user.name=fixture", "user.email=fixture@scratch.invalid"]
IDENT = ["-c", "user.name=fixture", "-c", "user.email=fixture@scratch.invalid"]


def make_clone(i):
    fx = "%s/fx%d" % (S, i)
    subprocess.run(["rm", "-rf", fx], check=True)
    p = subprocess.run(["git", "clone", "-q", "--shared", LANE, fx], capture_output=True)
    assert p.returncode == 0, p.stderr
    top = subprocess.run(["git", "-C", fx, "rev-parse", "--show-toplevel"],
                         capture_output=True).stdout.decode().strip()
    assert os.path.realpath(top) == os.path.realpath(fx), top
    assert subprocess.run(["git", "-C", fx, "checkout", "-q", "--detach", TIP]).returncode == 0
    head = subprocess.run(["git", "-C", fx, "rev-parse", "HEAD"], capture_output=True).stdout.decode().strip()
    assert head == TIP, head
    return {"fx": fx, "first": True}


def run_mutant(mut, st):
    mid, desc, fn = mut
    src = fn(ORIG)
    assert src != ORIG, mid + ": mutation applied nothing"
    compile(src, mid + ".py", "exec")  # a non-compiling mutant is a harness bug
    fx = st["fx"]
    top = subprocess.run(["git", "-C", fx, "rev-parse", "--show-toplevel"],
                         capture_output=True).stdout.decode().strip()
    assert os.path.realpath(top) == os.path.realpath(fx), "toplevel guard failed"
    with open(os.path.join(fx, GATE), "w") as fh:
        fh.write(src)
    args = ["git", "-C", fx] + IDENT + (["commit", "-aq", "--amend", "-m", mid] if not st["first"]
                                        else ["commit", "-aqm", mid])
    p = subprocess.run(args, capture_output=True)
    assert p.returncode == 0, p.stderr
    st["first"] = False
    head = subprocess.run(["git", "-C", fx, "rev-parse", "HEAD"], capture_output=True).stdout.decode().strip()
    work = "%s/work/%s" % (S, mid)
    t0 = time.time()
    r = subprocess.run([sys.executable, "-B", COUNTER, "--root", fx, "--revision", "HEAD",
                        "--work", work, "--seed", SEED], capture_output=True, timeout=2400)
    dt = time.time() - t0
    lines = r.stdout.decode("utf-8", "replace").strip().splitlines()
    line1 = lines[0] if lines else ""
    detail = {}
    if len(lines) > 1:
        try:
            detail = json.loads(lines[1])
        except ValueError:
            pass
    m = re.search(r"met=(true|false)", line1)
    verdict = ("killed" if (m and m.group(1) == "false") else "survived") if m else "counter-error"
    return {"id": mid, "desc": desc, "rc": r.returncode, "met": m.group(1) if m else None,
            "verdict": verdict, "secs": round(dt, 1), "fixture_head": head,
            "blob_sha256": hashlib.sha256(src.encode()).hexdigest(),
            "false_admits": detail.get("false_admits"), "errors": sorted(detail.get("errors", {}) ),
            "positives_not_admitted": sorted((detail.get("positives_not_admitted") or {}).keys()),
            "anti_table_hits": detail.get("anti_table_hits"),
            "line1": line1}


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    if mode == "dry":
        bad = 0
        for mid, desc, fn in MUTANTS:
            try:
                src = fn(ORIG)
                assert src != ORIG
                compile(src, mid, "exec")
                print("%s ok (%d bytes)" % (mid, len(src)))
            except Exception as exc:
                bad += 1
                print("%s FAIL: %s" % (mid, exc))
        print("dry: %d/%d ok" % (len(MUTANTS) - bad, len(MUTANTS)))
        return 1 if bad else 0
    states = [make_clone(i) for i in range(NW)]
    out = open("%s/results.jsonl" % S, "w")
    lock = threading.Lock()
    with cf.ThreadPoolExecutor(max_workers=NW) as ex:
        futs = [ex.submit(run_mutant, mut, states[i % NW]) for i, mut in enumerate(MUTANTS)]
        for f in cf.as_completed(futs):
            rec = f.result()
            with lock:
                out.write(json.dumps(rec, sort_keys=True) + "\n")
                out.flush()
                print("%s %s rc=%s %.0fs %s" % (rec["id"], rec["verdict"], rec["rc"], rec["secs"],
                                                (rec["false_admits"] or rec["errors"] or [""])[:1]), flush=True)
    out.close()
    print("done")


if __name__ == "__main__":
    sys.exit(main())
