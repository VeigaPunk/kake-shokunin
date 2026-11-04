#!/usr/bin/env python3
"""ExecTrial round-89 C2 real-data trial driver.

Builds cache_key inputs from recorded response headers (round-61 / round-81
capture trees), feeds each one on stdin to a candidate script in a fresh
subprocess, and records key, exit, stdout, stderr, and the fields that
participated in the key.

Usage: python3 -B trial.py <candidate.py> <out_dir> <wave_root>
  wave_root = <lane>/.ufo/waves
"""
import hashlib
import json
import os
import subprocess
import sys

CANDIDATE, OUT, WAVES = sys.argv[1], sys.argv[2], sys.argv[3]
US, RS, GS = '\x1f', '\x1e', '\x1c'
os.makedirs(OUT, exist_ok=True)


def load_capture(rel):
    path = os.path.join(WAVES, rel)
    raw_bytes = open(path, 'rb').read()
    d = json.loads(raw_bytes)
    vary_lines = [h['value'] for h in d['headers'] if h['name'].lower() == 'vary']
    combined = ', '.join(vary_lines) if vary_lines else None  # RFC 9110 s5.3 list combination
    return {
        'source': os.path.join('.ufo/waves', rel),
        'source_sha256': hashlib.sha256(raw_bytes).hexdigest(),
        'url': d['url'],
        'status': d['status'],
        'body_sha256': d['sha256'],
        'fetchedAt': d['fetchedAt'],
        'raw_vary_lines': vary_lines,
        'recorded_vary': combined,
    }


CAP = {
    'ds4cc-primary-r81': load_capture('round-81/capture/ds4cc-primary/response.json'),
    'ds4cc-sitemap-r81': load_capture('round-81/capture/ds4cc-sitemap/response.json'),
    'burnerchrome-kimi-r61': load_capture('round-61/capture/burnerchrome-kimi/response.json'),
    'vault-index-kimi-r61': load_capture('round-61/capture/vault-index-kimi/response.json'),
    'charter-ghp-r61': load_capture('round-61/capture/charter-ghp/response.json'),
    'ufo-fsd-kimi-pro-r61': load_capture('round-61/capture/ufo-fsd-kimi-pro/response.json'),
}

AE = 'gzip, deflate, br'
ORIGIN = 'https://requester.test'

# Each case: id, kind ('real' = surface URL and recorded vary; 'synthetic' = constructed),
# capture key (or None), input dict built from the recorded data.
CASES = []


def real(cid, capkey, request_headers, note):
    c = CAP[capkey]
    inp = {'uri': c['url'], 'request_headers': request_headers}
    if c['recorded_vary'] is not None:
        inp['vary'] = c['recorded_vary']
    CASES.append({'id': cid, 'kind': 'real', 'capture': capkey, 'input': inp, 'note': note})


def synth(cid, base_capkey, vary_override, request_headers, note):
    c = CAP[base_capkey]
    inp = {'uri': c['url'], 'request_headers': request_headers}
    if vary_override is not None:
        inp['vary'] = vary_override
    CASES.append({'id': cid, 'kind': 'synthetic', 'capture': base_capkey, 'input': inp, 'note': note})


# --- real-surface key construction ---
real('R1-ds4cc-primary-ae', 'ds4cc-primary-r81',
     {'Accept-Encoding': AE},
     'recorded vary Accept-Encoding (single line); status 200; request nominates only recorded field')
real('R2-burnerchrome-ae-origin-present', 'burnerchrome-kimi-r61',
     {'Accept-Encoding': AE, 'Origin': ORIGIN},
     'recorded vary arrives as two header lines (Accept-Encoding; Origin); combined by RFC 9110 s5.3')
real('R3-vault-index-ae-origin-absent', 'vault-index-kimi-r61',
     {'Accept-Encoding': AE},
     'same combined vary as R2 but Origin not presented -> GS marker path')
