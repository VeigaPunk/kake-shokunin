#!/usr/bin/env python3
"""Apply round-60's planned changes to the mock clone (spec-shaped, plausible cells)."""
import pathlib

MOCK = pathlib.Path("/fast/scratch/hyaku/kake-r60/ExecC1Predict/mock")

# 1. corpus/SOURCES.md — append three 11-cell registry rows after the last `| S…` row.
src = MOCK / "corpus/SOURCES.md"
text = src.read_text(encoding="utf-8")
lines = text.split("\n")
last_row = max(i for i, l in enumerate(lines) if l.startswith("| S"))
rows = [
 "| S427 | Google for Developers — Google Crawler (User Agent) Overview — https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers | docs | A | **How Google's operator says its crawlers identify in a server log** — the three signals (user-agent header, source IP, reverse DNS hostname), the robots.txt posture it states for common crawlers and special-case crawlers only, and the fleet distribution it gives | § Verify Google's crawlers and fetchers (Last updated 2026-06-12 UTC) | supersedes S425 — the three signals identify a Google crawler, and the page states a robots.txt posture for common crawlers and for special-case crawlers such as AdsBot, not for the user-triggered category | mined | 2026-10-27 | 180d | corpus/lessons/round-60.md |",
 "| S428 | Google for Developers — Google User-Triggered Fetchers — https://developers.google.com/crawling/docs/crawlers-fetchers/google-user-triggered-fetchers | docs | A | **The robots.txt posture of fetchers a user triggers** — which fetchers belong to the category and the posture the operator states for them | § Google user-triggered fetchers (Last updated 2026-08-19 UTC) | because the fetch was requested by a user, these fetchers generally ignore robots.txt rules | mined | 2026-10-27 | 180d | corpus/knowledge/google-user-triggered-fetchers.md, corpus/knowledge/googlebot-verification.md |",
 "| S429 | Google for Developers — Introduction to robots.txt — https://developers.google.com/search/docs/crawling-indexing/robots/intro | docs | A | **What robots.txt can and cannot enforce** — what the file is for, its limits as an access-control mechanism, and the other mechanisms the page points at | § What is robots.txt used for? (Last updated 2026-08-19 UTC) | robots.txt rules are directives for compliant crawlers and cannot enforce access control; a page can still be indexed without being crawled | mined | 2026-10-27 | 180d | corpus/knowledge/robots-txt-limits.md |",
]
lines = lines[: last_row + 1] + rows + lines[last_row + 1 :]
src.write_text("\n".join(lines), encoding="utf-8")

# 2. corpus/knowledge/google-user-triggered-fetchers.md — provenance trio + paragraph.
(MOCK / "corpus/knowledge/google-user-triggered-fetchers.md").write_text(
"""# Google user-triggered fetchers

source: S428 — https://developers.google.com/crawling/docs/crawlers-fetchers/google-user-triggered-fetchers
verified-at: 2026-10-27
recheck: 180d

Google separates the fetchers a product runs because a user asked for them from its automatic crawlers [S428]. Because the fetch was requested by a user, these fetchers generally ignore robots.txt rules; the page lists the category's agents and the IP ranges they arrive from [S428].
""",
 encoding="utf-8")

# 3. corpus/knowledge/robots-txt-limits.md — provenance trio + paragraph.
(MOCK / "corpus/knowledge/robots-txt-limits.md").write_text(
"""# robots.txt limits

source: S429 — https://developers.google.com/search/docs/crawling-indexing/robots/intro
verified-at: 2026-10-27
recheck: 180d

robots.txt carries directives, not enforcement: a crawler that complies follows the rules, but the file itself cannot enforce access control, and an uncrawled page may still be indexed through other references [S429].
""",
 encoding="utf-8")

