"""Read-only labrat: materialize the counter's K4/K5 fixtures via its own lane()/repo()
helpers and inspect the committed tree. Uses the counter as a library; no mutation outside
the given work dir."""
import importlib.util
import os
import subprocess
import sys

COUNTER = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58/c58_resolver_cases.py"
work = sys.argv[1]
spec = importlib.util.spec_from_file_location("c58", COUNTER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

reg_ok = "## Registry\n\n" + m.HDR + m.row("S001")
out = {}
for name, knowledge in (("k4", {"ok.md": "Cites S001.\n", "\u4e2d\u6587.md": "Cites S900.\n"}),
                        ("k5", {"ok.md": "Cites S001.\n", 'a"b.md': "Cites S901.\n"})):
    fl, lp, head = m.lane(work, name, m.registry(reg_ok), knowledge, git_lane=True)
    def g(*a):
        p = subprocess.run(["git", "-C", lp, *a], capture_output=True)
        return p.returncode, p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")
    rc_top, top = g("rev-parse", "--show-toplevel")
    rc_tree, tree = g("ls-tree", "-r", "--name-only", "HEAD")
    rc_status, status = g("status", "--porcelain")
    rc_show, show = g("show", "--stat", "--oneline", "HEAD")
    disk = sorted(os.listdir(os.path.join(lp, "corpus", "knowledge")))
    out[name] = {
        "toplevel_ok": os.path.realpath(top.strip()) == os.path.realpath(lp),
        "head": head[:12],
        "ls_tree": tree.splitlines(),
        "disk": disk,
        "status_clean": status.strip() == "",
        "commit_stat": show.strip().splitlines()[:2],
    }

import json
print(json.dumps({"work": work, "fsenc": sys.getfilesystemencoding(), "utf8_mode": sys.flags.utf8_mode,
                  "fixtures": out}, ensure_ascii=False, indent=1, sort_keys=True))
