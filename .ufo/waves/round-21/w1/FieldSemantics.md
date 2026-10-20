# FieldSemantics — critic report (kake round 21, wave 1)

Seat: `KakeR21.FieldSemantics` (critic, leaf, read-only). Axes: **freshness**, **operability**.
Snapshot: working tree 2026-10-20T08:57Z–09:00Z (tree was changing under scribes during the read); base `5009ecaa1cce10b895617a585ddd3f7c7c923a84`.
Files changed by this seat: **this report only**. No repo scripts executed; every check below is an in-memory replica (Bun eval) of the cited regex. No tools installed or updated.

## Target located

| checker | state at 08:59:56Z | field rule |
|---|---|---|
| `scripts/corpus-contract.mjs` (MetadataCheck) | **absent**, so it could not be audited. The findings below apply to its spec: "trio nonempty in first8". | — |
| `.ufo/waves/round-21/measure.mjs` (FrozenMeasurement) | present, read lines 1–324 | `FIELDS` lines 88–92: `/^source\s*:\s*\S/i`, `/^verified-at\s*:\s*\S/i`, `/^recheck\s*:\s*\S/i`, tested per line over `text.split(/\r?\n/, 8)` (line 199); any line, any order, duplicates allowed |

## Counterexample (strongest)

**The C1 score of 21/21 means only that the three keys are present. It does not show that a value is real or honest.** The `measure.mjs` rule returns `111` (complete) for every one of these first-8 headers:

