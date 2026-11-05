import importlib.util, sys, collections
sys.path.insert(0, "/fast/scratch/hyaku/kake-r97/CriticClaims")
from drive import *
spec = importlib.util.spec_from_file_location("c97i", W + "/c97_index.py")
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
rev = REV
readme = show("corpus/README.md")
rows = c.index_rows(readme)
names = [l.split("\t")[1].split("/")[-1] for l in sh(G, "-C", LANE, "ls-tree", rev, "corpus/knowledge/").splitlines() if l.endswith(".md")]
bod = {n: show("corpus/knowledge/" + n) for n in names}
print("md_entries", len(names), "index_rows", len(rows))
per = collections.defaultdict(list)
for cell, others, line in rows:
    for t in c.TOKEN.findall(cell):
        per[t].append((cell, others, line))
fail_rows = 0; multi = 0; failing_stale = []
for n in names:
    need = c.source_ids(bod[n]); bw = set(c.words(bod[n]))
    rs = per.get(n, [])
    if len(rs) > 1: multi += 1
    for cell, others, line in rs:
        have = c.ids_in(line)
        ow = c.words(" ".join(others))
        shared = {w for w in ow if len(w) >= c.SHARED_LEN and w in bw}
        ok = not (need - have) and len(ow) >= c.MIN_WORDS and len(shared) >= c.MIN_SHARED
        if not ok:
            fail_rows += 1; failing_stale.append((n, sorted(need - have)[:3], len(ow), len(shared), line[:90]))
print("entries_with_multiple_rows", multi, "failing_rows_still_in_readme", fail_rows)
for x in failing_stale[:50]: print(x)
noS = [n for n in names if not c.source_ids(bod[n])]
print("entries_with_no_S_ids_in_source_line_first15", len(noS), noS)
multi_tok = [cell for cell, _, _ in rows if len(c.TOKEN.findall(cell)) > 1]
print("rows_with_multiple_tokens", len(multi_tok))
