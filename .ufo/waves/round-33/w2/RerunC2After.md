# W2 RerunC2After — C2 after-measurement re-run (falsify)

Axes: freshness (primary, judged), operability (re-run determinism of the frozen counter), re-run agreement (my rerun vs frozen receipts).
Godspeed: axes named; probes run in parallel batches; no installs or updates performed (none needed).

## What I attacked
1. Re-ran the frozen counter `.ufo/waves/round-33/c2_pin_count.py` (blob 275476341e3a255cf2c4c7b3f9223561bd2e2668, identical at bc6c4a8, b1752a2, e490381, 1cf452e, 0a0acfb — no counter drift, so comparisons are apples-to-apples) in my own clone at 0a0acfb.
2. Attacked receipt honesty: do frozen receipts equal what the frozen counter actually outputs at those revs?
3. Attacked c4's teeth: is the "observed" verdict sensitive to page bytes/expected URL, or a constant?
4. Attacked upstream provenance: are the counter's PINNED blob ids really upstream 7fc6aa2f's objects?
5. Checked circularity: the counter never reads `.ufo/waves/round-33/verification/` (grep for verification/receipt/5777: no matches; it reads only `git ls-tree`/`show`/`archive` at `--rev`).

## Commands and exit codes (sandbox /fast/scratch/hyaku/kake-r33/w2/RerunC2After, TMPDIR set there)
- `git clone -q <lane> clone && git -C clone checkout -q 0a0acfb...` → CLONE_OK, rc 0.
- `python3 -B .ufo/waves/round-33/c2_pin_count.py --repo clone --rev <rev>` for 5777d5a, bc6c4a8, b1752a2, e490381, 1cf452e, 0a0acfb → rc 0 all six. Outputs saved: `/fast/scratch/hyaku/kake-r33/w2/RerunC2After/reruns/c2-<rev8>.json`.
- `git ls-tree <rev> -- .ufo/waves/round-33/c2_pin_count.py` × 5 revs → rc 0, same blob (see §1).
- Upstream (read-only, L1 clone /fast/scratch/hyaku/kake-r33/ds4cc-upstream): `log -1 7fc6aa2f` → `2026-10-21T17:32:55Z magga: Frostbite — Classic & Remastered at /magga/frostbite/`; `rev-parse 7fc6aa2f^` → 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28 (direct parent, so one commit); `diff-tree 1fbdb8ed 7fc6aa2f` → 9 added paths under magga/frostbite/ (3 index.html pages + js/assets), M magga/README.md, M magga/index.html, M sitemap.xml; loc count 97 → 100 = +3. rc 0 all. Matches declared claim (three new pages, +3 locs).
- Independent provenance: `git fetch --depth=5 gh 7fc6aa2fc12451dd451fed5a9ee7125f3a90e884` from https://github.com/VeigaPunk/ds4cc-marketplace.git into my sandbox clone → FETCH_OK, rc 0; `ls-tree -r 7fc6aa2f` on the fetched commit returned all four PINNED ids: sitemap.xml 67d8c7a50dc3a3734ce4be97ffa4810e1e257e12, frostbite/index.html e0d9ee29d9f1bf21faa0238e3253d4e9199304de, classic/index.html 12c58e2dae534f6569015fa3c0ec8cde502c5119, remastered/index.html 4e6d70ae05272e089f4564b1ed6f3c9b21a440a2, all mode 100644 — exact match to PINNED in the counter.
- A GitHub API attempt (`curl api.github.com/.../commits/7fc6aa2f`) returned no sha (likely host rate limit); superseded by the fetch above, which is the stronger check.

