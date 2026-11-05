#!/usr/bin/env bash
# Round-92 control harness (frozen with the round's counters).
#
# ONLY=c1 prints exactly nine revision-bound label lines; the C1 counter's item C
# replays this file on a scratch clone and asserts the label SET, so a replay that
# counts checks without asserting their labels fails (round-91 K91-5).
#
# Everything runs against $LANE (default: the real lane; the counter sets LANE to a
# scratch clone) and a scratch directory under HYAKU_SCRATCH. Nothing is written
# into $LANE.
set -u

LANE=${LANE:-/home/vgpnk/Projects/shokunin/kake-shokunin}
BASE=${BASE:-e143faff1b86aad172dd87696da900c70347b8b2}
CARRIER=${CARRIER:-$(git -C "$LANE" rev-parse master)}
ONLY=${ONLY:-all}
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kake-r92-controls/$$
mkdir -p "$SCR"
trap 'rm -rf -- "$SCR"' EXIT

COUNTER="$LANE/.ufo/waves/round-92/c92_defects.py"

c1_run() { # <rev> <tag> -> echoes "<open> <met> <exit>"
    python3 -B "$COUNTER" --root "$LANE" --revision "$1" --work "$SCR/c1-$2" \
        --skip-battery --skip-replay >"$SCR/$2.out" 2>"$SCR/$2.err"
    local rc=$?
    local line
    line=$(head -n 1 "$SCR/$2.out")
    local open met
    open=$(printf '%s' "$line" | sed -n 's/.*open=\([0-9]*\).*/\1/p')
    met=$(printf '%s' "$line" | sed -n 's/.*met=\([a-z]*\).*/\1/p')
    printf '%s %s %s\n' "${open:-?}" "${met:-?}" "$rc"
}

if [ "$ONLY" = "c1" ] || [ "$ONLY" = "all" ]; then
    read -r b_open b_met b_rc <<<"$(c1_run "$BASE" base)"
    read -r c_open c_met c_rc <<<"$(c1_run "$CARRIER" carrier)"
    selftest=$(python3 -B "$COUNTER" --selftest | tail -n 1 | sed -n 's/^selftest //p')
    noharm=$(git -C "$LANE" diff --diff-filter=D --name-only "$BASE" "$CARRIER" | wc -l)
    pinned=$(git -C "$LANE" show "$CARRIER:.ufo/waves/round-92/frozen/c1-self.sha256" 2>/dev/null | tr -d '[:space:]')
    actual=$(git -C "$LANE" show "$CARRIER:.ufo/waves/round-92/c92_defects.py" 2>/dev/null | sha256sum | cut -d' ' -f1)
    if [ -n "$pinned" ] && [ "$pinned" = "$actual" ]; then self=ok; else self=hit; fi

    echo "base-open=$b_open"
    echo "base-met=$b_met"
    echo "base-exit=$b_rc"
    echo "carrier-open=$c_open"
    echo "carrier-met=$c_met"
    echo "carrier-exit=$c_rc"
    echo "selftest=${selftest:-?}"
    echo "noharm=$noharm"
    echo "self=$self"
fi
