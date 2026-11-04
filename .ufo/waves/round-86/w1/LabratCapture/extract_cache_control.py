#!/usr/bin/env python3
"""Read the three assigned trees; emit only Cache-Control values and counts."""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
TREES = [LANE / '.ufo/waves/round-82/population',
         LANE / '.ufo/waves/round-82/capture',
         LANE / '.ufo/waves/round-83/capture-control']


def directives(value):
    # Commas inside quoted field-name lists are not directive separators.
    parts, start, quoted, escaped = [], 0, False, False
    for index, char in enumerate(value):
        if escaped:
            escaped = False
        elif quoted and char == '\\':
            escaped = True
        elif char == '"':
            quoted = not quoted
        elif char == ',' and not quoted:
            parts.append(value[start:index])
            start = index + 1
    parts.append(value[start:])
    return [{'name': part.split('=', 1)[0].strip().lower(),
             'text': part.strip()} for part in parts if part.strip()]


def main():
    inventory, values, errors, missing = [], [], [], []
    histogram = Counter()
    duplicate_values, duplicate_responses, conflicts = [], [], []
    for tree in TREES:
        if not tree.is_dir():
            missing.append(str(tree))
            continue
        for path in sorted(tree.rglob('*.json')):
            raw = path.read_bytes()
            item = {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest()}
            inventory.append(item)
            try:
                payload = json.loads(raw)
            except (ValueError, UnicodeDecodeError) as exc:
                errors.append({'path': str(path), 'error_type': type(exc).__name__})
                continue
            headers = payload.get('headers') if isinstance(payload, dict) else None
            item['headers_list_present'] = isinstance(headers, list)
            item['cache_control_values'] = 0
            if headers is None:
                continue
            if not isinstance(headers, list):
                errors.append({'path': str(path), 'error': 'headers is not a list'})
                continue
            response_names = Counter()
            for index, header in enumerate(headers):
                if not isinstance(header, dict) or not isinstance(header.get('name'), str):
                    errors.append({'path': str(path), 'header_index': index,
                                   'error': 'unexpected header shape'})
                    continue
                if header['name'].strip().lower() != 'cache-control':
                    continue
                value = header.get('value')
                if not isinstance(value, str):
                    errors.append({'path': str(path), 'header_index': index,
                                   'error': 'Cache-Control value is not a string'})
                    continue
                parsed = directives(value)
                names = Counter(d['name'] for d in parsed)
                duplicates = {name: count - 1 for name, count in names.items() if count > 1}
                record = {'path': str(path), 'header_index': index, 'value': value,
                          'directives': parsed, 'duplicate_extra_occurrences': duplicates}
                values.append(record)
                item['cache_control_values'] += 1
                histogram.update(names)
                response_names.update(names)
                if duplicates:
                    duplicate_values.append(record)
            repeats = {name: count - 1 for name, count in response_names.items() if count > 1}
            if repeats:
                duplicate_responses.append({'path': str(path), 'duplicate_extra_occurrences': repeats})
            if response_names['max-age'] and response_names['no-cache']:
                conflicts.append(str(path))
    max_age_repeats = sum(r['duplicate_extra_occurrences'].get('max-age', 0)
                          for r in duplicate_responses)
    complete = not missing and not errors
    result = {
        'scope': [str(tree) for tree in TREES], 'inventory': inventory,
        'missing_trees': missing, 'errors': errors,
        'summary': {
            'json_files': len(inventory),
            'files_with_headers_lists': sum(i.get('headers_list_present', False) for i in inventory),
            'total_values': len(values), 'directive_histogram': dict(sorted(histogram.items())),
            'values_with_duplicate_directives': len(duplicate_values),
            'duplicate_extra_occurrences_within_values': sum(sum(v['duplicate_extra_occurrences'].values()) for v in duplicate_values),
            'responses_with_duplicate_directives': len(duplicate_responses),
            'duplicate_extra_occurrences_across_field_lines': sum(sum(r['duplicate_extra_occurrences'].values()) for r in duplicate_responses),
            'duplicate_max_age_extra_occurrences_across_field_lines': max_age_repeats,
            's_maxage_occurrences': histogram['s-maxage'],
            'no_store_occurrences': histogram['no-store'],
            'max_age_no_cache_conflict_responses': len(conflicts)},
        'values': values, 'duplicate_values': duplicate_values,
        'duplicate_responses': duplicate_responses, 'conflict_paths': conflicts,
        'verdict': ('confirmed' if values and max_age_repeats == 0 else 'refuted') if complete else 'incomplete',
        'limit': 'Only the three assigned trees; no live requests or r84/r85 tree expansion. Synthetic-only duplicate exercise is bounded to this retained population, not all possible captures.'}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if complete else 1


if __name__ == '__main__':
    sys.exit(main())
