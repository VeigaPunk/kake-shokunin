#!/usr/bin/env python3
"""Reference re-implementation of the contract C1 rules, for pre-freeze recon only.

NOT the lane tool. Used by SentinelC1Bounds to test whether the contract's own
real-lane expectation (receipts=144 events=<k> undisclosed=0) can hold.
"""
import os, re, subprocess, sys, json

DETECT = re.compile(r"(?im)^\s*#\s*receipt\s*:|EXIT=|^VERDICT:")
SPAN = re.compile(r"(?im)(^#\s*receipt\s*:|revision\s*[:=]|EXIT\s*=|met\s*=|conditions_passed|"
                  r"cases_passed|findings\s*=|scores_held|members\s*=)")
PENDING = re.compile(r"(?i)\bpending\b")


def env():
    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    e.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    return e


def git(root, *args):
    return subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "-C", root, *args],
                          env=env(), capture_output=True, check=False, timeout=120)


def read(root, rev, path):
    d = git(root, "cat-file", "blob", f"{rev}:{path}")
    return d.stdout if d.returncode == 0 else None


def span_lines(text):
    return [m.group(0).strip() for m in SPAN.finditer(text)]


def main():
    root, rev, pop = sys.argv[1], sys.argv[2], sys.argv[3]
    paths = [l.strip() for l in open(pop, encoding="utf-8") if l.strip()]
    receipts, events, undisclosed, missing = [], [], [], []
    for p in paths:
        log = git(root, "log", "--first-parent", "--full-history", "--reverse",
                  "--format=%H", rev, "--", p)
        commits = [c for c in log.stdout.decode().split() if c]
        if not commits:
            missing.append(p)
            continue
        add, later = commits[0], commits[1:]
        first = read(root, add, p)
        if first is None:
            missing.append(p)
            continue
        ftext = first.decode("utf-8", "surrogateescape")
        if not DETECT.search(ftext):
            continue
        receipts.append(p)
        body = ftext
        prev_span = span_lines(ftext)
        was_pending = bool(PENDING.search(" ".join(prev_span)))
        for c in later:
            cur = read(root, c, p)
            if cur is None:
                continue
            ctext = cur.decode("utf-8", "surrogateescape")
            cur_span = span_lines(ctext)
            if cur_span != prev_span:
                kind = "pending_filled" if (was_pending and not PENDING.search(" ".join(cur_span))) else "rewrite"
                events.append((kind, p, c))
                was_pending = bool(PENDING.search(" ".join(cur_span)))
            prev_span = cur_span
    print(f"population={len(paths)} receipts={len(receipts)} events={len(events)} "
          f"missing={len(missing)} undisclosed={len(events)}")
    for kind, p, c in events:
        print(f"undisclosed_{kind} {p} {c[:12]}")
    for p in missing[:5]:
        print(f"absent-path {p}")


main()
