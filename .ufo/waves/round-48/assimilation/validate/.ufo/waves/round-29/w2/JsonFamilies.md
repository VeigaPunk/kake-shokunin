# Round 29 wave 2 — JsonFamilies (operability, falsify)

**Item attacked.** C2 tool `scripts/base_path_audit.py` at lane commit `7697990cbca20291f3b0367b8ff4220e93b38b03`: the round-27/28 open JSON and CLI families, probed with the 13 required refusal cases (duplicate JSON keys, NaN/Infinity, nesting depth 65 and 100000, version `true`, version `1.0`, extra keys, `pages` not a list, duplicate page file, duplicate page url, repeated `--manifest`, `--manifest=` empty, abbreviated `--man`).

**Bytes and method.** Sandbox clone `/fast/scratch/hyaku/kake-r29/w2/JsonFamilies/clone` at `7697990`; `scripts/base_path_audit.py` sha256 `e32646159b652710be4053bbdb001c3d11929ef63b055b7f57545231ac6965aa` (same before and after). `probe.py` runs the tool as a subprocess in a per-probe directory that also holds a real `index.html`, so a wrongly accepted manifest shows as exit 0 clean rather than as a page-read error; the same committed module is imported in-process to attribute each refusal to the layer that raised it. Commands (all exit 0): `python3 -B probe.py clone/scripts/base_path_audit.py work/pristine pristine.json`; `python3 -B clone/scripts/base_path_selftest.py --tool <mutant>`; `python3 -B clone/.ufo/waves/round-29/c2_matrix_count.py --root clone --revision <commit>`.

## Probe table (committed bytes)

| probe | exit | reason seen by the operator | refusal site |
|---|---|---|---|
| duplicate JSON key, top level | 2 | `input_invalid` | scripts/base_path_audit.py:208 |
| duplicate JSON key, inside a page | 2 | `input_invalid` | scripts/base_path_audit.py:208 |
| `NaN` | 2 | `input_invalid` | scripts/base_path_audit.py:213 |
| `Infinity` | 2 | `input_invalid` | scripts/base_path_audit.py:213 |
| `-Infinity` | 2 | `input_invalid` | scripts/base_path_audit.py:213 |
| nesting depth 65 | 2 | `input_invalid` | scripts/base_path_audit.py:200 |
| nesting depth 100000 | 2 | `input_invalid` | scripts/base_path_audit.py:200 |
| version `true` | 2 | `input_invalid` | scripts/base_path_audit.py:616 |
| version `1.0` | 2 | `input_invalid` | scripts/base_path_audit.py:616 |
| extra top-level key | 2 | `input_invalid` | scripts/base_path_audit.py:611 |
| extra key inside a page | 2 | `input_invalid` | scripts/base_path_audit.py:626 |
| `pages` is an object | 2 | `input_invalid` | scripts/base_path_audit.py:622 |
| `pages` is a string | 2 | `input_invalid` | scripts/base_path_audit.py:622 |
| duplicate page file | 2 | `input_invalid` | scripts/base_path_audit.py:634 |
| duplicate page url | 2 | `input_invalid` | scripts/base_path_audit.py:634 |
| repeated `--manifest` | 64 | usage, stderr `--manifest may be given only once` | scripts/base_path_audit.py:120 |
| `--manifest=` (empty value) | 2 | `input_invalid` | scripts/base_path_audit.py:256 |
| abbreviated `--man` | 64 | usage, stderr `unrecognized arguments: --man ...` | scripts/base_path_audit.py:160 |

Controls in the same pass: depth 64 is refused by the schema (`:626`), not by the depth limit, so the limit boundary is 65; 100000 brackets inside a JSON string reach the schema layer (`:618`), so the depth scan counts brackets outside strings only; version `"1"` → `:616`; `--manif`, `--man=VALUE`, `--base-path` and `--manifest` without a value → 64.

