#!/usr/bin/env python3
"""Per-revision inventory of what the CURRENT tool parses out of the lane:
registry ids (parse_registry), cited ids (parse_cited), plus lane tree facts."""
import importlib.util
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
TOOL = os.path.join(LANE, "scripts/id_resolver.py")

spec = importlib.util.spec_from_file_location("idres", TOOL)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def git(*args, cwd=LANE):
    p = subprocess.run(["git", "-C", cwd, *args], capture_output=True)
    return p.returncode, p.stdout


def main():
    revs = git("rev-list", "--first-parent", "-10", "master")[1].decode().split()
    for rev in revs:
        reg_text = git("show", f"{rev}:{mod.REGISTRY_REL}")[1].decode("utf-8", "replace")
        reg = mod.parse_registry(reg_text)
        # count raw table rows in the section the way the census would (upper bound)
        rows = [l for l in reg_text.splitlines()
                if l.startswith("| S") and "|" in l]
        paths = git("ls-tree", "-r", "-z", "--name-only", rev)[1].split(b"\0")
        rels = [p.decode("utf-8", "replace") for p in paths
                if p and p.decode("utf-8", "replace").startswith(mod.KNOWLEDGE_REL + "/")
                and p.decode("utf-8", "replace").endswith(".md")]
        bodies = {}
        for rel in rels:
            bodies[rel] = git("show", f"{rev}:{rel}")[1].decode("utf-8", "replace")
        cited = mod.parse_cited(bodies)
        dangling = sorted(set(cited) - set(reg))
        print(f"[{rev[:12]}] registry_ids={len(reg)} raw_S_rows={len(rows)} "
              f"knowledge_md_files={len(rels)} cited_ids={len(cited)} dangling={len(dangling)} {dangling[:6]}")


if __name__ == "__main__":
    main()
