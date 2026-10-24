import ctypes
import os
import resource
import sys
import time

CLONE_NEWPID = 0x20000000
libc = ctypes.CDLL(None, use_errno=True)
if libc.unshare(CLONE_NEWPID) != 0:
    sys.exit(ctypes.get_errno() or 1)

pid = os.fork()
if pid == 0:
    # This child is PID 1 in the new namespace; its child runs 0.10 CPU s.
    worker = os.fork()
    if worker == 0:
        start = time.process_time()
        while time.process_time() - start < 0.10:
            pass
        os._exit(0)
    os.waitpid(worker, 0)
    os._exit(0)
os.waitpid(pid, 0)
sys.stdout.write("NESTED_PIDNS_OK\n")
sys.stdout.flush()
sys.exit(97)
