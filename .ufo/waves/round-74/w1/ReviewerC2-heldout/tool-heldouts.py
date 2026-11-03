import importlib.util
import json
import pathlib

root = pathlib.Path('/fast/scratch/hyaku/kake-r74/ReviewerC2')
path = '/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-74/w1/ExecC2Tool/sidecar_reobserve.py'
spec = importlib.util.spec_from_file_location('repair', path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
results = []
for file in sorted((root / 'heldout').glob('*/corpus/knowledge/freshness-sidecar.json')):
    before = file.read_bytes()
    row = {'name': file.parents[2].name}
    for mode in ('check', 'write'):
        try:
            result, code = m.reobserve(file.parents[2], mode == 'write', '2026-11-03', 'linux-reviewer')
            row[mode] = {'exit': code, 'result': result, 'unchanged': before == file.read_bytes()}
        except Exception as error:
            row[mode] = {'exception': type(error).__name__, 'message': str(error), 'unchanged': before == file.read_bytes()}
    file.write_bytes(before)
    results.append(row)
print(json.dumps(results, indent=2))
