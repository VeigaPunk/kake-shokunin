# kake round 83 — frozen contract (attempt 1)

Lane: kake-shokunin (`/home/vgpnk/Projects/shokunin/kake-shokunin`)
Round: 83 · attempt 1 · host Linux/omp · written 2026-11-04T13:4xZ
Base measured revision: `826b0061f233ce1dffb9bd6874abc1342a864247` (lane `master` tip at round open:
the round-82 verifier spot-check commit)
Frozen before any seat ran. Amended only by a dated amendment written before the after-state it
governs; a predicate, target or kill rule never moves after a seat has scored.

Scores are held this round: a claim moves evidence, not a scalar. The lowest non-retired axis is
`calibration` (2), so C1 works it; C2 works `freshness` (10, held).

## C1 — calibration: the round-82 routed-defect queue closes

Population: the six items `D1` … `D6` filed by the non-author round-82 closure at
`corpus/lessons/round-82-verifier-spotcheck.md` §6. None added or dropped after this freeze.

Frozen predicate:

    met <=> open == 0

Decided from bytes by `python3 -B .ufo/waves/round-83/c83_defect_queue.py --root <tree>
[--revision <rev>] [--fleet <dir>] [--selftest]`, which reads the measured lane tree (an exported
revision in `--revision` mode) and the fleet repo read-only. No condition is decided by a sentence
that merely says "closed": each item carries a state conjunct re-derived from a non-lesson file.

| Item | State conjunct (re-derived, not quoted) | Row conjunct (`corpus/lessons/round-83.md`) |
|---|---|---|
| D1 | `.ufo/waves/round-83/w1-spec.json` and `w1-results.json` parse; settled = rows with non-empty output; `settled_attack >= 2` and `settled_attack / settled >= 0.25` for the run-15 attack roles {reviewer, critic, mutation-tester, labrat}; `.ufo/waves/round-83/w1-accounting.json` exists and its `settled_names`/`settled_attack`/`settled_share` equal the counter's own derivation | a `D1` line carrying `0/7` and `settled_attack=` |
| D2 | `.ufo/waves/round-83/w1-accounting.json` carries `bytes_basis == "utf-8"` and one `output_bytes` per settled seat equal to the UTF-8 length the counter re-derives from `w1-results.json` | a `D2` line carrying `UTF-8` and `w1-accounting.json` |
| D3 | `.ufo/waves/round-83/controls/after-c83-instrument-check.txt` exists, carries one `C2v1 revision=<40 hex>` line whose `bound` equals its `population`, `mismatches=0` and `met=true` | a `D3` line naming that receipt and `--check` |
| D4 | `corpus/lessons/round-83.md` carries an `[r83-erratum]` block quoting, as raw substrings, at least four physical lines the fleet commit `7678247a3c13b1dc03ed1cb8f80d2dba603ee0ca` removed from `.ufo/reports/round-81/kake.md` (lines ≥ 40 chars, `-`-prefixed in `git diff cb02b705 7678247a`), each quoted line absent from the amended blob | a `D4` line carrying `7678247a` and `erratum` |
| D5 | `.ufo/waves/round-83/killers/run_killers.py` exists and, run as `python3 -B … --check`, exits 0 printing `distinguished=5/5` over the five named survivors (C1 `m3`, `m5`; C2 `m2`, `m4`, `m5`), each row `killed` on its named fixture or `equivalent` with the guarding source line printed | a `D5` line carrying `distinguished=5/5` and the five names |
| D6 | `corpus/QUALITY.md` carries a criterion line containing `corpus/lessons/round-82.md`, `Gate` and `round-83` — the provenance rule the round-82 report prose got wrong | a `D6` line carrying `§Gate` and `corpus/QUALITY.md` |

Controls, all committed before the after-state:
- `controls/base-c83-defect-queue.txt` — the counter over base `826b0061`; must read
  `open=6 closed=0 met=false`, exit 1.
- `controls/ctl-c83-junk-queue.txt` — a tree whose lesson asserts all six items closed in prose
  (`junk_tree_build.py`, rebuilt from `junk-tree.json`); must read `open=6`, exit 1.
- `controls/c83-selftest-c1.txt` — one green fixture per item plus one mutant per item and a
  missing-tree fixture; must end `selftest: N/N passed`, exit 0.

