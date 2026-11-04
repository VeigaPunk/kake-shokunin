# ReviewerC2 — C2 attack report (kake round-76, w1, attempt 1)

Seat: ReviewerC2-7 (leaf; no subagents dispatched). Date: 2026-11-03.
Scope: attack claim C2's tool and case set before the after-state is claimed, per the
frozen contract §C2 and frozen amendments 1–2. Report paths are relative to the lane
checkout root; everything cited lives under `.ufo/waves/round-76/w1/ReviewerC2/`.

## Targets and bytes (pinned, drift-checked at close)

- Tool `ExecAuditTool/hreflang_audit.py`, final sha256
  `0762452fd86e55d6e34dd9072260ff0ae864fdf9199b8ff4734d09ecb8b60aac` (mtime 22:05:44).
  An intermediate revision `0a2454c6dfd6abadaf433bcdd29f5dddd44677ce8b20daa11eadb8774610bc05`
  (mtime 22:02:29) was attacked first; two defects found there are F1/F2 below.
- Matrix `ExecAuditMatrix/c76_hreflang_matrix.py`, final sha256
  `4958ede07559d15cfb95af57b99dcaee98883420a071847f78f02db248ad7756` (mtime 22:07:06);
  case set `ExecAuditMatrix/cases/` sha256 `a9401da4ace885bb37ffa8d4998c2692102c5db5444ffd6bd658d092a08b88b4`
  (71 case files at close; 44 existed at review start — the author re-derived the
  previously-undecided classes under amendment 2 while the review ran).
- Neither file changed between my last run and the sha re-check at report time.

The delivered tool was absent at review start (w1 held only `ScoutHreflangSources/` and
`swarm-registry.json`), so per seat spec I first implemented the contract in scratch and
attacked that; the delivered tool landed mid-review and became the sole target. No
subagent was used; scratch `/fast/scratch/hyaku/kake-r76/ReviewerC2-7` is removed at the
end of this review; nothing was written outside `w1/ReviewerC2*/`. No tools were
installed (operator 2026-10-19 authorization noted; python3 stdlib sufficed). Network
use: three public GETs of public documentation URLs (developers.google.com,
rfc-editor.org, iana.org), fetched 2026-11-03, saved and quoted in
`ReviewerC2/receipts/sources-quotes.txt`.

## Method

1. Pinned the attacked bytes into scratch; read every decision region.
2. Built 49 adversarial fixtures (`ReviewerC2/fixtures/`), ran each through the pinned
   tool (`--manifest … --root … --json`, TMPDIR inside scratch), recorded command,
   full stdout and exit per case (`ReviewerC2/receipts/case-*.txt`), compared with the
   verdict my contract+amendment reading derives (`receipts/verdicts-final.json`).
3. Ran the frozen matrix against the tool and against two adversarial A16 mutants and
   one multiset-collapse mutant (`receipts/matrix-*.txt`).
4. Re-derived the 3 still-undecided frozen cases' notes and named remaining gaps.
5. Grepped the tool for temp-dir literals and network imports (`receipts/tool-hygiene.txt`):
   0 hits each.

## Result summary

- Final battery: `cases=49 confirmed=6 ambiguous_conf=42 ambiguous_div=1 mismatch=0`
  (`receipts/driver-console-final.txt`). "ambiguous_conf" rows match the amendment-derived
  verdict; their notes record contract silences the amendments settled or limits.
- Matrix as delivered: `cases=71 decided=68 correct=68 wrong=0 undecided=3 constants_failed=4/4 met=true`
  (`receipts/matrix-asdelivered.txt`, exit 0).
- A16 falsification attempts all failed to sneak through (good): a bare
  `{"findings":[],"exit":0}` printer is wrong on all 68 decided cases with
  `shape=report lacks version,pages,counts`; a `pages=999` printer is wrong with
  `shape=pages=999 but manifest has N` (`receipts/matrix-a16-bare.txt`,
  `receipts/matrix-a16-pages.txt`).
- Multiset falsification: a tool emitting one `hreflang_self_missing` where a case
  expects 3× self_missing + 3× nonreciprocal is scored wrong (`receipts/matrix-multiset.txt`,
  my witness case `reviewerc2-multiset-cycle`). The counter's multiset rule holds.
- No matrix defect found: no constant passes every decided case
  (`constants_failed=4/4`); no correct-tool-fails-a-decided-case found on the final bytes.
- Tool selftest on final bytes: `selftest 59/59 passed`, `exit: 0`
  (`receipts/tool-selftest.txt`).

## Findings by severity

