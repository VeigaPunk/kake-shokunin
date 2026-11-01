# Gate-status ledger — historical and host-bound gates (adopted r66)

source: `considerthese/2026-10-26.md` proposal 5 (assimilation, adopted r66) + the lane's own re-runnable gate outputs — the round-66 counter receipt `.ufo/waves/round-66/controls/after-c66.txt` and the round-67 direct-run adjudication receipts under `.ufo/waves/round-67/controls/` (own-work tier-A; no SOURCES row)
verified-at: 2026-11-01 (round-66 receipt at revisions `a26fd6a5`/`f2b9e081`; round-67 adjudications at `6ff73edd1bac66c298e10e6f0f295088740c32b9`; trio fields added r67 per the r66 non-author closure defect 3 — a format fix, not a rewrite of claims; r68: the c56_selftally closing sentence reworded per the r67 non-author spot-check D-2 — its phrase self-matched the ledger-wording grep (grep -c counts matching lines; S435), so every recorded 5 → 1 count re-measured 5 → 2 at the r67 revisions; wording-only, verdict/class/disposition unchanged)
recheck: on any row's next re-adjudication, or at the next full c66-counter re-run, whichever comes first

Adopted from `considerthese/2026-10-26.md` proposal 5 ("Historical-gate list"):
a dated list of gates that go red by design on later trees or on a migrated
host, so a standing red is not misread as a fresh regression, and so a gate
that *should* be re-pinned is visible as such. Rows are derived line-for-line
from the round-66 receipts named below; nothing here is a claim that a
recorded status is correct — the receipts are the authority.

## Round-66 measurement (host: Windows, python 3.13.15, the c66 v2 counter)

Before this round the 28-member registry could not be adjudicated on this
host at all: `.ufo/waves/round-65/controls/c60-paired-thishost.txt` and the
round-66 re-run at base (`.ufo/waves/round-66/controls/c60-v1-base-r66.txt`)
both print `members=28 mismatches=28`, every observation dying of the
environment (exit 2, outside the family verdict alphabet). The round-66 v2
counter (`.ufo/waves/round-66/c66_gate_status_hostportable.py`, receipt
`controls/after-c66.txt` at revision `a26fd6a57a3549a927b2e9fb589cf72813af2c24`)
makes every member produce a real family-verdict exit:
`members=28 evaluated=28 structural=0 agreement=17 met=True` (evaluability,
not agreement — 11 label mismatches are measured and reported, not forced).

