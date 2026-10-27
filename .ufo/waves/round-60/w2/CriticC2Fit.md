# CriticC2Fit

ATTACKS: C2 operability-axis fit; whether append guard closes R59-D1; capability and controls.

AXIS:
The lane's AXES.md is absent at the stated B1 revision (`git show B1:AXES.md` fails), so I cannot verify a formal AXES.md definition that operability means runnable artifacts. Contract itself calls operability a lane tool (C2) and its scope is expressly a read-only CLI over committed corpus blobs. That supports a narrow runnable-artifact interpretation, but not a claim that it establishes publishing/web-property operation end-to-end. **[INFERENCE]** scorecard capability should remain scoped to the guard's described input/output and limits, not general publishing operability.

R59-D1:
The guard design directly addresses the reported c55 defect: it compares base-line byte subsequence rather than c55's byte-prefix rule, permits tagged in-file insertions, and preserves old content. C2 cases explicitly include R1 against the real lane history and K2/K15 cases that falsify the c55 prefix implementation. This is not a complete resolution of R59-D1 as a universal append-only guarantee: the contract explicitly discloses existential alignment ambiguities (CR1/P5) and rolling-base dependence; a guard run against an old base can let an untagged duplicate ride in a tag-led run. The correction is to state the operative guarantee narrowly as relative to a chosen base and accepted alignment, or tighten algorithm to require every inserted line in every alignment/run to satisfy intended tag semantics. Do not imply arbitrary correction authenticity; already out of scope.

CAPABILITY:
The C2 counter's do-nothing control is meaningfully nontrivial: declared 0/24, with additional always-clean, always-exit controls and c55 port; however, this is a contract assertion, not evidence I ran the frozen counter. Tool's observable feature is runnable and read-only by design, but whether it deserves lane-level axis credit is a scoring-policy judgment; it is not a publishing workflow or source verification system. The contract appropriately says it only covers scoped Markdown files and does not verify correction faithfulness. No independent executable counter output collected in this seat.

FINDINGS:

| severity | target file:line | issue | evidence command | fix |
|---|---|---|---|---|
| medium | `.ufo/waves/round-60/contract.md` C2 limits | C2's existential alignment rule is weaker than a per-insertion append-only guarantee when duplicates permit alternative alignments; a tag-led run can shelter untagged inserted material. This is explicitly admitted, not evidence of a broken frozen predicate. | Read contract § Stated limits: CR1/P5; inspected `w1/ExecGuardTool.files/append_guard.py` alignment implementation (`any_clean_alignment`, lines 275–302). | Describe capability as accepting at least one valid alignment relative to specified base; if stronger semantics are required, reject any untagged insertion under all admissible alignments and add adversarial cases. |
| low | `AXES.md` (absent at B1) | Formal lane axis definition unavailable at the specified build revision; cannot substantiate that a corpus guard is sufficient operability evidence beyond runnable artifact capability. | `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 8b33fd248d126b48d838af5c38bc175850f41a09:AXES.md` → `fatal: path 'AXES.md' does not exist`. | Keep C2 claim scoped to the implemented runnable guard; use the actual axis definition if it lives elsewhere. |

VERDICT: C2 is a plausible narrow runnable-tool operability claim and targets R59-D1, but it must not be advertised as a universal or semantically faithful append-only publishing capability; its own stated alignment limits materially bound the claim.