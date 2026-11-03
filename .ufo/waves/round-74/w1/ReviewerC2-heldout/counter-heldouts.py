import importlib.util
import json
import os
import pathlib
from unittest.mock import patch

root = pathlib.Path('/fast/scratch/hyaku/kake-r74/ReviewerC2')
artifact = pathlib.Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-74/w1/ExecC2Counter/c74_sidecar_reobserve.py')
spec = importlib.util.spec_from_file_location('candidate', artifact)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
output = []
for file in sorted((root / 'heldout').glob('*/corpus/knowledge/freshness-sidecar.json')):
    entries = json.loads(file.read_text())['entries']
    prior = [dict(e, kind='absent', date='2026-10-21', note='2026-10-21 absent; historical record, not an executable instruction') for e in entries]
    for e in prior:
        e.pop('history', None)
    def read_entries(repo, revision):
        return prior if revision == m.BASE_REVISION else entries
    with patch.object(m, 'read_entries', side_effect=read_entries):
        result = m.measure(str(root), 'fixture-after')
    output.append(dict(name=file.parents[2].name, **result))
print(json.dumps(output, indent=2))
