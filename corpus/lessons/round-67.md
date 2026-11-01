# Round 67 — lessons (kake)

Round opened 2026-10-31/11-01 on the Windows host at base
`6ff73edd1bac66c298e10e6f0f295088740c32b9` (round-66 verifier spot-check tip,
pushed). Frozen contract: `.ufo/waves/round-67/contract.md` (predicates and the
per-row disposition rule frozen before any after-state; amendment 1 recorded
pre-row). Python 3.13.15 (`python`; bare `python3` = WindowsApps Store stub),
node 24, git 2.55; no L2 dispatch surface (r65 L0 question stands, routed
around).

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| scope (this round, found while adjudicating) | the c66 counter's per-member classification reads any exit 1 as the family verdict `not met`, but c58/c59_resolver_cases exit 1 by CRASHING with an unhandled OSError before any case runs (`.ufo/waves/round-67/controls/c58-resolver-cases-direct.txt`, `c59-resolver-cases-direct.txt`) — the r66 receipt's `eval=ok` trusted an exit code that never was a verdict | none — the frozen r66 contract defined evaluated = exit inside {0,1,2,64}, and a crash can wear 1 | recorded on both ledger rows; the routed repair is a versioned counter that requires a verdict marker line on stdout before an exit counts as a family verdict |
| stale-premise (inherited-latent since r59, surfaced by the host migration) | c59_axis_evidence resolves registry pointers through `os.path.normpath`, which on Windows turns `scripts/id_resolver.py` into `scripts\id_resolver.py`; `git cat-file -t rev:path` needs forward slashes — rc 128 backslashed vs rc 0 forward-slashed on the same bytes (`.ufo/waves/round-67/controls/c59-axis-evidence-adjudication.txt` §5), all 23 pointers fail, mismatches=45 | the round-66 sidecar lesson mined this exact class for the sweep; no counter-side check existed | proven-mechanism receipt committed; repair routed as a versioned v3 counter (forward-slash normalization delta), operator ruling |
| stale-premise (inherited-latent since r58/r59) | the resolver-cases counters build fixtures named `a"b.md`, which NTFS cannot contain — unhandled `OSError: [Errno 22] Invalid argument` at fixture build, before any case runs (both direct-run receipts) | none at the r58/r59 landing (POSIX host); grounded this round by the new S434 row | proven-mechanism receipts committed; repair routed as versioned counters with NTFS-safe fixture names |
| attribution (r65/r66 wording corrected this round) | the ledger carried c56_selftally's red under the candidate mechanism "PYTHONUTF8 does not reach the fixed-key child env"; direct evidence refutes it: with a byte-copy `python3.exe` alias first in the caller PATH the inner spawn still exits 9009, and the first inner instrument's output is byte-identical with and without PYTHONUTF8 (`.ufo/waves/round-67/controls/c56-selftally-adjudication.txt`) — the proven mechanism is the frozen mandate of the literal name `python3` (c56_selftally.py:11,183-184) resolving to the inert Store stub on this host | the r66 contract disclosed the limit as candidate, unproven — the carry was honest but the attribution was wrong | ledger row rewritten with the proven two-part mechanism and the differential receipts; the PYTHONUTF8 candidate is marked refuted |
| landing (this round, caught before landing) | two early receipt attempts captured the exit of a pipe stage instead of the instrument (`echo EXIT=$?` after a pipe printed head's 0 for a tool that exited 1), and hand-typed revision strings / scratch paths drifted mid-round; the first S434 insert also put a literal `|` inside a cell (census E01, fields=12) | the CORPUS rule that a count carries its command, re-derivation habit, and the census itself | every round-67 receipt captures the true exit (`${PIPESTATUS[0]}` or unpiped redirect), every revision is git-derived (`git rev-parse HEAD`), and the census was re-run with unpiped exit capture; the S434 cell was reworded before any commit |

## Gate

Candidates: (a) re-adjudicate the six carried live-red registry rows with
revision-pinned receipts; (b) register the c66 host-portable counter in
SKILL.md (the r66 reject (d) routing); (c) date-stamp the two .kimi.pro
standing records (GET-only); (d) relabel mismatching rows to historical
without this-host pin runs; (e) force agreement or normalize red rows away;
(f) repair the frozen counters in place (c56 env, c59 normpath, fixture
names); (g) L2 wave.

- **Admit (a) as C1 — calibration 2→2 HOLD (lowest owned non-retired axis).**
  Frozen disposition rule per row (contract §C1): relabel only with a
  this-host pin run that exits 0 (none qualified — every mechanism found is
  host-intrinsic at every revision); disclose real debt and stay live; or
  carry with a proven mechanism. Outcomes, each receipted at base
  `6ff73edd…`: c58_receipt_rewrites was REAL disclosure debt (events=25,
  undisclosed=6 — the r65 directory-path incident pair, the r66 D2 append and
  the r66 settlement pins-diff extension; `controls/c58-receipt-rewrites-direct.txt`)
  → six matching entries appended to `.ufo/waves/round-58/receipt-rewrites.json`
  (events 19→25, each naming its disclosing path), gate green again at the
  round tip (`controls/c58-receipt-rewrites-after.txt`, met=True exit 0). The
  other five rows are carried with proven host-bound mechanisms, receipts
  committed: c56_selftally (interpreter-name mandate + Store stub; alias
  does not rescue; encoding ruled out), c57_idresolver_gate (tool's
  POSIX-only file API: selftest 10/72, fixture lanes silent exit 1, while the
  real-revision differential G4/G5 passes on this host), c58_resolver_cases +
  c59_resolver_cases (NTFS-forbidden fixture name, crash before any case),
  c59_axis_evidence (normpath corruption, all 23 pointers). Before:
  `agreement=17` with six carried live-reds (`controls/c66-before-r67.txt`);
  after: `agreement=18` at the round tip (`controls/c66-after-r67.txt`) —
  the +1 is the disclosed row, no label was forced. Counting command:
  `python -B .ufo/waves/round-66/c66_gate_status_hostportable.py --root . --revision <tip> --jobs 6`;
  ledger wording count: `grep -c "not adjudicated here\|candidate mechanism"
  corpus/knowledge/gate-status-ledger.md` 5 → 0. The five
  historical_not_green_at_pin rows are out of scope this round (frozen
  contract) and stand untouched.
- **Admit (b) as C2 — operability 10→10 HOLD.** The routed "first registry
  item" landed: `### Round 67 gate registry additions` appended below every
  sidecar-bound SKILL.md line (bound max 935; file 1377 → 1396 lines, bound
  lines untouched). `grep -c "c66_gate_status_hostportable" SKILL.md` 0 → 1.
  The row is outside the 28-member population regex; `structural == 0` and
  `members == 28` hold at the tip (c66-after receipt). No frozen counter
  bytes changed.
- **Admit (c) as C3 — freshness 10→10 HOLD.** The two .kimi.pro standing
  records date-stamped on this host, GET-only
  (`.ufo/waves/round-67/probes/receipt.json`): ufo-fsd.kimi.pro 200 / exactly
  612 bytes (SKILL property-table record and property-map:c49/c50
  re-derive); plazir27.kimi.pro 302 → statics preview-404-en.html, final 200
  / exactly 5,995 bytes (PQ-6's size re-derives; property-map:c56
  supersession confirmed). Dated corrections appended to
  `corpus/knowledge/publish-queue.md`. Counting command:
  `grep -c "r67 dated" corpus/knowledge/publish-queue.md` 0 → 1; digests
  verified mechanically against the committed bodies.
- **Reject (d):** relabelling without a this-host pin run — the frozen rule
  (K1) allows a relabel only when the documented command exits 0 at the pin
  on THIS host; every examined row is host-bound at every revision, so zero
  relabels were made (the honest count: SKILL.md Kind cells untouched).
- **Reject (e):** forcing agreement — only the row whose red was a real,
  documentable disclosure debt changed; the five host-bound rows stay red and
  carried, agreement reported as-is (18/28).
- **Reject (f):** in-place repairs of frozen counters (the c56 inner env, the
  c59 normpath line, the fixture names) — each repair rewrites frozen bytes
  and belongs to the operator's versioned-repair ruling (r65/r66 routing
  stands); the repairs are specified in the ledger rows and routed.
