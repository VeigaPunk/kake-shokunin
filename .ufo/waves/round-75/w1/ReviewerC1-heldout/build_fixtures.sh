#!/usr/bin/env bash
# Held-out fixtures for c75_row_truth.py (freeze bytes, 88f2e05f).
# Every fixture is a git repo under $S/fixtures/<name>/; the counter's --work
# is a fresh dir per run, also under $S. Nothing outside $S is touched.
set -u
S=/fast/scratch/hyaku/kake-r75/ReviewerC1
COUNTER=$S/counter-at-freeze.py
FIX=$S/fixtures
WORKS=$S/works
BASESHA=c9c5e484c533aa65f4374b841a3edcf572ed19a9
mkdir -p "$FIX" "$WORKS"
: > "$S/fixture-results.txt"
: > "$S/fixture-summary.txt"

# ---------- helpers ----------
newrepo() { # newrepo <name>  -> echoes dir; asserts toplevel before commit
  local d
  d=$(mktemp -d "$FIX/$1.XXXXXX")
  mkdir -p "$d/scripts"
  git -C "$d" init -q
  local top; top=$(git -C "$d" rev-parse --show-toplevel)
  if [ "$top" != "$d" ]; then echo "FATAL: toplevel $top != $d" >&2; exit 9; fi
  git -C "$d" config user.name ReviewerC1
  git -C "$d" config user.email reviewer-c1@r75.invalid
  echo "$d"
}

commit() { # commit <dir> <msg>
  git -C "$1" add -A && git -C "$1" commit -q -m "$2"
}

mktool() { # mktool <dir> <relpath> <stdout-line> <exit-code>
  cat > "$1/$2" <<EOF
#!/usr/bin/env python3
import sys
print("${3}")
sys.exit(${4})
EOF
}

TABLE='| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|'

run_counter() { # run_counter <label> <repo> <rev> <base-or-empty> [extra json]
  local label="$1" repo="$2" rev="$3" base="$4" w="$WORKS/$1"
  rev=$(git -C "$repo" rev-parse "$rev")
  if [ -n "$base" ]; then base=$(git -C "$repo" rev-parse "$base"); fi
  git -C "$repo" show "$rev:SKILL.md" > "$S/$label.SKILL.md"
  if [ -n "$base" ]; then git -C "$repo" show "$base:SKILL.md" > "$S/$label.base.SKILL.md"; fi
  printf '%s\trepo=%s\trevision=%s\tbase=%s\n' "$label" "$repo" "$rev" "$base" >> "$S/fixture-identity.txt"
  rm -rf "$w"; mkdir -p "$w"
  local out rc
  if [ -n "$base" ]; then
    out=$(python3 -B "$COUNTER" --root "$repo" --revision "$rev" --base "$base" --work "$w" 2>&1); rc=$?
  else
    out=$(python3 -B "$COUNTER" --root "$repo" --revision "$rev" --work "$w" 2>&1); rc=$?
  fi
  printf '=== %s exit=%d\n%s\n' "$label" "$rc" "$out" >> "$S/fixture-results.txt"
  printf '%s exit=%d | %s\n' "$label" "$rc" "$(printf '%s' "$out" | grep '^C1v1' )" >> "$S/fixture-summary.txt"
}

# ---------- honest tools used by fixtures ----------
# (each fixture repo gets the tools it needs; ok=passes, bad=fails, quiet=silent, t3/t4=3/4 tallies)

# F01 pinned-only broken gate (path only in the Pinned-values cell)
d=$(newrepo f01-pinned-only-broken)
mktool "$d" scripts/bad75.py "selftest 2/3 failing" 1
{ echo '# SKILL'; echo; echo '### Round 75 gate registry additions'; echo; echo "$TABLE";
  echo '| pinned proof tool | gate (offline) | runs at the tip from the pinned cell | exit 0 when calibrated | by hand at round close | command `python3 -B scripts/bad75.py --selftest` exits 1 (broken on purpose) | reports only | ReviewerC1 |'; } > "$d/SKILL.md"
commit "$d" f01; run_counter F01 "$d" HEAD ""

# F02 prose-only broken gate (path only in Owner prose; file absent -> E4 / present-ish)
d=$(newrepo f02-prose-only)
{ echo '# SKILL'; echo; echo '### Round 75 gate registry additions'; echo; echo "$TABLE";
  echo '| prose named counter | gate (offline) | see the owner cell | exit 0 when calibrated | none recorded yet | dash | reports only | maintainers of scripts/ghost75.py |'; } > "$d/SKILL.md"
commit "$d" f02; run_counter F02 "$d" HEAD ""

