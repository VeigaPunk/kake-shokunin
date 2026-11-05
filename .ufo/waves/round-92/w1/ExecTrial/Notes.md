# ExecTrial-6 — Notes: heuristic freshness instrument trial on recorded domain bytes

VERDICT: trial complete — 18/18 recorded surfaces decided at exit 0, 18/18 match the
frozen contract's decision order derived before the run; no instrument defect observed
on the exercised branches. Trial, not a claim.

## 1. What this seat is

Trial seat for round 92 C2 (kake). I ran the delivered
`scripts/heuristic_freshness.py` end-to-end on **real recorded domain bytes** and
tabulated what it decides. This is an operability exercise of a delivered
instrument, not a claim: it admits nothing about any live cache, any deployed
property, or whether the recorded headers were correct at capture time.

## 2. Population and provenance

18 recorded surfaces, all present, none substituted:

- 12 × `.ufo/waves/round-61/capture/` (vault-index-kimi, ufo-fsd-kimi-pro,
  plazir27-kimi, plazir15-kimi, plazir15-ghp, lucario-kimi, lucario-ghp,
  ds4cc-primary, ds4cc-kimi, charter-kimi, charter-ghp, burnerchrome-kimi)
- 3 × `.ufo/waves/round-81/capture/` (ds4cc-primary, ds4cc-robots, ds4cc-sitemap)
- 3 × `.ufo/waves/round-82/capture/` (same three ids, second capture instant)

Per-surface provenance (source path, response.json sha256, status, fetchedAt, url,
recorded tracked headers verbatim, absent fields, combined field lines, derived
epochs): `inputs.index.json` in this directory.

## 3. Input construction (what I fed the instrument)

For every surface I built exactly the contract's stdin object
(`{"stored": {"status", "headers"}, "now"}`):

- `status`: the recorded HTTP status as recorded (four r61 kimi pages are 404).
- Only the contract-deciding fields are carried: `Date`, `Last-Modified`,
  `Expires`, `Cache-Control`, `Vary` — **when present in the recording**. Absent
  fields are recorded per surface in `inputs.index.json` (`absent_tracked`) and
  were never invented. Absences found: `Last-Modified` and `Expires` absent on all
  8 kimi-200/404 surfaces that lack them; `Cache-Control` absent on the four 404s;
  **`Vary` absent entirely on r61-ufo-fsd-kimi-pro** (the only surface with no Vary
  at all).
- `Date`/`Last-Modified`/`Expires`: recorded HTTP-dates converted to epoch seconds
  and emitted as **decimal-integer strings** (e.g. `"1793092563"`). Contract
  clause 3 requires every header value to be a string; clause 5 requires Date to be
  "a decimal integer in epoch seconds" — i.e. a string whose content is a decimal
  integer. This is the lane's declared adapter convention (no HTTP-date parsing),
  the same one `scripts/cache_current_age.py` and `scripts/stored_reuse.py` use.
  Conversions cross-checked against GNU `date -u -d ... +%s` (3/3 equal). Recorded
  verbatim HTTP-date strings are kept in `inputs.index.json`.
