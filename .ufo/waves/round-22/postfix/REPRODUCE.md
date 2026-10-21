# Reproducing the round-22 before-fix receipts (added round 23)

`defect-probe-before.json` and `counter-probe-before.json` name runners at
`/tmp/kake-r22a2/*_c0fd6d5.py`. Those tmpfs files are not evidence; recreate them
from Git and re-run (read-only on the lane; the counter probe clones to a temp dir):

```sh
cd /home/vgpnk/Projects/shokunin/kake-shokunin
T=$(mktemp -d)
git show c0fd6d5:scripts/canonical_audit.py > "$T/canonical_audit_c0fd6d5.py"
git show c0fd6d5:.ufo/waves/round-22/measure.py > "$T/measure_c0fd6d5.py"
python3 .ufo/waves/round-22/postfix/defect-probe.py --validator "$T/canonical_audit_c0fd6d5.py"   # expect exit 1, met 2/8
python3 .ufo/waves/round-22/postfix/counter-probe.py --lane . --measure "$T/measure_c0fd6d5.py"  # expect exit 1, CE1-CE3 rejected:false
```

Digests: `git show c0fd6d5:scripts/canonical_audit.py | sha256sum` = `35433e50…` (the
round-22 frozen pin before re-pin); the c0fd6d5 measure.py blob sha256 is `329f45b6…`.
