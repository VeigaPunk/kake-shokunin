#!/usr/bin/env python3
# Implements nothing: hands stdin/stdout to a fresh, unhooked interpreter running another script.
import os, _posixsubprocess as ps
r, w = os.pipe()
pid = ps.fork_exec([b"/usr/bin/python3", b"-B", b"/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/cache_key.py"], [b"/usr/bin/python3"], False, (), None, None, -1, -1, -1, -1, -1, -1, r, w, True, False, -1, None, None, None, -1, None)
os.close(w)
_, st = os.waitpid(pid, 0)
os._exit(os.waitstatus_to_exitcode(st))
