#!/usr/bin/env python3
"""Offline selftest for round-26 source_text.text_of/normalize and committed text views.

Synthetic cases pin HTML skip tags, entity decoding, whitespace and punctuation
normalization, non-HTML passthrough and invalid UTF-8 replacement. normalize is also
compared with scripts/accessibility_packet.py normalized. Every fetched text view must
equal text_of(gunzip(raw)) plus one trailing LF for its effective fetch; the retry
manifest supersedes the failed attempt of the same row and index.

Standard library only; writes nothing. Prints one JSON summary; exit 0 when every case
passes, 1 otherwise.
"""
import functools
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True

SCHEMA = 'kake-r26-text-selftest-v1'
ROOT = Path(__file__).resolve().parents[4]
WAVE = ROOT / '.ufo/waves/round-26'
FETCHED = WAVE / 'fetched'

# (case, raw bytes, content type, expected text_of output)
TEXT_CASES = [
    ('skip_script', b'<p>Keep</p><script>var x = 1;</script><p>Also</p>', 'text/html', 'Keep Also'),
    ('skip_style', b'<style>p { color: red; }</style><p>Visible</p>', 'text/html; charset=utf-8', 'Visible'),
    ('skip_noscript', b'<noscript>Enable JS</noscript><p>Shown</p>', 'text/html', 'Shown'),
    ('skip_template', b'<template><p>Hidden</p></template>Shown', 'text/html', 'Shown'),
    ('skip_uppercase_tags', b'<SCRIPT>x</SCRIPT><Template>y</Template>z', 'text/html', 'z'),
    ('skip_nested_noscript_template', b'<noscript><template>x</template>y</noscript>z', 'text/html', 'z'),
    ('skip_nested_template', b'<template>a<template>b</template>c</template>d', 'text/html', 'd'),
    ('skip_style_inside_template', b'<template><style>a{}</style></template>d', 'text/html', 'd'),
    ('skip_stray_end_tags_do_not_underflow', b'</style>a</script>b<script>c</script>d', 'text/html', 'a b d'),
    ('skip_html_comment', b'<p>a</p><!-- <script>x</script> -->b', 'text/html', 'a b'),
    ('entities_named_and_numeric',
     b'<p>Tom &amp; Jerry &lt;3 &quot;x&quot; &#39;y&#39; &#x41;&#66;</p>',
     'text/html', 'Tom & Jerry <3 "x" \'y\' AB'),
    ('entities_nbsp_and_copy', b'<p>Copyright&nbsp;&copy;&nbsp;2026</p>', 'text/html', 'Copyright \u00a9 2026'),
    ('entities_unknown_left_alone', b'<p>a &zzqq; b</p>', 'text/html', 'a &zzqq; b'),
    ('entities_amp_lt_decoded_once', b'<p>&amp;lt;</p>', 'text/html', '&lt;'),
    ('entities_amp_amp_decoded_once', b'<p>&amp;amp;</p>', 'text/html', '&amp;'),
    ('html_block_gap_collapses', b'<p>One</p>\n\n<p>Two ,</p>', 'text/html', 'One Two,'),
    ('plain_whitespace_and_punctuation', b'  one\n\ttwo ,  three ( four ) .  ', 'text/plain; charset=utf-8',
     'one two, three (four).'),
    ('plain_entities_and_tags_untouched', b'Tom &amp; Jerry <b>bold</b> &lt;x&gt;', 'text/plain',
     'Tom &amp; Jerry <b>bold</b> &lt;x&gt;'),
    ('plain_script_not_skipped', b'<script>x</script>y', 'text/plain', '<script>x</script>y'),
    ('json_passthrough', b'{"html": "<script>x</script>"}', 'application/json', '{"html": "<script>x</script>"}'),
    ('empty_input', b'', None, ''),
    ('content_type_case_insensitive', b'<p>a</p>', 'Text/HTML; charset=UTF-8', 'a'),
    ('sniff_doctype_without_content_type',
     b'  \n<!DOCTYPE html><html><body><p>Hi &amp; bye</p><script>x</script></body></html>', None, 'Hi & bye'),
    ('sniff_html_without_content_type', b'<html><body>Hi</body></html>', None, 'Hi'),
    ('utf8_invalid_byte_plain', b'a\xffb', 'text/plain', 'a\ufffdb'),
    ('utf8_overlong_and_stray_continuation', b'\xc0\xaf', None, '\ufffd\ufffd'),
    ('utf8_truncated_sequence', b'x\xe2\x82', 'text/plain', 'x\ufffd'),
    ('utf8_invalid_in_html', b'<p>a\xffb</p>', 'text/html', 'a\ufffdb'),
    ('utf8_invalid_run', b'\xff\xfe\x80', None, '\ufffd\ufffd\ufffd'),
]

# (case, input, expected normalize output)
NORMALIZE_CASES = [
    ('normalize_whitespace_and_punctuation', 'A\n\t B  ,  C ( D ) ; E :F .', 'A B, C (D); E:F.'),
    ('normalize_unicode_whitespace', 'a\u00a0\u2003b\tc\r\nd\x0b\x0ce', 'a b c d e'),
    ('normalize_paren_spacing', '( open) and close (x )', '(open) and close (x)'),
    ('normalize_inner_punctuation_kept', 'f(x) , g(y) .', 'f(x), g(y).'),
    ('normalize_blank_is_empty', ' \t\n ', ''),
    ('normalize_square_bracket_spacing_as_accessibility_packet', 'x [ y ] z', 'x [ y ] z'),
]

