import importlib.util, json
LANE="/home/vgpnk/Projects/shokunin/kake-shokunin"
spec=importlib.util.spec_from_file_location("c93", LANE+"/.ufo/waves/round-93/c93_conditional.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def probe(label, inp):
    try: out=json.dumps(m.reference(inp), sort_keys=True)
    except m.Invalid as e: out="REFUSED: %s"%e
    print("%-58s -> %s"%(label,out))
def R(method,exists,etag,lm,im=None,inm=None,ims=None,ius=None,role=None):
    i={"method":method,"current":{"exists":exists,"etag":etag,"last_modified":lm},
       "request":{"if_match":im,"if_none_match":inm,"if_modified_since":ims,"if_unmodified_since":ius}}
    if role is not None: i["role"]=role
    return i

print("== B1 comma inside a quoted entity-tag (RFC 9110 8.8.3 etagc includes 0x2C) ==")
probe("B1a current.etag='\"a,b\"' accepted as a tag?", R("GET",True,'"a,b"',500))
probe("B1b if_match='\"a,b\"' (same tag in a list)", R("PUT",True,'"a,b"',500,im='"a,b"'))
probe("B1c if_none_match='\"a,b\"'", R("GET",True,'"a,b"',500,inm='"a,b"'))
print("== B2 semicolon and other punctuation inside a tag (legal etagc) ==")
probe("B2a current.etag='\"a;b=c\"'", R("GET",True,'"a;b=c"',500))
probe("B2b if_match='\"a;b=c\"'", R("PUT",True,'"a;b=c"',500,im='"a;b=c"'))
print("== B3 CONNECT (RFC 9110 13.2 line 6203-6207 MUST ignore) ==")
probe("B3a CONNECT im='\"z\"' mismatch", R("CONNECT",True,'"1"',500,im='"z"'))
probe("B3b CONNECT inm='\"1\"' match", R("CONNECT",True,'"1"',500,inm='"1"'))
print("== B4 cache role + POST (RFC 9111 4.3.2 line 881-885 MUST NOT evaluate) ==")
probe("B4a cache POST inm='\"1\"' match", R("POST",True,'"1"',500,inm='"1"',role="cache"))
probe("B4b cache POST im='\"z\"' mismatch (IM skipped in cache)", R("POST",True,'"1"',500,im='"z"',role="cache"))
print("== B5 cache role + IMS with no last_modified (RFC 9111 4.3.2 line 904-907 Date fallback) ==")
probe("B5a cache GET ims=500 lastmod=null", R("GET",True,None,None,ims=500,role="cache"))
print("== B6 negative epoch = pre-1970 legal IMF-fixdate ==")
probe("B6a ims=-2208988800", R("GET",True,None,500,ims=-2208988800))
probe("B6b last_modified=-2208988800", R("GET",True,None,-2208988800,ims=0))
print("== B7 obs-text inside a tag (RFC 9110 8.8.3 etagc includes obs-text) ==")
probe("B7a current.etag='\"a\\u0080b\"'", R("GET",True,'"ab"',500))
probe("B7b if_match='\"a\\u0080b\"'", R("PUT",True,'"ab"',500,im='"ab"'))
