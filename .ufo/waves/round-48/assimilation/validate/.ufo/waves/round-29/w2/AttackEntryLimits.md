# W2 attack — entry "What the lane can and cannot check offline" vs landed tool

Seat: KakeR29.AttackEntryLimits (leaf, falsify). Axes: operability, freshness.
Target: the section at `corpus/knowledge/pages-base-path.md:51-56`; byte-identical at
`.ufo/waves/round-29/verification/reject-path/entry.md:51-56` (diff of lines 51-64 differs
only by the corpus-only "Reading a finding" block at 58-60). Item attacked: each
Can/Cannot statement vs docstring + behaviour of `scripts/base_path_audit.py` at
7697990cbca20291f3b0367b8ff4220e93b38b03.
Sandbox: /fast/scratch/hyaku/kake-r29/w2/AttackEntryLimits/clone @ 7697990 (rev-parse
confirmed); TMPDIR inside sandbox. Lane untouched except this report. No installs (none needed).

## Commands (exact, with exit codes)

1. `TMPDIR=<sandbox>/tmp python3 -B clone/scripts/base_path_audit.py --manifest clone/probe/manifest.json`
   → EXIT=1, verdict `failed-policy`, pagesChecked 1, referencesChecked 18, 5 findings
   (all reason `outside_base_path`):
   `page.html#1:link[href]=/style.css`, `#3:a[href]=https://owner.github.io/other-repo/x.png`,
   `#4:area[href]=/map.png`, `#8:script[src]=/app.js`, `#18:form[action]=/submit`.
2. Same tool, probe-b manifest (page url `.../elsewhere/index.html` outside basePath)
   → EXIT=2, verdict `could-not-evaluate`, reason `page_outside_base_path`.
3. Same tool, probe-c manifest (page file `missing.html` absent) → EXIT=2, reason `input_invalid`.
4. `TMPDIR=<sandbox>/tmp python3 -B .ufo/waves/round-29/c2_matrix_count.py --root . --revision 7697990cbca20291f3b0367b8ff4220e93b38b03` (cwd = sandbox clone)
   → EXIT=0, `C2 30/30 at 7697990…`, byKind control 7/7 defect 14/14 input 8/8 usage 1/1,
   constantGatesAllRejected true; matrix sha256 75c08f64… matches the digest pinned in the
   counter source; tool sha256 e3264615… matches counter `toolSha256` and my clone's file.
5. Probe page design: one page with all 15 (element, attribute) pairs, two `<base>` elements
   (first `/repo/deep/`, second `/`), one `<template><img src="/tpl.png">`, plus a
   sibling-project `<a href>` on the same host. Predicted 18 references / 5 findings before
   running; output matched exactly.

## Per-statement verdicts

- Can-1 (`pages-base-path.md:53` — manifest shape, reference set, first-base rule, reason
  list) → **holds**. Every claim verified by run: exact manifest shape `{version, basePath,
  pages:[{file, url}]}` accepted (tool enforces exactly those keys, `scripts/base_path_audit.py`
  `_validate_manifest`); reference set matches `REFERENCE_ATTRIBUTES` (line 76) pair for pair —
  a/area/link href, img/script/iframe/source/audio/video/track/embed src, img/source srcset,
  video poster, form action (all 15 exercised; srcset counted per candidate, 18 refs); first
  base honoured (line 526-527; if the second `<base href="/">` had won, iframe
  `frame.html` would have resolved to `/frame.html` and produced a finding — it did not);
  reasons are exactly `outside_base_path`/`input_invalid`/`page_outside_base_path`
  (lines 65-67), each observed in runs 1-3. `outside_base_path` on the same-host sibling
  link matches the entry's own "Reading a finding" semantics (corpus page lines 58-60).
- Can-2 (`:54` — frozen 30-case matrix + counter) → **holds**. Independent rerun in my
  sandbox at 7697990: 30/30, exit 0, constants rejected, matrix digest matches pin.
- Cannot (`:55` — local files only; cannot show server responses, confirm the deployed base
  path, verify custom-domain mapping, tell missing vs redirected, identify the publishing
  repo; clean means only "matches the declared base path") → **holds**. Docstring line 8
  ("never opens a network connection and never writes to disk") matches behaviour: imports
  (lines 45-51) contain no network module; only urllib.parse string ops; all file opens are
  read-only (O_RDONLY family). basePath and page URLs are taken from the manifest as
  declarations (probe B shows an inconsistent declaration is refused, not reconciled); no
  fetch, DNS, or status anywhere, so missing-vs-redirect and repo identity are structurally
  invisible to the tool. "Clean says only…" is conservative and accurate: clean additionally
  ignores cross-site and non-HTTP(S) references and skips `<template>` content (line 518-523;
  my `/tpl.png` was neither counted nor reported), so it is if anything weaker than the
  entry's phrasing allows.
- Not established here (`:56`) → **not a tool-behaviour claim**; it is a scope admission
  about owned properties and is consistent with the tool's offline contract and lane bounds.
  No behavioural test possible without an authorized live read; nothing observed contradicts it.

## Nuances (not defects)

- Can-1 says the tool "resolves each local page's reference set … against basePath"; in fact
  only same-site HTTP(S) references are policy-checked (`_site_key`, line 345); cross-site and
  non-HTTP(S) references are silently skipped (matrix control K3 pins this). The entry does
  not claim cross-site reporting, so no contradiction — but a reader could over-assume coverage.
- Can-1 omits the tool's input constraints (1 MiB manifest / 2 MiB HTML caps, pages relative
  to the manifest directory, symlink/traversal refusal). Abbreviation, not error; docstring
  carries them.

## Residual risk / not verified

- I directly exercised 3 of the tool's input paths (missing file, page-outside-base, clean
  parse); the other rejection paths (symlink, traversal, oversize, dup keys) were covered only
  via the matrix I-cases passing in my rerun, not hand-run.
- Network absence is established by source reading + offline sandbox run; I did not strace.
- Real-input run numbers (`real-input/out/summary.json`, "4 findings") not reproduced here —
  that is another seat's assignment.
- Freshness of the C1 sources (S040-S043) was not re-fetched; out of scope for this seat.

Verdict for the attacked item: **holds** — all four statements match the landed tool's
docstring and observed behaviour at 7697990; no defect found. Installs: none.
