import json, subprocess, sys, tempfile
from pathlib import Path
LANE=Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
cand=(LANE/'scripts/cache_key.py').read_bytes().decode()
mut=cand.replace('return _esc(uri) + ("" if not parts else US + US.join(parts))','return uri + ("" if not parts else US + US.join(parts))')
def run(src,payload):
    d=Path(tempfile.mkdtemp(prefix='kake-r89-coll-')); p=d/'c.py'; p.write_bytes(src.encode() if isinstance(src,str) else src)
    q=subprocess.run([sys.executable,'-B',str(p)],input=json.dumps(payload),capture_output=True,text=True)
    return q.returncode,q.stdout.strip(),q.stderr.strip()
R1={'uri':'https://e.test/a','request_headers':{'b':'x'},'vary':'b'}
R2={'uri':'https://e.test/a\x1fb\x1ex','request_headers':{},'vary':''}
for name,src in (('canonical',cand),('no-escape mutant',mut)):
    print(name)
    print('  R1:', run(src,R1))
    print('  R2:', run(src,R2))
