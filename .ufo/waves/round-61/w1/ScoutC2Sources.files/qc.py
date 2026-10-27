#!/usr/bin/env python3
"""Replicates c61_recheck_pins.py quote semantics exactly (body_nodes / units / span_hits)."""
import re
SOURCES="/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/sources"
CJK_RE=re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff65-\uff9f\U00020000-\U0002ffff]")
TAG_CLOSE=re.compile(r"</[a-zA-Z][^>]{0,120}>")
CHROME=re.compile(r"(?is)<(script|style|noscript|svg|template|head|nav|aside|header|footer|form)\b.*?</\1\s*>")
COMMENT=re.compile(r"(?is)<!--.*?-->")
INLINE=re.compile(r"(?is)</?(?:a|abbr|b|bdi|bdo|cite|code|del|em|i|ins|kbd|mark|q|s|samp|small|span|strong|sub|sup|u|var)\b[^>]*>")
UNIT_FLOOR=6; CHAR_CEILING=160; UNIT_CEILING=25

def load(sid): return open(f"{SOURCES}/{sid}.html","rb").read()
def units(t): return len(CJK_RE.findall(t))+len([x for x in t.split() if not CJK_RE.search(x)])
def body_nodes(raw):
    text=raw.decode("utf-8","replace")
    if TAG_CLOSE.search(text):
        chunk=COMMENT.sub(" ",text); chunk=CHROME.sub(" ",chunk)
        nodes=re.findall(r">([^<>]+)(?=<)",chunk)
    else:
        nodes=re.split(r"\n[ \t]*\n",text)
    return [re.sub(r"\s+"," ",n).strip() for n in nodes if n.strip()]
def flat(raw):
    text=raw.decode("utf-8","replace")
    if not TAG_CLOSE.search(text): return body_nodes(raw)
    chunk=INLINE.sub("",CHROME.sub(" ",COMMENT.sub(" ",text)))
    return [re.sub(r"\s+"," ",n).strip() for n in re.findall(r">([^<>]+)(?=<)",chunk) if n.strip()]
def hits(span,nodes): return [i for i,n in enumerate(nodes) if span in n]
def status(sid,span):
    raw=load(sid); nodes=body_nodes(raw); h=hits(span,nodes)
    occ=len(h); u=units(span); c=len(span)
    verdict="OK" if (occ==1 and UNIT_FLOOR<=u<=UNIT_CEILING and c<=CHAR_CEILING and span.isascii()) else "FAIL"
    flags=[]
    if occ==0:
        if hits(span,flat(raw)): flags.append("crosses-inline-markup")
        else: flags.append("not-in-any-node")
    elif occ>1: flags.append(f"not-page-unique:{occ}nodes")
    if not(UNIT_FLOOR<=u<=UNIT_CEILING): flags.append(f"units={u}")
    if c>CHAR_CEILING: flags.append(f"chars={c}")
    if not span.isascii(): flags.append("non-ascii")
    return dict(sid=sid,verdict=verdict,units=u,chars=c,node_hits=occ,flags=flags,span=span)

if __name__=="__main__":
    import json,sys
    if sys.argv[1]=="check":
        print(json.dumps(status(sys.argv[2],sys.argv[3]),ensure_ascii=False,indent=1))
