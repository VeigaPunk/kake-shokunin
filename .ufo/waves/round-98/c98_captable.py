#!/usr/bin/env python3
"""c98_captable.py — round-98 C1 calibration counter (kake).

Surface: the `## Capabilities` table of the lane's SCORECARD.md (the lane's
self-assessment of what it can do) against the non-author closure record:
every `capabilities_added` entry of an ADMITTED kake closure in the fleet
MANIFEST.json (rounds < 98).

Both sides are read from committed bytes only, through /usr/bin/git with
GIT_NO_REPLACE_OBJECTS=1:
  lane  : git -C <root>  show <revision>:SCORECARD.md
  fleet : git -C <fleet> show <fleet-revision>:MANIFEST.json

Population E (entries): one per (round, text) of an admitted kake closure
(`type == closure`, `lane == kake`, admitted true, int(lane_round) < 98).
Rows R: data rows of the first GFM table, outside code fences, after the
exact heading `## Capabilities`, whose header's first cell is `Capability`
and that has >= 4 cells (Capability | What | Evidence | First-working round).

An entry e and a row r are COMPATIBLE iff all hold:
  K  key(e) == key(r.cell0), or the shorter key has >= 3 words and is a
     word-prefix of the longer one. key() lowercases, cuts at the first of
     ' (', ': ', ' - ', ' — ', '; ', collapses whitespace, strips '.,'.
  N  the first integer in r's last cell equals e's round.
  W  r.cell1 (what it can now do) has >= 8 words.
  P  r.cell2 (evidence) names, in backticks, >= 1 path that exists at the
     lane revision (`git cat-file -e REV:path`; the token's first
     whitespace-separated word, trailing ':' or ',' stripped).
  S  every `scripts/<name>.<py|mjs|sh>` and `.ufo/waves/round-N/<x>.py`
     path named in e's text appears somewhere in r's line.
A maximum one-to-one matching is taken (one row backs at most one entry).
  unlisted = entries left unmatched   (admitted capability, no row)
  unbacked = rows left unmatched      (row, no admitted capability)
  mismatches = unlisted + unbacked

Output line 1: `entries=E rows=R matched=M unlisted=U unbacked=B
mismatches=X met=<true|false>`; line 2: JSON detail. Exit 0 met
(X == 0 and E > 0), 1 not met, 2 setup error (missing heading/table, empty
population, git failure). `--selftest` runs the in-memory core fixtures.
Known limit (declared before data): a row whose name, round, word count and
an existing evidence path are right but whose prose is junk passes the
counter; the frozen predicate therefore carries a row-review conjunct.
"""
import argparse, json, os, re, subprocess, sys

GIT = "/usr/bin/git"
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1", LC_ALL="C")
ROUND_CAP = 98


def git(repo, *args, check=True):
    p = subprocess.run([GIT, "-C", repo, *args], capture_output=True, env=ENV)
    if check and p.returncode != 0:
        raise SystemExit(f"setup: git {' '.join(args)} failed rc={p.returncode}: "
                         f"{p.stderr.decode(errors='replace').strip()}")
    return p


CUTS = (" (", ": ", " - ", " — ", "; ")


def key(s):
    s = s.strip().lower()
    cut = len(s)
    for c in CUTS:
        i = s.find(c)
        if i != -1:
            cut = min(cut, i)
    s = re.sub(r"\s+", " ", s[:cut]).strip().strip(".,").strip()
    return s


def key_ok(a, b):
    if not a or not b:
        return False
    if a == b:
        return True
    wa, wb = a.split(" "), b.split(" ")
    short, long_ = (wa, wb) if len(wa) <= len(wb) else (wb, wa)
    return len(short) >= 3 and long_[:len(short)] == short


def split_cells(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    cells, cur, i = [], "", 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s) and s[i + 1] == "|":
            cur += "|"; i += 2; continue
        if ch == "|":
            cells.append(cur.strip()); cur = ""; i += 1; continue
        cur += ch; i += 1
    cells.append(cur.strip())
    return cells


def table_rows(text):
    """Return (rows, error). rows: list of (lineno, line, cells)."""
    lines = text.splitlines()
    fence = None
    head = None
    for i, l in enumerate(lines):
        m = re.match(r"^ {0,3}(`{3,}|~{3,})", l)
        if m:
            tok = m.group(1)
            if fence is None:
                fence = tok[0] * len(tok)
            elif tok[0] == fence[0] and len(tok) >= len(fence):
                fence = None
            continue
        if fence is None and l.rstrip() == "## Capabilities":
            head = i
            break
    if head is None:
        return None, "no `## Capabilities` heading outside fences"
    i = head + 1
    fence = None
    while i < len(lines):
        l = lines[i]
        if re.match(r"^#{1,2} ", l) and fence is None:
            return None, "no Capability table before next section"
        m = re.match(r"^ {0,3}(`{3,}|~{3,})", l)
        if m:
            tok = m.group(1)
            if fence is None:
                fence = tok[0] * len(tok)
            elif tok[0] == fence[0] and len(tok) >= len(fence):
                fence = None
            i += 1
            continue
        if fence is None and l.startswith("|"):
            hdr = split_cells(l)
            if len(hdr) >= 4 and hdr[0] == "Capability" and i + 1 < len(lines) \
                    and re.match(r"^\|\s*:?-{3,}", lines[i + 1]):
                rows = []
                j = i + 2
                while j < len(lines) and lines[j].startswith("|"):
                    rows.append((j + 1, lines[j], split_cells(lines[j])))
                    j += 1
                return rows, None
        i += 1
    return None, "no Capability table"


