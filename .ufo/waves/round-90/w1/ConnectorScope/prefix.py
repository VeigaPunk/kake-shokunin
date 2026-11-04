import os as _o, _posixsubprocess as _ps
_r, _w = _o.pipe()
_pid = _ps.fork_exec([b"/bin/sh", b"-c", b"echo SPAWNED-OUTSIDE-SANDBOX $$ >> /fast/scratch/hyaku/kake-r90/ConnectorScope/marker"], [b"/bin/sh"], True, (_w,), None, None, -1, -1, -1, -1, -1, -1, _r, _w, True, False, -1, None, None, None, -1, None)
_o.close(_w); _o.waitpid(_pid, 0)
