"""Real-registry mutant controls for c61_recheck_pins.py, run on the synthetic after-state built by
integ_driver.build_green(): each mutant must fail exactly the named condition(s)."""
import importlib.util
import json
import os
import re
import sys

S = "/fast/scratch/hyaku/kake-r61/ExecC3Counter"
spec = importlib.util.spec_from_file_location("drv", os.path.join(S, "integ_driver.py"))
drv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drv)

REG, LES, RC = drv.REGISTRY, drv.LESSON, os.path.join(drv.RECHECK, "receipts.json")


def set_cell(sid, index, value):
    lines = open(REG, encoding="utf-8").read().split("\n")
    for i, line in enumerate(lines):
        m = re.match(r"^ {0,3}\|\s*(S[0-9]{3,})\s*\|", line)
        if m and m.group(1) == sid:
            lines[i] = drv.cell_line(line, index, value)
    open(REG, "w", encoding="utf-8").write("\n".join(lines))


def main():
    green = drv.build_green()
    print("green tip:", green)
    out = drv.run(green)
    print("GREEN:", [l for l in out.stdout.splitlines() if "conditions_passed" in l][0], "exit", out.returncode)

    cases = []

    def case(name, mutate, expected):
        drv.git("reset", "-q", "--hard", green)
        mutate()
        rev = drv.commit(name.replace(" ", "-"), at=None)
        out = drv.run(rev)
        fails = sorted(l.split()[0] for l in out.stdout.splitlines() if l.strip().endswith("FAIL"))
        notes = [l.strip() for l in out.stdout.splitlines() if l.strip().startswith("- ")]
        ok = fails == sorted(expected)
        print(f"{name}: exit={out.returncode} fails={fails} expected={sorted(expected)} {'OK' if ok else 'MISMATCH'}")
        for note in notes[:2]:
            print("    ", note)

    case("over-pin non-due row S011", lambda: set_cell("S011", 9, "2027-10-19"), ["C6_append_only"])
    case("due pin earlier than the base cadence (S008 365d -> 2027-01-17)",
         lambda: set_cell("S008", 9, "2027-01-17"), [])  # inside the frozen bound: records exact=False
    case("dropped receipt for S003", lambda: _drop_receipt(), ["C4_receipt_pins"])
    case("non-200 carried row S005 with a Gate note", lambda: _carry_s005(), [])
    case("Gate quote absent from the body (S006)", lambda: _bad_quote_s006(), ["C3_gate_quotes"])


def _drop_receipt():
    doc = json.load(open(RC))
    doc["receipts"] = [e for e in doc["receipts"] if not e["url"].endswith("configuring-a-publishing-source-for-your-github-pages-site")]
    json.dump(doc, open(RC, "w"), indent=1)


def _carry_s005():
    set_cell("S005", 9, "90d")
    doc = json.load(open(RC))
    for entry in doc["receipts"]:
        if "managing-a-custom-domain" in entry["url"]:
            entry["status"] = 503
    json.dump(doc, open(RC, "w"), indent=1)
    lines = open(LES, encoding="utf-8").read().split("\n")
    lines = [("- S005 — https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/"
              "managing-a-custom-domain-for-your-github-pages-site — accessed 2026-10-27 — fetch_failed (HTTP 503); "
              "cadence kept, no date pin") if l.strip().startswith("- S005 ") else l for l in lines]
    open(LES, "w", encoding="utf-8").write("\n".join(lines))


def _bad_quote_s006():
    text = open(LES, encoding="utf-8").read()
    text = re.sub(r"(?m)^- S006 .*$",
                  '- S006 — https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll '
                  '— accessed 2026-10-27 — quote: "Fresh S006 synthetic body states the recheck pin rule fails" (10 units)',
                  text)
    open(LES, "w", encoding="utf-8").write(text)


if __name__ == "__main__":
    main()
