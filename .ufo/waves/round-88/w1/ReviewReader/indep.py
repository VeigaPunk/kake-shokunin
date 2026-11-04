#!/usr/bin/env python3
"""Independent Vary-match reader — round-88 review copy (seat ReviewReader).

Written from RFC 9111 section 4.1 and RFC 9110 sections 5.1, 5.2, 5.3, 5.5,
5.6.1 plus the declared round-88 profile in contract.md.  This file was
written before scripts/vary_match.py existed in the lane and before
ExecReader's candidate was read (neither had bytes at 2026-11-04T15:5x).

CLI contract (contract.md):
  stdin  : one JSON object {"vary": <string>, "stored": {name: value|list},
                            "presented": {name: value|list}}
  exit 0 + stdout "match"    -> the stored response may be reused
  exit 0 + stdout "mismatch" -> it may not (conservative exact profile)
  exit 1 + stderr "invalid_input: ..." and empty stdout -> refused input

Default verdicts follow the spec reading of the declared profile:
  * field names compare ASCII case-insensitively                      (9110 5.1)
  * repeated field lines combine in order into one field value,
    separated by a comma                                             (9110 5.2)
  * empty list elements in Vary are parsed and ignored                (9110 5.6.1.2)
  * a field value excludes leading/trailing OWS                       (9110 5.5)
  * after OWS removal values compare byte-identically — no field-specific
    normalisation (declared conservative profile)
  * CR, LF and NUL inside a field value are replaced by SP             (9110 5.5)
  * absent from both requests matches; absent from one does not
  * a "*" member always fails to match                              (9111 4.1)

Optional flags expose the places where the declared profile is silent or
stricter than the spec; they are review instruments, not part of the scored
contract:
  --refuse-empty-elements   refuse a Vary list containing an empty element
                            instead of ignoring it (round-88 counter behaviour)
  --refuse-empty-list       refuse [] instead of reading it as "no field lines"
  --refuse-combined-lines   refuse two JSON keys that are the same field name
                            in different case instead of combining them
  --keep-ctl                compare CR/LF/NUL raw instead of replacing with SP
  --explain                 print {"verdict":..., "reason":..., "checks":[...]}
"""
import json
import string
import sys

TCHAR = frozenset("!#$%&'*+-.^_`|~" + string.digits + string.ascii_letters)
OWS = ' \t'
CTL_INVALID = ('\r', '\n', '\x00')
# Serialisation used when a field name spans several lines (RFC 9110 5.3).
JOIN = ', '


class Refused(Exception):
    def __init__(self, reason, detail=''):
        super().__init__(reason)
        self.reason = reason
        self.detail = detail


def is_token(text):
    return isinstance(text, str) and text != '' and all(c in TCHAR for c in text)


def split_members(vary, refuse_empty):
    """Split Vary (ABNF: 1#field-name — a list) into stripped members."""
    members = [m.strip(OWS) for m in vary.split(',')]
    if refuse_empty:
        for m in members:
            if m == '':
                raise Refused('empty_list_element', 'Vary has an empty list element')
        return members
    kept = [m for m in members if m != '']
    if kept:
        return kept
    # Every element was empty: the list is empty, i.e. the field nominates
    # nothing.  A zero-member list is a legal recipient-side reading of
    # "#element => [ element ] *( OWS "," OWS [ element ] )" (RFC 9110 5.6.1.2).
    return []


def parse_vary(vary, refuse_empty):
    if not isinstance(vary, str):
        raise Refused('vary_not_string', 'Vary value is not a string')
    members = split_members(vary, refuse_empty)
    names, star = [], False
    for m in members:
        if m == '*':
            star = True
        elif is_token(m):
            names.append(m.lower())
        else:
            raise Refused('member_not_token', 'Vary member %r is not a field-name token' % m)
    return names, star


