# SimplifyInterface — round-22 W1 interface/schema simplification

Seat: `KakeR22.SimplifyInterface` (simplifier, leaf). Date 2026-10-20.
Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`, base observed
`7c61c8cc791bde36dd5e3688bdfea2678d90146c` (`git rev-parse HEAD`).
Frozen contract observed: `.ufo/waves/round-22/contract.json`, sha256
`f9a65a8ade6acb77f013104c60dcd2cfc7b63a0f65e855e710036f26ab746fe4`.

Scope: read-only review. The only file this seat wrote is this report. No
lane source, case, fixture, contract, verifier or lesson bytes were edited; no
tool was installed; no package transaction ran; no network was accessed.

Axes named: **operability** (one invocation grammar, one stdout shape, exact
exit choice), **single authority per fact** (matrix ids only in `cases.json`,
not mirrored in the validator), **evidence integrity** (delete mass, never a
fail-closed boundary).

## Bottom line

The frozen interface needs **no new flag, field or exit**. The avoidable
complexity is implementation mass, not schema surface: the observed implement
draft is ~820 lines, and more than 500 of them are not needed to satisfy the 32
frozen cases or any boundary a peer review named.

A scratch reference of the minimal shape — 253 lines **including** its CLI and
an 18-case selftest — reproduced the Matrix seat's 32-case candidate
expectations exactly (`cases.json` is untracked at this base: the contract
fixes the case names, Matrix fixes the ids and exits):

```
32/32 accepted: exit and finding-id list equal to cases.json (12 clean,
17 policy failures, 3 could-not-evaluate)
```

The scratch file is `/tmp/min_probe.py`, sha256
`dad14965f9d848d2fa262f3a6055ea2cc89510efaa9418e7a968fb9d67aea41f`
(observed). It is evidence that the deletions preserve the cases, **not** a
landed artifact, not an implementation pass, and not a substitute for
`measure.py`.

## What must survive (do not delete)

| Frozen surface | Required shape |
|---|---|
| CLI | `python3 scripts/canonical_audit.py --manifest <path> [--json]` or `--selftest`; no other documented mode |
| Exits | `0` clean, `1` failed policy, `2` input/unsupported, `64` usage |
| stdout | one JSON object: `verdict`, `pagesChecked`, `findings[]` each with `id` and `page`; diagnostics only on stderr |
| Manifest | `version: 1`, `pages[]` each with `url`, `file`, `expectedCanonical` |
| File resolution | relative to manifest directory; regular files only; reject symlinks and traversal; no network, no writes |
| Policy | exactly one canonical link in the explicit head; `rel` ASCII case-insensitive token list; first head `base href` or document URL; HTTP(S) normalized absolute comparison; query preserved; fragments and credentials rejected |
| Finding ids | the 10 frozen ids; no new id |
| Matrix | all 32 case names, each one expected exit **and** one expected id |
| Explicit limitations | HTMLParser is not an HTML5 tree builder; no encoding sniffing, JS, headers, redirects or Google selection |

## Observed draft and where the mass sits

Private clone `scripts/canonical_audit.py` is untracked and was mid-edit during
this review. Two snapshots were observed: `4e01aa77…` at 821 lines and
`7a6a631c…` at 818 lines. Spans below come from the 821-line snapshot; symbols
are the stable identifier if the file has moved again.

| Area | Observed lines | Needed for frozen cases |
|---|---:|---|
| imports, exceptions, argparse subclass | ~35 | ~10 |
| `usage()` prose | 25 | ~8 (limits belong in the module docstring) |
| `parse_cli` + argparse help | ~45 | ~20 (manual parser) |
| attr/rel helpers | 18 | ~10 |
| `CanonicalHTMLParser` | 174 | ~43 |
| `_host_and_port` + `_remove_dot_segments` + `normalize_http_url` | 131 | ~33 |
| bounded reads + file walk | 78 | ~27 |
| `evaluate_page` | 45 | ~22 |
| manifest validation + `audit_manifest` + `public_result` | 69 | ~26 |
| selftest (`_selftest_specs`, `_run_selftest_case`, `selftest`) | 155 | ~37 |
| `main` | 12 | ~10 |

## Exact deletions

### D1 — argparse and the help/abbreviation surface

Delete `import argparse`, `CanonicalArgumentParser`, `parse_cli`'s parser
construction, `add_help=True`, and the `--json`-with-`--selftest` special case
branch. Replace with one ~14-line argv loop that accepts exactly:

- `--manifest PATH` (space-separated form only; the contract example form),
- `--selftest`,
- `--json` (accepted no-op; stdout is already one JSON object),

and returns `64` for every other token, missing value, repeated mode, or
`--manifest` + `--selftest` combination.

Evidence (observed on the draft):

- `canonical_audit.py --help` → **exit 0**. `argparse`'s help action calls
  `parser.exit(0)` before the custom `error()` override; the contract exit map
  has no help exit, so a wrapper that checks only status reads a typo as clean.
- `canonical_audit.py --manif <manifest> --json` → **exit 0**: `argparse`
  accepts the abbreviation. `--manifest=<path>` is also accepted. Neither form
  is in the frozen grammar; both are extra surface no case needs.
- `--bogus` and a missing `--manifest` value do return 64 today, so the only
  loss is the accidental statuses above.
- `matrix.py` invokes exactly `--manifest <abs> --json`; `measure.py` and the
  frozen count never use `--help` or abbreviations (observed in both drafts).

Tradeoff: no `-h`. A two-line usage string goes to stderr on every 64, which is
enough operability and keeps stdout JSON-only.

### D2 — `public_result` and the internal `exit_code` key

Delete `public_result()` (6 lines) and the internal `exit_code` key it strips.
Build the final object once (`verdict`, `pagesChecked`, `findings`) and return
`(result, code)` from the audit function. In the observed draft the same
information is constructed, copied and stripped in three places.

### D3 — replace the 131-line URL layer with a tuple canonicalizer

Delete `_host_and_port` (62), `_remove_dot_segments` (22), `quote()` percent
re-encoding, IPv4/IPv6 canonicalization via `ipaddress`, DNS label regex,
URL-string serialization, the `has_query` "?" flag and the `absolute=` flag.
Delete imports `ipaddress`, `ntpath`, `quote`.

Replace with one function (`canon(raw, base=None) -> (scheme, host, port, path,
query)`, 21 lines in the scratch probe) used for the document URL, the first
base, the canonical href and `expectedCanonical`:

- reject empty/non-string, `#`, backslash and C0/control/space bytes;
- resolve with `urljoin` only when the reference has no scheme;
- `urlsplit`; scheme must be `http`/`https`; `.port` exceptions become URL
  errors; empty or non-ASCII host rejected; `username is not None` or
  `password is not None` rejected (this also catches `https://@host/`);