real('R4-charter-ghp-lowercase-names', 'charter-ghp-r61',
     {'accept-encoding': 'br'},
     'recorded Vary (capitalised header name) with lowercase request header name: case-insensitive lookup')
real('R5-ufo-fsd-kimi-pro-no-vary', 'ufo-fsd-kimi-pro-r61',
     {},
     'recorded response carries no Vary header -> vary absent -> key is ESC(uri) alone')
real('R6-ds4cc-sitemap-ae', 'ds4cc-sitemap-r81',
     {'Accept-Encoding': 'gzip'},
     'second path on same host, same recorded vary; different URI -> different key')

# --- present-empty vs absent, on real vary ---
real('R2b-burnerchrome-origin-present-empty', 'burnerchrome-kimi-r61',
     {'Accept-Encoding': AE, 'Origin': ''},
     'same as R2 but Origin presented as empty -> present-empty path (must differ from R3)')

# --- refusal cases ---
# No capture carries a Vary wildcard (verified by scan of all response.json under waves/).
# Refusals below are SYNTHETIC inputs built on a real surface URL and recorded vary.
synth('X1-synthetic-wildcard-on-ds4cc', 'ds4cc-primary-r81', '*',
      {'Accept-Encoding': AE},
      'SYNTHETIC: recorded surface, vary replaced with the wildcard; no capture carries *')
synth('X2-synthetic-trailing-comma-on-burnerchrome', 'burnerchrome-kimi-r61',
      CAP['burnerchrome-kimi-r61']['recorded_vary'] + ',',
      {'Accept-Encoding': AE, 'Origin': ORIGIN},
      'SYNTHETIC: recorded combined vary with trailing comma appended -> empty member')
synth('X3-synthetic-duplicate-header-case-on-burnerchrome', 'burnerchrome-kimi-r61',
      CAP['burnerchrome-kimi-r61']['recorded_vary'],
      {'Accept-Encoding': AE, 'origin': ORIGIN, 'Origin': ORIGIN},
      'SYNTHETIC: origin presented twice differing only in case -> duplicate refusal')
synth('X4-synthetic-crlf-in-origin-value', 'burnerchrome-kimi-r61',
      CAP['burnerchrome-kimi-r61']['recorded_vary'],
      {'Accept-Encoding': AE, 'Origin': 'https://requester.test\r\nX-Injected: 1'},
      'SYNTHETIC: CR/LF in presented value -> refusal')
synth('X5-synthetic-vary-duplicate-member-case', 'vault-index-kimi-r61',
      'Accept-Encoding, accept-encoding',
      {'Accept-Encoding': AE},
      'SYNTHETIC: duplicate vary member differing only in case -> refusal')


def run(case):
    payload = json.dumps(case['input'], ensure_ascii=True)
    p = subprocess.run([sys.executable, '-B', CANDIDATE], input=payload,
                       capture_output=True, text=True, timeout=30,
                       cwd=OUT)
    rec = {
        'id': case['id'], 'kind': case['kind'], 'capture': case['capture'],
        'note': case['note'], 'stdin_json': payload, 'exit': p.returncode,
        'stdout': p.stdout, 'stderr': p.stderr.strip(),
        'key': None, 'participating_fields': None,
    }
    if p.returncode == 0:
        key = json.loads(p.stdout)['key']
        rec['key'] = key
        parts = key.split(US)
        fields = []
        for part in parts[1:]:
            name, _, rest = part.partition(RS)
            if rest == GS:
                state = 'absent'
                val = None
            else:
                state = 'present-empty' if rest == '' else 'present'
                val = rest
            fields.append({'name': name, 'state': state, 'value_escaped': val})
        rec['participating_fields'] = fields
    return rec


results = [run(c) for c in CASES]
with open(os.path.join(OUT, 'results.json'), 'w') as f:
    json.dump({'candidate': CANDIDATE, 'captures': CAP, 'cases': results},
              f, indent=2, ensure_ascii=False)
for r in results:
    print(f"{r['id']}\texit={r['exit']}\tkey={r['key']!r}\terr={r['stderr']!r}")
