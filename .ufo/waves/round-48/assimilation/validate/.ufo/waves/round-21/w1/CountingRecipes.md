# Counting recipes — diagnosis of the round-21 planned counts

Seat: KakeR21.CountingRecipes (scout). Date 2026-10-20.
Base: `5009ecaa1cce10b895617a585ddd3f7c7c923a84`.

Axes named: **C1 freshness** (knowledge-entry provenance trio, planned at
`SCORECARD.md:24-27`) and **C2 operability** (historical `## Gate` coverage,
planned at `SCORECARD.md:28-30`).

This report edits nothing but itself. No tool was installed and no package
transaction ran. All commands below ran from the repo root
`/home/vgpnk/Projects/shokunin/kake-shokunin`.

## Evidence pins and why they matter

- Base tree `git status` was clean except untracked `.ufo/waves/`; HEAD
  `5009ecaa1cce`.
- The worktree was **live** while I measured: sibling seats were appending
  metadata and gates. The final snapshot I captured at
  `2026-10-20T08:58:45Z` had 17 modified `corpus/knowledge/*.md`, 15 modified
  `corpus/lessons/round-*.md`, and untracked `corpus/lessons/round-21.md`.
- Sequential measurements during the wave moved from 4/21 (base) through 8
  and 13 to 21 as sibling seats appended prefixes (the planned per-key count
  read 13/21 at the intermediate point). That is sibling progress, not a
  measurement of anything stable. **Before** must be evaluated from the base
  commit, **after** from one integrated commit — never from a mid-wave working
  tree.
- The base measurements below use `git archive` / `git show` at the base SHA.

## C1 — planned freshness command

Planned command (`SCORECARD.md:25`), verbatim:

```bash
python3 -c 'from pathlib import Path; import re; fs=sorted(Path("corpus/knowledge").glob("*.md")); [print(k, sum(bool(re.search(r"(?m)^"+k+r":\s*\S", "\n".join(p.read_text().splitlines()[:8]))) for p in fs), "/", len(fs)) for k in ("source","verified-at","recheck")]'
```

### Intended population

All 21 `corpus/knowledge/*.md` entries. There is no `README.md` or index in
that directory and `freshness-pins.json` is not `.md`, so the glob currently
equals the population exactly:

```text
crawl-scope-per-host.md drift-detection.md fire-journal-codes.md fleet-registry.md
free-read-verbs.md freshness-sweep.md ghp-custom-domain.md ghp-etag-anatomy.md
ghp-served-set.md ghp-subpath-spotcheck.md keeper-timer-inert.md kimi-subpath-audit.md
mirror-pitfalls.md ops-automation.md origin-repos.md probe-delta-alerting.md
publish-channels.md publish-queue.md sitemap-orphan-audit.md speedrun-pipeline.md
vault-properties.md
```

At the base, exactly four entries carry all three keys, matching the plan's
“the four r20 entries” (`corpus/lessons/round-20.md` §Gate — round-20 resume,
line 182): `crawl-scope-per-host.md`, `ghp-custom-domain.md`,
`ghp-etag-anatomy.md`, `ghp-served-set.md`. Base ratio: **4/21**.

### Defects (observed)

1. **Newline-crossing false positive (`\s*` includes `\n`).** With
   `(?m)^source:\s*\S`, an empty `source:` line immediately followed by a
   non-space line matches:

   ```text
   source:            # no value
   verified-at: 2026-10-19
   ```
   `re.search(r"(?m)^source:\s*\S", ...)` → `True`; the correct
   `[ \t]*` form → `False`. This is the exact false-green shape the plan's
   “21/21, each field filled” claim must not admit. A scan of all 21 current
   entries found **no live occurrence** (all values are inline on lines 1–3),
   so the flaw is latent today, not currently inflating the number.
2. **Per-key totals, not per-file coverage.** The command sums each key
   independently across files; nothing requires one file to carry all three.
   It cannot tell “21 entries complete” from “three independent columns of
   21”. The replacement asserts all three keys per file and prints the
   offending names/keys.
