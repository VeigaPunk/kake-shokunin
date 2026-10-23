# Round 37 wave 2 — DiffToolVsIndependent
Axes: operability (tested), freshness (no live-surface claim).
Measured revision: `79d3c780f9afb9bc013e3b13e73ee73e6a8ac13c`. No lane source/index/jj mutations.
Sandbox `S=/fast/scratch/hyaku/kake-r37w2/DiffToolVsIndependent`; evidence `E=$S/evidence`; clone `C=$S/clone`.
L/I/R below mean landed / independent / L1 reference, respectively.

## Commands and observed results
All Python commands ran from S with this exact prefix: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u KAKE_ABLATE TMPDIR=/fast/scratch/hyaku/kake-r37w2/DiffToolVsIndependent/tmp`.
Setup: `mkdir -p /fast/scratch/hyaku/kake-r37w2/DiffToolVsIndependent/tmp && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r37w2/DiffToolVsIndependent/tmp timeout 120 git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r37w2/DiffToolVsIndependent/clone && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r37w2/DiffToolVsIndependent/tmp timeout 60 git -C /fast/scratch/hyaku/kake-r37w2/DiffToolVsIndependent/clone checkout -q 79d3c780f9afb9bc013e3b13e73ee73e6a8ac13c` — exit 0, no output.
Read-only source commands: `timeout 30 git show 79d3c780f9afb9bc013e3b13e73ee73e6a8ac13c:<path>` for `scripts/robots_audit.py`, `.ufo/waves/round-37/retained/independent/independent_robots_audit.py`, `.ufo/waves/round-37/sealed/reference/ref.py`, and `.ufo/waves/round-37/sealed/reference/declaration.md` — each exit 0; read in C with Git variables unset.
`timeout --kill-after=3s 600s python3 -B differential.py generate-run` — exit 0: 8192 checks, 128 manifests, 384 CLI runs, 174 check disagreements, no crashes, zero L/I disagreements.
`timeout --kill-after=3s 600s python3 -B differential.py minimize` — exit 0: final reduction gives 98 ASCII-group disagreements, 76 exemption-order disagreements, 5 distinct minimal reproducers, all 5 confirmed through all three real CLIs. Earlier reduction passes also exited 0 (28, then 4 reproducers); final pass preserves the original causal family.
Seed 20261023; 1024 generated robots files. Grammar includes groups, ignored keys, comments, BOM, mixed CR/LF/CRLF, wildcards, terminal/nonterminal `$`, percent escapes, non-ASCII, empty/orphan rules, invalid UTF-8 and byte-limit edges. Checks include empty paths, queries/fragments, valid/invalid agents, statuses 199/200/201/204/206/299/300/399/400/401/403/404/410/429/499/500/503/599/600, boolean and float.
Each CLI was bounded by `timeout --kill-after=1s 20s /usr/bin/python3 -B <tool> --manifest <manifest>`; full argv, exit, stdout, stderr retained in `E/generated/<batch>/outputs.json`. At most three tool subprocesses concurrently; no network requests or installed tools.

## Exhaustive disagreement list and minimal reproducers
`E/disagreements-minimized.json:1-5312` records EVERY one of the 174 original checks, all three observed finding lists, original manifest/robots hashes, its minimal reproducer, deciding contract sentence, and argument. SHA-256 `ae060fc63cafc6b8b45dba3060370d3bcba22b5c5905a5d83e82d37108f5ef33`.
`E/minimal-index.json:1-104` is the authoritative five-reproducer index; SHA-256 `8799c858b276bcf23332cf2a4c896930ee77c5146ee21696943671ae4f786e73`.
Minimal manifest template: `{"version":1,"checks":[{"id":"c","robotsStatus":200,"userAgent":"K","robots":"robots.txt","url":"http://x/","expect":"allow"}]}`. Apply row URL/expect; write row bytes as robots.txt (UTF-8, no final newline). All outputs have version 1, checksEvaluated 1, finding check `c`.
| Reproducer under E/minimal/ | Original checks | robots.txt bytes (escaped newlines) | URL / expect | L and I output | R output |
|---|---:|---|---|---|---|
| a32254d23df8669a | 47 | `user-agent:K\ndisallow:/` | `http://x/` / allow | exit 0, clean, [] | exit 1, failed-policy, blocked |
| 70a90a85d472c6e3 | 50 | same | `http://x/` / disallow | exit 1, failed-policy, exposed | exit 0, clean, [] |
| bd89efa5cda3e021 | 1 | `user-agent:*\ndisallow:/\nuser-agent:K` | `http://x/` / disallow | exit 0, clean, [] | exit 1, failed-policy, exposed |
| 3622d113d57d691f | 44 | `user-agent:*\ndisallow:/` | `http://x/robots%2Etxt` / allow | exit 1, failed-policy, blocked | exit 0, clean, [] |
| 13060840e653f4c0 | 32 | same | `http://x/robots%2Etxt` / disallow | exit 0, clean, [] | exit 1, failed-policy, exposed |
These preserve the original three-tool output vectors; every surviving robots byte is necessary under single-byte deletion. Each directory contains manifest.json, robots.txt, and outputs.json with exact commands/results.
Replay any row: use the prefix above, then `timeout --kill-after=1s 20s python3 -B <tool> --manifest "$E/minimal/<id>/manifest.json"`; choose each of the three paths read above under C. Exit codes are in the table and each outputs.json.

