import re, subprocess
LANE="/home/vgpnk/Projects/shokunin/kake-shokunin"
paths=""".ufo/waves/round-52/control/census-after.txt
.ufo/waves/round-55/controls/c1-selftest.txt
.ufo/waves/round-57/controls/census-before.txt
.ufo/waves/round-60/controls/census-before.txt
.ufo/waves/round-37/retained/controls/c2/c2-junk.json
.ufo/waves/round-51/controls/c1-before-base.txt
.ufo/waves/round-59/controls/a2-noharm-at-T0.txt
.ufo/waves/round-60/controls/after-c1-gate-status-t1.txt
.ufo/waves/round-58/controls/census-before.txt
.ufo/waves/round-57/controls/tool-selftest-final.txt""".splitlines()
g_receipt=re.compile(r"(?im)^\s*#\s*receipt\s*:")
g_exit=re.compile(r"(?im)EXIT\s*=")
g_verdict=re.compile(r"(?im)^VERDICT:")
for p in paths:
    r2=subprocess.run(["git","-C",LANE,"log","--reverse","--format=%H %s","--",p],capture_output=True,text=True)
    lines=r2.stdout.splitlines()
    first=lines[0].split()[0]
    r=subprocess.run(["git","-C",LANE,"show",f"{first}:{p}"],capture_output=True)
    body=r.stdout.decode("utf-8","replace")
    has=any(g_receipt.search(l) or g_exit.search(l) or g_verdict.search(l) for l in body.splitlines())
    ncommits=len(lines)
    print(f"{'GRAMMAR' if has else 'NOGRAM '} commits={ncommits} first={first[:8]} {p}")
    if not has:
        print("   first-ver head:", body.splitlines()[:3])