- lowercase the host, drop the scheme's default port;
- dot segments removed by a 10-line stack algorithm that preserves `//`,
  empty path becomes `/`, query kept verbatim;
- compare tuples. No serialization, no percent rewriting, no empty-query
  distinction.

Grounded behavior (python3 3.14.8, observed):

```
canon('HTTPS://EXAMPLE.TEST:443/project/a/../a.html') ==
canon('https://example.test/project/a.html')            -> True
canon('https://example.test/project/%2e%2e/a.html')     -> path kept literal
canon('https://user@example.test/…') / 'https://@host/' -> URL error
```

The 32-case probe passes with this normalizer, including
`scheme_relative`, `query_preserved`, `invalid_url`, `javascript_url`,
`data_url`, `fragment_url`, `wrong_host/path/query`, `base_invalid`.

Limits that must be written down in the docstring (contract requires explicit
HTMLParser limits; the URL subset needs the same treatment): no IDNA/punycode,
no percent-encoding normalization (raw bytes compared; `%7e` ≠ `~`), no IPv6
text canonicalization, no trailing-dot host normalization, empty query `?`
indistinguishable from no query, non-ASCII host rejected. None of these is a
frozen case; each removes code rather than adding it.

### D4 — collapse the 174-line parser state machine to ~43 lines

