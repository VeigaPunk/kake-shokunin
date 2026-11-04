# ExecOracle — round-80 w1 report

**Verdict: independent re-derivation of the a2 oracle agrees with the frozen `expect/expect.json` on all 12 cases (exit, findings, and every check's `directives`/`effective`/`bots`); zero disagreements; no case looks fitted to the round-79 tool's behaviour — the frozen oracle stands.**

## What was done

- Read, in order: round-80 frozen contract, amendment 1 (A1–A3), all 12 case manifests, `make_cases.py`, and the round-79 frozen grammar (items 1–9). `expect/expect.json` was read only after my own per-case answer was fixed.
- `scripts/x_robots_tag_audit.py` was **never executed**. No production file was written (not my surface). No tools installed; system `python3` and `diff` only.
- Full derivation with per-case grammar citations:
  `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-80/w1/ExecOracle/derivation.md`.

## Per-case verdict table (mine vs `expect/expect.json`)

| id | expect | mine | verdict |
|---|---|---|---|
| c32 | clean, `unavailable_after:Wed, 03 Dec 2025 13:09:53 GMT`, exit 0 | same | agree |
| c33 | clean, `unavailable_after:Sunday, 06-Nov-94 08:49:37 GMT`, exit 0 | same | agree |
| c34 | clean, `unavailable_after:Sun Nov  6 08:49:37 1994` (double space kept), exit 0 | same | agree |
| c35 | clean, `unavailable_after:2025-12-31`, exit 0 | same | agree |
| c36 | clean, `unavailable_after:2025-12-31T23:59:59-03:00`, exit 0 | same | agree |
| c37 | `xrt_invalid_value` only, empty sets, exit 1 | same (A3: comma-bearing failing value → invalid only, never unknown) | agree |
| c38 | clean, 3 directives sorted, exit 0 | same (A1 protects the `Wed,` comma; comma after `GMT` segments) | agree |
| c39 | 2 directives kept, `xrt_duplicate_directive`, exit 1 | same (name-level duplicate, values differ — r79 c21 pin) | agree |
| c40 | global empty, `bots.googlebot=[unavailable_after:Wed, 03 Dec 2025 13:09:53 GMT]`, exit 0 | same (A1 reaches bot-scoped rules) | agree |
| c41 | 1 directive, `xrt_unknown_directive` only, exit 1 | same (`frobnicate`: no colon → G3 unknown) | agree |
| c42 | `max-snippet:20` + RFC 850 token, cap kept (no `nosnippet`), exit 0 | same | agree |
| c43 | `noindex` + asctime token (single space + `16`), exit 0 | same (comma after `1994` terminates; not weekday-following) | agree |

**Disagreement list: empty.**

## Anti-fitting finding (asked question)

**No fitted expectation found.** Structurally the set cannot be fitted to the round-79 tool: 10/12
cases (c32–c34, c37–c43) expect clean/invalid-only outcomes where the untouched round-79 tool
produces `xrt_invalid_value` + `xrt_unknown_directive` (`controls/base-c80-a2.txt`: `a2 wrong=10`);
A3 pins the divergence explicitly. The only two cases where old tool and oracle agree — c35, c36 —
are pinned by round-79 grammar item 5 (ISO shapes, date-only accepted). Two latent conventions are
named in the derivation (neither is a disagreement, both favour the frozen oracle):

1. **Value ws-trim** — needed by every comma-bearing case, standing alone only in c42
   (`max-snippet: 20`); textually entailed by A1's "leading weekday token of a value" phrasing plus
   the r79 segment-trim rule and the c05 bot-remainder pin, but not pinned by any r79 case. Any
   implementation passing c32–c41 implements it, so c42 follows.
2. **A2 asctime day notation** — the amendment's literal `{1,2}[0-9]{1,2}` is loose; prose + RFC 9110
   pin 1–2 spaces then 1–2 digits. An unpadded `Nov 6` is accepted by the loose reading only; no case
   exercises it, so strict and loose implementations both pass all 12. c34/c43 pin the padded forms.

## Evidence

- Oracle integrity (frozen bytes = authoring record output): scratch copy of `make_cases.py` re-run →
  `cases=12`, rc=0; `diff -r` frozen `cases/` vs regenerated rc=0; `diff expect/expect.json` rc=0;
  frozen sha256 `8f24c0aaede6a9c893a4f6bd079667b8047ffe570557e44862501b00c0568e9a`.
- Retained receipts: `.ufo/waves/round-80/w1/ExecOracle/receipts/repro-diff.txt` (sha256
  `8d8217208cfc32bdd524209095710770212fb2b7d057092a522cb1ecc5d541ec`) and
  `receipts/regenerated-expect.json` (sha256 `8f24c0aa…`, identical to frozen).
- Round-79 pins cited: `cases/c21/manifest.json:10` + `expect/expect.json:327` (name-level duplicate);
  `cases/c05/manifest.json:10` + `expect/expect.json:63-68` (bot-remainder trim).
- Scratch discipline: `/fast/scratch/hyaku/kake-r80/ExecOracle` removed, verified absent.

## Risks / notes for L1

- None blocking. The two latent conventions above are the only places a grammar-faithful
  implementation could diverge from the oracle; both are pinned by case outcomes once the set is run
  (10 cases force VT; no case forces the `Nov 6` edge, so either strict or loose A2 is safe this round).
