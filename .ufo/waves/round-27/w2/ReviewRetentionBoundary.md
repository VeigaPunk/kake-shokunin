# ReviewRetentionBoundary — r27 fresh falsification (privacy retention boundary)

Seat: `KakeR27.ReviewRetentionBoundary` · lane: leaf (no dispatch) · axis judged: **operability**
Candidate under attack: `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (read via explicit hash, never bare HEAD)

## 0. Artifact identity (verified, not assumed)
- `git rev-parse ac46a747:.ufo/waves/round-27/fetch_group.py` = `1c4b8672790072999fa934b19d854a392f8769ba`
- `git hash-object .ufo/waves/round-27/fetch_group.py` = `1c4b8672790072999fa934b19d854a392f8769ba` (worktree == candidate blob)
- `git rev-parse ac46a747:.ufo/waves/round-27/privacy_selftest.py` = `19e87daccf45d6a6506bbb43a89e76537781b62d` == `git hash-object` (same)
- Worktree clean of tracked modifications after all probes (`git status --porcelain | grep -v '^??'` → empty). No source edit, no repo write outside this report.
- Scratch only: `/fast/scratch/hyaku/kake-r27/ReviewRetentionBoundary/` (`TMPDIR` set there; no `/tmp`, no `/dev/shm`). No network call, no credential/token value, no raw public HTML copied to scratch.

## 1. Delivered retention selftest — REPRODUCED GREEN (author-side claim confirmed)
Declared expectation: `fetch_group.py --selftest` exits 0 with `failed:0` and 9/9 cases passing.
Command (cwd = repo root): `KAKE_R27_SCRATCH=…/delivered-selftest TMPDIR=…/tmp python3 -B .ufo/waves/round-27/fetch_group.py --selftest` → **EXIT=0**, `failed:0`, all 9 cases `passed:true` (html_retained_as_visible_text, html_without_content_type_is_filtered, code_bytes_retained_unchanged, sanitize_filters_html_and_replaces_own_file, sanitize_keeps_received_digest_and_observations, sanitize_never_logs_sentinel_values, sanitize_touches_no_other_path, sanitize_is_idempotent, + fixture-meaningfulness case). Re-run from a foreign cwd (seat dir): **EXIT=0**, `failed:0` → the selftest is cwd-independent (operable).
Matches the delivered receipt `verification/privacy-selftest.json` (exit 0, 9/9, sourceCandidate ac46a747…, cwd `/fast/scratch/hyaku/kake-r27/author-candidate`).

## 2. My own independent case (declared before running; `probe.py`, non-secret fixtures, no network)
Declared expectations (echoed by the script before any assertion): E2 text/html filtered (prose kept, 3 sentinels gone, no `<script`, no `authenticity_token`); E3 same body with content-type absent → filtered; E4 `.yml` code body → `received_code_bytes`, bytes identical; E5 sanitize run 1 (old `.raw.gz` removed, retained+sidecar present, sentinels absent from both, `receivedSha256`==sha256(raw html), `receivedBytes`==len(html), `sha256`/`bytes`==retained, url/status/fetchedAt unchanged, no network helper imported, sibling path untouched); E6 second sanitize (manifest bytes byte-identical, retained bytes byte-identical, receivedSha256/receivedBytes/status/fetchedAt/url identical); E7/E8 falsifiable hypotheses (fragment body must be filtered).
Actual: **E2 pass, E3 pass, E4 pass, E5 pass, E6 pass; E7 FAIL, E8 FAIL** (`EXIT=1`, `failed:2`).
So the mandated case (hidden input / attribute / script sentinel gone; prose kept; code bytes verbatim; second sanitize preserves receivedSha256/receivedBytes/status/fetchedAt/URLs and stable retained bytes) **holds**. The failure is a boundary-adjacent leak (F1).

## 3. Removal scope / preflight atomicity (`probe2.py`, declared before running)
E9 stray own `.raw.gz` not in the manifest survives migration → **confirmed** (file still on disk, unfiltered body still inside it).
E10 digest mismatch → `SystemExit: manifest digest mismatch for S004 1`, manifest byte-identical, no retained file, no sidecar, sibling raw untouched → **zero-mutation preflight confirmed**.
E11 manifest `file` is a symlink → refused (`manifest file is not a regular file: S003-1.raw.gz`), outside file intact → **confirmed**.
E12 manifest `file` escapes the directory → refused (`unsafe manifest file name for S003 1`) → **confirmed**.
E13 (added, declared in-file) migration of a markup-fragment capture → **leak confirmed end-to-end** (see F1).

## 4. Findings by severity

**F1 — HIGH (latent retention-boundary defect + false manifest claim).** `fetch_group.py` `classify()` decides HTML-ness by content-type or a byte sniff (`<!doctype`/`<html` prefix, else one of `<html <body <form <input <script <!doctype` inside the first 4096 bytes) and otherwise falls through to `source_text.text_of(body, content_type)`, whose own `looks_html` test is the same narrow one; with a non-HTML/absent content type that returns the **received body verbatim** (whitespace-normalized). Yet `_representation()` unconditionally asserts `kind:'public_visible_text'`, `htmlAttributesRetained:false`, `scriptBodiesRetained:false`, `formFieldValuesRetained:false`.
Evidence (own fixture, non-secret): E7 — body `<div data-session-id="PROBE-ATTRIBUTE-VALUE">…` with content-type `None` → kind `public_visible_text`, **attribute sentinel retained verbatim** (`retainedEqualsRawMarkup:true`, 123 bytes); E8 — same body with `application/octet-stream` → sentinel retained; E13 — the same leak through the migration path: `sanitize_existing` wrote `S003-1.public.txt.gz` whose retained bytes still contain `PROBE-STRAY-SENTINEL-VALUE`, while the emitted manifest says `kind=public_visible_text`, `htmlAttributesRetained=false`. The claim is therefore not true in general, and a non-secret-to-secret escalation is one sniffed-prefix change away.
Impact on the delivered corpus: **none observed** — all 6 HTML rows start with `<!DOCTYPE html>` → strict path; verified retained text of all 8 rows contains no markup except benign prose placeholders (`<user>`, `<organization>`), and 0 matches for `authenticity_token|csrf|ghp_|github_pat_|session_id|Authorization:|Bearer`. F1 is a latent defect + an over-broad metadata claim, not an observed leak in the frozen corpus.

**F2 — MEDIUM (received-vs-retained metadata is incomplete / classification not auditable).** The delivered `fetched/manifest.json` carries **no `contentType` and no `headers` for any of the 8 rows** (verified per record). The r26 helper does capture `content-type` (`fetch_sources.fetch` → `{k: response.headers.get(k) for k in HEADERS}`), but the delivered manifest was produced by `sanitize_existing` over a base manifest that lacked it, and `sanitize_existing` only forwards `entry.get('contentType')`. Consequences: (a) the HTML-vs-plaintext decision for the migration is not recorded and is not re-derivable after the raw bodies were dropped; (b) a consumer cannot distinguish "HTML filtered" from "plaintext retained verbatim" for a `public_visible_text` row except by comparing `receivedSha256` vs `sha256`; (c) a re-run of `--sanitize-existing` has no content type to fall back on and would re-decide by sniffing — exactly the F1 path. Honest parts confirmed: for all 6 HTML rows `receivedSha256 != sha256` and `receivedBytes` (138 096–240 439) ≠ retained `bytes` (3 492–14 700); for the 2 code rows `receivedSha256 == sha256` and `rawHttpBodyRetained:true` — i.e. received-vs-retained naming is truthful; the original received HTML digest is **not** reconstructable from the filtered bytes (by design; I did not attempt byte-identity inference).

**F3 — LOW/MEDIUM (removal scope is manifest-driven; stray own raw captures survive).** `sanitize_existing` removes only the own filenames it replaced (manifest-listed); E9: an own `S009-9.raw.gz` **not** listed in the manifest survives the migration with its unfiltered body still on disk. `fetch_all._drop_superseded_raw` likewise removes only `{row}-{index}.raw.gz` for manifest rows with `status==200`, so a raw capture of a non-200 row or of a row absent from the current manifest survives. The scope is stated in the docstring ("removes only the own filenames it replaced"), so this is a limitation, not concealed behaviour — but the wave's "privacy-filtered" property holds only for manifest-listed captures.
History check: `git rev-list --objects --all | grep round-27/fetched` lists **only** the 8 filtered files + manifest + 8 sidecars — **no `.raw.gz` was ever committed** in any ref, so no raw body entered git history. Good.

**F4 — INFO (properties confirmed, worth recording).** Preflight atomicity is real (E10: abort ⇒ manifest unchanged, zero files written, sibling untouched). Symlink and path-escape refusals hold (E11/E12). No network in the migration path: after `sanitize_existing`, `r26_fetch_sources` was **not** in `sys.modules` (fetch helper never loaded). Sentinels never reach stdout (E5: `stdoutMentionsSentinel:false`). Idempotence is byte-exact on my own fixture (E6). Corpus integrity read-only check: every record's `sha256`/`bytes` equals its decompressed `.gz`, and every `text/<row>-<idx>.txt` sidecar equals the retained bytes (8/8). `fetch_group.py`/`privacy_selftest.py` are exactly the candidate blobs (§0).

## 5. Residual risk / verification gaps
- The **default fetch path (`fetch_all`) was not executed** (network forbidden by scope). Its manifest writing, content-type capture and `_drop_superseded_raw` were read, not run → F3's fetch-side half and F2's "content-type is recorded on a fresh fetch" claim are **unverified by execution** (source-level only).
- `--sanitize-existing` was **not** run against the real `fetched/` directory (it would mutate the repo); the delivered corpus was verified read-only instead.
- `receivedSha256` for the 6 HTML rows cannot be verified against any received body (bodies not retained, not reconstructable) — treated as unverified-by-construction, not as verified.
- F1's severity for *future* captures depends on the content type the server sends; the frozen 8 rows are unaffected.
- No tool installs were required for this seat (no package/channel action taken, nothing to record).

## 6. Recommendation (advisory only — no edit made)
Make the boundary claim true rather than blanket-asserted: in `classify()`, force the HTML text view whenever the body contains markup signals (not only the current six tags / prefix test) and record the received content type in the manifest so the decision is auditable; and make `_representation()` derive `htmlAttributesRetained`/`scriptBodiesRetained`/`formFieldValuesRetained` from what actually happened instead of hardcoding `false`. Consider extending migration removal to own unlisted `*.raw.gz` in the fetched directory (F3).

Nothing in this report is a PASS from intent: every claim above is tied to a command, exit code and observed output recorded in §§1–3.
