import sys
src="/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-90/L1/src/"
Q=[("lesson S466","rfc9110.txt",1606,1607,"Field values containing CR, LF, or NUL characters are invalid and dangerous"),
("lesson S467a","rfc9111.txt",252,252,"and is composed from, at a minimum, the request method and target URI"),
("lesson S467b","rfc9111.txt",258,261,"Caches differentiate these responses by incorporating some of the original request's header fields into the cache key as well"),
("lesson S468a","rfc8259.txt",485,486,"JSON text exchanged between systems that are not part of a closed ecosystem MUST be encoded using UTF-8"),
("lesson S468b","rfc8259.txt",429,431,"the characters that MUST be escaped: quotation mark, reverse solidus, and the control characters (U+0000 through U+001F)"),
("lesson reject2 tchar %","rfc9110.txt",1735,1737,'"%"'),
("knowledge S466","rfc9110.txt",1606,1609,"Field values containing CR, LF, or NUL characters are invalid and dangerous"),
("knowledge S467","rfc9111.txt",251,251,'The "cache key" is the information a cache uses to choose a response'),
("knowledge S468","rfc8259.txt",485,486,"JSON text exchanged between systems that are not part of a closed ecosystem MUST be encoded using UTF-8")]
for name,f,a,b,q in Q:
    lines=open(src+f,encoding="utf-8").read().split("\n")
    span=" ".join(" ".join(lines[a-1:b]).split())
    nq=" ".join(q.split())
    # minimal line range actually containing quote
    best=None
    for j in range(len(lines)):
        for i in range(j,max(-1,j-6),-1):
            if nq in " ".join(" ".join(lines[i:j+1]).split()):
                best=(i+1,j+1);break
        if best: break
    print(f"{name}: words={len(q.split())} in_stated_range={nq in span} stated={a}-{b} minimal={best[0]}-{best[1] if best else None} range_exact={best==(a,b)}")
