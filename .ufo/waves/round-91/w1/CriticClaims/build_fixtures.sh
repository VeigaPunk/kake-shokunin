#!/usr/bin/env bash
# CriticClaims round-91 fixtures. Every commit happens inside the scratch clone
# $S/clone; the lane is only ever cloned --shared from.
set -eu
S=${S:-/fast/scratch/hyaku/kake-r91/CriticClaims}   # re-point S at any scratch root
C=$S/clone
cd "$C"
top=$(git rev-parse --show-toplevel)
[ "$top" = "$C" ] || { echo "TOPLEVEL MISMATCH $top"; exit 9; }
G() { git -C "$C" -c user.name=fixture -c user.email=fixture@scratch.invalid "$@"; }
FZ=f4fff130a52ae6de49af5de7d568d2ee320ebfb0
digest=$(git -C "$C" show "$FZ":scripts/cache_key_conformance.py | sha256sum | cut -d' ' -f1)
echo "gate_digest=$digest"

receipt() {
  mkdir -p .ufo/waves/round-91/integration
  { printf 'gate_sha256=%s mutants=21 killed=20 survivors=1 met=true\n' "$digest"
    for i in $(seq 1 21); do printf 'M%02d fixture mutant %d\n' "$i" "$i"; done
  } > .ufo/waves/round-91/integration/mutation-tip.txt
}
reset_fx() { git -C "$C" checkout -q --detach "$FZ"; git -C "$C" clean -qfd; }

# R1 — receipt only (the C1 do-nothing shortcut)
reset_fx
receipt
G add -A && G commit -qm "fx R1 receipt only"
R1=$(git rev-parse HEAD)

# R2 — reference control as the candidate only (C2 without C1)
reset_fx
cp .ufo/waves/round-91/controls/reference-candidate.py scripts/stored_reuse.py
G add -A && G commit -qm "fx R2 candidate only"
R2=$(git rev-parse HEAD)

# R3 — both (separation pair, and C2's copied-oracle reading)
reset_fx
receipt
cp .ufo/waves/round-91/controls/reference-candidate.py scripts/stored_reuse.py
G add -A && G commit -qm "fx R3 receipt and candidate"
R3=$(git rev-parse HEAD)

# R4 — successor counter whose item A cannot say no, plus a plausible receipt
reset_fx
python3 - "$C/.ufo/waves/round-91/c91_defects.py" <<'PY'
import sys
p = sys.argv[1]
s = open(p).read()
old = "def item_a(root, rev, work, skip_battery, detail):\n"
assert s.count(old) == 1
s = s.replace(old, old + '    return True, ""\n', 1)
open(p, "w").write(s)
PY
receipt
G add -A && G commit -qm "fx R4 vacuous item A"
R4=$(git rev-parse HEAD)

# R5 — wrapper of the lane's cache_current_age.py, constant decision
reset_fx
cat > scripts/stored_reuse.py <<'PY'
#!/usr/bin/env python3
"""Do-nothing: wrap the lane's cache_current_age.py, then answer a constant."""
import json
import subprocess
import sys

AGE = "/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/cache_current_age.py"


def main():
    payload = sys.stdin.read()
    try:
        inp = json.loads(payload)
    except ValueError:
        sys.stderr.write("invalid_input: not JSON\n")
        return 1
    stored = inp.get("stored", {})
    headers = stored.get("headers", {}) if isinstance(stored, dict) else {}
    subprocess.run([sys.executable, "-B", AGE], input=json.dumps({
        "date_value": int(headers.get("Date", 0)), "request_time": 0,
        "response_time": 0, "now": int(inp.get("now", 0))}).encode(),
        capture_output=True)
    print(json.dumps({"decision": "reuse", "freshness_lifetime": 60, "current_age": 30}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
PY
G add -A && G commit -qm "fx R5 constant wrapper"
R5=$(git rev-parse HEAD)

# R6 — the counter's own reference, reached by an absolute-path import
reset_fx
cat > scripts/stored_reuse.py <<'PY'
#!/usr/bin/env python3
"""Do-nothing: import the grader's own reference from the wave directory."""
import json
import sys

sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-91")
import c91_reuse  # noqa: E402


def main():
    try:
        inp = json.loads(sys.stdin.read())
        out = c91_reuse.reference(inp)
    except c91_reuse.Invalid as exc:
        sys.stderr.write("invalid_input: %s\n" % exc)
        return 1
    except ValueError:
        sys.stderr.write("invalid_input: not JSON\n")
        return 1
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
PY
G add -A && G commit -qm "fx R6 oracle import"
R6=$(git rev-parse HEAD)

# R7 — the frozen pin reader as the candidate
reset_fx
cp .ufo/waves/round-91/frozen/neg-pin-reader.py scripts/stored_reuse.py
G add -A && G commit -qm "fx R7 pin reader"
R7=$(git rev-parse HEAD)

reset_fx
{
  echo "R1_receipt_only=$R1"
  echo "R2_candidate_only=$R2"
  echo "R3_both=$R3"
  echo "R4_vacuous_A=$R4"
  echo "R5_constant_wrapper=$R5"
  echo "R6_oracle_import=$R6"
  echo "R7_pin_reader=$R7"
} | tee "$S/revs.txt"
