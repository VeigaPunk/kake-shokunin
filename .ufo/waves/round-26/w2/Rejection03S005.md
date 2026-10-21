# Rejection03S005: falsify L1's rejection of the S005 verification-date stamps

- Target: L1 disposition for `S005 × corpus/knowledge/ghp-custom-domain.md`, seat findings C1 (P02, line 2) and C3 (P09, line 17). The seat marked both STALE; L1 rejected them as historical (`statements.json` pair S005: `"seatStale": 3, "stale": 0`, l1Disposition "C1/C3 verification-date stamps are historical records, not wrong content").
- Candidate `e28312b`, base `97404de`. Judged on: freshness. Milestone: r26-recheck-falsify.
- **Verdict: AGREE.** Lines 2 and 17 are correct at their stated scope. Every S005 sentence they vouch for is still verbatim in the round-26 retained bytes, and in a live GET made today. Rejecting these findings therefore hides no staleness.

## Axes

1. **Claim truth at stated scope.** Is the 2026-10-19 date false?
2. **Content drift behind the stamp.** Did any S005 text vouched for by lines 2 and 17 change?
3. **Rule conformance.** Does the rejection follow QUALITY "Recheck adjudication — round 26" and the round-21 provenance and coordinate rules?
4. **Hidden-staleness consumers.** Does any tool read `verified-at` as current state, so that an old stamp would mask a due recheck?

## Evidence

### Axis 1: the dates were true when written

- `git log --format='%h %ad %s' --date=iso -- corpus/knowledge/ghp-custom-domain.md` gives three commits:
  - `02b6dd0 2026-10-19 19:38:03 -0300 round-20: resume …` (the file is created with both lines)
  - `9639ec7 2026-10-19 20:08:51 -0300 round-20: post-review fixes` (appends the S007 erratum only)
  - `e28312b 2026-10-21 …` (+4 lines appended at EOF, 0 deletions)
- `git show 02b6dd0:corpus/knowledge/ghp-custom-domain.md` already contains:
  - line 2: `verified-at: 2026-10-19 (GitHub Docs and REST API opened 2026-10-19)`
  - line 17: `**Source checks (quotes reopened 2026-10-19).**`
- Both lines are dated by authorship in a 2026-10-19 commit. Neither claims to be the latest verification, so a later reading does not falsify them. The round-21 rule (`corpus/QUALITY.md:46-48`) says "A provenance header records the original evidence date/revision". That is what line 2 does.

### Axis 2: no drift behind the stamp

Checked in-memory against `fetched/S005-1.raw.gz`:

- The gunzipped bytes are 240439 long with sha256 `dc89eecdf00c22581f1d85dd5c429d63e3d206f7d7a946c3c2f752a023e0cee9`, which equals the `manifest.json` S005 record (status 200, `fetchedAt` 2026-10-21T15:09:34.843922+00:00).
- Counts in the text view `text/S005-1.txt`:

| Phrase | Count |
|---|---|
| "no CNAME file is created, and any existing CNAME file is ignored" (line 18–19 quote, backticks removed) | 2 |
| "this will create a commit that adds a CNAME file directly to the root of your source branch" (line 19–20) | 2 |
| "We recommend verifying your custom domain prior to adding it to your repository" (line 20) | 1 |
| "We strongly recommend that you do not use wildcard DNS records" (line 21) | 3 |

- Ordered list under `id="configuring-an-apex-domain"`: item 4 is `Under "Custom domain", type your custom domain, then click Save. If you are publishing your site from a branch, this will create a commit …`. The "step 4" locator on line 18 holds. Item 3 now names the sidebar section "Code, planning, and automation". This is a step-3 label, not one of the vouched sentences.
- **Live comparison (plain public GET of the S005 URL from `corpus/SOURCES.md:13`, held in memory, not saved):** 240439 bytes, sha256 `6f3d1ad2…6be4`. A `difflib` byte diff against the retained raw gives 20 non-equal opcodes, all short hex or nonce tokens (`'91b7'→''`, `'2ebc7ccb0'→'4944693'`, …). These are build identifiers, not prose. The four phrase counts are identical in both copies (2/2, 2/2, 3/3, 9/9 in the whole-page text).

