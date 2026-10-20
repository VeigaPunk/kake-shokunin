# HistoricalDate — critic of C1: provenance metadata vs actual freshness

Seat: `KakeR21.HistoricalDate` (critic, leaf, read-only). Base `5009ecaa`; the
working tree was read about 09:00Z on 2026-10-20, after the 17 scribe prefixes
had landed (unstaged). The only repo file this seat wrote is this report. All
experiments ran on throwaway copies under `/tmp/hd-r21-*`; they were deleted
after use. No network reads were made, and no tools were installed or updated.

Axes: **freshness** (whether `verified-at` is honest, and whether the §paths gate
is harmed) and **operability** (whether the `recheck` lines can be executed).

## Verdict

- **The landed headers mostly hold up.** None invents a date, and none claims a
  live re-verification. The falsifier below passes 20 of 21 entries. The one
  failure is a false commit attribution (F2). Every one of the 17 new
  `verified-at` lines carries the class token `historical[-, ]not live-reverified`.
- **Neither planned instrument can detect a dishonest date (F1).** The SCORECARD
  count command and `freshness-sweep --section=paths` both accept invented and
  "live re-verified" dates. I planted such dates and both reported the same
  result as for honest headers. The 4→21 count shows the fields are present. It
  does not show they are true, and it does not show the facts are fresh.
- **C1 harms the §paths pin contract (F4).** It adds 4 new misses, which by
  itself is enough to make the gate exit 1. The exit code hides this because
  the gate was already at exit 1 at base.
- **Do not describe C1 as fresher facts.** It improves how legible the
  provenance is; the facts are no fresher. The first `verified-at` date runs
  from 2026-09-21 to 2026-09-29 for 16 of the 17 historical entries.
  `freshness-sweep` (own-work) is dated 2026-10-19.

## F1 — Counterexample: both instruments are blind to invented or live-claimed dates

I planted variants into copies of base `5009ecaa` and of the working tree:

| Variant (fleet-registry.md unless noted) | SCORECARD count | §paths sweep | Falsifier below |
|---|---|---|---|
| Honest historical header, absence annotated on the same line | 5/21 (base copy) | identical to base: exit 1, drift 3, newMissing 0 | pass |
| `verified-at: 2026-10-20 (live re-verified: 21 rows, 12 live)`, `recheck: weekly` | counted (5/21 on base, 21/21 on working tree) | **identical to base** | H1, H2, H6 FAIL |
| kimi-subpath-audit `verified-at: 2026-08-21 (index vintage)` (a content date) | 21/21 | — | H5 FAIL |
| origin-repos `verified-at: 2026-10-14 (r18 re-census)` (annotation date, after the prune) | 21/21 | — | H4 FAIL |
| speedrun-pipeline `verified-at: 2026-09-30` (date absent from evidence) | 21/21 | — | H3 FAIL |
| mirror-pitfalls with no historical/live class token | 21/21 | — | H1 FAIL |
| Header citing an absent `~/` path with **no** absence word | counted | drift 3→4, declaredAbsent 52→51, **exit still 1** | n/a (sweep metric) |

Every planted defect was counted as covered. The sweep exit code stayed the same
in every case, because base is already at exit 1.

### Falsifiable conditions (H0–H7)

All are checked per entry against the first 8 lines.

- **H0 — trio present.** The first 8 lines contain non-empty `source:`, `verified-at:` and `recheck:`.
- **H1 — declared class.** `verified-at` contains `historical[-, ]+not[- ]live[- ]re-?verified`
  (case-insensitive). The alternative is the *live-opened* class: every S### in
  `source:` except S019 has a `corpus/SOURCES.md` `opened` date equal to the first
  `verified-at` date. The 4 round-20 entries satisfy the alternative (S001–S013
  opened 2026-10-19). This splits 21/21 into 4 live-opened and 17 historical
  entries.
- **H2 — no round-21 date.** Any date ≥ 2026-10-20 must sit inside a negation
  (`not a 2026-10-20 domain recheck`). The wave contract forbids domain reads, so
  no round-21 domain evidence exists to back such a date. An entry with no date
  must name a revision.
- **H3 — dates grounded.** Every date in `verified-at` appears in the entry's
  base bytes, either as `YYYY-MM-DD` or in short `MM-DD` form, or is the commit
  date of a commit that touched the entry or is named in the same field.
