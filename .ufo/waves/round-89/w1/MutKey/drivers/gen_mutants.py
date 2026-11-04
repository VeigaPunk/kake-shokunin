#!/usr/bin/env python3
"""Generate single-point mutants of the C2 candidate.

Each entry: (id, contract clause, old substring, new substring). Every `old`
must occur exactly once in the candidate source; a multi-line `old` still
changes exactly one clause. Writes mutants/<id>.py and mutants/index.json.
"""
import json
import sys
from pathlib import Path

SRC = Path('/fast/scratch/hyaku/kake-r89/MutKey/ref/cache_key.py')
OUT = Path('/fast/scratch/hyaku/kake-r89/MutKey/mutants')

PRESENT = '            parts.append(_esc(name) + RS + _esc(_strip_ows(lowered[name])))'
ABSENT = '            parts.append(_esc(name) + RS + GS)'

MUTANTS = [
    ('M01-member-name-not-lowered', 'name case handling (member)',
     'names.append(member.lower())', 'names.append(member)'),
    ('M02-header-stored-as-presented', 'name case handling (header lookup)',
     'lowered[low] = value', 'lowered[name] = value'),
    ('M03-member-order-unsorted', 'member sort',
     '    return sorted(names)', '    return names'),
    ('M04-member-order-reversed', 'member sort (direction)',
     '    return sorted(names)', '    return sorted(names, reverse=True)'),
    ('M05-member-ows-not-trimmed', 'member OWS trim',
     'member = _strip_ows(raw)', 'member = raw'),
    ('M06-member-trim-wider-than-ows', 'member OWS trim (SP/HTAB only)',
     'member = _strip_ows(raw)', 'member = raw.strip()'),
    ('M07-value-ows-not-trimmed', 'value OWS trim',
     PRESENT, '            parts.append(_esc(name) + RS + _esc(lowered[name]))'),
    ('M08-value-trim-wider-than-ows', 'value OWS trim (SP/HTAB only)',
     PRESENT, '            parts.append(_esc(name) + RS + _esc(lowered[name].strip()))'),
    ('M09-value-case-lowered', 'value case',
     PRESENT, '            parts.append(_esc(name) + RS + _esc(_strip_ows(lowered[name]).lower()))'),
    ('M10-value-case-uppered', 'value case (inverse)',
     PRESENT, '            parts.append(_esc(name) + RS + _esc(_strip_ows(lowered[name]).upper()))'),
    ('M11-escape-percent-dropped', 'escaping %',
     '("%", "%25"),', '("%", "%"),'),
    ('M12-escape-GS-dropped', 'escaping U+001C',
     '(GS, "%1C"),', '(GS, GS),'),
    ('M13-escape-FS-dropped', 'escaping U+001D',
     '("\\x1d", "%1D"),', '("\\x1d", "\\x1d"),'),
    ('M14-escape-RS-dropped', 'escaping U+001E',
     '(RS, "%1E"),', '(RS, RS),'),
    ('M15-escape-US-dropped', 'escaping U+001F',
     '(US, "%1F"),', '(US, US),'),
    ('M16-escape-percent-last', 'escaping order (% escaped after separators)',
     '    ("%", "%25"),\n    (GS, "%1C"),\n    ("\\x1d", "%1D"),\n    (RS, "%1E"),\n    (US, "%1F"),',
     '    (GS, "%1C"),\n    ("\\x1d", "%1D"),\n    (RS, "%1E"),\n    (US, "%1F"),\n    ("%", "%25"),'),
    ('M17-absent-emits-empty', 'absent marker',
     ABSENT, '            parts.append(_esc(name) + RS)'),
    ('M18-present-empty-emits-absent', 'present-empty vs absent',
     PRESENT + '\n        else:',
     '            _v = _strip_ows(lowered[name])\n'
     '            parts.append(_esc(name) + RS + (GS if _v == "" else _esc(_v)))\n        else:'),
    ('M19-wildcard-not-refused', 'wildcard refusal',
     '        if member == "*":\n            raise _Invalid("vary wildcard nominates no field")',
     '        if member == "**":\n            raise _Invalid("vary wildcard nominates no field")'),
    ('M20-wildcard-anywhere-refused', 'wildcard refusal (over-broad)',
     'if member == "*":', 'if "*" in member:'),
    ('M21-duplicate-member-not-refused', 'duplicate member refusal',
     'if len(set(names)) != len(names):', 'if False:'),
    ('M22-duplicate-header-not-refused', 'duplicate header refusal',
     'if low in lowered:', 'if low in lowered and False:'),
    ('M23-crlf-check-dropped', 'CR/LF refusal',
     'if "\\r" in value or "\\n" in value:', 'if False:'),
    ('M24-lf-check-dropped', 'CR/LF refusal (LF half)',
     'if "\\r" in value or "\\n" in value:', 'if "\\r" in value:'),
    ('M25-header-token-check-dropped', 'token check (header name)',
     'if not isinstance(name, str) or not _is_token(name):',
     'if not isinstance(name, str):'),
    ('M26-vary-token-check-dropped', 'token check (Vary member)',
     'if not _is_token(member):', 'if not isinstance(member, str):'),
    ('M27-empty-vary-falls-through', 'empty Vary handling',
     '    if vary == "":\n        return []', '    if vary == "\\x00":\n        return []'),
    ('M28-layout-us-always', 'separator layout (no-member case)',
     'return _esc(uri) + ("" if not parts else US + US.join(parts))',
     'return _esc(uri) + US + US.join(parts)'),
    ('M29-layout-comma-join', 'separator layout (pair separator)',
     'US + US.join(parts)', 'US + ",".join(parts)'),
    ('M30-layout-rs-dropped', 'separator layout (name/value separator)',
     PRESENT, '            parts.append(_esc(name) + _esc(_strip_ows(lowered[name])))'),
    ('M31-uri-not-escaped', 'escaping the URI component',
     'return _esc(uri) + ("" if not parts else US + US.join(parts))',
     'return uri + ("" if not parts else US + US.join(parts))'),
    ('M32-value-internal-whitespace-collapsed', 'value byte-exactness (internal OWS)',
     PRESENT,
     '            parts.append(_esc(name) + RS + _esc(" ".join(_strip_ows(lowered[name]).split())))'),
    ('M33-header-name-casefold', 'ASCII-only lowercasing (equivalent probe)',
     'low = name.lower()', 'low = name.casefold()'),
    ('M34-refusal-exits-zero', 'refusal contract (exit 1)',
     '    except _Invalid as exc:\n        print(f"invalid_input: {exc}", file=sys.stderr)\n        return 1',
     '    except _Invalid as exc:\n        print(f"invalid_input: {exc}", file=sys.stderr)\n        return 0'),
    ('M36-duplicate-member-deduped', 'duplicate member refusal (dedupe instead)',
     '    return sorted(names)', '    return sorted(set(names))'),
    ('M37-absent-name-not-escaped', 'escaping of names (vacuous: names are tokens)',
     ABSENT, '            parts.append(name + RS + GS)'),
    ('M35-stdout-bare-key', 'success contract (JSON object)',
     'sys.stdout.write(json.dumps({"key": key}) + "\\n")', 'sys.stdout.write(key + "\\n")'),
]


def main():
    src = SRC.read_text()
    OUT.mkdir(parents=True, exist_ok=True)
    index = []
    bad = []
    for mid, clause, old, new in MUTANTS:
        n = src.count(old)
        if n != 1:
            bad.append((mid, n))
            continue
        text = src.replace(old, new)
        assert text != src, mid
        (OUT / f'{mid}.py').write_text(text)
        index.append({'id': mid, 'clause': clause, 'old': old, 'new': new,
                      'sha256': __import__('hashlib').sha256(text.encode()).hexdigest()})
    (OUT / 'index.json').write_text(json.dumps(index, indent=1) + '\n')
    for mid, n in bad:
        print(f'ANCHOR-COUNT {mid} occurrences={n}', file=sys.stderr)
    print(f'mutants={len(index)} skipped={len(bad)}')
    return 0 if not bad else 2


if __name__ == '__main__':
    raise SystemExit(main())
