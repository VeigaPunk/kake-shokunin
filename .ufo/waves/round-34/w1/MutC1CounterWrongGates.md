# C1 counter mutation probe

Lane axes: operability and freshness; this probe targets operability only. Scope: one isolated rule-breaking variant.

| Variant | Rule broken | Score | Case(s) catching it | Verdict |
|---|---|---:|---|---|
| `name-as-property` (`attrs.get("property")` changed to `attrs.get("property", attrs.get("name"))`) | `name="og:image"` must not count as `property="og:image"` | 27/28 | `D7-name-attribute-not-property` (expected exit 1; mutant exit 0) | Killed |

The scratch baseline was a minimal stdlib-only auditor at `/fast/scratch/hyaku/kake-r34/w1/MutC1CounterWrongGates/clone/scripts/link_preview_audit.py`; baseline detector result was **28/28**. Mutant receipt reports control 6/6, defect 12/13, input 7/7, usage 2/2 and all four constant gates rejected. The mutant's sole failure was D7. Restored bytes produced **28/28** with the same per-kind scores as baseline.

Commands and outputs (all paths/code remain in the isolated scratch clone):

- `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; mkdir -p /fast/scratch/hyaku/kake-r34/w1/MutC1CounterWrongGates/tmp && export TMPDIR=/fast/scratch/hyaku/kake-r34/w1/MutC1CounterWrongGates/tmp && git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r34/w1/MutC1CounterWrongGates/clone && git -C /fast/scratch/hyaku/kake-r34/w1/MutC1CounterWrongGates/clone checkout -q a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f && printf 'clone=%s\nrevision=' /fast/scratch/hyaku/kake-r34/w1/MutC1CounterWrongGates/clone && git -C /fast/scratch/hyaku/kake-r34/w1/MutC1CounterWrongGates/clone rev-parse HEAD` — exit 0; revision `a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f`.
- Baseline commit: `git add scripts/link_preview_audit.py && git -c user.name='Mutation Probe' -c user.email='mutation-probe@localhost' commit -q -m 'scratch: add correct link preview auditor' && git rev-parse HEAD` — exit 0; `ade2257cfa26e6c02b5d04a77cd3b5aa92333b10`.
- `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-34/c1_matrix_count.py --root /fast/scratch/hyaku/kake-r34/w1/MutC1CounterWrongGates/clone --revision ade2257cfa26e6c02b5d04a77cd3b5aa92333b10 > /fast/scratch/hyaku/kake-r34/w1/MutC1CounterWrongGates/baseline.json` — exit 0; stderr `C1 28/28 at ade2257cfa26e6c02b5d04a77cd3b5aa92333b10`.
- Mutant commit: `git add scripts/link_preview_audit.py && git -c user.name='Mutation Probe' -c user.email='mutation-probe@localhost' commit -q -m 'scratch mutant: count name as property' && git rev-parse HEAD` — exit 0; `d33e6089c1f18d075897b827ce86102316ce4ccc`.
- `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-34/c1_matrix_count.py --root /fast/scratch/hyaku/kake-r34/w1/MutC1CounterWrongGates/clone --revision d33e6089c1f18d075897b827ce86102316ce4ccc > /fast/scratch/hyaku/kake-r34/w1/MutC1CounterWrongGates/mutant.json` — exit 1; stderr `C1 27/28 at d33e6089c1f18d075897b827ce86102316ce4ccc`.
- Restore commit: `git add scripts/link_preview_audit.py && git -c user.name='Mutation Probe' -c user.email='mutation-probe@localhost' commit -q -m 'scratch: restore correct link preview auditor' && git rev-parse HEAD` — exit 0; `2ad255ba8dce32263bce910eb77204a40f682529`.
- `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-34/c1_matrix_count.py --root /fast/scratch/hyaku/kake-r34/w1/MutC1CounterWrongGates/clone --revision 2ad255ba8dce32263bce910eb77204a40f682529 > /fast/scratch/hyaku/kake-r34/w1/MutC1CounterWrongGates/restored.json` — exit 0; stderr `C1 28/28 at 2ad255ba8dce32263bce910eb77204a40f682529`.

Restoration evidence: baseline SHA-256 `db088fabd5dceaec9176fcb31af064d9a55186ba70a463ed9219ff43752690e8`; mutated SHA-256 `667c64aaff40eef99607c03d0d72cf44069fecc9ba684a091b9d41bd082ad46e`; restored SHA-256 `db088fabd5dceaec9176fcb31af064d9a55186ba70a463ed9219ff43752690e` (byte-identical to baseline). Receipts: `baseline.json`, `mutant.json`, `restored.json` under the scratch directory above. Contract evidence: `c1-matrix.json:9-12,228-245`; frozen detector logic: `c1_matrix_count.py:8-18,162-180`. No tools installed; no checks other than this counter run.
