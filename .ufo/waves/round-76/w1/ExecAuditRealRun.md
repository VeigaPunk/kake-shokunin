# ExecAuditRealRun — C2 real-input receipt (kake r76, w1)

Seat: one executor leaf. Inputs read before any after-state: `.ufo/waves/round-76/contract.md`,
`amendment-1.md`, `amendment-2.md`. Base revision `a0491fcd041cbc3fff2c964ecf6268557e45a5c1`.
Everything below is a run I made in this session; every number names the receipt file that carries it.
No network call was made (no fetch tool was invoked; the only process invocations are local `python3`).

## 1. Population — 12 directories, 8 with retained bytes

`receipts/census.txt:39` — `directories=12 with_retained_page_html=8 not_served=4`.

The four directories without bytes (`charter-kimi`, `lucario-kimi`, `plazir15-kimi`, `plazir27-kimi`)
hold only `audit.json` + `fetch.json`; all four carry the same 404 body sha256
(`93ddca9a021664d562e698eb99d52b84d696f81485847dcfeaf6f4a5c8fca966`, 13409 bytes) and no `page.html` or
`manifest.json`. `receipts/sha256-check.txt:11-14` records each as `page_html_present=false`.
This matches Amendment 1 §A1 exactly, so the audit population is the 8 served pages, and the four
not-served surfaces are reported as not-served — never counted clean and never counted as an error.

**Premise correction (against the unamended §C2 sentence).** §C2 says the run is "end-to-end on the 12
retained real surfaces". Twelve directories exist; eight retain bytes. Amendment 1 already corrected this,
and my census independently reproduces the correction from the tree, not from the amendment text.

## 2. Manifest and byte verification

`w1/ExecAuditRealRun/real-manifest.json` — version 1, 8 pages, one per retained directory:
`file` is relative to `--root` (the lane root), `url` is `pages[0].url` from that directory's retained
`manifest.json`. sha256 `448ebd9c73c2f563e88a43cc784734447ebe46fc6a077f59e7d2c406a366bc47`.

Before any page was used, each `page.html` sha256 was compared with the sha256 in its own retained
`fetch.json`. `receipts/sha256-check.txt:3-10` — all eight rows read `true`, with status 200:
burnerchrome-kimi 11976 B, charter-ghp 53660 B, ds4cc-kimi 74641 B, ds4cc-primary 76159 B,
lucario-ghp 3435 B, plazir15-ghp 38337 B, ufo-fsd-kimi-pro 612 B, vault-index-kimi 10059 B.
No mismatch occurred, so no page was excluded on byte grounds.

## 3. Declaration census (the §C2 item-2 census)

`receipts/declarations.txt:17` — `TOTAL alternate_declarations=2 canonical_declarations=3`.

| Surface | `<link rel=alternate>` (tag → href) | `rel=canonical` |
|---|---|---|
| burnerchrome-kimi | none | none |
| charter-ghp | `x-default` → `https://veigapunk.github.io/charter-ufo-fsd/`; `en` → same url | `https://veigapunk.github.io/charter-ufo-fsd/` |
| ds4cc-kimi | none | none |
| ds4cc-primary | none | `https://ds4cc.com/` |
| lucario-ghp | none | none |
| plazir15-ghp | none | `https://veigapunk.github.io/plazir-15-site/` |
| ufo-fsd-kimi-pro | none | none |
| vault-index-kimi | none | none |

(`receipts/declarations.txt:4-16` per page.) An independent raw-regex count over the same bytes agrees
page by page — `receipts/raw-scan.txt`, columns `hreflang` / `canonical`.

Two facts that bound what this receipt can claim:

- Only **one** of the eight pages declares any `hreflang` at all, and both of its declarations point at
  its own url (`x-default`, `en`). There is no cross-surface alternation anywhere in the retained corpus.
- Therefore the real-input run exercises the parser and the self/duplicate/canonical conditions on real
  bytes, but it cannot discriminate most of the finding set: `hreflang_nonreciprocal` and
  `hreflang_external_target` have no real candidate, and the seven pages with no alternates cannot produce
  any `hreflang_*` finding by construction.

## 4. The audit run

The ExecAuditTool file was rewritten by its own seat while I worked — five distinct sha256 values were
observed in this session between 21:59 and 22:04, of which only the two I pinned are citable. Every
receipt here is therefore produced against **pinned copies** under
`w1/ExecAuditRealRun/pinned/`, so the receipt is immutable and re-runnable:

