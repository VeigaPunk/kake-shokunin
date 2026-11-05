#!/usr/bin/env python3
# NG10: a synthetic fixture lane whose identity matches the frozen surface SHA
# by using the frozen surfaces list verbatim (SIMULATING a fully-resonant repo)
# and testing whether --base-pins-json can let a lane skip identity.
import hashlib, json, os, shutil, subprocess, sys
S='/fast/scratch/hyaku/kake-r95/ReviewC1'; FX=S+'/fixtures/NG10'
shutil.rmtree(FX, ignore_errors=True); os.makedirs(FX+'/lane/corpus/lessons', exist_ok=True)
os.makedirs(FX+'/lane/corpus/knowledge', exist_ok=True); os.makedirs(FX+'/lane/scripts', exist_ok=True); D=FX+'/lane'
surfaces=json.load(open(S+'/instruments/frozen/c1-surfaces.json'))
L='/home/vgpnk/Projects/shokunin/kake-shokunin'
# take lesson-01 blob from the real repo, in the lane
r=subprocess.run(['git','-C',L,'show','fdd5fdbeb8a2ba6c18f0f23135d1bee98068dca3:corpus/lessons/round-01.md'], capture_output=True)
lesson=r.stdout.decode('utf-8','replace')
open(D+'/corpus/lessons/round-01.md','w').write(lesson)
open(D+'/corpus/knowledge/entry.md','w').write('source: S001\nverified-at: 2026-11-05\nrecheck: 180d\n\nbody\n')
open(D+'/corpus/QUALITY.md','w').write('# Q\n\n## Round-01 criterion — a thing\n\nGrounded in `corpus/lessons/round-01.md`.\n')
open(D+'/corpus/SOURCES.md','w').write('# S\n\n## Registry\n\n| id | source |\n|---|---|\n| S001 | x |\n')
open(D+'/SKILL.md','w').write('| name | kind | entry | verdict |\n|---|---|---|---|\n| t | gate | `scripts/t.py` | 0=ok |\n')
open(D+'/scripts/t.py','w').write("print('t')\n")
subprocess.run(['git','-C',D,'init','-q']); subprocess.run(['git','-C',D,'config','user.email','reviewc1@example.invalid'])
subprocess.run(['git','-C',D,'config','user.name','reviewc1'])
subprocess.run(['git','-C',D,'add','-A']); subprocess.run(['git','-C',D,'commit','-q','-m','fixture'])
rev=subprocess.run(['git','-C',D,'rev-parse','HEAD'], capture_output=True).stdout.decode().strip()
print('[NG10] committed at', rev[:12])
with open(FX+'/rev', 'w') as fh: fh.write(rev)
