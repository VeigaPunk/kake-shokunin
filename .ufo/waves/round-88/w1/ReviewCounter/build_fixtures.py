#!/usr/bin/env python3
"""Build independent attack fixtures for round-88 C1 counter (c88_defect_queue.py).

Green tree is authored here from frozen base bytes, NOT from the counter's own
mirror_tree(), so a counter defect cannot be masked by sharing a writer.
"""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
W = LANE / '.ufo/waves/round-88'
FROZEN = W / 'frozen'
COUNTER = W / 'c88_defect_queue.py'
SCR = Path('/fast/scratch/hyaku/kake-r88/ReviewCounter')
FIX = SCR / 'fixtures'
WORK = SCR / 'work'
REC = SCR / 'receipts'

LEDGER = 'corpus/knowledge/gate-agreement-ledger.json'
ENTRY = 'corpus/knowledge/cache-current-age.md'
COMPANION = 'corpus/knowledge/gate-agreement-metadata.md'
TOOL = 'scripts/cache_current_age.py'

base_ledger = (FROZEN / 'base-gate-agreement-ledger.json').read_bytes()
base_entry = (FROZEN / 'base-cache-current-age.md').read_text()
base_tool = (FROZEN / 'base-cache_current_age.py').read_text()

DEFECT_LINE = '            raise ValueError(f"{key} must be an integer, not boolean")'
REPAIRED_LINE = ('            raise ValueError("%s must be an integer, not %s" % (key, "boolean" if '
                 'isinstance(value, bool) else type(value).__name__))')


def repaired_tool() -> str:
    assert DEFECT_LINE in base_tool, 'frozen base tool lost the defective diagnostic line'
    return base_tool.replace(DEFECT_LINE, REPAIRED_LINE)


def entry_fixed() -> str:
    lines = base_entry.splitlines()
    assert lines[2].startswith('recheck:'), lines[2]
    lines[2] = ('recheck: 180d or source/adapter change; reopen '
                'https://httpwg.org/specs/rfc9111.html#age.calculations and compare section 4.2.3 '
                'equations; the offline selftest command is item 4 of the checklist below.')
    lines.append('6. Offline selftest without a fixed scratch path: '
                 'TMPDIR=$(mktemp -d) python3 -B scripts/cache_current_age.py --selftest; '
                 'the directory is created by the shell and removed by the operator.')
    return '\n'.join(lines) + '\n'


def companion(digest: str, source_line: str | None = None, prefix_lines: list[str] | None = None) -> str:
    src = source_line if source_line is not None else (
        'source: ' + LEDGER + ' — lane metadata ledger; ledger sha256 ' + digest +
        '; originating verdicts in corpus/lessons/round-8{4,5,6}-verifier-spotcheck.md.')
    head = (src + '\n'
            'verified-at: 2026-11-04 — lane record of closure-owned decisions; round-88 counter '
            '.ufo/waves/round-88/c88_defect_queue.py.\n'
            'recheck: 180d or on a new verifier spot-check\n')
    pre = ('\n'.join(prefix_lines) + '\n') if prefix_lines else ''
    body = ('\n# Gate-agreement ledger — provenance companion\n\n'
            'Independent reviewer fixture, authored outside the counter.\n')
    return pre + head + body


def write_tree(name: str, ledger: bytes | None = None, entry: str | None = None,
               comp: str | None = None, tool: str | None = None) -> Path:
    root = FIX / name
    if root.exists():
        shutil.rmtree(root)
    ledger = base_ledger if ledger is None else ledger
    data = {LEDGER: ledger,
            ENTRY: (entry_fixed() if entry is None else entry).encode(),
            COMPANION: (companion(hashlib.sha256(ledger).hexdigest()) if comp is None else comp).encode(),
            TOOL: (repaired_tool() if tool is None else tool).encode()}
    for rel, blob in data.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(blob)
    return root


def stub_selftest_text(count: int = 61) -> str:
    return ('    print(f"selftest: {number} isolated CLI fixtures passed")\n    return 0\n')


