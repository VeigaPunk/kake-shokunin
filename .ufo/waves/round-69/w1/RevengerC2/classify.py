#!/usr/bin/env python3
"""RevengerC2 census: classify every citation of the literal `/tmp/kake-r` at a revision.

Unit = one line containing the literal (a "citation").
Class, per citation, decided by the token's immediate context:
  executable  the path is an operand of a command a reader/runner executes:
              preceded (after stripping quotes) by -o|-D|-C|--root|--manifest|--history|
              --validator|--output=, >|>>, `mktemp -d`, `git clone` destination, TMPDIR=,
              a NAME= assignment, `python3|node`, `cat`; or the line is a code line of a
              committed script assigning the literal (const/let/var ... '/tmp/kake-r...').
  historical  an absence/history marker occurs within 50 chars of the token on the same
              line: absent|historical|deleted|gone|no longer|reaper|skipped.
  pointer     neither: a bare provenance pointer.

Usage: python3 classify.py <lane> <rev>   -> per-file TSV on stdout, totals on stderr.
"""
import re, subprocess, sys, collections

TOK = re.compile(r'/tmp/kake-r[^\s`"\'),;|]*')
OPER = re.compile(
    r"(?:-o|-D|-C|--root|--manifest|--history|--validator|--output=)\s*$"
    r"|>>?\s*$|mktemp\s+-d\s*$|git\s+clone(?:\s+--?\S+)*\s+\S+\s*$"
    r"|TMPDIR=\s*$|[A-Za-z_][A-Za-z0-9_]*=\s*$|(?:python3|node)\s+(?:-B\s+)?$|cat\s+$")
ASSIGN = re.compile(r"^\s*(?:const|let|var)\s+\w+\s*=.*['\"`]/tmp/kake-r")
HIST = re.compile(r'\b(absent|historical|deleted|gone|no longer|reaper|skipped)\b', re.I)
CODE = ('.py', '.mjs', '.js', '.cjs', '.sh', '.bash')

def classify(line, path):
    found = False
    for m in TOK.finditer(line):
        before = line[:m.start()].rstrip()
        if OPER.search(before):
            return 'executable'
        if path.endswith(CODE) and ASSIGN.match(line) and not line.lstrip().startswith(('#', '//', '*')):
            return 'executable'
        window = line[max(0, m.start() - 50): m.end() + 50]
        if HIST.search(window):
            found = True
    return 'historical' if found else 'pointer'

def main(lane, rev):
    ents = sorted(subprocess.run(['git','-C',lane,'grep','-l','-F','/tmp/kake-r',rev,'--','.'],capture_output=True,text=True).stdout.split())
    print('file\tgroup\tcitations\texecutable\thistorical\tpointer')
    tot = collections.Counter()
    for ent in ents:
        p = ent.split(':', 1)[1]
        txt = subprocess.run(['git','-C',lane,'show',f'{rev}:{p}'],capture_output=True,text=True).stdout.split('\n')
        c = collections.Counter()
        for line in txt:
            if '/tmp/kake-r' in line:
                c[classify(line, p)] += 1
        grp = 'mirror' if 'assimilation' in p else 'scripts' if p.startswith('scripts/') else 'waves' if p.startswith('.ufo/waves/') else 'prose'
        tot.update(c)
        print(f"{p}\t{grp}\t{sum(c.values())}\t{c['executable']}\t{c['historical']}\t{c['pointer']}")
    print('#TOTAL', dict(tot), file=sys.stderr)

main(sys.argv[1], sys.argv[2])
