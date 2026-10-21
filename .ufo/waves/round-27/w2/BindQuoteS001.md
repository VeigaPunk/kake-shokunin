# BindQuoteS001 — r27 fresh falsification, technical source-binding for row S001

Seat KakeR27.BindQuoteS001 (leaf, no dispatch). Axes: **freshness** (do frozen fetches still bind
to live public bytes?) and **operability** (does the retained representation actually support the
ledger quote at its named anchor?). This is a binding/freshness attack only — no semantic PASS is
claimed from digests or substrings; pair semantics were reviewed separately (w1/Pair01A/B).

Candidate ac46a7472d945a6d7ff135e4d7f07b0b6913d835; declaration be375d90afc6fc7aca369ab3cf5247bf460aeed2.
All source reads used the explicit candidate hash; scratch only under /fast/scratch/hyaku/kake-r27/BindQuoteS001
(TMPDIR set); raw bodies kept in memory, never written; no header/token values recorded; no installs.

## 1. Every r27 manifest slot for S001 (fetched/manifest.json, 2 slots — no third URL)

| slot | url (pin) | declared status / fetchedAt | receivedSha256 / receivedBytes | retained file (gz sha256) |
|---|---|---|---|---|
| 1 | raw.githubusercontent.com/actions/upload-pages-artifact/**7b1f4a7**64d45c48632c6b24a0339c27f5614fb0b/action.yml | 200 / 2026-10-21T19:59:53.614354Z | 4524ed61c2fb61b4d7e88de2d779fe937461b6926aeb716b56f047ae3abcd046 / 2529 | S001-1.source.gz (37099a3487949d77103da370e28db9116ee4a59b368b406816a23083c79d687d) |
| 2 | raw.githubusercontent.com/actions/upload-pages-artifact/**5f327015**a708106f6f1b7c9a633901af30fe80cb/action.yml | 200 / 2026-10-21T19:59:53.803523Z | e8ce828a4f2a0e500dc506bc03c706881dab7dc4b7cd527c7ea175c6c0ca6741 / 2895 | S001-2.source.gz (198748c5e942bc90f2539bbc2e5f0134a5d99961d22b1e09e183d29c07d84bec) |

On-disk hashes match frozen-candidate.json sourceFiles exactly: both .gz, both text/ files,
manifest.json 33d650cddc9c65e1201b0ee9a5a93e16b6b3f5d694f8d95d8114037893aeb1d6, pairs.json
f1fa20cab67053fea3945330d14efa59f095ede22b6dacbb058d688d0b376a6a. Citing file
corpus/knowledge/static-canonical-preflight.md: `git cat-file blob ac46a747…:path` sha256
40ebd1dabc122e620d09974ac973b3262649be9520fea2fa42ebe4dce1ca8a12 == working tree == frozen entry.

## 2. Decompress / re-hash of the named retained representation (independent, this seat)

Declared before running: gzip -dc of each frozen .gz must reproduce manifest sha256 and byte count
exactly, and equal the text/ file for code rows.

- slot 1: decompressed sha256 4524ed61…cd046, 2529 B — == manifest sha256, == receivedSha256,
  == text/S001-1.txt byte-for-byte. **Match.**
- slot 2: decompressed sha256 e8ce828a…ca6741, 2895 B — all four identities equal. **Match.**

## 3. receivedSha256 vs retained digest — distinct fields, equal by declared design for S001

- Manifest separates the fields (HTML rows prove it: S002-1 receivedSha256 43d5e22d… / 200835 B vs
  retained sha256 21eb9c92… / 3496 B).
- For S001 both slots declare `retainedRepresentation.kind = received_code_bytes`,
  `derivation: received bytes verbatim (code/config source)`, `rawHttpBodyRetained: true`,
  `replacedFile: S001-N.raw.gz → S001-N.source.gz`. retention-shape-after.json rows 5–10 / 24–29
  confirm receivedSha256 == retainedSha256 for both slots.
- Verified transformation: .gz decompresses to exactly the received body (§2). The stated
  limitation (filtered bytes cannot reproduce original received HTML digest) **does not apply**
  to S001: nothing was filtered. I do not claim HTML-row reconstruction from this.

## 4. Fresh public GETs (one per row URL, in-memory; expectations declared before each probe)

Declared expected: HTTP 200; fresh sha256 == 4524ed61… (2529 B) slot 1; e8ce828a… (2895 B) slot 2.

- slot 1: actual 200, sha256 4524ed61…cd046, 2529 B — **raw drift: none; text drift: none**
  (fresh decoded text == retained text/S001-1.txt byte-equal).
- slot 2: actual 200, sha256 e8ce828a…ca6741, 2895 B — **raw drift: none; text drift: none**.
- Raw digest identity and prose identity are reported separately per contract; both hold here,
  and since pins are commit-addressed a cache cannot serve another revision.

Status/time vs declaration: manifest 200 at 19:59:53Z ≥ declaration be375d90 committed
2026-10-21T16:59:37-03:00 (=19:59:37Z, +16 s); candidate ac46a747 committed 18:51:48-03:00, after
fetches — ordering consistent with declared-before-implementation. No account/browser operations.

## 5. Anchor version label "v4.0.0 action.yml" binding (new probe)

Declared expected: GET of the same document addressed by tag v4.0.0 returns 200 and byte-content
identical to slot 1. Actual: 200, sha256 4524ed61…cd046, 2529 B — **tag v4.0.0 content ==
slot 1 pinned-commit content**. Corroborated (historical observation, w1/SourceOpenS001.md):
GitHub API unauthenticated — v4.0.0→7b1f4a7 (2025-08-14), main→5f327015 (2026-10-15).

## 6. pairs.json quote verification (the actual frozen quote, not the W1 suggestion)

Frozen pair (pairs.json, 1 S001 pair): row S001, file corpus/knowledge/static-canonical-preflight.md,
kind source, verdict HOLD, fetchIndex 1, anchor "v4.0.0 action.yml Archive artifact, Linux tar
command lines29–36", quote:
`tar \ --dereference --hard-dereference \ --directory "$INPUT_PATH" \ -cvf "$RUNNER_TEMP/artifact.tar" \ --exclude=.git \ --exclude=.github \ --exclude=".[^/]*"`

- Shape: 16 whitespace tokens, 10 alphanumeric words → ≥6 tokens ✓, ≤25 words ✓; specific tar
  flags, not boilerplate ✓.
- Exact words at named anchor: whitespace-normalized quote occurs verbatim inside slot-1 raw
  **lines 29–36** (1-based, of 85) and inside retained text/S001-1.txt:
  `29: tar \` / `30: --dereference --hard-dereference \` / `31: --directory "$INPUT_PATH" \`
  / `32: -cvf "$RUNNER_TEMP/artifact.tar" \` / `33: --exclude=.git \` / `34: --exclude=.github \`
  / `35: --exclude=".[^/]*" \` / `36: .` — quote spans 29–35, fully within the named window ✓.
- Raw and retained views agree because retention for S001 is verbatim (§3). count_c1.py's
  quote⊆text-view rule is satisfiable against current retention.
- Slot 2 (main) makes the dot-exclusion conditional (`include-hidden-files` input, upload-artifact
  v7.0.1), confirming the pair correctly binds to slot 1, not main.
- Divergence fact (not an error): w1/SourceOpenS001.md had suggested a different ledger quote
  (`description: "Path of the directory containing the static assets." …`); the frozen ledger
  instead pinned the tar quote — which I verified independently at its stated anchor above.
  Semantic adequacy of either quote is outside this seat.

## 7. New override/strict-status record touching this row (quoted verbatim)

strict-c1-disposition.json `unresolved[0]`:
`{"row":"S001","file":"corpus/knowledge/ghp-served-set.md","units":3,"authority":"r26 statements.json; w1/PairS001GhpServedSet.md rows5,21,23 and EOF adjudication at knowledge lines89–94","meaning":"Pinned-v3.0.1 recheck/count units lack retained version-specific bytes; the fourth old v3 attribution unit was separately corrected in r26, not one of these three."}`
So S001 carries 3 known-unknown strict units (one of the 3 unresolved pairs / 7 units); C1 stays
UNPROVABLE regardless of the 58 review records. discovered-pairs.json contains **no** S001 entry
(monotone discovery added S013, not S001); complete-ledger.json still enumerates six S001 citing
files (ghp-served-set, ghp-subpath-spotcheck, publish-channels, sitemap-orphan-audit,
speedrun-pipeline, static-canonical-preflight) — unchanged obligations.

## 8. Discrepancies and uncertainties

- None binding. Notes: (a) my §4 digests are new independent observations; equality with frozen
  values is the expected result and held. (b) §5 tag probe is one extra benign public GET beyond
  the two row URLs, taken to bind the anchor's version label; no retention beyond identity fields.
  (c) w1/SourceOpenS001.md's text-view hashes (90ef84b8…/ea804af2…, 2000/2350 B) describe the
  pre-migration filtered views; current frozen retention is verbatim source bytes — historical
  report text, not a current-state contradiction. (d) Header/cache state of my GETs was not
  recorded (by rule); commit-addressed pins make cache age immaterial to revision identity.

## 9. Repro (scratch /fast/scratch/hyaku/kake-r27/BindQuoteS001)

bind_s001.py (decompress/re-hash + quote window), fresh_get.py (both row URLs, in-memory),
v40_probe.py (tag binding); outputs bind_result.json, fresh_get.json, v40_probe.json.
No production/source/registry edits; no commits/index/remote changes; no policy-stopped material
touched; no tool installs (none needed).
