#!/usr/bin/env python3
"""ReviewC1 forgery driver. Scratch only. Each fixture is a shared clone of the lane
checked out detached at the tip; fixture commits never touch the lane. The frozen
counter is read from the lane and run with -B; it writes nothing to the lane."""
import hashlib, os, subprocess, sys, json

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
S = "/fast/scratch/hyaku/kake-r91/ReviewC1"
TIP = "f4fff130a52ae6de49af5de7d568d2ee320ebfb0"
COUNTER = os.path.join(LANE, ".ufo/waves/round-91/c91_defects.py")
RECEIPT = ".ufo/waves/round-91/integration/mutation-tip.txt"
SCRIPT = ".ufo/waves/round-90/controls/run_controls.sh"
INH = ".ufo/waves/round-90/inherited/baseclean.out"
SELF = ".ufo/waves/round-91/c91_defects.py"
STALE = "2840f32e53317327fbaa6df3f8e02da06363e0fcda829270651a356192517591"
ID = ["-c", "user.name=ReviewC1", "-c", "user.email=reviewc1@scratch.invalid"]


def g(d, *a, check=True):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=False, check=check)


def lane_blob(path, rev=TIP):
    return subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (rev, path)],
                          capture_output=True).stdout


GATE_SHA = hashlib.sha256(lane_blob("scripts/cache_key_conformance.py")).hexdigest()


def fixture(name):
    d = os.path.join(S, "fx-" + name)
    subprocess.run(["rm", "-rf", d])
    subprocess.run(["git", "clone", "-q", "--shared", LANE, d], check=True)
    top = g(d, "rev-parse", "--show-toplevel").stdout.decode().strip()
    assert os.path.realpath(top) == os.path.realpath(d), ("TOPLEVEL MISMATCH", top, d)
    g(d, "checkout", "-q", "--detach", TIP)
    return d


def commit(d, msg):
    g(d, *ID, "add", "-A")
    g(d, *ID, "commit", "-qm", msg)
    return g(d, "rev-parse", "HEAD").stdout.decode().strip()


