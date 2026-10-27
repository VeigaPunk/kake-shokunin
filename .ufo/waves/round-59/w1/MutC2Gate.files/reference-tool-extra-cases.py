def case_html_comment_row_not_registered():
    with _tmpdir() as base:
        lane = os.path.join(base, "demo-shokunin")
        text = _registry([("S001", "https://e.example/1")]).replace(
            "## Paths", "<!--" + NL + "| S960 | https://e.example/960 |" + NL + "-->" + NL + "## Paths")
        _write(os.path.join(lane, REGISTRY_REL), text)
        _write(os.path.join(lane, KNOWLEDGE_REL, "a.md"), "Cites S001 and S960." + NL)
        res = _summary(lane, fleet=base)
        _check(res.summary == (2, 1, 1, 0, 1), f"summary={res.summary}")
        _check([row[0] for row in res.dangling] == ["S960"], f"dangling={res.dangling}")


def case_setext_heading_ends_registry():
    with _tmpdir() as base:
        lane = os.path.join(base, "demo-shokunin")
        text = _registry([("S001", "https://e.example/1")]).replace(
            "## Paths", "Subsection" + NL + "---" + NL + NL + "| S961 | https://e.example/961 |" + NL + "## Paths")
        _write(os.path.join(lane, REGISTRY_REL), text)
        _write(os.path.join(lane, KNOWLEDGE_REL, "a.md"), "Cites S001 and S961." + NL)
        res = _summary(lane, fleet=base)
        _check(res.summary == (2, 1, 1, 0, 1), f"summary={res.summary}")
        _check([row[0] for row in res.dangling] == ["S961"], f"dangling={res.dangling}")


def case_in_lane_symlinked_dir_is_read():
    with _tmpdir() as base:
        lane = os.path.join(base, "demo-shokunin")
        _write(os.path.join(lane, REGISTRY_REL), _registry([("S001", "https://e.example/1")]))
        _write(os.path.join(lane, KNOWLEDGE_REL, "a.md"), "Cites S001." + NL)
        _write(os.path.join(lane, "notes_store", "hidden.md"), "Cites S962." + NL)
        os.symlink("../../notes_store", os.path.join(lane, KNOWLEDGE_REL, "linked"))
        res = _summary(lane, fleet=base)
        _check(res.summary == (2, 1, 1, 0, 1), f"summary={res.summary}")
        _check([row[0] for row in res.dangling] == ["S962"], f"dangling={res.dangling}")


def case_revision_symlink_resolved_in_tree():
    with _tmpdir() as base:
        lane = _repo(os.path.join(base, "demo-shokunin"))
        rev = _commit(lane, {REGISTRY_REL: _registry([("S001", "https://e.example/1")]),
                             KNOWLEDGE_REL + "/a.md": "Cites S001." + NL,
                             "corpus/notes.md": "Cites S963." + NL})
        os.symlink("../notes.md", os.path.join(lane, KNOWLEDGE_REL, "linked.md"))
        _git_ok(["git", "-C", lane, "add", "-A"])
        _git_ok(["git", "-C", lane, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
                  "-c", "commit.gpgsign=false", "commit", "-q", "-m", "link"])
        rev2 = _git_ok(["git", "-C", lane, "rev-parse", "HEAD"]).strip()
        res = _summary(lane, revision=rev2, fleet=base)
        _check(res.summary == (2, 1, 1, 0, 1), f"summary={res.summary}")
        _check([row[0] for row in res.dangling] == ["S963"], f"dangling={res.dangling}")


def case_revision_dangling_symlink_carries_no_citation():
    with _tmpdir() as base:
        lane = _repo(os.path.join(base, "demo-shokunin"))
        _commit(lane, {REGISTRY_REL: _registry([("S001", "https://e.example/1")]),
                       KNOWLEDGE_REL + "/a.md": "Cites S001." + NL})
        os.symlink("S964-target.md", os.path.join(lane, KNOWLEDGE_REL, "odd.md"))
        _git_ok(["git", "-C", lane, "add", "-A"])
        _git_ok(["git", "-C", lane, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
                  "-c", "commit.gpgsign=false", "commit", "-q", "-m", "link"])
        rev2 = _git_ok(["git", "-C", lane, "rev-parse", "HEAD"]).strip()
        res = _summary(lane, revision=rev2, fleet=base)
        _check(res.summary == (1, 1, 0, 0, 0), f"summary={res.summary}")