**Verdict on the attacked item: holds.** All 13 required probes are refused with exit 2 or 64, each by a distinct deliberate check. Exit 2 prints one JSON object with verdict `could-not-evaluate` and reason `input_invalid` (scripts/base_path_audit.py:66, 597-606); exit 64 prints usage text on stderr and the usage JSON on stdout (:94-99, 747-749).

## Coverage finding: the committed detectors do not pin these families

Seven behaviour-bearing mutants of the committed tool (one refusal point each, separate copies; the committed file was never edited) were run against both committed detectors. Every mutant flips at least one probe above; every mutant survives both detectors:

| mutant | probe it flips | committed selftest | declared C2 counter |
|---|---|---|---|
| M1 `allow_abbrev=True` (:160) | `--man` 64 → 0 clean | 30/30, exit 0 | 30/30, exit 0 |
| M2 drop `SingleManifestAction` (:163) | repeated `--manifest` 64 → 0 clean | 30/30, exit 0 | 30/30, exit 0 |
| M3 duplicate members last-value-wins (:208) | duplicate key 2 → 0 clean | 30/30, exit 0 | 30/30, exit 0 |
| M4 drop the version type test (:615) | version `true`/`1.0` 2 → 0 clean | 30/30, exit 0 | 30/30, exit 0 |
| M5 unknown top-level members allowed (:610) | extra key 2 → 0 clean | 30/30, exit 0 | 30/30, exit 0 |
| M5b unknown page members allowed (:625) | extra page key 2 → 0 clean | 30/30, exit 0 | 30/30, exit 0 |
| M6 nesting limit raised to 1000000 (:58) | depth 65/100000: refusing layer only | 30/30, exit 0 | 30/30, exit 0 |

The 30 committed cases (`.ufo/waves/round-29/c2-matrix.json`; kinds control 7, defect 14, input 8, usage 1) hold no duplicate-key, non-finite, depth, bool/float-version, extra-key, non-list-pages, duplicate-page, repeated-option, empty-value or abbreviation case. Coverage finding, not a tool defect: the C2 claim of 30/30 with rejected constant gates is true as stated and stays true for seven broken tools.

**Limits to state.** (1) Reason granularity: every input refusal prints the same `input_invalid` reason and the refusing layer appears nowhere in stdout or stderr, so an operator cannot tell a depth refusal from a schema refusal; the layer column above comes from in-process attribution of the committed module. (2) The nesting limit is not observable at the CLI: a schema-valid manifest nests at most three levels, so depth 64, 65 and 100000 all end as exit 2 with the same reason. The explicit 64-level text scan (:58, :197-200) is stack-independent, unlike the older tool whose depth limit depended on the CPython stack (`corpus/lessons/round-28.md:113-115`); under M6 the depth-100000 case falls back to the native `RecursionError` path (:217-218) and still exits 2. (3) Empty `--manifest` value: refused, but as an input error (exit 2, `input_invalid`, :256) rather than usage (64) like the other CLI-shape errors. (4) I measured refusal completeness only, not whether a clean manifest is audited correctly beyond the two reference kinds in the committed matrix.

**Not verified.** No network access and no live web property was touched. No fixture, tool or matrix file was added or changed in the lane; I wrote only this report. The round-27/28 tools were not re-run, and the 30-case matrix was not re-derived at any other revision. No package was installed (none needed; Python 3.14.8 already present).

**Restoration evidence.** `sha256sum clone/scripts/base_path_audit.py` = `e32646159b652710be4053bbdb001c3d11929ef63b055b7f57545231ac6965aa`; `git -C clone status --porcelain` empty; `git -C clone rev-parse HEAD` = `7697990cbca20291f3b0367b8ff4220e93b38b03`; the seven mutant branches existed only inside the sandbox clone and were deleted. Note: the lane working tree also shows modifications to `SKILL.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/pages-base-path.md` and `scripts/base_path_audit.py`; those are sibling seats' working-tree changes, not mine.
