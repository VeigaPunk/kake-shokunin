import importlib.util, json
LANE="/home/vgpnk/Projects/shokunin/kake-shokunin"
spec=importlib.util.spec_from_file_location("c93", LANE+"/.ufo/waves/round-93/c93_conditional.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
cases=m.hand_cases()
print("ALL 44 HAND CASE NAMES:")
for i,c in enumerate(cases): print("  %2d %s" % (i+1,c[0]))
print()
print("cases mentioning options/trace/connect:", [c[0] for c in cases if c[1].get("method") in ("OPTIONS","TRACE","CONNECT")])
print("cases with role=cache:", [c[0] for c in cases if c[1].get("role")=="cache"])
print("cases whose expected is None (refusals):", [c[0] for c in cases if c[2] is None])
print()
def probe(label, inp):
    try: out=json.dumps(m.reference(inp), sort_keys=True)
    except m.Invalid as e: out="REFUSED: %s"%e
    print("%-56s -> %s"%(label,out))
def R(method,exists,etag,lm,im=None,inm=None,ims=None,ius=None,role=None):
    i={"method":method,"current":{"exists":exists,"etag":etag,"last_modified":lm},
       "request":{"if_match":im,"if_none_match":inm,"if_modified_since":ims,"if_unmodified_since":ius}}
    if role is not None: i["role"]=role
    return i
print("== A6 label: passed precondition then 200 ==")
probe("A6  im='\"1\"' matches, inm='\"2\"' no match -> label?", R("PUT",True,'"1"',500,im='"1"',inm='"2"'))
print("== A13 role=null vs role=proxy ==")
i=R("GET",True,'"1"',500); i["role"]=None; probe("A13a role=null", i)
i=R("GET",True,'"1"',500); i["role"]="proxy"; probe("A13b role='proxy'", i)
print("== A20 OPTIONS/TRACE/CONNECT ==")
probe("A20a OPTIONS inm='\"1\"' matches -> contract 412", R("OPTIONS",True,'"1"',500,inm='"1"'))
probe("A20b TRACE   inm='\"1\"' matches -> contract 412", R("TRACE",True,'"1"',500,inm='"1"'))
probe("A20c CONNECT im='\"2\"' no match -> contract 412", R("CONNECT",True,'"1"',500,im='"2"'))
print("== A21 malformed current.etag scope of clause 3 ==")
probe("A21a current.etag='unquoted', inm='\"x\"'", R("GET",True,"unquoted",500,inm='"x"'))
print("== A24 padded star / padded tag ==")
probe("A24a im=' * ' exists=true", R("PUT",True,None,None,im=" * "))
probe("A24b im=' \"1\" ' exists=true (strong match)", R("PUT",True,'"1"',500,im=' "1" '))
probe("A24c im='* ' exists=false", R("PUT",False,None,None,im="* "))
print("== A26 empty list member per RFC 5.6.1.2 ==")
probe("A26a inm='\"a\",, \"b\"'", R("GET",True,'"1"',500,inm='"a",, "b"'))
probe("A26b im='\"a\",' ", R("PUT",True,'"1"',500,im='"a",'))
print("== A27 empty field value ==")
probe("A27a im='' (If-Match empty)", R("PUT",True,'"1"',500,im=""))
probe("A27b inm='' (If-None-Match empty)", R("GET",True,'"1"',500,inm=""))
print("== A28 negative epoch (pre-1970 legal IMF-fixdate) ==")
probe("A28a ims=-2208988800 (1900-01-01)", R("GET",True,None,500,ims=-2208988800))
probe("A28b ius=-2208988800", R("PUT",True,None,500,ius=-2208988800))
print("== A29 obs-text in etag per RFC 8.8.3 etagc ==")
probe("A29a current.etag='\"a\\u0080b\"' (obs-text)", R("GET",True,'"ab"',500,inm='"ab"'))
probe("A29b current.etag='\"a\\u00e9b\"'", R("GET",True,'"aéb"',500,inm='"aéb"'))
