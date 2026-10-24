# Pair10A — (S006, corpus/knowledge/static-canonical-preflight.md)

Axis: **freshness**. Seat: reviewer (leaf, no dispatch). Read-only: no ledger edit, no source edit, no Git
mutation. Repo `kake-shokunin`, HEAD `be375d90afc6fc7aca369ab3cf5247bf460aeed2` (r26 base
`83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`).

## 1. Exact citing line(s), range expanded

One citing form only: `grep -n "S00[1-6]" corpus/knowledge/static-canonical-preflight.md` → line 54; no other
S006 literal or range exists in the file.

- L54: `an assumed checkout served set (S001–S006, `ghp-served-set.md`). No production` (en dash ⇒ the range
  expands to six pairs for this file: S001, S002, S003, S004, S005, S006).

Surrounding claim (L52–54, verbatim):

```
while a symlink inside the manifest-relative page path is not. Prepare the
manifest over actual built/deployable HTML when that artifact exists, not over
an assumed checkout served set (S001–S006, `ghp-served-set.md`). No production
```

Corroboration: `corpus/lessons/round-26-verifier-spotcheck.md:11` — "The grouped **S001–S006** claim at
`corpus/knowledge/static-canonical-preflight.md:53–54` remains outside the final ledger and has no recorded final
adjudication." The pair is in the frozen r27 missing set (`c1-before.json` → `{"row":"S006","file":"corpus/knowledge/
static-canonical-preflight.md"}`). The parenthetical points to `corpus/knowledge/ghp-served-set.md`, itself citing
S006 at :1 and :30–33 ("S006's Jekyll defaults skip `node_modules`, `vendor`, names starting `_`, `.`, or `#`, and
names ending `~` … not every workflow uses that build path"), with the r26 recheck at :83.

## 2. Source identity and evidence (r27 retained bytes + one independent live GET)

Row S006 (tier A docs); scope cell "Default file exclusions in GitHub Pages Jekyll branch builds"; anchor cell
"Configuring Jekyll in your GitHub Pages site" (`corpus/SOURCES.md:14`).
URL: https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll

- **fetchIndex 1**, status 200.
- Quote (24 words, verbatim from the retained text view): `Jekyll doesn't build files or folders that: Are located
  in a folder called /node_modules or /vendor Start with _,., or # End with ~`. Verified: `len(q.split())==24` (≤25)
  and `' '.join(q.split()) in ' '.join(text.split())` → True for `.ufo/waves/round-27/fetched/text/S006-1.txt`.
- Anchor: H2 "Configuring Jekyll in your GitHub Pages site" (id `configuring-jekyll-in-your-github-pages-site`,
  present in the retained raw bytes) — exclusion list right after the "settings cannot be changed" list, before the
  "Front matter" H2.

| observation | raw sha256 | bytes | when |
|---|---|---|---|
| r27 retained `fetched/S006-1.raw.gz` (manifest value = recomputed, verified True) | `f0318abe7e63ecded4e7294484bd8cb68721e920b46d0b85399acb2a187742b6` | 138096 | 2026-10-21T19:59:56Z |
| r26 retained `round-26/fetched/S006-1.raw.gz` | `71a698604486380c05ca092adbc863dc653fc175eecea5a675891651cd3bdfbd` | 138096 | 2026-10-21T15:09:35Z |
| my independent GET (scratch `/fast/scratch/hyaku/kake-r27/Pair10A/S006-live.raw.gz`) | `b842e44c766f49f136ac991d6cda7844753d2c253ce95172505125035463a586` | 138096 | 2026-10-21T20:04:30Z |

Text views: r26 and r27 text views are **byte-identical** (sha256 `2d953b39b80cab8f7a51496dbbc627882d5b2451faa0567e0a1008e1bb5aa1f8`,
7676 bytes); my live body, re-extracted with the lane's own extractor (`.ufo/waves/round-26/source_text.py: text_of`),
equals that view exactly (7675 chars + the trailing newline the fetcher appends).

## 3. Freshness findings (my axis)

- **F1 — raw digest is not a stable freshness signal here.** Three fetches inside ~5 hours gave three different raw
  sha256 at identical length 138096; diffing r27 raw against my live raw shows 19 differing regions, all short
  hex-like request tokens. Only the text view is stable, so a recheck comparing a stored raw sha256 would report
  false drift and no ledger row may claim raw-digest stability. `count_c1.py` is unaffected (raw sha vs its own
  manifest; quote vs text view) and that check passes for this row.
- **F2 — no premise drift.** The relied-on passage is unchanged r26 → r27 → live.
- **F3 — no retry boilerplate.** The r27 manifest holds exactly one S006 entry (index 1); the r26 retry record
  (`manifest-retry.json`) covered S008 only. One clean public GET, not a retry artifact; no retry wording imported.
- **F4 — stale-premise test.** The cited sentence is a normative publisher directive, not a time-indexed observation,
  and the page carries no publication date (only fetch dates: opened 2026-10-19, re-fetched twice 2026-10-21). No
  dated premise exists that could have gone stale, and the backing text is unchanged ⇒ not a stale premise.
- **F5 — freshness gap (documentation, not falsity).** `static-canonical-preflight.md:2` stamps `verified-at:
  2026-10-20 (S020-S027) and 2026-10-21 (S028-S029)`; the S001–S006 group at :54 carries **no** date or anchor
  record in this file. The S006 recheck record lives only in the pointed-to entry (`ghp-served-set.md:83`, r26
  paragraph, HOLD at the same anchors). Natural append target; it does not make the attribution false ⇒ not STALE.
- **F6 — register under-report (named, not edited).** `corpus/SOURCES.md:14` row S006 `used-by` lists only
  `corpus/knowledge/ghp-served-set.md`, yet S006 is also cited at `sitemap-orphan-audit.md:1, :122, :124, :149` and
  `static-canonical-preflight.md:54`; the same under-report holds for S001/S002/S004 (also cited in
  `publish-channels.md:58–61`). `used-by` cells cannot bound the citing set — the denominator must be enumerated from
  the knowledge files, as `count_c1.py` does. This creates **no** new (row,file) pair: those pairs are inside 57.

## 4. S006's specific contribution, and the inferential step

What S006 says in the retained bytes: "By default, Jekyll doesn't build files or folders that: Are located in a
folder called /node_modules or /vendor Start with _,., or # End with ~ Are excluded by the exclude setting in your
configuration file If you want Jekyll to process any of these files, you can use the include setting in your
configuration file." Publishing-mode scope: "If you are publishing from a branch, changes to your site are published
automatically when the changes are merged into your site's publishing source. If you are publishing from a custom
GitHub Actions workflow, changes are published whenever your workflow is triggered …"; plus "GitHub Actions is now the
recommended approach".

**Contribution.** S006 supplies exactly one leg of the composite: under the legacy **branch (Jekyll) build path** the
built output is a strict subset of the checkout, with four named exclusion classes (plus the `exclude` setting,
`include` as override) — the mechanism that makes "an assumed checkout served set" wrong, the proposition line 54
needs.

**Inferential step (labelled).** [INFERENCE] Line 54's group citation is a **local synthesis**: the other leg
(Actions artifact membership — `.git`/`.github` excluded, v4 dotfile exclusion, artifact ≠ checkout) comes from
S001–S004. S006 alone does not entail the whole sentence, and the pointed-to entry already scopes it ("not every
workflow uses that build path").

**Scope limits (S006 does not support):** Actions artifact membership; the `.nojekyll` bypass (`.nojekyll` occurs
nowhere in the retained S006 text); "served set" as such; any statement about a specific site's files.

**Verdict: HOLD at its stated scope.** The attribution is neither wrong nor unsupported: the source names the
concrete exclusions that make the checkout a superset of the built output in one publishing mode. Not STALE — the
r26 STALE pattern was a *specific* statement attributed to the wrong source (e.g. S003's branch-vs-Actions sentence
pinned to `publish-channels.md:5–14`), which is not what happens here. Not UNVERIFIABLE — bytes retained twice today
plus an independent live fetch, all hash-verified, quote present verbatim at the named anchor.

## 5. Suggested C1 ledger record (contract C1 format)

```json
{
  "row": "S006",
  "file": "corpus/knowledge/static-canonical-preflight.md",
  "kind": "source",
  "verdict": "HOLD",
  "fetchIndex": 1,
  "quote": "Jekyll doesn't build files or folders that: Are located in a folder called /node_modules or /vendor Start with _,., or # End with ~",
  "anchor": "H2 'Configuring Jekyll in your GitHub Pages site' (id configuring-jekyll-in-your-github-pages-site), exclusion list after the 'settings cannot be changed' list and before the 'Front matter' H2",
  "reason": "Line 54 is a local synthesis, not six independent entailments. S006 contributes only the legacy branch-build leg: the page states that by default Jekyll does not build files or folders in /node_modules or /vendor, names starting with _ . or #, names ending ~, or exclude-configured paths, so under branch publishing the built output is a strict subset of the checkout and an assumed checkout served set is wrong. Scoped: the page's publishing-mode sentence covers branch publishing; the Actions-artifact half of the composite comes from S001-S004, and S006 says nothing about .nojekyll or about any site's files. Freshness: re-fetched 2026-10-21T19:59:56Z (raw sha256 f0318abe..., 138096 bytes) and independently 2026-10-21T20:04:30Z (raw sha256 b842e44c..., 138096 bytes); the extracted text view is byte-identical to the r26 fetch (sha256 2d953b39...), so the relied-on passage is unchanged. Raw HTML sha256 differs across the three fetches (dynamic request tokens only); freshness is established by the text view, not by the raw digest. No STALE tag is required for a HOLD row."
}
```

Verdict HOLD ⇒ the C1 rule "[r27-recheck S0NN STALE] in citing file" does not apply; adding such a tag would be
wrong. `fetchIndex` 1, quote and anchor are satisfied by the r27 retained bytes.

## 6. Suggested appended wording (optional precision/freshness note — NOT a STALE tag)

Recommended because of F5; append to `corpus/knowledge/static-canonical-preflight.md`:

```
- [r27-recheck S006 HOLD] Line 54's group citation (S001–S006) is a local synthesis, not six
  independent entailments. S006 contributes only the legacy branch-build mechanism: by default
  Jekyll does not build files or folders in `/node_modules` or `/vendor`, names starting with
  `_`, `.` or `#`, names ending `~`, or paths excluded by the `exclude` setting, so under branch
  publishing the built output is a strict subset of the checkout and an assumed checkout served
  set is wrong. The Actions-artifact half comes from S001–S004; S006 says nothing about
  `.nojekyll` or about any site's files. Re-fetched 2026-10-21 (raw sha256 f0318abe…, 138096
  bytes); the extracted text view is byte-identical to the r26 fetch (sha256 2d953b39…).
  Evidence: w1/Pair10A.md.
```

## 7. Discovery / denominator statements (monotone, nothing shrunk)

- My scan of `corpus/knowledge/**` found **no** S006 citing form outside the enumerated 57 pairs; the six group pairs
  all come from the single L54 range. Denominator stays 57; this seat adds nothing to `discovered-pairs.json`.
- Sibling seats own S001–S005 for the same line 54 (`c1-before.json`); per the contract's grouped-recommendation rule
  each source's contribution must be labelled — mine is the branch/Jekyll subset mechanism only.
- Named for the parent (not edited): the `used-by` under-report of F6 (S001/S002/S004/S006 rows in `corpus/SOURCES.md`)
  — a register-accuracy item, not a C1 obligation.
- Named for the parent (not edited): `(S006, corpus/knowledge/publish-channels.md)` enters the r27 missing set **only**
  through the metadata range "S001-S007" at `publish-channels.md:2` ("round-20 corrections 2026-10-19 (S001-S007
  opened that day)") — a date-stamp range, not a substantive statement citation. The sibling seat should judge it as a
  metadata-range citation (the contract keeps historical metadata in scope), with the reason stating that S006 supports
  no statement in that file.
- Observation, not made by this seat: the working tree carries uncommitted modifications to the frozen measuring
  instruments `.ufo/waves/round-27/count_c1.py` and `c2_count.py` (denominator monotonicity from `c1-before.json`, a
  `--selftest` hook, and a new check that (S001–S006, static-canonical-preflight.md) rows must be `kind:"source"`). The
  frozen-at-`be375d9` copies read corpus blobs by `--revision`, but L1 executes the working-tree script, so the
  instrument producing the C1 number differs from the committed freeze. My record complies with `kind:"source"`.

## 8. Residual risk / verification gaps

- I did not run `count_c1.py`, `c2_count.py` or any gate (no mid-flight tests in this lane). My pair enumeration is
  source-reading + grep; the authoritative denominator is L1's measured count.
- Raw HTML carries per-response tokens (F1): a future recheck comparing raw sha256 to a stored value reports false
  drift; compare text views. My live GET used plain urllib with a User-Agent only — no credentials, cookies, browser or
  publication action; scratch under `/fast/scratch/hyaku/kake-r27/Pair10A/`. The ledger's authority is the r27 retained
  bytes (fetchIndex 1); my live bytes are corroboration only.
- The Actions half of the composite sentence at line 54 is not verified by me (owned by the S001–S004 siblings); my HOLD
  covers S006's own leg at its own scope. The source carries no publication date, so a "stale because the doc is old"
  reading is unavailable from the source itself; only fetch dates exist.

## 9. Tooling

No installs, no upgrades, no pacman transactions (host-wide pacman pause respected). Python 3 stdlib only. No
repository file was modified; this report is the only artifact written.