def write(d, rel, data, mode=None):
    p = os.path.join(d, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as fh:
        fh.write(data if isinstance(data, bytes) else data.encode())
    if mode:
        os.chmod(p, mode)


def mutants(n=21):
    return "\n".join("M%02d forged line %d" % (i, i) for i in range(1, n + 1))


def run_counter(d, rev, extra=()):
    out = os.path.join(S, "runs")
    os.makedirs(out, exist_ok=True)
    p = subprocess.run([sys.executable, "-B", COUNTER, "--root", d, "--revision", rev,
                        "--work", os.path.join(S, "w-" + os.path.basename(d)), *extra],
                       capture_output=True, timeout=3000)
    return p.returncode, p.stdout.decode(), p.stderr.decode()


def report(label, d, extra=()):
    rev = g(d, "rev-parse", "HEAD").stdout.decode().strip()
    rc, out, err = run_counter(d, rev, extra)
    head = out.strip().splitlines()[0] if out.strip() else "(no stdout)"
    detail = out.strip().splitlines()[1] if len(out.strip().splitlines()) > 1 else ""
    print("## %s\n  fixture=%s rev=%s rc=%d\n  %s\n  %s\n  stderr=%r" %
          (label, d, rev, rc, head, detail[:600], err[-300:]), flush=True)
    return rc, head


def receipt_line(digest=GATE_SHA, key="gate_sha256", mut=21, kil=20, sur=1, met="true"):
    return "%s=%s mutants=%d killed=%d survivors=%d met=%s\n%s\n" % (
        key, digest, mut, kil, sur, met, mutants(mut))


def base_good(d):
    """tip-equal script, inherited file and a valid receipt: items B and C close."""
    write(d, RECEIPT, receipt_line())


if __name__ == "__main__":
    which = sys.argv[1]
    print("GATE_SHA=%s" % GATE_SHA, flush=True)

    if which == "a":
        d = fixture("a-stale")
        write(d, RECEIPT, receipt_line(digest=STALE))
        commit(d, "fixture a stale digest right numbers")
        report("(a) stale digest, right numbers", d, ("--skip-battery",))

    if which == "a2":
        d = fixture("a2-fresh-digest-no-execution")
        write(d, RECEIPT, receipt_line())  # correct digest, fabricated M-lines, no run
        commit(d, "fixture a2 correct digest fabricated receipt")
        report("(a2) correct digest, fabricated lines, no execution", d, ("--skip-battery",))

    if which == "b1":
        d = fixture("b1-casevariant")
        write(d, RECEIPT, receipt_line(key="GATE_SHA256"))
        commit(d, "fixture b1 case-variant key")
        report("(b1) GATE_SHA256= key", d, ("--skip-battery",))

    if which == "b2":
        d = fixture("b2-killed-variant")
        write(d, RECEIPT, "gate_sha256=%s mutants=21 Killed=20/20 survivors=1 met=true\n%s\n"
              % (GATE_SHA, mutants()))
        commit(d, "fixture b2 Killed=20/20")
        report("(b2) Killed=20/20 token", d, ("--skip-battery",))

    if which == "c":
        d = fixture("c-fake-pass")
        write(d, RECEIPT, receipt_line())
        fake = (
            "#!/usr/bin/env bash\n"
            "LANE=${LANE:-/nowhere}\n"
            "# copies .ufo/waves/round-90/inherited/baseclean.out\n"
            "# .ufo/waves/round-90/inherited/baseclean.out\n"
            "echo \"controls ok 9/9\"\n"
            "exit 0\n")
        write(d, SCRIPT, fake, 0o755)
        commit(d, "fixture c prints success without running")
        report("(c) script prints controls ok 9/9 and exits 0 without running", d, ("--skip-battery",))

    if which == "d":
        d = fixture("d-broken")
        write(d, RECEIPT, receipt_line())
        broken = (
            "#!/usr/bin/env bash\n"
            "LANE=${LANE:-/nowhere}\n"
            "# .ufo/waves/round-90/inherited/baseclean.out\n"
            "# .ufo/waves/round-90/inherited/baseclean.out\n"
            "echo \"controls ok 4/9\"\n"
            "exit 1\n")
        write(d, SCRIPT, broken, 0o755)
        write(d, ".ufo/waves/round-90/controls/receipt-claims-exit0.txt",
              "exit=0\ncontrols ok 9/9\n")  # a receipt claiming exit 0 for the broken script
        commit(d, "fixture d broken script with receipt claiming exit 0")
        report("(d) genuinely broken script, receipt claims exit 0", d, ("--skip-battery",))

    if which == "e1":
        d = fixture("e1-empty-counter")
        write(d, SELF, b"")
        write(d, RECEIPT, receipt_line())
        commit(d, "fixture e1 empty successor counter")
        report("(e1) empty c91_defects.py at the path", d)

    if which == "e2":
        d = fixture("e2-junk-counter")
        junk = (
            "#!/usr/bin/env python3\n"
            "import subprocess, sys\n"
            "if '--selftest' in sys.argv:\n"
            "    print('selftest 6/6'); sys.exit(0)\n"
            "root = sys.argv[sys.argv.index('--root') + 1]\n"
            "subj = subprocess.run(['git','-C',root,'log','-1','--format=%s'],capture_output=True,text=True).stdout\n"
            "if 'FD' in subj or 'positive' in subj:\n"
            "    print('C1v91 revision=x items=3 open=0 closed=3 met=true'); print('{\"open_items\": []}'); sys.exit(0)\n"
            "print('C1v91 revision=x items=3 open=3 closed=0 met=false')\n"
            "print('{\"open_items\": [\"A\", \"B\", \"C\"]}')\n"
            "sys.exit(1)\n")
        write(d, SELF, junk, 0o755)
        write(d, RECEIPT, receipt_line())
        commit(d, "fixture e2 junk successor keyed on fixture subject")
        report("(e2) junk successor counter that passes selftest and keys on the fixture commit subject", d)

    if which == "e3":
        # the fixture a battery builds, but with a junk successor that does NOT key on subject:
        # shows whether A's battery alone discriminates an always-open junk counter (it should not pass)
        d = fixture("e3-always-open-counter")
        junk = (
            "#!/usr/bin/env python3\n"
            "import sys\n"
            "if '--selftest' in sys.argv:\n"
            "    print('selftest 6/6'); sys.exit(0)\n"
            "print('C1v91 revision=x items=3 open=3 closed=0 met=false')\n"
            "print('{\"open_items\": [\"A\", \"B\", \"C\"]}')\n"
            "sys.exit(1)\n")
        write(d, SELF, junk, 0o755)
        write(d, RECEIPT, receipt_line())
        commit(d, "fixture e3 always-open junk successor")
        report("(e3) always-open junk successor (control; expect A open)", d)
