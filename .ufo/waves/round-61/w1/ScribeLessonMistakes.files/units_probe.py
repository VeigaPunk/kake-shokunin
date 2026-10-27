import re, sys, html
CJK_RE = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff65-\uff9f\U00020000-\U0002ffff]")
def units(t):
    return len(CJK_RE.findall(t)) + len([x for x in t.split() if not CJK_RE.search(x)])
S = "Some crawlers have more than one user agent token; you need to match only one crawler token for a rule to apply."
print("units", units(S), "chars", len(S), "tokens", len(S.split()))
path = sys.argv[1]
raw = open(path, encoding="utf-8", errors="replace").read()
text = re.sub(r"<[^>]+>", " ", raw)
text = html.unescape(text)
coll = " ".join(text.split())
print("raw substring of collapsed text:", coll.count(S))
print("also in raw bytes:", raw.count(S))
print("len collapsed", len(coll))
