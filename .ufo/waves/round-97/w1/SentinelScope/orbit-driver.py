import os, subprocess, sys, json
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
SC = os.environ["ORBIT"]
ctr = sys.argv[1]           # e.g. /home/.../.ufo/waves/round-97/c97_index.py
root = "--root", LANE
flags = sys.argv[2:]
def git(*a):
    e = dict(os.environ); e.setdefault("PATH", "/usr/bin:/bin")
    e.setdefault("GIT_NO_REPLACE_OBJECTS", "1")
    return subprocess.run(["/usr/bin/git", "-C", LANE, *a], capture_output=True, env=e)
rev = git("rev-parse", "master").stdout.decode().strip()
env = {"PATH": os.environ.get("FORCEDPATH", os.environ["PATH"]), "TMPDIR": SC + "/tmp",
       "HOME": SC + "/home", "SC": SC, "ORBIT": SC}
res = subprocess.run([os.environ.get("USED_PY", sys.executable), "-B", ctr,
                      "--root", LANE, "--revision", rev, "--work", SC + "/w"] + flags,
                     capture_output=True, env=env, cwd=SC)
print(res.stdout.decode())
sys.stderr.write(res.stderr.decode())
with open(SC + "/last.json", "w") as fh:
    json.dump({"rc": res.returncode, "ctr": ctr}, fh)