Kill rule: a base or junk control that reads `met=true` means the counter is wrong and C1 is **not
scored**. A counter whose selftest cannot run green is indistinguishable from a property that cannot
pass (round-81 mined mistake 1). The D6 row conjunct is prose by necessity (the defect is a prose
defect); its state conjunct is the standing criterion, and the junk control must still read `open=6`.

## C2 — freshness: the drift gate's header changes are classified, and the verdict re-derives

Declared surfaces: the three ids and urls frozen at `.ufo/waves/round-81/capture-expectations.json`
(`ds4cc-primary` `https://ds4cc.com/`, `ds4cc-robots` `https://ds4cc.com/robots.txt`,
`ds4cc-sitemap` `https://ds4cc.com/sitemap.xml`). Capture A is `.ufo/waves/round-81/capture`;
capture B is `.ufo/waves/round-82/capture`. No network call is made by the tool or the counter.

Frozen output grammar of the classifier `scripts/header_change_class.py` (one line per surface in
declared order, then one summary line; `--json` adds nothing the counter reads):

    surface=<id> status_a=<int> status_b=<int> diffs=<n> per_request=<n> validator=<n> representation=<n> policy=<n> unknown=<n> verdict=<same-object|representation-changed>
    summary surfaces=<n> diffs=<n> per_request=<n> validator=<n> representation=<n> policy=<n> unknown=<n> verdict=<same-object|representation-changed>

Frozen header-class table (lower-cased names; a changed header absent from the table is `unknown`):
- `per-request`: `age`, `cf-ray`, `connection`, `date`, `keep-alive`, `nel`, `report-to`,
  `server-timing`, `transfer-encoding`, `via`, `x-amz-cf-id`, `x-cache`, `x-cache-hits`,
  `x-fastly-request-id`, `x-github-edge-region`, `x-github-request-id`, `x-proxy-cache`,
  `x-request-id`, `x-request-start`, `x-served-by`, `x-timer`.
- `validator`: `etag`, `last-modified`.
- `representation`: `accept-ranges`, `content-encoding`, `content-language`, `content-length`,
  `content-location`, `content-md5`, `content-type`, `digest`, `vary`.
- `policy`: `access-control-allow-*`, `access-control-expose-headers`, `alt-svc`, `cache-control`,
  `content-security-policy`, `content-security-policy-report-only`, `cross-origin-*-policy`,
  `expires`, `link`, `permissions-policy`, `pragma`, `referrer-policy`, `server`,
  `strict-transport-security`, `x-content-type-options`, `x-frame-options`, `x-robots-tag`.

A surface verdict is `representation-changed` when status differs, body sha256 differs, or any
changed header classifies `validator`, `representation`, or `unknown`; otherwise `same-object`. The
summary verdict is `representation-changed` if any surface is, else `same-object`.

Frozen predicate:

    met <=> declared == 3
        and surfaces_a == 3 and surfaces_b == 3
        and receipts_ok      (GET, integer status 100..599, bytes == body length, sha256 == body
                              digest, truncated false)
        and diffs > 0 and validator == 0 and representation == 0 and unknown == 0
        and verdict == same-object
        and record_equal     (the committed record equals a fresh run's stdout after stripping one
                              trailing newline per side)
        and determinism      (two fresh runs print identical bytes)
        and control_ok       (`.ufo/waves/round-83/capture-control/{a,b}`: receipts vertify and the
                              classifier prints verdict=representation-changed with validator >= 1)
        and tool_offline     (no `socket`, `urllib`, `requests`, `http.client` import in
                              `scripts/header_change_class.py` outside its docstring)
        and selftest_ok      (the tool's selftest exits 0)

Controls, all committed before the after-state:
- `controls/base-c83-drift-class.txt` — the counter over base `826b0061`; the tool is absent, so it
  must read `tool_absent=1 met=false`, exit 1.
- `controls/ctl-c83-control-class.txt` — the counter over a tree in which the control pair is
  replaced by an identical pair; must read `control_ok=0 met=false`, exit 1.
- `controls/c83-selftest-c2.txt` — the counter's own fixtures; must end `selftest: N/N passed`,
  exit 0.

Kill rule: a base or control receipt that reads `met=true` means the counter is wrong and C2 is
**not scored**; a tool whose selftest cannot run green is not a capability.

## Freeze

This contract, both counters, the classifier tool, the junk builder and the base/control receipts
are committed together before the wave spec is dispatched. The wave, its seat reports and the after
receipts are the measured evidence; the report cites the carrier and the tip.