**F1 — tool defect vs A13, found on `0a2454c6…`, FIXED in `0762452f…`.**
The intermediate revision's `rel_tokens()` docstring said "ASCII-lowercased rel tokens"
but never lowercased the rel *values*, so `rel="ALTERNATE"` was invisible to the
alternate scanner. Observed on the intermediate bytes: fixture X01 (`rel="ALTERNATE"
hreflang="en-GB-oed"` over an invalid tag) returned `exit: 0` with no findings
(`receipts/history-driver-run-sha0a2454c6.txt`, line `X01   exit=0(exp 1) ids=[] exp=[hreflang_invalid_tag] info=[] pages=1 MISMATCH`).
On the final bytes the same fixture returns `exit: 1` with
`"id": "hreflang_invalid_tag"` (`receipts/case-X01.txt`), and the frozen case set now
carries `structure-rel-uppercase` expecting the same. Evidence note: the intermediate
receipts were overwritten by re-runs; the historical console above is the retained proof.

**F2 — selftest defect, found on `0a2454c6…`, FIXED in `0762452f…`.**
The intermediate revision's embedded selftest failed 5 cases (33/38, exit 1) because its
expectations contradicted amendments A2/A4/A9/A13: `relative_href_red`,
`relative_href_scheme_relative_red`, `relative_href_absent_red`,
`multiple_xdefault_red`, `alternate_stylesheet_red`. At that moment the C2 claim
"its own selftest passes" was false. On the final bytes: `selftest 59/59 passed`,
`exit: 0` (`receipts/tool-selftest.txt`). Evidence gap: the failing run's receipt was
overwritten by the final-byte re-run; the FAIL lines are quoted in-session only
(command recorded: `python3 -B <tool> --selftest --work <scratch>/tmp/selftest` at
~22:04). L1 may treat F1/F2 as closed-with-evidence or ask the tool author to co-sign.

**F3 — contradiction with a fetched source; OPEN, needs an L1/planner decision (not a
kill; verdicts remain derivable).**
The contract rule `hreflang_nonreciprocal` demands the return alternate carry *the same
tag*. Google's documented rule is weaker and different: "Missing return links : If page
X links to page Y, page Y must link back to page X."
(`receipts/sources-quotes.txt`, fetched 2026-11-03) — a return link, not a same-tag
link. Google's own canonical mixed-language cluster — page A (`en`) declaring
`en→A, fr→B`; page B (`fr`) declaring `en→A, fr→B` — is flagged twice by the as-written
rule. Receipt: `receipts/case-G01.txt` on the final bytes shows exactly this cluster
decided `exit: 1` with `hreflang_nonreciprocal` twice. Consequence: any real-world
cluster following Google's pattern (very likely among the 8 retained surfaces,
amendment 1) will mass-flag `hreflang_nonreciprocal` in the real-input run. Either the
contract should be amended to "B declares a return alternate with A's url" (drop
same-tag), or the capability row must state this strictness explicitly. I did not change
the contract or the matrix; the tool correctly implements the contract as written.

**F4 — grammar limits vs RFC 5646/IANA; derivable, record as limits (no kill).**
The frozen ASCII grammar rejects tags that are valid BCP-47:
`en-GB-oed` (IANA: `Type: grandfathered / Tag: en-GB-oed`, deprecated in favor of
`en-GB-oxendict`), `zh-yue` (IANA `Type: redundant / Tag: zh-yue`), and extension
singleton tags like `en-u-ca-gregory` (RFC 5646's ABNF has extension singletons;
variant grammar is `5*8alphanum`). The contract's verdict (`hreflang_invalid_tag`) is
derivable — frozen cases `invalid-tag-grandfathered-oed` and `invalid-tag-extension`
decide it — so this is not a defect; but the honest sentence for the capability row is
"validator for the frozen ASCII hreflang grammar", not "BCP-47 validator". My fixtures
T01–T04 document each with receipts.

