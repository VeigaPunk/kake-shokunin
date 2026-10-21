#!/usr/bin/env python3
"""Frozen C2 oracle: candidate gate must reject the unmodified inherited r26 citing set."""
import argparse,hashlib,json,pathlib,subprocess,tempfile,sys
W='.ufo/waves/round-27/'
def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=pathlib.Path,required=True);p.add_argument('--revision',required=True);a=p.parse_args()
    def b(path): return subprocess.check_output(['git','-C',str(a.root),'show',a.revision+':'+path],stderr=subprocess.DEVNULL)
    try:
        oracle=json.loads(b(W+'c2-oracle.json'));exp=json.loads(b(W+'frozen/expected.json'))
        with tempfile.TemporaryDirectory(prefix='c2-',dir='/fast/scratch/hyaku/kake-r27') as t:
            root=pathlib.Path(t)
            for path,digest in exp['sha256'].items():
                data=b(W+'frozen/'+path)
                if hashlib.sha256(data).hexdigest()!=digest:
                    print(json.dumps({'verdict':'could-not-evaluate','finding':'snapshot_tampered','file':path}));return 2
                dst=root/path;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
            gate=b('scripts/citing_set.py');(root/'gate.py').write_bytes(gate)
            run=subprocess.run([sys.executable,'-B',str(root/'gate.py'),'--root',str(root),'--population','population.json','--ledger','ledger.json','--json'],text=True,capture_output=True)
            out=json.loads(run.stdout); actual={(x.get('row'),x.get('file')) for x in out['findings'] if x['id']=='unadjudicated_citing_pair'}
            expected={(x['row'],x['file']) for x in oracle['expectedPairs']}
            passed=run.returncode==oracle['expectedExit'] and actual==expected and len(out['findings'])==len(expected)
            print(json.dumps({'revision':a.revision,'frozenRevision':oracle['frozenRevision'],'expected':len(expected),'detected':len(actual&expected),'falsePositive':len(actual-expected),'passed':passed,'gateExit':run.returncode,'gate':out,'stderr':run.stderr},indent=2));return 0 if passed else 1
    except subprocess.CalledProcessError as e:
        if e.cmd[-1].endswith(':scripts/citing_set.py'):
            print(json.dumps({'revision':a.revision,'expected':16,'detected':0,'passed':False,'finding':'gate_absent'}));return 1
        raise
    except Exception as e:
        print(json.dumps({'verdict':'could-not-evaluate','error':type(e).__name__+': '+str(e)}));return 2
if __name__=='__main__':sys.exit(main())