| id | first-8 content (abridged) | measure.mjs | defect it admits |
|---|---|---|---|
| M04 | `source: \u200B` (zero-width space) | 111 | invisible value counts as non-empty (`\u200B` is not `\s`) |
| M06 | `source: TODO` | 111 | placeholder source |
| M07 | `verified-at: unknown` | 111 | **unknown verification** counts as verified |
| M11 | `verified-at: historical-not-live-reverified` (no date/revision) | 111 | no date or revision, though CORPUS says `verified-at:` is a "commit or date" |
| M08 | `verified-at: 2026-10-20 live re-verified` | 111 | claims live verification today, which the planned C1 rules out |
| M09 / M10 | `verified-at: 2026-13-45` / `2099-01-01` | 111 | invalid calendar date / future date |
| M12 / M13 / M14 | `source: S999` / `S017` (rejected row) / `S015` (queued row) | 111 | dangling or non-mined registry id |
| M15 | `source: S019 metadata contract` alone | 111 | the metadata authority stands in for entry evidence (S019's own scope says "not verification of historical platform claims") |
| M16 / M17 | `recheck: cat ~/.config/gh/hosts.yml` / `recheck: git push origin main` | 111 | credential read / mutating recheck |
| M18 | heading + 3 prose lines, trio on lines 6–8 | 111 | trio is not first, though CORPUS says the fields "come first" |
| M19 | trio inside a ```` ``` ```` fence on lines 2–4 | 111 | trio is example code, not metadata |
| M21 / X02 | `Source:` / `Verified-At:` / `RECHECK: whenever` as legacy prose | 111 | regex is case-insensitive (`/i`) |
| M22 | `source: S011` then `source: S999` | 111 | duplicate keys with conflicting values |
| M23 | recheck / verified-at / source in reverse order | 111 | order not enforced |
| M27 | YAML `---` frontmatter around the trio | 111 | a different metadata convention passes silently |
| X01 | `source : S011`, `verified-at\t: …` | 111 | `\s*` before the colon accepts key variants |

These cases are rejected correctly: M01/M02/M26 (empty value, or spaces only, including CRLF), M05 (NBSP only), M20 (HTML comment), M29 (`verified_at`).

**False negatives** (a valid header that fails): M24, a UTF-8 BOM before `source:`, gives `011`; X03, lone-CR line endings, gives `100`. Neither appears in the current corpus; the risk is low.

## Evidence from the real corpus

1. **Base per-field count disagrees with `initial.json`.** At base, the `measure.mjs` rule counts `source` in **9** files. `initial.json` `metadata.source` says **4**. The 5 extra files are drift-detection, fire-journal-codes, fleet-registry, origin-repos and speedrun-pipeline. They match through legacy prose `Source:` lines under the `/i` flag. The trio total stays at 4/21 only because these files lack `verified-at`. Any per-field before/after delta built from `rows[].fields` therefore under-reports the source gain by 5.
2. **Current snapshot:** the `measure.mjs` rule gives 21/21 `111`, all line 4 blank, and all three fields on lines 1–3 in order. A strict lines-1-3 rule (below) also passes 21/21 on structure.
3. **`verified-at` meaning varies between entries (freshness axis):**
   - *Which date leads is inconsistent.* drift-detection, ops-automation and publish-queue lead with the r16 re-read date **2026-09-29**. free-read-verbs and sitemap-orphan-audit record the same r16 2026-09-29 re-read but lead with **2026-09-28**. publish-channels leads with the earliest date (**2026-09-26**). freshness-sweep leads with **2026-10-19**. QUALITY.md lines 46–47 say "records the original evidence date/revision", but no shared rule decides whether a later re-read counts as the original date.
   - *A naive "latest date" parser reads false freshness.* ops-automation and vault-properties contain the string `2026-10-20` inside "not a 2026-10-20 domain recheck". A max-date parser would mark both as verified today. free-read-verbs, probe-delta-alerting and publish-channels would read 2026-10-19 from absence notes and corrections.
   - *Mixed formats.* Values take several shapes: date first; datetime `2026-09-28T22:18Z` (keeper-timer-inert, where a `\b\d{4}-\d{2}-\d{2}\b` parser finds **no date**, as observed); prose first, `original evidence 2026-09-28` (probe-delta-alerting); several dates (publish-channels); and date plus commit `dd4eabf` (vault-properties).
4. **S019 citation.** 16/21 entries cite S019; the other 5 are crawl-scope, ghp-custom-domain, ghp-etag, ghp-served-set and sitemap-orphan-audit. The S019 row (SOURCES.md line 27) has `used-by` = `corpus/lessons/round-21.md` only. Earlier in this snapshot, several headers carried transient locators `S019 (corpus/CORPUS.md)` and "registration pending". `corpus/CORPUS.md` does not exist in kake. By 08:59Z, every header said `S019 in corpus/SOURCES.md` and no "pending" text remained. Nothing gates against those transient forms coming back.
5. **Recheck safety cannot be decided by regex.** A deny-list prototype gave **4/4 false positives** on real rechecks, and all of them are actually safe:
   - `fire` inside a grep pattern (fire-journal-codes)
   - `.env` in `process.env.HOME` (fleet-registry)
   - `>h` in `'<loc>https'` (kimi-subpath-audit)
   - `publish` in `r9-publish-queue.md` (publish-queue)

   Whether a recheck is safe needs a sentinel or human review. A pattern match is not enough.
6. **Adjacent finding (C2, same script).** `GATE_RE = /^##\s+Gate\b/m` matches `"##\nGate"`, because `\s+` crosses the newline. It also matches `## Gate-keeping notes` and a `## Gate` inside a code fence.
7. **The script's self-description is inaccurate.** `measure.mjs` emits `criteria.knowledge.fieldRegex: 'field name at column 0, non-empty value'`. The actual regex is case-insensitive, allows whitespace before the colon, and accepts any of the first 8 lines. The source comment on lines 86–87 does say case-insensitive; the JSON output does not.

## Impacted axes

- **Operability:** a green census can admit placeholder, unknown, duplicate or misplaced metadata, so the gate reports success when it should fail. Per-field counts are inflated at base, which undermines the before/after evidence.
- **Freshness:** `verified-at` has no machine-readable meaning. A freshness sweep reading these fields (CORPUS line 164) cannot rank entries without per-entry interpretation, and a naive parser reads false 2026-10-20 freshness from negated text.

## Defect vs tradeoff

- **Fixable defects:** case-insensitivity, the whitespace-before-colon and any-line window, duplicates, placeholders and invisible values, missing or invalid dates, dangling or rejected S-ids, the newline-crossing Gate regex, and the inaccurate `criteria` string.
- **Tradeoffs the canonical judge must not credit as proof:** whether a date is *true*, whether a recheck is *safe*, and whether a source *supports* the claim. No syntax gate can establish these. QUALITY.md lines 55–57 already says to "Reject a green structural census as proof…". The score claim should read "trio present and well-formed", never "verified".

## Smallest safe correction

Apply this to `measure.mjs` and to the pending `corpus-contract.mjs` spec. It is not a new authority; it is the same gate made tighter.

1. Strip a leading `\uFEFF`, split on `/\r\n|\r|\n/`, and require `^source:`, `^verified-at:`, `^recheck:` **case-sensitive on lines 1, 2, 3, in that order**, with line 4 blank. This is exactly what all 21 entries now do and what the scribe recipe prescribes.
2. Value test: remove `[\p{White_Space}\p{Cf}]`, then require a non-empty value that does not match `^(todo|tbd|unknown|n/?a|none|pending|-+|\?+)\b` (case-insensitive).
3. A key must not appear twice within the first 8 lines.
4. `verified-at` must **start with** a valid calendar `YYYY-MM-DD`, using a parser that does not require `\b` before `T`, and that date must not be after the run date. Otherwise it must start with a 7–40 hex revision that `git cat-file -e` resolves. When every S-id is S019 or none is present, require the token `historical` (all 16 local-evidence entries already carry it). The CORPUS/QUALITY ruling must say which date leads: *the latest date the claim was observed against its source*, or *the original baseline*. The choice determines which round-21 header lines move:
   - If "latest observed": free-read-verbs and sitemap-orphan-audit move to 2026-09-29 (r16), and publish-channels' 2026-09-26 lead is reviewed.
   - If "original baseline": drift-detection, ops-automation and publish-queue move to their 2026-09-28 baselines.

   These lines were added this round, so editing them changes no preexisting byte.
5. Every `S\d{3}` in `source:` must resolve to a SOURCES.md row with status `mined`. S019 must not be the only evidence token.
6. Leave recheck safety out of the regex gate. Record it as a sentinel review item.
7. Change `GATE_RE` to `/^## Gate[ \t]*$/m` (or `^##[ \t]+Gate[ \t]*$`), and skip fenced blocks.

I ran an in-memory prototype of items 1–5 plus the recheck deny-list. It rejected all 28 malformed fixtures (M01–M23 and M26–M30) and accepted the valid control plus the BOM (M24) and CRLF (M25) variants. On the real snapshot, 15/21 passed every rule. Of the 6 flags:

- 4 were deny-list false positives (evidence item 5). They are why item 6 keeps recheck safety out of the gate.
- keeper-timer-inert was a prototype bug: `\b` before `T` failed to parse a datetime. Item 4's parser requirement fixes it.
- probe-delta-alerting is a **real nonconformance** with item 4. Its `verified-at:` begins `original evidence 2026-09-28` instead of starting with the date. The fix is a reorder of that one round-21 prefix line (owner seat Knowledge16); no preexisting byte is affected.

With items 1–5 alone, 19/21 pass.

## Limits

- `corpus-contract.mjs` was not on disk at 08:59:56Z, so its actual regex is unaudited; these fixtures are what its `--selftest` should include.
- No `verified-at` date was checked against git history or LOG.md. HistoricalDate owns that.
- The knowledge files changed while I was reading them. The real-corpus counts reflect 08:57–09:00Z only, and L1 should re-measure once integration is final.
- The fixtures ran against a regex replica, not `node measure.mjs`. The replica copies lines 88–92 and 199 verbatim.
