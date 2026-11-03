import re
rows = {
 "staged S352 (verbatim, staged append line 72)":
   open('/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md').read().split('\n')[71],
 "crafted S901 (escaped pipe in scope, delimiter dropped)":
   "| S901 | craft | docs | A | scope \\| note | anchor | mined | 2026-11-03 | 180d | corpus/knowledge/ghost.md |",
 "normalized S438 (ExecMirror)":
   open('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-70/w1/ExecMirror/normalized-row.md').read().split('\n')[0],
}
hdr = "id source kind tier scope anchor teaches status opened recheck used-by".split()
for name, r in rows.items():
    raw = r.count('|')
    nf = raw + 1
    f = r.split('|')
    gfm = [c.strip() for c in re.split(r'(?<!\\)\|', r.strip().strip('|'))]
    print("==", name)
    print("   raw_pipes=%d awk_NF=%d census_NF==13? %s" % (raw, nf, nf == 13))
    print("   awk cells (census positions 2..12):")
    for i, c in enumerate(f[1:12], start=1):
        print("      $%d = %r" % (i+1, c.strip()))
    print("   GFM-visible cells: %d  %r" % (len(gfm), gfm))
    print("   census verdict for status/opened/recheck/used-by: %r %r %r %r" % (
        f[8].strip(), f[9].strip(), f[10].strip(), f[11].strip()))
