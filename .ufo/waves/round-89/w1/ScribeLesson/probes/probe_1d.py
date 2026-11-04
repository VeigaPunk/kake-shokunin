import importlib.util, json, tempfile
from pathlib import Path
LANE=Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
spec=importlib.util.spec_from_file_location('c89_key', LANE/'.ufo/waves/round-89/c89_key.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
cand=(LANE/'scripts/cache_key.py').read_bytes().decode()
mut=cand.replace('    ("\\x1d", "%1D"),\n','')
assert mut!=cand, 'anchor missing'
r=m.score_candidate(mut.encode(), Path(tempfile.mkdtemp(prefix='kake-r89-1d-')), m.SEED)
print('omit %1D escape:', r[:3], 'fails', r[3][:3])
# does any frozen case or property input contain U+001D?
import re
src=LANE/'.ufo/waves/round-89/c89_key.py'
txt=src.read_text()
print('U+001D in counter source:', '\x1d' in txt)
import json as J
cs=J.load(open(LANE/'.ufo/waves/round-89/frozen/c2-cases.json'))
print('U+001D in frozen cases:', any('\x1d' in J.dumps(c) for c in cs))
print('contract names %1D:', '%1D' in (LANE/'.ufo/waves/round-89/c2-contract.md').read_text())
