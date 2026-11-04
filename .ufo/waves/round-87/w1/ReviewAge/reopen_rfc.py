import urllib.request, hashlib, json, time
from pathlib import Path
out=Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ReviewAge')
u='https://www.rfc-editor.org/rfc/rfc9111.txt'
start=time.time_ns()
with urllib.request.urlopen(urllib.request.Request(u,method='GET'),timeout=40) as r:
    data=r.read(); status=r.status; headers={k:v for k,v in r.headers.items() if k.lower() in {'date','age','content-type','etag','cache-control','last-modified'}}; url=r.url
end=time.time_ns()
text=data.decode('utf-8')
section=text.split('\n4.2.3.  Calculating Age\n',1)[1].split('\n4.2.4.',1)[0]
delta=text.split('\n1.2.2.  Delta Seconds\n',1)[1].split('\n2. ',1)[0]
(out/'rfc9111-quotes.txt').write_text('4.2.3. Calculating Age\n'+section+'\n1.2.2. Delta Seconds\n'+delta)
receipt=dict(method='GET',url=url,status=status,request_ns=start,response_ns=end,sha256=hashlib.sha256(data).hexdigest(),headers=headers,retained='Sections 4.2.3 and 1.2.2 only')
(out/'rfc9111-get.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
