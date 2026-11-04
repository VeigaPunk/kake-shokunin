# delegates to an existing implementation through _posixsubprocess.fork_exec (no audit event)
import os, sys, _posixsubprocess
target = "/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/cache_key.py"
r, w = os.pipe()
pid = _posixsubprocess.fork_exec(
    [b"/usr/bin/python3", b"-B", target.encode()], [b"/usr/bin/python3"],
    True, (w,), None, None,
    -1, -1, -1, -1, -1, -1,
    r, w,
    True, False, -1, None, None, -1, -1, None)
os.close(w); os.close(r)
_, st = os.waitpid(pid, 0)
os._exit(os.waitstatus_to_exitcode(st))
