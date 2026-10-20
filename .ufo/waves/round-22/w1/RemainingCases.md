# RemainingCases — `comment_decoy`, `script_decoy`, `template_decoy`, `missing_head`, `manifest_traversal`, `symlink_html`

Seat: `KakeR22.RemainingCases` (read-only scout, round 22 W1, axis **operability**,
milestone `offline-canonical-capability`). The only file written is this report. No tests
of the validator or matrix were run; no lane/jj/git writes; no installs; no network
beyond official documentation fetches and read-only inspection of the Matrix seat's
private clone. Target HTML/JSON bytes were treated as data.

Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`, observed `HEAD =
7c61c8cc791bde36dd5e3688bdfea2678d90146c` (matches contract base).
`scripts/canonical_audit.py` is **absent at base** — no implementation evidence is
claimed. There is no LSP server/tool mounted for this subtree and no source file to
resolve, so semantic tracing via `lsp` is not applicable; parser behavior below was
observed by in-process stdlib probes, not by running the lane tool.

## Oracles used

1. **Frozen contract** `.ufo/waves/round-22/contract.json` (required):
   - policy: "Exactly one canonical link in explicit head per page … reject fragments and
     credentials. HTMLParser stdlib limitations must be explicit."
   - `fileResolution`: "HTML paths relative to manifest directory; regular files only,
     reject symlinks and traversal; no network or writes in normal mode".
   - outputs: JSON object with `verdict`, `pagesChecked`, `findings` (each `id` + `page`).
   - exitMap: 0 clean / 1 failed policy / 2 could-not-evaluate input-or-unsupported-shape /
     64 usage. Finding ids include `canonical_missing`, `input_invalid`, `html_unsupported`.
2. **Matrix seat's frozen independent expectations**, observed read-only at
   `/tmp/kake-r22-Matrix/.ufo/waves/round-22/{cases.json,fixtures/,matrix.py}`. The six
   frozen records checked here are:

   | case | fixture manifest | expected exit | expected finding id |
   |---|---|---|---|
   | `comment_decoy` | `fixtures/comment_decoy/manifest.json` | **0** | `clean` |
   | `script_decoy` | `fixtures/script_decoy/manifest.json` | **0** | `clean` |
   | `template_decoy` | `fixtures/template_decoy/manifest.json` | **0** | `clean` |
   | `missing_head` | `fixtures/missing_head/manifest.json` | **2** | `html_unsupported` |
   | `manifest_traversal` | `fixtures/manifest_traversal/manifest.json` | **2** | `input_invalid` |
   | `symlink_html` | `fixtures/symlink_html/manifest.json` | **2** | `input_invalid` |

   The three decoys are therefore **positive controls expected clean**, not
   `canonical_missing` failures. `matrix.py` synthesizes the symlink only at runtime and
   reduces stdout to `"clean"` when `findings` is empty, or the sole finding id otherwise;
   two emitted ids are joined with a comma and fail. Every case below is a one-page
   manifest, so one page-level finding (or none) is the only accepted shape.
3. **Local stdlib probes**, Python `3.14.8` (the lane's `python3`), feeding the exact
   frozen fixture bytes to `html.parser.HTMLParser` with `handle_starttag` /
   `handle_startendtag` / `handle_endtag` / `handle_comment` / `handle_data` recorded.
   These are parser observations, not validator runs.
4. **Official sources** (quotes and URLs at the end).

## Cross-cutting classification model (must be frozen for determinism)

The contract lists `input_invalid`, `html_unsupported`, and policy ids but does not spell
out precedence. The frozen six cases only become deterministic under a gate order. The
order consistent with the contract, `StdoutExit.md`, `SymlinkSafety.md`, and
`FilesystemThreat.md` is:

1. **CLI / manifest envelope** — usage (64); unreadable/invalid JSON, wrong version,
   wrong shape → exit 2 `input_invalid`.
2. **Per-page file resolution** — absolute path, any `..` component, any symlink in the
   path, non-regular file, unreadable file → exit 2 `input_invalid` for that page, before
   touching HTML content.
3. **HTML shape** — explicit `<head>` start tag must exist outside inert constructs;
   otherwise exit 2 `html_unsupported`, before canonical counting.
4. **Canonical policy gates** — outside-head link, missing/multiple canonical, absent/empty
   `href`, invalid/fragment/credential URL, base, then normalized equality → exit 1 with
   the single applicable id.
5. **Clean** — exit 0, `findings: []`.

Consequences exercised below:
- Decoys: shape valid, policy sees exactly one real head canonical → clean.
- `missing_head`: shape gate fires before counting, so the (absent) canonical is not
  reported as `canonical_missing`; frozen id is `html_unsupported`.
- Traversal/symlink: resolution gate fires before parsing, so a matching target must never
  produce clean or a canonical-content finding; frozen id is `input_invalid`.

For these one-page cases: exit 0 → `pagesChecked: 1`, `findings: []`; exit 1 → 
`pagesChecked: 1`, exactly one finding; exit 2 → recommend `pagesChecked: 0` (nothing was
evaluated) and exactly one finding `{id, page}` with `page` = manifest page `url`. The
contract does not freeze the `verdict` token; `"clean"` / `"failed"` /
`"cannot_evaluate"` are the natural choices, but only exit code and `id` are matrix-scored.
Stdout must be one parseable JSON object in normal mode; usage/tracebacks belong on stderr.

---

## 1. `comment_decoy` — frozen expected: exit 0 / `clean`

### Frozen fixture (exact bytes)

`fixtures/comment_decoy/manifest.json`:

```json
{"version":1,"pages":[{"url":"https://example.test/project/a.html","file":"page.html","expectedCanonical":"https://example.test/project/a.html"}]}
```

`fixtures/comment_decoy/page.html`:

```html
<!doctype html><html><head><!-- <link rel="canonical" href="https://wrong.test/"> --><link rel="canonical" href="https://example.test/project/a.html"></head><body></body></html>
```

### Observed token stream (probe of these bytes, 3.14.8)

```
start html; start head;
comment  '<link rel="canonical" href="https://wrong.test/">'
start link [('rel','canonical'),('href','https://example.test/project/a.html')]
end head; start body; end body; end html
```

The comment contributes a comment token only; exactly one `link` element exists in the
explicit head, and its `href` equals `expectedCanonical`.

### Expected observation

- exit **0**, `verdict` clean-ish, `pagesChecked` 1, `findings: []`.
- No `canonical_multiple` for the decoy and no `canonical_mismatch` for `wrong.test`.

### Why

A comment is character data inside a comment token, not markup; the HTML tokenizer has no
element production inside it, and Python's `handle_comment` is the only callback (the docs
explicitly also route IE conditional-comment content there). Counting start tags from the
parser therefore yields one canonical link. The decoy's `wrong.test` href must never be
resolved or compared. If a raw-text/regex scanner sees both `href` values it reports
`canonical_multiple` or `canonical_mismatch` on a page that is actually clean.

### Adjacent false-green attack (distinct from the frozen case)

Frozen fixture = *wrong* decoy + *right* real link (catches false red). Invert the roles so
a comment-blind scanner passes a genuinely wrong page:

```html
<!doctype html><html><head><!-- <link rel="canonical" href="https://example.test/project/a.html"> --><link rel="canonical" href="https://wrong.test/"></head><body></body></html>
```

Same manifest (`expectedCanonical = https://example.test/project/a.html`).

