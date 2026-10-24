# Round 31 attempt 2, wave 2 — ReviewC2StrictChecker (C2 strict supplement, freshness)

Seat: KakeR31a2.ReviewC2StrictChecker. Attacked `.ufo/waves/round-31/c2_strict_checks.py`
(committed sha256 `5111264f14ad74cdecf9568a7c41942fb009024210a6eb0ac82d533ec11846ad`,
identical at fde133a and tip 92235a0). All writes in
/fast/scratch/hyaku/kake-r31/a2-w2/ReviewC2StrictChecker/ except this report. No network, no installs.

## Controls (exit codes)

- `--root /fast/scratch/hyaku/kake-r31/w1/CriticC2Sizing/clone --revision b6580c79` → exit 1, 1/5.
- Same clone `--revision 5eabd69c` → exit 1, 2/5. The supplement does reject both wave-1 hollow commits.
- Own clone at fde133a → exit 0, 5/5; at 92235a0 → exit 0, 5/5.

## Falsification: three sandbox commits each pass S1-S5 while teaching nothing or lying

Builder `build_hollow.py`, clone `attack/` (base a16602a; sources/receipts kept verbatim):

- **H1 acbd76cfd86611d0bfe97339cd09dc2a8d95c0ce** "hollow": entry lines are "note one / note two"
  per id carrying one identical quote each; render.yaml section is a bare key list, every key line
  carrying the same unrelated quote. Exit 0, 5/5. Output `strict-acbd76c.json` (sha256 3b32fac0…).
- **H2 60aa2b5e4af26815389a8c5b6b44bde8a7e60f7c** "false": every claim asserts the opposite of the
  quoted source ("Render never builds a service from a Dockerfile", "must never bind to 0.0.0.0",
  "never uses HTTP health checks", "Blueprint never configures a web service"). Exit 0, 5/5.
  Output `strict-60aa2b5.json` (sha256 b8ed6d5f…).
- **H3 419b70c402640a8bdc3a386754434f9ced65f046** "nonsense": per-id S3 satisfied by one line pasted
  twice; the render.yaml section is headed `## This section is not about render.yaml`, contains the
  sentence "No blob d17ab7e5 here.", and satisfies all seven keys with ONE line of fake names
  ("`typedef `runtimex `dockerfilePathology `dockerContextual `healthCheckPathogen `envVarsity
  `syncopation"). Exit 0, 5/5. Output `strict-419b70c.json` (sha256 4272f426…).

## Gaps (c2_strict_checks.py, all at fde133a/92235a0)

- **G1 (S3, line ~121):** `uses` counts any line containing `\b{sid}\b` and a curly quote that is a
  6+ word substring of that id's body. The quote is never bound to the claim, the same quote fills
  both required lines, and two byte-identical lines count as two. H3 exploited all three.
- **G2 (S3):** no truth test. H2's claims negate the very sources they quote and pass.
- **G3 (S4, lines ~124-127):** `f"`{key}" in l` is a substring match — "`typedef" satisfies `type`,
  "`syncopation" satisfies `sync`; one line can satisfy all seven keys. The section predicate
  `"render.yaml" in l` is also a substring match — a heading saying "not about render.yaml" qualifies.
  `d17ab7e5` need only appear; "No blob d17ab7e5 here." passed. The quote per key may come from any
  of S057-S060 and need not relate to the key.
- **G4 (S1, `body_of`):** the body window starts AT the first "Copy page" marker, so marker/chrome
  text is in-body. Gate quotes like "Copy page Every Render Blueprint is backed by" (8 words, 5
  letter-words, unique to S057) pass S1 without being a statement the page makes. S1 also tests
  location and uniqueness only, never topicality.
- **G5 (S2, line ~117):** `url in cells[1]` is a substring test; hollow rows used cell 2
  "sandbox hollow row <url>" and passed. Other cells unvalidated (all "x" in H1-H3).

## Verdict (advisory)

The supplement is strictly better than the base counter (it kills both wave-1 hollows, and S5 binds
retained bytes), but a 5/5 still does not establish learning: an entry that is hollow, false, or
nonsense reaches 5/5. What S1-S5 certify is quote provenance and file plumbing only. The critic's R3
(person reads entry body) remains necessary; mechanical closure would need claim-quote binding — e.g.
each entry line's claim text outside the quote must itself occur near/around the quoted span in the
page body — a key-name boundary (\b after backtick), an affirmative d17ab7e5 line, and distinctness
of the two S3 lines.

## Commands and evidence

- `python3 -B build_hollow.py` (exit 0) → commits H1-H3 above, diffstat a16602a..HEAD: 3 files, +28.
- Checker runs: `python3 -B <lane>/.ufo/waves/round-31/c2_strict_checks.py --root <repo> --revision <rev>`;
  outputs in `/fast/scratch/hyaku/kake-r31/a2-w2/ReviewC2StrictChecker/strict-{acbd76c,60aa2b5,419b70c}.{json,err}`.
- `git show fde133a:…c2_strict_checks.py | sha256sum` = `git show 92235a0:…` = 5111264f… = checkerSha256
  field (executed file equals committed blob).
- Not verified: nothing was fetched (no network); the lane checkout and CriticC2Sizing clone were used
  read-only; lane files unmodified except this report.
