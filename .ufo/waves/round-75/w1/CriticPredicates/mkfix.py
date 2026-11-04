import os, subprocess, sys, shutil
S = os.path.dirname(os.path.abspath(__file__))
BASE = 'c9c5e484c533aa65f4374b841a3edcf572ed19a9'
HDR = ("\n### Round 75 gate registry additions\n\n"
       "Round 75 supersessions.\n\n"
       "| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |\n"
       "|---|---|---|---|---|---|---|---|\n")
ROW69 = ("| c69_tmp_honour.py | instrument (live; offline; demoted from gate by round 75: no self-test mode of its own) "
         "| `python3 -B .ufo/waves/round-69/c69_tmp_honour.py --root <lane> --revision <rev> --work <scratch dir>` "
         "| `0=met`; `1=not met`; `2=usage` "
         "| none (no self-test mode; `--selftest` is an argparse error, exit 2) "
         "| round-69 baseline | lane read-only | r75 |\n")
ROW74_HONEST = ("| c74_registry_gap.py | gate (live; offline over committed SKILL.md and counter-tree bytes) "
         "| `python3 -B .ufo/waves/round-74/c74_registry_gap.py --root <lane> --revision <rev>` "
         "| `0=met`; `1=not met`; `2=unevaluable`; `64=usage` "
         "| `python3 -B .ufo/waves/round-74/c74_registry_gap.py --selftest` -> `selftest 8/8`, exit 0 (eight fixtures f1 f2 f3 f4 f5 f6 f7 f8) "
         "| round-74 receipt | lane read-only | r75 |\n")
ROW74_LAUNDER = ("| c74_registry_gap.py | gate (live; offline over committed SKILL.md and counter-tree bytes) "
         "| `python3 -B .ufo/waves/round-74/c74_registry_gap.py --root <lane> --revision <rev>` "
         "| `0=met`; `1=not met`; `2=unevaluable`; `64=usage` "
         "| `python3 -B .ufo/waves/round-74/c74_registry_gap.py --selftest` "
         "| round-74 receipt | lane read-only | r75 |\n")
ROW_BOGUS_E4 = ("| commit-citation-lint | instrument (live; superseded row naming an extra path token) "
         "| `python3 -B scripts/citation_lint.py --root . --revision <commit> scripts/c75_missing_tool.py` "
         "| `0=met` "
         "| `python3 -B scripts/citation_lint.py --selftest` "
         "| round-47 receipt | scripts read-only | r75 |\n")
ROW52_FALSE_E2 = ("| wave-evidence-ledger | gate (offline, committed bytes only; no network) "
         "| `python3 -B .ufo/waves/round-52/c52_wave_ledger.py --root . --revision <commit>` "
         "| `0=met` "
         "| `python3 -B .ufo/waves/round-52/c52_wave_ledger.py --selftest` -> `19/19`, exit 0 (19 fixtures, sandbox repos) "
         "| round-52 baselines | lane read-only | r75 |\n")
ROW58_FALSE_E2 = ("| resolver-cases-counter | gate (the tool at the revision against gate-built fixture lanes) "
         "| `TMPDIR=<scratch> python3 -B .ufo/waves/round-58/c58_resolver_cases.py --root <lane> --revision <rev>` "
         "| `0=met` "
         "| `TMPDIR=<scratch> python3 -B .ufo/waves/round-58/c58_resolver_cases.py --selftest` -> `7/7` control tools, exit 0 "
         "| round-58 controls | lane read-only | r75 |\n")
ROW_NEW17 = ("| instrument-receipts | gate (live; offline; sha256 binding of the population) "
         "| `python3 -B scripts/instrument_receipts.py --root . --revision <commit> --check` "
         "| `0=met`; `1=not met`; `2=unevaluable`; `64=usage` "
         "| `python3 -B scripts/instrument_receipts.py --selftest` "
         "| corpus/knowledge/instrument-receipts.json | scripts read-only | r75 |\n")
NEWTOOL = '''#!/usr/bin/env python3
import argparse, sys
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root'); ap.add_argument('--revision'); ap.add_argument('--check', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    print('selftest 3/3')
    return 0
if __name__ == '__main__':
    sys.exit(main())
'''

ROW69_A3 = ("| c69_tmp_honour.py | gate (live; offline; operability: the freshness sweep carries no code-level scratch-root path literal) "
         "| `python3 -B .ufo/waves/round-69/c69_tmp_honour.py --root <lane> --revision <rev> --work <scratch dir>` "
         "| `0=met`; `1=not met`; `2=usage` "
         "| `python3 -B .ufo/waves/round-58/c58_receipt_rewrites.py --selftest` "
         "| round-69 baseline | lane read-only | r75 |\n")
ROW_E2SEG = ("| commit-citation-lint | gate (offline; no network) "
         "| `python3 -B scripts/citation_lint.py --root . --revision <commit>` "
         "| `0=met` "
         "| `python3 -B scripts/citation_lint.py --selftest` -> `9/9` passed; the round-47 receipt records `8/8` at its then-sha256 "
         "| round-47 receipt | scripts read-only | r75 |\n")
MODES = {
 'honest':   HDR + ROW69 + ROW74_HONEST,
 'launder':  HDR + ROW69 + ROW74_LAUNDER,
 'a3other':  HDR + ROW69_A3 + ROW74_HONEST,
 'e2seg':    HDR + ROW69 + ROW74_HONEST + ROW_E2SEG,
 'e4bogus':  HDR + ROW69 + ROW74_HONEST + ROW_BOGUS_E4,
 'e2false58':HDR + ROW69 + ROW74_HONEST + ROW58_FALSE_E2,
 'e2false52':HDR + ROW69 + ROW74_HONEST + ROW52_FALSE_E2,
 'pop17':    HDR + ROW69 + ROW74_HONEST + ROW_NEW17,
}
mode, dst = sys.argv[1], sys.argv[2]
subprocess.run(['git','clone','-q','--shared', os.path.join(S,'clone-base'), dst], check=True)
subprocess.run(['git','-C',dst,'checkout','-q',BASE], check=True)
assert subprocess.run(['git','-C',dst,'rev-parse','--show-toplevel'],capture_output=True,text=True).stdout.strip()==dst
p = os.path.join(dst,'SKILL.md')
with open(p,'a') as fh: fh.write(MODES[mode])
if mode == 'pop17':
    tp = os.path.join(dst,'scripts','instrument_receipts.py')
    with open(tp,'w') as fh: fh.write(NEWTOOL)
    subprocess.run(['git','-C',dst,'add','scripts/instrument_receipts.py'], check=True)
subprocess.run(['git','-C',dst,'add','SKILL.md'], check=True)
subprocess.run(['git','-C',dst,'-c','user.name=critic','-c','user.email=critic@local','commit','-q','-m',f'fixture: {mode}'], check=True)
print(subprocess.run(['git','-C',dst,'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip())