- Correct: one real head canonical `https://wrong.test/` → exit **1**,
  `canonical_mismatch`.
- False green: a scanner that takes the first/any matching `href` from raw text (the
  comment) returns clean.

### Implementation obligations / limitations

- Use `handle_comment` (ignore its data); never scan the source text for `<link`.
- Conditional comments are comments (`handle_comment`), so the same path covers them.
- An unclosed comment (`<!-- …` through EOF) is also fully consumed by `HTMLParser`
  (observed), so no start tag leaks from it; a regex requiring a closing `-->` would leak.

---

## 2. `script_decoy` — frozen expected: exit 0 / `clean`

### Frozen fixture (exact bytes)

`fixtures/script_decoy/manifest.json` is identical in shape to §1 (`page.html`, same URL).

`fixtures/script_decoy/page.html`:

```html
<!doctype html><html><head><script>const markup = '<link rel="canonical" href="https://wrong.test/">';</script><link rel="canonical" href="https://example.test/project/a.html"></head><body></body></html>
```

### Observed token stream (probe of these bytes, 3.14.8)

```
start html; start head;
start script; data 'const markup = \'<link rel="canonical" href="https:';
end script;
start link [('rel','canonical'),('href','https://example.test/project/a.html')]
end head; start body; end body; end html
```

