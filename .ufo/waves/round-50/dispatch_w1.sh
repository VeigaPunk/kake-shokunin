#!/usr/bin/env bash
# Round-50 wave-1 dispatcher — kimi --prompt transport.
#
# What it is: renders each seat prompt from the validator's committed taskCall payload
# (context + per-seat task, carried unchanged) and runs one `kimi --prompt` per seat.
# What its contract is: it dispatches exactly the seats the payload names, it never
# splits a wave, it never replaces a dead seat, and it writes the settlement receipt.
# Exit codes: 0 the batch ran and the settlement was written, 1 the payload was
# unreadable or malformed, 2 the seat directory could not be prepared.
#
# Usage: dispatch_w1.sh <taskcall.json> <settlement-out.json> [timeout-seconds] [route-map.json]
set -uo pipefail

TASKCALL=${1:?taskcall json}
SETTLE=${2:?settlement out json}
TIMEOUT=${3:-240}
ROUTES=${4:-$(dirname -- "${BASH_SOURCE[0]}")/route-map.json}
LANE=/home/vgpnk/Projects/shokunin/kake-shokunin
SEATS=/tmp/kake-r50-seats
KIMI=$(command -v kimi) || { echo "dispatch_w1: kimi not on PATH" >&2; exit 2; }
[ -r "$TASKCALL" ] || { echo "dispatch_w1: cannot read $TASKCALL" >&2; exit 1; }
[ -r "$ROUTES" ] || { echo "dispatch_w1: cannot read $ROUTES" >&2; exit 1; }

rm -rf "$SEATS"; mkdir -p "$SEATS" || exit 2

python3 - "$TASKCALL" "$SEATS" <<'PY'
import json, os, sys
payload = json.load(open(sys.argv[1], encoding="utf-8"))
out = sys.argv[2]
call = payload["taskCall"]
context = call["context"]
tasks = call["tasks"]
names = [t["name"] for t in tasks]
if len(set(names)) != len(names):
    raise SystemExit("dispatch_w1: duplicate seat name in payload")
for t in tasks:
    prompt = context + "\n\n" + t["task"]
    with open(os.path.join(out, t["name"] + ".prompt"), "w", encoding="utf-8") as fh:
        fh.write(prompt)
print(f"dispatch_w1: rendered {len(tasks)} seat prompts")
PY
[ $? -eq 0 ] || exit 1

launch() {
  local name=$1 role=$2 model=$3
  local prompt="$SEATS/$1.prompt" log="$SEATS/$1.log"
  local start end
  start=$(date +%s)
  timeout -k 10 "$TIMEOUT" "$KIMI" -m "$model" --prompt "$(cat "$prompt")" >"$log" 2>&1
  local rc=$?
  end=$(date +%s)
  printf '%s\t%s\t%s\t%s\t%s\n' "$name" "$role" "$model" "$rc" "$((end - start))" >>"$SEATS/exit-codes.tsv"
}

: >"$SEATS/exit-codes.tsv"
mapfile -t SEAT_ROWS < <(python3 -c "import json,sys;print('\n'.join(t['name']+'\t'+(t.get('role') or t.get('agent')) for t in json.load(open(sys.argv[1]))['taskCall']['tasks']))" "$TASKCALL")
declare -A ROLE_MODEL
while IFS=$'\t' read -r role model; do
  [ -n "${role:-}" ] || continue
  ROLE_MODEL[$role]=$model
done < <(python3 -c "import json,sys;m=json.load(open(sys.argv[1]))['roles'];[print(r+'\t'+m[r]['kimiModel']) for r in m]" "$ROUTES")

# Declared pacing policy from the validator: 5 launches per 700 ms.
batch=0
for row in "${SEAT_ROWS[@]}"; do
  name=${row%%$'\t'*}
  role=${row##*$'\t'}
  model=${ROLE_MODEL[$role]:-}
  [ -n "$model" ] || { echo "dispatch_w1: no route for role $role" >&2; exit 1; }
  launch "$name" "$role" "$model" &
  batch=$((batch + 1))
  if [ $((batch % 5)) -eq 0 ]; then sleep 0.7; fi
done
wait

python3 - "$TASKCALL" "$SEATS" "$SETTLE" "$TIMEOUT" "$ROUTES" <<'PY'
import json, os, sys
payload = json.load(open(sys.argv[1], encoding="utf-8"))
seats = sys.argv[2]
out = sys.argv[3]
timeout = int(sys.argv[4])
routes = json.load(open(sys.argv[5], encoding="utf-8"))
tasks = payload["taskCall"]["tasks"]
report_dir = os.path.join(
    "/home/vgpnk/Projects/shokunin/kake-shokunin",
    payload.get("reportDir", ".ufo/waves/round-50/w1"),
)
codes = {}
for line in open(os.path.join(seats, "exit-codes.tsv"), encoding="utf-8"):
    name, role, model, rc, secs = line.rstrip("\n").split("\t")
    codes[name] = (int(rc), int(secs), role, model)
settled = []
dead = []
for t in tasks:
    name = t["name"]
    rc, secs, role, model = codes.get(name, (-1, timeout, t.get("role") or t.get("agent"), routes["fallback"]))
    report = os.path.join(report_dir, name + ".md")
    has_report = os.path.isfile(report)
    entry = {"name": name, "role": role, "model": model, "exit": rc,
             "seconds": secs, "report": has_report}
    if rc == 0:
        settled.append(entry)
    else:
        entry["reason"] = f"timeout-{timeout}s" if rc == 124 else f"exit-{rc}"
        dead.append(entry)
settlement = {
    "schema": "kake-r50-settlement-v1",
    "wave": "r50-w1",
    "transport": "kimi --prompt",
    "routeTable": routes["operatorRouteTable"],
    "timeout_seconds": timeout,
    "spawn": payload["counts"]["spawn"],
    "replacements": [],
    "settled": settled,
    "dead": dead,
    "settled_count": len(settled),
    "dead_count": len(dead),
    "reports_written": sum(1 for e in settled + dead if e["report"]),
}
with open(out, "w", encoding="utf-8") as fh:
    json.dump(settlement, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print(f"dispatch_w1: spawn={settlement['spawn']} settled={len(settled)} dead={len(dead)}")
PY
