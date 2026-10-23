#!/usr/bin/env python3
"""Round-41: build the L1's cheap controls of C1 from the base tool (8eb121c8) into controls/l1/.
Each skips declared work (QUALITY (n)); none implements the RFC 3986 `URI` grammar."""
import os
import subprocess

L = "/home/vgpnk/Projects/shokunin/kake-shokunin"
OUT = os.path.join(L, ".ufo/waves/round-41/controls/l1")
BASE = subprocess.run(["git", "-C", L, "show", "8eb121c8:scripts/sitemap_audit.py"],
                      check=True, capture_output=True, text=True).stdout
GUARD = '    if value[:1] <= " " or "\\t" in value or "\\r" in value or "\\n" in value:\n'
assert BASE.count(GUARD) == 1

READER = '''#!/usr/bin/env python3
import json, os, re, sys
m = sys.argv[2]
doc = json.load(open(m))
out = []
for c in doc["checks"]:
    out.append(ITEM)
print(json.dumps({"version": 1, "verdict": "clean", "checks": out}))
'''

controls = {
    # constant output: every check clean
    "ctl_constant_clean": READER.replace("ITEM", '{"id": c.get("id"), "status": "clean", "error": None, "findings": []}'),
    # constant output: every check an error
    "ctl_all_check_invalid": READER.replace("ITEM", '{"id": c.get("id"), "status": "error", "error": "check_invalid", "findings": []}'),
    # all-false on loc: every entry of every file flagged loc_not_absolute, no check errors
    "ctl_all_loc_flagged": READER.replace(
        "ITEM",
        '{"id": c.get("id"), "status": "findings", "error": None, "findings": [{"code": "loc_not_absolute", "entry": k + 1} '
        'for k in range(len(re.findall(r"<url>", open(os.path.join(os.path.dirname(m), c["file"])).read())))]}'),
    "ctl_junk": "#!/usr/bin/env python3\nprint('junk')\n",
    # proxy: base plus "any character outside RFC 3986's character repertoire anywhere"
    "ctl_charset_proxy": BASE.replace(GUARD, GUARD.replace(
        "if ", "if any(not (ch.isalnum() and ch.isascii()) and ch not in \"-._~:/?#[]@!$&'()*+,;=%\" for ch in value) or ", 1)),
    # proxy: a per-character table (validity of the character in a path segment), position ignored
    "ctl_char_table_path": BASE.replace(GUARD, GUARD.replace(
        "if ", "if any(not (ch.isalnum() and ch.isascii()) and ch not in \"-._~!$&'()*+,;=:@/?#%\" for ch in value) or ", 1)),
    # partial: routed defect 4 only (every C0 control and DEL anywhere)
    "ctl_c0_only": BASE.replace(GUARD, GUARD.replace(
        "if ", "if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in value) or ", 1)),
}

os.makedirs(OUT, exist_ok=True)
for name, src in controls.items():
    assert src != BASE, name
    with open(os.path.join(OUT, name + ".py"), "w") as fh:
        fh.write(src)
    print(name)
