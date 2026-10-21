#!/usr/bin/env python3
"""Exercise revision/counter boundaries using a disposable local Git repository."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / '.ufo/waves/round-25'


def main():
    spec = importlib.util.spec_from_file_location('packet_counter', BASE / 'measure.py')
    counter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(counter)
    rows = []
    git_env = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
    git_env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull)
    with tempfile.TemporaryDirectory(prefix='kake-packet-counter-') as temporary:
        repo = Path(temporary)
        def git(*args):
            p = subprocess.run(['git', '-C', str(repo), '-c', 'user.name=kake-fixture',
                '-c', 'user.email=kake-fixture@invalid.local', '-c', 'core.hooksPath=/dev/null',
                '-c', 'commit.gpgsign=false', *args], env=git_env, capture_output=True, check=True)
            return p.stdout.decode().strip()
        def commit(message):
            git('add', '.')
            git('commit', '--allow-empty', '-qm', message)
            return git('rev-parse', 'HEAD')
        def put(rel, data):
            path = repo / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        def record(name, revision, expected_exit, finding=None, expected_accepted=None):
            out, code = counter.evaluate(repo, revision)
            passed = code == expected_exit and (finding is None or finding in out['findings'])
            if expected_accepted is not None:
                passed = passed and out['accepted'] == expected_accepted
            rows.append({'case': name, 'exit': code, 'findings': out['findings'],
                         'accepted': out['accepted'], 'passed': passed,
                         'websiteConformance': out['websiteConformance']})
        git('init', '-q')
        baseline = commit('absent baseline')
        record('absent_baseline', baseline, 1, 'capability_absent', 0)
        original = {rel: (ROOT / rel).read_bytes() for rel in
                    (counter.PACKET_TOOL, counter.POPULATION, counter.SOURCE, counter.CARDS)}
        for rel, data in original.items():
            put(rel, data)
        good = commit('complete candidate')
        record('complete_candidate', good, 0, expected_accepted=55)
        (repo / counter.POPULATION).unlink()
        missing = commit('candidate omits population')
        record('missing_candidate_population', missing, 2, 'input_invalid')
        put(counter.POPULATION, original[counter.POPULATION])
        (repo / counter.SOURCE).unlink()
        missing_source = commit('candidate omits source')
        record('missing_candidate_source', missing_source, 2, 'input_invalid')
        put(counter.SOURCE, original[counter.SOURCE])
        put(counter.PACKET_TOOL, b'import json\nprint(json.dumps({"verdict":"clean"}))\n')
        mismatch = commit('wrong tool output')
        record('tool_disagreement', mismatch, 2, 'tool_mismatch')
        put(counter.PACKET_TOOL, original[counter.PACKET_TOOL])
        put(counter.POPULATION, original[counter.POPULATION] + b' ')
        tampered = commit('changed population bytes')
        record('changed_population', tampered, 2, 'snapshot_tampered')
        put(counter.POPULATION, original[counter.POPULATION])
        put(counter.CARDS, original[counter.CARDS] + b' ')
        changed_cards = commit('changed reviewed packet bytes')
        record('changed_reviewed_packet', changed_cards, 2, 'snapshot_tampered')
        try:
            counter.GitStore(repo).read('0' * 40, counter.PACKET_TOOL)
        except counter.InputFailure as error:
            passed = error.finding == 'git_unavailable'
        else:
            passed = False
        rows.append({'case': 'git_failure_not_absence', 'passed': passed})
        try:
            counter.strict_json(b'[' * 2000 + b']' * 2000)
        except ValueError:
            passed = True
        else:
            passed = False
        rows.append({'case': 'unsupported_json_nesting', 'passed': passed})
    passed = all(row['passed'] for row in rows)
    print(json.dumps({'schema': 'kake-packet-counter-selftest-v1', 'passed': passed,
                      'total': len(rows), 'rows': rows, 'websiteConformance': 'not-assessed'}, sort_keys=True))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
