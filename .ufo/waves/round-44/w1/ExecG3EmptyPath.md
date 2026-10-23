# Kake R44 W1 — ExecG3EmptyPath

## Axes
- **Operability (target):** added deterministic G3 cases for empty URL paths and the `buildscope-m5-empty-path.py` behavior.
- **Freshness:** unchanged; this item does not alter ledger or publishing freshness data.

## Implementation
Wrote `.ufo/waves/round-44/classes/g3_empty_path.py`. It emits 120 `value`/`loc` units whose clean values have no path, plus 61 `prefixpair` units: one exact no-port witness and 60 valid-port forms. Each pair uses `https://<host>[/][:<port>]` as its first value and the same authority with no path as its second. `layout_f` derives the sitemap URL from the root-path first value, giving `https://<host>/sitemap.xml` (or its ported equivalent); the empty-path second value is therefore in scope under round 41's `/` normalization but out of scope under the control's empty-path behavior. Total: 181 units, 242 URL values.

The initial probe iteration put ported pathless values in single-value units; the frozen layout then generated invalid sitemap URLs for those cases. I revised those forms into root/pathless pairs. A second iteration witnessed; I added the no-port pair as well so the requested `https://<host>` witness shape is explicit. Only the final iteration below is acceptance evidence.

## Commands and evidence
Scratch setup command: `mkdir -p /fast/scratch/hyaku/kake-r44/ExecG3EmptyPath` (no output).

The following exact commands were run once for each of the three class revisions (six probe invocations total); `TMPDIR` kept probe temporaries in the assigned scratch directory:

```sh
TMPDIR=/fast/scratch/hyaku/kake-r44/ExecG3EmptyPath python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G3 --tool-file .ufo/waves/round-44/controls-r43/buildscope-m5-empty-path.py --seed 44
TMPDIR=/fast/scratch/hyaku/kake-r44/ExecG3EmptyPath python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G3 --tool-file .ufo/waves/round-44/controls-r43/buildscope-m5-empty-path.py --seed 211
```

Final revision — verbatim decisive JSON fields; each probe process exited **1** (witness):

```json
{"probe":"G3","seed":44,"units":181,"values":242,"ref41Exit":1,"candExit":1,"ref41OutSha256":"1d156de9c0f0f01aaa485dd3f38d008cd20ccbb635e7dc399946605eae2a4591","candOutSha256":"0170d327d565a5e93ab8fa405c53df84406c3f15b804565fa0fcd0786d8433b9","equal":false}
{"probe":"G3","seed":211,"units":181,"values":242,"ref41Exit":1,"candExit":1,"ref41OutSha256":"8040c30f53417ad187c9ce6d80f3411ec350c8948db327ffd192e0c935590fc9","candOutSha256":"f6f39641585cacd6ac9357062ef4724deffebd392ff8b1260ecbd0f8771f0715","equal":false}
```

Superseded iteration evidence (same commands; decisive fields copied from probe JSON):

- First draft, seed 44: `units=121`, `values=122`, `ref41Exit=2`, `candExit=2`, `ref41OutSha256=a7b3601ea3a891c44896b24c28e46f4850e9f5522b90091ca0eaee684ede622f`, `candOutSha256=1dd1d224d874f6e3b3f9c42fe949c01bd596d4445bcf437cda7a5accb7a52e1e`, `equal=false` (tail contained `check_invalid`). Seed 211: same counts/exits, `ref41OutSha256=bb64debeac4ad60b47ff2b9606a363f5cdf880633fb2497e23f5038276e17335`, `candOutSha256=757f636d870f2845b32e47f975eec2a6b5147e83ac0334411539e9fe63b6825b`, `equal=false` (tail contained `check_invalid`).
- Revised port-pair iteration, seed 44: `units=180`, `values=240`, `ref41Exit=1`, `candExit=1`, `ref41OutSha256=290dbb4e953725afb9b343ed477cea8edef0a0f0c1ca0302699df6ddccda1dc5`, `candOutSha256=553714a1a2f4e86256c58f77b4758286e64f9e14ac65c36c8fd9129698226c65`, `equal=false`. Seed 211: same counts/exits, `ref41OutSha256=21d1c5b08bd2f22acabbdc38882161e6de291795087138a98db122ff41cd24a0`, `candOutSha256=2ef0ed67829c11d76c4d79bd667ee5381a531f361760d44e4ad3f70ee58bf006`, `equal=false`.

No counter-wide run, build, lint, formatter, or other tests were run. No tools were installed. LSP was unavailable through the provided tool interface; source patterns and the frozen layout/control were inspected read-only. Blockers: none.

## Files written
- `.ufo/waves/round-44/classes/g3_empty_path.py`
- `.ufo/waves/round-44/w1/ExecG3EmptyPath.md`
