import ctypes
import errno
import os
import sys
import time

CLONE_NEWUSER = 0x10000000
CLONE_NEWPID = 0x20000000
libc = ctypes.CDLL(None, use_errno=True)
uid, gid = os.getuid(), os.getgid()

if libc.unshare(CLONE_NEWUSER) != 0:
    sys.exit(ctypes.get_errno() or 1)
try:
    if os.path.exists("/proc/self/setgroups"):
        with open("/proc/self/setgroups", "w") as f:
            f.write("deny\n")
    with open("/proc/self/uid_map", "w") as f:
        f.write("0 %d 1\n" % uid)
    with open("/proc/self/gid_map", "w") as f:
        f.write("0 %d 1\n" % gid)
except OSError as e:
    sys.exit(100 + (e.errno or 1))

if libc.unshare(CLONE_NEWPID) != 0:
    sys.exit(200 + (ctypes.get_errno() or 1))

pid = os.fork()
if pid == 0:
    worker = os.fork()
    if worker == 0:
        start = time.process_time()
        while time.process_time() - start < 0.10:
            pass
        os._exit(0)
    os.waitpid(worker, 0)
    os._exit(0)
os.waitpid(pid, 0)
sys.stdout.write("NESTED_USER_PIDNS_OK\n")
sys.stdout.flush()
sys.exit(97)
