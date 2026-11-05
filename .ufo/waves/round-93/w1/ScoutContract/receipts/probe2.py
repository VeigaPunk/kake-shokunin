import importlib.util, json, collections
LANE="/home/vgpnk/Projects/shokunin/kake-shokunin"
spec=importlib.util.spec_from_file_location("c93", LANE+"/.ufo/waves/round-93/c93_conditional.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

cases=m.hand_cases()
print("hand_cases() length =", len(cases))
print("docstring says:", [l for l in m.__doc__.splitlines() if "hand cases" in l])

gen=m.generate(93,120)
print("generated inputs:", len(gen))
meth=collections.Counter(i["method"] for i in gen)
print("generated methods:", dict(meth))

# how many generated cases are OPTIONS with a false If-None-Match -> contract 412, RFC9110 13.2 would ignore
opts=0
for i in gen:
    if i["method"] in ("OPTIONS","TRACE","CONNECT"):
        req=i["request"]
        inm=req.get("if_none_match")
        if inm is not None:
            try:
                parsed=m.parse_list(inm)
            except m.Invalid:
                continue
            cur=i["current"]
            curtag=m.parse_etag(cur["etag"]) if cur["etag"] is not None else None
            exists=cur["exists"]
            if parsed=="*":
                hit=exists
            else:
                hit = exists and curtag is not None and any(m.weak(t,curtag) for t in parsed)
            if not hit:
                opts+=1
print("generated cases where method in OPTIONS/TRACE/CONNECT and If-None-Match is FALSE (contract says 412; RFC9110 13.2 line 6203-6207 says the server MUST ignore conditional fields for such methods):", opts)

# population coverage of the ambiguity classes
def present(pred):
    n=0
    for i in gen:
        if pred(i): n+=1
    return n
print("gen with role present:", present(lambda i: "role" in i))
print("gen with role null:", present(lambda i: i.get("role",None) is None and "role" in i))
print("gen with whitespace-only / empty precondition value:", present(lambda i: any(isinstance(v,str) and v.strip(" \t")=="" for v in i["request"].values() if isinstance(v,str))))
print("gen with empty list member (',,' or trailing ','):", present(lambda i: any(isinstance(v,str) and (",," in v or v.endswith(",")) for v in i["request"].values() if isinstance(v,str))))
print("gen with '*' padded by whitespace:", present(lambda i: any(isinstance(v,str) and v.strip(" \t")=="*" and v!="*" for v in i["request"].values() if isinstance(v,str))))
print("gen with non-ASCII in a tag:", present(lambda i: any(isinstance(v,str) and any(ord(ch)>126 for ch in v) for v in i["request"].values() if isinstance(v,str))))
print("gen with negative date:", present(lambda i: any(isinstance(v,int) and v<0 for v in i["request"].values())))

# hand case names
print("hand case names:")
print(", ".join(c[0] for c in cases))
