# SourceOpenS002 — S002 source reopen (r27, freshness axis)

Seat: KakeR27.SourceOpenS002 (leaf, read-only). Scope: SOURCES row S002 only — both
release pages, compared with r27 retained bytes and with r26's earlier fetch. No live
lane edits, no ledger/oracle writes. L1 adjudicates; this is author-side evidence.

Frozen inputs read first: `.ufo/waves/round-27/contract.json`, `count_c1.py`,
`c2-oracle.json` (plus `c2_count.py` interface via contract). `c2-oracle.json`
`expectedPairs` contains exactly one S002 entry:
`{row: S002, file: corpus/knowledge/static-canonical-preflight.md}` — one of the 16
frozen missing pairs. That pair is this seat's primary obligation.

## 1. Live access receipts (two GETs, no cookies/auth, no cache busting)

| # | URL | HTTP | final URL | bytes | sha256 (live bytes) | observed UTC |
|---|-----|------|-----------|-------|---------------------|--------------|
| 1 | https://github.com/actions/upload-pages-artifact/releases/tag/v4.0.0 | 200 | same | 200887 | `3842aa309013a2d08db520848deee03362af919d82317c5374f79da1e9fa0503` | 2026-10-21T20:01:47Z (0.56 s) |
| 2 | https://github.com/actions/upload-pages-artifact/releases/tag/v5.0.0 | 200 | same | 205096 | `ef6eda0535396ed68525027910436e0c14ad8fd42052bcba9f23123b327fd9fe` | 2026-10-21T20:01:48Z (0.54 s) |

Command shape: `curl -sS -L --max-time 60 -o <name>.html -w '%{http_code} %{url_effective} %{size_download} %{time_total}' <url>`.
Scratch: `/fast/scratch/hyaku/kake-r27/SourceOpenS002/`. Page release dates shown live:
v4.0.0 `2025-08-14T19:21:06Z`; v5.0.0 `2026-04-10T18:22:59Z`. No `edited` marker on
either release body (0 matches for a standalone `edited` badge).

## 2. Retained vs live (r27 fetch 2026-10-21T19:59:5xZ; r26 fetch 2026-10-21T15:09Z)

| fetch | bytes | sha256 |
|-------|-------|--------|
| r26 S002-1 | 200830 | `455adcec328f88362641c1d533e1c7a65c46d5120f8ebe2d55b7dc5eaca6334f` |
| r27 S002-1 | 200835 | `43d5e22d3d02d07e4cb8abfb1bd35b01cc29ccba819fa1d9d3883c3f278ef070` |
| live S002-1 | 200887 | `3842aa30…e9fa0503` (above) |
| r26 S002-2 | 205035 | `28d5566afe0653febefea1777c191bd7afb1ecae02e502587c202b74f46fd998` |
| r27 S002-2 | 205035 | `bc5d74856acfadf73123ddc235c84019ed12e43af91b1b6c030b22c3786693a0` |
| live S002-2 | 205096 | `ef6eda05…b327fd9fe` (above) |

Raw bytes differ on every fetch. Token-level diff (difflib, S002-1 r27→live, ratio
0.9967) localises every difference to per-request markup: `data-nonce` v2 UUIDs,
`visitor_id`/`request_id` edge JSON, tooltip/select-panel/reaction element UUIDs, and
two `content=` asset digests. **No release-body token differs.**

Content identity after tag-strip + whitespace normalisation: equal for r27→live and
for r26→live on both pages (normalised lengths 3509 and 3588 chars, identical three
ways). Retained text hashes:
`text/S002-1.txt` = `b87d66d3432e435b40ec35ea84ac7bbea7d3efd6839564493bdeaf58bfd9143b`,
`text/S002-2.txt` = `3eab768ea16b2ee9f36547c256f1913e5ab446b2873c57bb91fba8d01df86230`.

Conclusion: pages are **content-stable over three fetches spanning ~5 h** and today's
reopen; byte hashes are not stable identifiers for these URLs.

## 3. Located support (<=25-word quotes at heading/code anchors)

**Q1 (primary; 14 words), v4.0.0 "What's Changed":**
> "Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact"

Anchor: retained `S002-1.raw.gz` line 699, `<li>` inside
`<div … class="markdown-body …"><h2>What's Changed</h2>` (heading at line 697);
retained `text/S002-1.txt` line 1 at offset 2628. Live page carries the same `<h2>`,
same `<li>`, and the sentence `Full Changelog: v3.0.1...v4.0.0`. Adjacent sentence on
the page points dotfile users to build their own artifact per the README requirements.

**Q2 (corroborating; 4 words), v5.0.0 "Changelog":**
> "feat: add include-hidden-files input"

Anchor: retained `S002-2.raw.gz` line 706,
`<li>feat: add <code>include-hidden-files</code> input … (#137)</li>`, under
`<h1>Changelog</h1>` (line 703); retained `text/S002-2.txt` line 1 offset 2703. The
same changelog lists "Update upload-artifact action to version 7 (#139)".

