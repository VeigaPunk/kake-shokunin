import importlib.util, os, re
W="/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58"
spec=importlib.util.spec_from_file_location("c58qt", os.path.join(W,"c58_quote_truth.py"))
qt=importlib.util.module_from_spec(spec); spec.loader.exec_module(qt)
t=open('/fast/scratch/hyaku/kake-r58/ExecSourceLive/live_2855.html',encoding='utf-8').read()
lo=t.find('class="article-info"'); hi=t.find('推荐阅读',lo+1)
chunk=re.sub(r"(?is)<(style|script)\b.*?</\1>","<>",t[lo:hi])
segs=re.findall(r">([^<>]+)(?=<)",chunk)
print("lo,hi",lo,hi,"nodes",len(segs))
for s in segs:
    s=s.strip()
    if s: print(f"{qt.units(s):3d}u {len(s):3d}c {s}")