def case_registry_symlink_outside_lane_is_unevaluable():
    with _tmpdir() as base:
        lane = os.path.join(base, "demo-shokunin")
        outside = os.path.join(base, "outside.md")
        _write(outside, _registry([("S001", "https://e.example/1"), ("S965", "https://e.example/965")]))
        _write(os.path.join(lane, KNOWLEDGE_REL, "a.md"), "Cites S001 and S965." + NL)
        os.symlink(outside, os.path.join(lane, REGISTRY_REL))
        res = _summary(lane, fleet=base)
        _check(res.status == 2 and "outside" in (res.error or ""), f"status={res.status} error={res.error}")


def case_non_utf8_path_at_revision():
    with _tmpdir() as base:
        lane = _repo(os.path.join(base, "demo-shokunin"))
        _commit(lane, {REGISTRY_REL: _registry([("S001", "https://e.example/1")]),
                       KNOWLEDGE_REL + "/a.md": "Cites S001." + NL})
        bad = os.path.join(os.fsencode(lane), b"corpus/knowledge/bad\xff.md")
        os.makedirs(os.path.dirname(bad), exist_ok=True)
        with open(bad, "wb") as fh:
            fh.write(b"Cites S966." + b"\n")
        _git_ok(["git", "-C", lane, "add", "-A"])
        _git_ok(["git", "-C", lane, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
                  "-c", "commit.gpgsign=false", "commit", "-q", "-m", "bad name"])
        rev2 = _git_ok(["git", "-C", lane, "rev-parse", "HEAD"]).strip()
        res = _summary(lane, revision=rev2, fleet=base)
        _check(res.status == 1, f"status={res.status} error={res.error}")
        _check(res.summary == (2, 1, 1, 0, 1), f"summary={res.summary}")
        _check([row[0] for row in res.dangling] == ["S966"], f"dangling={res.dangling}")


def case_non_toplevel_root_is_unevaluable():
    with _tmpdir() as base:
        repo_root = os.path.join(base, "anc")
        _repo(repo_root)
        _write(os.path.join(repo_root, REGISTRY_REL), _registry([("S001", "https://e.example/1")]))
        _write(os.path.join(repo_root, KNOWLEDGE_REL, "a.md"), "Cites S001." + NL)
        _write(os.path.join(repo_root, "lane", KNOWLEDGE_REL, "a.md"), "Cites S001." + NL)
        _commit(repo_root, {"README.md": "r" + NL})
        rev2 = _git_ok(["git", "-C", repo_root, "rev-parse", "HEAD"]).strip()
        res = _summary(os.path.join(repo_root, "lane"), revision=rev2, fleet=base)
        _check(res.status == 2 and "toplevel" in (res.error or ""), f"status={res.status} error={res.error}")


EXTRA_CASES = [
    ("a row inside an HTML comment does not register", case_html_comment_row_not_registered),
    ("a setext heading ends the Registry section", case_setext_heading_ends_registry),
    ("an in-lane symlinked knowledge directory is read", case_in_lane_symlinked_dir_is_read),
    ("a committed symlink is resolved inside the tree", case_revision_symlink_resolved_in_tree),
    ("a dangling committed symlink carries no citation", case_revision_dangling_symlink_carries_no_citation),
    ("a registry symlinked out of the lane is unevaluable", case_registry_symlink_outside_lane_is_unevaluable),
    ("a non-UTF-8 knowledge path is read at a revision", case_non_utf8_path_at_revision),
    ("a --root below a repository toplevel is unevaluable", case_non_toplevel_root_is_unevaluable),
]
