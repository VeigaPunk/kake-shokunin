# CriticSealedCasesFairness — revealed-key contract fairness
Axes: freshness, operability. Advisory static review of all 28 cases / 152 checks; no audit implementation, reference, counter, judge, admission or round verdict executed.
Evidence root E = `/fast/scratch/hyaku/kake-r36w2/CriticSealedCasesFairness/`. C=`E/SCORECARD.declared.md` (3555f63f); K=`E/cases.revealed.json` (fd1fb723624b742a00a6e8e908f3b42901d627f8); R=`E/case-review.txt`; D=`E/finding-derivations.json` (152 individual deciding reasons).
K sha256 `44c94838f31af6740a3f1bb4123abe6cbb8df0bbdd3414de7acbb3838863ef1d`; C sha256 `fae4688739e563cbf8e82b0c8083e8ffdde2861145cb0aa762c87fecd0c219ca`.
**Counterexample G08:** C:1606–1607 sketches every hop as `{status: integer, location: string}`, then says “a redirect hop needs location”; it never expressly marks location optional on nonredirects. Every case relies on that optionality. This is a fixable specification ambiguity, not a demonstrated implementation failure.
K:39–90 / R:1–7: k01 omits location on all five final hops. [INFERENCE] A literal-schema reading invokes C:1647–1650: five check_invalid findings, could-not-evaluate/2; the sealed key instead expects two gone + two http_error, failed-policy/1. This is an original sealed input, not an invented edge case.
Observed data census: 148 object checks; all 144 nonredirect terminal hops omit location. Counter materialization only renames ids/files, not hops (`E/sealed_count.pinned.py:114–140`); it does not cure G08.
Smallest safe correction: explicitly say “location is optional on nonredirect hops” in a disclosed contract amendment and qualify the old measurement as depending on that reading. A future key can supply empty terminal locations to avoid the dispute. Do not silently replace the frozen contract/key or rebrand old receipts as unambiguous.

