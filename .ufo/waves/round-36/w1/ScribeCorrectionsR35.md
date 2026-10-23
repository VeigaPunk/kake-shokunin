# Round 36, wave 1 — ScribeCorrectionsR35

## Behavior and findings
Drafted two append-only corrections in the sandbox. S084's Gate quote covers four of the seven retained fields, not the whole served body (`round-35.md:50`; `S084.txt:1`). The Preferred-Languages absent-field clause is stated directly in S078 RFC 9116 §2.5.8; the entry's `(S078, S079)` citation can be narrowed to S078 (`security-txt-publishing.md:51-52`; `S078.txt:1`). Both proposed notes quote the original and source and include repeatable grep commands. Original lane lines were not changed.

## Axes, gates, and surfaces
Axis: freshness / auditable source provenance. No build, sealed counter, test, or runtime gate was run; none was part of this editorial assignment. No source row or knowledge entry was edited. Lane writes were limited to this required report; the correction draft is in the sandbox. No network access, git command, package install, or sealed-key-tree access occurred.

## Commands and outcomes
- `mkdir -p /fast/scratch/hyaku/kake-r36w1/ScribeCorrectionsR35/tmp && export TMPDIR=/fast/scratch/hyaku/kake-r36w1/ScribeCorrectionsR35/tmp && printf 'workspace=%s\\n' "$TMPDIR"` — output `workspace=/fast/scratch/hyaku/kake-r36w1/ScribeCorrectionsR35/tmp`; exit 0.
- Workspace `grep` query `whole served body, field lines; 8 words` on `corpus/lessons/round-35.md` — match at line 50. Query `Acknowledgments: https://hackerone.com/github/hacktivity Preferred-Languages: en Canonical: https://github.com/.well-known/security.txt Policy: https://bounty.github.com` on retained `S084.txt` — match at line 1.
- Workspace `grep` query `absent, English may be assumed` on `corpus/knowledge/security-txt-publishing.md` — context lines 51-52. Query `If this field is absent, security researchers may assume that English is the language to be used` on retained `S078.txt` — match at line 1 and contains the quoted RFC sentence. The search tool exposes no process exit code; the grep command text in the draft is a reproducible shell equivalent, not a claim that shell grep was run. An initial query including unescaped `(S078, S079)` returned no match; the narrower literal phrase query returned lines 51-52.
- `sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-35.md /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/security-txt-publishing.md /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-35/sources/S084.txt /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-35/sources/S078.txt /fast/scratch/hyaku/kake-r36w1/ScribeCorrectionsR35/corrections.md` — exit 0.

## Evidence hashes
- `corpus/lessons/round-35.md` — `12820288f8319a93e87132a74b414faba75571807d80445cbf33b6bdf69b538e`
- `corpus/knowledge/security-txt-publishing.md` — `c402eb11005ef650fd4df869c3e36393970b81f3b7e1cdc63127aece822eebf1`
- `.ufo/waves/round-35/sources/S084.txt` — `35cf4b7ba43d9e84afaf5b56e145de6fe10758a82f794d46ac75ab9be043af58`
- `.ufo/waves/round-35/sources/S078.txt` — `4954ddcda4caf38985ebc7ea359a9c49fa78c5d9cbe14dde2bda794d39e50e44`
- Sandbox `corrections.md` — `e46299bd2fc9bc6281ef4ee674daf84f683d97e07aeacfdd0b908123e1171a76`

## Limits and artifacts
No tests or checks were run; no fresh source fetch was attempted. Report does not assert that the pasted shell commands were executed. Draft: `/fast/scratch/hyaku/kake-r36w1/ScribeCorrectionsR35/corrections.md`. Report: `.ufo/waves/round-36/w1/ScribeCorrectionsR35.md`.
