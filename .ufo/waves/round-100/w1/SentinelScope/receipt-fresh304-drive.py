"""Drive the real C2 counter's SANDBOX / run_candidate from outside (read-only import; no bytecode).
Usage: python3 -B drive.py <scratch-work> <probe-file>...  Writes nothing into the lane."""
import importlib.util, os, socket, subprocess, sys, threading, time
sys.dont_write_bytecode = True
COUNTER = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-100/c100_fresh304.py"
spec = importlib.util.spec_from_file_location("c100f", COUNTER)
m = importlib.util.module_from_spec(spec)
sys.modules["c100f"] = m
spec.loader.exec_module(m)
work, probes = sys.argv[1], sys.argv[2:]
os.makedirs(work, exist_ok=True)
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("127.0.0.1", 18765)); srv.listen(8)
def _serve():
    while True:
        c, _ = srv.accept(); c.sendall(b"HOST"); c.close()
threading.Thread(target=_serve, daemon=True).start()
ab = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
ab.bind("\0r100-sentinel-abs"); ab.listen(4)
print("sandbox_ok=", m.sandbox_ok(work), flush=True)
for p in probes:
    t0 = time.time()
    rc, out, err = m.run_candidate(p, b"")
    dt = round(time.time() - t0, 2)
    print("== probe", os.path.basename(p), "rc=%s elapsed=%ss" % (rc, dt))
    print(out[:6000])
    if err:
        print("stderr:", err[:600])
    surv = subprocess.run(["pgrep", "-fa", "r100-sentinel"], capture_output=True, text=True).stdout.strip()
    print("host_survivors:", repr(surv))
    if surv:
        subprocess.run(["pkill", "-f", "r100-sentinel"])
        print("killed_survivors(marker-only)")
