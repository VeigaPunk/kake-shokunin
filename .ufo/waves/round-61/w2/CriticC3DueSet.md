# CriticC3DueSet

## Axes
- **Freshness:** due-set selection and recheck/pin evidence correctness.
- **Operability:** counter detects violations of its frozen conditions.

## Counterexample and evidence

- **Due-set recomputation:** base `9f07731a873585e655a6518233ea39f5d9fb8204` has 16 non-rejected rows opened `2026-10-19` (S001–S016; S015/S016 are queued and correctly included; S017/S018 are rejected and excluded). Sorting the tie numerically by id selects S001–S010. The pending worktree registry appends S430–S433 opened later (`2026-10-27`), leaving the same oldest date, 16-way eligible tie, and due set. The C1 implementation matches this rule: status `!= rejected`, oldest opened date, numeric-id sort, first ten (`c61_recheck_pins.py:340-380`).
- **“Ten oldest” wording:** imprecise shorthand if read as chronological ordering of ten individual rows; here 16 share the oldest date, and the frozen operational rule explicitly resolves the tie by lowest id. No competing due set arises from the observed base or pending measured rows. Recommend describing it as “the ten lowest-id non-rejected rows among those with the oldest opened date,” rather than relying on “ten oldest.”
- **Date arithmetic:** all opened dates are `2026-10-19`. `+90d = 2027-01-17`; `+365d = 2027-10-19`. The pending registry pins S002–S007 to the former and S008–S010 to the latter; each equals its inclusive upper bound. S001 remains `on-release`, as the quote seat found its line-addressed anchor moved. The fetch/quote reports support this carry: S001 HTTP 200, but `include-hidden-files` is absent from the fetched v4 action file and the cited lines do not locate the named material; the second (main-commit) URL was not fetched. The proposed Gate note names `anchor_moved` and retains the cadence (`ExecC3Pins.md:67-83`).
- **Receipts:** worktree `receipts.json` has ten entries, each HTTP 200, `round61`, fetched on `2026-10-27` UTC; hashes of all ten local bodies match their receipts. S001/S002 receipts name the first of each row’s two URLs; both are members of the row URL set. S010 retains the fragment URL and has a fragmentless effective URL.
- **Pin-or-note completeness is not currently demonstrated by the lane state:** the observed Git HEAD is `f5a9b8acc8e4d0995e8ba849c4a9d56ba1ab0a8f`; at that committed revision `corpus/SOURCES.md` equals base, and round-61 lesson/recheck S010 are absent. In the worktree, nine pins are applied, but `corpus/lessons/round-61.md` remains untracked and its Gate lines contain placeholders. Thus C3/C5 cannot pass against the current committed revision; this is an integration/state limitation, not evidence that the planned nine pins are wrong. Do not call the worktree a measured committed revision.

## Counter defect / smallest safe correction

Frozen C4 says **each retained body** has a receipt carrying sha256, bytes, HTTP 200, fetchedAt on access date, `round61` userAgent, and URL equal to a row URL. The counter enforces all these checks for pinned rows (`violations`, around lines 541–589), but for carried rows it checks only sha256 and byte length (`c61_recheck_pins.py:600-617`); it merely records the carried receipt status. A counter mutant can change S001’s receipt status, date, userAgent, or URL and still pass C4 while S001 remains carried. That is a concrete false-green against frozen C4, regardless of the current S001 evidence being valid. **Smallest correction:** apply the same `violations()` checks to carried rows too; if the contract intends a weaker exception for non-200 carries, amend the frozen C4 text explicitly before scoring, rather than leaving the counter weaker than the declared condition.

C6 correctly compares every base non-due row’s raw line, and due rows’ only allowed cell change is `recheck`; appended rows are permitted (`c61_recheck_pins.py:650-684`).

## Impacted axes
- Freshness: due-set and date pins are stable/correct on observed data; Gate evidence remains uncommitted/incomplete at the observed HEAD.
- Operability: C4’s carried-row validation gap can admit false evidence while reporting all six conditions passed.

VERDICT: Due-set and date arithmetic withstand the observed counterexample; “ten oldest” should be clarified, but the material defect is C4’s weaker carried-row receipt checks, which need parity with the frozen condition before a clean C3 verdict is trustworthy.