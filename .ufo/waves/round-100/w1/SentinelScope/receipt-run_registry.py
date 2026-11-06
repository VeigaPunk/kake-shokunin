"""Scored fixtures for the REAL c100_registry.score() (imported read-only, no bytecode).
Usage: python3 -B run_registry.py <fixture-name>...   (env R100_FAKE_BWRAP=1 puts a failing bwrap first on PATH)
Fixture repos live under rg/fx/<name> (own git repo; identity via -c flags). Scored work dir: rg/w-<name>."""
import importlib.util, os, shutil, socket, subprocess, sys, threading, time, hashlib
sys.dont_write_bytecode = True
COUNTER = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-100/c100_registry.py"
spec = importlib.util.spec_from_file_location("c100r", COUNTER)
m = importlib.util.module_from_spec(spec)
sys.modules["c100r"] = m
spec.loader.exec_module(m)

BASE = "/fast/scratch/hyaku/kake-r100/SentinelScope/rg"
SRC = BASE + "/src/"
H = "| Name | Kind | Entry command | Verdict map | Self-test | Write scope | Owner |\n|---|---|---|---|---|---|---|\n"


def row(name, path, vm, st, owner="kake"):
    return "| %s | gate | `python3 -B %s` | %s | %s | none | %s |\n" % (name, path, vm, st, owner)


ST_A = "`python3 -B scripts/a.py --selftest`"
VM2 = "`0=ok`; `1=bad`"
VM3 = "`0=ok`; `1=bad`; `64=usage`"
FIX = {
    "control-honest": ({"scripts/a.py": "honest.py"}, row("a", "scripts/a.py", VM3, ST_A)),
    "control-noflag": ({"scripts/a.py": "honest.py"}, row("a", "scripts/a.py", VM2, ST_A)),
    "probeaware": ({"scripts/a.py": "probeaware.py"}, row("a", "scripts/a.py", VM2, ST_A)),
    "selfrewrite": ({"scripts/a.py": "selfrewrite.py"}, row("a", "scripts/a.py", VM2, ST_A)),
    "crossrow": ({"scripts/a.py": "crossrow_a.py", "scripts/crossrow_b.py": "crossrow_b.py"},
                 row("a", "scripts/a.py", VM2, ST_A) + row("b", "scripts/crossrow_b.py", VM2, "no self-test")),
    "crossrow-clean": ({"scripts/a.py": "crossrow_a.py", "scripts/crossrow_b.py": "crossrow_b.py"},
                       row("a", "scripts/a.py", VM3, ST_A) + row("b", "scripts/crossrow_b.py", VM2, "no self-test")),
    "detect": ({"scripts/a.py": "detect.py"}, row("a", "scripts/a.py", VM2, ST_A)),
    "evidence": ({"scripts/a.py": "evidence.py"}, row("a", "scripts/a.py", VM2, ST_A)),
    "outlive": ({"scripts/a.py": "outlive.py"}, row("a", "scripts/a.py", VM2, ST_A)),
    "disk": ({"scripts/a.py": "disk.py"}, row("a", "scripts/a.py", VM2, ST_A)),
    "symlink": ({"scripts/a.py": "symlink.py"}, row("a", "scripts/a.py", VM3, ST_A)),
    "oracle-visible": ({"scripts/a.py": "oracle_read.py", ".ufo/waves/round-100/c100_registry.py": "c100_registry_copy.py", ".ufo/waves/round-100/c100_fresh304.py": "c100_fresh304_copy.py"}, row("a", "scripts/a.py", VM3, ST_A)),
    "hang": ({"scripts/a.py": "hang.py"}, row("a", "scripts/a.py", VM2, ST_A)),
    "fail-open": ({"scripts/crossrow_b.py": "crossrow_b.py"}, row("b", "scripts/crossrow_b.py", VM2, "no self-test")),
}


