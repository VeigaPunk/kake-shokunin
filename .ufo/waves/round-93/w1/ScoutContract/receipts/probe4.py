import importlib.util, json
LANE="/home/vgpnk/Projects/shokunin/kake-shokunin"
spec=importlib.util.spec_from_file_location("c93", LANE+"/.ufo/waves/round-93/c93_conditional.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

gen=m.generate(93,120)
NOGET={"CONNECT","OPTIONS","TRACE"}
bad=[]
for idx,i in enumerate(gen):
    if i["method"] in NOGET:
        d=m.reference(i)
        if d["decision"]!="200":
            bad.append((idx,i["method"],d))
print("generated 120: cases with method in {CONNECT,OPTIONS,TRACE} whose contract decision != 200:", len(bad))
for b in bad: print("   idx=%d method=%s -> %s" % b)
print()
# same for hand cases
hb=[(c[0],c[1]["method"],c[2]) for c in m.hand_cases() if c[1]["method"] in NOGET]
print("hand cases with method in {CONNECT,OPTIONS,TRACE}:", hb)
print()
# which clause-4 refusals does RFC 5.6.1.2 require recipients to accept?
print("RFC 9110 5.6.1.2 recipient-accepted list shapes: '#element => [ element ] *( OWS \",\" OWS [ element ] )'")
for v in ['"a",, "b"','"a",','"a" , , "b"','','   ']:
    try:
        m.parse_list(v); print("   %-14r accepted by reference" % v)
    except m.Invalid as e:
        print("   %-14r REFUSED by reference (%s)" % (v,e))
print()
print("reference treats null role as invalid:", end=" ")
i={"method":"GET","current":{"exists":True,"etag":'"1"',"last_modified":500},
   "request":{"if_match":None,"if_none_match":None,"if_modified_since":None,"if_unmodified_since":None},"role":None}
try: print(m.reference(i))
except m.Invalid as e: print("REFUSED:",e)
