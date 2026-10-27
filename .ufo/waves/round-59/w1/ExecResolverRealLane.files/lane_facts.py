#!/usr/bin/env python3
"""Lane facts for the C2 no-harm baseline: symlinks, HTML comments and setext
underlines inside `## Registry` of corpus/SOURCES.md, non-UTF-8 names."""
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"


def git(*args):
    p = subprocess.run(["git", "-C", LANE, *args], capture_output=True)
    return p.returncode, p.stdout, p.stderr


def section_lines(text):
    """Lines of the `## Registry` section (ends at the next `# ` or `## ` heading)."""
    out = []
    inside = False
    for raw in text.splitlines():
        if raw.startswith("## ") and raw[3:].strip() == "Registry":
            inside = True
            continue
        if inside and (raw.startswith("# ") or raw.startswith("## ")):
            break
        if inside:
            out.append(raw)
    return out


def main():
    revs = sys.argv[1:] or ["master"]
    for rev in revs:
        rc, out, err = git("ls-tree", "-r", rev)
        lines = out.decode("utf-8", "replace").splitlines()
        modes = {}
        names = []
        for line in lines:
            meta, _, path = line.partition("\t")
            mode = meta.split()[0]
            modes[mode] = modes.get(mode, 0) + 1
            names.append(path)
        symlinks = modes.get("120000", 0)
        # non-UTF-8 names: ls-tree quotes unusual bytes by default (core.quotePath)
        rc2, raw, _ = git("-c", "core.quotePath=false", "ls-tree", "-r", "--name-only", rev)
        bad = []
        for b in raw.split(b"\0"):
            if not b:
                continue
            try:
                b.decode("utf-8")
            except UnicodeDecodeError:
                bad.append(b)
        rc3, sources, _ = git("show", f"{rev}:corpus/SOURCES.md")
        text = sources.decode("utf-8", "replace")
        sec = section_lines(text)
        comments = [l for l in sec if "<!--" in l or "-->" in l]
        setext = [l for l in sec if l.strip() and set(l.strip()) <= set("=-") and len(l.strip()) >= 2]
        print(f"[{rev[:12]}] tree_entries={len(lines)} symlinks={symlinks} modes={modes}")
        print(f"[{rev[:12]}] non_utf8_names={len(bad)} {bad[:5]!r}")
        print(f"[{rev[:12]}] registry_section_lines={len(sec)} html_comment_lines={len(comments)} setext_underline_lines={len(setext)}")
        for l in comments[:10]:
            print("   COMMENT:", l[:120])
        for l in setext[:10]:
            print("   SETEXT:", repr(l[:120]))


if __name__ == "__main__":
    main()
