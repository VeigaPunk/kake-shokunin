# Kake round 35 wave 1 — ScribeSkillRegistryRow

Routed defect 3 of the round-34 closure (`.ufo/waves/round-35` wave 1, milestone r35-build).
Landed base for every command and measurement: `318561efa67206699fdaf259ffb86e39f2d916a8`.
Deliverable: `/fast/scratch/hyaku/kake-r35/w1/ScribeSkillRegistryRow/registry.md` (draft only; the
lane's `SKILL.md` was not edited — a leaf seat does not write tracked lane files).

## What was built

A `### Link-preview audit gate registry — round 35` section with the exact eight-column precedent
header (Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof |
Write scope | Owner) and one `link-preview-audit` row, placed after `SKILL.md:721` and matching
`canonical-audit` at `:411` and `base-path-audit` at `:725`. The row records exits 0/1/2/64 with
reason names, the self-test command and its three exit codes, the round-34 frozen matrix proof,
the round-35 sealed counter, `none` write scope, owner `kake`.

Every command in the row exists at `318561ef` except the sealed counter's `--key-revision`, which
the row names as round-35 pending (no reveal commit has landed). The three round-35 C1 contract
repairs (SCORECARD at `81d9fd74`, bullets a–c) are marked as declared and not yet landed, because
two of them are measurably absent at `318561ef` and the third is still the old behavior.

## Observed state of the contract at `318561ef` (the finding that shapes the row)

Tool sha256 `cccc3a17256aa4387a57e55b039257f8b3a3d0a9f34dd925f62f4c73bd33a4db` — the same digest
the round-34 matrix receipt measured at `76fac3b`, so the round-34 pinned proof still addresses the
landed tool.

- (a) `og_url_multiple`: absent. `grep -c 'og_url_multiple'` on the tool returns 0.
- (b) template/svg/math exclusion: absent. The tool's docstring discloses it ("a canonical link …
  inside `<template>` or `<svg>`" counts).
- (c) unreadable-page isolation: absent. The tool collects `page_unreadable` and then returns
  `could-not-evaluate` with `pagesChecked` 0, discarding the readable pages' policy findings.
- The reason name `page_unreadable` itself already exists, so the row lists it in the exit-2 set
  without presenting it as a round-35 addition.

Sandbox probes (own files under `…/ScribeSkillRegistryRow/probe/`, no lane or sealed input):
- manifest with one non-UTF-8 page plus three readable pages → exit 2,
  `{"findings":[{"reason":"page_unreadable",…}],"pagesChecked":0,"verdict":"could-not-evaluate"}`.
- two pages: one with two `og:url`, one with `og:image` only inside `<template>` → exit 0, `clean`,
  `pagesChecked` 2.

## Commands run (sandbox clone at `318561ef`, `TMPDIR=/fast/scratch/hyaku/kake-r35/w1/ScribeSkillRegistryRow/tmp`)

| command | exit | observed |
|---|---|---|
| `git clone -q …/kake-shokunin …/ScribeSkillRegistryRow/clone` then `git checkout -q 318561ef…` | 0 | `HEAD` = `318561efa67206699fdaf259ffb86e39f2d916a8` |
| `timeout 120 python3 -B scripts/link_preview_selftest.py` | 0 | `cases 35, failed 0, passed 35, passedOverTotal "35/35", verdict clean` |
| `timeout 180 python3 -B .ufo/waves/round-34/c1_matrix_count.py --root . --revision 318561ef…` | 0 | `C1 28/28`, `constantGatesAllRejected true`, `matrixSha256 246a6a3b…`, `toolSha256 cccc3a17…` |
| `python3 -B scripts/link_preview_audit.py --manifest …/probe/manifest.json` | 2 | round-35 (c) delta, as above |
| `python3 -B scripts/link_preview_audit.py --manifest …/probe/m2.json` | 0 | round-35 (a)/(b) absence, as above |

Read, not rerun: `.ufo/waves/round-34/verification/c1-at-76fac3b.json` (28/28, byKind
defect 13/13, input 7/7, usage 2/2, control 6/6), `.ufo/waves/round-34/verification/selftest-link-preview-at-76fac3b.txt`
(passed 35, exit 0), `.ufo/waves/round-35/verification/control-c1-declaration.json` (base 14/24,
target 22), `control-c1-constant-clean.json` (7/24), `control-c1-lookup-dcef39b5.json` (7/24).

## Gates and bounds

- No subagent, no second judge, no admission stated. Lane `jj`/git untouched; no mutating git
  command in the lane; nothing written in the lane except this report.
- Sealed keys under `/fast/scratch/hyaku/kake-r35/sealed/` were not read, listed, stat'ed, copied
  or grepped; the sealed counter was not executed (its `--key-revision` is pending).
- No network request of any kind; no owned property touched. No tool installed or updated.

## Out of scope / not verified

- The row is a draft for the L1: nothing was inserted into `SKILL.md`, and no round-35 tool repair
  or C1 build was attempted (other seats own those).
- The closed items `KakeR31.CriticC1Counter` and `KakeR31.CriticSandboxThreatModel` were not
  approached; this seat's item does not drift there.
- I did not verify that the sealed counter scores any commit; only its public invocation and its
  exit-2 guard text were read.

## Evidence pointers

- Draft: `/fast/scratch/hyaku/kake-r35/w1/ScribeSkillRegistryRow/registry.md`
- Probes: `/fast/scratch/hyaku/kake-r35/w1/ScribeSkillRegistryRow/probe/{manifest.json,m2.json,pages/}`
- Precedents: `SKILL.md:411`, `SKILL.md:721`, `SKILL.md:725`; PROTOCOL §Gate standard
  (Registry and Delivery) at `PROTOCOL.md:388-437`.
- Defect source: `corpus/lessons/round-34-verifier-spotcheck.md`, routed defects item 3.
