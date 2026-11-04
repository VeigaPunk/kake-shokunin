import importlib.util, json, random, subprocess, sys, tempfile
from pathlib import Path
LANE=Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
spec=importlib.util.spec_from_file_location('c89_key', LANE/'.ufo/waves/round-89/c89_key.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
out={}
out['seed']=m.SEED
out['props_total']=m.PROPS_PER_CLASS*len(m.PROP_CLASSES)
cand=(LANE/'scripts/cache_key.py').read_bytes().decode()
def score(src, tag):
    r=m.score_candidate(src.encode() if isinstance(src,str) else src, Path(tempfile.mkdtemp(prefix='kake-r89-s-')), m.SEED)
    out[tag]={'frozen':r[0],'props':r[1],'refuse':r[2],'fails':r[3][:4],'guard':m.guard(src.encode() if isinstance(src,str) else src)}
score(cand,'A_integrated_candidate')
out['A_integrated_candidate']['met']= out['A_integrated_candidate']['frozen']==16 and out['A_integrated_candidate']['props']==200 and out['A_integrated_candidate']['refuse']==9
# B: URI not escaped
b=cand.replace('return _esc(uri) + ("" if not parts else US + US.join(parts))','return uri + ("" if not parts else US + US.join(parts))')
score(b,'B_uri_not_escaped')
# C: whitespace trim widened beyond SP/HTAB
c=cand.replace('OWS = " \\t"','OWS = " \\t\\n\\v\\f\\r"')
assert c!=cand
score(c,'C_trims_beyond_SP_HTAB')
# D: runtime-built import of the committed reference
d='''#!/usr/bin/env python3
import importlib.util, json, sys
p = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-89/" + "c89" + "_key.py"
spec = importlib.util.spec_from_file_location("ref", p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
obj = json.load(sys.stdin)
try:
    print(json.dumps({"key": mod.key_of(obj)}))
except mod.Invalid as e:
    print("invalid_input: " + str(e), file=sys.stderr); sys.exit(1)
'''
score(d,'D_runtime_built_reference_import')
# E: table over the committed seed population + frozen + refusals
TBL={}
def add(p):
    k=json.dumps(p,sort_keys=True)
    if k in TBL: return
    try: TBL[k]=('key', m.key_of(p))
    except m.Invalid as e: TBL[k]=('refuse', str(e))
for c_ in m.FROZEN: add(c_[1])
rng=random.Random(m.SEED)
for cls in m.PROP_CLASSES:
    for _ in range(m.PROPS_PER_CLASS):
        for label,l,r_,rel in m._props(rng):
            if label==cls: add(l); add(r_); break
for label,payload,want in m.REFUSALS: add(payload)
src=('\n'.join(['#!/usr/bin/env python3','import json, sys','T = '+repr(TBL),
 'obj = json.load(sys.stdin)','k = json.dumps(obj, sort_keys=True)',
 'if k not in T:','    print("invalid_input: unknown", file=sys.stderr); sys.exit(1)',
 'kind, val = T[k]','if kind == "key":','    print(json.dumps({"key": val})); sys.exit(0)',
 'print("invalid_input: " + val, file=sys.stderr); sys.exit(1)'])).encode()
score(src,'E_table_over_committed_seed_population')
out['E_table_over_committed_seed_population']['table_entries']=len(TBL)
# collision demo for B
def run(source,payload):
    dd=Path(tempfile.mkdtemp(prefix='kake-r89-run-')); p=dd/'c.py'; p.write_bytes(source.encode())
    q=subprocess.run([sys.executable,'-B',str(p)],input=json.dumps(payload),capture_output=True,text=True)
    return q.stdout.strip()
R1={'uri':'https://e.test/a','request_headers':{'b':'x'},'vary':'b'}
R2={'uri':'https://e.test/a\x1fb\x1ex','request_headers':{},'vary':''}
out['collision_demo']={
 'canonical_R1':run(cand,R1),'canonical_R2':run(cand,R2),
 'mutant_B_R1':run(b,R1),'mutant_B_R2':run(b,R2)}
Path('receipts/probes-c2.json').write_text(json.dumps(out, indent=2, ensure_ascii=False))
print(json.dumps({k:v for k,v in out.items() if k!='collision_demo'}, indent=2)[:2500])
print('collision:', json.dumps(out['collision_demo'], ensure_ascii=False))
