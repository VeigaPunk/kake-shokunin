#!/usr/bin/env python3
"""ReviewC1 process attacks P1-P8. Runs AFTER driver.py; reads revs from runs/_summary_routes.json.
Writes receipts under runs/. Touches nothing outside the scratch root.

Exact script that produced receipts/runs/P*.txt: base source plus the two
recorded fixes (bare revision sha parsed from the harness line; P6b ok-check
expects verdict=clean because the verdict-only line carries no self_pin field).
"""
import hashlib, json, os, shutil, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
S    = "/fast/scratch/hyaku/kake-r96/ReviewC1"
FX   = S + "/fx"
RUNS = S + "/runs"
C96  = LANE + "/.ufo/waves/round-96/c96_selfassess.py"
BASE = "bde9869144f69c5a459c0d2c93f5135922fe3a8d"

def log(m): print(m, flush=True)

def sha(p):
    with open(p, "rb") as fh: return hashlib.sha256(fh.read()).hexdigest()

def receipt(name, cmd, rc, out, extra=""):
    with open(os.path.join(RUNS, name + ".txt"), "w") as fh:
        fh.write("# route: %s\n# command: %s\nrc=%s\n" % (name, cmd, rc))
        line1 = out.splitlines()[0] if out.splitlines() else ""
        fh.write("line1: %s\n" % line1)
        fh.write("stdout_tail: %s\n" % out[-500:].replace("\n", " | "))
        if extra: fh.write("note: %s\n" % extra)
    return line1

summary = json.load(open(os.path.join(RUNS, "_summary_routes.json")))
base_rev = [t for t in summary["harness"]["c96_base"]["line1"].split()
            if t.startswith("revision=")][0].split("=", 1)[1]
rx01_rev = summary["routes"]["RX01-decisions-only-in-html-comment"]["rev"]
res = {}

ENV0 = dict(os.environ); ENV0["PYTHONPATH"] = ""; ENV0["TMPDIR"] = S + "/tmp"

def run(cmd, env=None, cwd=None, timeout=900):
    p = subprocess.run(cmd, capture_output=True, timeout=timeout,
                       env=env or ENV0, cwd=cwd or S)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")

# ---- P1: effectful subprocess.py on PYTHONPATH from a non-script directory
p1 = S + "/p1shadow"; shutil.rmtree(p1, ignore_errors=True); os.makedirs(p1)
open(p1 + "/subprocess.py", "w").write(
    "open(%r,'w').write('shadow-ran')\nraise SystemExit(7)\n" % (p1 + "/MARKER"))
env = dict(ENV0); env["PYTHONPATH"] = p1
rc, out, err = run(["python3", "-B", C96, "--root", FX, "--revision", base_rev,
                    "--verdict-only"], env=env)
marker = os.path.exists(p1 + "/MARKER")
ok = (not marker) and rc == 0 and "verdict=clean" in out
receipt("P1-pythonpath-shadow", "PYTHONPATH=%s python3 -B c96 --root fx --revision %s --verdict-only" % (p1, base_rev[:12]), rc, out,
        "marker_written=%s stderr=%r verdict=%s" % (marker, err[:120], "clean" if "verdict=clean" in out else "?"))
res["P1"] = {"ok": ok, "marker": marker, "rc": rc}
log("[P1] rc=%d marker=%s -> %s" % (rc, marker, "PASS" if ok else "FAIL"))

# ---- P2: effectful subprocess.py in the working directory (cwd shadow)
p2 = S + "/p2cwd"; shutil.rmtree(p2, ignore_errors=True); os.makedirs(p2)
open(p2 + "/subprocess.py", "w").write(
    "open(%r,'w').write('shadow-ran')\nraise SystemExit(7)\n" % (p2 + "/MARKER"))
rc, out, err = run(["python3", "-B", C96, "--root", FX, "--revision", base_rev,
                    "--verdict-only"], cwd=p2)