def main() -> int:
    for d in (FIX, WORK, REC):
        d.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(base_ledger).hexdigest()
    written = []

    # Green: independent repair of all three items.
    written.append(write_tree('A0-green'))
    # Converse control: pure frozen base (no repair at all).
    base_root = FIX / 'A0-base'
    if base_root.exists():
        shutil.rmtree(base_root)
    for rel, blob in ((LEDGER, base_ledger), (ENTRY, base_entry.encode()),
                      (TOOL, base_tool.encode())):
        p = base_root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(blob)
    written.append(base_root)

    # (a) records-only: plausible prose, frozen base tool.
    written.append(write_tree('a-records-only', tool=base_tool))

    # (b) one ledger row changed, companion digest updated to the changed bytes.
    rowled = base_ledger.replace(b'"agree"', b'"disagree"', 1)
    written.append(write_tree('b-ledger-row-newdigest', ledger=rowled,
                              comp=companion(hashlib.sha256(rowled).hexdigest())))
    written.append(write_tree('b-ledger-row-staledigest', ledger=rowled))
    # (b2) a semantic no-op byte change (whitespace) also must reopen D1.
    wsled = base_ledger.replace(b'"admit",', b'"admit" ,', 1)
    written.append(write_tree('b-ledger-whitespace', ledger=wsled,
                              comp=companion(hashlib.sha256(wsled).hexdigest())))

    # (c) ledger named with truncated / wrong digest, or a look-alike path.
    written.append(write_tree('c1-truncated-digest',
                              comp=companion(digest[:20])))
    written.append(write_tree('c2-wrong-digest',
                              comp=companion('f' * 64)))
    written.append(write_tree('c3-path-suffix-trap',
                              comp=companion(digest, 'source: ' + LEDGER + '.bak — backup copy of '
                                                     'the lane ledger; ledger sha256 ' + digest + '.')))
    written.append(write_tree('c4-path-other-dir',
                              comp=companion(digest, 'source: archive/corpus/knowledge/' +
                                                     'gate-agreement-ledger.json — archived copy; ledger sha256 ' +
                                                     digest + '.')))
    written.append(write_tree('c5-truncated-path',
                              comp=companion(digest, 'source: corpus/knowledge/gate-agreement-ledger — '
                                                     'lane ledger; ledger sha256 ' + digest + '.')))
    written.append(write_tree('c6-trio-after-seven-junk-lines',
                              comp=companion(digest, prefix_lines=['junk %d' % i for i in range(1, 6)])))

    # (d) recheck fixed, claim touched through insert / edit / line-ending change.
    ins = entry_fixed().splitlines()
    idx = next(i for i, l in enumerate(ins) if l.endswith('inferred on the observed path.'))
    contradict = ('The maximum below is the RFC\'s only permitted algorithm and every conforming '
                  'cache MUST apply it verbatim.')
    ins.insert(idx + 1, contradict)
    written.append(write_tree('d1-insert-contradicting-claim', entry='\n'.join(ins) + '\n'))

    rewrite = entry_fixed().replace(
        'Inputs: one JSON object with required `date_value`, `request_time`,',
        'Inputs: any JSON value; the tool infers the missing seconds itself,', 1)
    assert rewrite != entry_fixed()
    written.append(write_tree('d2-plain-claim-rewrite', entry=rewrite))

    crlf = entry_fixed().replace('\n', '\r\n')
    written.append(write_tree('d3-crlf-line-endings', entry=crlf))

    stale = base_entry.splitlines()[2]
    moved = entry_fixed().splitlines()
    moved.insert(4, 'Historical command retained: ' + stale)
    written.append(write_tree('d4-stale-recheck-moved-to-body', entry='\n'.join(moved) + '\n'))

    # (e) right diagnostic words, wrong arithmetic / wrong output types.
    hardcoded = '''#!/usr/bin/env python3
import json
import sys

REQ = ("date_value", "request_time", "response_time", "now")
OUT = {"apparent_age": 20, "response_delay": 10, "corrected_age_value": 15,
       "corrected_initial_age": 20, "resident_time": 30, "current_age": 50}


def main() -> int:
    if sys.argv[1:] == ["--selftest"]:
        print("selftest: 61 isolated CLI fixtures passed")
        return 0
    try:
        p = json.loads(sys.stdin.read())
        if not isinstance(p, dict):
            raise ValueError("input must be a JSON object")
        for k in REQ:
            if k not in p:
                raise ValueError("missing " + k)
        for k in (*REQ, "age_value"):
            v = p.get(k, 0)
            if not isinstance(v, int) or isinstance(v, bool):
                raise ValueError("%s must be an integer, not %s" % (
                    k, "boolean" if isinstance(v, bool) else type(v).__name__))
            if k != "date_value" and v < 0:
                raise ValueError(k + " must be nonnegative")
        if not p["request_time"] <= p["response_time"] <= p["now"]:
            raise ValueError("require request_time <= response_time <= now")
    except (ValueError, UnicodeError) as exc:
        print("invalid_input: " + str(exc), file=sys.stderr)
        return 1
    print(json.dumps(OUT, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''
    written.append(write_tree('e1-hardcoded-valid-output', tool=hardcoded))

    e2 = repaired_tool().replace(
        '    corrected_initial_age = max(apparent_age, corrected_age_value)',
        '    corrected_initial_age = max(apparent_age, corrected_age_value) if age_value else apparent_age',
        1)
    assert e2 != repaired_tool()
    written.append(write_tree('e2-wrong-arith-age-omitted', tool=e2))

    e3 = repaired_tool()
    for key in ('apparent_age', 'response_delay', 'corrected_age_value',
                'corrected_initial_age', 'resident_time', 'current_age'):
        old = f'        "{key}": {key},'
        assert old in e3, old
        e3 = e3.replace(old, f'        "{key}": float({key}),', 1)
    assert '                assert all(type(value) is int for value in output.values()), number' in e3
    e3 = e3.replace('                assert all(type(value) is int for value in output.values()), number',
                    '                pass  # type gate removed by the e3 mutant', 1)
    written.append(write_tree('e3-float-terms', tool=e3))

    e0 = repaired_tool().replace(
        '    current_age = corrected_initial_age + resident_time',
        '    current_age = corrected_initial_age + resident_time + 1', 1)
    assert e0 != repaired_tool()
    written.append(write_tree('e0-offbyone-caught', tool=e0))

    print(json.dumps({'fixtures': [p.name for p in written],
                      'digest': digest}, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
