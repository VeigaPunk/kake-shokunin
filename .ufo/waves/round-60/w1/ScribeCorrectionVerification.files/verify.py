#!/usr/bin/env python3
"""Read-only verifier for the round-60 C3 correction draft (seat ScribeCorrectionVerification).

    python3 -B verify.py [--lane /home/vgpnk/Projects/shokunin/kake-shokunin]

Reads the base blob with `git show` (read-only), the two artifacts in this directory and the retained
round-60 bodies, and prints one line per check. Exit 0 when every check holds, 1 otherwise.
"""
import argparse
import difflib
import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_REV = "97cdc122379711c2b02a8970752c8782da3ac81d"
PATH = "corpus/knowledge/googlebot-verification.md"
QUOTE = ("Because the fetch was requested by a user, these fetchers generally ignore "
         "robots.txt rules.")


def collapse(raw: bytes) -> str:
    return re.sub(r"\s+", " ", raw.decode("utf-8"))


def segments(text: str) -> list[str]:
    lo = text.find('class="devsite-article-body')
    hi = text.find("<devsite-content-footer", lo + 1)
    if lo < 0 or hi <= lo:
        return []
    chunk = re.sub(r"(?is)<(style|script)\b.*?</\1>", "<>", text[lo:hi])
    chunk = re.sub(r"(?is)<(aside|nav|devsite-feedback|devsite-thumb-rating)\b.*?</\1>", "<>", chunk)
    return re.findall(r">([^<>]+)(?=<)", chunk)


def units(text: str) -> int:
    return len(text.split())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default="/home/vgpnk/Projects/shokunin/kake-shokunin")
    a = ap.parse_args()
    base = subprocess.run(["git", "-C", a.lane, "show", f"{BASE_REV}:{PATH}"],
                          check=True, capture_output=True).stdout
    patch = open(os.path.join(HERE, "googlebot-verification.md"), "rb").read()
    run = open(os.path.join(HERE, "insert.md"), "rb").read()
    B, P, R = base.decode().split("\n"), patch.decode().split("\n"), run.decode().split("\n")
    bodies = {}
    for sid, rel in (("S426", "round-59/sources/S426.html"),
                     ("S427", "round-60/sources/S427.html"),
                     ("S428", "round-60/sources/S428.html"),
                     ("S429", "round-60/sources/S429.html")):
        bodies[sid] = collapse(open(os.path.join(a.lane, ".ufo/waves", rel), "rb").read())

    checks = []
    # locating the run in the patched file
    sm = difflib.SequenceMatcher(a=B, b=P, autojunk=False)
    ops = sm.get_opcodes()
    checks.append(("no base line replaced or deleted", all(t in ("equal", "insert") for t, *_ in ops)))
    # the correction run: 9 content lines + its closing blank line, occupying patched lines 40..49
    tag_i = next(i for i, line in enumerate(P) if "r60-correction 2026-10-27" in line)
    checks.append(("the base prefix up to and including the blank after base line 38 is untouched",
                   tag_i == 39 and P[:tag_i] == B[:tag_i] and B[38] == ""))
    # K15-shape: removing the run (tag line .. its closing blank) reproduces base exactly
    end = tag_i
    while end + 1 < len(P) and P[end] != "":
        end += 1
    checks.append(("run is tag line .. its closing blank line (first line non-blank, last line blank)",
                   P[tag_i] != "" and P[end] == ""))
    run_p = P[tag_i:end + 1]
    checks.append(("patched minus run equals base byte for byte", P[:tag_i] + P[end + 1:] == B))
    checks.append(("run equals insert.md lines", run_p == (R[:-1] if R and R[-1] == "" else R)))
    checks.append(("run first line starts with the tag prefix",
                   P[tag_i].startswith("  **[r60-correction 2026-10-27]**")))
    checks.append(("tag matches the guard regex outside code spans",
                   bool(re.search(r"\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\]", P[tag_i]))
                   and P[tag_i].count("`") % 2 == 0))
    checks.append(("tag line cites S428 and carries the quote", "S428" in P[tag_i] and QUOTE in P[tag_i]))
    checks.append(("quote is 6..25 units and <= 160 characters",
                   6 <= units(QUOTE) <= 25 and len(QUOTE) <= 160))
    checks.append(("quote is a substring of exactly one S428 article text node",
                   sum(QUOTE in s for s in segments(bodies["S428"])) == 1))
    checks.append(("quote is page-unique across S426..S429",
                   bodies["S428"].count(QUOTE) == 1
                   and all(bodies[s].count(QUOTE) == 0 for s in ("S426", "S427", "S429"))))
    spans = [q for line in run_p for q in re.findall(r'"([^"]*)"', line)]
    checks.append(("the run carries exactly one double-quoted span and it is the S428 quote", spans == [QUOTE]))
    checks.append(("no curly quotes in the run",
                   not re.search(r"[\u201c\u201d\u2018\u2019]", "\n".join(run_p))))
    checks.append(("base line 38 unchanged and present once",
                   P.count('  > "acts on the request of a user. Because the fetch was requested by a user, '
                           'these fetchers ignore robots.txt rules."') == 1))
    checks.append(("dated divergence printed by both bodies",
                   "Last updated 2026-03-20 UTC" in bodies["S426"]
                   and "Last updated 2026-08-19 UTC" in bodies["S428"]
                   and bodies["S426"].count("these fetchers ignore robots.txt rules") == 1
                   and bodies["S428"].count(QUOTE) == 1))
    checks.append(("base and patched both end with a newline",
                   base.endswith(b"\n") and patch.endswith(b"\n")))
    for label, ok in checks:
        print(("PASS " if ok else "FAIL ") + label)
    print(f"base_sha256={hashlib.sha256(base).hexdigest()} patched_sha256={hashlib.sha256(patch).hexdigest()} "
          f"base_bytes={len(base)} patched_bytes={len(patch)}")
    return 0 if all(ok for _, ok in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
