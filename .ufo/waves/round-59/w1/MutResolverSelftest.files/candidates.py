#!/usr/bin/env python3
"""Candidate selftest cases: for each surviving mutant, does a proposed case PASS on the pristine
tool and FAIL on the mutant? A candidate that kills its mutant closes the blind spot."""
import importlib.util
import os
import shutil
import subprocess
import sys

W = "/fast/scratch/hyaku/kake-r59/MutResolverSelftest/work/cand"
SRC = "/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/id_resolver.py"
REG = ("# Sources\n## Registry\n\n"
       "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
       "|---|---|---|---|---|---|---|---|---|---|---|\n")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def w(p, t):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write(t)


def git(path, *a):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", "-C", path, *a], capture_output=True, env=env)


def base_tool(t):
    return load(os.path.join(W, "..", "..", t), t.split(".")[0])


def case_registry_level3_heading(mod):
    """a level-3 heading does not end the Registry section; the rows after it still register"""
    d = os.path.join(W, "c_level3")
    shutil.rmtree(d, ignore_errors=True)
    lane = os.path.join(d, "demo-shokunin")
    w(lane + "/corpus/SOURCES.md", REG +
      "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n"
      "### Sub\n"
      "| S002 | https://e.example/2 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    w(lane + "/corpus/knowledge/a.md", "Cites S001 and S002.\n")
    res = mod.evaluate(lane, fleet=d)
    mod._check(res.summary == (2, 2, 0, 0, 0), f"summary={res.summary}")


def case_fence_indent_four_is_code(mod):
    """a 4-space indented fence is code, not a fence; the row after it still registers"""
    d = os.path.join(W, "c_indent4")
    shutil.rmtree(d, ignore_errors=True)
    lane = os.path.join(d, "demo-shokunin")
    w(lane + "/corpus/SOURCES.md", REG +
      "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n"
      "    ```\n"
      "| S002 | https://e.example/2 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    w(lane + "/corpus/knowledge/a.md", "Cites S001 and S002.\n")
    res = mod.evaluate(lane, fleet=d)
    mod._check(res.summary == (2, 2, 0, 0, 0), f"summary={res.summary}")


def case_fence_char_must_match(mod):
    """a backtick run does not close a tilde fence"""
    d = os.path.join(W, "c_char")
    shutil.rmtree(d, ignore_errors=True)
    lane = os.path.join(d, "demo-shokunin")
    w(lane + "/corpus/SOURCES.md", REG +
      "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n"
      "~~~\n| S002 | https://e.example/2 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n```\n"
      "| S003 | https://e.example/3 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n~~~\n")
    w(lane + "/corpus/knowledge/a.md", "Cites S001, S002 and S003.\n")
    res = mod.evaluate(lane, fleet=d)
    mod._check(res.summary == (3, 1, 2, 0, 2), f"summary={res.summary}")


def case_fence_info_string_no_backtick(mod):
    """a backtick in the info string means the line is not a fence; the row after it registers"""
    d = os.path.join(W, "c_info")
    shutil.rmtree(d, ignore_errors=True)
    lane = os.path.join(d, "demo-shokunin")
    w(lane + "/corpus/SOURCES.md", REG +
      "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n"
      "```a`b\n| S002 | https://e.example/2 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n```\n")
    w(lane + "/corpus/knowledge/a.md", "Cites S001 and S002.\n")
    res = mod.evaluate(lane, fleet=d)
    mod._check(res.summary == (2, 2, 0, 0, 0), f"summary={res.summary}")


def case_fence_close_trailing_space(mod):
    """a closing run may carry trailing whitespace"""
    d = os.path.join(W, "c_closews")
    shutil.rmtree(d, ignore_errors=True)
    lane = os.path.join(d, "demo-shokunin")
    w(lane + "/corpus/SOURCES.md", REG +
      "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n"
      "```\n| S002 | https://e.example/2 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n```  \n"
      "| S003 | https://e.example/3 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    w(lane + "/corpus/knowledge/a.md", "Cites S001, S002 and S003.\n")
    res = mod.evaluate(lane, fleet=d)
    mod._check(res.summary == (3, 2, 1, 0, 1), f"summary={res.summary}")


def case_registry_url_only_from_source_cell(mod):
    """url-match uses the source cell only; a URL in a later cell is not a source URL"""
    d = os.path.join(W, "c_urllater")
    shutil.rmtree(d, ignore_errors=True)
    lane = os.path.join(d, "demo-shokunin")
    w(lane + "/corpus/SOURCES.md", REG + "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    w(lane + "/corpus/knowledge/a.md", "Cites S700, see https://a.example/7\n")
    w(os.path.join(d, "alpha-shokunin", "corpus/SOURCES.md"),
      REG + "| S700 | t | docs | A | s | a | x | mined | 2026-10-25 | 90d | https://a.example/7 |\n")
    res = mod.evaluate(lane, fleet=d)
    mod._check(res.dangling[0][3] == [], f"url-match={res.dangling[0][3]}")


def case_only_md_knowledge_files(mod):
    """a .markdown file is not a knowledge file"""
    d = os.path.join(W, "c_mdonly")
    shutil.rmtree(d, ignore_errors=True)
    lane = os.path.join(d, "demo-shokunin")
    w(lane + "/corpus/SOURCES.md", REG + "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    w(lane + "/corpus/knowledge/a.markdown", "Cites S001 and S777.\n")
    res = mod.evaluate(lane, fleet=d)
    mod._check(res.status == 2, f"status={res.status} error={res.error}")


def case_default_fleet_is_parent_of_root(mod):
    """without --fleet the fleet root is the parent of --root, so the sibling is found"""
    d = os.path.join(W, "c_defaultfleet")
    shutil.rmtree(d, ignore_errors=True)
    fleet = os.path.join(d, "fleet")
    lane = os.path.join(fleet, "demo-shokunin")
    w(lane + "/corpus/SOURCES.md", REG + "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    w(lane + "/corpus/knowledge/a.md", "Cites S700.\n")
    w(os.path.join(fleet, "alpha-shokunin", "corpus/SOURCES.md"),
      REG + "| S700 | https://a.example/7 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    res = mod.evaluate(lane)
    mod._check(res.dangling[0][2] == ["alpha-shokunin"], f"owners={res.dangling[0][2]}")


def case_revision_empty_knowledge_is_unevaluable(mod):
    """a revision with no knowledge file is unevaluable, never clean"""
    d = os.path.join(W, "c_emptyrev")
    shutil.rmtree(d, ignore_errors=True)
    lane = os.path.join(d, "demo-shokunin")
    w(lane + "/corpus/SOURCES.md", REG + "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    git(lane, "init", "-q")
    git(lane, "add", "-A")
    git(lane, "-c", "user.name=selftest", "-c", "user.email=selftest@local", "-c", "commit.gpgsign=false",
        "commit", "-q", "-m", "f")
    head = git(lane, "rev-parse", "HEAD").stdout.decode().strip()
    res = mod.evaluate(lane, revision=head, fleet=d)
    mod._check(res.status == 2 and "knowledge" in (res.error or ""), f"status={res.status} error={res.error}")


def case_revision_must_be_a_commit(mod):
    """a revision that is not a commit is unevaluable"""
    d = os.path.join(W, "c_tree")
    shutil.rmtree(d, ignore_errors=True)
    lane = os.path.join(d, "demo-shokunin")
    w(lane + "/corpus/SOURCES.md", REG + "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    w(lane + "/corpus/knowledge/a.md", "Cites S001.\n")
    git(lane, "init", "-q")
    git(lane, "add", "-A")
    git(lane, "-c", "user.name=selftest", "-c", "user.email=selftest@local", "-c", "commit.gpgsign=false",
        "commit", "-q", "-m", "f")
    head = git(lane, "rev-parse", "HEAD").stdout.decode().strip()
    tree = git(lane, "rev-parse", head + "^{tree}").stdout.decode().strip()
    res = mod.evaluate(lane, revision=tree, fleet=d)
    mod._check(res.status == 2 and res.error, f"status={res.status} error={res.error}")


def case_revision_knowledge_prefix_needs_separator(mod):
    """corpus/knowledge-notes/ is not under corpus/knowledge/"""
    d = os.path.join(W, "c_prefix")
    shutil.rmtree(d, ignore_errors=True)
    lane = os.path.join(d, "demo-shokunin")
    w(lane + "/corpus/SOURCES.md", REG + "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    w(lane + "/corpus/knowledge/a.md", "Cites S001.\n")
    w(lane + "/corpus/knowledge-notes/b.md", "Cites S777.\n")
    git(lane, "init", "-q")
    git(lane, "add", "-A")
    git(lane, "-c", "user.name=selftest", "-c", "user.email=selftest@local", "-c", "commit.gpgsign=false",
        "commit", "-q", "-m", "f")
    head = git(lane, "rev-parse", "HEAD").stdout.decode().strip()
    res = mod.evaluate(lane, revision=head, fleet=d)
    mod._check(res.summary == (1, 1, 0, 0, 0), f"summary={res.summary}")


def case_linked_worktree_sibling_read_at_head(mod):
    """a sibling that is a linked git worktree is read at HEAD, not at its dirty file"""
    d = os.path.join(W, "c_worktree")
    shutil.rmtree(d, ignore_errors=True)
    fleet = os.path.join(d, "fleet")
    lane = os.path.join(fleet, "demo-shokunin")
    w(lane + "/corpus/SOURCES.md", REG + "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    w(lane + "/corpus/knowledge/a.md", "Cites S777.\n")
    main_repo = os.path.join(fleet, "alpha-shokunin")
    w(main_repo + "/corpus/SOURCES.md", REG + "| S777 | https://a.example/7 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    git(main_repo, "init", "-q")
    git(main_repo, "add", "-A")
    git(main_repo, "-c", "user.name=selftest", "-c", "user.email=selftest@local", "-c", "commit.gpgsign=false",
        "commit", "-q", "-m", "f")
    linked = os.path.join(fleet, "beta-shokunin")
    rc = git(main_repo, "worktree", "add", "-q", linked).returncode
    if rc != 0:
        raise AssertionError("git worktree add failed")
    w(linked + "/corpus/SOURCES.md", REG + "| S999 | https://b.example/9 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    res = mod.evaluate(lane, fleet=fleet)
    mod._check(res.dangling[0][2] == ["alpha-shokunin", "beta-shokunin"], f"owners={res.dangling[0][2]}")


def case_unowned_count_is_not_the_dangling_count(mod):
    """the summary prints unowned = dangling - owned_elsewhere"""
    d = os.path.join(W, "c_unowned")
    shutil.rmtree(d, ignore_errors=True)
    lane = os.path.join(d, "demo-shokunin")
    w(lane + "/corpus/SOURCES.md", REG + "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    w(lane + "/corpus/knowledge/a.md", "Cites S700 and S800.\n")
    w(os.path.join(d, "alpha-shokunin", "corpus/SOURCES.md"),
      REG + "| S700 | https://a.example/7 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    res = mod.evaluate(lane, fleet=d)
    lines = mod.render(res)
    mod._check(lines[-1].endswith("owned_elsewhere=1 unowned=1"), f"line={lines[-1]}")


def case_non_utf8_knowledge_path_at_revision(mod):
    """a non-UTF-8 knowledge file name at a revision is read, not fatal"""
    d = os.path.join(W, "c_nonutf8")
    shutil.rmtree(d, ignore_errors=True)
    lane = os.path.join(d, "demo-shokunin")
    w(lane + "/corpus/SOURCES.md", REG + "| S001 | https://e.example/1 | docs | A | s | a | x | mined | 2026-10-25 | 90d | - |\n")
    w(lane + "/corpus/knowledge/ok.md", "Cites S001.\n")
    bad = os.path.join(os.fsencode(lane), b"corpus/knowledge/bad\xff.md")
    os.makedirs(os.path.dirname(bad), exist_ok=True)
    with open(bad, "wb") as fh:
        fh.write(b"Cites S900.\n")
    git(lane, "init", "-q")
    git(lane, "add", "-A")
    git(lane, "-c", "user.name=selftest", "-c", "user.email=selftest@local", "-c", "commit.gpgsign=false",
        "commit", "-q", "-m", "f")
    head = git(lane, "rev-parse", "HEAD").stdout.decode().strip()
    res = mod.evaluate(lane, revision=head, fleet=d)
    mod._check(res.status == 1, f"status={res.status} error={res.error}")
    mod._check(res.summary == (2, 1, 1, 0, 1), f"summary={res.summary}")


CANDIDATES = {
    "M03": case_registry_level3_heading,
    "M04": case_fence_indent_four_is_code,
    "M06": case_fence_char_must_match,
    "M07": case_fence_info_string_no_backtick,
    "M35": case_fence_close_trailing_space,
    "M09": case_registry_url_only_from_source_cell,
    "M11": case_only_md_knowledge_files,
    "M22": case_default_fleet_is_parent_of_root,
    "M31": case_revision_empty_knowledge_is_unevaluable,
    "M17": case_revision_must_be_a_commit,
    "M33": case_revision_knowledge_prefix_needs_separator,
    "M34": case_linked_worktree_sibling_read_at_head,
    "M37": case_unowned_count_is_not_the_dangling_count,
    "M14": case_non_utf8_knowledge_path_at_revision,
}


def main():
    os.makedirs(W, exist_ok=True)
    os.makedirs(os.path.join(W, "tmp"), exist_ok=True)
    for mid, fn in CANDIDATES.items():
        results = {}
        for label, path in (("pristine", SRC), ("mutant", os.path.join(W, "..", "..", "work", f"{mid}.py"))):
            if not os.path.exists(path):
                results[label] = "MISSING"
                continue
            mod = load(path, f"m_{label}_{mid}")
            try:
                fn(mod)
            except Exception as exc:
                results[label] = f"FAIL({type(exc).__name__}: {exc})"[:120]
            else:
                results[label] = "PASS"
        verdict = ("KILLS" if results.get("pristine") == "PASS" and results.get("mutant", "").startswith("FAIL")
                   else "does-not-kill")
        print(f"{mid} {verdict:14s} pristine={results.get('pristine')} mutant={results.get('mutant')}")


if __name__ == "__main__":
    main()
