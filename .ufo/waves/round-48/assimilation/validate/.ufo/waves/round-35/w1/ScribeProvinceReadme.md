# ScribeProvinceReadme — round-35 PROVINCE + corpus/README drafts
Sealed-key exposure: none. Nothing under `/fast/scratch/hyaku/kake-r35/sealed/`
was read, listed, stat'ed, copied or grepped; no key content was requested.

## What was built

Two paste-ready drafts in the shape of the landed round-34 sections, written
from the retained round-35 texts, `corpus/SOURCES.md`, `SCORECARD.md` round-35
declaration and four wave-1 sibling reports. No network read by this seat.

- `/fast/scratch/hyaku/kake-r35/w1/ScribeProvinceReadme/province.md`
  — `## Round-35 security.txt publishing frontier step`, five paragraphs:
  held-ground entry + sources; the RFC's placement and field rules; the Pages
  build path (Jekyll dot paths, `include:`, Actions artifact dotfiles, ds4cc
  census, project-site base path); not-Core boundary; owned-property /
  out-of-province / open list. sha256 `2f62835b9f4d62b8e1cade46c7573c23cdb6f6af8975e5cfa8e6a590938e3e7a`, 103 lines, 1028 words.
- `/fast/scratch/hyaku/kake-r35/w1/ScribeProvinceReadme/readme.md`
  — `## Coverage — round 35 (2026-10-22)`, one coverage row plus the closing
  provenance paragraph (rows gained, S081 rejected, digests, no gate, ds4cc
  census, wave-1 reads, out-of-province). sha256 `3f27a9f5041d5b70e8798e498471eee57198a27bd268385c1ff658617e393e20`, 39 lines, 530 words.

Both files open with an HTML comment recording that
`corpus/knowledge/security-txt-publishing.md` does not exist at base, so the
integrator must check the entry-describing sentences against the landed entry
before paste. Neither draft claims a gate for this ground: it says the C2
counter reads entry text, cites, size and retained texts, not a served file.

## Commands run (exit codes)

All sandbox `TMPDIR=/fast/scratch/hyaku/kake-r35/w1/ScribeProvinceReadme/tmp`.
1. `mkdir -p …/ScribeProvinceReadme/tmp` and `wc -l PROVINCE.md corpus/README.md` → 0 (199 / 326).
2. `grep -n "^#{1,4} " PROVINCE.md corpus/README.md` → 0 (section map).
3. `read` PROVINCE.md `:120-199`, `:1-119`; README `:300-326` → 0 (round-34 shapes).
4. `python3` context extractors over `sources/S078,S079,S080,S082,S083,S084,S085,S006.txt` → 0 (facts + exact wording).
5. `grep -rn -i "security\.txt\|securitytxt" PROVINCE.md corpus/ scripts/ SKILL.md QUALITY.md SCORECARD.md` → 0; hits only `SCORECARD.md:1376,1427` (no prior ground in PROVINCE, corpus or scripts).
6. `grep -n "^| S00[126]\b" corpus/SOURCES.md`; `ls corpus/knowledge` → 0 (S001/S002/S006 rows read; no security-txt entry at base).
7. Quote checker (python3, whitespace-collapsed substring test of every `“…”` span against the eight retained texts) → 0: province.md 11 spans, 0 unmatched (S078 ×9 incl. signing/Expires/Content-Type/scope/Canonical, S080 ×1, S082 ×1 trivial `RECOMMENDED` later strengthened to the S078 signing sentence); readme.md 0 curly spans by design (prose row). Post-edit rerun → 0, 0 unmatched.
8. Bleed/sealed scan (python3, term list WCAG/accessibility/Render/Open Graph/CrUX/robots.txt plus `sealed`) → 0, all empty.
9. `mkdir -p .ufo/waves/round-35/w1` (already present) → 0; `wc -l` on four sibling scout reports → 0.

No build, no counter, no test run. No tool installed or updated.

## Findings that shaped the drafts (advisory)
1. **S001 citation defect avoided.** v4.0.0 hard-codes the dotfile exclude and
   has no `include-hidden-files`; that input first appears at v5.0.0
   (`ScoutPagesDotfilesSource.md`). The draft says exactly that, so it does not
   repeat the S001 over-claim that scout flagged.
2. **The lane's own publisher cannot serve the file today.** At `7fc6aa2f` the
   public tree has no `.well-known`, no `security.txt`, no `_config.yml`, a root
   `.nojekyll`, and one Pages workflow pinned to `upload-pages-artifact@v3`
   with `include-hidden-files` unset (`ScoutDs4ccWellKnown.md`). Whether that
   pinned tag already includes hidden files is open: the exclusion is
   documented as a v4.0.0 change, and no opened row settles the v3 tag. The
   draft names this as open rather than guessing.
3. **RFC 9116 is current.** No update/obsoletion relation; 1 verified erratum
   is a comment cross-reference and the 2 reported ones touch the `Expires`
   example's lowercase `z` and the ABNF CRLF line (`ScoutRfc9116Errata.md`).
   The draft therefore quotes normative sentences only and never §2.5.5's
   example.
4. **Project-site placement is unsettled.** A project site is served under
   `https://<owner>.github.io/<repo>/` (S040–S043), and no opened row says a
   subpath satisfies a domain-level `/.well-known/` placement; the draft
   forbids the entry from asserting it.
5. **S081 rejected as secondary**; nine retained rows (S006, S078–S085) carry
   body and visible-text sha256, so a later re-open compares digests.
6. Out-of-province named in both drafts: vulnerability handling itself (intake,
   triage, remediation, disclosure timing, bounty and policy operation, whether
   a contact channel works); writing, adding, building or deploying the file on
   an owned site is operator-owned; key custody is adjacent to `kagi`.

## Not verified
- The C2 entry does not exist at base; the drafts' sentences about it are the
  form to take once it lands (caveat comment at the top of both files).
- Sibling scout numbers were read, not re-derived by this seat; the drafts
  attribute them by report path and restate no census counts.
- No live request of any kind, no deploy, no build, no counter run; header,
  TLS and redirect conformance of S084/S085 is stated as unobserved.
- No lane tracked file, git index or jj state was touched; only this report was written.