Conclusion: the content vouched for by both stamps is unchanged from 2026-10-21T15:09Z to now, and nothing in it is wrong.

### Axis 3: the rejection follows the rules and records the note the rules require

- `corpus/QUALITY.md:217-221`: "STALE means the statement is wrong or unsupported at its own stated scope. A historical verified-at date … is not a stale claim; record it as a note."
- `statements.json` `rule`: "Historical dates and base-scoped pointers are not stale."
- The note is recorded. The appended section in the candidate (`ghp-custom-domain.md`, "## Round-26 source recheck") says that S003, S005 and S007 were re-fetched 2026-10-21 and judged HOLD. It adds: "Older verified-at/reopened dates in this entry remain the historical record of the earlier reading; they are not rewritten."
- The round-21 "names whether that evidence is historical" requirement (`QUALITY.md:46-48`) is met by that appended sentence. Rewriting line 2 inline would break "Metadata prefixes preserve every prior byte" (`QUALITY.md:53`).
- `corpus/lessons/round-26.md:55-58` lists "verification-date stamps (S005×2, S020, S021) — a historical date is not a false claim". This matches the ledger.
- The C2 part of the disposition was checked as a consistency spot check only. `git show cb807bc:corpus/knowledge/publish-channels.md` line 9 is "`CNAME` file pins `ds4cc.com`.", which matches the statement at its "at base `cb807bc`" label.

### Axis 4: nothing treats `verified-at` as current freshness state

- Running `grep -rn -i 'verified-at'` over `*.mjs`, `*.py` and `*.js` finds it only in `scripts/corpus-contract.mjs`, the shape check "non-empty in first 8 lines", whose header says "shape, not truth". It also appears in the historical `round-21/measure.mjs`, whose semantics say "not evidence of absent live verification".
- `scripts/freshness-sweep.mjs` has no `verified-at` read.
- So the 2026-10-19 stamp drives no due-date calculation. Even if a tool did read it, an older date would make the recheck due sooner, not later. The stamp cannot mask staleness.

## Strongest counterexample tried, and why it fails

The case for STALE is: "`verified-at` should mean the latest verification. After the 2026-10-21 fetch, line 2 understates freshness, and line 17 implies the quotes were last reopened on 10-19." Two things defeat it:

- **(a) No tool or rule defines it that way.** No contract or tool assigns `verified-at` "latest" semantics; QUALITY round 21 defines it as the *original* evidence date.
- **(b) The error would point the safe way.** Understating freshness is conservative. "Wrong at stated scope" requires the claim to be false, and both lines state a 10-19 event that did happen (Axis 1). The vouched content still holds (Axis 2).

The only true STALE path would be a changed S005 sentence, and none changed.

## Residual observations (not defects in this rejection)

- The `corpus/SOURCES.md:13` S005 registry row still reads "fetched 2026-10-19" in its anchor cell and `opened 2026-10-19`. This is seat flag F3, and it belongs to the row target, not to lines 2 and 17. The round-26 "bounded recheck" paragraph that the candidate added to SOURCES.md records the 2026-10-21 re-fetch, so no reader is misled about the latest verification.
- The REST API clause on line 2 and the S003 quote under line 17 belong to the S007 and S003 pairs and were not judged here.

## Commands run

- `git log`, `git show 02b6dd0:…`, `git show 97404de:…`, `git show cb807bc:corpus/knowledge/publish-channels.md`, `git diff 97404de e28312b -- …`, `git diff --stat`: all read-only.
- In-memory `python3`: manifest read, gunzip plus sha256, phrase counts, apex `<ol>` item listing, one live `urllib` GET of the S005 HTML URL from SOURCES.md, and a `difflib` comparison. Nothing was written.
- `grep` and `sed` for reads over scripts, QUALITY, lessons and SOURCES. No round-24 material was read; one `git log` listing showed a round-24 commit subject on `publish-channels.md`, which was not opened.

## Tooling

No installs or upgrades. Tools used: the existing python3 (stdlib), git and grep. pacman was not touched (host-wide pause).

```json
{"target":"S005 l1Disposition C1/C3 (ghp-custom-domain.md lines 2,17)","verdict":"AGREE","severity":"none"}
```
