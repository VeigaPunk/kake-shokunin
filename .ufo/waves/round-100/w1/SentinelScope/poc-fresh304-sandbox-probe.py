#!/usr/bin/env python3
"""SentinelScope PoC (C2, c100_fresh304.py SANDBOX): candidate-side probes of the case sandbox.

Usage: python3 -B poc-fresh304-sandbox-probe.py --scratch DIR
Imports the REAL counter read-only and runs candidate programs through its own SANDBOX/run_candidate
(the same argv the counter uses). Checks: introspection of /proc, fds, env, mounts and namespaces;
writes (ro /usr, candidate file, tmpfs /tmp and /dev); network (host loopback listener and host
abstract socket, both started here on ephemeral ports; 1.1.1.1); outlive (detached daemons);
cross-case persistence (/tmp, /dev/shm); tmpfs and fork resource use (bounded: 2 GiB, 200 forks);
rlimits; sandbox_ok() fail-closed under a broken bind. Host survivors are scanned in /proc afterwards.
Writes only under --scratch; the only host processes it starts are its own listener and its own
bounded children."""
import argparse
import importlib.util
import json
import os
import socket
import sys
import threading
import time

sys.dont_write_bytecode = True
LANE_COUNTER = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-100/c100_fresh304.py"
MARK = "r100-sentinel-poc-"

PROBE = r'''
import os, sys, json, socket, errno, resource
out = {}
out["pid"] = os.getpid(); out["ppid"] = os.getppid(); out["cwd"] = os.getcwd()
out["env"] = dict(os.environ)
out["pids_visible"] = sorted(int(p) for p in os.listdir("/proc") if p.isdigit())
out["fds"] = {}
for fd in os.listdir("/proc/self/fd"):
    try: out["fds"][fd] = os.readlink("/proc/self/fd/" + fd)
    except OSError as e: out["fds"][fd] = "ERR " + str(e)
out["pid1_cmdline"] = open("/proc/1/cmdline", "rb").read().replace(b"\0", b" ").decode(errors="replace")[:400]
out["status"] = [l for l in open("/proc/self/status").read().splitlines() if l.startswith(("Cap", "NSpid", "Seccomp", "NoNewPrivs"))]
out["mountinfo_roots"] = [l.split(" - ")[0] for l in open("/proc/self/mountinfo").read().splitlines()][-3:]
w = {}
for p in ["/usr/poc_w", "/cand/freshen_304.py", "/tmp/poc_w", "/dev/poc_w", "/etc/poc_w"]:
    try: open(p, "w").write("x"); w[p] = "WROTE"
    except OSError as e: w[p] = errno.errorcode.get(e.errno, str(e.errno))
out["writes"] = w
out["host_paths"] = {p: os.path.exists(p) for p in ["/home", "/fast", "/run", "/var", "/root", "/etc/shadow"]}
net = {}
for name, fam, addr in [("tcp_1.1.1.1:53", socket.AF_INET, ("1.1.1.1", 53)),
                        ("tcp_host_loopback", socket.AF_INET, ("127.0.0.1", HOST_PORT)),
                        ("unix_abstract_host", socket.AF_UNIX, "\0" + ABSTRACT)]:
    s = socket.socket(fam, socket.SOCK_STREAM); s.settimeout(2)
    try: s.connect(addr); net[name] = "CONNECTED"
    except OSError as e: net[name] = type(e).__name__ + ":" + str(e.errno)
    finally: s.close()
out["net"] = net
out["rlimits"] = {n: resource.getrlimit(getattr(resource, n)) for n in ["RLIMIT_AS", "RLIMIT_NPROC", "RLIMIT_FSIZE", "RLIMIT_CPU"]}
print(json.dumps(out, indent=1, default=str))
'''