Delete `HEAD_VOID_ELEMENTS`, `HEAD_TEXT_ELEMENTS`, `head_open`,
`head_closed`, `body_seen→error` paths, the `unsupported` flag's shape
diagnostics, `raw_head_element`, `noscript_depth`, `handle_data`,
`finish_supported`, and the elaborate `handle_endtag` error rules.

Keep one small state:

- `head_seen`, `in_head`, `body_started`;
- one suppression counter map for `template`, `svg`, `math`, `noscript`
  (nested start increments; matching end decrements; everything else in a
  suppressed subtree ignored);
- one `HEAD_ALLOWED` set; a non-head element while `in_head` closes head scope
  (literal, browser-like), and later links count as outside;
- first `base href` only; canonical `link` collection in and out of head;
- `handle_startendtag`: for suppressed elements treat as start (HTML self-close
  flag is ignored on non-void elements), otherwise start+end;
- `missing head` at EOF → `html_unsupported`; body start closes and blocks
  head re-open; repeated `<head>` before body is a no-op; stray `</head>` is a
  no-op.

This still satisfies the head-boundary asks in `HeadBoundary.md` (HB-01..HB-04,
HB-06) and `ParserScope.md` P2, with far less state. The scratch probe verifies:

```
<head/> + link                  -> canonical_outside_head
head reopened after body        -> canonical_outside_head
repeated <head> … </head>       -> clean
<template/> decoy then real     -> clean
unclosed <template>             -> canonical_missing (non-clean)
body <svg><link bad></svg>      -> clean (decoy ignored)
```

The last line is an operational deletion worth stating explicitly: the draft
sets `unsupported = True` on any `svg`/`math` start tag anywhere, so a normal
static page with one inline SVG icon is reported `html_unsupported` exit 2.
Observed on the draft:

```
<body><svg width="1" height="1"></svg></body>  -> exit 2
```

That is a false “cannot evaluate” on common real pages. Suppressing the subtree
and continuing keeps the fail-closed property for signals (a canonical inside
SVG is not counted) without rejecting the document.

Also keep raw-text handling version-independent: set
`CDATA_CONTENT_ELEMENTS = HTMLParser.CDATA_CONTENT_ELEMENTS +
HTMLParser.RCDATA_CONTENT_ELEMENTS + ("plaintext",)`. Do **not** replace the
tuple with a shorter one; the stdlib class tuple is what enables CDATA mode
(verified in the 3.14 source), so a shorter tuple cannot cover
`xmp`/`iframe`/`noembed`/`noframes`.

Tradeoff: malformed head shapes that the draft classified `html_unsupported`
now become policy findings (`canonical_outside_head` / `canonical_missing`) or
clean when the literal structure is unambiguous. Both outcomes are non-clean
for the shapes that matter; no frozen case changes. If L1 prefers the stricter
classification, keep the `HEAD_ALLOWED` scope close and delete only the error
branches around it.

### D5 — selftest must not mirror the matrix

Delete `_selftest_specs` (64 lines, 39 cases) and the per-case temp
directories/manifests for pure cases (34 more lines). The observed selftest
reuses 34 frozen case names with different payloads — for example its
`comment_decoy` is a decoy-only head expecting `canonical_missing`, while the
frozen fixture in `cases.json` is a valid canonical **plus** a decoy expecting
clean. That creates two authorities over the same names.

Replace with ~37 lines:

- ~10 pure rows calling `evaluate_page` directly, one per finding id;
- 5 argv rows proving `64`;
- 3 temp-only I/O rows proving `input_invalid` (traversal, leaf symlink,
  intermediate symlink directory).

Rationale and evidence: `SimplifyProof.md` E4 says explicitly “Drop instead:
duplicating the 32 matrix cases in selftest”; `matrix.py`/`cases.json` already
exercise all 10 ids, so the selftest's job is rule coverage and the CLI map, not
the oracle. The scratch probe's 18-row selftest passes and never touches the
lane tree.

### D6 — one read helper, one walk, keep the safety core

Delete the duplicated open/fstat sequences between `read_manifest_bytes` and
`read_page_bytes`, the chunked `read_bounded_fd` loop, `READ_CHUNK_BYTES`, the
`ntpath` absolute/drive checks and the per-call `hasattr` spread.

Keep, because a peer review and a probe both require it:

