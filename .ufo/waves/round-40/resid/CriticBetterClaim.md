# CriticBetterClaim — static residual attack
Axes: operability (false findings and diagnostic correctness); freshness (accuracy of the amended guidance).
Commands executed: none; exit codes N/A. Critic/read-only seat: all new outcomes below are [INFERENCE], not executed checks or passes. No tools installed or updated.
Checked: current `scripts/sitemap_audit.py`, frozen contract, SKILL amendment, declaration/kill block, round-40 lesson/log, counter polarities, selftest cases and stored receipts.
Base comparison: `/fast/scratch/hyaku/kake-r40/shared/ref_fix.diff:3-41` supplies the three base-to-reference hunks; the inspected verification tree contained receipts but no diff. Current guard placement agrees with these hunks. This is not an independently recomputed hash comparison.
Aliases: T=`scripts/sitemap_audit.py`; C=`.ufo/waves/round-39/c1-contract.md`; A=`SKILL.md`.

## Strongest counterexamples [INFERENCE]
Common manifest: `{"version":1,"checks":[{"id":"c","file":"a.xml","sitemapUrl":"http://h.example/sitemap.xml"}]}`.
Let X be UTF-8 bytes `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>http://h.example/ab</loc></url></urlset>`. NUL below means an actual byte 0x00, not an XML character reference.

**F1 — build worse; preservation of sentence 7: wrong (MEDIUM).**
`a.xml` = `<?xml version="1.0" encoding="ISO-8859-1"?>` + X + NUL.
Base: only `encoding_invalid`; build: only `xml_malformed`; both failed-policy/exit 1. Sentence 7 explicitly makes a non-UTF-8 declaration `encoding_invalid` with no other finding (C:34-37), and the base checks that declaration first.
Evidence: T:183-193 now returns for NUL before consulting the declaration; exact insertion at shared diff:12-20. This is a changed contract diagnostic, not an improved rejection. Existing selftest encoding cases at `scripts/sitemap_audit_selftest.py:256-283` lack the NUL interaction.
Smallest safe correction: retain the NUL repair, but put the declared-encoding gate before it; add this interaction fixture.

**F2 — build worse against the retained D3 reading; “not changed”: wrong (LOW).**
`a.xml` = `<!DOCTYPE urlset>` + X + NUL.
Base: `doctype_present` because the prescan reaches the DTD event before the later NUL; build: `xml_malformed` before any prescan. Both failed-policy/exit 1.
Evidence: T:157-171,189-195; sentence 9 at C:39-40; retained precedence at A:1145-1147 and `corpus/lessons/round-40.md:30-32`. This is not a claim that the ambiguous s8/s9 ordering is universally source-mandated: it contradicts the round's explicitly retained choice.
Smallest safe correction: on NUL-bearing decoded text, preserve a DTD event reached in the prefix before the first NUL, then return xml_malformed otherwise. Do not simply allow the full NUL-interleaved stream to be re-sniffed as UTF-16. Keep F1's encoding precedence first.

**F3 — build worse under sentence 14's literal “at any level”; ignored-extension preservation: wrong (MEDIUM).**
In X replace the loc with `<loc>http://h.example/a<x:note xmlns:x="urn:x">&#9;</x:note>b</loc>`.
Ignoring the foreign element leaves `http://h.example/ab`, so C:44-48 (s14),60-73 (s21-26) require clean. Base predicts clean/exit 0; build predicts failed-policy/exit 1, `loc_not_absolute` at entry 1.
Evidence: T:101-102 includes the foreign child's TAB through unfiltered itertext; T:271-277 then applies the new T:70-71 guard to that contaminated value. This is a new false finding, even though extraction was already imperfect. The sampled foreign extension is outside loc (`.ufo/waves/round-40/c1_count.py:108`) and misses it.
Smallest safe correction: exclude foreign subtrees from element-value extraction while preserving their tail text, then apply s21 stripping and the URL guard. Do not ban mixed content to evade s14. Caveat: the prior review called general mixed-content values undefined (`.ufo/waves/round-39/resid/ReviewBuildContract.md:23-25`); this witness specifically invokes the explicit foreign-element rule, not arbitrary child markup.

## Other attacked input classes [INFERENCE]
| Input class | Comparison / statement status | Contract sentence and current code |
|---|---|---|
| Legitimate Unicode path/IRI: `http://h.example/é` | equal; no new Unicode rejection found | s22-26, C:61-73; T:67-86 |
| `%09`/`%0A` in loc, or percent-escaped path separators | equal; preservation holds, no decoding by the guard | s22,26, C:61-71; T:70,85,283-285 |
| Leading TAB/trailing CRLF in loc | equal, clean; A:1142-1143's unqualified “anywhere” is overstated | s21, C:60-61; T:101-102,272-275 |
| Non-object `"x"`, then a valid check with id `"x"`; integer 7 then string `"7"` | equal; no phantom id reservation | s4,33, C:22-25,90-93; T:332-344 |
| Distinct case/Unicode-normalization ids; repeated empty-string id | equal for distinct ids; better for repeats after missing-member checks; exact identity holds | s4, C:22-25; T:335-344 |
| Ordinary ASCII UTF-16LE/BE without BOM, no DTD | better: false clean becomes xml_malformed | s6,8, C:34-39; T:183-190 |
| BOM-less UTF-16 containing é whose bytes fail UTF-8 decoding | equal, encoding_invalid; A:1140-1141's blanket description is overstated | s6, C:34-37; T:183-186; counter E9 at `c1_count.py:92` |
| Interior literal/character-reference TAB/CR/LF in the actual loc; raw controls in sitemapUrl | better rejection, not evidence for rejecting escapes or ignored text | s4,21-22; T:70-71,272-277,349-351 |

The unrestricted “better without regressions” reading is overstated: F1 is a direct diagnostic regression; F2 changes the retained reading; F3 changes a contract-valid input's verdict under s14. These are fixable defects, not a necessary operability/freshness tradeoff. No round verdict is issued.
Guidance-only corrections: qualify loc controls as remaining after s21 stripping; qualify the UTF-16 statement by successful UTF-8 decoding; retain the source-versus-lane-reading distinction already corrected in S115.
Stored `.ufo/waves/round-40/verification/build/selftest-new-on-build.txt:1-2` says PASS 179/179, exit 0; that is read evidence only and does not exercise these new counterexamples.
