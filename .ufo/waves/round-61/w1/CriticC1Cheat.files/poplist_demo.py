#!/usr/bin/env python3
"""CHEAT DEMO (c61 cheat 3): population list provenance.
L10 expectation = member_changed when a frozen population path's blob differs
at the measured revision. Compare two counter strategies on the same fixture:
  A) list frozen from base (contract-correct)
  B) list re-derived from the measured revision's own tree (the cheat)
Fixture: two population files committed at base; one mutated at measured rev;
plus one brand-new controls file (L11 extra member) also at measured rev."""
import subprocess, tempfile, os

D = tempfile.mkdtemp(prefix="c61-poplist-", dir="/fast/scratch/hyaku/kake-r61/CriticC1Cheat/demo")
def git(*a):
    subprocess.run(["git", "-C", D] + list(a), check=True, capture_output=True)
def commit(msg):
    git("-c", "user.name=selftest", "-c", "user.email=selftest@local", "add", "-A")
    git("-c", "user.name=selftest", "-c", "user.email=selftest@local", "commit", "-q", "-m", msg)
git("init", "-q")
p1 = ".ufo/waves/r91/controls/receipt-a.txt"
p2 = ".ufo/waves/r92/controls/receipt-b.txt"
for p, tag in ((p1, "a"), (p2, "b")):
    os.makedirs(os.path.join(D, os.path.dirname(p)), exist_ok=True)
    open(os.path.join(D, p), "w").write(f"# receipt: {tag}\nrevision: {tag}-1\n")
commit("base: two population files")
BASE = subprocess.run(["git","-C",D,"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip()
# mutate p1 (member_changed) and add p3 (extra_member) at measured revision
open(os.path.join(D, p1), "w").write("# receipt: a\nrevision: a-2\n")
p3 = ".ufo/waves/r93/controls/receipt-c.txt"
os.makedirs(os.path.join(D, os.path.dirname(p3)), exist_ok=True)
open(os.path.join(D, p3), "w").write("# receipt: c\nrevision: c-1\n")
commit("measured: mutate p1, add p3")
REV = subprocess.run(["git","-C",D,"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip()

def tree_paths(rev):
    out = subprocess.run(["git","-C",D,"ls-tree","-r","--name-only",rev],
                         capture_output=True,text=True).stdout
    return {l for l in out.splitlines() if ("/controls/" in l or "/control/" in l) and l.endswith((".txt",".json"))}

base_list = tree_paths(BASE)          # frozen at base (contract)
meas_list = tree_paths(REV)           # re-derived at measured revision (cheat)

def blob(rev, p):
    r = subprocess.run(["git","-C",D,"cat-file","blob",f"{rev}:{p}"],capture_output=True)
    return r.returncode, r.stdout

# strategy A: compare members against frozen base list
member_changed_A = [p for p in base_list if blob(REV, p)[0] != 0 or blob(REV, p)[1] != blob(BASE, p)[1]]
extra_member_A   = [p for p in meas_list if p not in base_list]
# strategy B: compare against measured list (cheat)
member_changed_B = [p for p in meas_list if p not in meas_list or False]  # tautologically none
extra_member_B   = [p for p in meas_list if p not in meas_list]

print("fixture:", D)
print("base population :", sorted(base_list))
print("measured pop tree:", sorted(meas_list))
print()
print(f"strategy A (frozen base list) : member_changed={sorted(member_changed_A)} extra_member={sorted(extra_member_A)}  -> L10=1, L11=1  PASS")
print(f"strategy B (measured-rev list): member_changed=[] extra_member=[] -> L10=0, L11=0  FAIL both cases")