- manifest directory opened once as the anchor;
- each directory component opened with `dir_fd=…, O_DIRECTORY|O_NOFOLLOW`;
- leaf opened with `O_NOFOLLOW|O_NONBLOCK`, `fstat` must be `S_ISREG`;
- size caps before reading; strict `utf-8-sig` decode with
  `html_unsupported` on decode failure;
- manifest strictness (`version` exact int 1, exact page keys, non-empty
  `pages`); the draft already rejects `pages: []` with exit 2 (observed).

Evidence for keeping `O_NONBLOCK`: a probe that opened a FIFO with
`O_RDONLY|O_NOFOLLOW` blocked until the 300 s command timeout; adding
`O_NONBLOCK` and the `fstat` regular check rejected the FIFO as
`input_invalid` in 0.019 s. A directory, a leaf symlink, an intermediate
symlink directory and a missing file all return exit 2 the same way.

### D7 — evaluate/audit: one ordered chain, one finding per page

Keep the draft's precedence (base resolution, then multiple, outside, missing,
href missing/empty, fragment, URL invalid, mismatch). Freeze it in the
docstring; matrix cases are single-defect so the order only matters off-matrix.
Delete the `assert href is not None`; keep the value in a local. Keep one
finding per page: `matrix.py` compares the id list exactly, so a page emitting
two ids fails any single-id case. `pagesChecked` should be the number of pages
actually evaluated; manifest-level errors stay `0` with `page: null`.

### D8 — optional prose trim

`usage()` is 25 lines of prose. Eight lines (grammar, one-line policy, exit
map, pointer to the module docstring for limits) are enough; the contract's
“limitations must be explicit” requirement is satisfied by the docstring
sections, not by CLI length. This is the only purely cosmetic deletion.

### D9 — final import set

After D1/D3/D6 the needed imports are `json, os, stat, sys, tempfile`,
`HTMLParser`, `urljoin, urlsplit`. Deleted: `argparse`, `ipaddress`, `ntpath`,
`quote`; `re` is needed only if the ASCII-whitespace splitter keeps its regex
form (a `replace`/`split` helper avoids it).

## Minimal shape and budget

Scratch inventory (253 lines total, observed):

| Part | Lines |
|---|---:|
| docstring, imports, constants | 12 |
| ASCII lower/token/attr/rel helpers | 12 |
| `P` HTMLParser | 43 |
| `dots` (dot segments) | 12 |
| `canon` (tuple) | 21 |
| `read_page` (walk + no-follow + cap) | 27 |
| `evaluate` | 22 |
| `serialize` (base string for `urljoin`) | 3 |
| `audit` (manifest + findings + verdict) | 23 |
| `parse_cli` | 14 |
| `selftest` | 37 |
| `main` | 10 |
| shebang/blank | 17 |

Add a few lines for the manifest read helper and the explicit docstring limit
list; a landed shape around **260–280 lines** is realistic against 818–821
observed. The deletions above are independent: an implementer under time
pressure can take D1, D2, D5 and D6 without touching the parser or URL layer.

## Preservation proof

Scratch command (mirrors `matrix.py`: absolute manifest, `--json`, cwd at the
candidate root):

```
python3 /tmp/run_min_probe.py
# invokes: python3 /tmp/min_probe.py --manifest <abs> --json
# ACCEPTED 32 / 32
```

| Expected class | Cases | Result |
|---|---|---|
| clean, exit 0 | 12 positive controls (`absolute_match` … `query_preserved`) | all clean |
| `canonical_missing`, 1 | `missing_link`, `comment_decoy`, `script_decoy`, `template_decoy` | all |
| `canonical_multiple`, 1 | `duplicate_same`, `duplicate_different` | all |
| `canonical_outside_head`, 1 | `body_link` | yes |
| `canonical_href_missing`, 1 | `href_absent`, `href_empty` | both |
| `canonical_url_invalid`, 1 | `invalid_url`, `javascript_url`, `data_url` | all |
| `canonical_fragment`, 1 | `fragment_url` | yes |
| `canonical_mismatch`, 1 | `wrong_host`, `wrong_path`, `wrong_query` | all |
| `base_url_invalid`, 1 | `base_invalid` | yes |
| `html_unsupported`, 2 | `missing_head` | yes |
| `input_invalid`, 2 | `manifest_traversal`, `symlink_html` | both |

