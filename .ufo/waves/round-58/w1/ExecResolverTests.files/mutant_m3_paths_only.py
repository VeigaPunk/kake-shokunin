# junk control M3: correct -z knowledge paths, registry parsing still fence-blind
import importlib.util, sys
spec = importlib.util.spec_from_file_location("cur", "/fast/scratch/hyaku/kake-r58/ExecResolverTests/cur_id_resolver.py")
cur = importlib.util.module_from_spec(spec); spec.loader.exec_module(cur)
_orig = cur.knowledge_bodies
def knowledge_bodies(root, revision):
    if not revision:
        return _orig(root, revision)
    proc = cur._git(root, "ls-tree", "-r", "-z", "--name-only", revision)
    if proc.returncode != 0:
        return None, f"cannot list {revision[:12]}"
    rels = [r for r in cur._text(proc).split("\0")
            if r.startswith(cur.KNOWLEDGE_REL + "/") and r.endswith(".md")]
    bodies = {}
    for rel in rels:
        blob = cur._git(root, "show", f"{revision}:{rel}")
        if blob.returncode != 0:
            return None, f"cannot read {rel} at {revision[:12]}"
        bodies[rel] = cur._text(blob)
    if not bodies:
        return None, f"no knowledge file at {revision[:12]}"
    return bodies, None
cur.knowledge_bodies = knowledge_bodies
sys.exit(cur.main(sys.argv[1:]))