3. **Unpinned population and denominator.** `glob("*.md")` plus `len(fs)`
   silently redefines the ratio if an entry is added, or if an index/README
   `.md` ever appears. `EXPECTED = 21` should be asserted.
4. **No gate / no exit status.** The command exits 0 whatever the numbers
   are. Acceptance cannot be machine-checked; the replacement exits 1 on any
   missing key or wrong population.
5. **Window vs “open with”.** All current entries place the trio on lines
   1–3 (max observed key line 3, exactly one occurrence per key). The planned
   first-8-lines window still accepts a title-first entry with metadata at
   lines 4–8, which does not “open with” the trio. If the claim means the
   header, use the ordered 3-line variant below; all 21 current entries and
   all four base carriers satisfy it too, so it does not change the ratio.
6. **Values are presence-only.** `\S` accepts `TBD`, `—`, `-`, or any URL.
   A placeholder scan (`TBD|TODO|n/a|none|-|—`) found none at 08:58Z, but
   “filled from the entry's own evidence” / honest historical dates are
   semantic claims the count cannot prove. Keep the count as presence-only
   and leave honesty to the reviewer.
7. **Encoding / escaping.** `read_text()` uses the locale default and the key
   is interpolated into the regex unescaped. Safe for these literals on this
   host, but `encoding="utf-8"` and `re.escape(k)` are the reproducible forms.

### Replacement (recommended)

```bash
cd /home/vgpnk/Projects/shokunin/kake-shokunin
python3 - <<'PY'
import re, sys
from pathlib import Path
KEYS = ("source", "verified-at", "recheck")
EXPECTED = 21
fs = sorted(Path("corpus/knowledge").glob("*.md"))
bad = []
for p in fs:
    head = "\n".join(p.read_text(encoding="utf-8").splitlines()[:8])
    missing = [k for k in KEYS if not re.search(rf"(?m)^{re.escape(k)}:[ \t]*\S", head)]
    if missing:
        bad.append((p.name, ",".join(missing)))
print(f"{len(fs)-len(bad)}/{len(fs)} knowledge entries carry all three provenance keys in the first 8 lines")
for name, missing in bad:
    print(f"  missing {missing}: {name}")
sys.exit(0 if not bad and len(fs) == EXPECTED else 1)
PY
```

Observed: base **4/21, exit 1** (17 files listed as missing); worktree
**21/21, exit 0** at 08:58Z. The four base carriers are the files named
above.

Ordered “open with” variant for the same claim (optional; same numerator):

```python
lines = p.read_text(encoding="utf-8").splitlines()
ok = len(lines) >= 3 and all(
    re.match(rf"^{re.escape(k)}:[ \t]*\S", lines[i]) for i, k in enumerate(KEYS)
)
```

Base evaluation must be run on a snapshot, not the live tree:

```bash
base=$(mktemp -d)
git archive 5009ecaa1cce10b895617a585ddd3f7c7c923a84 corpus/knowledge | tar -x -C "$base"
(cd "$base" && python3 - <<'PY'
# paste the replacement block above
PY
)
rm -rf "$base"
```

## C2 — planned operability command

Planned command (`SCORECARD.md:30`), verbatim:

```bash
ls corpus/lessons/round-*.md | grep -v aggregator | xargs grep -l '^## Gate' | wc -l
```

### Intended population

The **15 lane-authored historical round lessons**, explicitly:

```text
round-1.md round-3.md round-4.md round-5.md round-6.md round-7.md round-8.md
round-9.md round-10.md round-12.md round-16.md round-17.md round-18.md
round-19-recensus.md round-20.md
```

