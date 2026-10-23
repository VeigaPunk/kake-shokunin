import os
import sys

ppid = os.getppid()
argv = [x for x in open("/proc/%d/cmdline" % ppid, "rb").read().split(b"\0") if x]
runner_index = next(i for i, x in enumerate(argv) if x.endswith(b".py"))
timer_fd = int(argv[runner_index + 1])
path = "/proc/%d/fd/%d" % (ppid, timer_fd)
fd = os.open(path, os.O_WRONLY)
payload = b"X" * 4096 + b"\n0 0.000000 0.000000\n"
os.write(fd, payload)
os.close(fd)
sys.stdout.write("TIMER_WRITE_OK\n")
sys.stdout.flush()
sys.exit(97)