Note this table follows `cases.json` (the frozen oracle), not
`SimplifyProof.md`'s contract-derived table. The two disagree on the decoys and
`href_empty`; that is a decision L1 must arbitrate once (below).

Boundary probes observed on the scratch shape:

| Probe | Result |
|---|---|
| inline `<svg>` in body beside a valid canonical | clean (draft: exit 2) |
| FIFO named as page file | `input_invalid`, 0.019 s, no hang |
| leaf symlink / intermediate symlink dir / directory / missing file | `input_invalid` |
| non-UTF-8 HTML bytes | `html_unsupported` |
| `https://user@…`, `https://@…` | `canonical_url_invalid` |
| `href="…a.html#"` | `canonical_fragment` |
| uppercase scheme/host, `:443`, `a/../a` vs plain URL | tuple equality true |
| `%2e%2e` in path | preserved, not decoded |
| `<head/>` then link; head reopened after body | `canonical_outside_head` |
| template self-close decoy; repeated heads | clean |
| `pages: []`; `version: true` | `input_invalid`, exit 2 |
| `--help`, `--bogus`, missing `--manifest` value, conflicting modes | 64, stderr only |
| clean run stdout | exactly `{"findings":[],"pagesChecked":1,"verdict":"clean"}` |

## Fail-closed boundaries to keep

1. Every argv not in the frozen grammar → 64; no status-0 help path.
2. Manifest unreadable, non-JSON, `version != 1`, empty `pages`, non-string or
   missing page fields, invalid `url`/`expectedCanonical` → 2 `input_invalid`.
3. Page file absolute, backslash, empty/dot/dotdot component, missing,
   non-regular, symlink at any component, oversize, non-UTF-8 → 2.
4. Credentials (including empty userinfo) and literal `#` (including bare `#`)
   rejected before comparison; non-HTTP(S) scheme → 1.
5. Duplicate canonical links fail even when the destinations agree; duplicate
   detection precedes URL comparison.
6. First head base wins; later bases are ignored; an invalid first base is
   never skipped in favor of the second base or the document URL.
7. Explicit head only: no implicit head synthesis; a body-only canonical is
   outside; no head at all is `html_unsupported`.
8. Comments, script/style raw text, template/svg/math subtrees and noscript
   contents never contribute a canonical signal.
9. No network; no writes in manifest mode; selftest writes only a temp tree.
10. One JSON object on stdout; diagnostics on stderr; no timestamp, cwd or
    environment path in the object.

## Single-freeze decisions and cross-seat conflicts

These are interface-level ambiguities where two seats can both be right; each
must be frozen once before the matrix is trusted.

| # | Issue | Positions observed | Recommendation |
|---|---|---|---|
| 1 | `href_empty` id | `cases.json` + current draft: `canonical_href_missing`; `URLNormalization.md`: `canonical_url_invalid` | Keep `cases.json` (frozen oracle) and the draft; if the peer reading is preferred, change `cases.json` first, then rerun Measure — never let the validator disagree with its oracle |
| 2 | Decoy payload semantics | `cases.json` fixtures: valid canonical **plus** decoy → clean; `SimplifyProof.md`: decoy-only → `canonical_missing`; draft's embedded selftest: decoy-only | Follow `cases.json`; delete the mirrored selftest names (D5) so the disagreement cannot resurface |
| 3 | Empty `pages` | draft now rejects with 2 (observed); `ManifestSchema.md` recommends reject; the 821-line snapshot's logic allowed clean (read, not run) | Keep reject; one line, no case conflict |
| 4 | `findings[].page` identity | contract says “page”; draft uses page `url` for policy findings, `null` for manifest-global; `ManifestSchema.md` suggests a fixed sentinel | Freeze exactly that: page URL for page findings, `null` for manifest-global; do not add file/index |
| 5 | `pagesChecked` | draft counts evaluated pages; contract silent | Freeze “pages actually evaluated”; manifest-global errors stay 0 |
| 6 | `verdict` strings | contract gives no enum; draft uses `clean`, `failed-policy`, `could-not-evaluate` | Freeze those three; one renderer |
| 7 | HTML shape strictness | draft marks svg/math/stray-head shapes unsupported; `ParserScope.md`/`HeadBoundary.md` require explicit scope rules, not necessarily exit 2 | Minimal literal scope (D4); document the tradeoff; keep the head guards |
| 8 | `--json` with `--selftest` | draft rejects 64; grammar attaches `[--json]` to manifest; D1 accepts it as a no-op | Accept-and-ignore is the lower-surface choice (D1); one branch either way; never add a second output renderer |
| 9 | CDATA tuple | draft replaces the stdlib tuple; a shorter replacement loses `xmp`/`iframe`/`noembed`/`noframes` | Extend `HTMLParser.CDATA_CONTENT_ELEMENTS + RCDATA_CONTENT_ELEMENTS + ("plaintext",)` |
| 10 | Strict-vs-lenient manifest keys | draft rejects unknown keys; `ManifestSchema.md` agrees | Keep strict; a typo must not become a skipped field |