- **Reject (g):** L2 wave — no dispatch surface exists on this host; the
  round is L1-only, disclosed (kake round-65 L0 question stands, routed
  around, never treated as answered).
- **Fresh-start duty (§7).** The rendered prompt's §7 declares this a
  fresh-start round off the r62/r63/r64 rejections; note the staleness: r65
  and r66 were since admitted by non-author spot-checks, and this round still
  honors the duty. Ruled out and why: (1) any calibration claim whose green
  survives marker-prose or a hidden criterion (r62's falsified counter,
  r63/r64 kill rules) — C1's delta is direct-run receipts and a ledgered
  disclosure measured by the verifier-reproduced c66 counter, and C1 promises
  no agreement number (K5); (2) counters without committed differential
  fixtures — every mechanism here is a committed direct-run differential;
  (3) re-adjudications by relabel without pin runs (the r64 causation class)
  — rejected above as (d); (4) freshness via SOURCES recheck cadences —
  measured 0 rows due (awk sweep over opened+cadence, 2026-10-31), nothing to
  move, so the probe class was chosen instead.
- **Sourced claims.** S133 re-opened live (C1's evaluability predicate rests
  on its returncode semantics): one GET, 2026-11-01T07:52:20Z, HTTP 200,
  208,624 bytes, sha256 `624069f9…78a5d` — same size as the r66 body, bytes
  drifted upstream again (receipt `.ufo/waves/round-67/sources/receipt.json`;
  retained body committed beside it); located quote (11 words): "an exit
  status of 0 indicates that it ran successfully" (§Popen.returncode). S434
  opened live and written this round (grounds the NTFS fixture-name
  mechanism): one GET, HTTP 200, 67,904 bytes, sha256 `8e7f3450…031f1d`;
  located quote, 16 words: "Use any character in the current code page for a
  name, including Unicode characters and characters in the extended
  character set (128–255), except for the following:" (§Naming Requirements,
  the reserved-set item; the list that follows names the nine reserved
  characters). Amendment 1 to the round contract (recorded pre-row) widened
  the SOURCES clause from byte-frozen to append-only-one-row for exactly this.

## Protocol work (not claims)

- Carry-in D1 (r66 closure defect 1): name-map erratum appended to
  `.ufo/waves/round-66/contract.md` (append-only; recorded lines untouched).
- Carry-in D2 (defect 2): scoping erratum appended to
  `.ufo/waves/round-66/controls/noharm-final.txt` (whole-tree deletions
  enumerated: pins −6, sidecar −273, sweep repair −3; five-file scope claim
  preserved).
- Carry-in D3 (defect 3): the provenance trio `source:` / `verified-at:` /
  `recheck:` prepended to `corpus/knowledge/gate-status-ledger.md` (the r66
  closure sanctioned the in-file format fix; claims untouched).
- Assimilation: `considerthese/2026-10-26.md` proposals 1–4 evaluated;
  none adopted — proposal 2 (receipt-rewrite watch) is superseded by the
  standing c58_receipt_rewrites gate whose backlog this round ledgered;
  proposal 4 is verifier-side data, not lane-ownable; proposals 1/3 need
  surfaces this host lacks. The shokuknow register is unreachable from this
  host.
- Census, sweeps, after-receipts: see the round report; all commands and
  exits recorded in `.ufo/waves/round-67/controls/`.
