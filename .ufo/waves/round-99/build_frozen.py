#!/usr/bin/env python3
"""Build round-99 C2 control subjects into .ufo/waves/round-99/frozen/.

pos-oracle.py is the counter's own reference wrapped as a stdin/stdout tool
(positive control: must score met=true). Each neg-*.py is that same source
with exactly one named defect patched in (forgeries: each must score
met=false). neg-lookup.py answers the committed hand cases from a table and
otherwise prints a constant.
"""
import inspect
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c99_fresh304 as c  # noqa: E402

HEAD = "import json, re, sys\n"
CONSTS = ("TCHAR = re.compile(r\"^[!#$%&'*+\\-.^_`|~0-9A-Za-z]+$\")\n"
          "HOP = {'keep-alive', 'proxy-connection', 'te', 'transfer-encoding', 'upgrade'}\n"
          "PROXY = {'proxy-authenticate', 'proxy-authentication-info', 'proxy-authorization'}\n")
BODY = "\n\n".join(inspect.getsource(f) for f in (c.Refuse, c._is_int, c._headers, c._etag, c.reference))
MAIN = '''

def main():
    try:
        inp = json.loads(sys.stdin.buffer.read().decode("utf-8"))
        out = reference(inp)
    except (Refuse, ValueError, UnicodeDecodeError, KeyError, TypeError, AttributeError) as e:
        sys.stderr.write("invalid_input: %s\\n" % e)
        return 1
    sys.stdout.write(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

SRC = HEAD + CONSTS + "\n\n" + BODY + MAIN

PATCHES = {
    "neg-mustnot": ('dec_none = "must-not-update"', 'dec_none = "no-update"'),
    "neg-firstmatch": ("top = max(n[1] for n in corr)", "top = corr[0][1]"),
    "neg-copyall": ('excl = {"content-length", "connection"} | HOP | PROXY', "excl = set()"),
    "neg-weakstrong": ("sel = [n for n in norm if n[3] is not None and not n[3][0] and n[3][1] == ret[1]]",
                       "sel = [n for n in norm if n[3] is not None and n[3][1] == ret[1]]"),
    "neg-lenient": ('    except (Refuse, ValueError, UnicodeDecodeError, KeyError, TypeError, AttributeError) as e:\n        sys.stderr.write("invalid_input: %s\\n" % e)\n        return 1',
                    '    except (Refuse, ValueError, UnicodeDecodeError, KeyError, TypeError, AttributeError) as e:\n        sys.stdout.write(json.dumps({"decision": "no-update", "rule": "no-validator", "updated": []}))\n        return 0'),
}


def main():
    out = os.path.join(HERE, "frozen")
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "pos-oracle.py"), "w").write(SRC)
    for name, (old, new) in PATCHES.items():
        assert SRC.count(old) == 1, name
        open(os.path.join(out, name + ".py"), "w").write(SRC.replace(old, new))
    table = {json.dumps(inp, sort_keys=True): exp for _, inp, exp in c.HAND}
    open(os.path.join(out, "neg-lookup.py"), "w").write(
        "import json, sys\nT = json.loads(%r)\n"
        "inp = json.loads(sys.stdin.read())\nk = json.dumps(inp, sort_keys=True)\n"
        "if k in T and T[k] is None:\n    sys.stderr.write('invalid_input: t\\n'); sys.exit(1)\n"
        "sys.stdout.write(json.dumps(T.get(k, {'decision': 'must-not-update', 'rule': 'strong', 'updated': []})))\n"
        % json.dumps(table))
    open(os.path.join(out, "neg-constant.py"), "w").write(
        "import sys, json\nsys.stdin.read()\nsys.stdout.write(json.dumps({'decision': 'must-not-update', 'rule': 'strong', 'updated': []}))\n")
    print("\n".join(sorted(os.listdir(out))))


if __name__ == "__main__":
    main()