def build(name):
    files, rows = FIX[name]
    D = os.path.join(BASE, "fx", name)
    shutil.rmtree(D, ignore_errors=True)
    os.makedirs(D)
    subprocess.run(["git", "-C", D, "init", "-q"], check=True)
    top = subprocess.run(["git", "-C", D, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(D), top
    for p, src in files.items():
        os.makedirs(os.path.join(D, os.path.dirname(p)), exist_ok=True)
        shutil.copy(SRC + src, os.path.join(D, p))
    open(os.path.join(D, "SKILL.md"), "w").write(H + rows)
    subprocess.run(["git", "-C", D, "add", "-A"], check=True)
    subprocess.run(["git", "-C", D, "-c", "user.name=SentinelScope", "-c", "user.email=SentinelScope@example.invalid",
                    "commit", "-q", "-m", "fixture " + name], check=True)
    return D


srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("127.0.0.1", 18766))
srv.listen(8)


def _serve():
    while True:
        c, _ = srv.accept()
        c.sendall(b"HOST")
        c.close()


threading.Thread(target=_serve, daemon=True).start()
ab = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
ab.bind("\0r100-sentinel-abs2")
ab.listen(4)

ctl = subprocess.Popen(["/usr/bin/python3", "-c", "import time;time.sleep(59)", "r100-sentinel-hostctl"])
time.sleep(0.3)
print("pgrep_control_sees_host_marker:", bool(subprocess.run(["pgrep", "-f", "r100-sentinel-hostctl"], capture_output=True, text=True).stdout.strip()))
ctl.kill()
ctl.wait()

if os.environ.get("R100_FAKE_BWRAP"):
    fb = BASE + "/fakebin"
    os.environ["PATH"] = fb + ":" + os.environ["PATH"]
    print("PATH_PREPENDED", fb, "bwrap_resolves_to", shutil.which("bwrap"))

for name in sys.argv[1:]:
    D = build(name)
    W = os.path.join(BASE, "w-" + name)
    shutil.rmtree(W, ignore_errors=True)
    os.makedirs(W)
    t0 = time.time()
    met, text = m.score(D, "HEAD", W)
    dt = round(time.time() - t0, 1)
    print("=== fixture %s met=%s elapsed=%ss" % (name, met, dt))
    print(text)
    if name == "fail-open":
        tree = os.path.join(W, "tree")
        print("direct probe rc of scripts/crossrow_b.py under this bwrap:", m.probe("scripts/crossrow_b.py", tree, W, [100]))
    surv = subprocess.run(["pgrep", "-fa", "r100-sentinel"], capture_output=True, text=True).stdout.strip()
    print("host_survivors:", repr(surv))
    if surv:
        subprocess.run(["pkill", "-f", "r100-sentinel-fx8"])
        print("killed_survivors(marker-only)")
    ev = os.path.join(W, "tree", "evidence.txt")
    if os.path.exists(ev):
        print("evidence.txt:", open(ev).read())
    for rel in ["scripts/a.py", "scripts/crossrow_b.py", "bigfile.bin", "planted-link-dir", "planted-link-file"]:
        p = os.path.join(W, "tree", rel)
        if os.path.lexists(p):
            if os.path.islink(p):
                print("tree-symlink", rel, "->", os.readlink(p))
            else:
                print("tree-file", rel, "size", os.path.getsize(p), "sha256", hashlib.sha256(open(p, "rb").read()[:4096]).hexdigest()[:12])
    committed = subprocess.run(["git", "-C", D, "show", "HEAD:scripts/a.py"], capture_output=True).stdout
    print("committed scripts/a.py sha256", hashlib.sha256(committed).hexdigest()[:12] if committed else "absent")
    if name == "symlink":
        shutil.rmtree(W)  # exactly what c100_registry.main() does in its finally
        print("after counter-style rmtree(work): victim.txt exists =", os.path.exists(BASE + "/victim-dir/victim.txt"),
              "victim-dir exists =", os.path.isdir(BASE + "/victim-dir"))
    print()
