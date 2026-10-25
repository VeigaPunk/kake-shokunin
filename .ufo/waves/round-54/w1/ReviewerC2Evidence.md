# ReviewerC2Evidence — round-54 w1 finding

Seat: `L1Kake54.ReviewerC2Evidence` — leaf reviewer, read-only wave. Sole write:
this report.

Scope: (a) does the committed round-53 closure give evidence for zero committed
seat reports; (b) does the settlement manifest reference that evidence;
(c) unsupported settlement clauses.

## Verdict

(a) **Yes** — the committed non-author closure carries the zero-committed-reports
evidence, re-derived below. (b) **Yes** — the manifest cites exactly the two
committed artifacts that carry it. (c) **No unsupported clause found**; two
low-severity observations and one timing note below.

## (a) Evidence for zero committed reports — VERIFIED

Committed closure artifacts, all present at round-open base
`68228b2d74e7930ae4f07e90e382a0d03ab80c7b` and still at current HEAD `8e408e0`:

- `corpus/lessons/round-53-verifier-spotcheck.md` (committed `68228b2`, non-author
  integrator hyaku) §Dead-seat reconciliation: "**Committed seat reports: 0.** No
  `.ufo/waves/round-53/w1/` directory exists; the 17 committed files under
  round-53 waves are the spec, gate artifacts, retained bodies, receipts and
  `gate-draft.md`." (spotcheck:72). §73 enumerates the seven unresolvable
  seat-report pointers.
- Re-derived independently at both revisions: `git ls-tree -r` shows **0** paths
  under `.ufo/waves/round-53/w1/` at `68228b2` and at HEAD `8e408e0`; exactly 17
  files under `.ufo/waves/round-53/` at `68228b2` (18 at HEAD — the +1 is
  `settlement.md` itself; no conflict, the spotcheck predates it).
- `w53-spec.json` (committed `fd91527`): `items` length 40, `maxLanes` 40,
  role mix scout 14 / connector 1 / executor 3 / scribe 6 / reviewer 8 /
  critic 8, `reportDir: .ufo/waves/round-53/w1` — the declared 40 and the exact
  directory whose absence equals zero reports. All seven manifest names are
  literal seat `name` values in `items`.
- Fleet-side committed closure `.ufo/reports/round-53/kake.md` (fleet repo,
  read-only cross-check): "A settlement artifact was not captured, so dead-seat
  count is **unverified**; no seat replacement was made." — consistent, not a
  second count.

## (b) Manifest references the evidence — VERIFIED

`.ufo/waves/round-53/settlement.md` (28 lines; committed at `8e408e0`, blob
`623db9a9`; sha256 `1e7b9fc3…` byte-identical committed vs working tree) closes
its header paragraph with: "Evidence:
`corpus/lessons/round-53-verifier-spotcheck.md` §§Conformance and Dead-seat
reconciliation; `w53-spec.json`." Both targets are committed and both carry the
40-spawned / 0-committed basis (§Dead-seat reconciliation is the precise carrier
of the 0; §Conformance is a real section of the same file but tangential to the
count — citation-precision nit only).

## (c) Settlement clause audit — per clause

| Clause | Supported? | Basis |
|---|---|---|
| 40 spawned seats, role mix 14/1/3/6/8/8 | yes | `w53-spec.json` items/maxLanes, re-derived |
| 0 committed seat reports, no `w1/` dir | yes | spotcheck:72 + `git ls-tree` at 68228b2 and HEAD |
| "evidence-backed settlement count" 40-vs-0 | yes | both of the above |
| Death outcomes "not recoverable… unverified, not inferred" | yes, with nit | spotcheck:74 says count "remains unverified"; "not recoverable" is slightly stronger — only committed-lane unrecoverability is proven (LOW-1) |
| No missing report recreated / no `resolved` row | yes | manifest table all-`lost`; no fabricated transcript text |
| Seven names absent from lane tree | yes | `find` + `git log --all` per name: no file, no history anywhere |
| All seven "Cited by round-53 lesson" | yes | `round-53.md` lines 11, 13, 15, 29 — three bare-basename citations, all literally present |
| "The 40-seat launch happened" | yes | committed dispatch digest in spotcheck header + fleet report |
| "without changing prior round-53 prose" | yes | `round-53.md` shows no post-closure edit; settlement is a new file |

### Findings (severity: LOW — nothing blocks)

- **LOW-1 — "not recoverable" overstates by a hair.** Spotcheck supports
  "unverified / not captured" for committed artifacts; whether transcripts exist
  outside the lane repo was not and cannot be proven from lane bytes. The same
  sentence marks deaths **unverified**, so the overclaim is contained; read
  "recoverable" as "recoverable from committed lane artifacts."
- **LOW-2 — 4-vs-7 citation asymmetry is real but non-vacuous.** The counter's
  `NAME_RE` requires the literal `.ufo/waves/round-53/w1/` prefix, so only 4
  names are machine-extractable from lesson bytes (base receipt `uncovered=4`,
  ExecC2Base confirmed). The manifest's seven `lost` rows cover the full
  `REQUIRED_SEAT_NAMES` set — which is the stricter contract P2.3 reading.
  Receipts printing `uncovered=4` could be misread as "only 4 cited"; documented
  here and in `ExecC2Base.md`.
- **Timing note (not a defect):** mid-review the manifest was untracked; HEAD
  then moved `acae1dc` → `8e408e0` ("round-54: repair S374 calibration and
  settle r53 ops debt"), committing it. Re-verified post-move: committed blob
  `623db9a9` matches working tree. P2.2's "manifest committed" is now
  satisfiable; receipt timing should note this transition.

## Residual risk / verification gaps

- The other 33 seats are left in the "unverified" bucket — correct per contract
  (naming them `lost` would be fabrication), but the `lost` table is the cited
  subset, not a full dead-seat census; the manifest's last paragraph already
  says so.
- Counter mechanics (`MANIFEST_RE`, `has_loss_basis`, registry-row half P2.1)
  are sibling seats' scope; this review checked evidence, referencing, and
  clause support only.
- No seat transcripts were sought outside the lane repo — consistent with the
  settlement treating them as lost pointers.

## Tools

None installed or updated (pacman untouched per host-wide pause). Read-only
commands only: `git ls-tree/log/show/cat-file/status`, `find`, `grep`, `python3`
(JSON spec parse, sha256).

## Evidence

- `.ufo/waves/round-53/settlement.md` (committed `8e408e0`, blob `623db9a9`)
- `corpus/lessons/round-53-verifier-spotcheck.md` (committed `68228b2`) §§header,
  Conformance, Dead-seat reconciliation
- `.ufo/waves/round-53/w53-spec.json` (committed `fd91527`): reportDir, items,
  role mix re-derived
- `corpus/lessons/round-53.md` lines 11, 13, 15, 29 (seven citations)
- `.ufo/reports/round-53/kake.md` (fleet repo, read-only): unverified dead-seat
  admission
- `.ufo/waves/round-54/contract.md` claim C2 (P2.1–P2.3);
  `.ufo/waves/round-54/w1/ExecC2Base.md` (base-control receipt parity)