| Pinned copy | sha256 | Bytes | Its own selftest | Real-input run |
|---|---|---|---|---|
| `hreflang_audit_asrun_58a2cdcece48.py` (primary) | `58a2cdcece489b3c407c818b77398d428a3e38b3c0f6812db2e4bf7ace67955a` | 56827 | `selftest 55/55 passed` (exit 0) | exit 0 |
| `hreflang_audit_asrun_0a2454c6dfd6.py` (earlier) | `0a2454c6dfd6abadaf433bcdd29f5dddd44677ce8b20daa11eadb8774610bc05` | 50408 | `selftest 33/38 passed` (exit 1) | exit 0 |

`receipts/tool-versions.txt` carries both rows; the live file's sha256 at receipt time equalled the primary
pinned copy. The identical real-input outcome on a red build and a green build is the version-stability
evidence: the eight-page verdict does not depend on which of the two builds read it.

**Command (wrapped for width; the exact absolute command line is `receipts/real-input-run.txt:1`):**

```sh
python3 -B pinned/hreflang_audit_asrun_58a2cdcece48.py \
  --manifest .ufo/waves/round-76/w1/ExecAuditRealRun/real-manifest.json \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin --json --work <scratch>
```

**Observed (`receipts/real-input-run.txt:2-4`; the exit code is also in `receipts/real-input-run.exit:1`).**
The line below is the file's line 4, quoted up to `by_id` and elided there with `...`:

```
exit=0
{"version": 1, "pages": 8, "findings": [], "counts": {"policy": 0, "info": 0, "input": 0, "by_id": {...
```

`findings` is the empty list, `counts.policy` `counts.info` and `counts.input` are all 0, and every
`by_id` counter is 0. **There is no finding to attribute to a page id — the set is empty.** Verdict
`exit 0`, i.e. clean over the 8-page manifest.

Per-surface isolation (`receipts/per-page.txt:4-11`): each of the eight pages was also audited alone in its
own one-page manifest; all eight read `exit=0` with an empty `findings` list. No page-level verdict depends
on cross-page state.

Root invariance (`receipts/root-invariance.txt`): the same eight pages were copied byte-for-byte into a
scratch mirror (each copy sha256-checked equal to its original by the driver) and audited through a
different `--root` and manifest; the output is the same document — `exit=0`, 8 pages, empty findings.

Supplementary fault-path run (`receipts/absent-surfaces-run.txt`): a 12-page manifest that also names the
four not-served directories exits `exit=2` with four `input_unreadable` findings, one per missing
`page.html` (`charter-kimi`, `lucario-kimi`, `plazir15-kimi`, `plazir27-kimi`). Nothing was silently
skipped; the four are reported, not scored as clean.

## 5. Cross-check against the lane's canonical audit

`scripts/canonical_audit.py` resolves page files strictly relative to its own manifest directory (no
absolute paths, no traversal, no symlinks), so the retained pages were mirrored byte-for-byte and audited
through a v1 manifest in that mirror (`receipts/canonical-audit.txt:1-4`, exit 1,
`canonical_missing` on the five pages that declare no canonical).

Agreement is exact on the question asked — which pages declare a canonical at all:
`receipts/canonical-crosscheck.txt:10` — `AGREEMENT 8/8 pages on whether rel=canonical is declared`,
with declared = `charter-ghp`, `ds4cc-primary`, `plazir15-ghp` and absent on the other five.

