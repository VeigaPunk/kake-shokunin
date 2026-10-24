# ReviewCensusBefore — census before + registry shape (kake, r31 w1)

Axes: freshness (is `.ufo/waves/round-31/census-before.txt` still the live state?) and
operability (does a wave-1 S057-S06x row keep `sources-census.sh validate` exit 0?).

## Commands run (all read-only; sandbox /fast/scratch/hyaku/kake-r31/w1/ReviewCensusBefore)

1. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → **exit 0**
2. `scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kake` → **exit 0**
3. `diff .ufo/waves/round-31/census-before.txt live-validate.txt` → only line 3 (`exit=0`,
   the capture command's own echo) is extra in the before file; findings lines identical.
4. `TMPDIR=<sandbox> scripts/sources-census.sh selftest` → **exit 0**, `96` killed
   mutants, `no survivors`, `selftest ok` — every E/W check below demonstrably fires.

## Live census output (validate, 2026-10-22)

```
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
```
exit=0. Byte-identical findings to `census-before.txt`; the before artifact is fresh
against the working tree (registry still ends at S056, next unused id is **S057**).

Census mode: kake rows=56 — tier.A=47, tier.B=1, tier.C=8; status mined=43,
queued=6, rejected=7; tier.invalid=0, status.invalid=0, missing=0.

The single W04 is the known intentional cross-scope pair: S028 (URI schemes) and
S033 (media types) both cite `https://www.rfc-editor.org/rfc/rfc9110.txt`. W04 is a
warning: it never changes exit status (header line 20 and selftest
`W04-does-not-fail-validation`).

## Row checklist — new S057-S06x keeps exit 0

Script-enforced (`scripts/sources-census.sh:523-703`, row_pass gawk + usedby_findings;
selftest-verified):

1. **Placement** — row inside the `## Registry` section (before the next `##` heading).
   An S-row anywhere else → E12, exit 1. 0-3 leading spaces tolerated; ≥4 = indented
   code, silently ignored.
2. **Column count** — exactly 13 pipe-fields = 11 cells (E01 otherwise, printed as
   `fields=N`); no `|` inside any cell (frozen contract, CORPUS.md:75).
3. **id** — `^S[0-9]{3,}$` (E02); unique across the table (E03). Script does not enforce
   ordering; contract says next unused, never reused → S057, S058, …
4. **source URL duplicates** — first `https?://…` token is normalized (strip `#fragment`,
   trailing `/`, scheme; lowercase host) then compared: same URL in a *different* scope →
   W04 (harmless, exit stays 0); same URL + same scope where a non-rejected row already
   exists → E04, unless `teaches` contains `supersedes S[0-9]{3}`.
5. **kind** — one of `spec|docs|paper|code|tool|dataset|talk|book|community|own-work`
   (E05). Render docs rows → `docs`.
6. **tier** — exactly `A`, `B` or `C` (E06); `community` + tier A → E10. Render
   web-services rows as tier A `docs` are fine; community tutorials must be C.
7. **status vocabulary** — `queued|mined|rejected` only (E07). `watch` is **not** a
   status (lands in status.invalid in census counts and E07 in validate). Recheck
   cadence travels in `recheck`, never in status.
8. **opened date format** — `YYYY-MM-DD`, a real calendar date (mktime round-trip),
   not in the future vs UTC today (2026-10-22) → E08. The four opens were
   2026-10-22, so this holds only if landed the same UTC day or later; a typo like
   `2026-10-32` or `2026-13-01` also fails.
9. **recheck** — valid ISO date, or `NNd` (e.g. `90d`), or a symbolic word
   (`[A-Za-z][A-Za-z0-9 _-]*`, e.g. `on-release`, `annual`) → E09. Symbolic cadences are
   reported by `overdue`, never judged overdue.
10. **used-by paths that must exist** — comma-separated repo-relative paths or `—`.
    For `mined` rows every listed path is checked on disk relative to the lane root
    (E11); mined with `—` → W03; tier C + mined with paths → W01. **E11 never fires for
    queued/rejected rows** — a queued row may carry a not-yet-existing path, but the
    moment status flips to mined the cited file must exist (i.e. before flipping
    S057-S060 to mined, `corpus/knowledge/render-web-services.md` and any lesson path
    must be committed in the same tree).
11. **teaches** — free text, but a `rejected` row needs ≥8 chars (W02); contract form is
    `REJECTED: <reason>; flip: <what would change the verdict>` (also what buys the E04
    exemption only via `supersedes S0NN`).
12. **Exit mapping** — any E-code (or overdue) → 1; warnings only → 0; missing registry
    → 2; so all E01-E12 above are the exact exit-0 surface.

Contract items (frozen SOURCES-CONTRACT-v1, CORPUS.md:64-121; partially census-visible,
not all script-enforced): anchor = exact section/heading/page/line **plus revision**
(never a bare homepage) — the C2 rows use retained-text sha256 prefixes and fetch
timestamps, consistent with S050-S055; teaches = one grounded learner benefit; opened =
date the author opened the source; round-lesson `## Gate` must record per new row the
URL, access date and a ≤25-word quote grounding teaches (rule 1; non-author re-open
sample); append-only — only status/recheck/used-by change in place with old→new logged
(rule 2); no credential material or session URLs (rule 6).

## Findings

- **INFO** — before artifact fresh: live validate reproduces
  `census-before.txt` exactly (findings lines and exit 0), lane still at S056. No
  drift since capture.
- **INFO** — checklist above is the complete E-surface, each check selftest-verified
  (96/96 mutants killed) on this exact script version.
- **RISK (low)** — `sources-census.sh` is the fleet script at
  `/home/vgpnk/Projects/shokunin/scripts/`, not pinned by hash in the before artifact;
  a future script change would shift the exit-0 surface without changing the before
  file. If the wave needs a pinned reference, record its blob with the before artifact.
- **RISK (low)** — E04/W04 normalize away fragments and trailing slashes only; URL case
  of the path is preserved except host lowercasing, so `…/rfc9110.txt` vs
  `…/RFC9110.TXT` would evade the duplicate check. No current row does this.
- **Not verified** — I did not mutation-test a hostile row against the live kake
  registry (lane writes are out of bounds for this seat); mutant behavior is attested
  by the script's own selftest fixtures, not by a live-lane probe. I did not check
  whether the S057-S060 rows are drafted anywhere; at review time they are not in the
  working tree.

Report: .ufo/waves/round-31/w1/ReviewCensusBefore.md
