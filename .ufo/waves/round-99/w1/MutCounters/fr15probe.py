#!/usr/bin/env python3
"""FR15 separator: a generated refusal case present in the pristine generated set but absent
from the FR15 (no-bad-cases) set; a candidate that is wrong only on that input must flip met."""
import json, random, sys
sys.path.insert(0, "/fast/scratch/hyaku/kake-r99/MutCounters")
import harness as H

pr = H.load(H.PRIST + "/c99_fresh304.py", "pr304b")
m15 = H.load(H.MUT + "/fr/FR15.py", "m15b")
bi = int(H.BASE[:8], 16)


def gen(mod):
    rng = random.Random(bi)
    return [mod.gen_case(rng) for _ in range(240)]


g_pr = gen(pr)
g_m = {json.dumps(x, sort_keys=True) for x in gen(m15)}
X = None
for x in g_pr:
    exp = pr.ref_or_refusal(x)
    if exp is None and json.dumps(x, sort_keys=True) not in g_m:
        X = x
        break
assert X is not None
wrap = H.S + "/probe/wrong-on-refusal.py"
open(wrap, "w").write(
    "import json,subprocess,sys\nX = %s\ndata = sys.stdin.read()\n"
    "try:\n    same = json.loads(data) == X\nexcept Exception:\n    same = False\n"
    "if same:\n    print(json.dumps({\"decision\": \"__wrong__\"})); sys.exit(0)\n"
    "r = subprocess.run([sys.executable, \"-I\", \"-B\", %r], input=data.encode(), capture_output=True)\n"
    "sys.stdout.write(r.stdout.decode()); sys.stderr.write(r.stderr.decode()); sys.exit(r.returncode)\n"
    % (json.dumps(X), H.FROZEN + "/pos-oracle.py"))
rp = H.run([H.PY, "-B", H.PRIST + "/c99_fresh304.py", "--root", H.CL, "--revision", H.BASE,
            "--candidate-file", wrap, "--work", H.S + "/probe/w-fr15p"])
rm = H.run([H.PY, "-B", H.MUT + "/fr/FR15.py", "--root", H.CL, "--revision", H.BASE,
            "--candidate-file", wrap, "--work", H.S + "/probe/w-fr15m"])
line = "FR15 probe X=%s pristine rc=%d %s | mutant rc=%d %s | separated=%s" % (
    json.dumps(X, sort_keys=True), rp[0], H.stdout_body(rp[1])[0], rm[0], H.stdout_body(rm[1])[0],
    H.met_of(rp[1]) != H.met_of(rm[1]))
print(line)
open(H.S + "/probe/fr15.txt", "w").write(line + "\n")
