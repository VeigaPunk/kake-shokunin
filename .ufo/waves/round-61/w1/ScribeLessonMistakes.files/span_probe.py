import re, subprocess, pathlib
SPAN = re.compile(r"(?im)(^#\s*receipt\s*:|revision\s*[:=]|EXIT\s*=|met\s*=|conditions_passed|cases_passed|findings\s*=|scores_held|members\s*=)")
def git(*a):
    p = subprocess.run(["git", *a], capture_output=True, text=True, cwd="/home/vgpnk/Projects/shokunin/kake-shokunin")
    return p.stdout
paths = [l.strip() for l in open("/fast/scratch/hyaku/kake-r61/ScribeLessonMistakes/multitouch.txt")]
rows=[]
for line in paths:
    _, path = line.split(" ", 1)
    commits = git("log","--first-parent","--format=%H","--",path).split()
    events=[]; touched=0
    for c in commits:
        parent = git("rev-parse", c+"^").strip()
        if not parent: continue
        cur = git("show", f"{c}:{path}")
        try: prev = git("show", f"{parent}:{path}")
        except Exception: prev = None
        if not prev: continue
        if cur != prev:
            touched += 1
            span = lambda t: [l for l in t.splitlines() if SPAN.search(l)]
            if span(cur) != span(prev):
                events.append(c[:10])
    rows.append((path, len(commits), touched, events))
tot=0
for path,n,t,ev in rows:
    tot += len(ev)
    print(f"{n:2d} commits | {t} changed-after-add | span-changing={len(ev)} {ev} | {path}")
print("total span-changing event commits (first-parent, matching files):", tot)
