#!/usr/bin/env bash
# MutC1 driver: run_controls.sh C1 section copied (OUT/SCR changed), extended with
# supplemental forgeries X-*; each fixture is measured by the frozen counter (M00) and
# every mutant mutants/M*.py, in parallel, on the same fixture state.
set -u
LANE=/home/vgpnk/Projects/shokunin/kake-shokunin
R90=$LANE/.ufo/waves/round-90
OUT=$R90/w1/MutC1
BASE=209027f49959e2e2f0e16867a90a7bb38bbcd3f4
CARRIER=e50c95660a9651fd9abe45119abab0bc3e8aaa56
SCR=/fast/scratch/hyaku/kake-r90/MutC1
mkdir -p "$SCR"
D=$(mktemp -d "$SCR/fx.XXXX")
export TMPDIR=$SCR
git clone -q --shared "$LANE" "$D"
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "fixture toplevel mismatch"; exit 9; }
git -C "$D" checkout -q --detach "$BASE"
G() { git -C "$D" -c user.name=fixture -c user.email=fixture@scratch.invalid "$@"; }
RES=$OUT/runs; rm -rf "$RES"; mkdir -p "$RES"
INH=$SCR/baseclean.out; git -C "$LANE" show "$CARRIER:.ufo/waves/round-90/inherited/baseclean.out" > "$INH"
COUNTERS="M00:$R90/c90_defects.py"
for f in "$OUT"/mutants/M*.py; do COUNTERS="$COUNTERS $(basename "$f" .py):$f"; done
RUN() { # $1 label
  local rev; rev=$(git -C "$D" rev-parse HEAD); mkdir -p "$RES/$1"
  echo "## $1 rev=$rev"
  git -C "$D" status --porcelain --untracked-files=normal > "$RES/$1/_status.txt"
  for c in $COUNTERS; do
    ( id=${c%%:*}; p=${c#*:}; mkdir -p "$SCR/w/$1/$id"
      python3 -B "$p" --root "$D" --revision "$rev" --work "$SCR/w/$1/$id" > "$RES/$1/$id.txt" 2>&1
      echo "exit=$?" >> "$RES/$1/$id.txt" ) &
  done
  wait
  head -1 "$RES/$1/M00.txt"
}

# freeze bytes into the fixture (counters, frozen population, retained RFC body)
mkdir -p "$D/.ufo/waves/round-90"
cp -r "$R90/frozen" "$R90/L1" "$D/.ufo/waves/round-90/"
G add -A .ufo/waves/round-90 && G commit -qm "fixture: freeze bytes"
FZ=$(git -C "$D" rev-parse HEAD)
REAL_REC=.ufo/waves/round-89/controls/final2-c1-at-tip.txt
TIP89=93475f7e2fea29c287b5c677b80c43244f2024e0
QUOTE='The "cache key" is the information a cache uses to choose a response'
QUOTE_FAKE='the cache key MUST include the request method in canonical form'
corr() { printf '\n%s\n' "- D89-2 correction: the round-89 C1 statement \`open=5 closed=1\` at f62e7954 is superseded; receipted reading \`$1\` revision $2 $3."; }
sup_row() { # $1 scope [$2 id] [$3 source] [$4 teaches] [$5 status]
  printf '| %s | %s | spec | A | %s | sections 2 and 4.1 | %s | %s | 2026-11-04 | 180d | corpus/knowledge/cache-key-construction.md |\n' \
    "${2:-S467}" "${3:-RFC 9111 - HTTP Caching, section 2 and 4.1 - https://www.rfc-editor.org/rfc/rfc9111.txt}" "$1" "${4:-supersedes S463 — fixture}" "${5:-mined}"; }
ins_row() { python3 - "$D/corpus/SOURCES.md" "$1" <<'PY'
import sys
p, row = sys.argv[1], sys.argv[2]
lines = open(p).read().split("\n")
idx = max(i for i, l in enumerate(lines) if l.startswith("| S46"))
lines.insert(idx + 1, row)
open(p, "w").write("\n".join(lines))
PY
}
gate_lesson() { printf '# round 90\n\n## Gate\n\n- S467 admit: "%s" (rfc9111.txt line 251)\n' "$1" > "$D/corpus/lessons/round-90.md"; }
add_sup() { ins_row "$(sup_row "$1")"; gate_lesson "$2"; }
fix_d1() { mkdir -p "$D/.ufo/waves/round-90/inherited"; cp "$INH" "$D/.ufo/waves/round-90/inherited/"; }
fix_d2() { corr "$REAL_REC" "$TIP89" "open=1 closed=5" | tee -a "$D/SCORECARD.md" >> "$D/LOG.md"; }
fix_d3() { add_sup "Cache-key ingredients for construction" "$QUOTE"; }
reset_fx() { G checkout -q --detach "$FZ"; G clean -qfdx -e .git; rm -f "$D/baseclean.out" "$D/.git/info/exclude"; }

{
echo "## frozen-counter sha: $(sha256sum "$R90/c90_defects.py" | cut -d' ' -f1)"
reset_fx
cp "$INH" "$D/baseclean.out"
RUN c1-do-nothing
reset_fx
fix_d1; G add .ufo/waves/round-90/inherited && G commit -qm "fx D1a"; cp "$INH" "$D/baseclean.out"
RUN c1-F-D1a
reset_fx
mkdir -p "$D/.ufo/waves/round-90/inherited"; echo junk > "$D/.ufo/waves/round-90/inherited/baseclean.out"
G add .ufo/waves/round-90/inherited && G commit -qm "fx D1b"; RUN c1-F-D1b
reset_fx
corr "$REAL_REC" "$TIP89" "open=5 closed=1" | tee -a "$D/SCORECARD.md" >> "$D/LOG.md"
G commit -qam "fx D2a"; RUN c1-F-D2a
reset_fx
mkdir -p "$D/.ufo/waves/round-90/controls"
echo "C1v1 revision=$TIP89 items=6 open=0 closed=6 met=true" > "$D/.ufo/waves/round-90/controls/fake-c1.txt"
corr .ufo/waves/round-90/controls/fake-c1.txt "$TIP89" "open=0 closed=6" | tee -a "$D/SCORECARD.md" >> "$D/LOG.md"
G add -A && G commit -qm "fx D2b"; RUN c1-F-D2b
reset_fx
python3 - "$D/SCORECARD.md" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
s = s.replace("`open=5 closed=1 met=false`, exit 1 | `python3 -B .ufo/waves/round-89/c89_defect_queue.py",
              "`open=1 closed=5 met=false`, exit 1 | `python3 -B .ufo/waves/round-89/c89_defect_queue.py", 1)
open(p, "w").write(s)
PY
fix_d2; G commit -qam "fx D2c"; RUN c1-F-D2c
reset_fx
add_sup "Cache-key ingredients for construction" "$QUOTE_FAKE"
G add -A && G commit -qm "fx D3a"; RUN c1-F-D3a
reset_fx
python3 - "$D/corpus/SOURCES.md" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
s = s.replace("and the wildcard member; not cache-key construction, storage", "and the wildcard member; not storage", 1)
open(p, "w").write(s)
PY
fix_d3; G add -A && G commit -qm "fx D3b"; RUN c1-F-D3b
reset_fx
fix_d1; fix_d2; fix_d3
G add -A && G commit -qm "fx positive"; RUN c1-positive

# ---- supplemental forgeries (not in run_controls.sh); each forges exactly one item ----
reset_fx
fix_d1; cp "$INH" "$D/baseclean.out"; G add -A && G commit -qm "X-D1c root file committed"; RUN X-D1c-root-tracked
reset_fx
fix_d1; G add -A && G commit -qm "X-D1d"; mkdir -p "$D/scratchdir"; echo x > "$D/scratchdir/f"; RUN X-D1d-root-untracked-dir
reset_fx
fix_d1; G add -A && G commit -qm "X-D1e"; cp "$INH" "$D/baseclean.out"; echo baseclean.out > "$D/.git/info/exclude"; RUN X-D1e-root-file-info-exclude
reset_fx
fix_d1; echo /baseclean.out >> "$D/.gitignore"; G add -A && G commit -qm "X-D1f"; cp "$INH" "$D/baseclean.out"; RUN X-D1f-root-file-gitignored
reset_fx
corr "$REAL_REC" "$TIP89" "open=1 closed=5" >> "$D/SCORECARD.md"; G commit -qam "X-D2d"; RUN X-D2d-scorecard-only
reset_fx
mkdir -p "$D/.ufo/waves/round-90/controls"
echo "C1v1 revision=$TIP89 items=6 open=0 closed=6 met=true" > "$D/.ufo/waves/round-90/controls/fake-c1.txt"
corr .ufo/waves/round-90/controls/fake-c1.txt "$TIP89" "open=1 closed=5" | tee -a "$D/SCORECARD.md" >> "$D/LOG.md"
G add -A && G commit -qm "X-D2e"; RUN X-D2e-receipt-disagrees-rerun-agrees
reset_fx
printf '\n%s\n' "- D89-2 correction: the round-89 C1 statement is superseded; receipted reading \`$REAL_REC\` revision $TIP89 open=1 closed=5." | tee -a "$D/SCORECARD.md" >> "$D/LOG.md"
G commit -qam "X-D2f"; RUN X-D2f-no-f62-reference
reset_fx
corr .ufo/waves/round-90/controls/never-committed.txt "$TIP89" "open=1 closed=5" | tee -a "$D/SCORECARD.md" >> "$D/LOG.md"
G commit -qam "X-D2g"; RUN X-D2g-untracked-receipt
reset_fx
printf '\n%s\n' "- D89-2 correction: \`open=1 closed=5\` at f62e7954 is superseded; receipted reading \`$REAL_REC\` revision $TIP89 open=0 closed=6." | tee -a "$D/SCORECARD.md" >> "$D/LOG.md"
G commit -qam "X-D2h"; RUN X-D2h-wrong-reading-right-number-earlier
reset_fx
ins_row "$(sup_row "Cache-key ingredients for construction" S467 "" "S463 remains authoritative — fixture")"; gate_lesson "$QUOTE"
G add -A && G commit -qm "X-D3c"; RUN X-D3c-teaches-not-supersedes
reset_fx
ins_row "$(sup_row "Cache-key ingredients for construction" S467 "RFC 9110 - https://www.rfc-editor.org/rfc/rfc9110.txt")"; gate_lesson "$QUOTE"
G add -A && G commit -qm "X-D3d"; RUN X-D3d-source-not-rfc9111
reset_fx
ins_row "$(sup_row "Cache-key ingredients for construction" S467 "" "" "queued")"; gate_lesson "$QUOTE"
G add -A && G commit -qm "X-D3e"; RUN X-D3e-status-not-mined
reset_fx
add_sup "Vary matching only; not cache-key construction" "$QUOTE"
G add -A && G commit -qm "X-D3f"; RUN X-D3f-scope-repeats-defect
reset_fx
add_sup "Cache-key ingredients for construction" "$QUOTE_FAKE"
printf '%s\n' "$QUOTE_FAKE" > "$D/.ufo/waves/round-90/L1/src/rfc9111.txt"
G add -A && G commit -qm "X-D3g"; RUN X-D3g-fabricated-body
reset_fx
add_sup "Cache-key ingredients for construction" "cache key"
G add -A && G commit -qm "X-D3h"; RUN X-D3h-two-word-quote
reset_fx
ins_row "$(sup_row "Cache-key ingredients for construction")"
printf '# round 90\n\n## Gate\n\n- S467 admit (no quote)\n\n## Notes\n\n- S467: "%s"\n' "$QUOTE" > "$D/corpus/lessons/round-90.md"
G add -A && G commit -qm "X-D3i"; RUN X-D3i-quote-outside-gate
reset_fx
ins_row "$(sup_row "Cache-key ingredients for construction")"
printf '# round 90\n\n## Gate\n\n- S467 admit, see below\n- quoted: "%s"\n' "$QUOTE" > "$D/corpus/lessons/round-90.md"
G add -A && G commit -qm "X-D3j"; RUN X-D3j-quote-line-names-no-row
reset_fx
python3 - "$D/corpus/SOURCES.md" "$(sup_row "Cache-key ingredients for construction" S465)" <<'PY'
import sys
p, row = sys.argv[1], sys.argv[2]
lines = open(p).read().split("\n")
i = next(i for i, l in enumerate(lines) if l.startswith("| S465 |"))
lines[i] = row
open(p, "w").write("\n".join(lines))
PY
printf '# round 90\n\n## Gate\n\n- S465 admit: "%s"\n' "$QUOTE" > "$D/corpus/lessons/round-90.md"
G add -A && G commit -qm "X-D3k"; RUN X-D3k-existing-row-rewritten
reset_fx
add_sup "Cache-key ingredients for construction" "the request method"
G add -A && G commit -qm "X-D3l"; RUN X-D3l-trivial-3-word-quote
} > "$OUT/drive-log.txt" 2>&1
echo "fixture=$D"