def clean_value(value, keep_ctl):
    """Apply the 9110 5.5 edge-OWS removal (definitional) and CR/LF/NUL rule."""
    if not isinstance(value, str):
        raise Refused('value_not_string', 'field value is not a string')
    if not keep_ctl:
        for bad in CTL_INVALID:
            if bad in value:
                value = value.replace(bad, ' ')
    return value.strip(OWS)


def combine(side, refuse_combined, keep_ctl, refuse_empty_list):
    """Return {lower-name: combined field value} for one request side."""
    if not isinstance(side, dict):
        raise Refused('side_not_object', 'request side is not a JSON object')
    out = {}
    for key, value in side.items():
        if not is_token(key):
            raise Refused('field_name_not_token', 'field name %r is not a token' % (key,))
        if isinstance(value, list):
            if not all(isinstance(v, str) for v in value):
                raise Refused('value_not_string', 'list value holds a non-string')
            if not value:
                if refuse_empty_list:
                    raise Refused('empty_list_value', 'field value is an empty list')
                continue  # zero field lines == the field is absent
            piece = JOIN.join(value)
        elif isinstance(value, str):
            piece = value
        else:
            raise Refused('value_not_string', 'field value is not a string or list')
        low = key.lower()
        if low in out:
            if refuse_combined:
                raise Refused('duplicate_field_name',
                              'two field lines with the same name %r' % (key,))
            out[low] = out[low] + JOIN + piece
        else:
            out[low] = piece
    return {name: clean_value(v, keep_ctl) for name, v in out.items()}


def verdict(payload, opts):
    if not isinstance(payload, dict):
        raise Refused('input_not_object', 'stdin is not one JSON object')
    for key in ('vary', 'stored', 'presented'):
        if key not in payload:
            raise Refused('missing_key', 'input lacks %r' % (key,))
    names, star = parse_vary(payload['vary'], opts['refuse_empty_elements'])
    stored = combine(payload['stored'], opts['refuse_combined_lines'],
                     opts['keep_ctl'], opts['refuse_empty_list'])
    presented = combine(payload['presented'], opts['refuse_combined_lines'],
                        opts['keep_ctl'], opts['refuse_empty_list'])
    if star:
        return 'mismatch', 'vary_star_member', []
    checks = []
    seen = set()
    for name in names:
        if name in seen:
            continue
        seen.add(name)
        left = stored.get(name)
        right = presented.get(name)
        if left is None and right is None:
            checks.append([name, 'absent-both'])
            continue
        if left is None or right is None:
            checks.append([name, 'present-one-side'])
            return 'mismatch', 'nominated_field_present_one_side', checks
        if left != right:
            checks.append([name, 'value-differs'])
            return 'mismatch', 'nominated_field_value_differs', checks
        checks.append([name, 'equal'])
    return 'match', 'all_nominated_fields_equal', checks


def main(argv):
    opts = dict(refuse_empty_elements=False, refuse_empty_list=False,
                refuse_combined_lines=False, keep_ctl=False, explain=False)
    for arg in argv[1:]:
        if arg == '--refuse-empty-elements':
            opts['refuse_empty_elements'] = True
        elif arg == '--refuse-empty-list':
            opts['refuse_empty_list'] = True
        elif arg == '--refuse-combined-lines':
            opts['refuse_combined_lines'] = True
        elif arg == '--keep-ctl':
            opts['keep_ctl'] = True
        elif arg == '--explain':
            opts['explain'] = True
        else:
            sys.stderr.write('invalid_input: unknown argument %r\n' % (arg,))
            return 1
    try:
        payload = json.load(sys.stdin)
    except (ValueError, UnicodeDecodeError) as exc:
        sys.stderr.write('invalid_input: stdout is not JSON: %s\n' % (exc,))
        return 1
    try:
        result, reason, checks = verdict(payload, opts)
    except Refused as exc:
        sys.stderr.write('invalid_input: %s: %s\n' % (exc.reason, exc.detail))
        return 1
    if opts['explain']:
        sys.stdout.write(json.dumps({'verdict': result, 'reason': reason,
                                     'checks': checks}, sort_keys=True) + '\n')
    else:
        sys.stdout.write(result + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
