#!/usr/bin/env python3
"""DP blowup probe 2 — states stay wide, failure decided late."""
import importlib.util, os, subprocess, time, tempfile

spec = importlib.util.spec_from_file_location(
    "ag", "/fast/scratch/hyaku/kake-r60/SentinelGuard/lane/scripts/append_guard.py")
ag = importlib.util.module_from_spec(spec); spec.loader.exec_module(ag)
S = os.environ["TMPDIR"]
SC = [ag.scope_regex(p) for p in ag.DEFAULT_SCOPE]

def count_states(base, rev):
    """Instrumented copy of any_clean_alignment: peak states and step count."""
    m = len(base)
    tagged = [ag.line_is_tagged(r, b"\x00" * len(r)) for r in rev]
    states = {(0, False)}
    peak, steps = len(states), 0
    for j, r in enumerate(rev):
        nxt = set()
        for i, in_run in states:
            if i < m and r == base[i]:
                nxt.add((i + 1, False))
            if in_run or i == m or tagged[j]:
                nxt.add((i, True))
        steps += len(states)
        states = nxt
        peak = max(peak, len(states))
        if not states:
            return False, peak, steps, j
    return any(i == m for i, _ in states), peak, steps, len(rev)

for n in (500, 1000, 2000, 4000):
    base = [b"x"] * (n - 1) + [b"z"]
    rev = [b"x"] * (n - 1) + [b"untagged"] + [b"z"]
    t0 = time.monotonic()
    ok, peak, steps, upto = count_states(base, rev)
    dt = time.monotonic() - t0
    print(f"fail-late n={n}: clean={ok} peak_states={peak} state_steps={steps} "
          f"died_at_line={upto} wall={dt:.2f}s")

for n in (1000, 2000, 4000):
    tag = b"[r60-correction 2026-10-27] fix"
    base = [b"x"] * n
    rev = [b"x"] * n + [tag]
    t0 = time.monotonic()
    ok, peak, steps, upto = count_states(base, rev)
    dt = time.monotonic() - t0
    print(f"clean-eof-append n={n}: clean={ok} peak_states={peak} "
          f"state_steps={steps} wall={dt:.2f}s")