OUTLIVE = (
    "import os, time\n"
    "pid = os.fork()\n"
    "if pid == 0:\n"
    "    os.setsid()\n"
    "    os.execv('/usr/bin/python3', ['python3', '-c', 'import time;time.sleep(90)', '" + MARK + "outlive-a'])\n"
    "pid2 = os.fork()\n"
    "if pid2 == 0:\n"
    "    os.setsid()\n"
    "    if os.fork() == 0:\n"
    "        fd = os.open('/dev/null', os.O_RDWR)\n"
    "        [os.dup2(fd, k) for k in (0, 1, 2)]\n"
    "        os.execv('/usr/bin/python3', ['python3', '-c', 'import time;time.sleep(91)', '" + MARK + "outlive-b'])\n"
    "    os._exit(0)\n"
    "os.waitpid(pid2, 0)\n"
    "print('spawned')\n")

RESOURCE = (
    "import os, time\n"
    "buf = b'\\0' * (1 << 20)\n"
    "with open('/tmp/poc_big', 'wb') as f:\n"
    "    for _ in range(2048):\n"
    "        f.write(buf)\n"
    "st = os.statvfs('/tmp')\n"
    "pids = []\n"
    "for i in range(200):\n"
    "    p = os.fork()\n"
    "    if p == 0:\n"
    "        time.sleep(1); os._exit(0)\n"
    "    pids.append(p)\n"
    "for p in pids: os.waitpid(p, 0)\n"
    "print('tmp_total', st.f_blocks * st.f_frsize, 'wrote', os.path.getsize('/tmp/poc_big'), 'forks', len(pids))\n")

CROSS = (
    "import os\n"
    "print('before', sorted(os.listdir('/tmp')), sorted(os.listdir('/dev/shm')))\n"
    "open('/tmp/poc_marker', 'w').write('x')\n"
    "open('/dev/shm/poc_marker', 'w').write('x')\n")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def write(path, text):
    open(path, "w").write(text)
    return path


def scan(pat):
    hits = []
    me, parent = os.getpid(), os.getppid()
    for pid in os.listdir("/proc"):
        if not pid.isdigit() or int(pid) in (me, parent):
            continue
        try:
            cmd = open("/proc/%s/cmdline" % pid, "rb").read()
        except OSError:
            continue
        if pat.encode() in cmd:
            hits.append(int(pid))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    a = ap.parse_args()
    root = os.path.abspath(a.scratch)
    os.makedirs(root, exist_ok=True)
    m = load(LANE_COUNTER, "c100f")

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind(("127.0.0.1", 0))
    srv.listen(4)
    host_port = srv.getsockname()[1]
    ab = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    abstract = MARK + "abs"
    ab.bind("\0" + abstract)
    ab.listen(4)
    threading.Thread(target=lambda: [srv.accept()[0].close() for _ in iter(int, 1)], daemon=True).start()

    work = os.path.join(root, "work")
    os.makedirs(work, exist_ok=True)
    print("sandbox_ok:", m.sandbox_ok(work))

    def run(label, src, data=b""):
        path = write(os.path.join(root, label + ".py"), src)
        t0 = time.time()
        rc, out, err = m.run_candidate(path, data)
        dt = round(time.time() - t0, 2)
        print("== %s rc=%s elapsed=%ss" % (label, rc, dt))
        print(out[:3000] if label != "resource" else out)
        if err:
            print("stderr:", err[:300])
        return rc, out

    probe_src = PROBE.replace("HOST_PORT", str(host_port)).replace("ABSTRACT", repr(abstract))
    run("introspect", probe_src)
    run("outlive", OUTLIVE)
    time.sleep(1)
    print("host_survivors_after_outlive:", scan(MARK + "outlive"))
    run("resource", RESOURCE)
    run("cross-case-1", CROSS)
    run("cross-case-2", CROSS)
    print("survivors_after_all:", scan(MARK))

    # fail-closed: same SANDBOX list with a broken bind must make sandbox_ok() False (counter exits 2)
    saved = m.SANDBOX
    m.SANDBOX = ["bwrap", "--ro-bind", "/nonexistent-r100-src", "/nonexistent-r100-dst"] + saved[1:]
    print("sandbox_ok_with_broken_bind:", m.sandbox_ok(work))
    m.SANDBOX = saved
    srv.close()
    ab.close()


if __name__ == "__main__":
    sys.exit(main())
