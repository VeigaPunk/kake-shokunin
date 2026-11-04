#!/usr/bin/env python3
"""Emit the mutation matrix and trimmed divergence witnesses."""
import json
from pathlib import Path

S = Path('/fast/scratch/hyaku/kake-r89/MutKey')
recs = {r['id']: r for r in json.loads((S / 'receipts/live/score.json').read_text())}
index = {r['id']: r for r in json.loads((S / 'mutants/index.json').read_text())}
diff = json.loads((S / 'receipts/diff/diff.json').read_text())['mutants']
out = S / 'receipts/matrix.tsv'
rows = ['id\tclause\tverdict\tfrozen\tprops\trefuse\tfirst_fail\tdifferences\twitness_case\tsha256']
witness_dir = S / 'receipts/witness'
witness_dir.mkdir(parents=True, exist_ok=True)
for mid, rec in recs.items():
    d = diff.get(mid, {})
    first = (rec.get('fails') or ['-'])[0].replace('\t', ' ')
    rows.append('\t'.join([mid, index.get(mid, {}).get('clause', 'reference candidate'),
                           rec['verdict'], rec.get('frozen', '-'), rec.get('props', '-'),
                           rec.get('refuse', '-'), first,
                           str(d.get('divergences', 0)),
                           (d.get('witness') or {}).get('case', '-'),
                           rec['sha256']]))
    lines = (S / 'receipts/diff' / f'{mid}.jsonl')
    if lines.exists() and mid in diff:
        keep = [json.loads(x) for x in lines.read_text().splitlines()[:20]]
        (witness_dir / f'{mid}.json').write_text(json.dumps(
            {'divergences': diff[mid]['divergences'], 'first_20': keep}, indent=1) + '\n')
out.write_text('\n'.join(rows) + '\n')
print(out.read_text())