| Gate | Registry label | This-host observed | Class | Ledger disposition |
|---|---|---|---|---|
| c48_lint_count | live | e_T=0 | ok | recorded green re-derives on this host |
| c48_quote_truth | live | e_T=0 | ok | recorded green re-derives on this host |
| c49_order | live | e_T=0 | ok | recorded green re-derives on this host |
| c49_quote_truth | live | e_T=0 | ok | recorded green re-derives on this host |
| c50_durable | live | e_T=0 | ok | recorded green re-derives on this host |
| c50_quote_class | live | e_T=0 | ok | recorded green re-derives on this host |
| c51_quote_truth | live | e_T=0 | ok | recorded green re-derives on this host |
| c51_wave_ledger | live | e_T=0 | ok | recorded green re-derives on this host |
| c52_gate_registry | live | e_T=0 | ok | recorded green re-derives on this host |
| c52_mutation_ladder | live | e_T=0 | ok | recorded green re-derives on this host |
| c52_quote_truth | live | e_T=0 | ok | recorded green re-derives on this host |
| c52_wave_ledger | live | e_T=0 | ok | recorded green re-derives on this host |
| c53_gate_truth | never-met | e_T=1, e_P=1 | ok | red-at-pin red-at-tip by design; re-derives |
| c54_ops_debt | live | e_T=0 | ok | recorded green re-derives on this host |
| c54_s374_calib | live | e_T=0 | ok | recorded green re-derives on this host |
| c55_quote_truth | historical | e_T=1, **e_P=1** | historical_not_green_at_pin | pin run no longer reproduces its green on this host — read as host-era, not a tip regression; not adjudicated here |
| c55_readme_index | live | e_T=0 | ok | recorded green re-derives on this host |
| c56_quote_truth | historical | e_T=1, **e_P=1** | historical_not_green_at_pin | the r55-known "6/8 on every later tree" gate (it pins 158 rows); now also not green at its own pin on this host |
| c56_selftally | live | **e_T=2** | live_not_green | PROVEN r67 (`.ufo/waves/round-67/controls/c56-selftally-adjudication.txt`): host-intrinsic interpreter-name binding — the gate's frozen bytes mandate the literal `python3` interpreter for every documented selftest (c56_selftally.py:11,183-184) and on this host bare `python3` resolves to the inert WindowsApps Store stub (rc 9009, no output); a byte-copy `python3.exe` alias first in the caller PATH does not rescue the inner spawn (same 9009, receipted); encoding is ruled out (PYTHONUTF8 differential output identical). The r65/r66 PYTHONUTF8 attribution is REFUTED by this differential. Carry stands; a repair rewrites frozen bytes — operator ruling (r65/r66 routing). |
| c57_idresolver_gate | live | **e_T=1** | live_not_green | PROVEN r67 (`.ufo/waves/round-67/controls/c57-idresolver-direct.txt`): host semantics, not corpus growth — the frozen id_resolver tool's POSIX-only file API fails on Windows (its selftest harness hits `os.O_NONBLOCK` in 62 of 72 cases; `os.mkfifo`; an NTFS-forbidden `"` fixture name; a strict-utf-8 decode case), selftest 10/72 and fixture lanes exit 1 silently, while the gate's real-revision differential still passes on this host (G4 red-before exit 1, G5 green 116/116 exit 0). Carry stands; repair = versioned tool + gate rewrite — operator ruling. |
| c57_quote_truth | historical | e_T=1, **e_P=1** | historical_not_green_at_pin | as c55/c56 above |
| c57_receipt_pins | live | e_T=0 | ok | recorded green re-derives on this host |
| c58_quote_truth | historical | e_T=1, **e_P=1** | historical_not_green_at_pin | as c55/c56 above |
| c58_receipt_rewrites | live | **e_T=1** | live_not_green | ADJUDICATED r67 (`.ufo/waves/round-67/controls/c58-receipt-rewrites-direct.txt`, direct run at base: events=25 undisclosed=6): a real disclosure debt, not host or growth — six r65/r66 receipt events were unledgered (the r65 directory-path incident delete+readd pair on census-before.txt and l1-c2-prederivation.txt; the r66 D2 relabel append to base-c1.txt; the r66 settlement extension of pins-diff.txt). Fixed in-round by appending the six matching entries to the disclosure ledger `.ufo/waves/round-58/receipt-rewrites.json` (events 19→25, each naming its disclosing lesson/LOG path); the gate is green again at the round-67 tip (after receipt `c58-receipt-rewrites-after.txt`). |
| c58_resolver_cases | live | **e_T=1** | live_not_green | PROVEN r67 (`.ufo/waves/round-67/controls/c58-resolver-cases-direct.txt`): host-intrinsic fixture-build crash — the K5 fixture writes `a"b.md`, a name NTFS cannot contain, and the counter dies with an unhandled OSError before any case runs. Consequence recorded for the instrument family: a traceback exit 1 is indistinguishable from a family `not met` exit 1 in the c66 counter's per-member classification (the r66 receipt's `eval=ok` trusted the exit code). The r58 14/14 receipt at its own revision `de7d96e7` stands. Carry stands; repair = versioned counter with NTFS-safe fixture names — operator ruling. |
| c59_axis_evidence | live | **e_T=1** | live_not_green | PROVEN r67 (`.ufo/waves/round-67/controls/c59-axis-evidence-adjudication.txt`): host-separator corruption inside the frozen counter itself — `os.path.normpath` converts every registry pointer to backslashes while `git cat-file -t rev:path` requires forward slashes (same bytes, backslashed rc 128 vs forward-slashed rc 0, differential receipted); all 23 pointers fail and the run prints mismatches=45. Not corpus drift. Carry stands; repair = versioned v3 counter with a forward-slash normalization delta — operator ruling. |
| c59_quote_truth | historical | e_T=1, **e_P=1** | historical_not_green_at_pin | as c55/c56 above |
| c59_resolver_cases | live | **e_T=1** | live_not_green | PROVEN r67 (`.ufo/waves/round-67/controls/c59-resolver-cases-direct.txt`): the same NTFS fixture-name crash as c58_resolver_cases — the K5 fixture writes `a"b.md` and the counter dies with an unhandled OSError at fixture build. The r59 21/21 receipt at its own revision stands. Carry stands; repair = versioned counter with NTFS-safe fixture names — operator ruling. |

## Older known-historical entries (proposal 5's original list)

- `c56_quote_truth.py` — red on every tree after its pin (pins 158 registry
  rows; recorded r55). See above: now also not green at its pin on this host.
- `c53_gate_truth.py` — never-met by design (red at pin and tip); it exists to
  prove the counter catches a never-green gate.
- The three `~/Projects`-era path gates of the freshness sweep are superseded
  by the §paths sidecar mechanism (the 2026-10-30 host migration moved every
  former home tree; the r66 re-pin restored the offline gate to exit 0).

## How to use this ledger

A red row in the SKILL.md registry is "expected red" only while its receipt
chain says so; any round may re-adjudicate a row by re-running its documented
command at the revision the row names and committing the receipt. What this
ledger forbids is silent normalization: a gate that stops re-deriving must be
either re-pinned with a dated receipt or carried here with a named mechanism.
