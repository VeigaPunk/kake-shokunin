# Round 21 · w1 · CausalSeparation (connector, read-only)

Lane: `kake-shokunin`. Base measured: `5009eca` (= the wave's shared base `5009ecaa1cce10b895617a585ddd3f7c7c923a84`).
Scope: check C1/C2 independently verifiable populations, the lowest-axis tie rule, the S019 frontier step against the claim cap, and whether a third capability claim is needed. Nothing was added or edited.

Measurement caveat: the working tree is being written by the wave's Knowledge scribes while this report was made. A knowledge-entry count read mid-wave gave 17/21 (`drift-detection.md` had just gained a `source:` line 1 that was absent at base). Only base-commit counts (`git show 5009eca:…`) are used below as the "before" state. Live counts are not stable until integration.

## 1. Axes named

| Axis | Score (SCORECARD, base) | Retired? | Role this round |
|---|---|---|---|
| freshness | 10 (ceiling) | no (SCORECARD §Retired: "NOT retired") | C1 |
| operability | 10 (ceiling) | no (only the free-read-verb sub-surface is retired, r12) | C2 as labelled (see §3.4) |

Saturation line 10/10 on both; stagnation window N=1 (SCORECARD §Saturation). Capability table has one row, "Curated source registry", first-working round 20 (resume). Because a capability entered inside the window, the stagnation nudge (AXES.md §The stagnation nudge) does not fire, and the lowest-axis obligation applies. SCORECARD says the same: "round 21 is **not** waived by the nudge."

## 2. C1 — freshness, knowledge provenance trio

**Population (base `5009eca`, `corpus/knowledge/*.md`): 21 entries.**

Trio check: `(?m)^<key>:\s*\S` over the first 8 lines, the SCORECARD command's own rule.
- Present: 4/21 (`crawl-scope-per-host.md`, `ghp-custom-domain.md`, `ghp-etag-anatomy.md`, `ghp-served-set.md`). This reproduces the SCORECARD "Before: 4/21" exactly.
- In order on lines 1–3 (`source`, `verified-at`, `recheck`): the same 4. The 8-line rule therefore cannot tell order or position apart from presence.
- To fix (17): `drift-detection`, `fire-journal-codes`, `fleet-registry`, `free-read-verbs`, `freshness-sweep`, `ghp-subpath-spotcheck`, `keeper-timer-inert`, `kimi-subpath-audit`, `mirror-pitfalls`, `ops-automation`, `origin-repos`, `probe-delta-alerting`, `publish-channels`, `publish-queue`, `sitemap-orphan-audit`, `speedrun-pipeline`, `vault-properties`.

**Independently verifiable?** Yes, on two conditions.
1. The after-count must be measured on a fixed commit, not on the moving working tree.
2. The planned count is weaker than the contract. CORPUS.md says the trio "come first" (lines 1–3). The SCORECARD command accepts it anywhere in the first 8 lines, including after a title or inside prose. A stricter count is `first3 == [source, verified-at, recheck]` plus a non-empty value. The 4 base entries pass it, so the stricter count does not change the before-state.
- Also: `(?m)^key:\s*\S` matches `source: ~` and similar placeholder values. "Honest metadata" is judged by reading, not by this regex.

**Causal separability: not clean as planned.** C1 is a pure prefix addition, so every line of the 17 files moves down by the number of inserted lines. Line-anchored pointers into those files go stale. Counted at base (regex on tracked text, bare `name.md:N` tokens included, approximate):
- 187 live line-anchored citations into the 17 targets across 16 files. Largest: `freshness-sweep.md` 61, `publish-channels.md` 27 (incl. `corpus/QUALITY.md:15` → `publish-channels.md:9`), `ops-automation.md` 15, `fire-journal-codes.md` 14, `sitemap-orphan-audit.md` 14, `probe-delta-alerting.md` 14, `free-read-verbs.md` 12, `publish-queue.md` 9.
- Aggregator-authored lessons that may not be edited cite the targets: `corpus/lessons/round-6-aggregator-audit.md` (pointers into `vault-properties`, `origin-repos`, `kimi-subpath-audit`, `ghp-subpath-spotcheck`, `fleet-registry`). Lane-authored `round-10.md` and `round-19-recensus.md` also cite them and can take tail corrections. Pointers in the aggregator lesson cannot be repaired in place.
- About 1508 historical `.ufo/` cites also point into the 17 targets. They are historical records and need no repair.
- `corpus/QUALITY.md` (L1-owned) is among the citers, so it needs an L1 correction.
- The QUALITY.md post-review ruling (`corpus/QUALITY.md:33-39`) allows an adjacent note "only with an inbound-anchor movement census and corrections for moved pointers; otherwise leave the location uncleared." C1 as planned ships without that census, so it is incomplete as written. Corrections must be new tail lines or new files, never in-place edits to aggregator lessons. Unrepairable pointers are named debt.

**S019 cite.** Drift-detection's new `source:` text names "S019 … metadata contract only (registration pending in L1 CORPUS.md)". S019 has no row (§5). Until L1 registers it, any entry that cites S019 cites a nonexistent row. Entries should cite the CORPUS.md path, or wait for registration.

## 3. C2 — lesson `## Gate` coverage (labelled operability)

### 3.1 Population
- `corpus/lessons/round-*.md` at base: 23 files.
- Excluded as aggregator (filename contains `aggregator`): 7 (`round-1-aggregator-audit`, `round-4-aggregator-audit`, `round-5-aggregator-audit`, `round-5-aggregator-mirror-pathless-cli-invocation`, `round-6-aggregator-audit`, `round-8-aggregator-box3-coldrun`, `round-9-aggregator-corpus-verdict`). Left: 16.
- Excluded as verifier/integrator-authored: `round-20-verifier-spotcheck.md`. Its header reads "Written by the integrator, not the lane." CORPUS.md says outside reviews are new files. Left: **15 lane-authored**, matching the claim's denominator.
- Authorship for the other 15 is taken from their titles and headers. I did not audit each file's commit author.

### 3.2 Numerator (base)
- `grep -l '^## Gate'` over the 16-file universe returns 1 (`round-20.md`). That is the SCORECARD "Before: 1/15."
- `round-20.md` has two gate headings: line 41 `## Gate` and line 182 `## Gate — round-20 resume`. The second also matches `^## Gate`.
- `round-8-aggregator-box3-coldrun.md` has one, but it is aggregator-authored and excluded.

### 3.3 Counting-command defects
- The SCORECARD command prints a numerator only. Its universe includes `round-20-verifier-spotcheck.md`. The "after = 15" claim is therefore not checkable by the command as written.
- Recommendation: enumerate the 15 files explicitly. Use `^## Gate$` (exact heading) so the round-20 resume heading is not counted as a second gate.

### 3.4 Axis fit (risk, not changed)
- AXES.md defines operability as "runnable artifacts: checklists that are executable, commands that exist, scripts that run … A checklist item can be run and produces the stated outcome."
- C2's measurement is a heading-presence grep. It shows documentation present, not an operability outcome.
- A lesson Gate records candidates, admits and rejects. AXES maps that to discernment/calibration. CORPUS.md says lanes without a Gate section "had nowhere to keep a rejection."
- SCORECARD says calibration "belong[s] to other lanes — not scored here."
- So if C2 is calibration, it is not a claim on an owned axis. The round then has one owned-axis claim (C1), and "two claims on the tied-lowest owned axes" overstates it.
- This does not block C1, but it must be resolved by L1 before the SCORECARD row is written.

### 3.5 Causal separability and gate content
- C2 is EOF appends only, so it does not move lesson line numbers. C2 is independent of C1 for lesson line numbers.
- It is **not** independent if a Gate cites a knowledge-entry line number. Gates citing knowledge lines must be written after C1, or should cite paths only.
- Historical gates must not invent admits, rejects or non-author review. Pattern already in use: `round-3.md:33`, "Retrospective round-21 reconstruction, not original admission … Rejected: not recorded." Reuse it.
- SOURCES rule 1: a round's Gate records URL, access date and quote for each new row. Historical gates add no rows, so no new source claims are needed.

## 4. Lowest-axis tie rule

- AXES.md §Working the axes: "At least one claim works the lane's **lowest-scoring non-retired axis**, except when the stagnation nudge waives it." Also: "two claims on one axis in one round count as one claim."
- AXES.md defines no tie-break. I did not open the PROTOCOL appendix "Multi-claim rounds" (PROTOCOL.md:96-97 cites it).
- Kake's practice when tied: LOG.md:443-444 and :478-479 chose freshness over operability on a falsifiable defect (the false-green). Round 20 was blocked, so that choice is not an admitted precedent.
- Round 21: both owned axes are 10/10. Either axis satisfies the obligation, so the tie does not bind. C1 alone satisfies "at least one claim on the lowest axis." C2 is optional for the obligation.
- Under the ceiling, C1 and C2 can only show HOLD, not a score change. Their before→after must be counts or verdicts, as SCORECARD already does.

## 5. S019 frontier step within the claim cap

- `corpus/SOURCES.md` registry: S001–S018 (18 rows, per SCORECARD census). S019 is the next unused id. There is no S019 row.
- Kake-tree mentions of `S019` at base: none. The only in-flight mention is the drift-detection edit described in §2. Shokunin-root `CORPUS.md` does not mention S019. The S019 references in `.ufo/` belong to other lanes.
- Rule: a row is written only after its source is opened in the writing round, with the Gate recording URL, date and quote (SOURCES rule 1). Only L1 writes SOURCES.md (the wave contract gives L1 SOURCES). So S019 is an L1 registration step, not a C1/C2 claim.
- Claim cap: registering S019 adds 0 claims. It is the PROTOCOL "Sources & frontier" record of rows before→after, not an axis move. Cap impact: none.
- Caveat: S019 would be a local `own-work` row pointing outside the lane repo (`/home/vgpnk/Projects/shokunin/CORPUS.md`). SOURCES says own-work anchors are repo paths or commands, so the row either needs a repo-relative anchor or a documented exception from L1.

## 6. Third capability claim: not needed (not added)

Reasons:
1. AXES §Capabilities: a capability enters only through a round that demonstrates it running. Round 21 has no capability it must demonstrate.
2. The nudge is off because the registry capability entered in round 20 resume (SCORECARD Capabilities table). The lowest-axis obligation applies, and C1 satisfies it.
3. Claim cap: AXES allows 1–3 claims on distinct axes. Two are declared. A third capability claim would still need its own axis verdict, and the source-registry capability already has its row. S019 is registry content, not a new capability.
4. SCORECARD already commits: "if round 21 adds no capability, round 22 should be a frontier/capability move." That is the planned place for a capability claim.

**What would flip this.** If L1 or the operator rules that the round-20 registry capability did not enter, the nudge fires: both owned axes are at the saturation line and no capability entered in the window. The round would then have to be a frontier/capability move, and a capability claim would be required. Round 20's C3 is still a self-verdict pending non-author verification (SCORECARD round-20 resume), so this is a real open decision. It belongs to L1/operator. I did not add a claim.

## 7. Decisions and actions for the parent (L1)

1. **C2 axis classification:** keep operability (then make the check executable, e.g. a script that validates each Gate's required sub-sections) or re-label as calibration/discernment, which this lane does not score.
2. **Round-20 capability status:** decide whether C3 counts as entered (controls the nudge, §6).
3. **C1 completeness:** add the inbound-anchor movement census and correction tails. Correct `corpus/QUALITY.md:15` and other L1-owned pointers via L1. Record aggregator-lesson pointers as named debt.
4. **C1 check strength:** use the first-3-lines-in-order check in addition to the 8-line presence count.
5. **C2 counting command:** enumerate the 15 files and use `^## Gate$`.
6. **S019:** register or drop it in SOURCES.md (L1 only). Until then no entry may cite S019 as a row.

## 8. Evidence

- Base counts: `git show 5009ecaa1cce10b895617a585ddd3f7c7c923a84:corpus/knowledge/<f>` (21 files; trio 4/21). Lessons: `git ls-tree` on the base (23 round-*.md; 1 `## Gate` file among the 16 non-aggregator files; `round-20.md` has `## Gate` at lines 41 and 182).
- Verifier authorship: `corpus/lessons/round-20-verifier-spotcheck.md:1-5`.
- Quality rules: `corpus/QUALITY.md:9-20` (criteria incl. "Population unit named"), `corpus/QUALITY.md:33-39` (append-only and inbound-anchor ruling).
- Axes/cap/nudge: `/home/vgpnk/Projects/shokunin/AXES.md` §Working the axes, §Capabilities, §The stagnation nudge.
- Contract: `/home/vgpnk/Projects/shokunin/CORPUS.md` lines 18-20 (trio, `## Gate`), 163-170 (trio "come first"), 112-115 (SOURCES rule 1).
- Scorecard: `SCORECARD.md` lines 19-34 (round-21 plan), 166-185 (round-20 resume claims), 206-211 (saturation and window), 216-226 (post-review ruling).
- Tie evidence: `LOG.md:443-444`, `LOG.md:478-479`.
- Inbound census: the tracked-text regex run described in §2 (`(?<![A-Za-z0-9_-])((?:corpus/knowledge/)?name.md):N`). Bare-name tokens are included, so the 187 figure is approximate.

## 9. Limitations

- I did not open PROTOCOL.md's appendix ("Multi-claim rounds", "Sources & frontier") in full. Statements about it are limited to the lines cited.
- Authorship of the 15 lane lessons is inferred from titles and headers, not from commit history.
- The inbound-citation count is a text regex, not a parser. Bare `name.md:N` tokens may include a few non-knowledge references.
- The counts above are base-commit measurements. Live counts were in flux (17/21 observed mid-wave) and must be re-measured at integration.
- Not run: build, lint, tests, the freshness sweep, or any network read. Per the directive, verification is the main agent's job.

## 10. Changes and tooling

- Files changed: this report only, `.ufo/waves/round-21/w1/CausalSeparation.md`. No commits, no other files, no SCORECARD/LOG/QUALITY/SOURCES/README/SKILL edits.
- Credential or auth files: not read. `~/.omp/agent/agent.db*`: not read.
- Tool installs or upgrades: none. The read-only git and Python used are existing host tools.
