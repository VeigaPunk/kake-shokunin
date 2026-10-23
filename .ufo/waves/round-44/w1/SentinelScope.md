# Wave 1 scope and safety review

**Axes:** operability (write/process boundaries) and freshness (receipt integrity). **Severity:** High for the unisolated class-module execution path; Medium for the audit/probe output-path controls and the contradictory `c44_audit.py` instructions; Low for optional tool-install writes. Static review only: no shell commands, probes, audit runs, network calls, or mutations were performed by this seat.

## Evidence inspected

- `.ufo/waves/round-44/make_w1_spec.py:26-59, 76-136, 138-227, 229-286` and `w1-spec.json` (`.items|length` returned `35`; the advertised 36 seats therefore include the L1/coordinator or the item count needs correction).
- `c44_count_v5.py:92-96, 136-159, 920-978, 1037-1067`; `c44_probe.py:39-100`; `c44_audit.py:61-80, 92-107, 120-158`.
- `verification/` directory read: only `freeze/` exists there now; `freeze/` contains `control-v4blind.json` and `tools/` receipts. The prescribed `verification/smoke-v4.json` and `verification/tools/` are not present in the listing.
- Credential-pattern scan of `make_w1_spec.py` and `w1-spec.json`: no matches. This is evidence about prompt text, not a runtime-secret scan.

The shared prompt's relevant exact bounds are: **“Only the L1 commits. You never run git commit/jj/git push, never edit the fleet repo /home/vgpnk/Projects/shokunin, never edit a sibling lane, never touch `.ufo/state/` or the fleet `.ufo/watchdog.log`.”**; **“Files you may write: the one lane path your item names, plus your scratch dir and your report. Nothing else.”**; scratch is `/fast/scratch/hyaku/kake-r44/<YourSeatName>/`; reports are `.ufo/waves/round-44/w1/<YourSeatName>.md`.

## Matrix

Every row also has its own report path `.ufo/waves/round-44/w1/<Item>.md` and may use `/fast/scratch/hyaku/kake-r44/<Item>/**`. “None” means no additional, expressly assigned lane path. Tool-generated temporary files and the tool-install exception are described below.

| Item | Additional item-specific writable paths | Verdict |
|---|---|---|
| ExecG1LongPort | `.ufo/waves/round-44/classes/g1_longport_grammar.py` | Explicit class target; within the one-path rule. |
| ExecG2DefaultPort | `.ufo/waves/round-44/classes/g2_default_port.py` | Explicit class target; within the one-path rule. |
| ExecG3EmptyPath | `.ufo/waves/round-44/classes/g3_empty_path.py` | Explicit class target; within the one-path rule. |
| ExecG4PortScope | `.ufo/waves/round-44/classes/g4_port_scope.py` | Explicit class target; within the one-path rule. |
| ExecG5Prefix | `.ufo/waves/round-44/classes/g5_prefix_cut_45plus.py` | Explicit class target; within the one-path rule. |
| ExecG6Fold | `.ufo/waves/round-44/classes/g6_fold_pairs.py` | Explicit class target; within the one-path rule. |
| ExecG7Bands | `.ufo/waves/round-44/classes/g7_band_memos.py` | Explicit class target; within the one-path rule. |
| ExecG8Hosts | `.ufo/waves/round-44/classes/g8_host_tables.py` | Explicit class target; within the one-path rule. |
| ExecG9PortDigits | `.ufo/waves/round-44/classes/g9_port_digits.py` | Explicit class target; within the one-path rule. |
| ExecG10Windows | `.ufo/waves/round-44/classes/g10_headtail_windows.py` | Explicit class target; within the one-path rule. |
| ExecLedgerCheck | `scripts/ledger_latest_check.py`; `.ufo/waves/round-44/ledger-quotes.json`; `.ufo/waves/round-44/verification/ledger-before.txt`; a `.exit` companion (its exact filename is not specified) | Explicitly instructed. The companion filename needs to be fixed. |
| ExecAudit | `.ufo/waves/round-44/c44_audit.py`; `.ufo/waves/round-44/verification/smoke-v4.json`; audit-created `.ufo/waves/round-44/verification/tools/<control-name>.json` | **Conflict:** the common prompt lists `c44_audit.py` under “Frozen artifacts you must not edit,” while this item says “Harden” it and directs changing its criterion. The smoke and tools receipts are intended new outputs. Resolve the ownership/freeze contradiction before execution. |
| ScoutPortFamily | None | Its prompt says not to write under the lane except its report. |
| ScoutFoldFamily | None | Same read-only lane bound. |
| ScoutBandFamily | None | Same read-only lane bound. |
| ScoutHostFamily | None | Same read-only lane bound. |
| ScoutWindowFamily | None | Same read-only lane bound. |
| ScoutBuildMutants | None | Same read-only lane bound. |
| ScoutRegistry | None | Report only. |
| ScoutRef41Semantics | None | Manifests and tool copies go in its scratch directory. |
| ReviewCounterContract | None | Checks are read-only; report only. |
| ReviewAuditDriver | None | Scratch audit copy/TSV/output are required in scratch; no real driver edit. |
| ReviewInheritedLineage | None | Read-only checks; report only. |
| ReviewLedgerCheck | None | It explicitly says not to edit the checker; report only. |
| CriticClaimC1 | None | Report only. |
| CriticClaimC2 | None | Report only. |
| ConnectorSibling | None | Sibling lanes are expressly read-only; report only. |
| SentinelScope | None | This report only. |
| RevengerControls | None | Report only. |
| MutationTesterAudit | None | Mutated audit copies, TSV, and audit outputs belong in scratch; no real driver edit. |
| LabratKelvin | None | Hand-made fixture belongs in scratch; report only. |
| LabratScopeSmu | None | Hand-made fixture belongs in scratch; report only. |
| SimplifierInherited | None | It explicitly says not to delete anything; report only. |
| ScribeSources | `corpus/lessons/round-44.md` | Explicitly requested new lesson. It is a working-tree content change, not a commit; distinguish it from the L1-only Git-history rule. |
| CriticMathDenominator | None | It explicitly says not to edit anything; report only. |

