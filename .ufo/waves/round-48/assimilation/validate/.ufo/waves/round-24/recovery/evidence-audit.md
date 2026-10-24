# Round 24 inherited evidence audit

Read-only inventory of the inherited round-24 wave, measurement, census, session, and Git evidence. This is a documentary audit, not an independent admission or a rerun of any assignment.

## Wave sizes, mixes, and returned reports

| Wave | Declared seats and mix | Report files | Accounting |
|---|---|---|---|
| W1 (`kake-r24-w1`) | 72 registry members: scout 18, reviewer 15, executor 9, mutation-tester 8, revenger 8, scribe 6, critic 4, sentinel 2, connector 1, simplifier 1. Work is chiefly freshness/path inventory plus C1/C2 counter, gap, source, review, and writing tasks. | 55 Markdown reports in `w1/`. Their basenames match the non-death registry seats. | `w1-deaths.json` records 17 dead, unreplaced seats; its 17 names are exactly the registry/report set difference. The file has 55 returned reports and 17 deaths. All reports remain author-side. |
| W2 (`kake-r24-w2`) | 64 registry members: reviewer 19, mutation-tester 17, executor 10, critic 6, scout 4, revenger 4, connector 1, sentinel 1, scribe 1, simplifier 1. The spec has 30 freshness and 42 operability axis assignments (eight seats have both); task groups are 19 `FalsifyPathT01–T19`, 26 `ReplayCases01–26`, three source reopens (S032–S034), six mutation reviews, and ten boundary/review/pipe/scribe/sentinel tasks. | **0** Markdown reports; `w2/` contains only `swarm-registry.json`. | The 64 registry declarations have no returned-report/status fields. The durable interruption inventory records 0 reports, no replacements, 62 aborted requests, one provider 429, and one interrupted-without-final. |

The interruption inventory records coordinator termination at `2026-10-21T12:22:15.004Z` with `cyber_policy`, and says admission is paused pending complete falsify-wave reports and non-author closure. Do not retry, rephrase, or route around that refusal. Its inventory observation time is `2026-10-21T12:35:43.314531+00:00`. I inspected selected W2 transcript artifacts only for any final substantive finding: sampled W2 `.md` artifacts were empty; the `SimplifyFinalReplay` artifact is canceled/no-final and its visible late tool result repeats a W1 `SimplifyReplayPort` excerpt. No completed W2 finding can be credited from those partial records. The transcript records are not substitute reports.

## Recorded measurements

The files are inherited JSON results, not measurements rerun for this audit. `recovery/provenance-audit.json` explicitly describes its method as a documentary Git-blob/digest audit and says no gate, selftest, or probe was rerun.

| Stage | Revision | C1 path counter | C2 replay counter |
|---|---|---:|---:|
| Baseline (`measure-c1-before.json`, `measure-c2-before.json`) | `ab85dbdba4499f35f7dab9c9635b9b605679dbe5` | exit 1; 0/19 accepted | exit 1; 81/130 correct (61/110 rejects, 20/20 accepts) |
| C1-only intermediate (`measure-c1-c1-only.json`, `measure-c2-c1-only.json`) | `3d07733b482f88c42cb008397188237c80e42b67` | exit 0; 19/19 accepted | exit 1; still 81/130 (61/110 rejects, 20/20 accepts) |
| Final implementation (`measure-c1-after.json`, `measure-c2-after.json`) | `faace82dcf50e1c563d437f2caecb77a9a865880` | exit 0; 19/19 accepted: 3 drift, 12 new-missing, 4 recovered | exit 0; 130/130 correct (110/110 rejects, 20/20 accepts) |

The C2 result identifies fixture base `f7de3ab4e9f030a15a857a5a08631bd8e690f436` and population SHA-256 `16da1936f30e2e7bfa405d9b51dfc18ab686edbd9f1d36f65d76626b0cab7b8f`. Final control JSONs at `faace82` record C1 17/17 with claim counts HOLD 79, STALE 55, UNVERIFIABLE 42, and C2 12/12 with 3 clean, 5 failed-policy, 4 not-served. These are local author-side results; they do not fill the missing W2 falsification or establish admission.

## Source-census evidence

`recovery/source-census.json` records:

- Before, revision `f7de3ab4e9f030a15a857a5a08631bd8e690f436`: 31 rows (A 29, C 2); statuses mined 27, queued 2, rejected 2.
- After, revision `faace82dcf50e1c563d437f2caecb77a9a865880`: 34 rows (A 32, C 2); statuses mined 30, queued 2, rejected 2.
- Added rows S032, S033, S034; `oldRowsChanged` is empty.
- Recorded validator invocation: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`; exit 0. Its stdout includes `W04 S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes`, followed by `kake ok` for `corpus/SOURCES.md`.

This is the recorded census result and validator output, not an independent source recheck.

## Committed versus uncommitted outputs

At the pre-report Git observation, HEAD was `faace82dcf50e1c563d437f2caecb77a9a865880`, commit timestamp `2026-10-21T09:18:12-03:00`, subject `round-24: harden receipt replay with typed parsing and safe rejections`. There were 98 tracked paths under `.ufo/waves/round-24`; 56 under `w1/` (55 reports plus registry) and 19 C1 receipts. Those tracked W1 reports/receipts were clean at that observation. The report inventory of 55 W1 outputs is therefore committed, but the updated death ledger is not.

The pre-report `git status --short --untracked-files=all -- .ufo/waves/round-24` had 21 entries: one modified tracked file, `w1-deaths.json`, and 20 untracked outputs:

- `c1-selftest.json`, `c2-counter-selftest.json`, `canonical-matrix.json`, `canonical-selftest.json`, `corpus-contract.json`, `gen_w2.py`, `implementation-suite.json`, `measure-c1-after.json`, `measure-c2-after.json`, `replay-c1-control.json`, `replay-c2-control.json`, `replay-selftest.json`, `sweep-selftest.json`;
- `w2-dispatch.json`, `w2-spec.json`, `w2-taskcall.json`, `w2/swarm-registry.json`;
- `recovery/interruption-inventory.json`, `recovery/provenance-audit.json`, `recovery/source-census.json`.

The before/intermediate measurements and populations are among the unchanged tracked artifacts. This audit file is being added under the requested recovery directory, so it is a further uncommitted report not included in the pre-report status count.

## Tool-install claims in W1 reports

A search across the W1 report files found one positive tool/interpreter-install claim: `w1/SourcePythonDatetime.md:72` records installation of CPython 3.10.22 and 3.15.0 using `uv python install 3.10 3.15`, uv 0.13.0, via the uv-managed interpreter channel, to compare the pre-3.11 boundary with the current documentation version. Line 74 clarifies that no Python packages or lane production files were installed/edited. Other install mentions found in W1 reports are negative disclosures or references to existing tools, not additional install claims. No tool was installed or updated for this audit.

## Limits and disposition

- No W2 report was returned; no dead/aborted seat was retried or credited. No independent falsification or non-author closure is evidenced.
- Partial transcript content is not promoted to a finding. The W1 measurements, selftests, counter outputs, and source-census JSON remain local author-side evidence.
- This audit did not run tests, builds, probes, or validators, and made no lane, corpus, index, jj, fleet, sibling, or configuration edits; only this uniquely assigned report was written.
