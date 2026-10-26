#!/usr/bin/env python3
"""Derive the six junk resolver tools (plus one extra probe) from the shipped candidate.

Base artifact: scripts/id_resolver.py at lane revision 4b8c73050470ada9e6583f3b12d659d1bed6a17f.
Each junk file injects exactly one defect; every injected defect leaves the tool's own
`--selftest` (33 cases) green, so the gate's G2 stays PASS and the differential conditions
G3/G4/G5 are the only ones that can see the defect. Each replacement is asserted to apply
exactly once, so a silent no-op variant is impossible.

Usage: python3 -B make_junk.py <source id_resolver.py> <out dir>
"""
import sys
import os

BASE = "4b8c73050470ada9e6583f3b12d659d1bed6a17f"

RENDER_OLD = '''def render(result):
    lines = []
    for sid, paths, owners, matched in result.dangling:
        lines.append(
            f"DANGLING {sid} cited-by={','.join(paths)} "
            f"owners={','.join(owners) or '-'} url-match={','.join(matched) or '-'}"
        )
    cited_n, resolved, dangling, owned, unowned = result.summary
    lines.append(
        f"ids_cited={cited_n} ids_resolved={resolved} dangling={dangling} "
        f"owned_elsewhere={owned} unowned={unowned}"
    )
    return lines
'''

MAIN_OLD = '''    result = evaluate(args.root, args.revision, args.fleet)
    if result.status == 2:
        print(f"id_resolver: unevaluable: {result.error}", file=sys.stderr)
        return 2
    for line in render(result):
        print(line)
    return result.status
'''

CONST_NEW = '''    for sid, path in (
        ("S367", "corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md"),
        ("S372", "corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md"),
        ("S373", "corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md"),
        ("S390", "corpus/knowledge/baidu-friendly-crawl-guidance.md"),
        ("S409", "corpus/knowledge/baidu-friendly-crawl-guidance.md"),
    ):
        print(f"DANGLING {sid} cited-by={path} owners=kotodama-shokunin url-match=-")
    print("ids_cited=105 ids_resolved=100 dangling=5 owned_elsewhere=5 unowned=0")
    return 1
'''

WORKTREE_NEW = '''    result = evaluate(args.root, None, args.fleet)  # DEFECT: --revision ignored, working tree read
    if result.status == 2:
        print(f"id_resolver: unevaluable: {result.error}", file=sys.stderr)
        return 2
    for line in render(result):
        print(line)
    return result.status
'''

NOFLEET_NEW = '''    result = evaluate(args.root, args.revision, None)  # DEFECT: --fleet ignored, parent of --root used
    if result.status == 2:
        print(f"id_resolver: unevaluable: {result.error}", file=sys.stderr)
        return 2
    for line in render(result):
        print(line)
    return result.status
'''

DEFAULTGUARD_NEW = '''    if not args.fleet:  # DEFECT: the documented default (parent of --root) is not implemented
        print("usage: id_resolver.py --root <lane> --revision <rev> --fleet <fleet root>", file=sys.stderr)
        return 64
    result = evaluate(args.root, args.revision, args.fleet)
    if result.status == 2:
        print(f"id_resolver: unevaluable: {result.error}", file=sys.stderr)
        return 2
    for line in render(result):
        print(line)
    return result.status
'''

UNSORTED_NEW = '''def render(result):
    lines = []
    for sid, paths, owners, matched in reversed(result.dangling):  # DEFECT: line order reversed
        lines.append(
            f"DANGLING {sid} cited-by={','.join(reversed(paths))} "
            f"owners={','.join(reversed(owners)) or '-'} url-match={','.join(reversed(matched)) or '-'}"
        )
    cited_n, resolved, dangling, owned, unowned = result.summary
    lines.append(
        f"ids_cited={cited_n} ids_resolved={resolved} dangling={dangling} "
        f"owned_elsewhere={owned} unowned={unowned}"
    )
    return lines
'''

NOURL_NEW = '''def render(result):
    lines = []
    for sid, paths, owners, matched in result.dangling:
        lines.append(
            f"DANGLING {sid} cited-by={','.join(paths)} "
            f"owners={','.join(owners) or '-'} url-match=-"  # DEFECT: url-match never reported
        )
    cited_n, resolved, dangling, owned, unowned = result.summary
    lines.append(
        f"ids_cited={cited_n} ids_resolved={resolved} dangling={dangling} "
        f"owned_elsewhere={owned} unowned={unowned}"
    )
    return lines
'''

OFFBYONE_NEW = '''def render(result):
    lines = []
    for sid, paths, owners, matched in result.dangling:
        lines.append(
            f"DANGLING {sid} cited-by={','.join(paths)} "
            f"owners={','.join(owners) or '-'} url-match={','.join(matched) or '-'}"
        )
    cited_n, resolved, dangling, owned, unowned = result.summary
    lines.append(
        f"ids_cited={cited_n} ids_resolved={resolved} dangling={dangling} "
        f"owned_elsewhere={owned + 1} unowned={unowned}"  # DEFECT: owned_elsewhere off by one
    )
    return lines
'''

VARIANTS = [
    ("junk_const.py", "a constant printer: prints the round-52 red block and a fixed summary, exit 1",
     [("MAIN", MAIN_OLD, CONST_NEW)]),
    ("junk_worktree.py", "reads the working tree instead of --revision (CLI-level)",
     [("MAIN", MAIN_OLD, WORKTREE_NEW)]),
    ("junk_nofleet.py", "ignores --fleet and uses the parent of --root",
     [("MAIN", MAIN_OLD, NOFLEET_NEW)]),
    ("junk_unsorted.py", "reverse-sorted DANGLING line order, cited-by, owners and url-match",
     [("RENDER", RENDER_OLD, UNSORTED_NEW)]),
    ("junk_nourl.py", "url-match is always `-`",
     [("RENDER", RENDER_OLD, NOURL_NEW)]),
    ("junk_offbyone.py", "owned_elsewhere printed as owned+1",
     [("RENDER", RENDER_OLD, OFFBYONE_NEW)]),
    ("probe_defaultfleet.py", "extra probe: default --fleet (parent of --root) not implemented",
     [("MAIN", MAIN_OLD, DEFAULTGUARD_NEW)]),
]


def main(argv):
    if len(argv) != 3:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 64
    src, out = argv[1], argv[2]
    text = open(src, encoding="utf-8").read()
    os.makedirs(out, exist_ok=True)
    for name, why, edits in VARIANTS:
        body = text
        for label, old, new in edits:
            n = body.count(old)
            if n != 1:
                print(f"{name}: anchor {label} matched {n} times, refusing", file=sys.stderr)
                return 1
            body = body.replace(old, new)
        header = (
            f"# JUNK VARIANT of scripts/id_resolver.py @ {BASE[:12]}\n"
            f"# defect (single): {why}\n"
            f"# generated by ExecGateFlake/make_junk.py; --selftest is unchanged (33 cases)\n"
        )
        with open(os.path.join(out, name), "w", encoding="utf-8") as handle:
            handle.write(header + body)
        print(f"wrote {name}: {why}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
