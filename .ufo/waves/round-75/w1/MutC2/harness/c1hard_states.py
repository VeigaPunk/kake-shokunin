#!/usr/bin/env python3
"""c1hard_states.py — concrete states for the three surviving hardened-counter mutants."""
import importlib.util, json, os, shutil, subprocess, sys
HERE='/fast/scratch/hyaku/kake-r75/MutationTesterC2'
BASE=os.environ.get('C1HARD', os.path.join(HERE,'work','c1hard','c75_hard.py'))
MUT=os.path.join(HERE,'work','c1hard','mut')
WORK=os.path.join(HERE,'work','c1hard','states')

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

P=load(BASE,'c1h_pristine')
M={mid:load(os.path.join(MUT,mid,'c75_row_truth.py'),'c1h_'+mid)
   for mid in ('H-M4','H-M5','H-M6')}

SCRIPT_NO_SELFTEST='print("quiet fixture")\n'
SCRIPT_NO_TALLY=("import argparse\n"
                 "ap=argparse.ArgumentParser()\n"
                 "ap.add_argument('--selftest', action='store_true')\n"
                 "print('selftest done')\n")

def build(fid, rows, files):
    fx=P.Fixture(WORK,fid)
    for rel,text in files.items(): fx.write(rel,text)
    fx.write('SKILL.md',P._skill_md(rows))
    rev=fx.commit(fid)
    tree=os.path.join(fx.base_dir,'tree2')
    shutil.rmtree(tree,ignore_errors=True)
    subprocess.run(['git','clone','-q','--shared',fx.repo,tree],check=True)
    subprocess.run(['git','-C',tree,'checkout','-q',rev],check=True)
    scratch=os.path.join(fx.base_dir,'scratch2')
    return fx,rev,tree,scratch

def measure(mod,fx,rev,tree,scratch,pop):
    res=mod.measure(fx.repo,rev,tree,scratch,pop)
    return {'summary':mod.format_summary(rev,res),'findings':res['findings']}

def full_row(name,kind,entry,verdict,selftest,pinned='none'):
    return (f'| {name} | {kind} | `{entry}` | {verdict} | {selftest} | {pinned} | none | fixture |')

states={}

# S1 (H-M5): a gate row claims selftest 2/2 but the command prints no tally.
rows=[full_row('.ufo/fixtures/no_tally.py','gate (live; fixture)',
               'python3 -B .ufo/fixtures/no_tally.py','`0=met`; `1=not met`',
               '`python3 -B .ufo/fixtures/no_tally.py --selftest` → `selftest 2/2`')]
fx,rev,tree,scratch=build('s1_no_tally',rows,{'.ufo/fixtures/no_tally.py':SCRIPT_NO_TALLY})
states['S1_no_tally']={mid:measure(mod,fx,rev,tree,scratch,['.ufo/fixtures/no_tally.py'])
                       for mid,mod in [('pristine',P)]+list(M.items())}

# S2 (H-M6): the word differential is in the Verdict cell, never in the Kind cell.
rows=[full_row('.ufo/fixtures/no_selftest.py','gate (live; fixture)',
               'python3 -B .ufo/fixtures/no_selftest.py',
               '`0=met`; the differential substitute lives in the receipt',
               'none (no self-test mode)')]
fx,rev,tree,scratch=build('s2_diff_elsewhere',rows,{'.ufo/fixtures/no_selftest.py':SCRIPT_NO_SELFTEST})
states['S2_differential_outside_kind']={mid:measure(mod,fx,rev,tree,scratch,['.ufo/fixtures/no_selftest.py'])
                       for mid,mod in [('pristine',P)]+list(M.items())}

# S3 (H-M4): the claim segment records 3/3; a receipt-history pair 9/9 follows ';'.
rows=[full_row('.ufo/fixtures/ok.py','gate (live; fixture)',
               'python3 -B .ufo/fixtures/ok.py','`0=met`; `1=not met`',
               '`python3 -B .ufo/fixtures/ok.py --selftest` (3/3 fixture checks); witness 9/9 in the receipt')]
fx,rev,tree,scratch=build('s3_history_pair',rows,{'.ufo/fixtures/ok.py':P.SCRIPT_OK})
states['S3_history_pair']={mid:measure(mod,fx,rev,tree,scratch,['.ufo/fixtures/ok.py'])
                       for mid,mod in [('pristine',P)]+list(M.items())}

json.dump(states,open(os.path.join(HERE,'work','c1hard-states.json'),'w'),indent=2)
for name,res in states.items():
    print('==',name)
    for who,val in res.items():
        print('  ',who,val['summary'])