- **H3b — commit attribution.** A lane commit credited with evidence must be the
  commit that introduced that evidence. Check with
  `git log --reverse -S'<literal>' -- <entry>`.
- **H4 — absent-source ceiling.** For a historical-class entry whose base carries
  absence annotations, the first date must be ≤ 2026-10-12 (the W7 prune).
  Nothing can be verified from a source after it is gone. `freshness-sweep.md`
  is exempt: its source is present and own-work.
- **H5 — observation date, not content date.** The first date must appear on a
  base line that records an observation (read, run, observed, baseline, probe,
  fetch and so on). It must not be an `mtime`, `updatedAt`, `lastmod`, vintage
  or "embedded max date" value.
- **H6 — no live claim.** No phrase such as `live re-verified`, `re-verified today`
  or `confirmed now` may appear outside a negation.
- **H7 — no asserted result.** `recheck` must not state an observed round-21
  result. An `expect …` clause is allowed.

These conditions are *necessary* conditions. They do not prove truth. They cannot
show that the chosen date is the best honest date, and H3b only fires when a
size or count literal follows the commit.

### Results

- **Working tree:** 1 violation, H3b on vault-properties (F2).
- **Planted copy:** 8 violations, which catch all 5 planted defects. The 8th line
  is the real vault-properties defect, which is also present in the copy.
- **Base:** only H0 fires, for the 17 entries that had no metadata. The 4
  round-20 entries pass H1 through the live-opened class.

### Predicate script

This is the exact predicate that produced the results above. It was run from
`/tmp`, which has since been deleted. Paste it into a file to re-run:
`python3 <file> /home/vgpnk/Projects/shokunin/kake-shokunin`.