### Finding 1 — reference ASCII matching is wrong (98 checks)
Deciding sentence, `C/SCORECARD.md:1827-1830`: a group matches when its name equals the check token “compared ASCII case-insensitively”; absent a match, combine every `*` group, otherwise allow.
U+212A KELVIN SIGN `K` is not ASCII K. Thus the first two rows must ALLOW (no matching/star group); the third must DISALLOW (the star group applies). L/I implement this correctly. R uses Unicode `.lower()` at `C/.ufo/waves/round-37/sealed/reference/ref.py:76-77`, falsely matching K to K and, in the third row, suppressing fallback even though the false match has no rules.
Verdict: R's asserted contract-grounded behavior is **wrong** on this family; L/I **hold** on these checks. Evidence: first representative `outputs.json:13-21,57-69`; fallback representative `outputs.json:13-21,57-69`.

### Finding 2 — implicit allow ordering is not a unique oracle (76 checks)
Deciding text, `C/SCORECARD.md:1838-1844`: path-to-match is constructed first; “The path `/robots.txt` is always allowed”; “Before comparison both the rule value and the path are normalized”. It never explicitly orders exemption versus normalization.
L/I explicitly document raw-path exemption (`C/scripts/robots_audit.py:44-47`; independent file:9-11). Under that reading the encoded spelling is not exempt, `disallow:/` matches, and DISALLOW is correct. R normalizes first (`ref.py:135-138`), yielding `/robots.txt` and ALLOW. The clause order favors the documented raw reading, but does not uniquely settle the other reading.
Verdict: agreement with a uniquely specified oracle is **overstated**; unique frozen-contract answer is **unverifiable**, not a proved landed-tool defect. Under the documented L/I lane reading, their outputs **hold**. Both expectation directions and exact outputs are retained in the last two rows.

## One mutation probe and exact restoration
Mutant: scratch `C/scripts/robots_audit.py:308`, equal-length allow tie assignment changed from `decision = "allow"` to `decision = "disallow"`; no other behavior point mutated.
Detector fixture: `user-agent: *\ndisallow: /x\nallow: /x\n`; status 200, Bot, `https://example.invalid/x`, expect allow. Contract `SCORECARD.md:1835-1837` requires allow to win, so all three must report clean, evaluated 1, [] and exit 0.
Same bounded detector, with the common prefix, on pristine/mutated/restored bytes:
- `timeout --kill-after=3s 60s python3 -B differential.py probe --label pristine` — exit 0; L/I/R clean, [] (all exit 0).
- `timeout --kill-after=3s 60s python3 -B differential.py probe --label mutated` — exit 1; L exit 1, failed-policy, `[{"check":"tie","reason":"blocked"}]`; I/R remain clean, [] (exit 0).
- `timeout --kill-after=3s 60s python3 -B differential.py probe --label restored` — exit 0; L/I/R clean, [] (all exit 0).
Verdict: **killed**, with passing baseline and restored run. Only the same line was changed back before restored evaluation.
Before/restored SHA-256: `5eb767ec68a649145102619ed13754428bef489e432ed50eb20e9e50542cabae`; mutant: `4a2807503f8f2a8fc4e0ce926ec14f2e108110fd5015ffc2a47ac302204fcf42`.
Restoration evidence: `E/mutation/pristine.json:3,10,23-31`, `mutated.json:3,10,23-35`, `restored.json:3,10,23-31`. Exact hashes match; no subsequent mutation/probe.

## Evidence and bounds
Generator `S/differential.py` SHA-256 `0143db80518da9239ecab0d8ae0d4dd4ae9f42a9c945960668dc45fa5a7b1716`; `E/inventory.json:7-52` records measured revision, all three source hashes and feature/status counts. `E/summary.json:1-105` and `E/reduction-summary.json:1-9` hold counts.
Hash command: `timeout 30s sha256sum differential.py evidence/disagreements-minimized.json evidence/minimal-index.json evidence/reduction-summary.json` — exit 0; hashes above. L/I equality on this generated corpus **holds**; universal correctness is not claimed. No round admission judgment; all started finite processes completed.
