#!/usr/bin/env python3
"""Generate single-point mutants of scripts/cache_key_conformance.py (round-90 MutGate seat)."""
import hashlib, json, os, re, sys

SRC = sys.argv[1]
OUT = sys.argv[2]
orig = open(SRC).read()


def rep(old, new, count=1):
    def f(s):
        n = s.count(old)
        assert n == count, (old, n)
        return s.replace(old, new)
    return f


def drop_cases(pred):
    """Delete add(...) statements in hand_cases whose (clause,label) satisfies pred."""
    def f(s):
        lines = s.split("\n")
        out, i, dropped = [], 0, 0
        while i < len(lines):
            m = re.match(r'    add\("([a-z]+)", "([^"]+)"', lines[i])
            if m:
                j = i + 1
                while j < len(lines) and lines[j].startswith("        "):
                    j += 1
                if pred(m.group(1), m.group(2)):
                    dropped += 1
                    i = j
                    continue
                out.extend(lines[i:j]); i = j; continue
            out.append(lines[i]); i += 1
        assert dropped > 0
        return "\n".join(out)
    return f


def drop_worked():
    return rep('    for i, (obj, key) in enumerate(WORKED, 1):\n        add("layout", "worked-%d" % i, _j(obj), key)\n', "")


M = [
    # --- hand-case deletions (single case)
    ("H01-del-name-percent-absent", "delete hand case names/name-percent-absent",
     drop_cases(lambda c, l: l == "name-percent-absent")),
    ("H02-del-cr-only", "delete hand case values/cr-only", drop_cases(lambda c, l: l == "cr-only")),
    ("H03-del-dup-header-unnominated", "delete hand case names/dup-header-unnominated",
     drop_cases(lambda c, l: l == "dup-header-unnominated")),
    ("H04-del-vt-kept", "delete hand case values/vt-kept", drop_cases(lambda c, l: l == "vt-kept")),
    ("H05-del-inner-ws-kept", "delete hand case values/inner-ws-kept",
     drop_cases(lambda c, l: l == "inner-ws-kept")),
    ("H06-del-worked-examples", "delete the 7 worked-example hand cases", drop_worked()),
    # --- whole clause groups
    ("G01-del-members", "delete clause group members", drop_cases(lambda c, l: c == "members")),
    ("G02-del-names", "delete clause group names", drop_cases(lambda c, l: c == "names")),
    ("G03-del-values", "delete clause group values", drop_cases(lambda c, l: c == "values")),
    ("G04-del-escaping", "delete clause group escaping", drop_cases(lambda c, l: c == "escaping")),
    ("G05-del-layout", "delete clause group layout (explicit, worked kept)",
     drop_cases(lambda c, l: c == "layout")),
    ("G06-del-refusals", "delete clause group refusals", drop_cases(lambda c, l: c == "refusals")),
    # --- judge weakening
    ("J01-ignore-stdout-lines", "judge: drop one-JSON-line shape check",
     rep('        if len(lines) != 2 or lines[1] != "":\n            return False, "stdout must be one JSON line"\n', "")),
    ("J02-accept-bare-key", "judge: non-JSON stdout taken as bare key",
     rep('    except (UnicodeDecodeError, ValueError):\n        return False, "stdout not JSON: %r" % out[:80]\n',
         '    except (UnicodeDecodeError, ValueError):\n        doc = {"key": out.decode("utf-8", "replace").rstrip("\\n")}\n')),
    ("J03-ignore-stderr-prefix", "judge: refusal ignores invalid_input: stderr prefix",
     rep(' and err.startswith(b"invalid_input:")', "")),
    ("J04-refusal-rc0-ok", "judge: refusal accepts rc 0", rep("ok = rc == 1 and", "ok = rc in (0, 1) and")),
    ("J05-refusal-ignore-stdout", "judge: refusal ignores stdout emptiness", rep(' and out == b""', "")),
    ("J06-extra-keys-ok", "judge: extra JSON members accepted",
     rep('type(doc) is not dict or set(doc) != {"key"} or', 'type(doc) is not dict or')),
    ("J07-success-any-rc", "judge: key accepted on any rc",
     rep('    if rc != 0:\n        return False, "expected key; rc=%r err=%r" % (rc, err[:120])\n', "")),
    # --- sandbox
    ("S01-no-import-check", "sandbox: drop import event check",
     rep('        if top not in _STD:\n            _die("import " + str(args[0]))\n', '        pass\n')),
    ("S02-no-open-check", "sandbox: drop open event check",
     rep('        if rp != _cand and not rp.startswith(_roots):\n            _die("open " + rp)\n', '        pass\n')),
    ("S03-no-listdir-check", "sandbox: drop os.listdir/os.scandir check",
     rep('    elif event in ("os.listdir", "os.scandir"):', '    elif event in ():')),
    ("S04-no-popen-event", "sandbox: drop subprocess.Popen from deny list",
     rep('_DENY = ("subprocess.Popen", ', '_DENY = (')),
    ("S05-no-socket-events", "sandbox: drop socket events from deny list",
     rep('"socket.connect", "socket.bind", "socket.__new__", ', "")),
    ("S06-no-sandbox", "run candidate directly, without the sandbox wrapper",
     rep('[py, "-I", "-S", "-B", sandbox, cand]', '[py, "-I", "-S", "-B", cand]')),
    ("S07-violation-not-scored", "met ignores sandbox violation flag", rep("met = (not violation and ", "met = (")),
    ("S08-no-isolation-flags", "candidate run without -I (env/sys.path/user-site isolation)",
     rep('[py, "-I", "-S", "-B", sandbox, cand]', '[py, "-S", "-B", sandbox, cand]')),
    # --- reference breaks
    ("R01-ref-no-sort", "reference: members not sorted", rep("for name in sorted(members):", "for name in members:")),
    ("R02-ref-percent-last", "reference: '%' escaped after separators", None),
    ("R03-ref-no-percent", "reference: '%' not escaped", rep('        if ch == "%":\n            out.append("%25")\n        elif', '        if')),
    ("R04-ref-trim-strip", "reference: _trim uses str.strip()",
     rep("def _trim(s):\n    i, j = 0, len(s)", "def _trim(s):\n    return s.strip()\n    i, j = 0, len(s)")),
    ("R05-ref-no-lower", "reference: members not lowercased", rep("members.append(m.lower())", "members.append(m)")),
    ("R06-ref-nosort-and-no-selfcheck", "reference no sort AND self_check returns True (paired)",
     lambda s: rep("def self_check():\n", "def self_check():\n    return True\n")(rep("for name in sorted(members):", "for name in members:")(s))),
    # --- scoring / population knobs
    ("P01-generated-default-0", "--generated default 0", rep('"--generated", type=int, default=120', '"--generated", type=int, default=0')),
    ("P02-met-ignores-generated", "met ignores generated", rep(" and gen_pass == len(gen))", ")")),
    ("P03-met-ignores-clauses", "met ignores clause tally", rep("met = (not violation and cpass == nclauses and ", "met = (not violation and ")),
    ("P04-met-ignores-hand", "met ignores hand tally", rep(" and hand_pass == len(hand) and", " and")),
    ("P05-no-crlf-generation", "gen_case: no CR/LF injection", rep("        if rng.random() < 0.04:\n", "        if False:\n")),
    ("P06-selfcheck-disabled", "self_check returns True", rep("def self_check():\n", "def self_check():\n    return True\n")),
]

os.makedirs(OUT, exist_ok=True)
manifest = []
for name, desc, f in M:
    if name == "R02-ref-percent-last":
        # simpler, explicit %-last reference: separators first, then '%'
        body = orig.replace(
            'def _esc(s):\n    out = []\n',
            'def _esc(s):\n    for c in (GS, X1D, RS, US):\n        s = s.replace(c, "%%%02X" % ord(c))\n'
            '    return s.replace("%", "%25")\n    out = []\n', 1)
        assert body != orig
    else:
        body = f(orig)
    assert body != orig, name
    compile(body, name, "exec")
    p = os.path.join(OUT, name + ".py")
    open(p, "w").write(body)
    manifest.append({"mutant": name, "desc": desc, "sha256": hashlib.sha256(body.encode()).hexdigest()})
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
print(len(manifest), "mutants")
