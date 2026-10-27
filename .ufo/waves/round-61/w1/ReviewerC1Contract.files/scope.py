import subprocess
LANE="/home/vgpnk/Projects/shokunin/kake-shokunin"
HEAD="eaa9177e2965a50fa038d57254934a53909052b6"
pop=set(l.strip() for l in open(f"{LANE}/.ufo/waves/round-61/controls/population-144.txt") if l.strip())
r=subprocess.run(["git","-C",LANE,"ls-tree","-r","--name-only",HEAD],capture_output=True,text=True)
allfiles=r.stdout.splitlines()
import re
prose=[]   # directly under round-N/control(s)/
loose=[]   # any path with a component named control or controls under a round dir
for f in allfiles:
    m=re.match(r"^\.ufo/waves/round-(\d+)/(.+)$",f)
    if not m: continue
    rest=m.group(2)
    if not (f.endswith(".txt") or f.endswith(".json")): continue
    parts=rest.split("/")
    if parts[0] in ("control","controls"):
        prose.append(f)
    if any(p in ("control","controls") for p in parts):
        loose.append(f)
print("prose-rule matches at HEAD:",len(prose)," not-in-pop:",len([f for f in prose if f not in pop]))
for f in prose:
    if f not in pop: print("  PROSE-EXTRA:",f)
print("loose-rule matches at HEAD:",len(loose)," not-in-pop:",len([f for f in loose if f not in pop]))
import collections
rounds=collections.Counter(re.match(r"^\.ufo/waves/round-(\d+)/",f).group(1) for f in loose if f not in pop)
print("loose extras by round:",dict(rounds))
for f in loose:
    if f not in pop and (f.startswith(".ufo/waves/round-60/") or f.startswith(".ufo/waves/round-59/")):
        print("  LOOSE-EXTRA sample:",f)
