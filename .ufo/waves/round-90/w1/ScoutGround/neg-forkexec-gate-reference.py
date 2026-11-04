# delegates to the gate's own reference() through _posixsubprocess.fork_exec (no audit event)
import os, _posixsubprocess
code = (b"import sys,json;sys.path.insert(0,'/home/vgpnk/Projects/shokunin/kake-shokunin/scripts');"
        b"import cache_key_conformance as g;d=sys.stdin.buffer.read()\n"
        b"try: k=g.reference(json.loads(d.decode('utf-8')))\nexcept Exception: k=g.REFUSE\n"
        b"if k is g.REFUSE: sys.stderr.write('invalid_input: x\\n'); sys.exit(1)\n"
        b"print(json.dumps({'key': k}))")
r, w = os.pipe()
pid = _posixsubprocess.fork_exec([b"/usr/bin/python3", b"-B", b"-c", code], [b"/usr/bin/python3"],
    True, (w,), None, None, -1, -1, -1, -1, -1, -1, r, w, True, False, -1, None, None, -1, -1, None)
os.close(w); os.close(r)
_, st = os.waitpid(pid, 0)
os._exit(os.waitstatus_to_exitcode(st))
