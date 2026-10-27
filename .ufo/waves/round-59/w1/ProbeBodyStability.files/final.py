#!/usr/bin/env python3
"""ProbeBodyStability part 5: final validation of the recommended recheck spans.

For each recommended span:
  - counter's own span_tools.check verdict on the RETAINED body (units/char ceilings, one text node, page-unique);
  - the same checks against every FRESH fetch (in one text node of that fetch's article block);
  - grep -F single-line containment in the raw file of every body (retained + 3 fetches);
  - whether the span crosses a whitespace-collapsed text-node boundary (it must not).
"""
from __future__ import annotations

import importlib.util
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
WAVE = f"{LANE}/.ufo/waves/round-59"
SCRATCH = "/fast/scratch/hyaku/kake-r59/ProbeBodyStability"

spec = importlib.util.spec_from_file_location("c59qt", f"{WAVE}/c59_quote_truth.py")
qt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qt)

PICK = {
    "S425": "Therefore, your logs may show visits from several IP addresses.",
    "S426": "Run a reverse DNS lookup on the accessing IP address from your logs, using the",
}


def collapsed(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return qt.re.sub(r"\s+", " ", fh.read())


def main():
    for sid, span in PICK.items():
        print(f"=== {sid} ===")
        print(f"recommended span: {span!r}")
        r = subprocess.run(["python3", "-B", f"{WAVE}/span_tools.py", "check", sid, span],
                           capture_output=True, text=True)
        print(f"  span_tools.check (retained): {r.stdout.strip()}")
        for n in (1, 2, 3):
            p = f"{SCRATCH}/fetches/{sid}.{n}.html"
            t = collapsed(p)
            segs = [s.strip() for s in qt.text_segments(t, sid)]
            hosts = [s for s in segs if span in s]
            # grep -F on the raw file: single line?
            raw = open(p, encoding="utf-8", newline="").read()
            hits = [i + 1 for i, l in enumerate(raw.split("\n")) if span in l]
            print(f"  fetch{n}: in_one_text_node={len(hosts) == 1} nodes_with_span={len(hosts)} "
                  f"count_in_body={t.count(span)} raw_line_hits={hits}")
        # does the span cross a text-node boundary? (it must be inside ONE node)
        t = collapsed(f"{WAVE}/sources/{sid}.html")
        segs = [s.strip() for s in qt.text_segments(t, sid)]
        hosts = [s for s in segs if span in s]
        print(f"  retained: hosts={hosts}")
        print(f"  topic '{qt.TOPIC[sid]}' carried by span: {qt.TOPIC[sid].lower() in span.lower()}")
        print()


if __name__ == "__main__":
    main()