# 4. googlebot-verification.md — 3-line tagged run after line 38.
gv = MOCK / "corpus/knowledge/googlebot-verification.md"
glines = gv.read_text(encoding="utf-8").split("\n")
run = [
 '  **[r60-correction 2026-10-27]** the quote above is from S426\'s category table and pre-dates the dedicated',
 "  user-triggered fetchers page [S428], which now states the posture directly: because the fetch was requested",
 '  by a user, these fetchers "generally ignore robots.txt rules" rather than ignore them outright.',
]
glines = glines[:38] + run + glines[38:]
gv.write_text("\n".join(glines), encoding="utf-8")

# 5. SCORECARD.md — append ## Round 60.
sc = MOCK / "SCORECARD.md"
sc.write_text(sc.read_text(encoding="utf-8") +
"""## Round 60 — declared claims (before implementation lands)

| Claim | Axis | Predicate |
|---|---|---|
| C1 | calibration | the gate registry's status labels of the 28 round 48-59 counters match their observed exits |
| C2 | operability | `scripts/append_guard.py` append-only rule accepts a tagged in-file correction and catches rewrites/deletions, 24/24 |
| C3 | freshness (sourced) | S425 scope overstatement superseded on S427; user-triggered fetchers robots.txt posture re-verified on S428; robots.txt limits assimilated on S429 |
""", encoding="utf-8")

# 6. LOG.md — append ## Round 60.
lg = MOCK / "LOG.md"
lg.write_text(lg.read_text(encoding="utf-8") +
"""## Round 60 — 2026-10-27

- **Frontier / assimilation.** robots.txt posture and limits per Google crawler category: S427 re-opens the S425 overview URL and supersedes its scope; S428 lane-found user-triggered fetchers page; S429 (staged S415 renumbered by document) robots.txt introduction. Registry 164 -> 167; 0-3-space collision check: 8; quarantine slice 12 rows, none adopted.
- **C1 calibration.** Gate-registry labels of the 28 round 48-59 counters against observed exits; scorecard scores held (10/10/2).
- **C2 operability.** `scripts/append_guard.py`: append-only rule with a tagged in-file correction escape; gate `c60_guard_cases.py` over 24 cases.
- **C3 freshness (sourced).** Entries `google-user-triggered-fetchers.md` (S428) and `robots-txt-limits.md` (S429); append-only `[r60-correction 2026-10-27]` run in `googlebot-verification.md`.
- **Swarm.** Two v1 waves planned (w1 build, w2 falsify); counters frozen before any after-state is scored.
""", encoding="utf-8")

# 7. SKILL.md — append ### Round 60 gate registry additions with one complete row.
sk = MOCK / "SKILL.md"
sk.write_text(sk.read_text(encoding="utf-8") +
"""
### Round 60 gate registry additions

Round 60 ships three counters whose predicates are frozen in `.ufo/waves/round-60/contract.json` before any data; receipts
`.ufo/waves/round-60/controls/` are committed once, after the run they record. Withdrawal rule: a row goes when its counter leaves the tree.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| gate-status-counter | gate (offline; the 28 round 48-59 counters' labels against observed exits at the measured revision) | `python3 -B .ufo/waves/round-60/c60_gate_status.py --root . --revision <rev> [--work <scratch>] [--jobs N] [--json]` | `0=met` (`members == 28 AND mismatches == 0 AND scores_held == 3`); `1=not met`; `2=could-not-evaluate` (revision unresolved, SKILL.md/SCORECARD.md unreadable, clone failure); `64=usage` | `python3 -B .ufo/waves/round-60/c60_gate_status.py --selftest` | base control `.ufo/waves/round-60/controls/base-c1-gate-status.txt` | read-only Git blobs; clone runs in scratch | kake |
""", encoding="utf-8")

# 8. scripts/append_guard.py — stub.
(MOCK / "scripts/append_guard.py").write_text(
"""#!/usr/bin/env python3
\"\"\"append_guard — append-only correction guard for corpus/knowledge files (round-60 stub).\"\"\"
import sys


def main() -> int:
    return 2


if __name__ == "__main__":
    sys.exit(main())
""", encoding="utf-8")

print("mock edits applied")