def entry_paths(text):
    return sorted(set(re.findall(r"scripts/[\w.\-]+\.(?:py|mjs|sh)", text)) |
                  set(re.findall(r"\.ufo/waves/round-\d+/[\w.\-/]+\.py", text)))


def evidence_paths(cell):
    out = []
    for tok in re.findall(r"`([^`]+)`", cell):
        w = tok.strip().split()
        if not w:
            continue
        p = w[0].rstrip(":,;")
        if "/" in p or re.search(r"\.(py|md|json|txt|mjs|sh|tsv)$", p):
            if p.startswith("./"):
                p = p[2:]
            out.append(p)
    return out


def first_int(cell):
    m = re.search(r"\d+", cell)
    return int(m.group(0)) if m else None


def compatible(e, row, exists):
    _, line, cells = row
    if len(cells) < 4:
        return False
    if not key_ok(key(e["text"]), key(cells[0])):
        return False
    if first_int(cells[-1]) != e["round"]:
        return False
    if len(cells[1].split()) < 8:
        return False
    if not any(exists(p) for p in evidence_paths(cells[2])):
        return False
    for p in entry_paths(e["text"]):
        if p not in line:
            return False
    return True


def max_match(entries, rows, exists):
    adj = [[j for j, r in enumerate(rows) if compatible(e, r, exists)] for e in entries]
    match_r = [-1] * len(rows)

    def aug(i, seen):
        for j in adj[i]:
            if j in seen:
                continue
            seen.add(j)
            if match_r[j] == -1 or aug(match_r[j], seen):
                match_r[j] = i
                return True
        return False

    for i in range(len(entries)):
        aug(i, set())
    return match_r


def population(manifest):
    seen, out = set(), []
    for x in manifest.get("rounds", []):
        if x.get("lane") != "kake" or x.get("type") != "closure":
            continue
        if x.get("admitted") not in (True, "True", "true"):
            continue
        try:
            r = int(str(x.get("lane_round")))
        except ValueError:
            continue
        if r >= ROUND_CAP:
            continue
        for t in x.get("capabilities_added") or []:
            if not isinstance(t, str) or not t.strip():
                continue
            k = (r, t.strip())
            if k in seen:
                continue
            seen.add(k)
            out.append({"round": r, "text": t.strip()})
    out.sort(key=lambda e: (e["round"], e["text"]))
    return out


def score(scorecard, manifest, exists):
    entries = population(manifest)
    rows, err = table_rows(scorecard)
    if err:
        return None, err
    if not entries:
        return None, "empty population"
    match_r = max_match(entries, rows, exists)
    matched_e = {i for i in match_r if i != -1}
    unlisted = [entries[i] for i in range(len(entries)) if i not in matched_e]
    unbacked = [{"line": rows[j][0], "cell0": rows[j][2][0] if rows[j][2] else ""}
                for j in range(len(rows)) if match_r[j] == -1]
    res = {"entries": len(entries), "rows": len(rows), "matched": len(matched_e),
           "unlisted": len(unlisted), "unbacked": len(unbacked),
           "mismatches": len(unlisted) + len(unbacked),
           "unlisted_detail": [f"r{e['round']}: {e['text'][:90]}" for e in unlisted],
           "unbacked_detail": unbacked,
           "pairs": [{"line": rows[j][0], "round": entries[i]["round"],
                      "entry": entries[i]["text"][:60]}
                     for j, i in enumerate(match_r) if i != -1]}
    return res, None


def line1(res):
    met = res["mismatches"] == 0 and res["entries"] > 0
    return (f"entries={res['entries']} rows={res['rows']} matched={res['matched']} "
            f"unlisted={res['unlisted']} unbacked={res['unbacked']} "
            f"mismatches={res['mismatches']} met={'true' if met else 'false'}"), met


