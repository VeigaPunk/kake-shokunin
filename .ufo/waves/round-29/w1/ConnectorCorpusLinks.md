# ConnectorCorpusLinks — round 29 wave 1 (connector, leaf)

Axes: operability, freshness. Lane HEAD read: `e58b66c203bed4e38f89afeaa9573d980344ab64`.
Sandbox: `/fast/scratch/hyaku/kake-r29/w1/ConnectorCorpusLinks/` (clone, probes, `append-notes.md`
with paste-ready note text and a draft Capabilities row). No lane file changed except this report.
No installs.

## Non-obvious move (one proposal)

The entry must cite S024, and the tool must not import `canonical_audit`.
1. The entry draft is scoped to S040–S043 only (`w1-spec.json`, DraftEntryBasePath seat), but it is
   asked to explain the base-element break. None of S040–S043 mentions a base element (search of the
   retained `sources/S04?.txt` for `<base`, `base element` or `base href` found nothing). So the
   base-element claim is unsourced unless the entry body cites S024, using the qualified wording
   "first base element with an href attribute" (round-26 S024 corrections, static-canonical-preflight.md:196-197).
   Citing S024 then requires three things in the same commit: the S024 used-by change below,
   the entry file itself (census error E11 otherwise), and a lesson record of one new citing pair.
2. The C2 counter copies only `scripts/base_path_audit.py` into a temp directory
   (`.ufo/waves/round-29/c2_matrix_count.py:136-141`). A tool that imports `canonical_audit` for
   shared input-safety helpers fails every case there, so mirror the code and do not import it.

## Used-by changes (corpus/SOURCES.md)

| Row | Old used-by | New used-by | Condition |
|---|---|---|---|
| S024 (SOURCES.md:32) | corpus/knowledge/static-canonical-preflight.md, corpus/lessons/round-22.md | corpus/knowledge/pages-base-path.md, corpus/knowledge/static-canonical-preflight.md, corpus/lessons/round-22.md | The entry body cites S024. Add `corpus/lessons/round-29.md` if the lesson cites it too. Order follows the round-27 used-by convention: knowledge files alphabetically, then lessons. |
| S029 (SOURCES.md:37) | corpus/knowledge/static-canonical-preflight.md, corpus/lessons/round-22.md | unchanged | The entry needs no RFC 3986 claim. The same-host protocol-relative defect case (D5) depends on scheme inheritance from the base, which RFC 3986 section 5.2 covers. S029's anchor is section 3 only, so citing S029 for it would stretch the attribution. |

No used-by cell names a script (no `scripts/*.py` path appears in SOURCES.md), so neither row should
list `scripts/base_path_audit.py`.

## Cross-links (append-only notes; full text in sandbox `append-notes.md`)

| Target | Points to | Why | S-id tokens added |
|---|---|---|---|
| static-canonical-preflight.md (EOF) | pages-base-path.md, scripts/base_path_audit.py | The probe below shows the canonical audit is clean on a page with a `/style.css` link, so its clean result says nothing about containment. Also covers the manifest difference and base-element policy (body `<base>` rejected here as local policy, versus first `base[href]` in the base-path audit) | S024 only, already cited in this file |
| ghp-served-set.md (EOF) | pages-base-path.md | Artifact membership (lines 8-12) and serving location are separate. Build the base-path manifest from the built artifact | none |
| crawl-scope-per-host.md (EOF) | pages-base-path.md, scripts/base_path_audit.py | Lines 8-10 already name `<repo>/` project sites. Outside-base references land in the shared host root that holds the one robots file. Marked [INFERENCE] | none |
| ghp-custom-domain.md (optional) | pages-base-path.md | With a custom domain the base path is `/` | none |
| ghp-subpath-spotcheck.md, kimi-subpath-audit.md | no link | There "subpath" means paths inside a site, not the site's mount point. A link would conflate the two | — |

Keep S040–S043 tokens out of these notes. Otherwise each note adds a new citing file to the
S040–S043 rows, and their declared used-by values (entry plus lesson) become incomplete.

## How base_path_audit relates to canonical_audit

- **Shared:** the same built-page population, chosen from the deployable artifact (static-canonical-preflight.md:52-54), the same `{file, url}` page keys, and the same input-safety habits (no-follow opens under the manifest directory: canonical_audit.py:537-616). The exit-code meanings 0/1/2/64 and the could-not-evaluate verdict also match.
- **Different policy and schema:** canonical_audit accepts exactly `{version, pages}` with page keys `{url, file, expectedCanonical}` (canonical_audit.py:685, 695). The base-path manifest adds `basePath` and drops `expectedCanonical` (c2-matrix.json, interface). Keep two manifests and derive one from the other: drop `expectedCanonical` and add `basePath`. A union schema would change canonical_audit's frozen exact-key contract, which its round-22 32-case matrix covers. That trades operability on one tool for convenience on the other.
- **Capabilities table:** draft row in `append-notes.md`. It enters only after a measured 30/30 with the constant gates rejected and closure admission (SCORECARD.md:202-203).

## Contradiction left open (for the C2 builder and falsifiers)

How should `///style.css` be handled? canonical_audit rejects it as invalid (static-canonical-preflight.md:80-88, S029/S028). Python `urljoin` resolves it to `https://o.github.io/style.css`, which would give an outside_base_path finding. WHATWG reads `style.css` as the host, which makes it another origin and ignored. The matrix has no case for it, and the tool's interface does not say which reading applies. No reading gives a false clean under urljoin, but the reason code differs from canonical policy. Not verified against the tool, which does not exist yet.

## Commands run (sandbox, TMPDIR inside sandbox)

- `git clone -q <lane> .../clone` exit 0, HEAD e58b66c.
- Citing-set gate (round-27 population and ledger): `python3 -B scripts/citing_set.py --root . --population .ufo/waves/round-27/frozen/population.json --ledger .ufo/waves/round-27/complete-ledger.json --json`
  - At HEAD: exit 1 with 1 finding, the existing pair (S018, field-performance-cwv.md).
  - Stub entry citing S040 only: exit 1, same single finding.
  - Stub entry also citing S024: exit 1, adds (S024, pages-base-path.md).
  - Stub entry also citing S029: exit 1, adds (S029, pages-base-path.md). The stub was removed afterwards.
- Census: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root <sandbox>/fleet <sandbox>/clone`
  - Base: exit 0, only the existing W04.
  - S024 used-by changed but entry missing: exit 1, `E11 S024 missing used-by corpus/knowledge/pages-base-path.md`.
  - With the entry file present: exit 0. Both files were restored afterwards.
- `canonical_audit.py --manifest <base-path manifest> --json`: exit 2, `input_invalid`. With a canonical manifest over a page linking `/style.css`: exit 0, `clean`.
- Import probe: a sandbox commit `176af1a` adds a stub tool that imports canonical_audit and prints the constant-clean JSON. `c2_matrix_count.py --revision 176af1a`: exit 1, 0/30. The same run's constant-clean gate scores 7/30, so the import alone costs 7 cases. Output sha256 `161b8940…3800a` at `<sandbox>/c2-importprobe.json`.

## Not verified

- I did not run any base_path_audit behaviour, because the tool is absent at HEAD.
- I did not run C1's `c1_quote_truth.py`; the S024 citation does not enter its checks (b_entry_body_cites covers only S040–S043).
- I did not draft or quote-check any S024 wording against retained bytes this round.
- No live probes or network access.