The decoy markup is delivered as `handle_data` inside `script`; exactly one real `link`
element exists in head and matches.

### Expected observation

- exit **0**, `pagesChecked` 1, `findings: []`.

### Why

`script` content is raw text in the HTML tokenizer and in `HTMLParser`: the docs state
"The content of elements like script and style is returned as is, without further
parsing". The decoy text can never produce a start tag, so it cannot count as a second
canonical or supply a mismatching href. CPython 3.13/3.14 source also lists
`CDATA_CONTENT_ELEMENTS = ("script", "style", "xmp", "iframe", "noembed", "noframes")` and
`RCDATA_CONTENT_ELEMENTS = ("textarea", "title")`, so those lookalikes are data too on the
lane interpreter (observed for `title`/`textarea`/`xmp`/`iframe`).

### Adjacent false-green attack (distinct from the frozen case)

Frozen fixture = wrong script decoy + right real link. Invert:

```html
<!doctype html><html><head><script>const markup = '<link rel="canonical" href="https://example.test/project/a.html">';</script><link rel="canonical" href="https://wrong.test/"></head><body></body></html>
```

- Correct: `script` text ignored; the real head canonical is `https://wrong.test/` →
  exit **1**, `canonical_mismatch`.
- False green: a raw-text scanner that finds the matching href inside the script returns
  clean (or `canonical_multiple` if it counts both).

### Implementation obligations / limitations

- Count only `handle_starttag`/`handle_startendtag`; never regex the script body.
- Do not try to model JavaScript strings: a literal `</script>` in a JS string closes the
  script in the HTML tokenizer, and following markup really is markup. The parser's
  tokenization is the contract, not JS semantics.
- Parser version pin: behavior above observed on 3.14.8 and corroborated by the 3.13/3.14
  source constants; record the interpreter in the tool's limitation note.

---

## 3. `template_decoy` — frozen expected: exit 0 / `clean`

### Frozen fixture (exact bytes)

`fixtures/template_decoy/manifest.json` is identical in shape to §1.

`fixtures/template_decoy/page.html`:

```html
<!doctype html><html><head><template><link rel="canonical" href="https://wrong.test/"></template><link rel="canonical" href="https://example.test/project/a.html"></head><body></body></html>
```

### Observed token stream (probe of these bytes, 3.14.8)

```
start html; start head;
start template;
start link [('rel','canonical'),('href','https://wrong.test/')]
end template;
start link [('rel','canonical'),('href','https://example.test/project/a.html')]
end head; start body; end body; end html
```

`HTMLParser` tokenizes the template contents like ordinary markup. A flat start-tag count
sees **two** canonical links and returns `canonical_multiple`; the correct answer counts
only the post-`</template>` link.

### Expected observation

- exit **0**, `pagesChecked` 1, `findings: []`.

### Why

WHATWG HTML §4.12.3: each `template` element has an associated `DocumentFragment` object
that "is its template contents"; "The template contents of a template element are not
children of the element itself." The contents are owned by an inert template document and
enter the document tree only when script clones them. A `<link rel=canonical>` inside
`<template>` is therefore not a document-level link and cannot satisfy, duplicate, or
contradict the head canonical. The parser does not model this (no tree, no template
inertness), so the audit must track template depth itself and ignore `link`/`base` start
tags while that depth is positive.

### Adjacent false-green attack (distinct from the frozen case)

Nested template whose *inner* close must not re-enable document scope:

```html
<!doctype html><html><head><template><template></template><link rel="canonical" href="https://example.test/project/a.html"></template></head><body></body></html>
```

Same manifest. The only canonical sits inside the still-open **outer** template contents.

- Correct: exit **1**, `canonical_missing` (no document-level canonical).
- False green: an `in_template` **boolean** is cleared by the inner `</template>`, so the
  matching link is counted as document-level and the run returns clean. A depth counter is
  required, not a flag.
- Observed token order for this variant: `start template; start template; end template;
  start link(matching); end template; end head` — exactly the trap.

### Implementation obligations / limitations

- Maintain `template_depth`; increment on `template` start, decrement on `template` end,
  and ignore all link/base events while `depth > 0`. Nested templates must be counted.
