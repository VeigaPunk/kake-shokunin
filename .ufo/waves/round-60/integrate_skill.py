#!/usr/bin/env python3
"""Round-60 L1 integration of the wave-1 registry drafts into SKILL.md (run once, before the build commit).

1. Relabels three existing rows in place (Kind cell only; line count unchanged; none of the lines is bound by
   corpus/knowledge/freshness-sidecar.json, whose SKILL.md bindings are lines 16, 19, 20, 364, 423, 431, 445, 448-450):
   c53_gate_truth.py -> never met (pin fd91527a, w1/ExecC1Data53); receipt-pin-counter pin 32754df7 -> 20217f23
   (w1/ExecC1Registered: red at 32754df7, green from 20217f23); crawler-identity-quote-truth-counter -> historical
   (pin b322ccab; round 60 appends S427-S429, w1/ExecC1Predict, w1/CriticD1Collision).
2. Appends `### Round 60 gate-status ledger and registry additions` at EOF: the label rules, the historical-gate list
   (considerthese/2026-10-26.md proposal 5) as bullets (no table row may repeat a member path: C1 duplicate_row), the
   12 missing member rows (w1/ExecC1Data48, Data50, Data52, Data53, label edits named below) and the four round-60 rows
   (w1/ScribeC2Rows, tallies filled from the round-60 selftest receipts)."""
import re
import sys

P = "SKILL.md"
text = open(P, encoding="utf-8").read()
W1 = ".ufo/waves/round-60/w1"


def cells(line):
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]


def row(c):
    assert len(c) == 8 and all(c) and not any(re.search(r"(?<!\\)\|", x) for x in c), c[0]
    return "| " + " | ".join(c) + " |"


def replace_kind(name, new_kind):
    global text
    lines = text.split("\n")
    hits = [i for i, l in enumerate(lines) if l.startswith(f"| {name} |")]
    assert len(hits) == 1, (name, hits)
    c = cells(lines[hits[0]])
    assert len(c) == 8, (name, len(c))
    c[1] = new_kind
    lines[hits[0]] = row(c)
    text = "\n".join(lines)


replace_kind("c53_gate_truth.py",
             "gate (never met: red at its round-53 measured revision `fd91527a286086c1f4e6d4f44f715a907f041b5d` (exit 1) and at "
             "every committed revision run since, the round-60 base included: the S312/S329 locator and refusal defects it "
             "measures were never repaired; relabelled in round 60 from `w1/ExecC1Data53.md`)")
replace_kind("receipt-pin-counter",
             "gate (historical from round 58: green from `20217f23eca15862febe14545523832e21584106`, the commit that landed the third "
             "round-57 after-receipt — red at the round-57 measured revision `32754df7` itself (`new_receipts=0 scorecard_pin=0`), the pin "
             "this cell carried until round 60 (`.ufo/waves/round-60/w1/ExecC1Registered.md`); red on later trees by design because the "
             "frozen file set includes the round-57 resolver and receipts; whole-ancestry history walk)")
replace_kind("crawler-identity-quote-truth-counter",
             "gate (historical from round 60: green at its round-59 measured revision `b322ccabe1628fc0cfe80c2dddca03ed154d1349`; red "
             "from round 60 on by design — C8 requires the registry minus S425/S426 to equal the 162-row pre-append mirror, and round 60 "
             "appends S427-S429 (`.ufo/waves/round-60/w1/CriticD1Collision.md`); offline, committed bytes only; quote truth plus the "
             "append-only stale-claim correction)")


def drafted(seat, name):
    for l in open(f"{W1}/{seat}.files/rows.md", encoding="utf-8"):
        if l.startswith(f"| {name} |"):
            return cells(l)
    raise SystemExit(f"{seat}: no row {name}")


members = []
for seat, names in (("ExecC1Data48", ("citation-lint-existence-counter", "client-rendering-quote-truth-counter",
                                       "pre-append-order-counter", "crawl-budget-quote-truth-counter")),
                    ("ExecC1Data50", ("wave-grant-durability-counter", "quote-class-counter", "wave-evidence-ledger-v1",
                                      "canonical-crawler-identity-quote-truth-counter"))):
    for n in names:
        members.append(drafted(seat, n))
lad = drafted("ExecC1Data52", "ledger-mutation-ladder")
lad[2] = ("`python3 -B .ufo/waves/round-52/c52_mutation_ladder.py` (no arguments: it reads its own checkout, so the revision reaches it "
          "through the checkout it runs in)")
members.append(lad)
members.append(drafted("ExecC1Data52", "gate-registry-completeness-counter"))
ops = drafted("ExecC1Data53", "c54_ops_debt.py")
ops[0] = "ops-debt-counter"
ops[1] = ("gate (historical from round 60: green at its round-54 measured revision `a631cc0246b97f2a949d61186c7466468faf94d6` and on "
          "every tree up to the round-60 base; red from round 60 on by design — its registry check requires the round-53 row's Kind "
          "cell to read exactly `gate`, and round 60 relabels that row from observed exits (`.ufo/waves/round-60/w1/ExecC1Data53.md`); "
          "reads committed bytes)")
