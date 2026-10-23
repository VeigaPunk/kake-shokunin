# ExecD1Check — round 40, wave 1 (operability)

Built the D1 enforcement check and showed it can fail. The round's mined mistake — a routed defect
("fix D1") accepted without re-deriving it from its source — would have made a `version="1.1"`
urlset rejectable; the declaration (`SCORECARD.md:2571-2574`) rejects that fix, and this check
enforces the rejection.

## Artifacts (all under /fast/scratch/hyaku/kake-r40w1/ExecD1Check/)
- `d1_check.py` sha256 `8949aea5633130d2e56cfdc597014bab1dafa373ff562b508f541956e76b7131` —
  `--tool <path> [--out <receipt.json>]`; two files written UTF-8, byte-identical apart from the
  declaration's `version` (`documents_isolated: true` asserted), 1.0-only content (two in-scope
  `loc`s, valid `lastmod`/`changefreq`/`priority`); one manifest and one run per file; exit 0
  green, 1 red, 2 cannot-evaluate.
- `mutant_d1_fixed.py` sha256 `45f9c9e5a130e40709fb9328fbca3f13aeb69664dbbea63cd3005f79472b7ec1` —
  `ref_fix.py` plus `_declared_version(text) != "1.0" → xml_malformed` (the rejected D1 fix);
  `diff -u /fast/scratch/hyaku/kake-r40/shared/ref_fix.py mutant_d1_fixed.py` exit 0, only that
  helper and 3-line gate.
- receipts: base `2cdd4bec`, ref `66c1e663`, mutant `88134bd5`, const-clean `de13d828`,
  absent `f878c4a5`, counter `2ba086ee` (sha256 prefixes; full values in the sandbox).

## Runs (python 3.14.8, lane tip f043c72; `timeout 120 prlimit --as=4000000000 python3 -B`)
| tool | observed | exit | verdict |
|---|---|---|---|
| `scripts/sitemap_audit.py` (base) | v11 exit 0 clean []; v20 exit 1 findings `[[xml_malformed,null]]` | **0** | reading holds |
| `/fast/scratch/hyaku/kake-r40/shared/ref_fix.py` | identical pair | **0** | repair never touches D1 |
| `mutant_d1_fixed.py` | v11 `[[xml_malformed,null]]` (fails); v20 same (passes) | **1** | catches the D1 fix |
| `.ufo/waves/round-40/controls/l1/const_clean.py` | v11 clean (passes); v20 clean (fails) | **1** | catches `2.0` blindness |
| `/nonexistent/tool.py` | cannot-evaluate | **2** | operability path |

Counter (`c1_count.py` sha256 `6d73b8f4…`) on the mutant, `--label ExecD1Check-MutantD1`: exit 0, `passed 30/30`, `byClass E 9/9 U 13/13 R 8/8`, `selftest PASS 150/150`, `met true`, seed 20825759536453.

## Attacked statements
- **"the D1 rejection can be enforced"** — holds: a two-file differential (same bytes, only
  `version`) is green on base and on the reference repair.
- **"shown able to fail"** — holds both ways: over-application (mutant rejects `1.1`, exit 1) and under-application (const-clean accepts `2.0`, exit 1).
- **"a routed defect accepted without re-deriving it would have broken the tool on D1"** —
  *overstated as written*: the D1 fix breaks nothing the round measures. The mutant meets the
  frozen predicate exactly (30/30, selftest 150/150, `met true`); "broken" holds only against
  contract sentence 8. That is the mined-mistake point restated: the predicate is blind to D1 and
  only a dedicated check catches it.
- **"D1 is not a deviation"** — enforceable and falsifiable, so the declaration is operative; the
  reading's truth is CriticD1Reject's call. The check is green on base and ref because it encodes
  the same reading, not because it proves it.

## Findings
- `SCORECARD.md:2571-2574` declares D1 not a deviation; `.ufo/waves/round-40/sources/xml-1.0.html:517-520`
  carries the Note ("process it as a 1.0 document") and, at :517, `SHOULD NOT` — a document
  constraint, not a well-formedness constraint, which is what keeps sentence 8 satisfied.
- `ref_fix.diff` has no version hunk (only U/E/R at contract :67, :184, :334 regions), confirmed behaviourally by the base/ref green pair.
- `c1_count.py` witnesses contain no `1.1`/`2.0` document: the mutant's 30/30 is structural, not
  seed luck.

## Risks / blockers
- Enforces a reading, not a proof: if the D1 rejection were wrong, the check is green on the wrong behaviour.
- `version="1.1"` acceptance is expat behaviour (Python 3.14.8); a future interpreter that rejects it turns base and ref red for an environmental reason, distinguishable from regression only via the per-case receipts.
- Not wired into the predicate or selftest (out of scope): a post-build D1 regression would still
  meet C1 — demonstrated, not assumed.
- No blockers. No installs; no git/jj mutation; writes confined to the sandbox and this report.
