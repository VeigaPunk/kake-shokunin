# Kake R36 W1 — ScribeMistakeMine

Axes: freshness, operability.

## Behavior and findings

Drafted five new `## Mistakes` rows at `/fast/scratch/hyaku/kake-r36w1/ScribeMistakeMine/mistakes.md`: unsupported v2 size-cap loosening; S084 “whole served body” overstatement; “absent → English” misattribution to S079; C1 target slack/omitted nesting; and control key-blindness. Each row has a resolvable source path:line pointer, captured-by disposition, fix, and an observed failure witness or an explicit note that its proposed check was not run.

Deduplicated the all-false/unsourced control (`corpus/lessons/round-35.md:223`), round-34 census/control-description/registry/raw-byte issues (`round-35.md:78-81`) and the full-score control (`round-34.md:68`). The S074 overclaim was already drafted by the round-35 mistake miner (`.ufo/waves/round-35/w1/ScribeMistakeMine.md:42-44`) and disposed at `round-35.md:97`; not repeated.

## Sweep and commands

Used `grep` across the four requested lesson/spot-check files for Mistakes headings, the named candidate phrases, and routed defects; then `read` on the returned line ranges and exact raw ranges. Search hits located r35 routed defects 2–5 and the earlier mistake tables; reads confirmed the cited evidence and deduplication. The tool calls and search pattern are pasted in the sandbox draft. These read/search tools do not provide shell exit codes.

Only shell command: `timeout 300s mkdir -p /fast/scratch/hyaku/kake-r36w1/ScribeMistakeMine/tmp` — completed without output; Bash tool reported success (exit 0). A `read` mistakenly addressed `/fast/scratch/hyaku/kake-r36w1/ScribeMistakeMine.md` and returned “not found”; corrected to the actual `.../ScribeMistakeMine/mistakes.md` path.

## Gates, touched surfaces, limits

- Gates: no counter, tests, build, or live network request run. Existing failure witnesses are reported from cited closure/lesson text; the proposed new checks are explicitly unrun.
- Touched surfaces: sandbox draft above; this report only in the lane. No product code, tracked lane file, index, jj state, or Git state changed. No clone or tool installation.
- Sealed key: did not list, read, stat, search, or open `/fast/scratch/hyaku/kake-r36/` or run the counter.
- Provenance: findings are advisory source-text mining, not an admission or verdict. The search/read tools, not shell `grep`, were used for the source sweep.

Report: .ufo/waves/round-36/w1/ScribeMistakeMine.md