Tag-to-commit anchors in SOURCES are supported by the pages themselves: v4 page contains
`7b1f4a764d45c48632c6b24a0339c27f5614fb0b` (2 occurrences) and displays `7b1f4a7`;
v5 page contains `fc324d3547104276b827a68afc52ff2a11cc49c9` (2 occurrences) and
displays `fc324d3`. Neither page states the v5 *default* for the new input — that is
S001's `action.yml` claim.

## 4. Classification against the tested inference

Tested sentence, `corpus/knowledge/static-canonical-preflight.md:53–54`:
"Prepare the manifest over actual built/deployable HTML when that artifact exists, not
over an assumed checkout served set (S001–S006, `ghp-served-set.md`)."

- **Direct support: none.** S002 does not mention a manifest, an audit input, built
  HTML, or a preflight. It cannot be read as instructing manifest preparation.
- **Indirect contribution: yes, and it is the load-bearing premise.** Q1 establishes
  that the deployable artifact is a filtered projection of the checkout (dotfiles
  excluded by default in v4.0.0), so a manifest enumerated from the checkout can name
  pages that are not in the deployed artifact. Q2 shows the exclusion is not a fixed
  property but a version/input-dependent choice (v5.0.0 adds the opt-in input), so no
  checkout-derived assumption is safe across action versions. Both statements make
  "actual built/deployable HTML" the correct object of measurement; neither states the
  recommendation. *Inferential step, labelled:* artifact ⊢ filtered checkout set (Q1),
  plus artifact membership varies with pinned action version (Q2) ⇒ a checkout-based
  manifest is not a sound proxy for the deployable set.
- **Irrelevant / contradiction: none.** Nothing in either page contradicts the
  inference or the entry's narrower claim that the archive "does not alone establish a
  live site's membership"; Q1 concerns the artifact, not final Pages serving.

**Teaching still holds:** yes, at its version-pinned scope. The pair's support survives
a fresh open with the anchor text unchanged; the recommendation remains local synthesis
across the grouped sources, not an entailment of S002 alone.

## 5. Adjudication recommendation (L1 decides; not written by this seat)

Primary pair — `row S002`, `file corpus/knowledge/static-canonical-preflight.md`,
`kind source`, `fetchIndex 1`, **recommended HOLD**, quote Q1, anchor "v4.0.0 release
body `<div class=markdown-body>` `<h2>What's Changed</h2>` `<li>`, retained raw line 699",
reason: source supports the artifact-vs-checkout premise; the manifest recommendation is
the citing file's synthesis, explicitly not entailed by this row. Q2 (fetchIndex 2) is
available as corroboration if L1 prefers the version-dependence framing.

Secondary (already decided in r26 statements, recheck only): `row S002`,
`file corpus/knowledge/ghp-served-set.md`, quote Q1, verdict HOLD at its stated scope
("v5.0.0 release notes announce the input" is also present, Q2). Fresh open found no
drift; no STALE correction is warranted.

## 6. Denominator note (monotone)

S002 literal occurrences in `corpus/knowledge/`: `ghp-served-set.md` (lines 1, 25, 83,
93), `publish-channels.md` (1, 58, 60, 84), `sitemap-orphan-audit.md` (1, 122, 124, 149),
`speedrun-pipeline.md` (1, 70, 99), `static-canonical-preflight.md` (54, as
`S001–S006`). r26 `statements.json` already carries four pairs (ghp-served-set,
publish-channels, sitemap-orphan-audit, speedrun-pipeline). The single **new** S002 pair
is the grouped `static-canonical-preflight.md` one — exactly the frozen oracle entry.
No additional S002 citing form was discovered; the denominator is unchanged by this seat.

## 7. Uncertainties / residual gaps

- GitHub release pages are mutable and release bodies editable; this reopen proves
  today's text, not future text. Rechecks should compare the anchor sentences (or
  normalised text), not raw sha256, because of per-request nonces and a dynamic
  "N commits to main since this release" counter.
- S002 speaks only to artifact packaging for the pinned tags. It neither states the v5
  input default nor addresses final live-site serving; those remain S001's and S003/
  S004's scopes respectively. Latest-release status beyond v5.0.0 was not checked —
  outside the row's named URLs and out of scope.
- The Q2 line is a changelog feature entry, not a behavioural guarantee; it is recorded
  as versioned evidence, not as proof of default-on inclusion.

## 8. Hygiene

No tool installs or updates. No pacman usage. No writes outside this report; scratch
confined to `/fast/scratch/hyaku/kake-r27/SourceOpenS002/`. Only the two row URLs were
opened; no broad or package downloads; no credentials/cookies/auth.

Report: .ufo/waves/round-27/w1/SourceOpenS002.md
