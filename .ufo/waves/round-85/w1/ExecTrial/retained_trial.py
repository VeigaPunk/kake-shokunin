#!/usr/bin/env python3
"""Author-side offline retained witness, independent of production decoders."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
PAIR = ROOT / '.ufo/waves/round-84/capture-control/equivalent'
SCRATCH = Path('/fast/scratch/hyaku/kake-r85/ExecTrial')
KNOWN = frozenset((
    'no-referrer', 'no-referrer-when-downgrade', 'same-origin', 'origin',
    'strict-origin', 'origin-when-cross-origin',
    'strict-origin-when-cross-origin', 'unsafe-url',
))


def decode(fields):
    """Select the last recognized token without importing candidate code."""
    tokens = [part.strip() for value in fields for part in value.split(',')]
    for token in reversed(tokens):
        if token in KNOWN:
            return tokens, token
    return tokens, ''


def main():
    captures = []
    for side in ('a', 'b'):
        path = PAIR / side / 'ds4cc-sitemap/response.json'
        raw = path.read_bytes()
        response = json.loads(raw)
        matches = [
            {'response_header_index': index, 'name': header['name'],
             'value': header['value']}
            for index, header in enumerate(response['headers'])
            if header['name'].lower() == 'referrer-policy'
        ]
        fields = [header['value'] for header in matches]
        tokens, effective = decode(fields)
        captures.append({
            'side': side, 'input_path': str(path),
            'sha256': hashlib.sha256(raw).hexdigest(),
            'ordered_matching_headers': matches, 'ordered_field_values': fields,
            'ordered_tokens': tokens, 'effective': effective,
        })

    command = [
        sys.executable, '-B', str(ROOT / 'scripts/policy_value_class.py'),
        '--a', str(PAIR / 'a'), '--b', str(PAIR / 'b'),
        '--declared', str(ROOT / '.ufo/waves/round-81/capture-expectations.json'),
    ]
    process = subprocess.run(
        command, cwd=SCRATCH, env={**os.environ, 'TMPDIR': str(SCRATCH)},
        text=True, capture_output=True, check=False,
    )
    classifier_files = [ROOT / 'scripts/policy_value_class.py',
                        ROOT / 'scripts/header_change_class.py',
                        ROOT / '.ufo/waves/round-81/capture-expectations.json']
    classifier = {
        'command': command, 'cwd': str(SCRATCH), 'TMPDIR': str(SCRATCH),
        'exit': process.returncode, 'stdout': process.stdout,
        'stderr': process.stderr,
        'input_sha256': {str(path): hashlib.sha256(path.read_bytes()).hexdigest()
                         for path in classifier_files},
    }
    summary = process.stdout.splitlines()[-1] if process.stdout else ''
    equivalent = summary.endswith('verdict=policy-rewritten-equivalent')
    differs = captures[0]['effective'] != captures[1]['effective']
    print(json.dumps({
        'scope': 'author-side offline domain preparation; not publication approval',
        'decoder': 'independent last-recognized token selection; case-sensitive',
        'captures': captures, 'r84_classifier': classifier,
        'r84_rewritten_equivalent': equivalent,
        'effective_tokens_differ': differs,
    }, indent=2))
    return 0 if process.returncode == 0 and equivalent and differs else 1


if __name__ == '__main__':
    raise SystemExit(main())
