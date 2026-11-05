#!/usr/bin/env python3
"""Live cross-check: do the fixture findings have live instances at the base?

Read-only over the lane repo (git show / ls-tree at base). Writes nothing to
the lane; stdout goes to receipts/live-crosscheck.txt.
"""
import re
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
BASE = "10ecbd1ade91d0721e87a9942a66a2b61d5ce8d5"
ID_RE = re.compile(r"S\d{3,}")
CRIT_RE = re.compile(r"Round[- ]\d+")
PATH_RE = re.compile(r"`((?:scripts|corpus|\.ufo)/[^`\s]+)`")


def git(*a):
    p = subprocess.run(["git", "-C", LANE, *a], capture_output=True)
    assert p.returncode == 0, (a, p.stderr)
    return p.stdout.decode("utf-8", "replace")


def show(path):
    return git("show", "%s:%s" % (BASE, path))


out = []
def say(s):
    out.append(s)

# ---- E3 live: ids that resolve via non-row tokens -------------------------
sources = show("corpus/SOURCES.md")
row_ids = set(re.findall(r"(?m)^\s{0,3}\|\s*(S\d{3,})\b", sources))
all_tokens = set(ID_RE.findall(sources))
prose_only = all_tokens - row_ids
say("E3-live: SOURCES.md row-leading ids=%d, all S-tokens=%d, tokens that are NOT row ids=%d"
    % (len(row_ids), len(all_tokens), len(prose_only)))
if prose_only:
    say("  prose-only tokens (first 12): %s" % ", ".join(sorted(prose_only)[:12]))

lessons_paths = [p for p in git("ls-tree", "-r", "--name-only", BASE, "--",
                                "corpus/lessons").splitlines() if p]
entries_paths = [p for p in git("ls-tree", "-r", "--name-only", BASE, "--",
                                "corpus/knowledge").splitlines() if p.endswith(".md")]
say("E3-live: entries=%d" % len(entries_paths))
prose_cited = []
short_cited = []
for p in sorted(entries_paths):
    text = show(p)
    m = re.search(r"(?m)^source:.*$", "\n".join(text.splitlines()[:8]))
    if not m:
        continue
    ids = ID_RE.findall(m.group(0))
    if ids and all(i in prose_only for i in ids):
        prose_cited.append((p, ids))
    short = re.findall(r"(?m)^source:.*\bS\d{1,2}\b", text[:2000])
    if short and not ids:
        short_cited.append((p, short[0][:80]))
say("  entries whose ids resolve ONLY via prose tokens: %d %s"
    % (len(prose_cited), prose_cited[:6]))
say("  entries with a 1-2 digit S-id and no 3+ digit id on source: %d %s"
    % (len(short_cited), short_cited[:6]))

# ---- E2 live: Round sections outside the counted population ---------------
quality = show("corpus/QUALITY.md")
round_secs, counted_secs, uncounted = 0, 0, []
for section in re.split(r"(?m)^## ", quality)[1:]:
    head = section.splitlines()[0].strip() if section.splitlines() else ""
    if not CRIT_RE.match(head):
        continue
    round_secs += 1
    if re.search(r"criteri", section[:400], re.I):
        counted_secs += 1
    else:
        uncounted.append(head)
say("E2-live: headings matching Round[- ]digits=%d, counted by counter=%d, uncounted=%d"
    % (round_secs, counted_secs, len(uncounted)))
for h in uncounted[:8]:
    say("  uncounted: %s" % h)

# ---- E1/E4 live: Gate whitespace variants, extra Mistakes sections --------
gate_trailing, gate_other, two_mistakes = [], [], []
for p in [x for x in lessons_paths
          if re.search(r"/(round-[^/]*\.md)$", x)
          and not x.endswith("-verifier-spotcheck.md") and "aggregator" not in x]:
    text = show(p)
    if re.search(r"(?m)^## Gate[ \t]+\S*[ \t]*$", text) and \
       not re.search(r"(?m)^## Gate\s*$", text):
        gate_other.append(p)
    for m in re.finditer(r"(?m)^## Gate.*$", text):
        if m.group(0) != "## Gate":
            gate_trailing.append((p, repr(m.group(0))))
    if len(re.findall(r"(?m)^## Mistakes\s*$", text)) > 1:
        two_mistakes.append(p)
say("E1-live: lesson count considered=%d" % len([x for x in lessons_paths]))
say("  Gate lines not exactly '## Gate' (e.g. trailing ws / variants): %d %s"
    % (len(gate_trailing), gate_trailing[:6]))
say("E4-live: lessons with MORE THAN ONE '## Mistakes' heading: %d %s"
    % (len(two_mistakes), two_mistakes[:6]))

# ---- E5 live: row paths that are trees, or unbackticked path mentions -----
skill = show("SKILL.md")
rows = 0
tree_paths, unbacked = [], []
for line in skill.splitlines():
    if not line.startswith("|"):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 4:
        continue
    rows += 1
    body = " ".join(cells)
    for raw in PATH_RE.findall(body):
        raw = re.sub(r":\d+(-\d+)?$", "", raw).rstrip("`,.")
        t = subprocess.run(["git", "-C", LANE, "cat-file", "-t",
                            "%s:%s" % (BASE, raw)], capture_output=True, text=True)
        if t.returncode == 0 and t.stdout.strip() == "tree":
            tree_paths.append(raw)
    stripped = PATH_RE.sub("", body)
    for m in re.finditer(r"(?:scripts|corpus|\.ufo)/[^\s`,|]+", stripped):
        unbacked.append((m.group(0), line[:70]))
say("E5-live: SKILL rows counted=%d" % rows)
say("  row paths resolving to a TREE (directory), not a blob: %d %s"
    % (len(set(tree_paths)), sorted(set(tree_paths))[:10]))
say("  path-shaped mentions outside backticks in rows: %d %s"
    % (len(unbacked), unbacked[:6]))

print("\n".join(out))
