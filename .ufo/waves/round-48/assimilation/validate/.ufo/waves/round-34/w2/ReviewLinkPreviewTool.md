# ReviewLinkPreviewTool — code review of `scripts/link_preview_audit.py` (Kake R34, wave 2)

Tool sha256 `8dd0018248e04d4e7dd7d901acd846b687a420b559125695b7f2cf5a3c91d875`, byte-identical at
5613071 and 24a1647 (empty `git diff --stat` between the two). All runs in sandbox
`/fast/scratch/hyaku/kake-r34/w2/ReviewLinkPreviewTool/` (clone checked out 24a1647, TMPDIR under it).
No lane files touched besides this report; no tools installed (tooling directive: none needed).
Repro battery: `/fast/scratch/hyaku/kake-r34/w2/ReviewLinkPreviewTool/repro_battery.py`.

## Interface check — `c1-matrix.json` "interface" vs code: CONFORMANT
Each sentence exercised against the tool:
1. One JSON object on stdout for exits 0/1/2 (observed in every run); exit 64 stderr-only, no JSON
   (`no-args` → 64, stderr "the following arguments are required: --manifest", stdout empty).
2. 0 clean / 1 failed-policy / 2 could-not-evaluate all observed and mutually exclusive; input
   findings carry only `input_invalid` / `page_unreadable`.
3. Manifest v1 shape: `version: true` → 2 input_invalid; `1.0` → 2; empty `pages` → 2;
   page `url: "/only/path"` → 2; `file: "/etc/hostname"` → 2; `file: "../x.html"` → 2 (resolves
   outside); symlink escaping the dir → 2 input_invalid; symlink inside dir → 0 clean; page file is
   a directory → 2 page_unreadable; non-UTF-8 page (0xFF) → 2 page_unreadable.
4. `property=` exact match: `property="OG:TITLE"` not counted; `name=` only → 1
   og_required_missing; whitespace-only content not counted (og:type `"  "` + real og:type → 0 clean).
5. All four policy findings triggered; exact-string canonical comparison confirmed
   (og:url `HTTPS://E.com/p` vs canonical `https://e.com/p` → 1); `<base>` ignored, relative
   canonical resolved against page URL — docstring claim true; cross-ref accurate
   (canonical_audit.py:648-655 honours base).
6. Sentence 6 governs the counter, not the tool — nothing to check in the tool.

## Docstring claims verified
- "never opens a network connection": imports are parse-only (argparse/json/sys/html.parser/
  pathlib/urllib.parse) and empirical: run with `socket.socket`/`create_connection`/`getaddrinfo`
  poisoned to raise → exit 0 clean.
- "never writes to disk": code inspection — only `Path.read_text` and stdout print.
- NOT-check list accurate: static parse; no og:image fetch; twitter:card ignored; tag position
  untracked (meta in body counts); name= forms ignored; `<base>` ignored; no serving checks.

## Findings (severity-ranked, each reproduced in sandbox)

### M1 — duplicate HTML attributes: last wins, flips verdicts (Medium)
`link_preview_audit.py:78` `attributes = dict(attrs)` keeps the LAST duplicate attribute; WHATWG
parsers keep the first, and sibling `scripts/base_path_audit.py:193-196` implements
`attrs_first_wins` for exactly this reason. Repro A: only og:title candidate is
`<meta property="og:title" property="og:description" content="T">` → exit 1
og_required_missing:og:title (first-wins reading → clean). Repro B cross-check: reversed order
(`og:description` then `og:title`) → counted as og:title → exit 0. Same last-wins applies to
rel/content dupes on `<link>`. html.parser passes duplicates through; only the dict fold is wrong.

### M2 — unbounded reads: 300 MB page → 616 MB child RSS; contract can break on MemoryError (Medium)
No size cap anywhere (manifest or pages); `Path.read_text` slurps whole files.
`base_path_audit.py:71-72` caps 1 MB manifest / 2 MB HTML (read_bounded_fd :330),
`canonical_audit.py:24-25` likewise. Repro: 300 MB page → rc=0, child max RSS 616 MB (~2x file).
A page beyond RAM raises MemoryError, which is not in `audit_manifest`'s except tuple → traceback,
exit 1, no JSON on stdout — breaking the "one JSON object for exits 0/1/2" sentence. Local-only
inputs lower the stakes, but the lane's own convention caps this.

### L1 — repeated `--manifest` silently keeps the last (Low)
Repro: `--manifest <clean> --manifest <failing>` → exit 1 (last wins). Sibling
`base_path_audit.py:131-182` (SingleManifestAction) → exit 64 "--manifest may be given only once"
(verified run). No interface sentence violated (64 promised only for missing/unknown); convention
divergence from the sibling tool.

### L2 — canonical link picked anywhere in the document, incl. `<template>`/`<svg>` (Low)
`handle_starttag` (:77-90) takes the first `rel~=canonical` link anywhere; html.parser has no tree
model. Repro: `<template><link rel="canonical" href="https://wrong.example/"></template>` before a
matching head canonical → exit 1 og_url_not_canonical (false positive). Same with `<svg>`.
Sibling `canonical_audit.py` refuses the same inputs as unsupported (:207-210, :289-291). The
docstring's tag-position disclosure covers meta only, not canonical pickup. Related ambiguity:
"first canonical link wins" — the tool skips a href-less canonical and uses a later one
(`<link rel=canonical>` then `<link rel=canonical href=other>` → exit 1); defensible
(browser-like), but the interface sentence reads first-canonical-wins.

### L3 — manifest JSON not strict: duplicate keys kept-last (Low)
Plain `json.loads` (:121): `{"version": 2, "version": 1, ...}` → accepted, exit 0. Sibling
`base_path_audit.py:200` strict_json refuses duplicate keys. Manifest read also uncapped (see M2).
Note: BOM manifests are rejected by BOTH this tool and base_path_audit (both exit 2 input_invalid,
verified) — no divergence there.

## Notes (no action required)
- Multiple og:url: only the first is compared; garbage second og:url passes clean. Interface is
  silent; S068 mandates a single og:type only.
- Exit-2 attribution: manifest-stage escapes give `page: null`, read-stage escapes give the page
  URL — harmless under the reason-only input comparison.
- Unknown argument `--manifestx x` reports misleading "arguments are required: --manifest"
  (argparse required-check precedes the unrecognized check); exit 64 is correct.
- `-h` → exit 0, help on stdout, no JSON — consistent with the exit-64-needs-no-JSON sentence.

## Residual risk / not verified
- I verified the interface sentences and docstring claims, not all 28 matrix expectations
  (counter reported 28/28 by L1 receipts; not re-run here).
- The MemoryError contract break (M2 tail) is inferred from code paths, not reproduced at OOM scale.
- No live-network or owned-site requests; holds respected (no counter-trust or sandbox-threat lines).
