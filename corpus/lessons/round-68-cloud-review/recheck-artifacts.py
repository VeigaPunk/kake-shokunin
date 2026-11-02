#!/usr/bin/env python3
"""Independent read-only committed-artifact recheck; 0 verified, 1 assertion fails."""
import hashlib,html,json,pathlib,re,subprocess
root=pathlib.Path(__file__).resolve().parents[2]/'lanes/kake'
base='396128196ffb1c3184a6dc4491da1e5612a3b425';tip='17072048d5990c3d0e663d0cf51752aae6919d7b'
def blob(r,p):return subprocess.check_output(['git','-C',str(root),'show',r+':'+p])
for r in (base,tip):
 for path,pattern in [('corpus/knowledge/gate-status-ledger.md',rb'not adjudicated here|candidate mechanism'),('corpus/knowledge/publish-queue.md',rb'r68 dated')]:
  print(r,path,'count='+str(sum(bool(re.search(pattern,x)) for x in blob(r,path).splitlines())))
 print(r,'SOURCES rows='+str(len(re.findall(rb'^\|\s*S\d{3,}\s*\|',blob(r,'corpus/SOURCES.md'),re.M))))
for kind,key in [('probes','probes'),('sources','opens')]:
 prefix='.ufo/waves/round-68/'+kind+'/'
 for row in json.loads(blob(tip,prefix+'receipt.json'))[key]:
  body=blob(tip,prefix+row['bodyFile']);digest=hashlib.sha256(body).hexdigest()
  assert len(body)==row['bytes'] and digest==row['sha256']
  print(row['bodyFile'],len(body),digest,'MATCH')
  if kind=='sources':
   q=row['locatedQuote'];flat=' '.join(html.unescape(re.sub('<[^>]+>',' ',body.decode())).split())
   assert q in flat and len(q.split())==14
   print('GNU quote words=14 collapsed=True raw='+str(q in body.decode()))
for path in ['LOG.md','SCORECARD.md','corpus/knowledge/publish-queue.md']:
 assert blob(tip,path).startswith(blob(base,path));print(path,'byte-prefix-append=True')
for name,retained in [('gnu','sources/S435-grep-manual.html'),('lucario','probes/veigapunk.github.io_lucario.body'),('charter','probes/veigapunk.github.io_charter-ufo-fsd.body'),('burnerchrome','probes/burnerchrome.kimi.page.body')]:
 fresh=pathlib.Path(__file__).parent/'live'/f'{name}.body'
 assert fresh.read_bytes()==blob(tip,'.ufo/waves/round-68/'+retained);print(name,'live-byte-identical=True')
