import os, sys, _posixsubprocess
o = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "cache_key.py")
data = sys.stdin.buffer.read()
i_r, i_w = os.pipe(); o_r, o_w = os.pipe(); e_r, e_w = os.pipe(); x_r, x_w = os.pipe()
pid = _posixsubprocess.fork_exec([b"/usr/bin/python3", o.encode()], (b"/usr/bin/python3",), True, (x_w,), None, None,
    i_r, i_w, o_r, o_w, e_r, e_w, x_r, x_w, True, False, -1, None, None, None, -1, None)
for f in (i_r, o_w, e_w, x_w): os.close(f)
os.write(i_w, data); os.close(i_w)
out = b""
while True:
    b = os.read(o_r, 65536)
    if not b: break
    out += b
err = b""
while True:
    b = os.read(e_r, 65536)
    if not b: break
    err += b
_, st = os.waitpid(pid, 0)
sys.stdout.buffer.write(out); sys.stderr.buffer.write(err)
sys.exit(os.waitstatus_to_exitcode(st))
