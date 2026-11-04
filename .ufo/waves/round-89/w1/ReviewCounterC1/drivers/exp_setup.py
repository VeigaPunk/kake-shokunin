import importlib.util, os, subprocess, sys, shutil
from pathlib import Path

S = Path('/fast/scratch/hyaku/kake-r89/ReviewCounterC1')
LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
BASE = '76225160d0dff8d2042fbcd037bd08b0971d5e07'
G = S / 'g-git'

spec = importlib.util.spec_from_file_location('c89', S / 'counters' / 'c89_defect_queue.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

tool = subprocess.run(['git', '-C', str(LANE), 'show', f'{BASE}:scripts/vary_match.py'],
                      capture_output=True).stdout
assert tool, 'base tool bytes'
mod._tool_text = lambda: tool

assert not G.exists(), 'g-git exists'
G.mkdir()
def sh(*a, env=None):
    return subprocess.run(['git', '-C', str(G), *a], check=True, capture_output=True, text=True,
                          env=env)
sh('init', '-q')
sh('config', 'user.email', 'r@r'); sh('config', 'user.name', 'r')
top = sh('rev-parse', '--show-toplevel').stdout.strip()
assert top == str(G), top

# green tree (from the counter's own generator, tool bytes from the frozen base)
mod.green_tree(G)
freeze = LANE / '.ufo/waves/round-89/c89_key.py'
(G / '.ufo/waves/round-89').mkdir(parents=True, exist_ok=True)
shutil.copy(freeze, G / mod.FREEZE_PATH)
# commit 1: everything except dispatch
env1 = dict(os.environ, GIT_AUTHOR_DATE='2026-11-04T10:00:00Z', GIT_COMMITTER_DATE='2026-11-04T10:00:00Z')
sh('add', '-A'); sh('commit', '-qm', 'freeze+green', env=env1)
(G / mod.DISPATCH_PATH).write_text('dispatch\n')
env2 = dict(os.environ, GIT_AUTHOR_DATE='2026-11-04T11:00:00Z', GIT_COMMITTER_DATE='2026-11-04T11:00:00Z')
sh('add', '-A'); sh('commit', '-qm', 'dispatch', env=env2)
sh('branch', '-f', 'green')
print(sh('rev-parse', 'HEAD').stdout.strip(), 'green HEAD')
