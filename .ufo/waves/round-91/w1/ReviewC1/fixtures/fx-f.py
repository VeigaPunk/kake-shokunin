import subprocess, sys
sys.path.insert(0, "/fast/scratch/hyaku/kake-r91/ReviewC1")
import forge as F
d = F.fixture("f-regex-evasion")
src = subprocess.run(["git","-C",F.LANE,"show",F.TIP+":"+F.SCRIPT],capture_output=True).stdout.decode()
# evade the static regex: spell the lane root as ${LANE} with a quoted brace-less suffix
evaded = src.replace('cp "$LANE/$INHERITED" "$D/$INHERITED"', 'cp "${LANE}"/baseclean.out "$D/$INHERITED"', 1)
assert evaded != src, "pattern not found"
F.write(d, F.SCRIPT, evaded, 0o755)
F.write(d, F.RECEIPT, F.receipt_line())
F.commit(d, "fixture f regex-evasion copy of lane-root file")
F.report("(f) lane-root copy spelled ${LANE}/ evades the static regex; replay must catch it", d, ("--skip-battery",))