marker = os.path.exists(p2 + "/MARKER")
ok = (not marker) and rc == 0 and "verdict=clean" in out
receipt("P2-cwd-shadow", "(cd %s && python3 -B c96 --root fx --revision %s --verdict-only)" % (p2, base_rev[:12]), rc, out,
        "marker_written=%s stderr=%r" % (marker, err[:120]))
res["P2"] = {"ok": ok, "marker": marker, "rc": rc}
log("[P2] rc=%d marker=%s -> %s" % (rc, marker, "PASS" if ok else "FAIL"))

# ---- P3: effectful subprocess.py beside the counter COPY (script dir shadow)
p3 = S + "/p3beside"; shutil.rmtree(p3, ignore_errors=True); os.makedirs(p3 + "/frozen")
shutil.copyfile(C96, p3 + "/c96.py")
shutil.copyfile(LANE + "/.ufo/waves/round-96/frozen/c1-surfaces.json", p3 + "/frozen/c1-surfaces.json")
open(p3 + "/subprocess.py", "w").write(
    "open(%r,'w').write('shadow-ran')\nraise SystemExit(7)\n" % (p3 + "/MARKER"))
copy_before = sha(p3 + "/c96.py")
rc, out, err = run(["python3", "-B", p3 + "/c96.py", "--root", FX,
                    "--revision", base_rev, "--verdict-only"], cwd=p3)
marker = os.path.exists(p3 + "/MARKER")
copy_after = sha(p3 + "/c96.py")
true_digest = "a282da654d5ee6af923abb2cae4bd0a4fd6e4309db81de5a67999ed7b25ad134"
ok = (not marker) and rc == 0 and copy_before == copy_after == true_digest and "verdict=clean" in out
receipt("P3-effectful-beside-counter-copy",
        "cp c96 %s/c96.py + subprocess.py; python3 -B %s/c96.py --root fx --revision %s --verdict-only" % (p3, p3, base_rev[:12]),
        rc, out, "marker=%s copy_sha_before=%s after=%s (true=%s)" % (marker, copy_before[:12], copy_after[:12], true_digest[:12]))
res["P3"] = {"ok": ok, "marker": marker, "rc": rc}
log("[P3] rc=%d marker=%s -> %s" % (rc, marker, "PASS" if ok else "FAIL"))

# ---- P4: --surfaces-file must be refused (exit 2)
rc, out, err = run(["python3", "-B", C96, "--root", FX, "--revision", base_rev,
                    "--surfaces-file", "x.json"])
ok = rc == 2 and "surfaces-file" in (err + out)
receipt("P4-surfaces-file-refusal", "c96 --root fx --revision %s --surfaces-file x.json" % base_rev[:12],
        rc, out, "stderr=%r" % err[:200])
res["P4"] = {"ok": ok, "rc": rc}
log("[P4] rc=%d -> %s" % (rc, "PASS" if ok else "FAIL"))

# ---- P5: --verdict-only can never print met=true
rc, out, err = run(["python3", "-B", C96, "--root", FX, "--revision", base_rev,
                    "--verdict-only"])
ok = rc == 0 and "met=n/a" in out and "met=true" not in out and "verdict=clean" in out
receipt("P5-verdict-only-never-met-true", "c96 --root fx --revision %s --verdict-only (clean lane state)" % base_rev[:12],
        rc, out, "met=true present: %s" % ("met=true" in out))
res["P5"] = {"ok": ok, "rc": rc}
log("[P5] rc=%d met=true-in-out=%s -> %s" % (rc, "met=true" in out, "PASS" if ok else "FAIL"))

# ---- P6: --self-pin mismatch exit 2; correct pin ok
rc, out, err = run(["python3", "-B", C96, "--root", FX, "--revision", base_rev,
                    "--verdict-only", "--self-pin", "0" * 64])
ok_a = rc == 2 and "self_pin=mismatch" in out
receipt("P6a-self-pin-mismatch", "c96 ... --self-pin 000...000", rc, out, "")
true_pin = sha(C96)
rc2, out2, err2 = run(["python3", "-B", C96, "--root", FX, "--revision", base_rev,
                       "--verdict-only", "--self-pin", true_pin])
