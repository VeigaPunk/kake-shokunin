# Round 33 C2 sitemap recount — 7fc6aa2f

Axis: freshness. Independent recount of the two pinned `sitemap.xml` blobs using Python's `xml.etree.ElementTree`; extracted all elements whose local XML tag is `loc`, compared the URL sets, and counted duplicates per commit.

Fresh clone: `/fast/scratch/hyaku/kake-r33/w1/ExecRecountSitemapAt7fc6/clone`.

Commands and exit codes:

1. `mkdir -p /fast/scratch/hyaku/kake-r33/w1/ExecRecountSitemapAt7fc6/tmp && unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && export TMPDIR=/fast/scratch/hyaku/kake-r33/w1/ExecRecountSitemapAt7fc6/tmp && git clone -q https://github.com/VeigaPunk/ds4cc-marketplace.git /fast/scratch/hyaku/kake-r33/w1/ExecRecountSitemapAt7fc6/clone && git -C /fast/scratch/hyaku/kake-r33/w1/ExecRecountSitemapAt7fc6/clone checkout -q 7fc6aa2fc12451dd451fed5a9ee7125f3a90e884` — exit 0, no output.
2. Exact XML recount command — exit 0:

```sh
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && python3 -c 'import collections, subprocess, xml.etree.ElementTree as ET; repo="/fast/scratch/hyaku/kake-r33/w1/ExecRecountSitemapAt7fc6/clone"; revs=["1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28", "7fc6aa2fc12451dd451fed5a9ee7125f3a90e884"]; locs={}; blobs={};
for rev in revs:
 data=subprocess.check_output(["git","-C",repo,"show",f"{rev}:sitemap.xml"], text=True); root=ET.fromstring(data); locs[rev]=[e.text.strip() for e in root.iter() if e.tag.rsplit("}",1)[-1]=="loc"]; blobs[rev]=subprocess.check_output(["git","-C",repo,"rev-parse",f"{rev}:sitemap.xml"], text=True).strip(); counts=collections.Counter(locs[rev]); print(f"{rev} blob={blobs[rev]} count={len(locs[rev])} duplicates={sorted(x for x,n in counts.items() if n>1)}")
old,new=(locs[r] for r in revs); print("added:"); [print(x) for x in sorted(set(new)-set(old))]; print("removed:"); [print(x) for x in sorted(set(old)-set(new))]'
```

Observed stdout:

```text
1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28 blob=f6e254afae651c87b5ad9f87195e8caf5735eb7d count=97 duplicates=[]
7fc6aa2fc12451dd451fed5a9ee7125f3a90e884 blob=67d8c7a50dc3a3734ce4be97ffa4810e1e257e12 count=100 duplicates=[]
added:
https://ds4cc.com/magga/frostbite/
https://ds4cc.com/magga/frostbite/classic/
https://ds4cc.com/magga/frostbite/remastered/
removed:
```

Evidence pointers: retained Git objects `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28:sitemap.xml` (blob `f6e254afae651c87b5ad9f87195e8caf5735eb7d`) and `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884:sitemap.xml` (blob `67d8c7a50dc3a3734ce4be97ffa4810e1e257e12`) in the fresh clone above; complete parser output is retained in this report. Duplicate check: none at either revision. No tools installed. No build, test, lint, or formatter run.
