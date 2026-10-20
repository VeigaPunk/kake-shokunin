#!/usr/bin/env python3
"""Replay the committed canonical fixture population after digest verification."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default=str(Path(__file__).resolve().parents[3]))
    args = parser.parse_args()
    root = Path(args.root).resolve()
    evidence = root / '.ufo/waves/round-22'
    try:
        expected = json.loads((evidence / 'frozen/expected.json').read_text())
        inputs = expected['inputs']
        if not isinstance(inputs, dict) or not inputs:
            raise ValueError('empty digest population')
        for relative, digest in inputs.items():
            path = root / relative
            if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(root):
                raise ValueError('unsafe snapshot member')
            if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                raise ValueError('snapshot member digest mismatch')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'verdict': 'could-not-evaluate', 'id': 'snapshot_tampered', 'error': str(exc)}))
        return 2
    run = subprocess.run([sys.executable, str(evidence / 'matrix.py'), '--root', str(root), '--json'], capture_output=True, text=True)
    try:
        actual = json.loads(run.stdout)
        matched = run.returncode == expected['exit'] and actual['accepted'] == expected['accepted'] and actual['total'] == expected['total']
    except (ValueError, KeyError, TypeError):
        matched = False
        actual = None
    print(json.dumps({'verdict': 'clean' if matched else 'failed', 'id': 'frozen_replay_match' if matched else 'frozen_replay_mismatch', 'inputsVerified': len(inputs), 'expected': {k: expected[k] for k in ('exit', 'accepted', 'total')}, 'actualExit': run.returncode, 'actual': actual, 'stderr': run.stderr}, indent=2))
    return 0 if matched else 1


if __name__ == '__main__':
    raise SystemExit(main())