```python
#!/usr/bin/env python3
import re, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]); BASE = sys.argv[2] if len(sys.argv) > 2 else "5009ecaa"
LANE = Path("/home/vgpnk/Projects/shokunin/kake-shokunin")
ROUND_OPEN = "2026-10-20"; PRUNE = "2026-10-12"
DATE = re.compile(r"20\d\d-\d\d-\d\d")
NEG = re.compile(r"(?i)\bnot (?:a )?(?:live[- ]?)?(?:\S+ )?(?:domain )?re-?(?:check|verif)|\bnot a 20\d\d-\d\d-\d\d\b|historical[- ,]+not[- ]live")
CLASS_HIST = re.compile(r"(?i)historical[-, ]+not[- ]live[- ]re-?verified")
LIVE = re.compile(r"(?i)\b(re-?verified (?:today|this round|live)|live[- ]re-?verified|confirmed (?:today|now|live)|checked today|currently (?:holds|verified)|verified live)\b")
OBS = re.compile(r"(?i)\b(read|run|ran|observ\w*|verif\w*|baseline|fetch\w*|GET|captur\w*|probe\w*|re-read|snapshot|swept|sweep|audit\w*|measured|grep\w*|commit|recorded|checked|opened|round|r\d+)\b")
ABS = re.compile(r"(?i)\b(absent|vanished|gone|removed)\b")
def git(*a): return subprocess.run(["git", "-C", str(LANE), *a], capture_output=True, text=True).stdout
src_rows = {}
for l in (root / "corpus/SOURCES.md").read_text().splitlines():
    m = re.match(r"\| (S\d{3}) \|", l)
    if m: src_rows[m.group(1)] = [x.strip() for x in l.split("|")][9]
viol = []
for p in sorted((root / "corpus/knowledge").glob("*.md")):
    name = p.name; head = {}
    for l in p.read_text().splitlines()[:8]:
        m = re.match(r"^(source|verified-at|recheck):\s*(\S.*)$", l)
        if m: head[m.group(1)] = m.group(2)
    if len(head) < 3: viol.append((name, "H0", "trio incomplete in first 8 lines")); continue
    v = head["verified-at"]; base = git("show", f"{BASE}:corpus/knowledge/{name}")
    dates = DATE.findall(v); first = dates[0] if dates else None
    ids = [i for i in re.findall(r"\bS\d{3}\b", head["source"].split("Metadata authority")[0].split("metadata contract")[0]) if i != "S019"]
    live_ok = bool(ids) and first and all(src_rows.get(i) == first for i in ids) and not CLASS_HIST.search(v)
    if not CLASS_HIST.search(v) and not live_ok: viol.append((name, "H1", "no historical token and not live-opened class"))
    for d in dates:
        if d >= ROUND_OPEN:
            ctx = v[max(0, v.find(d) - 30): v.find(d) + 10]
            if not re.search(r"(?i)not a\s*$|not a " + d, ctx): viol.append((name, "H2", f"date {d} >= round-21 open outside negation"))
    if not first and not re.search(r"\b[0-9a-f]{7,40}\b", v): viol.append((name, "H2", "no date and no revision"))
    cdates = set(git("log", "--format=%cs", BASE, "--", f"corpus/knowledge/{name}").split())
    for h in re.findall(r"\b[0-9a-f]{7,40}\b", v): cdates |= set(git("log", "-1", "--format=%cs", h, "--").split())
    for d in set(dates):
        if d >= ROUND_OPEN or d in base or d[5:] in base or d in cdates: continue
        viol.append((name, "H3", f"date {d} not in entry base bytes or its commit dates"))
    for h in re.findall(r"\b(?=[0-9a-f]*[a-f])(?=[0-9a-f]*\d)[0-9a-f]{7,40}\b", v):
        if subprocess.run(["git", "-C", str(LANE), "cat-file", "-e", h + "^{commit}"], capture_output=True).returncode: continue
        for lit in re.findall(r"\+?\d+B\b|\b\d+ rows\b|\b\d+ events\b", v):
            intro = git("log", "--reverse", "--format=%h", f"-S{lit}", BASE, "--", f"corpus/knowledge/{name}").split()
            if intro and not h.startswith(intro[0][:7]) and not intro[0].startswith(h[:7]):
                viol.append((name, "H3b", f"commit {h} credited, but literal '{lit}' was introduced by {intro[0]}"))
    if CLASS_HIST.search(v) and ABS.search(base) and first and first > PRUNE and name != "freshness-sweep.md":
        viol.append((name, "H4", f"first verified-at {first} after {PRUNE} prune while sources are annotated absent"))
    if first and first < ROUND_OPEN and (first in base or first[5:] in base):
        obs = [l for l in base.splitlines() if (first in l or first[5:] in l) and OBS.search(l) and not re.search(r"(?i)embedded max date|mtime|updatedAt|lastmod|vintage", l)]
        if not obs and first not in cdates: viol.append((name, "H5", f"first date {first} appears only as content/vintage date"))
    for m in LIVE.finditer(v):
        if not NEG.search(v[max(0, m.start() - 40): m.end() + 5]): viol.append((name, "H6", f"live claim '{m.group(0)}'"))
    if re.search(r"(?i)\b(returns|returned|now reads|currently|→)\b", head["recheck"]) and "expect" not in head["recheck"]:
        viol.append((name, "H7", "recheck asserts an observed result"))
for x in viol: print("FAIL", *x, sep="\t")
print(f"violations={len(viol)}"); sys.exit(1 if viol else 0)
```

**Smallest correction (acceptance).** Report the C1 claim as "provenance
coverage 4→21, of which 4 are live-opened and 17 historical", never as
"verified" or "fresh". Gate acceptance on all three of:

1. the count (21/21);
2. predicate exit 0;
3. `node scripts/freshness-sweep.mjs --section=paths --json` with `counts.newMissing == 0` and `counts.drift` not above base.

## F2 — False provenance: vault-properties credits the wrong commit (fix before integration)

The header reads: `verified-at: 2026-09-28, kake commit dd4eabf (original baseline
GETs, byte-equivalence check, +157B seed diff; …)`.