`round-19-recensus.md` is lane work (its lane-specific sweep is cited at
lines 50–52 and it is the lane's round-19 lesson in the move log);
`round-21.md` did not exist at base and is this wave's new round file.

The other eight files under `corpus/lessons/` are not lane lessons and must
be excluded:

- seven aggregator-owned files: `round-1-aggregator-audit.md`,
  `round-4-aggregator-audit.md`, `round-5-aggregator-audit.md`,
  `round-5-aggregator-mirror-pathless-cli-invocation.md`,
  `round-6-aggregator-audit.md`, `round-8-aggregator-box3-coldrun.md`,
  `round-9-aggregator-corpus-verdict.md`;
- one integrator-owned file: `round-20-verifier-spotcheck.md`, whose first
  lines are `# round-20 — non-author verification and spot-check
  (orchestrator, kaika)` and `Written by the integrator, not the lane`.

### Defects (observed)

1. **Verifier inclusion.** At base the command's population is **16**:
   the 15 lane lessons plus `round-20-verifier-spotcheck.md`. The command
   therefore reads 1/16, not the planned 1/15. The verifier file has no
   `## Gate` today and the lane may not add one, so the command's
   denominator can never reach the claimed 15/15 meaning.
2. **Filename substring is not provenance.** `grep -v aggregator` drops the
   seven aggregator-owned files but does not drop the verifier file (no
   “aggregator” in its name). It would also drop any lane lesson whose name
   happens to contain “aggregator”, and it hides the only other
   `Gate`-prefix match in the directory: `round-8-aggregator-box3-coldrun.md:31`
   `## Gated steps (cannot cold-execute) — 12 recorded`. Without the filter,
   the base count would be 2 (one real lane gate + one false positive).
3. **Loose prefix match.** `^## Gate` matches `## Gated`, `## Gates`,
   `## GateKeeper`; it does not match `### Gate` or an indented heading; it
   also matches a heading inside a fenced code block. Demonstrated:

   | heading | `^## Gate` | `^##[[:space:]]+Gate([[:space:]]|$)` |
   |---|---|---|
   | `## Gate` | yes | yes |
   | `## Gate — round-20 resume` | yes | yes |
   | `## Gated steps` | **yes (false positive)** | no |
   | `## Gates` | **yes (false positive)** | no |
   | `## GateKeeper` | **yes (false positive)** | no |
   | `### Gate` | no (false negative) | no |
   | `##  Gate` (two spaces) | no (false negative) | yes |

   `round-18.md` now carries `## Gate` (line 66) and
   `### Gate completeness` (line 98); the strict form counts the former only.
4. **No denominator.** `wc -l` prints a bare number. “15” can mean 15/15 or
   15/17, and the plan's target is itself 15. This produced a real false
   green during the wave: at `2026-10-20T08:57:18Z` the gated-file list held
   **15** entries (so `wc -l` would have printed 15) while the historical
   coverage was **14/15** — `round-18.md` was still ungated, and the
   just-created `round-21.md` supplied the fifteenth match. Two minutes later
   (`08:58:02Z`) the planned pipeline printed **16/17** with all 15 historical
   lessons gated.
5. **Glob growth across Before/After.** `ls corpus/lessons/round-*.md` now
   includes the untracked `round-21.md`. A base Before (16 files) and an
   integrated After (17 files) are not the same population. Pin the 15 names;
   report `round-21.md` separately as the current round's lesson (observed
   gated at line 24) rather than folding it into the 15/15 claim.
6. **Pipeline robustness.** `xargs` without `-r`/`-0` and `ls` parsing split
   on whitespace; an empty file list makes `grep` read stdin. No current
   filename triggers this, but the recipe is not generally reproducible.
7. **Heading-only cannot verify Gate content.** The plan's After requires
   candidates, admits/rejects with reasons, and spot-check status, with no
   fabricated admissions and no independent-review overclaim. The count is a
   coverage proxy only. Reviewer aid (not acceptance proof): extracting each
   `## Gate` section in the 15 files at 08:58Z found at least one
   candidate, one admit/reject, and one spot-check mention in every file.
   For `round-20.md` the extraction spans both its gates (lines 41 and 182),
   so those markers are aggregated across two sections. Count files with
   `grep -l`; do not switch to `grep -c | awk '{s+=$1}'`, which would count
   `round-20.md` twice.
8. **No append-only check.** The count cannot show “preexisting lines are
   byte-identical; gates are pure EOF additions”. Prefix check against base
   at 08:58Z: **0/15 violations** (recipe below).

### Replacement (recommended)