**F5 — remaining undecidable classes (contract defects to name, per the seat spec).**
1. *Whitespace around the href value* (fixture H06, `receipts/case-H06.txt`): A12 makes
   RFC 3986 the parse authority, and ` https://… ` does not parse under it (→
   `hreflang_relative_href`, and via A4 the padded link cannot self-satisfy →
   `hreflang_self_missing`); the tool strips surrounding whitespace (WHATWG reading) and
   returns clean. The tag side is settled (frozen `invalid-tag-padded` = the literal
   reading; my T09 matches it), leaving the tool internally asymmetric: tag values are
   grammar-matched raw, href values are stripped. One amendment term ("surrounding
   ASCII whitespace is stripped from attribute values before parsing/matching") settles it.
2. *Shared-file fault id* (frozen `undecided-shared-file`): A15 forbids two pages
   sharing a file but names no id. My X08 shows the tool already faults it as
   `input_unreadable` and exits 2 (`receipts/case-X08.txt`); deciding the frozen case to
   `{exit 2, [input_unreadable]}` would cost nothing and is consistent with A15's
   sentence.
3. *svg/template crossing* (frozen `undecided-svg-template-crossing`) and *encoding
   policy for undecodable bytes* (frozen `undecided-unreadable-undecodable`): genuinely
   unstated; the tool's latin-1 fallback means byte-undecodability never fires, which
   should be stated as a limit if kept.

**F6 — A16/A2 checks (matrix side): no defect.**
The counter validates the full report shape (version/pages/findings/counts/exit, pages
count vs manifest, exit-field == process exit), compares ids as multisets, excludes
`hreflang_external_target` from scoring, and its selftest actively asserts that an
all-passing constant is a matrix defect. My two mutants and the multiplicity-collapser
were all rejected. `met=true` on the delivered pair is honest: 68/68 decided correct.

**F7 — process notes for the L1.**
- My first battery draft mislabeled six Google-pattern fixtures as "cross-clean";
  the tool was right and my expectations were wrong. Fixed mid-review; the corrected
  fixtures are what landed. Recorded for honesty since the intermediate console shows
  those MISMATCH rows (`receipts/history-driver-run-sha0a2454c6.txt`).
- Amendment 1 (real-input population = 8 retained served pages, 4 recorded
  `not-served`) concerns `ExecAuditRealRun`, not this seat; I verified nothing about the
  real run. The capability row must say 8, per amendment 1.
- Tool hygiene: no temp-dir literal, no network imports (`receipts/tool-hygiene.txt`);
  matrix runs used `--work` under my scratch only.

## Verdict table

Machine rows: `ReviewerC2/receipts/verdicts-final.json`; per-case stdout/exit:
`receipts/case-<id>.txt`. Statuses: CONFIRMED = observed equals a verdict derivable from
the base contract alone; AMBIG-CONF = observed equals the amendment-2-derived verdict and
the row carries the settling term; AMBIG-DIV = still formally undecidable (H06 only).
Highlights (full 49 rows in the JSON):

| case | observed | expected | status | note |
|---|---|---|---|---|
| T01 en-GB-oed | exit 1 invalid_tag | same | CONFIRMED | F4 limit, IANA-grandfathered |
| T04 en-u-ca-gregory | exit 1 invalid_tag | same | CONFIRMED | F4 limit, RFC 5646 extension |
| T06 X-DEFAULT ×2 | exit 1 dup+2×multi_xdefault | same | AMBIG-CONF | A11+A2 per-annotation |
| T09 ` en ` | exit 1 invalid_tag | same | AMBIG-CONF | frozen invalid-tag-padded decides the literal reading |
| H01 `&amp;` reciprocity | exit 0 | same | AMBIG-CONF | A13 entity decode |
| H02 uppercase scheme/host | exit 0 | same | AMBIG-CONF | A3 normalization |
| H05b absolute+fragment | exit 1 self_missing | same | AMBIG-CONF | A3 preserves fragments |
| H06 padded href | exit 0 | [relative, self_missing] literal | AMBIG-DIV | F5.1, the one open class |
| S05b svg link | exit 0 | same | AMBIG-CONF | A13 svg not scanned |
| R01 all-pairs 3-cluster | exit 0 | same | AMBIG-CONF | fully reciprocal cluster is clean |
| R07 version 2 | exit 64 | same | AMBIG-CONF | A15 |
| R08 fault+findings | exit 2 [invalid_tag, dup_url] | same | AMBIG-CONF | A8 coexistence |
| C02 trailing-slash canonical | exit 1 canonical_not_self | same | AMBIG-CONF | A3 slash significant |
| X01 rel="ALTERNATE" | exit 1 invalid_tag | same | AMBIG-CONF | F1 fixed; frozen structure-rel-uppercase |
| X05 relative href self | exit 1 relative+self_missing | same | AMBIG-CONF | A4 |
| X07 symlink page | exit 2 input_unreadable | same | AMBIG-CONF | A15 |
| X08 shared file | exit 2 [canon, self, input_unreadable] | same | AMBIG-CONF | F5.2 id naming |
| X10 triple duplicate | exit 1 dup ×2 | same | AMBIG-CONF | A2 per repeat occurrence |
| G01 Google-pattern cluster | exit 1 nonreciprocal ×2 | same per contract | AMBIG-CONF | F3 contradiction with Google |

## Residual risk and verification gaps

- My 49 fixtures overlap but do not replace the frozen 71-case matrix; the matrix's own
  sha-recorded receipt (`receipts/matrix-asdelivered.txt`) is the scoreable one.
- The intermediate-revision findings F1/F2 rest on one retained console receipt plus
  in-session quotes; the bytes themselves were overwritten by the author's fix.
- I did not run the 8-surface real-input audit (another seat's deliverable under
  amendment 1). F3 predicts mass `hreflang_nonreciprocal` there if the surfaces follow
  Google's pattern; that prediction is unverified by me.
- The 3 frozen `undecided-*` cases stay excluded from scoring; F5 recommends terms for
  two of them and a limit statement for the third.
