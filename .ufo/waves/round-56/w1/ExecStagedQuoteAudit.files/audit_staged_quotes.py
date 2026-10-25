#!/usr/bin/env python3
# ExecStagedQuoteAudit (round-56 W1, read-only): staged entries vs retained bodies.
import re, subprocess
SRC = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-56/sources"
KNW = "/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge"
IDS = ("S367", "S419", "S420")
CJK = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff65-\uff9f\U00020000-\U0002ffff]")
PAIRS = (("yahoo-japan-link-target-crawl-restriction.md", "S367"),
         ("yahoo-japan-deleted-url-recrawl.md", "S419"),
         ("yahoo-japan-soft-404-recrawl.md", "S420"))

def units(t):                      # the counter's rule: 1 per CJK char, 1 per non-CJK whitespace token
    return len(CJK.findall(t)) + len([w for w in t.split() if not CJK.search(w)])

def body(sid):
    return open(f"{SRC}/{sid}.html", encoding="utf-8", newline="").read()

def window(t):                     # first <h2> .. 個別リンクURL widget
    lo, hi, h2 = t.find("更新日"), t.find("個別リンクURL"), t.find("<h2")
    return (h2, hi) if min(lo, hi, h2) >= 0 and hi > lo else None

def in_content(t, s):
    w = window(t); i = t.find(s)
    while i >= 0:
        if w[0] <= i < w[1]: return True
        i = t.find(s, i + 1)
    return False

def norm(s):                       # diagnostic only: decode the 4 entities the bodies carry, drop whitespace
    for a, b in (("&quot;", '"'), ("&lt;", "<"), ("&gt;", ">"), ("&amp;", "&")): s = s.replace(a, b)
    return re.sub(r"\s+", "", s)

def grep_count(pat, path):
    p = subprocess.run(["grep", "-F", "-c", "--", pat, path], capture_output=True, text=True)
    return p.stdout.strip(), p.returncode

rows = []
for fname, sid in PAIRS:
    md, t = open(f"{KNW}/{fname}", encoding="utf-8").read(), body(sid)
    others = [body(k) for k in IDS if k != sid]
    print(f"\n=== {fname} -> body {sid} ({len(t)} chars)")
    spans = [m.group(1) for m in re.finditer(r'"([^"]*)"', md)]
    print(f"double-quoted spans found: {len(spans)} (all listed; >=2u is the audited set)")
    for s in spans:
        u, raw, w = units(s), s in t, window(t)
        r = {"file": fname, "body": sid, "span": s, "units": u, "raw": raw,
             "in_article": in_content(t, s) if raw else False, "count": t.count(s),
             "count_article": t[w[0]:w[1]].count(s), "over25": u > 25,
             "unique": raw and t.count(s) == 1 and not any(s in o for o in others),
             "norm_hit": norm(s) in norm(t)}
        rows.append(r)
        print(f"  Q units={u:<3} raw={'yes' if raw else 'no ':<3} in_article={'yes' if r['in_article'] else 'no ':<3}"
              f" count={r['count']} (article {r['count_article']}) unique={'yes' if r['unique'] else 'no ':<3}"
              f" over25={'yes' if r['over25'] else 'no ':<3} norm_hit={'yes' if r['norm_hit'] else 'no'} | {s!r}")
    rec = [l for l in md.splitlines() if l.startswith("recheck:")][0]
    m = re.search(r"grep -F -c '([^']*)'", rec)
    pat = m.group(1)
    cnt, rc = grep_count(pat, f"{SRC}/{sid}.html")
    print(f"  RECHECK grep -F -c units={units(pat)} raw={'yes' if pat in t else 'no'} count={cnt} rc={rc}"
          f" over25={'yes' if units(pat) > 25 else 'no'} | {pat!r}")
    src = [l for l in md.splitlines() if l.startswith("source:")][0]
    sect = src.split("§ ", 1)[1].split(" (更新日", 1)[0]
    print(f"  SOURCE label section: {sect!r}")
    print(f"    raw count={t.count(sect)}  whitespace-stripped count={norm(t).count(norm(sect))}")
    for seg in [x for x in sect.split(" → ") if x.strip()]:
        print(f"    segment {seg!r}: raw={t.count(seg)} norm={norm(t).count(norm(seg))}")
    print(f"    url {re.search(r'(https?://\S+)', src).group(1)} in body={'yes' if re.search(r'(https?://\S+)', src).group(1) in t else 'no'}")

aud = [r for r in rows if r["units"] >= 2]
print("\n=== SUMMARY")
print(f"spans_total={len(rows)} spans_audited(>=2u)={len(aud)} over25={sum(r['over25'] for r in aud)}"
      f" non_substring={sum(not r['raw'] for r in aud)} not_in_article={sum(r['raw'] and not r['in_article'] for r in aud)}"
      f" not_page_unique={sum(not r['unique'] for r in aud)}")
for r in aud:
    if r["over25"] or not r["raw"]:
        print(f"  FLAG {r['body']} units={r['units']} over25={r['over25']} raw={r['raw']} | {r['span']!r}")
