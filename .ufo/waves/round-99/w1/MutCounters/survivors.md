# MutCounters survivors (round 99, w1)

Source: `mutants.tsv` (this directory). Probes below were run by `harness.py probes` and
`fr15probe.py` (outputs in `probes.txt`, `fr15.txt`). A survivor here means the frozen controls
and the counter's own selftest did not flip; "separated" means a fixture input on which the
pristine counter and the mutant differ in verdict (met/rc), run after the mutant was generated.
A probe is a recipe for the next round's controls, not a control kill.

## Registry counter (`c99_registry.py`)

- **RG01 owner dropped from REQUIRED.** Input: a registry table with columns
  `Name | Kind | Entry command | Verdict map | Self-test | Write scope` (no Owner), one row for
  `scripts/a.py`. Pristine: `unlisted=1 met=false`, rc 1. Mutant: `KeyError: 'owner'` traceback,
  empty stdout, rc 1. Separated (crash, not a verdict). Every control table has Owner, so no control reaches this.
- **RG03 names_path trailing boundary dropped.** Entry `` `python3 -B scripts/a.pyx` `` (self-test
  `scripts/a.py --selftest`). Pristine rc 1 `unlisted=1`; mutant rc 0 `listed=1 met=true`. Separated.
- **RG04 names_path leading `=` dropped.** Entry `` `python3 -B --file=scripts/a.py` ``. Pristine
  rc 0 `met=true`; mutant rc 1 `unlisted=1`. Separated. (No control uses `--x=path` form.)
- **RG05 verdict `0` at cell end dropped.** Verdict map `` `1` failed; exit 0 ``. Pristine rc 0; mutant rc 1. Separated.
- **RG06 verdict `1` lookbehind dropped.** Verdict map `` `0` clean; `21` odd ``. Pristine rc 1 (no
  standalone 1); mutant rc 0 (false pass on `21`). Separated.
- **RG07 owner compared on 4-char prefix.** Owner cell `kakeX`. Pristine rc 1; mutant rc 0. Separated.
- **RG09 owner backtick-strip dropped (mutant stricter).** Owner cell `` `kake` ``. Pristine rc 0;
  mutant rc 1. Separated. No control backticks its owner cell.
- **RG11 forbidden-backtick dropped — EQUIVALENT.** `SPAN` is `` `([^`]+)` ``, so no span can contain a backtick; the check cannot fire. Not separable; counted as survived.
- **RG18 `.mjs` population filter dropped.** Files `scripts/a.py` (selftest-capable) and
  `scripts/c.mjs`; one row for a.py. Pristine rc 1 `tools=2 unlisted=1 met=false`; mutant rc 0
  `tools=1 met=true`. Separated. On the committed controls only the detail changes
  (`probe-delta.mjs` leaves the unlisted list in base-c1), so no met flip in controls.
- **RG19 dangling `.mjs` token not detected.** Row for a.py plus row whose entry is `` `node scripts/ghost.mjs` `` (file absent). Pristine rc 1 `dangling=1`; mutant rc 0 `dangling=0 met=true`. Separated.
- **RG23 `no self-test` phrase case-sensitive.** Row for `scripts/b.py` (no `--selftest`) with self-test cell `No self-test`. Pristine rc 0 listed; mutant rc 1 unlisted. Separated (`probes.txt`). Control run NOT-RUN.
- **RG27 table-row contiguity dropped.** Table: header, separator, row a.py, line `<!-- note -->`, row for `scripts/b.py` (self-test `no self-test`). Pristine rc 1 `unlisted=1`; mutant rc 0 `unlisted=0`. Separated (`probes.txt`). Control run NOT-RUN.
- **NOT-RUN, no verified separator (analysis only, [INFERENCE]):**
  - RG24 (`no self-test` accepted for a tool that has `--selftest`): the existing selftest case `no-selftest-claim-false` should flip; batch-1 claim unverified.
  - RG25 (`\|` escape protection dropped in SPLIT): the committed `cache_key.py` row with `` \| `` inside a code span should mis-split; batch-1 claim unverified.
  - RG26 (`selftest` header alias dropped): a table whose self-test column is headed `Selftest` should be ignored by the mutant; no control has this header.
  - RG28 (escaped-pipe trailing-cell check dropped): not separated.
  - RG29 (sibling `*selftest*` file match dropped): the existing selftest case `separate-selftest-file` should flip.

## Fresh304 counter (`c99_fresh304.py`)

- **FR01 etag `!` (0x21) dropped.** Stored and response `ETag: "!"`. Pristine `update/strong`; mutant refusal. Separated (direct reference call). Control run NOT-RUN.
- **FR02 obs-text upper bound 0xFF → 0xFE.** Stored and response `ETag: "\u00ff"`. Pristine `update/strong`; mutant refusal. Separated. Control NOT-RUN.
- **FR03 etag length check lowered.** Stored `ETag: "` (one quote character), response `ETag: "x"`. Pristine refusal; mutant `must-not-update`. Separated. Control NOT-RUN.
- **FR15 generator bad-case rate zero.** The pristine generated set contains an `extra`-key refusal case absent from the mutant's set; a candidate that is wrong only on that input flips met. Input (from `fr15.txt`): `{"extra": 1, "response": {"headers": {"X-Foo": "r-3"}, "status": 304}, "stored": [{"headers": {"Content-Length": "94", "etag": "\"\u00e9\""}, "id": "s0", "received": 6}]}`. Pristine rc 1 `generated=239/240 met=false`; mutant rc 0 `generated=240/240 met=true`. Separated. The mutant still emits 20 refusal-class cases from ambiguous-tie grammar (not isolated further).
- **FR16 seed derivation XOR 1.** Seed differs (`3454273765` vs `3454273764`), outcome identical on the committed candidates. Separator: a candidate that is the oracle except on the first generated input present in `gen_case` output under `Random(int(BASE[:8],16) ^ 1)` and absent from `Random(int(BASE[:8],16))`. Pristine `met=true` rc 0; mutant `met=false` rc 1. Separated (`probes.txt`, truncated there; regenerate with the harness's `gen_set`).
- **FR19 empty connection token guard dropped — EQUIVALENT.** `""` can never be a header key (TCHAR rejects empty names), so adding it to the exclusion set changes nothing.
- **FR20 judge refusal stdout check dropped.** `judge(None, (1, '{"x": 1}', 'invalid_input: x'))`. Pristine `False`; mutant `True`. Separated. No control gives a refusal with stdout.
- **FR21 judge accepts rc 1 decisions.** `judge({"a": 1}, (1, '{"a": 1}', ''))`. Pristine `False`; mutant `True`. Separated. No control exits 1 with a correct decision.
- **FR22 NUL in header value admitted.** Response headers `{"X-V": "a\u0000b"}`, no stored entries. Pristine refusal; mutant `no-update`. Separated. No control or hand case carries a NUL.
- **Control-kill status unverified (NOT-RUN):** FR01, FR02, FR03 (batch-1 `met-None` results have the same empty-output signature as the disk-fault artefacts documented in MutCounters.md) and FR14 (`met = hp == len(HAND)`), whose batch-1 `pos-oracle rc 0->1` cannot be produced by this mutation and is therefore spurious.