## Results
### 1. Re-run vs receipts (JSON deep-compare, byte-equal semantics)
- 5777d5a: met 0/4 — IDENTICAL to c2-before-5777d5a.json.
- bc6c4a8: met 0/4 — IDENTICAL to c2-at-bc6c4a8.json.
- b1752a2: met 4/4 — IDENTICAL to c2-after-b1752a2.json (declared "after" value reproduced).
- e490381: met 4/4 — IDENTICAL to c2-at-e490381.json.
- 1cf452e: met 4/4 — IDENTICAL to c2-at-1cf452e.json.
- 0a0acfb (tip, no receipt): met 4/4, all conditions true, detail identical in shape (100 locs, stated 100, three canonical clean) — pin holds at tip.
Zero differences anywhere. The receipts are faithful recordings, not hand-authored claims.

### 2. c4 teeth probes (rev tip's own scripts/canonical_audit.py on extracted retained bytes)
- Control (pristine frostbite/index.html, expected = own URL): `{"findings":[],"pagesChecked":1,"verdict":"clean"}` — matches counter's observed.
- Tampered page (canonical href → https://ds4cc.com/evil/, expected = own URL): verdict `failed-policy`, finding `canonical_mismatch` — c4 would flip false if the doc claimed clean against such bytes.
- Crossed input (classic page bytes, expected = root URL): `failed-policy` / `canonical_mismatch`.
- Wrong expectedCanonical on pristine page: `failed-policy` / `canonical_mismatch`.
- Minimal handcrafted page (selftest-style): `clean` — audit logic sane on simple input.
So the c4 verdict is a real function of retained bytes + expected URL, not a constant. Spy instrumentation (module-import of the counter with subprocess.run wrapped) captured the counter's exact argv+manifest at tip: manifest inside RETAIN_DIR, one page per manifest, audit path `<tmp>/x/scripts/canonical_audit.py`, output rc 0, `verdict:"clean"` for all three pages — my probes matched it exactly once corrected.
- Honest note: my first teeth probe false-alarmed (`failed-policy` on "pristine" bytes) because an earlier probe mutated the extracted page and never restored it. Re-run on genuinely pristine bytes resolved it to harness contamination, not a counter defect. No finding against the counter.

### 3. Bound checks
- `canonical_audit.py` does no network I/O (doc line 4-5 "does not ... fetch URLs"; imports urllib.parse only; subprocess only for its internal selftest). The counter's c4 therefore makes no live request to ds4cc.com when run — owned-sites bound respected by the counter itself and by my probes.
- All writes confined to /fast/scratch/hyaku/kake-r33/w2/RerunC2After (clone, reruns/, tmp/); lane untouched except this report.

## Findings by severity
- None (no defect found). C2 declared after-value (met 4, guard conditions c1-c4) reproduced exactly at b1752a2, e490381, 1cf452e and now also holds at tip 0a0acfb; before/base values (met 0) reproduced; upstream provenance independently confirmed from github.com including the +3 sitemap locs (97→100) and single-commit advance from 1fbdb8ed at 2026-10-21T17:32:55Z.

## Residual risk / not verified
- c4 by declared contract trusts the revision's own audit script output; a rev whose audit script unconditionally printed `clean` would pass c4. I deliberately did not push this line — it is adjacent to the held items (KakeR31.CriticC1Counter; "no item asks whether a counter may trust runner-reported codes"), so I stopped at input-sensitivity of the audit itself.
- Negative-path mutations of c2 (SOURCES.md row) and c3 (heading section) logic were not run; both were exercised only on the positive path (plus the met-0 revs where they correctly fail). My assignment was re-run + comparison, so this is recorded, not remedied.
- Counter does not check the audit subprocess's exit code (parses stdout JSON only); a nonzero-exit-but-valid-JSON run would still compare verdicts. Consequence-free in every observed run (rc 0); noted as hardening margin, not a defect.
- sitemap-locs compares a single stated line to the XML-parsed count; a second malformed `sitemap-locs:` line elsewhere in the section is caught (regex `^sitemap-locs: (\d+)$` with len==1 check).

Report: /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-33/w2/RerunC2After.md
Raw rerun outputs: /fast/scratch/hyaku/kake-r33/w2/RerunC2After/reruns/c2-{5777d5af,bc6c4a8d,b1752a24,e4903817,1cf452ea,0a0acfb1}.json