- `Cache-Control`, `Vary`: byte-exact as recorded (the contract's clause 2 trims).
- **Repeated field lines**: 7 of the 12 r61 surfaces record two `Vary:` field
  lines (Cloudflare sends `Vary: Accept-Encoding` and `Vary: Origin`). The
  contract's JSON header object cannot represent repeated names, and its clause 1
  refuses duplicate header names, so the faithful duplicated shape is
  inexpressible. I combined them per **RFC 9110 §5.2 field-line combination**
  (`Vary: Accept-Encoding, Origin`) before building the JSON object; every
  combination is listed per surface under `combined_field_lines` in
  `inputs.index.json`. See finding F3 (routed).
- `now`: the recorded `fetchedAt` instant in epoch seconds (r61: 2026-10-27
  09:15:53–09:16:02Z; r81: 2026-11-04 12:05:06Z; r82: 2026-11-04 13:00:27–28Z).
- `shared`: omitted (contract default `false`). No input exercised `shared=true`;
  the seat spec names no shared run and none was added.

## 4. The misbuilt-input incident (my defect, retained as a receipt)

My first build emitted `Date`/`Expires`/`Last-Modified` as **JSON numbers**.
The instrument refused all 18 inputs, exit 1, empty stdout, exactly
`invalid_input: header name or value is not a string` — clause 3 working as
written on real-ish malformed input. This was my bug, not the instrument's; I
rebuilt with integer strings and re-ran. Retained demonstration:
`outputs/validation-refusal-clause3.txt` (rebuilt single probe, exit 1).

## 5. Results

Per-surface table with the recorded headers each decision rests on:
`trial.txt` in this directory. Per-surface raw receipts:
`inputs/<surface>.json` (exact stdin) and `outputs/<surface>.{out,err,rc}`.

| Decision | Count | Surfaces |
|---|---|---|
| `not-storable` | 4 | r61 burnerchrome-kimi, ds4cc-kimi, ufo-fsd-kimi-pro, vault-index-kimi (`no-store`) |
| `explicit`, lifetime 600, heuristic=false | 10 | r61 charter-ghp, ds4cc-primary, lucario-ghp, plazir15-ghp; r81/r82 ds4cc-primary/-robots/-sitemap (`max-age=600` shadows `Expires`) |
| `heuristic-undecided` | 4 | r61 charter-kimi, lucario-kimi, plazir15-kimi, plazir27-kimi (404 is heuristically cacheable, no explicit freshness, no `Last-Modified`) |
| refusal | 0 | — |

Agreement: 18/18 with the decision I derived from the frozen contract text
(`.ufo/waves/round-92/c2-contract.md`, clauses 9–13) **before** any instrument
execution; the derivation is hard-coded with clause citations in
`make_table.py` (`EXPECTED`). Ordering attestation: `EXPECTED` was authored while
the instrument had not yet landed and was never altered after the first run —
but note the *mtime cannot evidence this*: a later cosmetic edit (removing a dead
format line, after the successful run) bumped `make_table.py`'s mtime to
21:41:49, past the instrument's landing (21:40:40, `seat-inventory.txt`). The
ordering therefore rests on this attestation, not on filesystem timestamps —
recorded as a receipt-hygiene slip in F2. No decision value was edited to match.

## 6. What the trial proves

- The delivered instrument runs end-to-end on the real recorded header sets of
  18 public surfaces (12 from round 61, two later ds4cc captures) without
  crashing, hanging, or emitting anything but the contract's output shapes.
- On every branch the corpus exercises, its decisions and lifetimes follow the
  frozen contract: not-storable (clause 9), explicit via max-age with Expires
  shadowed (clause 10), heuristic-undecided via the cacheable-status gate plus a
  missing Last-Modified (clauses 11, 13).
- Clause-3 type validation refuses malformed values on real-shaped input
  (§4 receipt).

## 7. What the trial does **not** prove (honest limits)

- Nothing about a live cache, a deployed property, or any future behaviour;
  nothing about whether the recorded headers were *correct* at capture time
  (provenance is the capture transcript, as PROVINCE records for the drift
  ground).
- **The clause-12 heuristic branch is not witnessed by real bytes.** No recorded
  surface reaches clause 12: every `Last-Modified`-bearing 200 also carries
  `max-age=600` (explicit wins, clause 10 precedes), and every 404 lacks
  `Last-Modified`. The §4.2.2-core heuristic lifetime formula
  (`min((Date−Last-Modified)//10, 86400)`) is therefore evidenced only by the
  counter's synthetic cases (ExecHeuristic's receipt), never by this corpus.
- The `Expires − Date` arm of clause 10 never decides: on all four surfaces
  where `Expires` is present, `max-age` shadows it. On r81/r82 ds4cc-primary the
  recorded `Expires` precedes `Date` (would give −1072 s and −4394 s); the
  shadowing makes that moot here, faithfully.
- No `Vary: *`, no `private`, no `shared=true`, no `public`, no
  `s-maxage`, no `not-heuristically-cacheable` outcome occurs in the corpus;
  those branches are untouched by this trial.
