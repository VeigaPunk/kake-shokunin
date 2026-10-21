# R27 residual — PrivacyBoundary (KakeR27.PrivacyBoundary)

Seat `KakeR27.PrivacyBoundary` (leaf, writer-privacy): worktree
`/fast/scratch/hyaku/kake-r27/writer-privacy`, branch `kake-r27-privacy`, base
`9ba102d4a0175c927adb54a005464ce2aa722099`. Nothing committed/pushed, no live-lane or
r26 write, no network call, no token value read or printed. Parent `KakeR27` integrates.

## Delivered (3 source paths, exact)

| path | state | sha256 |
|---|---|---|
| `.ufo/waves/round-27/fetch_group.py` | rewritten | `c3b96fa02dc57bf21d72dec253fe5296ebe42d5715289cb559c0ac71cf1442fb` |
| `.ufo/waves/round-27/oracle_selftest.py` | modified (3 lines) | `1bcf4f889d173efc341d126af222f74e11941b705dcdfc661ae70059c72ecb42` |
| `.ufo/waves/round-27/privacy_selftest.py` | new | `faa46832bfd6e49705f033e55734622db4b21300bed1d6dfda4aaf7cf62abe12` |

## Behaviour

1. Fresh-open mode (default, `--root`) keeps one public GET per recorded URL and never
   writes the received HTML. Retention = `source_text.text_of(body, content_type)
   .encode()` (public visible text) gzipped as `<row>-<idx>.public.txt.gz`; a code/config
   URL (`action.yml`, `.yml/.yaml/.py/.sh/.js/.ts`) keeps its received bytes as
   `<row>-<idx>.source.gz`. Attributes, script bodies, hidden-input values and form state
   are never persisted; only `content-type` is recorded, no header set, cookie or token is
   stored or logged.
2. Manifest separates the representations: `sha256`/`bytes` name the RETAINED bytes,
   `receivedSha256`/`receivedBytes` keep the observation of the original HTTP body, and
   `retainedRepresentation` states kind, derivation, `rawHttpBodyRetained`,
   `htmlAttributesRetained:false`, `scriptBodiesRetained:false`,
   `formFieldValuesRetained:false` and the note that the received body is not retained and
   not reconstructable. The quote sidecar `text/<row>-<idx>.txt` is byte-identical to the
   retained payload.
3. `--sanitize-existing` is offline (the fetch helper is not even loaded). It reads only
   `<root>/.ufo/waves/round-27/fetched/manifest.json` and that directory's own files, filters
   each record, writes the retained file plus sidecar, rewrites the manifest preserving
   URL/status/fetchedAt/received digest, then unlinks only the own replaced basenames
   (validated: plain basename, regular file, no symlink, inside the fetched directory). r26
   data and every other path are untouched. Idempotent: an already filtered record keeps its
   original `receivedSha256`/`receivedBytes`/`fetchedAt` and is not reclassified as a new GET;
   a second run gives byte-identical manifest and bytes.
4. `oracle_selftest.py`: the hard-coded `S002-1.raw.gz` becomes the file name the manifest
   gives for (S002, index 1); all strict expected outputs/targets are unchanged.
5. `privacy_selftest.py` (new): synthetic non-secret HTML with a sentinel hidden-input value,
   a sentinel attribute value, a sentinel script body and public prose, plus a plaintext code
   file. Cases: HTML retention strips every sentinel and keeps the prose; code/plaintext bytes
   are unchanged; offline migration strips the sentinel, keeps the received digest and
   observations, removes the replaced own file, touches no other path, and a repeated sanitize
   is idempotent. No stub gate, no fake assertion.

## Explicit limitation (agreed with the parent)

Original received hashes stay observable but cannot be recomputed from the filtered bytes.
The retained representation is NOT the original HTTP body and no whole-body byte identity is
claimed; attributes/script bodies/form values that are not retained are unproved and not
reconstructable from the retained artifacts.

## Order of operations for the L1

`count_c1.py` freezes the fetched manifest at its FIRST committed version
(`fetched_manifest_changed` compares the revision blob with the oldest committed one). The r27
capture is uncommitted, so `--sanitize-existing` must run BEFORE the first commit of it.

Suggested (not run by me):
```
python3 .ufo/waves/round-27/fetch_group.py --sanitize-existing --root <repo>
python3 .ufo/waves/round-27/fetch_group.py --selftest
python3 .ufo/waves/round-27/oracle_selftest.py --kind c1 --source-root <repo>
python3 .ufo/waves/round-27/count_c1.py --root <repo> --revision <rev>
```
`--selftest` is exposed on `fetch_group.py`; the same run is directly
`python3 .ufo/waves/round-27/privacy_selftest.py`. The selftest writes only under
`/fast/scratch/hyaku/kake-r27/PrivacyBoundary/` (override with `KAKE_R27_SCRATCH`).

## What I actually ran (evidence)
Only a syntax parse of the three files (`ast.parse`, no bytecode written): 320 / 205 / 66
lines, all parse; plus `git status`, `git diff`, `sha256sum` in the worktree. NO selftest,
oracle, counter, build, lint or formatter was executed — the wave instruction was to skip
all checks in flight and leave the gate to the parent.

## Unrun checks the L1 should execute
1. `fetch_group.py --selftest` (privacy boundary cases, synthetic only).
2. `fetch_group.py --sanitize-existing --root <live repo>` on the real capture, then
   confirm: the own `*.raw.gz` files are gone, no retained file carries an attribute value
   or hidden input, `sha256`/`bytes` match the retained payload, `receivedSha256`/
   `receivedBytes` still match the original observation, `fetchedAt` is unchanged, and a
   second run changes nothing (idempotence).
3. `oracle_selftest.py --kind c1` and `--kind c2`, then `count_c1.py`.
4. C1 strict stays unprovable while the six inherited unknown units remain; do not force
   green. This work does not change that.

## Risks / notes
- The live r27 manifest has no `content-type`, so HTML is sniffed from the received bytes
  as the r26 `source_text.text_of` helper does, plus a wider markup sniff (`<html`,
  `<body`, `<form`, `<input`, `<script`, `<!doctype` in the first 4 KiB).
- A non-HTML, non-code payload is retained as whitespace-normalised visible text, not as
  received bytes; only the recorded `action.yml` rows keep received bytes. Raw retention is
  limited to code/config suffixes, so `.md`/`.txt`/`.json` bodies are reduced to visible
  text and a token inside such a body would not be provably absent.
- No source evidence was frozen or hashed here (the r27 capture is uncommitted, so there
  is no first-version hash to report). No tooling was installed or updated in this seat.

