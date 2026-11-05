# ExecReceipts — round 96 standing receipts (census, assimilation, freeze supersession)

Seat (copy) of the Report trailer `.ufo/waves/round-96/w1/ExecReceipts.md`;
kept inside the seat directory per the hard bounds.

## Deliverables (this directory)

| File | Content | Evidence |
|---|---|---|
| `census-before.txt` | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` full output + exit code + SOURCES row count | exit_code=0; W04 duplicate-URL warnings only; row_count=216 (grep rc=0); revision `049e8eca2f0fa5e981232eb4efe367357dce578c` (freeze commit) |
| `assimilation/reg-ids` | 216 ids from `LANE/corpus/SOURCES.md` (frozen 0-3-leading-space pipeline) | wc -l=216; delta vs round-95 committed `reg-ids` = +S479 only |
| `assimilation/staged-ids` | 129 ids from `$S/merge/kake/SOURCES.append.md` | wc -l=129; identical to round-95 committed |
| `assimilation/collisions` | `comm -12 reg-ids staged-ids` | wc -l=8: S312 S329 S367 S372 S373 S374 S390 S409; identical to round-95 committed |
| `freeze-supersession.md` | Round-95 freeze stale-digest evidence + draft supersession paragraph | `grep -n "04be4a7d\\|9eff04c5" .ufo/waves/round-95/freeze.md` rc=0 (lines 160/162); `git cat-file -e 4f443b3f^{commit}` rc=0; `git diff 43cdd9fc 4f443b3f --stat` shows the instrument blob paths byte-identical |
| `ExecReceipts.md` (this file) | Seat report | — |

## Verification

- Instrument digests first verified before attacking (sha256sum rc=0):
  `c96_selfassess.py a282da65…`, `c96_reval.py ec40aec1…` both match
  `controls/instrument-sha256.txt`. No mismatch → no finding, no repair.
- Frozen commands taken verbatim from the campaign addendum (round-91
  `assimilation/README.md`): `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'`
  pipeline into `reg-ids` / `staged-ids`, `comm -12` into `collisions`.
- Census `ok` line present; exit 0; no non-W04 findings.
- Assimilation verdict unchanged from round 95: **assimilation:none** — 8
  collisions mean the package still cannot be adopted append-only.

## Scratch hygiene

- Scratch root `/fast/scratch/hyaku/kake-r96/ExecReceipts/` contained only
  `census.stdout`; deleted before yield (`test ! -e` → deleted_rc=0).
  Evidence was copied into this directory before deletion. No tool installs;
  no sysctl changes; no mutating git (read-only `cat-file`/`log`/`diff` only).

EXEC-RECEIPTS census=0 rows=216 collisions=8
