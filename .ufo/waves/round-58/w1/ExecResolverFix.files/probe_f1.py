import os, subprocess, sys, tempfile
BASE = "/fast/scratch/hyaku/kake-r58/ExecResolverFix/probe"
os.makedirs(BASE, exist_ok=True)
D = tempfile.mkdtemp(dir=BASE)
env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
def run(*a, cwd=None):
    p = subprocess.run(list(a), cwd=cwd, env=env, capture_output=True)
    return p.returncode, p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")
run("git", "init", "-q", D)
rc, top = run("git", "-C", D, "rev-parse", "--show-toplevel")
assert rc == 0 and os.path.realpath(top.strip()) == os.path.realpath(D), (rc, top)
os.makedirs(os.path.join(D, "corpus", "knowledge"))
with open(os.path.join(D, "corpus", "SOURCES.md"), "w", encoding="utf-8", newline="") as h:
    h.write("# Sources\n\n## Registry\n\n| id | source |\n| --- | --- |\n| S001 | https://example.invalid/1 |\n")
for name, cite in (("nl\nname.md", "Cites S902."), ("back\\slash.md", "Cites S903."), ("plain.md", "Cites S001.")):
    with open(os.path.join(D, "corpus", "knowledge", name), "w", encoding="utf-8", newline="") as h:
        h.write(cite + "\n")
run("git", "-C", D, "add", "-A")
run("git", "-C", D, "-c", "user.name=selftest", "-c", "user.email=selftest@local", "-c", "commit.gpgsign=false", "commit", "-q", "-m", "probe")
rc, rev = run("git", "-C", D, "rev-parse", "HEAD")
rev = rev.strip()
empty = os.path.join(BASE, "empty-fleet"); os.makedirs(empty, exist_ok=True)
for label, tool in (("base", "/fast/scratch/hyaku/kake-r58/ExecResolverFix/receipts/base_tool.py"),
                    ("cand", "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58/w1/ExecResolverFix.files/id_resolver.py")):
    rc, out = run(sys.executable, "-B", tool, "--root", D, "--revision", rev, "--fleet", empty)
    print(f"== {label} exit={rc} root={D} rev={rev[:12]}")
    for line in out.strip().splitlines():
        print("   " + line.replace("\n", "\\n"))