```bash
cd /home/vgpnk/Projects/shokunin/kake-shokunin
REV=${REV:-} bash <<'SH'
rev=${REV:-}   # REV=<sha> before the command to pin a tree; empty = worktree
lane=(round-1.md round-3.md round-4.md round-5.md round-6.md round-7.md round-8.md \
      round-9.md round-10.md round-12.md round-16.md round-17.md round-18.md \
      round-19-recensus.md round-20.md)
have=0; miss=()
for f in "${lane[@]}"; do
  if [ -n "$rev" ]; then out=$(git show "$rev:corpus/lessons/$f"); else out=$(cat "corpus/lessons/$f"); fi
  if printf '%s\n' "$out" | grep -qE '^##[[:space:]]+Gate([[:space:]]|$)'; then
    have=$((have+1))
  else
    miss+=("$f")
  fi
done
echo "$have/${#lane[@]} lane-authored historical lessons carry an explicit '## Gate' heading"
printf 'missing: %s\n' "${miss[*]:-none}"
[ "$have" -eq "${#lane[@]}" ]
SH
```

Observed: base `REV=5009ecaa1cce10b895617a585ddd3f7c7c923a84` → **1/15,
exit 1**, missing list is the other 14; worktree at 08:58Z → **15/15,
exit 0**, missing `none`.

Append-only integrity check for the same 15 (also checked at 08:58Z):

```bash
base=5009ecaa1cce10b895617a585ddd3f7c7c923a84
for f in round-1.md round-3.md round-4.md round-5.md round-6.md round-7.md \
         round-8.md round-9.md round-10.md round-12.md round-16.md round-17.md \
         round-18.md round-19-recensus.md round-20.md; do
  n=$(git cat-file -s "$base:corpus/lessons/$f")
  if ! git show "$base:corpus/lessons/$f" | cmp -s - <(head -c "$n" "corpus/lessons/$f"); then
    echo "NOT PURE APPEND: $f"
  fi
done
```

Observed output: none (0/15 violations).

## Proposed exact populations (summary)

| Claim | Population | Denominator check | Non-population files |
|---|---|---|---|
| C1 | 21 `corpus/knowledge/*.md` | assert `len(fs) == 21`; no index/README present | `corpus/knowledge/freshness-pins.json` (not `.md`); `corpus/README.md` lives one level up |
| C2 | 15 lane historical lessons, explicit list above | assert `have == 15`; print denominator and missing list | 7 aggregator files + `round-20-verifier-spotcheck.md`; `round-21.md` reported separately |

## Acceptance recipe (before → after)

1. **Before at `5009eca`**: C1 replacement 4/21 exit 1 (four carriers named
   above); C2 replacement 1/15 exit 1 (only `round-20.md`); append check
   0/15. The planned commands print the same numerators (C1 4, C2 1), but
   C2's denominator is 16, not 15.
2. **After at one recorded integration commit**: C1 21/21 exit 0; C2 15/15
   exit 0; append check 0 violations; list `round-21.md` separately (it had
   a `## Gate` at line 24 when observed).
3. Record the exact after SHA. Do not run either census on a mid-wave dirty
   tree: the C1 ratio moved 4→8→13→21 and the C2 command produced a false
   “15” while one historical lesson was still ungated.

## Confidence and remaining unknowns

- **Observed** (high confidence): both command outputs, base and worktree
  counts, the 08:57:18Z false green, regex behavior, file contents and
  author lines, append-integrity result.
- **Inference**: the planner's intent that 15 is the historical population
  and that `round-20-verifier-spotcheck.md` is outside it (supported by its
  own first paragraph); that `round-21.md` should be reported separately is
  a recommendation for Main, not an observed contract.
- **Unresolved**: (a) whether any gate's admits/rejects are fabricated or
  whether “independent review” is overclaimed — not countable, needs the
  non-author reviewer; (b) whether a knowledge entry will be added before
  integration (the `EXPECTED = 21` assertion fails loudly by design);
  (c) heading matches inside fenced blocks are not exercised in current data,
  so the strict regex is preferred but still line-based, not fence-aware;
  (d) provenance is not machine-readable in filenames or front matter, so the
  C2 allowlist must be maintained explicitly.

File changes: this report only
(`.ufo/waves/round-21/w1/CountingRecipes.md`). No lane file was modified, no
commit was made, and no credential/auth file was read.