The draft's behavior was executed on the observed 818-line revision: it
rejects empty `pages`, rejects FIFOs quickly, accepts `--manif` (abbreviation),
accepts `--manifest=…`, and exits 0 on `--help`. The earlier 821-line snapshot
was read at the same symbols (not run; it was mid-edit). The first two listed
behaviors are input handling; the last three are the D1 surface.

## Suggested L1 checks after integration

This seat ran no build, test, lint or formatter against the lane and makes no
claim that the draft passes. The post-integration checks are:

1. `python3 scripts/canonical_audit.py --selftest` → 0.
2. `python3 .ufo/waves/round-22/measure.py --root . --revision <tip>` →
   `accepted == total == 32`, one revision-pinned receipt.
3. Direct CLI: clean manifest → 0; `wrong_query` fixture → 1; traversal and
   symlink fixtures → 2; `--help`, `--bogus`, `--manifest` with no value → 64.
4. `--json` accepted on the manifest form; stdout parses as one object; stderr
   empty for evaluated runs.
5. Tree digest before/after a manifest run, excluding `scripts/` fixtures
   supplied by the harness, to prove no writes.
6. If D1 is applied: no `argparse`, `ipaddress`, `ntpath` or `quote` imports;
   no `--help` success path.

## Evidence and reproducibility

- Contract sha256 and base revision as above; `cases.json` read from the
  Matrix seat's private clone (untracked candidate; the base tree has no
  `cases.json`).
- `python3 --version` on host: `3.14.8` (only python3 on host).
- HTMLParser probes: tag and attribute names are lowercased; `rel` values are
  not (casefold needed); attributes are entity-decoded (`&amp;` → `&`);
  comments are a separate callback; script/style and, on 3.14, `xmp/iframe/
  noembed/noframes` are raw text (class tuple) and `title/textarea` RCDATA;
  `<template>` contents are ordinary tags (depth counter needed); `<svg>`
  content is emitted (subtree suppression needed).
- urllib probes: `urljoin` resolves the relative/root/scheme-relative cases and
  preserves query; absolute URLs keep dot segments (so `dots()` is required);
  `.hostname` lowercases; `.port` raises for non-numeric/out-of-range; empty
  userinfo yields `username == ""`, not `None`.
- argparse probe: `--help`/`-h` → `SystemExit(0)` even with an `error()`
  override; abbreviation and `=` forms are accepted by default.
- Filesystem probe: `O_NOFOLLOW` blocks leaf symlinks; `O_DIRECTORY|O_NOFOLLOW`
  blocks intermediate symlink directories; a FIFO without `O_NONBLOCK` hung;
  with `O_NONBLOCK` it is rejected by `fstat` in 0.019 s.
- Scratch artifact: `/tmp/min_probe.py` (253 lines, sha above) and
  `/tmp/run_min_probe.py` (32-case runner). Both are scratch only; the lane
  tree is unchanged by this seat.

No tool installs or updates were made; all pacman transactions remain paused;
no host service, credential, package or network operation is part of this
report.
