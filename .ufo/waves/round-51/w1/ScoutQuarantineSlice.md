# Scout quarantine slice — kake, round 51 wave 1

Read-only. No cited source was fetched. Nothing was adopted or appended. The only write is this file.
No tool was installed or upgraded.

Axes walked: **freshness** (register HEAD vs the lane's current registry), **fidelity** (committed
slice vs a verbatim re-derivation), **accounting** (slice size vs the register's own tallies).

## 1. Filter and provenance

The round-51 item says "the awk filter in the round prompt" but does not quote it. The literal text
exists in the round-50 prompt source, `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-50/make_spec_w1.py:93`:

```
awk -F'|' -v l='kake' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}'
```

Provenance check that the reconstruction is the intended filter: running it against the register
reproduces the round-50 committed slice byte-for-byte (`diff` exit 0; both 453 bytes, 12 lines).
The round-51 spec (`make_spec_w1.py`, `w51-spec.json`, `w51-taskcall.json`) contains no filter text
at all (`grep "exact filter"` and a search for the literal pattern both return no hits).

Run verbatim against `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`,
exit 0, output:

```
 S142   `payload-absent` 
 S143   `payload-absent` 
 S148   `payload-absent` 
 S156   `payload-absent` 
 S161   `payload-absent` 
 S193   `payload-absent` 
 S194   `payload-absent` 
 S195   `payload-absent` 
 S206   `payload-absent` 
 S154`   the cited source could not be fetched, so no quote was checked 
 S178`   the cited source could not be fetched, so no quote was checked 
 S184`   the cited source could not be fetched, so no quote was checked 
```

## 2. Row count and S-id integrity

- **Row count: 12** (`wc -l` = 12, exit 0).
- **Every line carries an S-id: yes, 12/12.** The `$4` cell of all 12 matched
  `^[[:space:]]*S[0-9]+`?[[:space:]]*$` (`grep -c` = 12).
- Three of the ids carry a **stray trailing backtick** (`S154\``, `S178\``, `S184\``). That is the
  register's own defect, not the filter's: all **109** rows of the register's second table carry it
  (`grep -cE '^\| `[a-z0-9-]+` \| round[0-9]+ \| S[0-9]+` \|'` over lines 264+ = 109; zero rows of that
  table have a clean id).
- The ids, in filter order (normalized):
  **S142, S143, S148, S156, S161, S193, S194, S195, S206, S154, S178, S184**.
- Classes as the register writes them: nine `payload-absent` (S142, S143, S148, S156, S161, S193,
  S194, S195, S206) and three "the cited source could not be fetched, so no quote was checked"
  (S154, S178, S184).

## 3. Comparison with the committed slice

`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-51/assimilation/quarantine-slice`
(432 bytes, 12 lines; committed at `19a99bd`, 2026-10-24 23:20:47 -0300):

- Same 12 ids, same order, same row count: **re-derived content agrees**.
- **Not byte-identical.** Verbatim `diff -u` shows 24 changed lines = all 12 lines, and a
  backtick-stripped `diff` between both sides exits **0**. The committed slice is the filter output
  with every backtick removed (453 → 432 bytes = 21 backticks).
- Consequence: stripping the backticks also erases the register's stray-backtick defect on S154/S178/
  S184, so the committed slice renders those ids as clean, and renders `payload-absent` as bare text
  (it reads like a verdict rather than a backticked class token).
- The slice is tracked, and at lane tip `9d13768` the blob sha (`9c095eda…`) equals
  `git hash-object` of the worktree file; `git status --porcelain` for the path is empty. No
  post-commit drift.
- Later corroboration (not my basis — it appeared at 03:40:16, after my derivation): another seat
  wrote untracked `assimilation/quarantine-slice.raw` plus `.argv.txt`, whose note says the committed
  "quarantine-slice normalized away backticks". That `.raw` is byte-identical to my filter output and
  to the round-50 slice (`sha256 6d92f440…`, `diff` exit 0). It confirms the backtick-only delta; it
  does not change the comparison verdict above.

## 4. Accounting: 12 in the slice vs 9 in the register's own kake tally

The register has two tables and the filter is section-blind (both place lane/round/id in `$2/$3/$4`):

| register section | rows | kake rows |
|---|---|---|
| `## Rows` (`payload-absent`, well-formed 7-column table) | 194 | 9 |
| `## By lane` (sum over 19 lanes) | **194** | **`kake` 9** |
| `## Rows whose quotes were NEVER CHECKED` | 109 | 3 |

So the committed slice's 12 = 9 fabrication-class rows + 3 never-checked rows. The register's own
kake tally is **9**, and the register's second section says those three "are not fabrications and
they are not confirmed" (commit `d4ab45f2`: "cannot be seen is not demonstrably absent"). A reader
comparing the slice to the register's by-lane table sees 12 vs 9 with no marker in the slice
explaining the gap.

Also: the bare S-id is **not a global key** in this register. Seven of the twelve ids also occur under
other lanes (S142 `kumitate` round4 + `tabi` round3; S143 `tabi`/`tameshi`/`kumitate`; S148 `tabi`;
S154 `tabi`; S178 `kumitate` round8; S195 `mado`; S206 `kama`). Adoption or cross-lane matching by
id alone would be ambiguous.

## 5. Registry presence (adoption basis)

For each of the 12 ids, `git show HEAD:corpus/SOURCES.md | grep -cE "\| <id> \|"` → **0**, and
`grep -cE "\| <id> \|" corpus/SOURCES.md` → **0**. All twelve: S142 0, S143 0, S148 0, S154 0,
S156 0, S161 0, S178 0, S184 0, S193 0, S194 0, S195 0, S206 0 (HEAD and worktree).
**No slice id is in the lane's live registry**, so there is nothing here to adopt even if it were
desirable.

## 6. Freshness evidence

- Register `HEAD` = `d4ab45f2` (2026-10-24 08:37:10 -0300); `git status --porcelain` on the file is
  empty and `git diff --stat HEAD` is empty → worktree bytes == HEAD bytes.
- The slice commit (23:20:47) postdates the register commit by ~14 h, and the register has no later
  commit, so there is no drift window between the derivation and the commit.
- The census the register is generated from (`quote-lint-full-v5.json`, same commit) already contains
  the lane's newest registry ids: S249 (5 findings), **S262 (3)**, **S263 (7)**, S273 (1), S274 (5),
  S286 (11). The register's input is current with respect to the round-51 registry tail.
- Observation, not a defect: 23 of the 145 registry ids have no per-quote finding in that census
  (S001–S017, S022, S023, S026, S028, S029, S030). Registry rows carry no quote column, so a missing
  finding is consistent with "no quote attached to that row"; I did not verify each row's lane docs,
  so I do not call this staleness.

## 7. What the committed bytes do and do not prove

Proved: at register `d4ab45f2`, the filter yields 12 kake rows with the 12 ids above and the committed
slice has the same ids in the same order.

Not proved by the committed slice: byte-fidelity to the filter (it fails, backticks stripped, no
generating command recorded anywhere in round-51); class separation (9 fabrication-class vs 3
never-checked rows are merged); global id uniqueness (seven ids are shared with other lanes);
registry presence (all 12 absent).

## Remaining unknowns

- The literal round-51 prompt text is not on disk anywhere under the lane; the filter was taken from
  the round-50 prompt file and validated by reproducing the round-50 committed slice exactly.
- Whether the backtick stripping in the round-51 slice was deliberate: the commit that introduced
  the slice records no generating command (`grep` for `quarantine-slice` in the round-51 scripts hits
  only the spec text). The later untracked `.argv.txt` names only the verbatim awk run into `.raw`
  and states the committed file "normalized away backticks"; it records no normalization command and
  no rationale.

Report: .ufo/waves/round-51/w1/ScoutQuarantineSlice.md