The two tools do not agree on a *verdict* — canonical_audit exits 1 because five pages lack a canonical,
while the hreflang audit exits 0 because a missing canonical is out of its scope (Amendment 2 §A5 makes
"no canonical" the page's own url, which is not a `hreflang_canonical_not_self`). That difference is the
intended scope split, not a disagreement about the bytes.

## 6. Advisory differential (not a matrix case, no verdict asserted)

An independent reference build of the contract-as-amended sits at `w1/ExecAuditRealRun/hreflang_audit_ref.py`
(written from the contract + amendment text, not copied from ExecAuditTool; its own selftest is 35 cases,
`receipts/ref-selftest.txt`). On the real manifest it returns the same document
(`receipts/ref-real-input-run.txt`: `exit=0`, `"pages": 8`, empty findings).

Eleven synthetic probes aimed at Amendment 2 decisions were run through both builds
(`receipts/differential-probe.txt`): 9 of 11 agree on exit code and id multiset. The two that differ:

- `p3_two_xdefault_same_href` — two identically-targeted `x-default` links. Both emit
  `hreflang_duplicate_pair`; the tool then emits `hreflang_multiple_xdefault` **twice**, the reference once.
  Amendment 2 §A2 emits a policy finding "once per offending annotation (one per `<link>` element), except
  `hreflang_self_missing` and `hreflang_canonical_not_self`, which are emitted once per page". For a
  page-level condition like multiple x-default the clause supports either count, so this is undecided
  rather than wrong; it needs a matrix case to fix one reading.
- `p11_duplicate_file_two_pages` — two manifest entries naming one file. Both exit 2. The tool emits one
  `input_unreadable` naming the repeating page; the reference emits one per entry. §A2 says input faults
  are "once per manifest entry", which favours two; §A15 only says two pages may not share a file and names
  no id or count.

Fixtures, both command lines and both JSON bodies for `p1` (relative href), `p3`, `p10` (version 2) and `p11`
are in `receipts/divergence.txt` so the matrix or review seat can turn either reading into a case without
re-deriving my fixtures.

## 7. Limits — what this receipt does not measure

- **Retained bytes, not live serving.** The pages are the 2026-10-21 snapshots (`fetchedAt` per surface in
  `receipts/census.txt`). Nothing here says what any of these hosts serves today, or that any page is
  correct for a search engine.
- **Static parse only.** No rendering, no JavaScript, no HTTP headers, no `Vary`, no live fetch — the §C2
  limits, unchanged.
- **No language claim.** `hreflang` syntax validity is not a statement about the language of any page.
- **Weak discrimination on real input.** Two declarations, both self-referential, on one page (§3). A clean
  verdict here is mostly a statement that eight real documents parse without a policy finding, not that
  hreflang policy is healthy across the fleet.
- **Tool authorship is not mine.** The audited tool is another seat's file and moved under me; the numbers
  above belong to the pinned sha256 values in §4. If the tool changes again before landing, the L1 must
  re-run this receipt against the final bytes — `receipts-driver.py` reads `KAKE_TOOL` for exactly that.
- **The tool's own selftest is its claim, not mine.** I ran it and recorded the result verbatim
  (`receipts/tool-selftest.txt`, `receipts/tool-versions.txt`); I make no assertion that 55 cases are the
  right cases.

## 8. Reproduction

Layout used: scratch `S=/fast/scratch/hyaku/kake-r76/ExecAuditRealRun`, the reference build at
`$S/ref/hreflang_audit.py`, the driver at `$S/ref/drive.py` and the raw counters at `$S/ref/scan.py` (shipped as
`w1/ExecAuditRealRun/hreflang_audit_ref.py`, `receipts-driver.py` and `raw-scan.py`; drop them at those
paths, `mkdir -p $S/{tmp,work,work-tool}`),
then:

```sh
KAKE_TOOL=<pinned tool copy> TMPDIR=$S/tmp python3 -B $S/ref/drive.py \
  /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-76/w1/ExecAuditRealRun/receipts
```

The driver rebuilds the scratch mirror, re-verifies every `page.html` sha256 against `fetch.json`, and
rewrites all receipts except `tool-identity.txt` (two `sha256sum` lines; `versions-writer.py` and
`divergence-writer.py` write `tool-versions.txt` and `divergence.txt`).

## 9. Deliverables and status

Written under `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-76/w1/` only:

| Path | What |
|---|---|
| `ExecAuditRealRun.md` | this report |
| `ExecAuditRealRun/real-manifest.json` | v1 manifest over the 8 served surfaces |
| `ExecAuditRealRun/absent-surfaces-manifest.json` | supplementary 12-surface manifest for the fault path |
| `ExecAuditRealRun/receipts/` | 18 receipts (§4-§6, §2) |
| `ExecAuditRealRun/pinned/` | the two as-run tool snapshots (`.py`, outside the receipt universe) |
| `ExecAuditRealRun/hreflang_audit_ref.py`, `receipts-driver.py`, `raw-scan.py`, `versions-writer.py`, `divergence-writer.py` | the instruments behind the receipts |

C2 real-input target as amended (Amendment 1): all 8 retained pages read — yes; each `page.html` sha256
verified against its `fetch.json` sha256 — yes, 8/8; output recorded — yes, exit 0 with an empty finding set;
the 4 not-served surfaces reported as not-served — yes. No file was written outside my wave directory and no git mutation was run. `git status` in the lane also
shows sibling seats' in-flight edits (`M corpus/SOURCES.md`, `?? corpus/knowledge/hreflang-declaration.md`);
those are not mine — my writes are exactly the paths tabulated above. No tool was installed or
upgraded (no pacman, no `uv tool`, no npx).
