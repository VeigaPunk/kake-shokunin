import hashlib, json, subprocess, sys
from pathlib import Path
sys.set_int_max_str_digits(0)
script=Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecAge/cache_current_age.py')
out=Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ReviewAge')
scratch='/fast/scratch/hyaku/kake-r87/ReviewAge'
before=hashlib.sha256(script.read_bytes()).hexdigest()
keys=('apparent_age','response_delay','corrected_age_value','corrected_initial_age','resident_time','current_age')
results=[]
def check(label,payload,expected=None,raw=False):
    text=payload if raw else json.dumps(payload)
    p=subprocess.run([sys.executable,'-B',str(script)],input=text,text=True,capture_output=True,cwd=scratch,timeout=10)
    if expected is None:
        assert p.returncode==1 and not p.stdout and p.stderr.strip(),(label,p.returncode,p.stdout,p.stderr)
    else:
        actual=json.loads(p.stdout)
        assert p.returncode==0 and not p.stderr and actual==dict(zip(keys,expected)),(label,p.returncode,p.stdout[:500],p.stderr)
        assert all(type(v) is int for v in actual.values()),label
    results.append({'label':label,'exit':p.returncode,'ok':True})
check('omitted Age apparent wins',dict(date_value=4,request_time=19,response_time=26,now=39),(22,7,7,22,13,35))
check('future Date delay wins',dict(date_value=105,request_time=71,response_time=79,now=92),(0,8,8,8,13,21))
check('Age plus delay wins',dict(date_value=22,request_time=31,response_time=42,now=58,age_value=37),(20,11,48,48,16,64))
check('max tie',dict(date_value=27,request_time=31,response_time=42,now=58,age_value=4),(15,11,15,15,16,31))
check('negative Date epoch boundary',dict(date_value=-1,request_time=0,response_time=0,now=1),(1,0,0,1,1,2))
check('all zero omitted Age',dict(date_value=0,request_time=0,response_time=0,now=0),(0,0,0,0,0,0))
n=10**5000
check('5001 digit no cap',dict(date_value=-n,request_time=2,response_time=7,now=18,age_value=n+3),(n+7,5,n+8,n+8,11,n+19))
base=dict(date_value=4,request_time=19,response_time=26,now=39)
for key in base:
    check('missing '+key,{k:v for k,v in base.items() if k!=key})
for key in (*base,'age_value'):
    for bad in (None,True,False,1.0,'1',[],{}):
        check(key+' bad '+repr(bad),dict(base,**{key:bad}))
for key in ('request_time','response_time','now','age_value'):
    check(key+' negative',dict(base,**{key:-2}))
check('request after response',dict(base,request_time=27))
check('now before response',dict(base,now=25))
for text in ('','{','[]','null','true','1','{} {}','{"date_value": NaN}'):
    check('invalid document '+repr(text),text,raw=True)
after=hashlib.sha256(script.read_bytes()).hexdigest()
assert before==after,'candidate changed during probe'
receipt={'command':[sys.executable,'-B',str(script)],'candidate_sha256':before,'fresh_inputs_only':True,'passed':len(results),'cases':results}
(out/'fresh-results.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'passed':len(results),'candidate_sha256':before,'candidate_stable':True}))