## Per-case verdict and deciding sentence
Every row is **depends-on-undecided-point (G08)**, decided by the conflicting hop-schema/prose sentence above. Conditional on optional terminal location, no additional expected-finding contradiction was found. Below: missing=quote_missing; invalid=check_invalid; hold=no finding. Unlisted checks hold. C:1652–1653 + usage give failed-policy/1 for k01–k20 and could-not-evaluate/2 for k21–k28. D retains full contract sentences and check-by-check reasoning.
| Case / decoded evidence | Verdict | Conditional findings and deciding contract sentence |
|---|---|---|
| k01 R:1–7 | depends-on-undecided-point G08 | x1/x2 gone; x3/x5 http_error (403/206); x4 holds. C:1611–1613: “404 or 410: one gone finding”; “Any other status (including other 2xx): one http_error finding.” |
| k02 R:9–15 | depends-on-undecided-point G08 | Same findings, other statuses 503/202; x4 holds. Same deciding sentences C:1611–1613. |
| k03 R:17–23 | depends-on-undecided-point G08 | Same findings, other statuses 204/203; x4 holds. Same deciding sentences C:1611–1613. |
| k04 R:25–31 | depends-on-undecided-point G08 | Same findings, other statuses 429/226; x4 holds. Same deciding sentences C:1611–1613. |
| k05 R:33–37 | depends-on-undecided-point G08 | x1 moved→https://docs.example.org/a/b/x/page; x3 moved→https://b.example.com/two/three + gone; x2 holds. C:1617–1620: moved targets the last hop of the leading permanent run, in addition to final-status outcome; C:1611–1613. |
| k06 R:39–43 | depends-on-undecided-point G08 | x1 moved→https://cdn.example.net/r?id=7; x3 moved→http://example.net/v3/ + gone; x2 starts 303, so no moved. Same deciding sentences C:1614–1620; 303 is explicit policy. |
| k07 R:45–49 | depends-on-undecided-point G08 | x1 moved→https://example.org/new/guide/; x3 moved→https://site.example.io/p/r/s?page=2 + gone, stopping before 303; x2 holds. Same deciding sentences C:1614–1620. |
| k08 R:51–55 | depends-on-undecided-point G08 | x1 moved→https://modern.example.com/y; x3 moved→https://a.example.org/5/6 + gone; x2 holds. Same deciding sentences C:1614–1620. |
| k09 R:57–68 | depends-on-undecided-point G08 | x2–x5 missing: quotes only in script/style/template/comment. x1/6/7 hold. C:1622–1628 orders those removals, then tags, then references, and expressly keeps title; (d) supplies missing. |
| k10 R:70–81 | depends-on-undecided-point G08 | Same findings and deciding sentence C:1622–1632; &lt;and&gt; is decoded only after tags, so x6 holds rather than losing “and”. |
| k11 R:83–94 | depends-on-undecided-point G08 | Same findings and deciding sentence C:1622–1632; named references and NBSP become matching text under (c),(d). |
| k12 R:96–107 | depends-on-undecided-point G08 | Same findings and deciding sentence C:1622–1632; euro/times/equals references decode; x1/6/7 hold. |
| k13 R:109–117 | depends-on-undecided-point G08 | x4 missing (Moved versus moved). x1–x3 hold after whitespace deletion, tag concatenation, and NFKC ﬁ/ＲＦＣ. C:1629–1632: normalize NFKC, delete isspace, substring match; “matching is case-sensitive.” |
| k14 R:119–127 | depends-on-undecided-point G08 | x4 missing (GONE versus Gone); x1–x3 hold, including Ⅳ/ﬂ. Same deciding sentence C:1629–1632; plain-text x4 still fails case. |
| k15 R:129–137 | depends-on-undecided-point G08 | x4 missing (The Include Setting versus the include setting); x1–x3 hold, including ①/②. Same deciding sentence C:1629–1632. |
| k16 R:139–147 | depends-on-undecided-point G08 | x4 missing (lowercase versus Normalization Form KC); x1–x3 hold, including ＨＴＴＰ. Same deciding sentence C:1629–1632. |
| k17 R:149–161 | depends-on-undecided-point G08 | x2 unsupported_type (PDF); x5 missing (plain &amp; stays literal); x6 missing (XHTML script removed). C:1633–1636: plain decoded body is kept as is; any other type gets unsupported_type; C:1622–1625 expressly includes XHTML. |
| k18 R:163–175 | depends-on-undecided-point G08 | Same findings, unsupported type JSON; x1/x3/x4 hold. Same deciding sentences C:1633–1636,1622–1625. |
| k19 R:177–189 | depends-on-undecided-point G08 | Same findings, unsupported type SVG; literal comment/reference in plain x1 stays. Same deciding sentences C:1633–1636,1622–1625. |
| k20 R:191–203 | depends-on-undecided-point G08 | Same findings, unsupported octet-stream; literal script in plain x1 stays. Same deciding sentences C:1633–1636,1622–1625. |
| k21 R:205–220 | depends-on-undecided-point G08 | x3 charset_unsupported (shift_jis); x5 missing (UTF-8 café bytes decoded as windows-1252). x1/x2/x4 hold: alias, BE BOM override, UTF-8 default. C:1637–1644 explicitly defines those branches; (d) supplies missing. |
| k22 R:222–237 | depends-on-undecided-point G08 | Same findings, unsupported gbk; us-ascii alias, LE BOM override, UTF-8 default hold. Same deciding sentences C:1637–1644,1629–1632. |
| k23 R:239–254 | depends-on-undecided-point G08 | Same findings, unsupported koi8-r; LATIN1 alias, BE BOM override, UTF-8 default hold. Same deciding sentences C:1637–1644,1629–1632. |
| k24 R:256–271 | depends-on-undecided-point G08 | Same findings, unsupported euc-kr; Windows-1252 alias, LE BOM override, UTF-8 default hold. Same deciding sentences C:1637–1644,1629–1632. |
| k25 R:273–283 | depends-on-undecided-point G08 | null,x2–x5 invalid (nonobject, relative URL, escape, redirect without Location, terminal redirect); x6 gone; x7 missing; x8 holds. C:1647–1650: a manifest-rule violation gets one check_invalid and no other finding; other checks remain evaluated. |
| k26 R:285–295 | depends-on-undecided-point G08 | Same findings; nonobject=7, x2 FTP, x6=410. Same deciding sentence C:1647–1650 plus explicit URL/terminal-hop requirements C:1604–1610 and (a),(d). |
| k27 R:297–307 | depends-on-undecided-point G08 | Same findings; nonobject=null, x2 empty host, x6=404. Same deciding sentences C:1647–1650,1604–1610 and (a),(d). |
| k28 R:309–319 | depends-on-undecided-point G08 | Same findings; nonobject=list, x2 relative URL, x6=410. Same deciding sentences C:1647–1650,1604–1610 and (a),(d). |

