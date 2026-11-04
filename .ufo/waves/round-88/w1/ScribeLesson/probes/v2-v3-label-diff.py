import importlib.util, json
spec = importlib.util.spec_from_file_location('c88vary', '/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/c88_vary.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for cid in ('r53','r150','r193'):
    c = [x for x in m.RANDOM_CASES if x['id']==cid][0]
    print(cid, json.dumps(c, sort_keys=True))
    print('  reference ->', m.reference(c['vary'], c['stored'], c['presented']), 'expected', c['verdict'])