- `now` is validated but decision-irrelevant: contract clauses 9–13 read only
  status and headers; no exercised decision consumes `now`. The recorded
  fetch-time skew (Date up to +2 s after fetchedAt on charter-kimi and
  plazir15-kimi, +1 s on vault-index-kimi) is passed through faithfully and
  affects nothing.
- `run_trial.py` always exits 0 (it is a recorder); per-surface exit codes live
  in `outputs/<surface>.rc` and the tally in `outputs/summary.json`. Read those,
  not the runner's exit.

## 8. Findings for the routed list (defects, not edits)

- **F1 — coverage (instrument/corpus, routed):** the recorded round-61/81/82
  corpus cannot exercise the heuristic branch (clause 12) or the `Expires−Date`
  arm. Any future "real-byte" freshness evidence needs a capture of a surface
  with `Last-Modified` and no explicit freshness. This trial must not be cited
  as clause-12 evidence.
- **F2 — self-defects, fixed during the trial:** (a) my first input build used
  JSON numbers for HTTP-date fields; all 18 inputs were correctly refused
  (clause 3). Retained receipt `outputs/validation-refusal-clause3.txt`; builder
  fixed and re-run. Positive side-signal: the instrument's type validation fires
  on real-shaped malformed input. (b) A cosmetic post-run edit to
  `make_table.py` (dead format line) bumped its mtime past the instrument
  landing, destroying the cheap mtime witness that the `EXPECTED` derivation
  predates the runs; the ordering is attested in §5 instead. Receipt hygiene:
  stop touching trial scripts after the measured run.
- **F3 — contract shape vs HTTP reality (routed):** 7 of 12 r61 surfaces carry
  two `Vary:` field lines. The contract's JSON header object cannot represent
  repeated names and clause 1 refuses duplicate names, so a faithful adapter
  must combine field lines (RFC 9110 §5.2) *before* the contract boundary —
  the contract nowhere declares this. A successor contract version should state
  the combination rule at the adapter boundary, or the duplicate-shape refusal
  will keep silently depending on each caller's private choice. My choice is
  recorded in §3 and per surface in `inputs.index.json`.

## 9. Environment, tooling, network

- Python 3.14.8, stdlib only; no packages installed (tooling authorization not
  exercised); no pacman; no git mutation anywhere (no clone needed — the trial
  runs read-only over LANE and writes only this seat directory); **no network
  GET was performed** (all bytes are the committed recordings).
- Lane head at run time `f0b2dc635e34cc1c593655d926af74f19bd21034`; freeze
  revision `a5640ca02c20f94a0fa03af41b977b46ae99808e` verified as an ancestor.
- Instrument binding: `scripts/heuristic_freshness.py` sha256
  `7bfe82da8e1a1d541930ef1b4ee64cfe9b3fa5b8169680795bcc8626d2f37f5c`
  (22 985 bytes), **uncommitted worktree bytes at run time** — the digest is the
  binding; after the wave lands, re-hash against the committed blob.
  ExecHeuristic reports the frozen counter reads `met=true`
  (28/28, 120/120, 5/5) for this subject at clone rev `846d7642…`
  (`w1/ExecHeuristic/` receipts) — sibling receipt, not re-verified by me.

## 10. Replay

```
cd /home/vgpnk/Projects/shokunin/kake-shokunin
python3 -B .ufo/waves/round-92/w1/ExecTrial/build_inputs.py   # exit 0; rebuilds inputs/ (18)
python3 -B .ufo/waves/round-92/w1/ExecTrial/run_trial.py      # recorder exit 0; outputs/summary.json: exit0=18 refused=0
python3 -B .ufo/waves/round-92/w1/ExecTrial/make_table.py     # exit 0; agree=18/18 refused=0
```

All three scripts are stdlib-only, deterministic (`sort_keys` JSON dumps), and
delete nothing. Scratch `/fast/scratch/hyaku/kake-r92/ExecTrial/` was used only
as a mount point and removed before yield; no receipt lives there.