- `<template/>` is emitted as `handle_startendtag` (observed). In HTML the self-closing
  flag is ignored on non-void HTML elements, so `<template/>` does **not** close a template;
  treating `startend` as start+end (the base-class default) makes a following inert link
  visible. Either special-case `template` `startend` as depth+1 (and document that this
  deliberately differs from `HTMLParser`'s default) or classify the shape unsupported.
  This is not exercised by the frozen matrix; put it in the selftest/hardening set.
- Unclosed `<template>` at EOF: `HTMLParser` still emits the inner link; leaving depth > 0
  to EOF correctly suppresses it.

---

## 4. `missing_head` — frozen expected: exit 2 / `html_unsupported`

### Frozen fixture (exact bytes)

`fixtures/missing_head/manifest.json` is identical in shape to §1.

`fixtures/missing_head/page.html`:

```html
<!doctype html><html><body><p>This document has no explicit head element.</p></body></html>
```

### Observed token stream (probe of these bytes, 3.14.8)

```
start html; start body; start p; data 'This document has no explicit head element.';
end p; end body; end html
```

No `head` event is synthesized; no link is present.

### Expected observation

- exit **2**, `pagesChecked` 0 (recommended), exactly one finding
  `{"id":"html_unsupported","page":"https://example.test/project/a.html"}`.
- Must **not** be reported as `canonical_missing` (exit 1) or clean (exit 0).

### Why

The contract scopes the capability to "Explicit-head serialized static HTML only" and
reserves exit 2 for "could-not-evaluate input/unsupported shape", with a dedicated
`html_unsupported` id. A real HTML5 parser would not fail: the "before head" insertion
mode says "Insert an HTML element for a \"head\" start tag token with no attributes" —
i.e. browsers synthesize a head even when the tag is omitted, and authoring permits the
start tag omission ("A head element's start tag can be omitted if the element is empty…").
`HTMLParser` performs no tree construction and the docs state it "does not check that end
tags match start tags or call the end-tag handler for elements which are closed implicitly
by closing an outer element." The audit therefore cannot decide where an implicit head
would begin; the honest offline classification is `html_unsupported`, not a policy verdict
on a shape it explicitly does not model. Freezing shape-first precedence makes this
deterministic and keeps `canonical_missing` reserved for documents with an explicit head
and zero canonical links (`missing_link` already covers that).

### Adjacent false-green attack (distinct from the frozen case)

No explicit head, but a matching canonical in the would-be implicit head:

```html
<!doctype html><html><link rel="canonical" href="https://example.test/project/a.html"><body><p>x</p></body></html>
```

Same manifest.

- Correct under the frozen scope gate: exit **2**, `html_unsupported` (the page is not an
  explicit-head document; the link's effective head membership is exactly what the audit
  cannot model).
- False green: a validator that treats "no `<head>` seen" as an implicit whole-document
  head, or scans the entire token stream for canonical links, finds the matching href and
  returns clean. `HTMLParser` does emit that `link` start tag (observed without a head
  event), so this attack is live. This is distinct from `body_link`, which has an explicit
  head and yields `canonical_outside_head` exit 1.

### Implementation obligations / limitations

- Require an explicit `<head>` **start tag** outside comment/script/template. If absent
  when parsing completes, emit `html_unsupported` before counting links.
- Define the head region as: `<head>` start → `</head>` end, or `<body>` start, or EOF.
  `HTMLParser` will not synthesize the end tag, so the audit must close the region itself.
- A `<head>` start tag inside template contents must not satisfy the explicit-head gate
  (template contents are a separate fragment).
- `<head/>` arrives as `startend`; treat it as a head start (self-closing is ignored for
  non-void HTML elements) and keep the region open until `</head>`/`<body>`/EOF. Not in
  the frozen matrix; freeze the choice in the selftest.

---

## 5. `manifest_traversal` — frozen expected: exit 2 / `input_invalid`

### Frozen fixture (exact bytes)

`fixtures/manifest_traversal/manifest.json`:

```json
{"version":1,"pages":[{"url":"https://example.test/project/a.html","file":"../escape.html","expectedCanonical":"https://example.test/project/a.html"}]}
```

`fixtures/manifest_traversal/page.html` exists and contains a **matching** head canonical,
but the manifest never references it:

```html
<!doctype html><html><head><link rel="canonical" href="https://example.test/project/a.html"></head><body></body></html>
```

**Observed fixture defect: `fixtures/escape.html` does not exist.** The case directory's
`page.html` is unused, and the traversal target one level up is absent. The validator is
never asked to read a real outside file, so the case as frozen cannot distinguish *explicit
traversal rejection* from *the file happened to be missing* (both can map to
`input_invalid` exit 2). This is a false-confidence gap, not a wrong expected id.

### Expected observation (after making the escape target real)

- exit **2**, `pagesChecked` 0, exactly one finding
  `{"id":"input_invalid","page":"https://example.test/project/a.html"}`.
- No canonical content finding, no clean result, no raw target bytes in stdout/stderr.

### Why

Contract `fileResolution`: page files are "relative to manifest directory … reject
symlinks and traversal". `../escape.html` leaves the manifest directory; it is an input
failure, not a page policy failure. The discriminating property is that the path resolves
to a real, parseable, matching page if a validator naively joins and reads it:
`os.path.join(base, "../escape.html")` + containment-free open → clean exit 0. Explicit
lexical rejection keeps the file unread and yields exit 2.

### Recommended fixture repair (Matrix seat owns the file)

Add `fixtures/escape.html` (one level above `fixtures/manifest_traversal/`) with exactly
the bytes of the unused `fixtures/manifest_traversal/page.html` above. Then:

- correct validator: `..` rejected before open → exit 2 `input_invalid`;
- naive join+read: opens `fixtures/escape.html`, canonical matches → exit 0 / clean, which
  the matrix rejects. The case becomes a true falsifier.
Do not commit symlinks for this; only the symlink case needs a runtime tree.

### Adjacent false-green attack (distinct from the frozen case)

Absolute `file` value pointing at an existing, matching page (runtime temp tree):

```json
{"version":1,"pages":[{"url":"https://example.test/project/a.html","file":"/tmp/<t>/page.html","expectedCanonical":"https://example.test/project/a.html"}]}
```

with `/tmp/<t>/page.html` containing the matching canonical.

- Correct: absolute paths are not "relative to manifest directory" → exit **2**,
  `input_invalid`.
- False green: Python's own join semantics make this tempting — the docs state "If a
  segment is an absolute path … then all previous segments are ignored and joining
  continues from the absolute path segment." A `join(base, file)` + read returns clean.

### Implementation obligations / limitations

- Reject lexically, before any filesystem call: absolute paths, any component equal to
  `..`, empty path, NUL/newline. Do not URL-decode the `file` field (it is a filesystem
  path; `%2e%2e` is a literal name, not traversal). `sub/../page.html` stays inside the
  directory after normalization but still contains a traversal component — recommend
  rejecting any `..` uniformly so normalization cannot become a policy switch.
- Resolve the manifest's *directory* (its parent), not the process CWD and not the file
  path as a base URL; open relative to a held directory descriptor where practical.
- A missing ordinary file is also `input_invalid` exit 2, but that classification must not
  be the only reason this matrix case passes — hence the real target above.

---

## 6. `symlink_html` — frozen expected: exit 2 / `input_invalid`

### Frozen fixture

`fixtures/symlink_html/manifest.json`:

```json
{"version":1,"pages":[{"url":"https://example.test/project/a.html","file":"linked.html","expectedCanonical":"https://example.test/project/a.html"}]}
```

`fixtures/symlink_html/target.html` contains a matching canonical:

```html
<!doctype html><html><head><link rel="canonical" href="https://example.test/project/a.html"></head><body></body></html>
```

`matrix.py` copies `manifest.json` + `target.html` into a fresh temp directory and creates
`linked.html -> target.html` there, so the symlink target exists, is regular, is in-tree,
and matches. (The source fixture directory intentionally has no symlink; the runtime tree
is the right mechanism.)

### Expected observation

- exit **2**, `pagesChecked` 0, exactly one finding
  `{"id":"input_invalid","page":"https://example.test/project/a.html"}`.
- Must not follow the link to a clean result, and must not emit a canonical-content id.

### Why

Contract `fileResolution`: "regular files only, reject symlinks and traversal". The frozen
target being in-tree and matching is deliberate: an implementation that only checks
`realpath(...)` containment, or `Path.is_file()`/`stat()` (both follow the final symlink),
accepts this page and returns clean. The contract does not carve out in-root symlinks, so
the final component being a symlink is itself the input failure. `lstat`/`fstat` on a
no-follow open makes the decision observable before content is parsed.

### Adjacent false-green attack (distinct from the frozen case)

Intermediate directory symlink with a **regular** final component:

```
<t>/manifest.json          file: "linked/page.html"
<t>/linked -> <t>/real     (symlink directory)
<t>/real/page.html         regular file, matching canonical
```

- Correct: a symlink occurs in the path (contract rejects symlinks; the final component
  alone is not enough) → exit **2**, `input_invalid`.
- False green: checking only the final component with `lstat`/`is_symlink()` passes
  (`page.html` is regular); if the resolved directory stays in-tree, a realpath-containment
  check also passes, and the matching page returns clean.
- Variants worth a selftest row: final symlink to an **external** matching file, final
  symlink **dangling**, and `linked` pointing outside the manifest directory. All are
  `input_invalid` exit 2; none may be reported as `canonical_missing` or a read traceback.
- Distinct from the frozen case: the frozen one is a final-component symlink to an in-tree
  target; the attack moves the symlink into an ancestor component.

### Implementation obligations / limitations

- Prefer descriptor-relative walking: open the manifest directory, then each relative
  component with `O_NOFOLLOW` (`O_DIRECTORY` for non-final), final `O_NOFOLLOW|O_RDONLY`,
  and verify `fstat(fd).st_mode` is regular before reading. Any `ELOOP` → `input_invalid`.
- If using `lstat`, check **every** component, not just the last, and still prefer
  `O_NOFOLLOW` to close the check-then-open race in a writable directory.
- A dangling symlink is `input_invalid`, not "file not found" and not an uncaught
  traceback.
- The contract does not define symlink semantics for the `--manifest` path itself or for
  its parent directory (`SymlinkSafety.md` F2). Keep that boundary documented; do not let
  an unstated manifest-path policy change the meaning of relative page paths.
- Direct invocation of the committed fixture without `matrix.py` has no `linked.html`, so
  it degrades to a missing-file `input_invalid` — same exit/id, but non-discriminating.
  The frozen matrix always goes through `matrix.py`; keep it that way.

---

## Findings for L1 / Matrix freeze

1. **Fix `manifest_traversal` before counting it as acceptance.** Add a real
   `fixtures/escape.html` with the matching canonical (bytes above). Without it the case
   can pass because the file is absent, not because traversal was rejected. This is the
   only frozen-fixture defect found among the six.
2. **Freeze the gate order** in §“Cross-cutting classification model”: input/manifest →
   file resolution → explicit-head shape → canonical policy. This makes `missing_head`
   deterministically exit 2 `html_unsupported` (not exit 1 `canonical_missing`) and makes
   traversal/symlink deterministic `input_invalid` even when the target would be clean.
3. **Freeze explicit-head membership**: a `<head>` start tag outside
   comment/script/template opens the head region; it closes at `</head>`, `<body>`, or
   EOF; absence at EOF → `html_unsupported`. `<head>` inside template contents does not
   count.
4. **Freeze template handling as a depth counter**, not a boolean; `<template/>` is a start
   (self-closing ignored) or unsupported, never a no-op close.
5. **Freeze traversal strictness**: reject absolute and any `..` component lexically,
   before opening, uniformly (including in-root normalization such as `sub/../page.html`);
   no URL decoding.
6. **Freeze symlink strictness**: any symlink component, including in-tree and dangling,
   is `input_invalid`; use no-follow descriptor opens and verify regularity by `fstat`.
7. **One finding per page for these cases.** Matrix joins multiple ids and fails; do not
   emit companion findings (e.g. `canonical_mismatch` alongside `canonical_multiple`).
8. **Supplement the decoy cases with inverted-role false-green variants** (the adjacent
   attacks above) in `--selftest` or a supplemental suite. The frozen decoys catch
   over-counting (false red); they do not prove a validator rejects a matching decoy when
   the real canonical is wrong or absent.
9. **Document the interpreter**: raw-text/RCDATA behavior above is from CPython 3.13/3.14
   and observed on 3.14.8; pin or state the minimum.

## Sources (official; accessed 2026-10-20; quotes verified in fetched text)

1. **Frozen contract**, `.ufo/waves/round-22/contract.json`, base
   `7c61c8cc791bde36dd5e3688bdfea2678d90146c` (interface/policy/exitMap/matrixCases).
2. **WHATWG HTML Standard, §4.12.3 "The template element"**,
   https://html.spec.whatwg.org/multipage/scripting.html#the-template-element
   Exact: "The template contents of a template element are not children of the element
   itself." Also: "Each template element has an associated DocumentFragment object that is
   its template contents." (inert template document, null browsing context). Used for §3.
3. **WHATWG HTML Standard, §13.2.6.4.3 "The 'before head' insertion mode"**,
   https://html.spec.whatwg.org/multipage/parsing.html#the-before-head-insertion-mode
   Exact (rather, the "Anything else" branch): `Insert an HTML element for a "head" start
   tag token with no attributes.` — confirms browsers synthesize a head that `HTMLParser`
   does not. Used for §4.
4. **WHATWG HTML Standard, §4.3.1 "The head element"**,
   https://html.spec.whatwg.org/multipage/semantics.html#the-head-element
   Exact: "A head element's start tag can be omitted if the element is empty, or if the
   first thing inside the head element is an element." — the omission is legal authoring,
   but the audit's frozen scope requires the explicit tag. Used for §4.
5. **Python documentation, `html.parser`**, https://docs.python.org/3/library/html.parser.html
   Exact quotes: "This parser does not check that end tags match start tags or call the
   end-tag handler for elements which are closed implicitly by closing an outer element.";
   "The content of elements like script and style is returned as is, without further
   parsing"; "This method is called when a comment is encountered (e.g.
   `<!--comment-->`)."; "The content of Internet Explorer conditional comments (condcoms)
   will also be sent to this method". Used for §§1–4.
6. **CPython source (official), raw-text element sets**:
   https://raw.githubusercontent.com/python/cpython/3.13/Lib/html/parser.py and
   https://raw.githubusercontent.com/python/cpython/3.14/Lib/html/parser.py
   Exact: `CDATA_CONTENT_ELEMENTS = ("script", "style", "xmp", "iframe", "noembed",
   "noframes")`; `RCDATA_CONTENT_ELEMENTS = ("textarea", "title")`. Used for §2 and the
   interpreter-scope note.
7. **Python documentation, `os.path`**, https://docs.python.org/3/library/os.path.html#os.path.join
   Exact: "If a segment is an absolute path … then all previous segments are ignored and
   joining continues from the absolute path segment." Used for §5 adjacent attack.
8. **Python documentation, `os.open` flags**, https://docs.python.org/3/library/os.html#os.open
   Lists `O_NOFOLLOW` as a Unix flag ("consult the open(2) manual page on Unix"). The
   no-follow/`ELOOP` behavior relied on for §6 is standard POSIX `open(2)` semantics,
   marked **[INFERENCE from OS semantics]**, not a Python-doc assertion.
9. **Contract-adjacent sibling reports** (read-only, same wave):
   `PythonParser.md` (tokenizer-only, no tree; script/comment safe),
   `HTMLTemplate.md` (template contents inert; `template_decoy` exit 1 `canonical_missing`
   when no real link), `SymlinkSafety.md` (all symlink components; `input_invalid`),
   `FilesystemThreat.md` (canary/absolute/intermediate-symlink fixture set),
   `StdoutExit.md` (exit-2 precedence and `pagesChecked` honesty), `ManifestSchema.md`.

## Remaining unknowns / non-claims

- No validator exists at base, and none was run: nothing here asserts observed
  implementation behavior or a matrix pass. The only executions were stdlib parser probes
  on fixture bytes.
- `verdict` string values and `pagesChecked` conventions for exit 2 are not frozen by the
  contract; recommendations above are advisory, while exit code + single finding id are
  matrix-scored.
- Multi-page aggregation and mixed exit-1/exit-2 precedence are outside this ticket.
- The traversal fixture repair is a recommendation to the Matrix seat; this seat did not
  edit it (read-only boundary).
- Raw-text behavior for interpreters older than 3.13 and for pathological encodings/NULs
  was not tested; pin the interpreter in the tool's limitation note.

Report: `.ufo/waves/round-22/w1/RemainingCases.md`
