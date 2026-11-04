import importlib.util, json, collections
spec = importlib.util.spec_from_file_location('c88','/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/c88_vary.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
hits = collections.Counter()
def instrumented(vary, stored, presented):
    if not isinstance(vary, str):
        hits['vary_not_str']+=1; return 'invalid'
    members=[x.strip(m.OWS) for x in vary.split(',')]
    if not members or any(x=='' for x in members):
        hits['empty_member']+=1; return 'invalid'
    names,star=[],False
    for x in members:
        if x=='*': star=True; hits['star']+=1
        elif m.is_token(x): names.append(x.lower())
        else: hits['nontoken_member']+=1; return 'invalid'
    def norm(side):
        if not isinstance(side,dict): hits['side_not_dict']+=1; return None
        out={}
        for k,v in side.items():
            if not m.is_token(k): hits['nontoken_key']+=1; return None
            low=k.lower()
            if low in out: hits['dup_key_in_side']+=1; return None
            if isinstance(v,str): out[low]=v
            elif isinstance(v,list) and v and all(isinstance(x,str) for x in v):
                out[low]=', '.join(v); hits['list_join']+=1
            else: hits['bad_value_type']+=1; return None
        return out
    a,b=norm(stored),norm(presented)
    if a is None or b is None: hits['side_invalid']+=1; return 'invalid'
    if star: hits['star_mismatch']+=1; return 'mismatch'
    for n in set(names):
        l,r=a.get(n),b.get(n)
        if l is None and r is None: hits['absent_both']+=1; continue
        if l is None or r is None: hits['absent_one']+=1; return 'mismatch'
        if l.strip(m.OWS)!=r.strip(m.OWS): hits['value_diff']+=1; return 'mismatch'
    hits['all_match']+=1; return 'match'
bad=0
for pop,c in [('frozen',x) for x in m.CASES]+[('random',x) for x in m.RANDOM_CASES]:
    got=instrumented(c['vary'],c['stored'],c['presented'])
    want=c['verdict'] if c['exit']==0 else 'invalid'
    if got!=want: bad+=1; print('DISAGREE',pop,c['id'],got,want)
print('population 220 disagreements',bad)
print(json.dumps(dict(sorted(hits.items())),indent=1))
print('UNEXERCISED:', [k for k in ('vary_not_str','empty_member','nontoken_member','star','star_mismatch','nontoken_key','dup_key_in_side','list_join','bad_value_type','absent_both','absent_one','value_diff','all_match','side_invalid') if hits[k]==0])