**Common extra write surfaces:** the prompt also says **“Tool installs are authorized for any tool that helps (official channels only; record tool/version/channel/reason in your report) ... use `uv tool`, `npx`, or an official binary into `~/.local/bin`.”** A seat choosing to install may therefore write under `~/.local/bin/` or package-manager-managed directories outside its scratch/report/item paths; no item requires an install. The counter/probe also create transient files under Python's `tempfile.gettempdir()` (not pinned by the prompt to the per-seat scratch path). The probe normally removes its temp tree; the counter uses a `TemporaryDirectory` for normal runs.

## Named gaps and findings

### 1. High — class modules execute outside the sandbox

**Prompt text:** “The counter calls `cases(rng, h)` and expects `(units, n)” and **“Deterministic from `rng` only; no I/O, no network, no environment reads, no imports of the control tools. Standard library only.”** The latter is a behavioral prohibition, not isolation. The item says to write Python class modules and then run them with the probe.

**Evidence / path:** `c44_count_v5.py:136-152` imports each class with `exec_module`; main calls `load_classes(root)` at line 1046 and calls `classes[key].cases(...)` at 1064 before `box.run`. The probe loads the module at `c44_probe.py:58` and calls `cases` at line 77 before creating/running the sandbox at lines 79-81. `bwrap` and its `--unshare-all`, `--clearenv`, and read-only case bind occur only inside `Sandbox.run` (`c44_count_v5.py:944-955`).

**Exploit path / impact:** a malicious or accidentally side-effecting module can execute ordinary Python at import or in `cases` with the seat process's filesystem, environment, network, and subprocess access. It can bypass the `git commit`/fleet/sibling/`.ufo/state` prohibitions, read ambient credentials, send network traffic, start processes, or write outside scratch before the candidate-tool sandbox is entered. No such code was run. The prompt does not authorize those actions; this is an enforcement gap, not a compliant action.

**Smallest remediation:** run module import and `cases` in a constrained subprocess/container with cleared environment, network disabled, read-only repository inputs, and one dedicated writable scratch/temp output; validate a bounded serialized result before `layout_f` consumes it. Otherwise accept only a trusted, reviewed class artifact and do not execute seat-authored modules on a credential-bearing host.

### 2. Medium — generated input has no aggregate size/count quota

**Prompt text:** the class contract specifies `(units, n)` and deterministic generation, but does not set a hard maximum; shape guidance such as “about 100 pairs” is not a limit.

**Evidence / impact:** `layout_f` creates an XML file per value/pair and writes value strings into those files (`c44_count_v5.py:546-605`). There is no cap on returned unit count, `n`, per-value length, or total generated input bytes before this happens. The class code and layout run outside `_limits`. The counter's actual limits are `OUT_CAP = 256 * 1024 * 1024` and `AS_CAP = 4 * 1024 * 1024 * 1024` (`:95-96`), applied to the sandbox runner at `:920-922`; `RUN_TIMEOUT = 600` seconds per sandbox run (`:94`, `:957-961`). They cap the target process's output file size, address space, and one run's wall time—not class generation or temporary input disk usage. Thus a class can exhaust memory/disk before the capped subprocess starts; temp cleanup is not a quota.

**Can values escape via path traversal?** Not through the current layout: file names are random hex, while generated strings are inserted as XML content (`:552-605`); the case directory is read-only bound for tool runs (`:947`). This does not mitigate the unsandboxed Python-code path in gap 1.

**Smallest remediation:** enforce maxima for units, individual string length, total encoded XML/manifest bytes, and generation time before writing; apply a filesystem quota or bounded tmpfs to the case directory.

### 3. Medium — audit and probe outputs are not destination-confined

**Prompt text:** ExecAudit acceptance runs `c44_audit.py ... --out .ufo/waves/round-44/verification/smoke-v4.json`. No prompt sentence authorizes overwriting an existing evidence receipt; the shared bound instead limits writes to named paths.

**Evidence / exploit path:** `c44_audit.py` accepts arbitrary `--out`, creates `<outdir>/tools`, writes per-control files there (`:77-79, 92-98`), and opens the summary with mode `"w"` (`:156-158`); optional build outputs also use that directory (`:121-128`). Neither path nor pre-existence is checked. Choosing an existing receipt as `--out` can replace it; choosing its directory as `outdir` can replace `tools/<name>.json`. The current prescribed `verification/smoke-v4.json` path is not present in the inspected directory listing, and its default `verification/tools/` output would be new, so that prescribed invocation does not presently collide with the listed `verification/freeze/` receipts. The driver could nevertheless target `verification/freeze/control-v4blind.json` and the corresponding `freeze/tools/` files if given that output path. This is technical capability, not prompt-authorized scope.

`c44_probe.py` normally uses a temporary tree and removes it (`:68-100`), and its prescribed command omits `--keep`. But the CLI exposes `--keep DIR` (`:45`); `copytree(..., dirs_exist_ok=True)` and the subsequent `open(.../manifest.json, "w")` (`:90-95`) can merge into and overwrite a caller-selected destination. No prompt sentence tells seats to use `--keep` or authorizes a lane/evidence destination.

**Smallest remediation:** confine audit outputs to a new, dedicated, per-run directory under approved scratch or a fixed non-existing verification path; reject paths outside the allowed root and refuse existing files. Remove `--keep` or require a non-existing, canonical path inside the seat's scratch directory.

### 4. Medium — contradictory edit authority for `c44_audit.py`

**Exact conflicting sentences:** common context: **“`.ufo/waves/round-44/c44_audit.py` ... [is among] Frozen artifacts you must not edit”**; ExecAudit target/change: **“Harden ... `c44_audit.py`”** and **“Change the witnessed criterion...”**

**Impact:** ExecAudit cannot complete while honoring both clauses; the matrix therefore marks this path conflict rather than treating the item-specific target as silently overriding the freeze. **Smallest remediation:** have the L1 explicitly remove `c44_audit.py` from the frozen list or reassign the change to the L1, and state which version is authoritative before edits.

### 5. Low — tooling install exception exceeds the file allowlist

**Exact sentence:** **“Tool installs are authorized for any tool that helps ... use `uv tool`, `npx`, or an official binary into `~/.local/bin`.”** This expressly allows writes outside “the one lane path ... plus your scratch dir and your report.” No install is requested by an item. **Smallest remediation:** disallow installs for this wave or list the allowed package-manager destinations and their relationship to the per-seat write bound.

## Boundary verdicts

- **Git history / commit / push:** no item instructs or prompt-authorizes a leaf to run `git commit`, `jj`, or `git push`; the exact shared sentence forbids these, and the other listed Git commands (`show`, `log`, `rev-parse`) are reads. ScribeSources is explicitly allowed to write the new `corpus/lessons/round-44.md`, so lane content/history-as-documents does change in the working tree; only L1 is authorized to commit it. Gap 1 means this is not technically enforced against malicious class code.
- **Fleet, sibling lanes, `.ufo/state/`:** no compliant item has write permission there; shared bounds expressly prohibit them. ConnectorSibling and scout tasks are read-only. Gap 1 means code execution can bypass the prohibition.
- **Network / credentials:** no item directs a network request or embeds an apparent credential. Relevant direct commands are local Git/source reads and offline tool runs; the class contract explicitly forbids network and environment reads. Optional official-tool installation is the only explicit route that may use a network. No runtime network or secret access was tested. Gap 1 leaves the module import process with ambient access, so the prompt prohibition alone cannot guarantee no exfiltration.
- **Evidence receipts:** the prescribed audit output creates new `smoke-v4.json` and `verification/tools/*.json` at the current inspected state; it does not presently overwrite the listed freeze receipt. The audit and probe APIs can overwrite if given colliding destinations, as above; prompt instructions do not authorize that choice.

**Smallest overall change:** resolve the audit freeze conflict; run class modules and generator calls isolated with hard input quotas; and make audit/probe output paths canonical, confined, and non-overwriting. No files other than this report were written by this seat.