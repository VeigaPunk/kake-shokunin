import importlib.util, os, subprocess, sys

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

base = load("base_tool", "/fast/scratch/hyaku/kake-r58/ExecResolverFix/receipts/base_tool.py")
cand = load("cand_tool", "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58/w1/ExecResolverFix.files/id_resolver.py")
root = "/home/vgpnk/Projects/shokunin"
diffs = 0
for name in sorted(os.listdir(root)):
    d = os.path.join(root, name)
    if not name.endswith("-shokunin") or not os.path.isdir(d):
        continue
    if os.path.exists(os.path.join(d, ".git")):
        p = subprocess.run(["git", "-C", d, "show", "HEAD:corpus/SOURCES.md"], capture_output=True)
        text = p.stdout.decode("utf-8", "replace") if p.returncode == 0 else ""
    else:
        f = os.path.join(d, "corpus/SOURCES.md")
        text = open(f, encoding="utf-8", errors="replace").read() if os.path.isfile(f) else ""
    if not text:
        print(f"{name}: no registry")
        continue
    a, b = base.parse_registry(text), cand.parse_registry(text)
    same = a == b
    diffs += 0 if same else 1
    added = sorted(set(b) - set(a)); lost = sorted(set(a) - set(b))
    print(f"{name}: rows={len(a)} parity={'same' if same else 'DIFF'} gained={added} lost={lost}")
print(f"registries_differing={diffs}")