ok_b = rc2 == 0 and "verdict=clean" in out2  # verdict-only line carries no self_pin field
receipt("P6b-self-pin-correct", "c96 ... --self-pin <true sha>", rc2, out2, "")
res["P6"] = {"ok": ok_a and ok_b, "mismatch_rc": rc, "true_rc": rc2}
log("[P6] mismatch rc=%d, true rc=%d -> %s" % (rc, rc2, "PASS" if ok_a and ok_b else "FAIL"))

# ---- P7: --base-pins-json zero floors cannot green identity violations
zero = json.dumps({"lessons": 0, "entries": 0, "rows": 0, "criteria": 0})
rx04_rev = summary["routes"]["RX04-entry-deleted-after-base"]["rev"]
rc, out, err = run(["python3", "-B", C96, "--root", FX, "--revision", rx04_rev,
                    "--verdict-only", "--base-pins-json", zero])
ident = []
try: ident = json.loads(out.splitlines()[1]).get("identity_missing", [])
except Exception: pass
ok_a = rc == 1 and "verdict=failed" in out and any(x.startswith("entry:") for x in ident)
receipt("P7a-zero-floors-on-deleted-entry", "c96 --root fx --revision <RX04 rev> --verdict-only --base-pins-json %s" % zero,
        rc, out, "identity_entries=%s" % [x for x in ident if x.startswith("entry:")])
rc2, out2, err2 = run(["python3", "-B", C96, "--root", FX, "--revision", base_rev,
                       "--verdict-only", "--base-pins-json", zero])
ok_b = rc2 == 0 and "verdict=clean" in out2
receipt("P7b-zero-floors-on-clean-base", "c96 --root fx --revision %s --verdict-only --base-pins-json %s" % (base_rev[:12], zero),
        rc2, out2, "")
res["P7"] = {"ok": ok_a and ok_b}
log("[P7] a rc=%d entry-ident=%s, b rc=%d -> %s" % (rc, ok_a, rc2, "PASS" if ok_a and ok_b else "FAIL"))

# ---- P8: PATH git shim serving clean bytes for the defective lesson (environment trust)
p8 = S + "/shim"; shutil.rmtree(p8, ignore_errors=True); os.makedirs(p8)
clean_lesson = S + "/shim_clean_lesson.md"
open(clean_lesson, "w").write(
    "# r96\n\n## Gate\n\nadmit: the sampled gate decisions.\n"
    "reject: the junk shapes below.\n\n## Mistakes\n\n| # | Class |\n|---|---|\n| 1 | a |\n")
target = "%s:corpus/lessons/round-96.md" % rx01_rev
shim = p8 + "/git"
open(shim, "w").write("""#!/bin/bash
if [ "$3" = "show" ] && [ "$4" = "%s" ]; then
  cat %s; exit 0
fi
exec /usr/bin/git "$@"
""" % (target, clean_lesson))
os.chmod(shim, 0o755)
env = dict(ENV0); env["PATH"] = p8 + ":" + ENV0["PATH"]
rc, out, err = run(["python3", "-B", C96, "--root", FX, "--revision", rx01_rev,
                    "--verdict-only"], env=env)
ok = rc == 0 and "verdict=clean" in out
receipt("P8-git-shim-path", "PATH=%s:$PATH c96 --root fx --revision <RX01 rev> --verdict-only (shim serves clean bytes for round-96.md)" % p8,
        rc, out, "shim_intercepts=%s" % target)
res["P8"] = {"ok": ok, "rc": rc, "class": "environment-trust residual (counter saw clean bytes)"}
log("[P8] rc=%d clean=%s -> observed (environment residual)" % (rc, ok))

with open(os.path.join(RUNS, "_summary_process.json"), "w") as fh:
    json.dump(res, fh, indent=1)
log("[process] all done")