# Compared with accessibility_packet.normalized; includes controls and the closing-bracket case.
DIFFERENTIAL_INPUTS = [
    'A\n\t B  ,  C ( D ) ; E :F .',
    'a\u00a0\u2003b\tc\r\nd\x0b\x0ce',
    '( open) and close (x )',
    'f(x) , g(y) .',
    'p(q ) r : s ; t . u',
    'a [b] , c',
    'x [ y ] z',
    'a ] b',
    'end ]',
    ' \t\n ',
]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def record(rows, name, detail):
    rows.append({'case': name, 'passed': detail is None, 'detail': detail})


def guarded(rows, name, check):
    try:
        record(rows, name, check())
    except Exception as exc:  # a crashing case is a failed case, never a bare traceback
        record(rows, name, f'{type(exc).__name__}: {exc}')


def text_case(text_of, raw, content_type, expected):
    first = text_of(raw, content_type)
    second = text_of(raw, content_type)
    if first == expected and second == expected:
        return None
    return {'expected': expected, 'actual': first, 'second_call': second}


def normalize_case(normalize, text, expected):
    actual = normalize(text)
    return None if actual == expected else {'expected': expected, 'actual': actual}


def differential_case(normalize, accessibility, inputs):
    mismatches = []
    for text in inputs:
        ours, reference = normalize(text), accessibility.normalized(text)
        if ours != reference:
            mismatches.append({'input': text, 'normalize': ours, 'accessibility_packet': reference})
    return mismatches or None


def fetch_key(entry):
    return entry['row'], entry['index']


def view_case(text_of, entry):
    raw = gzip.decompress((FETCHED / entry['file']).read_bytes())
    expected = (text_of(raw, entry['headers'].get('content-type')) + '\n').encode('utf-8')
    actual = (FETCHED / 'text' / f"{entry['row']}-{entry['index']}.txt").read_bytes()
    checks = {
        'raw_sha256_matches_manifest': hashlib.sha256(raw).hexdigest() == entry['sha256'],
        'raw_bytes_match_manifest': len(raw) == entry['bytes'],
        'view_equals_text_of_plus_lf': actual == expected,
    }
    if all(checks.values()):
        return None
    detail = {'raw_file': entry['file'], **checks, 'expected_bytes': len(expected), 'actual_bytes': len(actual)}
    if not checks['view_equals_text_of_plus_lf']:
        detail['first_difference_byte'] = next(
            (i for i, (a, b) in enumerate(zip(actual, expected)) if a != b), min(len(actual), len(expected)))
    return detail


def corpus_cases(rows, text_of):
    manifest = json.loads((FETCHED / 'manifest.json').read_bytes())
    retry = json.loads((FETCHED / 'manifest-retry.json').read_bytes())
    base = {fetch_key(entry): entry for entry in manifest}
    effective = dict(base)
    effective.update({fetch_key(entry): entry for entry in retry})

    superseded = []
    for key in map(fetch_key, retry):
        if key not in base or base[key]['status'] == 200:
            superseded.append({'key': f'{key[0]}-{key[1]}',
                               'manifest_status': base[key]['status'] if key in base else None})
    record(rows, 'retry_supersedes_failed_attempt_only', superseded or None)

    not_ok = [f'{row}-{index}' for (row, index), entry in sorted(effective.items())
              if entry['status'] != 200 or entry.get('error') is not None]
    record(rows, 'effective_fetches_status_200_without_error', not_ok or None)

    expected_names = {f'{row}-{index}.txt' for row, index in effective}
    actual_names = {path.name for path in (FETCHED / 'text').glob('*.txt')}
    record(rows, 'text_views_are_exactly_the_effective_fetches',
           None if expected_names == actual_names else
           {'missing': sorted(expected_names - actual_names), 'extra': sorted(actual_names - expected_names)})

    for key in sorted(effective):
        guarded(rows, f'fetch_view:{key[0]}-{key[1]}', functools.partial(view_case, text_of, effective[key]))


def main():
    rows = []
    try:
        source_text = load_module('round26_source_text', WAVE / 'source_text.py')
        accessibility = load_module('kake_accessibility_packet', ROOT / 'scripts/accessibility_packet.py')
        text_of, normalize = source_text.text_of, source_text.normalize
    except Exception as exc:
        print(json.dumps({'schema': SCHEMA, 'passed': False, 'error': f'{type(exc).__name__}: {exc}'},
                         sort_keys=True))
        return 1
    for name, raw, content_type, expected in TEXT_CASES:
        guarded(rows, name, functools.partial(text_case, text_of, raw, content_type, expected))
    for name, text, expected in NORMALIZE_CASES:
        guarded(rows, name, functools.partial(normalize_case, normalize, text, expected))
    guarded(rows, 'normalize_matches_accessibility_packet',
            functools.partial(differential_case, normalize, accessibility, DIFFERENTIAL_INPUTS))
    try:
        corpus_cases(rows, text_of)
    except Exception as exc:
        record(rows, 'corpus_inputs_load', f'{type(exc).__name__}: {exc}')
    failed = [row['case'] for row in rows if not row['passed']]
    print(json.dumps({'schema': SCHEMA, 'python': sys.version.split()[0], 'passed': not failed,
                      'total': len(rows), 'failed': failed, 'rows': rows}, sort_keys=True))
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
