# junk control M1: fence-blind (current) + the cheapest quoted-path "fix" (core.quotePath=false)
import importlib.util, sys
spec = importlib.util.spec_from_file_location("cur", "/fast/scratch/hyaku/kake-r58/ExecResolverTests/cur_id_resolver.py")
cur = importlib.util.module_from_spec(spec); spec.loader.exec_module(cur)
def _git(root, *args):
    if args and args[0] == "ls-tree":
        args = ("-c", "core.quotePath=false") + args
    return cur._spawn(["git", "-C", root, *args])
cur._git = _git
sys.exit(cur.main(sys.argv[1:]))
