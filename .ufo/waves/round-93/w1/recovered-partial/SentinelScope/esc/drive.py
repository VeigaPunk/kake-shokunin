import json, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
work = os.path.join(here, "work")
sandbox = os.path.join(here, "sandbox.py")
subjects = sorted(os.listdir(os.path.join(work, "tree", "scripts")))
for name in subjects:
    if not name.endswith(".py") or name.startswith("written"): continue
    path = os.path.join(work, "tree", "scripts", name)
    p = subprocess.run([sys.executable, "-B", sandbox, path], input=b"{}",
                       capture_output=True, timeout=60, cwd=work,
                       env={"PATH": "/usr/bin:/bin", "HOME": work})
    print("== %s rc=%d" % (name, p.returncode))
    print("   out:", p.stdout.decode("utf-8", "replace").strip().replace("\n", " | ")[:300])
    print("   err:", p.stderr.decode("utf-8", "replace").strip().replace("\n", " | ")[:300])
