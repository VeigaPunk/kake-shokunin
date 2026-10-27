#!/usr/bin/env python3
"""SentinelC1Exec probe harness for round-60 w2 (C1 counter execution safety).

Read-only w.r.t. the lane: it clones the lane with `git clone --shared` into WORK and reads the
counter from the clone at B1.  Every fixture, scratch dir and marker file lives under WORK.

usage: python3 -B probe_all.py <WORK> [lane]
"""
import glob
import importlib.util
import json
import os
import shutil
import signal
import socket
import subprocess
import sys
import time

WORK = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "./probe-sentinelc1exec")
LANE = sys.argv[2] if len(sys.argv) > 2 else "/home/vgpnk/Projects/shokunin/kake-shokunin"
B1 = "8b33fd248d126b48d838af5c38bc175850f41a09"


def sh(*args, **kw):
    return subprocess.run(args, capture_output=True, text=True, **kw)


def fresh(path):
    shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path)
    return path


def load_counter(path):
    spec = importlib.util.spec_from_file_location("c60", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def init_repo(d, files, msg="fixture"):
    """git init in d (asserted toplevel) + one commit holding `files`."""
    os.makedirs(d, exist_ok=True)
    sh("git", "-C", d, "init", "-q")
    top = sh("git", "-C", d, "rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    for name, data in files.items():
        with open(os.path.join(d, name), "w") as fh:
            fh.write(data)
    sh("git", "-C", d, "add", "-A")
    sh("git", "-C", d, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
       "commit", "-qm", msg)
    return sh("git", "-C", d, "rev-parse", "HEAD").stdout.strip()


def commit(d, files, msg="more"):
    for name, data in files.items():
        with open(os.path.join(d, name), "w") as fh:
            fh.write(data)
    sh("git", "-C", d, "add", "-A")
    sh("git", "-C", d, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
       "commit", "-qm", msg)
    return sh("git", "-C", d, "rev-parse", "HEAD").stdout.strip()


def head(work):
    print("\n== 0. counter source and clone")
    clone = os.path.join(work, "lane")
    if not os.path.isdir(clone + "/.git"):
        sh("git", "clone", "-q", "--shared", LANE, clone)
    sh("git", "-C", clone, "checkout", "-q", "--detach", B1)
    top = sh("git", "-C", clone, "rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(clone)
    counter = os.path.join(clone, ".ufo/waves/round-60/c60_gate_status.py")
    print("clone toplevel:", top, "| B1:", sh("git", "-C", clone, "rev-parse", "HEAD").stdout.strip())
    print("counter blobs identical to lane:",
          sh("git", "-C", clone, "hash-object", counter).stdout.strip() ==
          sh("git", "-C", LANE, "hash-object",
             LANE + "/.ufo/waves/round-60/c60_gate_status.py").stdout.strip())
    return counter


def env_probe(c60, fx, tip, work):
    print("\n== 1. env scrub: hostile parent env, sitecustomize/.pth in the clone")
    evil = fresh(os.path.join(work, "evil"))
    marker = os.path.join(work, "probe")
    os.makedirs(marker, exist_ok=True)
    sitesrc = 'open(%r,"w").write("x")\n' % os.path.join(marker, "SITECUSTOMIZE_LEAK")
    for name in ("sitecustomize.py", "usercustomize.py"):
        with open(os.path.join(evil, name), "w") as fh:
            fh.write(sitesrc)
    with open(os.path.join(evil, "leak.pth"), "w") as fh:
        fh.write('import os; open(%r,"w").write("x")\n' % os.path.join(marker, "PTH_LEAK"))
    os.environ["PYTHONPATH"] = evil
    os.environ["PYTHONSTARTUP"] = os.path.join(evil, "sitecustomize.py")
    out = os.path.join(marker, "env.json")
    rc = c60.run_member(fx, ["python3", "-B", "env_m.py", out, "--revision", "<commit>"],
                        "env_m.py", tip, os.path.join(work, "runs"))
    rec = json.load(open(out))
    print("rc=%s env=%s" % (rc, rec["env"]))
    print("cwd=%s exists_after_run=%s" % (rec["cwd"], os.path.isdir(rec["cwd"])))
    print("writable lane .git=%s writable outside clone=%s" %
          (rec["writable_lane"], rec["writable_scratch_sibling"]))
    print("sitecustomize leak=%s .pth leak=%s" %
          (os.path.exists(os.path.join(marker, "SITECUSTOMIZE_LEAK")),
           os.path.exists(os.path.join(marker, "PTH_LEAK"))))
    os.environ.pop("PYTHONPATH")
    os.environ.pop("PYTHONSTARTUP")


def escape_probe(c60, fx, tip, work):
    print("\n== 2. member writes outside its clone; locked dir blocks cleanup")
    marker = os.path.join(work, "probe", "ESCAPED_WRITE")
    if os.path.exists(marker):
        os.remove(marker)
    rc = c60.run_member(fx, ["python3", "-B", "env_m.py", "--revision", "<commit>"],
                        "env_m.py", tip, os.path.join(work, "runs"))
    left = glob.glob(os.path.join(work, "runs", "c60-run-*"))
    print("rc=%s wrote %s: %s | leftovers: %s" % (rc, marker, os.path.exists(marker),
                                                  [os.path.basename(x) for x in left]))
    print("-- 2b. a member that leaves an unreadable dir makes rmtree() fail silently")
    rc = c60.run_member(fx, ["python3", "-B", "locked_m.py", "--revision", "<commit>"],
                        "locked_m.py", tip, os.path.join(work, "runs"))
    left = glob.glob(os.path.join(work, "runs", "c60-run-*"))
    print("locked_m rc=%s leftovers=%s (normal run, no signal, no timeout)" %
          (rc, [os.path.basename(x) for x in left]))
    for x in left:
        shutil.rmtree(os.path.join(x, "clone"), ignore_errors=True)
        sh("chmod", "-R", "u+rwX", x)
        shutil.rmtree(x, ignore_errors=True)


def socket_probe(c60, fx, tip, work):
    print("\n== 3. member may open sockets (docstring says 'No network')")
    marker = os.path.join(work, "probe", "NET_OK")
    if os.path.exists(marker):
        os.remove(marker)
    rc = c60.run_member(fx, ["python3", "-B", "net_m.py", "--revision", "<commit>"],
                        "net_m.py", tip, os.path.join(work, "runs"))
    print("rc=%s socket bind+connect=%s" % (rc, os.path.exists(marker)))


def process_probe(c60, fx, tip, work):
    print("\n== 4. process containment: forked daemon, timeout, orphaned grandchild")
    pidfile = os.path.join(work, "probe", "daemon.pid")
    rc = c60.run_member(fx, ["python3", "-B", "fork_m.py", "--revision", "<commit>"],
                        "fork_m.py", tip, os.path.join(work, "runs"))
    pid = int(open(pidfile).read())
    alive = os.path.isdir("/proc/%d" % pid)
    print("fork_m rc=%s daemon alive after run_member returned: %s cwd=%s" %
          (rc, alive, os.readlink("/proc/%d/cwd" % pid) if alive else "-"))
    if alive:
        os.kill(pid, 9)
    c60.TIMEOUT = 5
    for name in ("loop_m.py", "loopfork_m.py"):
        gpid_f = os.path.join(work, "probe", "grandchild.pid")
        if os.path.exists(gpid_f):
            os.remove(gpid_f)
        t = time.time()
        rc = c60.run_member(fx, ["python3", "-B", name, "--revision", "<commit>"], name, tip,
                            os.path.join(work, "runs"))
        left = glob.glob(os.path.join(work, "runs", "c60-run-*"))
        extra = ""
        if os.path.exists(gpid_f):
            gpid = int(open(gpid_f).read())
            extra = " grandchild alive=%s ppid=%s" % (
                os.path.isdir("/proc/%d" % gpid),
                open("/proc/%d/stat" % gpid).read().split()[3] if os.path.isdir("/proc/%d" % gpid) else "-")
            if os.path.isdir("/proc/%d" % gpid):
                os.kill(gpid, 9)
        print("%s rc=%s %.1fs leftovers=%s%s" % (name, rc, time.time() - t,
                                                 [os.path.basename(x) for x in left], extra))


def classify_probe(c60, work):
    print("\n== 5. a hung observation is scored as a LABEL mismatch, never unevaluable")
    fx = fresh(os.path.join(work, "fx2"))
    pin = init_repo(fx, {"slow.py": "import time\nwhile True: time.sleep(0.2)\n"}, "pin")
    tip = commit(fx, {"t.txt": "tuned\n"})
    c60.TIMEOUT = 3
    head_row = ("| Name | Kind | Entry command | Verdict map | Self-test | Proof | Write scope | Owner |\n"
                "|---|---|---|---|---|---|---|---|\n")
    for kind in ("historical %s" % pin, "never met %s" % pin, "live"):
        skill = head_row + ("| slow | %s | `python3 -B slow.py --root . --revision <commit>` | "
                            "`0=met`; `1=not met` | x | x | x | kake |\n" % kind)
        res = c60.eval_member("slow.py", c60.md_tables(skill), skill, fx, tip,
                              os.path.join(work, "runs"))
        print("kind=%-14s e_T=%s e_P=%s classes=%s" %
              (kind.split()[0], res["e_T"], res["e_P"], res["classes"]))
    print("first_class of a timeout verdict:", c60.first_class(["historical_bad_exit"]))


def argv_probe(c60):
    print("\n== 6. argv shape check: no injection, but free-form flags/paths accepted")
    for words, env, name in [
        (["python3", "-B", "m.py", "--revision", "<commit>"], {}, "baseline"),
        (["python3", "-B", "m.py", "--revision", "<commit>", "--work",
          "/home/vgpnk/Projects/shokunin/kake-shokunin"], {}, "lane path as flag value"),
        (["python3", "-B", "m.py", "--revision", "<commit>", "--out", "../../"], {}, "relative escape"),
        (["python3", "-B", "m.py", "--revision", "<commit>", "&&", "true"], {}, "metachar"),
        (["python3", "-B", "m.py", "--revision", "<commit>", "--selftest"], {}, "selftest"),
        (["python3", "-B", "m.py", "--revision", "<commit>"],
         {"PYTHONPATH": "/x"}, "env word"),
        (["python3", "-B", "m.py", "--revision", "<commit>", "--fleet", "<fleet root>"], {},
         "fleet root arg"),
    ]:
        print("%-22s -> %r" % (name, c60.validate_command(words, env, "m.py")))
    print("argv injection of a placeholder inside a word:",
          repr(c60.validate_command(["python3", "-B", "m.py", "--revision", "<commit>",
                                     "--work=<scratch>"], {}, "m.py")))


def cleanup_probe(counter, fx, tip, work):
    print("\n== 7. --work cleanup deletes foreign c60-run-* / c60-self-* dirs")
    shared = fresh(os.path.join(work, "shared"))
    keep = os.path.join(shared, "c60-run-KEEPME")
    os.makedirs(keep)
    open(os.path.join(keep, "important.txt"), "w").write("important\n")
    p = sh(sys.executable, "-B", counter, "--root", fx, "--revision", tip, "--work", shared)
    print("counter exit=%s | KEEPME still there: %s | shared now: %s" %
          (p.returncode, os.path.isdir(keep), sorted(os.listdir(shared))))

    print("\n== 8. work dir falls back to /tmp when TMPDIR is unset")
    os.environ.pop("TMPDIR", None)
    c60 = load_counter(counter)
    seen = {}

    def fake(root, revid, w, jobs):
        seen["work"] = w
        seen["live"] = os.path.isdir(w)
        return 1, [], 0, 0
    c60.measure = fake
    sys.argv = ["c60", "--root", fx, "--revision", tip]
    rc = c60.main()
    print("exit=%s work dir=%s existed=%s removed_after=%s" %
          (rc, seen.get("work"), seen.get("live"), not os.path.exists(seen.get("work", ""))))

    print("\n== 9. SIGTERM / SIGINT mid-run (real counter, real lane clone)")
    os.environ["TMPDIR"] = os.path.join(work, "tmpint")
    os.makedirs(os.environ["TMPDIR"], exist_ok=True)
    lane_clone = os.path.join(work, "lane")
    for sig in (signal.SIGTERM, signal.SIGINT):
        target = fresh(os.path.join(work, "sig_" + sig.name))
        p = subprocess.Popen([sys.executable, "-B", counter, "--root", lane_clone,
                              "--revision", B1, "--work", target, "--jobs", "2"],
                             stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
                             start_new_session=True)
        time.sleep(4)
        os.killpg(p.pid, sig)
        _out, err = p.communicate()
        print("%s exit=%s leftovers=%s stderr_last=%r" %
              (sig.name, p.returncode, sorted(os.listdir(target)),
               (err.strip().splitlines() or [""])[-1][:80]))
    # no --work: the work dir is a tempdir under TMPDIR and is only removed by main()'s finally
    p = subprocess.Popen([sys.executable, "-B", counter, "--root", lane_clone, "--revision", B1,
                          "--jobs", "2"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         start_new_session=True)
    time.sleep(4)
    os.killpg(p.pid, signal.SIGTERM)
    p.wait()
    print("SIGTERM without --work: exit=%s TMPDIR residue=%s" %
          (p.returncode, sorted(os.listdir(os.environ["TMPDIR"]))))


def git_arg_probe(counter, work):
    print("\n== 10. git argument injection attempts (no shell; git args are fixed / hex / --)")
    for args, name in [
        (["--root=--upload-pack=/bin/true", "--revision", B1], "root looks like a git option"),
        (["--root", LANE, "--revision=--all"], "revision looks like a git option"),
        (["--root", LANE, "--revision=--verify"], "revision = another option"),
    ]:
        p = sh(sys.executable, "-B", counter, *args)
        print("%-32s exit=%s out=%r" % (name, p.returncode, p.stdout.strip().splitlines()[:1]))


def crash_probe(counter, fx, tip, work):
    print("\n== 11. an unexpected exception is not 'unevaluable': the process exits 1 = 'not met'")
    driver = os.path.join(work, "crash_driver.py")
    with open(driver, "w") as fh:
        fh.write(
            "import importlib.util, sys\n"
            "spec = importlib.util.spec_from_file_location('c60', %r)\n"
            "c60 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c60)\n"
            "c60.measure = lambda *a, **k: (_ for _ in ()).throw(ValueError('logic error'))\n"
            "sys.argv = ['c60', '--root', %r, '--revision', %r]\n"
            "sys.exit(c60.main())\n" % (counter, fx, tip))
    p = sh(sys.executable, "-B", driver)
    print("exit=%s stderr_last=%r stdout=%r" %
          (p.returncode, (p.stderr.strip().splitlines() or [""])[-1][:60], p.stdout[-40:]))


def main():
    fresh(WORK)
    os.makedirs(os.path.join(WORK, "probe"), exist_ok=True)
    os.makedirs(os.path.join(WORK, "runs"), exist_ok=True)
    os.makedirs(os.path.join(WORK, "tmpint"), exist_ok=True)
    counter = head(WORK)
    c60 = load_counter(counter)

    fx = os.path.join(WORK, "fx")
    tip = init_repo(fx, {
        "sitecustomize.py": 'open(%r,"w").write("x")\n' % os.path.join(WORK, "probe", "SITE_AT_ROOT"),
        "env_m.py": (
            "import json, os, sys\n"
            "json.dump({'env': dict(os.environ), 'cwd': os.getcwd(), 'argv': sys.argv,\n"
            "           'writable_lane': os.access(%r, os.W_OK),\n"
            "           'writable_scratch_sibling': os.access(os.path.dirname(os.getcwd()), os.W_OK)},\n"
            "          open(sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].endswith('.json')\n"
            "               else '/dev/null', 'w'), indent=1)\n"
            "open(%r,'w').write('outside the clone\\n')\n"
            % (LANE + "/.git", os.path.join(WORK, "probe", "ESCAPED_WRITE"))),
        "locked_m.py": ("import os\n"
                        "d = os.path.join(os.getcwd(), 'locked'); os.makedirs(d, exist_ok=True)\n"
                        "open(os.path.join(d,'f'),'w').write('x'); os.chmod(d, 0o500)\n"),
        "net_m.py": ("import socket\n"
                     "s=socket.socket(); s.bind(('127.0.0.1',0)); s.listen(1)\n"
                     "c=socket.create_connection(s.getsockname(),2); c.close(); s.close()\n"
                     "open(%r,'w').write('ok\\n')\n" % os.path.join(WORK, "probe", "NET_OK")),
        "fork_m.py": ("import os, sys, time\n"
                      "pid=os.fork()\n"
                      "if pid==0:\n"
                      "    os.setsid()\n"
                      "    p2=os.fork()\n"
                      "    if p2>0: os._exit(0)\n"
                      "    open(%r,'w').write(str(os.getpid()))\n"
                      "    time.sleep(120); os._exit(0)\n"
                      "os.waitpid(pid,0); sys.exit(0)\n" % os.path.join(WORK, "probe", "daemon.pid")),
        "loop_m.py": "import time\nwhile True: time.sleep(0.2)\n",
        "loopfork_m.py": ("import os, time\n"
                          "pid=os.fork()\n"
                          "if pid==0:\n"
                          "    open(%r,'w').write(str(os.getpid()))\n"
                          "    time.sleep(120); os._exit(0)\n"
                          "while True: time.sleep(0.2)\n" % os.path.join(WORK, "probe", "grandchild.pid")),
    }, "fixture")
    # env_m.py needs the json path as argv[1]; the first probe passes it explicitly
    env_probe(c60, fx, tip, WORK)
    escape_probe(c60, fx, tip, WORK)
    socket_probe(c60, fx, tip, WORK)
    process_probe(c60, fx, tip, WORK)
    classify_probe(c60, WORK)
    argv_probe(c60)
    cleanup_probe(counter, fx, tip, WORK)
    git_arg_probe(counter, WORK)
    crash_probe(counter, fx, tip, WORK)
    print("\nWORK =", WORK)


if __name__ == "__main__":
    main()
