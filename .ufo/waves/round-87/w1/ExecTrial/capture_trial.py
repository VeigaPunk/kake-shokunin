#!/usr/bin/env python3
"""Round-87 ExecTrial: ONE real GET to https://ds4cc.com/, sanitized record + receipt.

Retains only: public Date / Age / Cache-Control headers, status, final URL,
request/response times, body sha256/bytes (+body file when 0 < bytes <= cap).
Cookies, authorization and every other header are dropped, never written.
Missing/invalid Date or non-digit Age => honest could-not-evaluate; nothing
synthetic is ever relabeled as observed timing.
"""
import email.utils
import hashlib
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

OUT = Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecTrial')
URL = 'https://ds4cc.com/'
CAP = 2 * 1024 * 1024  # 2 MiB cap on retained body


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


record = {
    'seat': 'ExecTrial',
    'round': 'kake-r87-w1',
    'trial': 'C2 cache_current_age single-property GET',
    'method': 'GET',
    'requested_url': URL,
    'user_agent': 'kake-r87-exectrial/1 (stdlib urllib; single public GET)',
    'body_cap_bytes': CAP,
}

request_time = int(time.time())
record['request_time'] = request_time

body = b''
final_url = None
status = None
headers = None
transport_error = None
try:
    req = urllib.request.Request(URL, headers={'User-Agent': record['user_agent']})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read(CAP)
        response_time = int(time.time())  # immediately after reading body
        final_url = r.geturl()
        status = r.status
        headers = r.headers
except urllib.error.HTTPError as e:
    # An HTTP error response is still an observed response; capture honestly.
    try:
        body = e.read(CAP)
    except Exception:
        body = b''
    response_time = int(time.time())
    final_url = e.geturl() if hasattr(e, 'geturl') else URL
    status = e.code
    headers = e.headers
    transport_error = f'HTTPError {e.code}'
except Exception as e:  # URLError, timeouts, TLS: no observed response at all
    response_time = int(time.time())
    transport_error = f'{type(e).__name__}: {e}'

record['response_time'] = response_time
record['trial_now'] = max(response_time, int(time.time()))
record['status'] = status
record['final_url'] = final_url
record['redirected'] = bool(final_url is not None and final_url != URL)
record['transport_error'] = transport_error
record['captured_at_utc'] = email.utils.formatdate(record['trial_now'], usegmt=True)

# --- sanitized public headers only ---
date_raw = headers.get('Date') if headers is not None else None
age_raw = headers.get('Age') if headers is not None else None
cc_raw = headers.get('Cache-Control') if headers is not None else None
record['date_header'] = date_raw
record['cache_control_header'] = cc_raw
record['age_header'] = age_raw

date_epoch = None
if date_raw is None:
    date_note = 'absent'
else:
    try:
        dt = email.utils.parsedate_to_datetime(date_raw)
    except (TypeError, ValueError):
        dt = None
    if dt is None:
        date_note = 'unparseable'
    elif dt.tzinfo is None:
        date_note = 'naive_unusable'
    else:
        date_epoch = int(dt.timestamp())  # aware GMT -> epoch seconds
        date_note = 'ok'
record['date_epoch'] = date_epoch
record['date_note'] = date_note

if age_raw is None:
    age_value, age_note = 0, 'absent_default_0'
elif re.fullmatch(r'[0-9]+', age_raw):
    age_value, age_note = int(age_raw), 'ok'
else:
    age_value, age_note = None, 'invalid_not_digits'
record['age_value'] = age_value
record['age_note'] = age_note

record['body_bytes'] = len(body)
record['body_may_be_truncated'] = len(body) == CAP
record['body_sha256'] = sha256_hex(body) if body else None

# --- trial status; never fabricate inputs ---
if transport_error is not None and status is None:
    trial_status, trial_reason = 'could_not_evaluate', f'no_response: {transport_error}'
elif date_note != 'ok':
    trial_status, trial_reason = 'could_not_evaluate', f'date_{date_note}'
elif age_note == 'invalid_not_digits':
    trial_status, trial_reason = 'could_not_evaluate', 'age_header_invalid'
else:
    trial_status, trial_reason = 'evaluable', None
record['trial_status'] = trial_status
record['trial_reason'] = trial_reason
record['tool_input'] = (
    {
        'date_value': date_epoch,
        'request_time': request_time,
        'response_time': response_time,
        'now': record['trial_now'],
        'age_value': age_value,
    }
    if trial_status == 'evaluable'
    else None
)

OUT.mkdir(parents=True, exist_ok=True)
if body:
    (OUT / 'body.html').write_bytes(body)
record_path = OUT / 'trial-record.json'
record_path.write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')

receipt = {
    'artifact': 'ExecTrial single GET capture',
    'command': 'python3 -B capture_trial.py  (cwd: /fast/scratch/hyaku/kake-r87/ExecTrial-2)',
    'exit': 0,
    'url': URL,
    'request_time': request_time,
    'response_time': response_time,
    'trial_now': record['trial_now'],
    'status': status,
    'final_url': final_url,
    'redirected': record['redirected'],
    'transport_error': transport_error,
    'trial_status': trial_status,
    'trial_reason': trial_reason,
    'retained_files': {
        'trial-record.json': sha256_hex(record_path.read_bytes()),
        'body.html': sha256_hex((OUT / 'body.html').read_bytes()) if body else None,
    },
    'retained_bytes': {'trial-record.json': record_path.stat().st_size, 'body.html': len(body)},
    'sanitization': 'only Date/Age/Cache-Control/status/final URL/times/sha256/bytes retained; no cookies, no auth, no other headers',
}
(OUT / 'receipt.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
print(json.dumps(receipt, sort_keys=True))