members.append(ops)
cal = drafted("ExecC1Data53", "c54_s374_calib.py")
cal[0] = "s374-calibration-counter"
members.append(cal)
assert len(members) == 12
for m in members:
    assert not re.search(r"\bhistorical\b", m[1], re.I) or m[0] in ("gate-registry-completeness-counter", "ops-debt-counter"), m[0]

r60 = []
for l in open(f"{W1}/ScribeC2Rows.files/rows.md", encoding="utf-8"):
    if l.startswith("| ") and cells(l)[0] in ("append-guard", "gate-status-counter", "guard-cases-counter",
                                              "user-triggered-quote-truth-counter"):
        r60.append(cells(l))
assert [c[0] for c in r60] == ["append-guard", "gate-status-counter", "guard-cases-counter", "user-triggered-quote-truth-counter"]
FILL = {"append-guard": "38", "gate-status-counter": "76", "guard-cases-counter": "6", "user-triggered-quote-truth-counter": "140"}
for c in r60:
    for i in range(8):
        if "<N>" in c[i]:
            c[i] = c[i].replace("<N>", FILL[c[0]])
    assert "<N>" not in " ".join(c), c[0]
r60[1][1] = ("gate (offline; calibration: the `SKILL.md` gate-registry status labels of the 28 frozen round 48–59 counters against their "
             "observed exits; each member command runs without a shell, cwd = a fresh `git clone --shared` detached at the revision "
             "under test, env fixed to PATH/HOME/TMPDIR/LANG, timeout 1800 s (timeout → 124); contract amendments A2–A7 and A3a; the "
             "counter's own file is not a member; also holds the three SCORECARD axis scores)")

SECTION = f"""
### Round 60 gate-status ledger and registry additions

Round 60 claim C1 (`.ufo/waves/round-60/contract.md` § Claim C1 and amendments A2–A7, A3a) reads every registry row's `Kind` cell as a
label and checks it against observed exits: `python3 -B .ufo/waves/round-60/c60_gate_status.py --root . --revision <rev>`. The labels:

- **live** — the `Kind` cell holds neither word below; the documented command exits 0 at the measured revision.
- **historical** — the cell holds the word `historical` and, as its first 40-hex revision, a pin at which the command exits 0; at the
  measured revision it exits 1 by design, because its predicate pins a frozen input (a registry mirror, a byte-prefix window, a frozen
  file set or ledger). The rest of the cell says what fails later.
- **never met** — the cell holds the words `never met` (any separator) and, as its first 40-hex revision, the round's measured revision at
  which the command already exited 1; it exits 1 at the measured revision too. It records a registered command that was never green.

Relabel duty (routed defect R59-D1): a live row that a round's own change turns red is relabelled, with its pin, in the same build that
turns it red and before the after-state is measured — the contract names it before data (round 60: the round-59
`crawler-identity-quote-truth-counter`, reddened by rows S427–S429, and `ops-debt-counter`, reddened by the honest relabel of the
round-53 row). A pin is a revision the command was run at, never a remembered one: round 60 found the `receipt-pin-counter` pin pointing
at a revision where its own command exits 1 (`.ufo/waves/round-60/w1/ExecC1Registered.md`) and moved it.

Historical-gate list (`considerthese/2026-10-26.md` proposal 5; a view over the rows' `Kind` cells, which stay the authority; names,
not paths, so no second table row repeats a member path):

- historical: `quote-truth-counter` (round 52), `gate-registry-completeness-counter` (52), `readme-index-counter` (55),
  `yahoo-robots-quote-truth-counter` (55), `yahoo-crawl-handling-quote-truth-counter` (56), `receipt-pin-counter` (57),
  `baidu-dead-link-quote-truth-counter` (57), `baidu-crawler-identification-quote-truth` (58), `ops-debt-counter` (54, from round 60),
  `crawler-identity-quote-truth-counter` (59, from round 60).
- never met: `c53_gate_truth.py` (53).
- live: every other member row; `id-resolver-gate` is live only with `--fleet` (it reads sibling lanes' registries, so it is not
  hermetic).
- outside the population: the round 40–47 counters (17 files) carry no label here and are not claimed.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
""" + "\n".join(row(c) for c in members + r60) + "\n"

if "### Round 60 gate-status ledger" in text:
    sys.exit("already integrated")
if not text.endswith("\n"):
    text += "\n"
text += SECTION
open(P, "w", encoding="utf-8").write(text)
print("relabelled 3, appended", len(members), "member rows and", len(r60), "round-60 rows")
