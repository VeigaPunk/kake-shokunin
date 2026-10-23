# ScribeSkillRegistry — round 36, wave 1

## Axes and behavior
- Axes: operability (judged) and freshness (lane-owned). Drafted the source-recheck registry row and six-line procedure in the sandbox artifact; no product implementation or SOURCES row was changed.
- The row records the eight precedent columns, exit map, self-test, write scope, owner, and frozen predicate. The procedure handles `moved`, `gone`, and `quote_missing`, preserving the SOURCES append-only correction rule.
- Build-state note: `scripts/source_snapshot.py`, `scripts/source_recheck.py`, and `scripts/source_recheck_selftest.py` were absent in the observed lane scripts tree; all their invocations are marked round-36 pending in the draft.

## Gates and commands
- Drafted only; no audit, self-test, or sealed counter command was executed. The declared frozen predicate is `met: passed >= 25 of 28 sealed cases` (counter v3); its gate status is unmeasured by this seat.
- Exact shell command: `timeout 300 mkdir -p /fast/scratch/hyaku/kake-r36w1/ScribeSkillRegistry /fast/scratch/hyaku/kake-r36w1/ScribeSkillRegistry/tmp && export TMPDIR=/fast/scratch/hyaku/kake-r36w1/ScribeSkillRegistry/tmp && printf 'sandbox=%s\nTMPDIR=%s\n' /fast/scratch/hyaku/kake-r36w1/ScribeSkillRegistry "$TMPDIR"` — exit 0; output named the sandbox and TMPDIR.
- Exact hash command: `timeout 300 sha256sum /fast/scratch/hyaku/kake-r36w1/ScribeSkillRegistry/registry.md /home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md /home/vgpnk/Projects/shokunin/kake-shokunin/SCORECARD.md /home/vgpnk/Projects/shokunin/PROTOCOL.md /home/vgpnk/Projects/shokunin/CORPUS.md /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-36/sealed_count.py; rc=$?; printf 'exit=%s\n' "$rc"; exit "$rc"` — exit 0. SHA-256 values are below.
- No tests/build/lint, network requests, Git/jj commands, tool installs, or accesses under `/fast/scratch/hyaku/kake-r36/` occurred. The public counter source was read, never run; no key/cases were accessed.

## Touched surfaces and provenance
- New sandbox artifact: `/fast/scratch/hyaku/kake-r36w1/ScribeSkillRegistry/registry.md:1-16`; SHA-256 `86aa9088bac1dbd3b2918e9ed3356405d8c003b0aba2c4a9d2e44eb47b019625`.
- Only lane file written: `.ufo/waves/round-36/w1/ScribeSkillRegistry.md` (this report). No tracked lane files were edited.
- Registry column precedent: `SKILL.md:721-725` and `SKILL.md:1043-1046`; SHA-256 `303fb1f4b74b3780daabedda91c3ef1775a9185ed31da66af29214427603e6d2`.
- Round-36 declared contract and verdict semantics: `SCORECARD.md:1562-1656` (base `b720d79976a1fb8fe6a8eb4b9f50e946b0cd5e07`); SHA-256 `07401885b17e124cf13aff87a92bb31056275f1bb940401f47d1eed46048f883`.
- Gate row schema: `/home/vgpnk/Projects/shokunin/PROTOCOL.md:375-419`; SHA-256 `886e459b2aa79b8198912ad54bd57fbb025cc424d78684a02fb3d4c832d4411a`.
- SOURCES append-only/change rules: `/home/vgpnk/Projects/shokunin/CORPUS.md:86-118`; SHA-256 `88556402940e7a0f1dbbed3abef9e00c87a90db6f80eaed03269e371f50050b8`.
- Public frozen counter constants: `.ufo/waves/round-36/sealed_count.py:60-66`; SHA-256 `88ec59140258ce759107b7472fdd07a005b7c1bb8b3ba5218347e4518342ff8e`.

## Findings and limits
- The contract makes non-permanent redirects non-`moved`; only 404/410 produce `gone`; unsupported charset and malformed input are could-not-evaluate. The draft maps those contract reasons into the registry verdict classes.
- `moved` correction is expressed as a superseding row, not an in-place URL edit, consistent with `CORPUS.md`; a `gone` status change is logged old→new.
- No conclusion is made about tool behavior, self-test success, sealed-case score, live source freshness, or round admission. No software was installed or updated.

## Artifact paths
- Draft: `/fast/scratch/hyaku/kake-r36w1/ScribeSkillRegistry/registry.md`
- Report: `.ufo/waves/round-36/w1/ScribeSkillRegistry.md`
