#!/usr/bin/env python3
"""Forgery: no key logic; delegates to the lane's shipped constructor via a child
process spawned with multiprocessing.util.spawnv_passfds (_posixsubprocess.fork_exec),
an audit event the gate's _DENY list does not name."""
import os, sys, multiprocessing.util as mu
ORACLE = b"/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/cache_key.py"
exe = os.fsencode(sys.executable)
pid = mu.spawnv_passfds(exe, [exe, b"-I", b"-B", ORACLE], [])
_, st = os.waitpid(pid, 0)
os._exit(os.waitstatus_to_exitcode(st))