def selftest():
    T = "## Capabilities\n\n| Capability | What it can now do | Evidence pointer | First-working round |\n|---|---|---|---|\n"
    W = "reads a manifest and reports read-only findings offline for publishers"
    man = lambda caps: {"rounds": [{"lane": "kake", "type": "closure", "admitted": True,
                                     "lane_round": str(r), "capabilities_added": [t]}
                                    for r, t in caps]}
    ex = lambda p: p in ("scripts/a.py", "scripts/b.py", ".ufo/waves/round-9/x.txt")
    cases = []
    good = T + f"| Alpha audit | {W} | `scripts/a.py` | 5 |\n"
    cases.append(("match", good, man([(5, "Alpha audit (scripts/a.py)")]), 0))
    cases.append(("unlisted", T + "| Other thing here | " + W + " | `scripts/a.py` | 5 |\n",
                  man([(5, "Alpha audit")]), 2))
    cases.append(("wrong-round", T + f"| Alpha audit | {W} | `scripts/a.py` | 6 |\n",
                  man([(5, "Alpha audit")]), 2))
    cases.append(("few-words", T + "| Alpha audit | reads stuff | `scripts/a.py` | 5 |\n",
                  man([(5, "Alpha audit")]), 2))
    cases.append(("missing-path", T + f"| Alpha audit | {W} | `scripts/zz.py` | 5 |\n",
                  man([(5, "Alpha audit")]), 2))
    cases.append(("entry-script-not-named", T + f"| Alpha audit | {W} | `scripts/b.py` | 5 |\n",
                  man([(5, "Alpha audit (scripts/a.py)")]), 2))
    mega = T + f"| Alpha audit | {W} | `scripts/a.py` | 5 |\n"
    cases.append(("one-row-two-entries", mega,
                  man([(5, "Alpha audit"), (5, "Alpha audit: second")]), 1))
    cases.append(("prefix-3words", T + f"| GET snapshot replay tool | {W} | `scripts/a.py` | 5 |\n",
                  man([(5, "GET snapshot replay tool over twelve surfaces")]), 0))
    cases.append(("prefix-2words-refused", T + f"| GET snapshot | {W} | `scripts/a.py` | 5 |\n",
                  man([(5, "GET snapshot replay")]), 2))
    fenced = "```\n" + T + f"| Alpha audit | {W} | `scripts/a.py` | 5 |\n```\n"
    cases.append(("fenced-heading-only", fenced, man([(5, "Alpha audit")]), "err"))
    cases.append(("unbacked-row", good + f"| Beta audit | {W} | `scripts/b.py` | 7 |\n",
                  man([(5, "Alpha audit (scripts/a.py)")]), 1))
    rej = {"rounds": [{"lane": "kake", "type": "closure", "admitted": False,
                       "lane_round": "5", "capabilities_added": ["Alpha audit"]}]}
    cases.append(("rejected-not-population", good, rej, "err"))
    other = {"rounds": [{"lane": "kama", "type": "closure", "admitted": True,
                         "lane_round": "5", "capabilities_added": ["Alpha audit"]}]}
    cases.append(("other-lane-not-population", good, other, "err"))
    cap98 = man([(5, "Alpha audit (scripts/a.py)"), (98, "Future thing")])
    cases.append(("round-cap", good, cap98, 0))
    cases.append(("table-after-next-section", "## Capabilities\n\n## Other\n" + T.split("\n", 2)[2] +
                  f"| Alpha audit | {W} | `scripts/a.py` | 5 |\n", man([(5, "Alpha audit")]), "err"))
    cases.append(("second-table-ignored", good + "\nprose\n\n| Capability | a | b | c |\n|---|---|---|---|\n"
                  f"| Beta audit | {W} | `scripts/b.py` | 7 |\n",
                  man([(5, "Alpha audit (scripts/a.py)"), (7, "Beta audit")]), 1))
    ok = 0
    for name, sc, mf, want in cases:
        res, err = score(sc, mf, ex)
        got = "err" if err else res["mismatches"]
        status = "ok" if got == want else "FAIL"
        ok += status == "ok"
        print(f"{status} {name}: want={want} got={got}")
    print(f"selftest {ok}/{len(cases)}")
    return 0 if ok == len(cases) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--revision")
    ap.add_argument("--fleet", default="/home/vgpnk/Projects/shokunin")
    ap.add_argument("--fleet-revision")
    ap.add_argument("--work")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.root and a.revision and a.fleet_revision):
        print("usage: --root --revision --fleet-revision required", file=sys.stderr)
        return 2
    try:
        rev = git(a.root, "rev-parse", "--verify", a.revision + "^{commit}").stdout.decode().strip()
        frev = git(a.fleet, "rev-parse", "--verify", a.fleet_revision + "^{commit}").stdout.decode().strip()
        sc = git(a.root, "show", f"{rev}:SCORECARD.md").stdout.decode("utf-8")
        mf = json.loads(git(a.fleet, "show", f"{frev}:MANIFEST.json").stdout.decode("utf-8"))
    except SystemExit as e:
        print(f"setup-error {e}")
        return 2
    cache = {}

    def exists(p):
        if p not in cache:
            cache[p] = git(a.root, "cat-file", "-e", f"{rev}:{p}", check=False).returncode == 0
        return cache[p]

    res, err = score(sc, mf, exists)
    if err:
        print(f"setup-error {err} revision={rev} fleet-revision={frev}")
        return 2
    l1, met = line1(res)
    print(l1 + f" revision={rev} fleet-revision={frev}")
    print(json.dumps(res, ensure_ascii=False))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
