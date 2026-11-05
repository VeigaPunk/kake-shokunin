import importlib.util, json, sys
LANE="/home/vgpnk/Projects/shokunin/kake-shokunin"
spec=importlib.util.spec_from_file_location("c93", LANE+"/.ufo/waves/round-93/c93_conditional.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def probe(label, inp):
    try:
        out = m.reference(inp)
    except m.Invalid as e:
        out = "REFUSED: %s" % e
    print("%-58s -> %s" % (label, json.dumps(out, sort_keys=True) if not isinstance(out,str) else out))

def R(method, exists, etag, lm, im=None, inm=None, ims=None, ius=None, role=None):
    i={"method":method,"current":{"exists":exists,"etag":etag,"last_modified":lm},
       "request":{"if_match":im,"if_none_match":inm,"if_modified_since":ims,"if_unmodified_since":ius}}
    if role: i["role"]=role
    return i

print("== A1/A2 cache-role semantics ==")
probe("A1 cache POST inm=* exists=true (RFC9111 MUST NOT evaluate)", R("POST",True,'"1"',500,inm="*",role="cache"))
probe("A1b origin POST inm=* exists=true", R("POST",True,'"1"',500,inm="*"))
probe("A2 cache GET ims=500 lastmod=null (RFC9111 Date fallback)", R("GET",True,None,None,ims=500,role="cache"))
probe("A2b origin GET ims=500 lastmod=null", R("GET",True,None,None,ims=500))
probe("A2c cache GET inm='\"1\"' etag='\"1\"' exists=true (304 vs serve stored)", R("GET",True,'"1"',500,inm='"1"',role="cache"))

print("== A3 whitespace around the star ==")
probe("A3 if_match=' * ' (strip->star?)", R("PUT",True,None,None,im=" * "))
probe("A3b if_match='*' exists=true", R("PUT",True,None,None,im="*"))
probe("A3c if_match=' \"1\" ' exists=false", R("PUT",False,None,None,im=' "1" '))

print("== A4 empty list members (RFC9110 5.6.1.2 MUST accept) ==")
probe("A4 if_none_match='\"a\",, \"b\"'", R("GET",True,'"1"',500,inm='"a",, "b"'))
probe("A4b if_none_match='\"a\",' (trailing empty)", R("GET",True,'"1"',500,inm='"a",'))
probe("A4c if_none_match='\"a\" , , \"b\"'", R("GET",True,'"1"',500,inm='"a" , , "b"'))

print("== A5 empty whole value ==")
probe("A5 if_match='' (empty string)", R("PUT",True,'"1"',500,im=""))
probe("A5b if_match=' ' (whitespace only)", R("PUT",True,'"1"',500,im=" "))

print("== A6 precondition label on 200 after a passed precondition ==")
probe("A6 if_match ok + inm no-match -> 200 label?", R("PUT",True,'"1"',500,im='"1"',inm='"2"'))
probe("A6b if_match no-match -> 412", R("PUT",True,'"1"',500,im='"2"'))

print("== A12 role=null ==")
probe("A12 role=null", R("PUT",True,'"1"',500,im='"2"',role=None) if False else None)
i=R("PUT",True,'"1"',500,im='"2"'); i["role"]=None
probe("A12 role=null (explicit)", i)
probe("A12b role absent", R("PUT",True,'"1"',500,im='"2"'))

print("== A20 options/trace: RFC9110 13.2 MUST ignore ==")
probe("A20 method=OPTIONS inm='\"1\"' (RFC: ignore -> 200)", R("OPTIONS",True,'"1"',500,inm='"1"'))
probe("A20b method=TRACE inm='\"1\"'", R("TRACE",True,'"1"',500,inm='"1"'))
probe("A20c method=CONNECT im='\"2\"'", R("CONNECT",True,'"1"',500,im='"2"'))

print("== obs-text / etagc vs RFC 8.8.3 (%x21 / %x23-7E / obs-text) ==")
probe("A21 etag with U+0080 obs-text", R("GET",True,'"ab"',500,inm='"ab"'))
probe("A21b etag with U+00E9", R("GET",True,'"aéb"',500,inm='"aéb"'))

print("== negative epoch date (pre-1970 HTTP-date) ==")
probe("A22 if_modified_since=-1", R("GET",True,None,500,ims=-1))
probe("A22b last_modified=-1", R("GET",True,None,-1,ims=500))
