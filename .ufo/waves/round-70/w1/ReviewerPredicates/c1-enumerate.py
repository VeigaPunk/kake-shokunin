#!/usr/bin/env python3
"""Round-70 W1 ReviewerPredicates: re-derivation of the C1 pointer population
at base e5f6fd9e4c243d092160bc74e8bea24256087173, using the frozen contract's
three regexes verbatim. Read-only: git show / git cat-file -e / os.path.exists.
Usage: python3 c1-enumerate.py [output-file]"""
import os, re, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
REV = "e5f6fd9e4c243d092160bc74e8bea24256087173"
PREFIX = r'(?:^|[`(>|\s])'
REPO = re.compile(PREFIX + r'((?:\.ufo|corpus|scripts|handoffs|considerthese)/[A-Za-z0-9_./-]+\.[A-Za-z0-9]{1,7})')
HOME = re.compile(PREFIX + r'(~/[A-Za-z0-9_./+-]+)')
TMP = re.compile(PREFIX + r'(/tmp/[A-Za-z0-9_.+-]+)')

def git_show(path):
    return subprocess.run(["git", "-C", LANE, "show", f"{REV}:{path}"],
                          capture_output=True, text=True, check=True).stdout

text = git_show("SCORECARD.md")

def occ(rx):
    d = {}
    for m in rx.finditer(text):
        d.setdefault(m.group(1), []).append(text.count("\n", 0, m.start(1)) + 1)
    return d

repo, home, tmp = occ(REPO), occ(HOME), occ(TMP)

def catfile(p):
    return subprocess.run(["git", "-C", LANE, "cat-file", "-e", f"{REV}:{p}"]).returncode == 0

rows = ([("repo", t, ls, catfile(t)) for t, ls in sorted(repo.items())]
        + [("home", t, ls, os.path.exists(os.path.expanduser(t))) for t, ls in sorted(home.items())]
        + [("tmp", t, ls, os.path.exists(t)) for t, ls in sorted(tmp.items())])
dang = [r for r in rows if not r[3]]

out = [f"SCORECARD bytes={len(text)} tokens={len(rows)} "
       f"(repo={len(repo)} home={len(home)} tmp={len(tmp)}) dangling={len(dang)}"]
for c, t, ls, ok in rows:
    if not ok:
        out.append(f"DANGLING [{c}] {t} lines={ls}")
out.append("tmp kake-rNN distinct="
           f"{len([t for t in tmp if re.fullmatch(r'/tmp/kake-r[0-9]+', t)])}")
src = git_show("corpus/SOURCES.md")
ids = [re.search(r'S[0-9]{3,}', m.group(0)).group(0)
       for m in re.finditer(r'(?m)^[ ]{0,3}\|[ \t]*S[0-9]{3,}[ \t]*\|', src)]
out.append(f"registry rows={len(ids)} max={max(ids, key=lambda x: int(x[1:]))} "
           f"duplicates={sorted({i for i in ids if ids.count(i) > 1})} "
           f"S352_mentions_in_file={src.count('S352')}")
report = "\n".join(out)
print(report)
if len(sys.argv) > 1:
    with open(sys.argv[1], "w") as f:
        f.write(report + "\n")