## Mapping all 18 previously undecided points
U=`/fast/scratch/hyaku/kake-r36w1/CriticContractAmbiguity/ambiguity.json`, sha256 `7b6be0a4b47f0b271e0d797a22000cac934793f2a089cd9d0bd199e59df89ce3`; W1 report counts/index: `.ufo/waves/round-36/w1/CriticContractAmbiguity.md:13–35`. “None” means no sealed expectation depends on the disputed branch, not that the contract settles it.
| Point / U line | Dependent cases / reason |
|---|---|
| A01 / 3 | None: no non-200 check supplies an optional body/contentType. |
| B05 / 531 | None: redirect Locations have no unescaped-space/malformed-URI dispute. |
| B06 / 595 | None: all resolved redirect targets are HTTP(S) with hosts. |
| C04 / 850 | None: no comment synthesizes a suppression tag. |
| C05 / 908 | None: all suppression elements have matching end tags. |
| C06 / 966 | None: all comments have closing -->. |
| C09 / 1148 | None: no suppression tag occurs in a quoted attribute. |
| E01 / 1578 | None: unsupported-type checks use ASCII bodies and no charset; either decoding-order reading adds no charset finding. |
| E02 / 1647 | None: all contentType boundaries are ASCII; body Unicode whitespace is a different rule. |
| F03 / 2027 | None: no charset name has whitespace before =. |
| F06 / 2209 | None: no duplicate charset parameter. |
| G02 / 2402 | None: ordinary dictionaries serialize without duplicate members. |
| G03 / 2460 | None: every version token is 1, not 1.0. |
| G04 / 2518 | None: all status tokens are integers, not integral fractions. |
| G05 / 2576 | None: no disputed invalid percent escape; g URL failures violate explicit absolute/scheme/host rules. |
| G06 / 2634 | None: materializer writes regular files, not symlinks (pinned counter:117–125). |
| G07 / 2698 | None: materializer uses UTF-8 json.dumps text without a manifest BOM (pinned counter:137–139). |
| G08 / 2756 | k01–k28: omitted final Location; deciding sentences and counterexample above. |

303: k06/x2 and k07/x3 depend on classifying 303 as nonpermanent. C:1614 expressly does that, so it is not an undecided expectation. `.ufo/waves/round-36/w1/ScoutReopenS088.md:29,39–43` reports RFC 9110 never calls it temporary: fix the RFC attribution/identify lane policy, not the frozen behavior. I did not reopen the RFC over the network.
CP1252: no case depends on bytes 81/8D/8F/90/9D under windows-1252 (`.ufo/waves/round-36/w1/ExecProbeCp1252.md:7–17,38–45`). Only raw 81 occurs, in k13/k.html’s UTF-8 ﬁ (EF AC 81), not a CP1252-decoded check. All eight CP1252-decoded checks k21–k24/x1,x5 contain none of those five bytes; BOM bodies override labels. No quote contains those controls. Evidence: `E/static-census.json`, R:115,205–271. This is a coverage limit, not an unfair expectation.
Freshness/operability impact: an implementation following the literal displayed schema can disagree on every case; conversely these cases cannot establish the five-byte WHATWG/Python distinction. No extra contradiction found once G08 is resolved toward optional terminal location; no round-level conclusion is drawn.

## Executed commands and limits
Git environment: GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE removed before each git command; TMPDIR=`/fast/scratch/hyaku/kake-r36w2/CriticSealedCasesFairness/tmp`. Full commands/exits/stdout hashes: `E/capture-commands.json`.
`timeout 30 mkdir -p /fast/scratch/hyaku/kake-r36w2/CriticSealedCasesFairness/tmp` — exit 0, no stdout.
`timeout 30 git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 3555f63f:SCORECARD.md` — exit 0; captured C, 138498 bytes.
`timeout 30 git -C /home/vgpnk/Projects/shokunin/kake-shokunin show fd1fb723624b742a00a6e8e908f3b42901d627f8:.ufo/waves/round-36/sealed/cases.json` — exit 0; captured K, 81589 bytes, key version 2 / 28 cases.
`timeout 30 git -C /home/vgpnk/Projects/shokunin/kake-shokunin show f3a38bf8e68f6cee386125d34b5e95ac9b2df66e:.ufo/waves/round-36/sealed_count.py` — exit 0; static inspection only, sha256 `88ec59140258ce759107b7472fdd07a005b7c1bb8b3ba5218347e4518342ff8e`.
`timeout 30 sha256sum /fast/scratch/hyaku/kake-r36w2/CriticSealedCasesFairness/case-review.txt /fast/scratch/hyaku/kake-r36w2/CriticSealedCasesFairness/static-census.json /fast/scratch/hyaku/kake-r36w1/CriticContractAmbiguity/ambiguity.json` — exit 0; R=`812daccf…68206b`, census=`ced053ec…b8bcd8`, U hash above.
Bounded Python Eval data-only cells (30–90 s) decoded all bodies and recorded 152 static derivations plus the 18-point map. One report-count print hit NameError (cell exit 1), corrected without rerunning the extraction; final counts: 28 case rows / 18 point rows. Inferred alternative outputs are not executions.
Not verified: source_recheck runtime behavior, sealed pass count, controls/ablations, live-source freshness, canonical admission. No network, installs/upgrades, lane/index mutations except this report, or surviving child processes. All additional artifacts stay under E.
