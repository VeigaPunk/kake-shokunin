# ReviewerCounterDataflow — counter review

## Finding (actionable; frozen counter remains untouched)

**High: resolution is gated by presence markers, not proof that the S432 disagreement was substantively resolved.** `.ufo/waves/round-62/c62_calibration.py:33-38` sets correction/criterion/lesson_gate/source_row from literal substring checks. In particular, `criterion` only requires `substantive located quote` and the spotcheck filename anywhere in QUALITY (`:35`); it never verifies the criterion text actually distinguishes substantive evidence from a generic lead-in, includes admit/reject behavior, or is grounded in the cited disagreement. `correction` similarly checks the quote and two labels anywhere in the knowledge blob (`:33-34`), without requiring the quote to be attached to the S432 correction or that the cited excerpt supports the row. `lesson_gate` accepts the four tokens anywhere (`:36-37`). These can be satisfied by unrelated prose / fabricated boilerplate while leaving the disputed knowledge citation and QUALITY guidance unchanged. A committed revision can therefore report `met=true` despite no semantic learning or correction. This is a false-positive route in the frozen counter's proof, not a recommendation to alter the frozen predicate.

**High: the raw disagreement count is not S432-row scoped.** At `:31-32`, every line containing both `S432` and `Disagree` is counted, regardless of whether it is an actual table row, and resolution sets `unresolved=0` whenever the presence checks pass (`:39-41`), irrespective of count or identity. The counter thus does not evidence that the unique retained verifier disagreement remains present and was specifically resolved; arbitrary matching text can inflate the count, and any matching strings elsewhere can be zeroed by unrelated markers.

**Medium: source-row existence is a weak substring check.** `:38` tests only `"| S432 |" in SOURCES`; this does not establish a valid source-table row, row uniqueness, or correspondence to Fetch URL / retained section. Empty/missing blobs other than spotcheck silently become `""` in `blob` (`:19-24`), so missing lesson/QUALITY/SOURCES become ordinary false conditions rather than explicit evaluation errors. Base audit recorded the round-62 lesson absent at base, which is expected for the new artifact, but means this gate is not a base-existing lesson proof.

## Revision-bound dataflow

The measurement input is appropriately sourced from Git blobs: `:19-24` invokes `git -C root show rev:path`, and `:26-27` loads the five `PATHS` at the supplied revision. It does not read working-tree corpus data. `BASE` is the specified commit (`:8`); the existing independent scout report confirms it resolves as a commit and confirms four paths exist while `corpus/lessons/round-62.md` is absent at base (`.ufo/waves/round-62/w1/ScoutCounterDataflow.md:3-7`). The base-control values are supplied in the assignment, not rerun here.

## Evidence / commands

- `read /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-62/c62_calibration.py:19-43` — exact Git blob read and weak marker aggregation described above.
- `read /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-62/w1/ScoutCounterDataflow.md:3-7` — recorded commit/root and path-existence checks.
- `read .../.ufo/waves/round-62/contract.md:5-10` — frozen claim requires the disagreement to be learned through corrected citation and grounded QUALITY criterion; source boundary says quote supports purpose, not live property headers.
- No LSP device is mounted in this environment (`read xd://lsp` returned “No such tool: xd://lsp”); no code semantic references/diagnostics were available. Counter is a standalone script with no caller analysis claimed. No commands executed against the counter; no claim, counter, criterion, score, or lane file other than this report was changed.

## Residual risk / verification gaps

The counter validates token co-occurrence, not semantic support. Manual review of the committed knowledge correction, QUALITY criterion, lesson Gate, and retained S432 source remains necessary before accepting a passing measurement. In particular confirm the corrected citation is attached to the intended knowledge claim and does not overstate nosniff value grammar, and preserve the round-61 Admit/Disagree row. No independent post-change execution or after-state is asserted.
