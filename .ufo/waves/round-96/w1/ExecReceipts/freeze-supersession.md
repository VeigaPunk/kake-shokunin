# Freeze supersession evidence (round-95 Amendment A digests)

## Finding

`corpus/lessons/round-95-verifier-spotcheck.md` "Routed to round 96" item 6
flags that the round-95 freeze file still instructs readers to hash the
withdrawn Amendment-A digests. Filed bytes are never rewritten, so the
supersession is recorded here and must be carried into the round-96 lesson.

## Stale-text evidence (current tip)

- `grep -n "04be4a7d\|9eff04c5" .ufo/waves/round-95/freeze.md` rc=0:
  - line 160: `c95_selfassess.py` sha256 `04be4a7dc32adee08e386936e2af8257a191421bd2005c97b40af49933a24a32`
  - line 162: `frozen/c1-surfaces.json` sha256 `9eff04c5a0567f50a3a27004ac7d5aab4d4dc2d1311c4a8d8eb623db8ec4f665`
- Lines 169-171 of the same file still read: "A wave seat that reproduced a
  context-digest mismatch on the C1 counter was looking at the pre-amendment
  bytes: this section is the explanation, and every post-amendment check must
  hash the values above."

The Amendment-A values were introduced by commit `d9be693f` (post-freeze
instrument edit) after the freeze commit `8f638b59`, flagged by
CriticClaims-67 and SentinelScope-30 F1, and withdrawn from scoring by
orchestrator integrity ruling option (b) (`corpus/lessons/round-95.md` Gate).

## Authoritative ruling receipt set

- `git cat-file -e 4f443b3f^{commit}` rc=0; `git cat-file -t 4f443b3f` =
  `commit`. Commit subject: "round-95: integrity ruling option (b) -
  restore frozen instrument bytes and controls; amendment A withdrawn from
  scoring".
- `git diff 43cdd9fc 4f443b3f --stat -- .ufo/waves/round-95/c95_selfassess.py
  .ufo/waves/round-95/frozen/c1-surfaces.json
  .ufo/waves/round-95/controls/instrument-sha256.txt` rc=0: the two
  instrument blob paths are byte-identical between the instruments commit
  `43cdd9fc` and the ruling commit `4f443b3f` (empty diff on both paths);
  only `controls/instrument-sha256.txt` differs (+8 insertions) because the
  pins file did not exist in `43cdd9fc` (`git show
  43cdd9fc:.ufo/waves/round-95/controls/instrument-sha256.txt` → fatal: path
  exists on disk, but not in '43cdd9fc') and was added by `4f443b3f` pinning
  the restored bytes. The full `43cdd9fc..4f443b3f` diff adds the freeze
  file, control receipts and restore-verify receipts; it does not alter the
  instrument blobs.
- Tip-byte digests filesystem: `c95_selfassess.py` =
  `8fd27d626883f2b6852ea2ee425706a77a72eeaee10ef740b8e0fc15ac03b193`
  and `frozen/c1-surfaces.json` =
  `00a04c9a68f00de1561d70822a8ff3cab718583de4cd2cbf6ebd06e87b5d47b8`,
  both matching `controls/instrument-sha256.txt` and the spot-check's
  tip-blob hash. The round-96 freeze separately pins the round-95 counter
  at `8fd27d62…` as never amended.

## Draft supersession paragraph for the round-96 lesson

> The round-95 freeze file (`freeze.md` Amendment A, lines 160-171) still
> carries the withdrawn Amendment-A digests `04be4a7d…` / `9eff04c5…` and
> instructs checkers to hash those values; filed bytes are never rewritten,
> so that instruction is superseded by the integrity-ruling receipt set at
> commit `4f443b3f` (option (b)): the authoritative instrument digests are
> the round-95 tip-byte values `8fd27d62…` (`c95_selfassess.py`) and
> `00a04c9a…` (`frozen/c1-surfaces.json`), byte-identical to the instruments
> commit `43cdd9fc` and pinned in `controls/instrument-sha256.txt`; any
> check hashing `04be4a7d…` / `9eff04c5…` verifies the withdrawn amendment
> and is invalid for scoring.

## What this seat did not do

- No byte in `round-95/freeze.md` was edited (read-only grep/sed evidence
  only). No instrument was repaired or re-pinned. The round-96 counters
  reproduce the instrument-sha256 pins exactly:
  `c96_selfassess.py a282da65…`, `c96_reval.py ec40aec1…` (sha256sum rc=0).