- `git log` shows the entry was **added in `ed0b632`** ("round-9: … vault
  PROPERTIES[] baseline … +157B seed/site-id findings").
- `dd4eabf` (round-10) changed exactly one line of this file, a line-pin
  `:891-894` → `:903`.
- `git log --reverse -S'+157B'` returns `ed0b632`.
- The scribe report (`w1/Knowledge21.md:18`) says it chose dd4eabf as the
  "latest commit touching the entry". The header text, however, credits it with
  the baseline.

The date (2026-09-28) is still correct. Correction, prefix-only: replace
`kake commit dd4eabf` with `kake commit ed0b632 (round-9 baseline; dd4eabf later
re-pinned one line)`.

## F3 — A new header's own line pointer is wrong after the prefix

`publish-channels.md:1` says the corrections are "cited by the round-20
corrections (lines 54-57)". After the +4 prefix, those `Base …` bullets sit at
**lines 58–61**, and lines 54–57 are the `Source:` line, blanks and a heading.
The pointer was written in base numbering. `w1/NoTrade.md` found the same thing
independently. Correction: write `58-61`, or anchor by text ("the four `Base …`
r20-correction bullets at EOF").

## F4 — C1 alone adds 4 new misses on the §paths pin

I copied base `5009ecaa`, overlaid only the working-tree `corpus/knowledge/*.md`,
and ran `node scripts/freshness-sweep.mjs --section=paths --repo <copy> --json`:

| | exit | drift | newMissing | declaredAbsent | unresolved |
|---|---|---|---|---|---|
| base | 1 | 3 | 0 | 52 | 8 |
| base + C1 headers only | 1 | 3 | **4** | 56 | 9 |
| full working tree (C1+C2) | 1 | 6 | 5 | 54 | 9 |

- The 4 misses come from C1 recheck and source lines:
  - `~/Projects/ds4cc-marketplace/render.yaml` (`publish-channels.md:3`)
  - `~/Projects/plazir-15-site/.github/workflows/pages.yml` (`publish-channels.md:3`)
  - `~/Projects/webzites/fleet` (`mirror-pitfalls.md:3`)
  - `~/Projects/webzites/state/probe-latest.json` (`drift-detection.md:3`)
- The 5th miss in the full tree, `sentinel-sourceless-extract-r9.md`, and all 3
  extra drift targets come from C2 Gate text (`round-4.md:46`, `round-9.md:179`,
  `round-17.md:64-65`).
- The new unresolved token is the glob
  `~/Projects/webzites/state/recreate-plazir15-*.json` (`fire-journal-codes.md:3`).
  It is informational only.
- At `freshness-sweep.mjs:521`, `ok = drift === 0 && newMissing === 0`. The
  selftest case at `:1269-1271` asserts exit 1 when newMissing is non-zero and
  drift is empty. So C1 is an independent exit-1 cause, and the already-red base
  hides it.

Smallest correction, with no re-pin needed: spell each recheck path as its
already-pinned ancestor. All four ancestors are confirmed in `pins.pathsMissSet`:

- `render.yaml` → `~/Projects/ds4cc-marketplace`
- `pages.yml` → `~/Projects/plazir-15-site`
- `~/Projects/webzites/fleet` → `~/Projects/webzites/fleet/kimi-surface-ops.md`
- `probe-latest.json` → `~/Projects/webzites/state`

The alternative is the re-pin to 55→60 that `w1/NoTrade.md` proposes. That is
the integrator's decision and must be reported as growth of the miss set.

## F5 — freshness-sweep's 2026-10-19 date backs a superseded "exits 0" claim

- The header says `verified-at: 2026-10-19 (round-20 citation-local correction
  and S014 run …) — historical, not live-reverified`.
- The body's "Round-20 resume note (2026-10-19)" says "the §paths run exits 0".
  The SCORECARD "Post-review ruling — round 20" already says "gate exit remains
  1". My base run today gives exit 1 with drift 3 (`w1/CurrentToolEntry.md` F1
  agrees).
- The header's recheck, `grep -cF 'function scanCitations'`, only checks that a
  function exists. It cannot catch this.

Correction, prefix-only: add "post-review §paths exit 1; the resume note's
'exits 0' is superseded (SCORECARD Post-review ruling)" to `verified-at`, and use
`node scripts/freshness-sweep.mjs --section=paths --offline` as the recheck. It
is local and read-only, and it exercises the entry's own claim.

## F6 — Recheck executability (operability)

- **kimi-subpath-audit.** The recheck is `git -C ds4cc-marketplace show
  f3d2ecd:sitemap.xml`. It depends on the working directory, and `f3d2ecd` was a
  **local unpushed** commit: `LOG.md:107` says "working-tree-only (unpushed
  `e82a262`/`f3d2ecd`)" and `LOG.md:166` says "absent from `origin/main`".
  Restoring the checkout from origin therefore cannot satisfy "restore at
  f3d2ecd". Only "retire" is reachable unless a backup exists. Correction: name
  that fact, and use `~/Projects/ds4cc-marketplace`, an already-pinned absolute
  path.
