# CriticReadingAB — control/oracle boundary
Axes: operability is the claimed capability surface; freshness is also lane-owned but is not assessed by this review (F:2354-2361; P:5-7).
Citation roots: lane-relative paths use `/home/vgpnk/Projects/shokunin/kake-shokunin/`.
F=`ceecb1b1f9093471eb0b17d2c9190e78bceb0b78:SCORECARD.md`; D=`915e9e87:SCORECARD.md`; T=`72edf2123f92b9dc546494cbffcc777ed3c3cd3a:SCORECARD.md`.
P=`/home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-39.md`; V=`.ufo/waves/round-39/verification`.
R37=`corpus/lessons/round-37-verifier-spotcheck.md`; R38=`corpus/lessons/round-38-verifier-spotcheck.md`.

Counterexample: the reference already scored 24/met=true, sha256 `663e051e10b9fca2db55fa13497b965fb19fb107b3791123769fc8534a2d69f8`; its attempt-3 receipt pins the same tool and frozen counter hashes (V/pre-summary.jsonl:40; V/a3/ref.json:2-12).
**Reading A [INFERENCE]: it is a control.** “Every tool scored” has no temporal qualification, and the sole exception is the exact build bytes—not oracle role, authorship or implementation completeness. The pre-build receipt therefore activates rule (1): exploratory, not a numerical admission (F:2380-2399).
**Report under A:** identify that receipt/hash and 24/met=true; say “C1 declared exploratory under kill rule (1).” Numerical scores remain diagnostic. A reasoned, named non-author exploratory review is required for `unprovable-but-better`; absent that, report `unprovable`, not measured success (F:2394-2399; P:29-35).

**Reading B, strongest case [INFERENCE]: it is the declared key-design oracle, not a control.** The original declaration separately records “Key-design evidence, L1 alone, before this declaration”; named shapes explicitly include reference mutants, and the control wave follows the declaration. Thus the distinction has contextual support in frozen text, not merely later convenience (F:2380-2393,2400-2403).
B also fits §6.9's purpose: exclude a do-nothing/work-skipping target, not require a correct oracle to fail. Unlike the round-38 wrapper exemption, the reference role was already named in this declaration (P:352-356; F:2380-2384; R38:76-89).
B's defect: naming a role does not explicitly exempt it; oracle and control membership can coexist. “Whoever wrote it and however much … implements” resists exactly that implied carve-out (F:2385-2388).
**Report under B:** explicitly state the assumed oracle exemption and identity, keep the numerical claim open, and report only actual build measurements and control consequences. Reference 24 is not an after-build result; a build below 24 misses, another qualifying control invokes the applicable kill rule (F:2378-2399).
Both outcomes and the unresolved interpretation must be disclosed; the recorded defect expressly leaves the declaration unchanged and does not settle it for the L1 (D:2408-2414).

**Strict-closure recommendation [INFERENCE]: adopt A.** The explicit universal class and sole exception outweigh the contextual B reading; adding an oracle exclusion now narrows the frozen rule after its successful score (F:2385-2396; P:351,357-360).
R37 refused an undeclared “does not skip the work” exemption despite reproduced passing numbers (R37:65-76).
R38 likewise rejected post-score classification, even accepting that excluded tools were correct implementations; substance did not rescue the declared boundary (R38:76-99).
Apply this round's actual consequence—pre-build exploratory—not R37/R38's different withdrawal/rejection wording. This is a claim-definition defect, not evidence that the sitemap implementation is wrong or an axis harmed (F:2394-2399; R38:109-111).
**Re-score:** under A it changes no disposition, but supplies an unambiguous post-declaration, pre-build 24 receipt; even a prospective-only interpretation of “scored” no longer avoids rule (1) (T:2416,2431-2432; V/a3/ref.json:2-12; F:2394-2396).
Under B a genuinely original role exemption would survive re-scoring the same oracle; timing alone cannot defend B after this re-score (F:2380-2388; D:2407-2411; T:2431-2432).
Existing check receipts demonstrate the disputed switch, not its legitimacy: A lists one meeting control/exit 1; B adds `--oracle-sha`, exempts that receipt/exit 0. The latter cannot adjudicate its own exemption (V/a3-jcheck/A.txt:1-6; V/a3-jcheck/B.txt:1-6; P:357-360).
Smallest safe correction [INFERENCE]: report A's exploratory consequence now, preserve both readings and frozen bytes; any future numerical re-claim must freeze an explicit oracle/build/control boundary before scoring, rather than silently retrofit this one (F:2394-2396; D:2412-2414; R38:97-99,168-173).

Source-retrieval commands, each exit 0 (recorded in the evidence artifact:2-5):
`timeout 30s git -C /home/vgpnk/Projects/shokunin/kake-shokunin show ceecb1b1f9093471eb0b17d2c9190e78bceb0b78:SCORECARD.md`
`timeout 30s git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 915e9e87:SCORECARD.md`
`timeout 30s git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 72edf2123f92b9dc546494cbffcc777ed3c3cd3a:SCORECARD.md`
Evidence deliverable: `/fast/scratch/hyaku/kake-r39a3w1/CriticReadingAB/evidence.txt`; sha256 `368f593ccaffcac744695704304c8275cedda19b3f2cf40c6381ac98c3640814`.
Hash command: `timeout 10s sha256sum /fast/scratch/hyaku/kake-r39a3w1/CriticReadingAB/evidence.txt && printf 'exit=0\n'` → exit 0.
Read-only analysis; no counter, build, test or judge run; no private reference implementation/key accessed; no installs or updates. Existing receipts above are not executions by this seat (evidence artifact:1-6,38-52,58).
