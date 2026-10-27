# ScoutCensusState — round-63 w1 census scout report

Seat: ScoutCensusState (leaf, no subagent dispatch). Date: 2026-10-27.
Scope: run the frozen manual census commands from
`/home/vgpnk/Projects/shokunin/CORPUS.md` §"SOURCES.md — where a shokunin
learns" (lines 133–148) against
`/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`; compare with
the round-start census recorded in `corpus/lessons/round-63.md` and
`corpus/lessons/round-62.md`; confirm no registry cell changed this round;
name the W04 count. All commands run read-only with cwd =
`/home/vgpnk/Projects/shokunin/kake-shokunin`. Frozen claim, counters and
receipts untouched; no installs needed; nothing written outside this report.

## Frozen manual census results (CORPUS.md:133–148 commands, verbatim)

All seven frozen commands were executed unmodified (relative path
`corpus/SOURCES.md` resolved from the kake-shokunin repo root):

1. **Row count** — `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → **171**
2. **Malformed rows** (NF≠13, must print 0) → **0**
3. **Tier histogram** → **A=148 B=6 C=17** (Σ = 171, matches row count)
4. **Status histogram** → **mined=141 queued=8 rejected=22** (Σ = 171)
5. **Duplicate ids** (must print nothing) → **nothing printed**
6. **Enum violations / tier inflation** (tier, status, kind, A+community; must
   print nothing) → **nothing printed**
7. **Mined used-by existence** (missing paths; must print nothing) →
   **nothing printed** — every `mined` row's used-by path exists

Every "must print 0 / nothing" guard held. The registry is well-formed and
fully mined-row-grounded as it stands.

## Comparison with recorded round-start census

- `kake-shokunin/corpus/lessons/round-63.md` "Sources census" section
  (round-start, recorded 2026-10-27 before any registry edit):
  "`scripts/sources-census.sh validate --root … kake` → 171 rows,
  16 W04 cross-scope duplicate-URL warnings, exit 0. No `corpus/SOURCES.md`
  row was added or changed this round."
- `kake-shokunin/corpus/lessons/round-62.md` "Sources census" section:
  identical figures — 171 rows, 16 W04, exit 0, and "No SOURCES row was
  added or changed".
- Measured now: **171 rows, 0 malformed, histograms as above** — matches both
  recorded censuses exactly. No drift between rounds 62→63 and none this
  round.

## Scripted census and W04 count

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate
--root /home/vgpnk/Projects/shokunin kake`

- Exit code: **0**; final line `ok
  /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`.
- **W04 count: 16** — cross-scope duplicate-URL warnings, one per row:
  S033, S088, S092, S098, S099, S102, S110, S111, S115, S116, S117, S127,
  S416, S417, S427, S433 (each a duplicate RFC/WHATWG/W3C/python-docs/Baidu-
  college/crawler-docs URL appearing in another scope's registry). Counted
  via `awk '$2=="W04"'` on the script output → 16. Matches the recorded
  round-start figure of 16 in both lessons files.

## No registry cell changed this round (byte-level evidence)

- `git diff --exit-code 13d4519818db28cd0aa912e49020659140d7b9fa
  05b0d7f4b4a23513390f7b92547e2b0f1fccb06f -- corpus/SOURCES.md` → exit 0:
  **byte-identical** between the round-62 base tip and the measured
  after-receipts commit.
- Working-tree file integrity: `sha256sum corpus/SOURCES.md` →
  `63af1594e2f8d0b499fbf2673424bf818cf93dd380232a8c8d546eef00f75ae2`, identical
  to `git show 05b0d7f4…:corpus/SOURCES.md | sha256sum`. The file I censused is
  exactly the measured-commit bytes.
- The two round-63 commits on top of base (`6d8c52a6` freeze contract /
  counter / quote tool, `05b0d7f4` fixture-binding note) touched neither
  `corpus/SOURCES.md` nor any registry row; S432 stays `mined` and unchanged,
  consistent with the round-63 gate's "No registry row added or changed; S432
  stays `mined`".

## Verdict

The corpus registry is intact and exactly as recorded at round start:
171 rows, well-formed (0 malformed, 0 duplicate ids, 0 enum/tier violations,
all mined used-by paths present), tier A=148/B=6/C=17, status
mined=141/queued=8/rejected=22, scripted census exit 0 with **W04 = 16**.
No registry cell changed between base `13d45198…` and measured
`05b0d7f4…`; round-62 and round-63 recorded censuses both match the live
state. Claim of registry stability: **confirmed**.

## Evidence index (absolute paths)

- Commands source: `/home/vgpnk/Projects/shokunin/CORPUS.md:133-148`
- Registry: `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`
  (sha256 `63af1594…5ae2`)
- Recorded censuses:
  `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-63.md`
  (Sources census section),
  `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-62.md`
  (Sources census section)
- Census tool: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`
  (unmodified, read-only use)