- **sitemap-orphan-audit.** The recheck greps lane prose only
  (`grep -nF 'include-hidden-files' corpus/knowledge/ghp-served-set.md
  corpus/SOURCES.md`). It cannot fail when the world changes, so it re-checks
  the correction text, not the 103-loc / 0-orphan claim. Correction: label it
  "lane-text consistency check, not a claim recheck". The operator
  restore-or-retire clause already present then carries the actual recheck.

## F7 — The first date means different things in different entries (low severity)

- **Latest partial re-verification as the first date:** drift-detection,
  ops-automation and publish-queue lead with 2026-09-29. In drift-detection, the
  r16 re-verification on 2026-09-29 covers only §"plazir15-ghp live-vs-source
  drift" (base line 67), not the whole entry.
- **Original evidence as the first date:** fleet-registry, free-read-verbs,
  probe-delta and others lead with it.
- A consumer computing staleness from the first token gets inconsistent
  semantics. The error is only about one day here, but there is no rule behind
  it.

Correction: the first date should be the claim-wide evidence date, and any later
partial re-verification should be scoped ("r16 re-verification of the plazir15
subsection 2026-09-29"). This is a convention tradeoff for L1 and QUALITY.md,
not a truth defect.

## F8 — The prefix changes line identity for inbound pointers

Pure prefixes keep every byte, but they move line addresses. Examples:

- `keeper-timer-inert.md:101` says "`corpus/knowledge/publish-queue.md:32` now
  reads 'operator config edit'". Line 32 is now PQ-8, and the PQ-12 row it means
  is now at line 36.
- `corpus/QUALITY.md:15` cites `publish-channels.md:9` for the CNAME line, which
  is now at line 13.
- `ghp-custom-domain.md:35` and `ghp-served-set.md:17` cite `publish-channels.md:5-9`
  and `:5-14`, which now include the header and title.
- The newly authored C2 Gate text has 19 refs into C1-shifted entries, written
  in **mixed numbering bases**. `round-12.md:81-82`, `round-10.md:72` and
  `round-8.md:74` use base numbering; `round-3.md:40` → `publish-queue.md:36`
  uses working-tree numbering. Neither kind is revision-bound.

`QUALITY.md` (round-21 addition) already requires "a same-byte line mapping and a
correction register". `w1/PointerRisk.md`, `w1/NoTrade.md` and
`w1/ScopeOverlap.md` cover the census. This seat only confirms that C1 is the
cause and that no gate detects it.

## Minor (no action required)

- `mirror-pitfalls.md:3` (recheck) cites "the 2026-10-12 prune" and "r18
  re-census (2026-10-14)". Both dates are true elsewhere in the lane but appear
  in no line of this entry, because the entry has no r18 annotations. The lane
  record supports them.
- `fire-journal-codes.md:2` writes 2026-09-26, which the base records as
  "09-26/09-27". It is an expansion and is grounded.

## Evidence locations

- Headers: `corpus/knowledge/*.md:1-3` (working tree), with base bodies read via
  `git show 5009ecaa:corpus/knowledge/<f>`.
- Sweep semantics: `scripts/freshness-sweep.mjs:477-479, 508, 521, 1007, 1269-1271`.
  Pins: `corpus/knowledge/freshness-pins.json` (`pathsMissSet` has 55 entries).
- SOURCES `opened` column: S001–S013 = 2026-10-19; S019 row at `corpus/SOURCES.md:27`.
- Commit facts: `ed0b632` added vault-properties; `dd4eabf` changed one line of
  it; `cd5b381` = round-1; `18537e9` = round-5 (2026-09-28); `cb807bc` = 2026-10-17;
  `02b6dd0` is the last commit touching `scripts/freshness-sweep.mjs`.

## Limitations

- The predicate checks necessary conditions only. It cannot prove that a date is
  the best honest choice, and H3b only covers literal-bearing claims.
- I read the working tree as a snapshot while peers were still writing. Lesson
  results (C2) may change.
- The sweep ran with the real `$HOME`, so its results reflect the filesystem on
  2026-10-20.
- I made no edits to targets. Corrections F2–F6 belong to the owning scribes or
  to L1.
