# ExecC2Tool — round 74 w1

## Deliverable

Artifact: `.ufo/waves/round-74/w1/ExecC2Tool/sidecar_reobserve.py` (intended production destination `scripts/sidecar_reobserve.py`, for L1 to apply). No production file edited.

Axes: freshness, observation-history fidelity, write confinement, deterministic output. Frozen C2 predicate unchanged.

## Behavior

- Stdlib-only; default `--check` reports without writing. `--write` requires calendar-valid `--date YYYY-MM-DD`. `--root` defaults to `.`, `--host` to `platform.system().lower() + '-' + platform.machine()`; supports `--json`, `--selftest`, `--work DIR`.
- Reads only the fixed sidecar under root. Entry `file` is citation text, never an existence-probe or output path. Tokens beginning `~/` expand using HOME; other relative tokens resolve under root. Uses `os.stat`, with FileNotFoundError/NotADirectoryError classified as absent, other OSError as unevaluable.
- Scans all entries before any rewrite. Unevaluable anywhere returns 2 with counts and leaves bytes untouched. Invalid schema/entry/history or invalid new-note vocabulary also refuses before writing.
- Only absent/present entries flip. Appends prior `{date, kind, note}` while retaining existing history; generates the exact requested note. Restored entries and genuinely absent entries remain unchanged. No rewrite when no flips exist.
- Rewrites via `json.dump(indent=2)` plus newline. Rejects sidecar symlinks and resolved paths outside root; writes only the fixed sidecar, not temporary siblings or entry paths.
- Text counts (code-derived, not exercised): `sidecar_reobserve mode=check entries=N absent=N restored=N present=N absent_present=N absent_absent=N restored_absent=N unevaluable=N flipped=0 wrote=false`. Counts describe the input observation; `flipped` and `wrote` describe the action. Completed observations exit 0 even if repair candidates exist; unevaluable/errors exit 2. This tool is not the C2 acceptance counter.
- Eight selftest fixtures included: flip, restored-present no-op, whole-write refusal on unevaluable, existing-history preservation, safe/unsafe note vocabulary, HOME expansion, check-byte preservation, schema refusal. Fixtures use `TemporaryDirectory(dir=work)`; when work is unspecified the stdlib honors TMPDIR. No hard-coded temporary-root literal.

## Retained evidence and commands

Read the frozen contract and controls directly. `controls/base-c2-sidecar.txt` records base entries=174, absent=148, restored=26, absent_present=144, absent_absent=4, contradictions=144. These are retained control observations, not a fresh tool result.

Committed input was obtained with:

```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show ced2878a1e77f57afb4ee3baebf1021e5130399b:corpus/knowledge/freshness-sidecar.json
```

Executed inside diagnostic shell pipelines; supervised exit notifications were 0. A captured scratch copy reported 103243 bytes, schema `kake-paths-sidecar-v1`, 174 entries, 148 absent/26 restored, no history arrays. Scratch capture was inspected through the read tool, then deleted. Initial diagnostic shell calls supplied `name` and returned service-like PID notices without stdout; reported this tool behavior via `xd://report_issue`. No diagnostic result is claimed as a repair-tool verification.

Scratch cleanup executed exactly:

```sh
rm -rf -- /fast/scratch/hyaku/kake-r74/ExecC2Tool
```

Exit 0. No scratch tree retained. No fixture git repo or git mutation occurred. No tools installed or updated.

## Verification / handoff

No build, lint, formatter, smoke check, or selftest run: editing-wave instructions reserve execution for L1/reviewer. L1 should run the artifact's `--selftest --work <exclusive scratch parent>` with TMPDIR explicitly assigned, run default check against a committed-base extraction, write that scratch sidecar with `--date 2026-11-03 --host linux-x86_64`, then run the C2 acceptance counter and sweep gates. These checks have NOT passed merely because fixtures are implemented.

LSP unavailable: this seat's mounted tool inventory exposes no LSP definition/reference/refactor interface. Implementation introduces a standalone artifact with no production callsite edits. Production docs are owned by the scribe; command surface was sent to ScribeKnowledge-2 and artifact availability to ReviewerC2-5.

## Risks / blockers

No implementation blocker. Runtime correctness remains unverified by this seat. The write uses direct truncation of the fixed sidecar, not atomic replacement (avoids writing another path); callers should retain the committed original before invoking write. Observation is host-local and can change after stat. An absence-vocabulary match anywhere in the exact generated note, including host class or citation text, refuses rather than emitting an invalid restored note.

Self-evaluation: accuracy 4 (implementation not executed), completeness 4 (all requested CLI/features and fixtures present; integration owned by L1), clarity 4 (ordered counts and explicit exit semantics), actionability 4 (ready artifact, pending gate execution), conciseness 4 (selftests dominate size). No acceptance or landing claim made.
