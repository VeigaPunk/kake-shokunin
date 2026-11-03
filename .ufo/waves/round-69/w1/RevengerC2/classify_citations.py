#!/usr/bin/env python3
"""RevengerC2 census: classify every base-revision citation of /tmp/kake-r.

Class rules, applied in this order to each citation line:
  executable  a command a reader is told to run, or a code line in a committed
              script: shell verb + the /tmp path as its operand (mktemp, git clone,
              curl -o/-D, python3/node <script> whose argv names the path, redirection
              into the path, `SEATS=`, `const X = '...'`, opens/reads).
  historical  the line marks the path absent or historical (word-boundary
              absent|historical|deleted|gone|no longer|reaper|skipped).
  pointer     neither: a bare provenance pointer to a directory that is not on disk.
Usage: python3 classify_citations.py <lane> <rev>   (writes a TSV to stdout)
"""
import re, subprocess, sys, collections

CMD = re.compile(r"""(mktemp\s+-d|git\s+clone|git\s+-C\s+\S+\s+clone|curl\s|wget\s|timeout\s+-k
  |^\s*SEATS=|>\s*/tmp|>>\s*/tmp|-o\s+/tmp|-D\s+/tmp
  |(python3|node)\s+(-B\s+)?(\S*/)?/tmp/kake-r|--root\s+/tmp|--manifest\s+/tmp|--history\s+/tmp
  |--output=/tmp|(const|let|var)\s+\w+\s*=\s*process\.env\.\w+\s*\|\|\s*'/tmp)""", re.X)
HIST = re.compile(r'\b(absent|historical|deleted|gone|no longer|reaper|skipped)\b', re.I)

def main(lane, rev):
    out = subprocess.run(['git','-C',lane,'grep','-l','-F','/tmp/kake-r',rev,'--','.'],capture_output=True,text=True).stdout.split()
    rows=[]
    for ent in sorted(out):
        p = ent.split(':',1)[1]
        txt = subprocess.run(['git','-C',lane,'show',f'{rev}:{p}'],capture_output=True,text=True).stdout.split('\n')
        c = collections.Counter()
        for line in txt:
            if '/tmp/kake-r' not in line: continue
            s = line.strip()
            if CMD.search(s): k='executable'
            elif HIST.search(s): k='historical'
            else: k='pointer'
            c[k]+=1
        grp = 'mirror' if 'assimilation' in p else 'scripts' if p.startswith('scripts/') else 'waves' if p.startswith('.ufo/waves/') else 'prose'
        rows.append((p,grp,sum(c.values()),c['executable'],c['historical'],c['pointer']))
    print('file\tgroup\tcitations\texecutable\thistorical\tpointer')
    for r in rows: print('\t'.join(map(str,r)))

main(sys.argv[1], sys.argv[2])
