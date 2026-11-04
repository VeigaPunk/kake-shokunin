#!/usr/bin/env python3
"""Is the control score load-sensitive? Same bytes, same seed, under load."""
import importlib.util, multiprocessing, pathlib, subprocess, sys, time

S = pathlib.Path('/fast/scratch/hyaku/kake-r89/MutKey')
spec = importlib.util.spec_from_file_location('cf', S / 'counter-frozen/c89_key.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

log = []
real = m.run_candidate
def wrapper(path, payload, work, timeout=30):
    try:
        p = real(path, payload, work, timeout)
        log.append(('rc', p.returncode, p.stderr.strip()[:80]))
        return p
    except subprocess.TimeoutExpired as e:
        log.append(('timeout', None, str(e)[:80]))
        raise
m.run_candidate = wrapper

src = (S / 'counter-frozen/controls/ctl-constant-key.py').read_bytes()

def spin():
    end = time.time() + 25
    x = 0
    while time.time() < end:
        x = (x * 1103515245 + 12345) % 2147483648

if __name__ == '__main__':
    procs = [multiprocessing.Process(target=spin) for _ in range(32)]
    for p in procs: p.start()
    t0 = time.time()
    frozen, props, refuse, fails = m.score_candidate(src, S / 'work/loadprobe', 89089)
    dt = time.time() - t0
    for p in procs: p.terminate()
    kinds = {}
    for k, rc, err in log:
        kinds[k] = kinds.get(k, 0) + 1
    print(f'under load: frozen={frozen} props={props} refuse={refuse} runs={len(log)} '
          f'kinds={kinds} wall={dt:.1f}s')
    print('first fails:', fails[:3])
    print('sample outcomes:', log[:4])
    log.clear()
    frozen, props, refuse, fails = m.score_candidate(src, S / 'work/loadprobe-quiet', 89089)
    print(f'unloaded:   frozen={frozen} props={props} refuse={refuse} runs={len(log)}')
    print('sample outcomes:', log[:4])