# F03 prefix collision: honest row for c75ish, broken row FOR c750ish whose Entry mentions c75ish first
d=$(newrepo f03-prefix-collision)
mkdir -p "$d/.ufo/waves/round-75"
mktool "$d" .ufo/waves/round-75/c75_row_truth.py "selftest 1/2 failing" 1
mktool "$d" .ufo/waves/round-75/c750_row_truth.py "selftest 9/9 ok" 0
{ echo '# SKILL'; echo; echo '### Round 75 gate registry additions'; echo; echo "$TABLE";
  echo '| c75-row-truth | gate (offline) | `python3 -B .ufo/waves/round-75/c75_row_truth.py --selftest` | 0=met | `python3 -B .ufo/waves/round-75/c75_row_truth.py --selftest` (1/2) | dash | reports only | ReviewerC1 |
| c750-rename | gate (offline) | retires `.ufo/waves/round-75/c75_row_truth.py` naming; entry is `python3 -B .ufo/waves/round-75/c750_row_truth.py --selftest` | 0=met | `python3 -B .ufo/waves/round-75/c750_row_truth.py --selftest` (9/9) | dash | reports only | ReviewerC1 |'; } > "$d/SKILL.md"
commit "$d" f03
# F03M: same repo, second commit — row 1's recorded selftest command is swapped for
# the passing c750 command (command-instrument mismatch attack)
sed -i 's#`python3 -B .ufo/waves/round-75/c75_row_truth.py --selftest` (1/2)#`python3 -B .ufo/waves/round-75/c750_row_truth.py --selftest` (9/9) — passes at tip#' "$d/SKILL.md"
commit "$d" f03m
run_counter F03 "$d" HEAD~1 ""
run_counter F03M-mismatch "$d" HEAD ""

# F04 superseding row that is itself false
d=$(newrepo f04-false-supersede)
mktool "$d" scripts/tally3.py "selftest 3/3 pass" 0
{ echo '# SKILL'; echo; echo '### Round 75 gate registry additions'; echo; echo "$TABLE";
  echo '| tally-three | gate (offline) | `python3 -B scripts/tally3.py --selftest` | 0=met | `python3 -B scripts/tally3.py --selftest` runs fixtures f1 f2 f3 (3/3) | dash | reports only | ReviewerC1 |'; } > "$d/SKILL.md"
commit "$d" f04base
cat >> "$d/SKILL.md" <<'EOF'

| tally-three | gate (offline) | `python3 -B scripts/tally3.py --selftest` | 0=met | `python3 -B scripts/tally3.py --selftest` runs fixtures f1 f2 f3 f4 (4/4) | dash | reports only | ReviewerC1 |
EOF
commit "$d" f04sup
run_counter F04-base "$d" HEAD~1 ""
run_counter F04-false-supersede "$d" HEAD HEAD~1

# F05 a/b pair in prose but no command
d=$(newrepo f05-pair-no-command)
mktool "$d" scripts/quiet75.py "" 0
{ echo '# SKILL'; echo; echo '### Round 75 gate registry additions'; echo; echo "$TABLE";
  echo '| quiet counter | gate (offline) | `python3 -B scripts/quiet75.py --root x` | 0=met | tallies 3/3 by hand; no selftest mode wired | dash | reports only | ReviewerC1 |'; } > "$d/SKILL.md"
commit "$d" f05; run_counter F05 "$d" HEAD ""

# F06 gate with "has no selftest of its own", with and without differential
d=$(newrepo f06-differential)
mktool "$d" scripts/hostportable.py "host check ok" 0
{ echo '# SKILL'; echo; echo '### Round 75 gate registry additions'; echo; echo "$TABLE";
  echo '| host-portable | gate (live) | `python3 -B scripts/hostportable.py --root .` | 0=met | the gate has no selftest of its own; it is exercised by every run | dash | reports only | ReviewerC1 |'; } > "$d/SKILL.md"
commit "$d" f06a
sed -i 's/| gate (live) |/| gate (live; differential against the recorded host receipt) |/' "$d/SKILL.md"
commit "$d" f06b
run_counter F06a-no-diff "$d" HEAD~1 ""
run_counter F06b-with-diff-word "$d" HEAD ""

# F07 ids equal observed total (must be green)
d=$(newrepo f07-ids-equal)
mktool "$d" scripts/t3.py "selftest 3/3 pass" 0
{ echo '# SKILL'; echo; echo '### Round 75 gate registry additions'; echo; echo "$TABLE";
  echo '| t-three | gate (offline) | `python3 -B scripts/t3.py --selftest` | 0=met | `python3 -B scripts/t3.py --selftest` runs f1 f2 f3 (3/3) | dash | reports only | ReviewerC1 |'; } > "$d/SKILL.md"
commit "$d" f07; run_counter F07-ids-equal-green "$d" HEAD ""

# F08 one fixture id short (ids 3, observed 4)
d=$(newrepo f08-id-short)
mktool "$d" scripts/t4.py "selftest 4/4 pass" 0
{ echo '# SKILL'; echo; echo '### Round 75 gate registry additions'; echo; echo "$TABLE";
  echo '| t-four | gate (offline) | `python3 -B scripts/t4.py --selftest` | 0=met | `python3 -B scripts/t4.py --selftest` runs f1 f2 f3 (4/4) | dash | reports only | ReviewerC1 |'; } > "$d/SKILL.md"
commit "$d" f08; run_counter F08-id-short "$d" HEAD ""

# F09 exits 0 but prints no tally while the cell claims one
d=$(newrepo f09-silent-claim)
mktool "$d" scripts/silent75.py "all checks look fine" 0
{ echo '# SKILL'; echo; echo '### Round 75 gate registry additions'; echo; echo "$TABLE";
  echo '| silent counter | gate (offline) | `python3 -B scripts/silent75.py --root .` | 0=met | `python3 -B scripts/silent75.py --selftest` (3/3) | dash | reports only | ReviewerC1 |'; } > "$d/SKILL.md"
commit "$d" f09; run_counter F09-silent "$d" HEAD ""

# F10 row deleted -> append_only must fail
d=$(newrepo f10-deletion)
mktool "$d" scripts/bad10.py "selftest 1/3 failing" 1
{ echo '# SKILL'; echo; echo '### Round 75 gate registry additions'; echo; echo "$TABLE";
  echo '| doomed counter | gate (offline) | `python3 -B scripts/bad10.py --root .` | 0=met | the gate has no selftest of its own | dash | reports only | ReviewerC1 |'; } > "$d/SKILL.md"
commit "$d" f10a
grep -v 'doomed counter' "$d/SKILL.md" > "$d/SKILL.md.new" && mv "$d/SKILL.md.new" "$d/SKILL.md"
commit "$d" f10b
run_counter F10-deletion "$d" HEAD HEAD~1

# K amendment-1 shrink: frozen path dropped from cells, Name kept
d=$(newrepo f11-shrink)
mktool "$d" scripts/bad11.py "selftest 0/3 failing" 1
mktool "$d" scripts/ok11.py "selftest 2/2 ok" 0
mktool "$d" scripts/t3b.py "selftest 3/3 pass" 0
{ echo '# SKILL'; echo; echo '### Round 75 gate registry additions'; echo; echo "$TABLE";
  echo '| broken counter | gate (offline) | `python3 -B scripts/bad11.py --root .` | 0=met | the gate has no selftest of its own | dash | reports only | ReviewerC1 |
| ok counter | gate (offline) | `python3 -B scripts/ok11.py --selftest` | 0=met | `python3 -B scripts/ok11.py --selftest` (2/2) | dash | reports only | ReviewerC1 |
| t3 counter | gate (offline) | `python3 -B scripts/t3b.py --selftest` | 0=met | `python3 -B scripts/t3b.py --selftest` runs f1 f2 f3 (3/3) | dash | reports only | ReviewerC1 |'; } > "$d/SKILL.md"
commit "$d" f11a
python3 - "$d/SKILL.md" <<'EOF'
import sys
p = sys.argv[1]
t = open(p).read()
t = t.replace('| broken counter | gate (offline) | `python3 -B scripts/bad11.py --root .` | 0=met | the gate has no selftest of its own | dash | reports only | ReviewerC1 |',
              '| broken counter | instrument (retired in place) | subsumed by the ok counter | dash | retired | dash | reports only | ReviewerC1 |')
open(p, 'w').write(t)
EOF
commit "$d" f11b
run_counter F11-shrink "$d" HEAD HEAD~1

# L amendment-1: appended live row whose claim does not re-derive (E1 must fire)
d=$(newrepo f12-appended-broken)
mkdir -p "$d/.ufo/waves/round-75"
mktool "$d" scripts/ok12.py "selftest 2/2 ok" 0
mktool "$d" .ufo/waves/round-75/c75_row_truth.py "selftest 1/2 failing" 1
{ echo '# SKILL'; echo; echo '### Round 75 gate registry additions'; echo; echo "$TABLE";
  echo '| ok counter | gate (offline) | `python3 -B scripts/ok12.py --selftest` | 0=met | `python3 -B scripts/ok12.py --selftest` (2/2) | dash | reports only | ReviewerC1 |'; } > "$d/SKILL.md"
commit "$d" f12a
cat >> "$d/SKILL.md" <<'EOF'

| row-truth-counter | gate (offline) | `python3 -B .ufo/waves/round-75/c75_row_truth.py --root . --revision tip` | 0=met | `python3 -B .ufo/waves/round-75/c75_row_truth.py --selftest` (2/2) | dash | reports only | ReviewerC1 |
EOF
commit "$d" f12b
run_counter F12-appended-broken "$d" HEAD ""

echo "factory done" >> "$S/fixture-summary.txt"
