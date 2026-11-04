#!/usr/bin/env python3
"""Verify the S455 quotes against the retained bytes: raw-substring + line + word count."""
import hashlib, sys
P='/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-82/w1/ScoutSources/rfc9110.txt'
b=open(P,'rb').read(); t=b.decode('utf-8')
print('path', P)
print('bytes', len(b))
print('sha256', hashlib.sha256(b).hexdigest())
cases=[
 ('ETAG_DEFINITION_RAW_24W',
  'The "ETag" field in a response provides the current entity tag for\n'
  '   the selected representation, as determined at the conclusion of\n'
  '   handling the request.'),
 ('STRONG_DEF_FRAGMENT_RAW_16W',
  'representation metadata that changes value\n'
  '   whenever a change occurs to the representation data that would be'),
 ('STRONG_DEF_SINGLE_LINE_RAW_9W',
  'A "strong validator" is representation metadata that changes value'),
 ('STRONG_DEF_FULL_SENTENCE_COLLAPSED_31W',
  'A "strong validator" is representation metadata that changes value whenever a change occurs to the '
  'representation data that would be observable in the content of a 200 (OK) response to GET.'),
 ('WEAK_DEF_RAW_17W',
  'a "weak validator" is representation metadata that might\n'
  '   not change for every change to the representation data.'),
 ('STRONG_COMPARISON_RAW_15W',
  'two entity tags are equivalent if both are not\n'
  '      weak and their opaque-tags match character-by-character.'),
]
for name,q in cases:
    i=t.find(q)
    ln=t[:i].count('\n')+1 if i>=0 else None
    endline=t[:i+len(q)].count('\n')+1 if i>=0 else None
    print(f'{name}\traw={i>=0}\twords={len(q.split())}\tlines={ln}-{endline}\toffset={i}')
print('--- headings ---')
for n in ('8.8.1.  Weak versus Strong','8.8.2.  Last-Modified','8.8.3.  ETag','8.8.3.1.  Generation','8.8.3.2.  Comparison','8.8.3.3.  Example'):
    i=t.find('\n'+n)
    print(f'{n!r}\tline={t[:i+1].count(chr(10))+1 if i>=0 else None}')
i=t.find('\n9.  Methods')
print('next top-level 9. Methods\tline=', t[:i+1].count(chr(10))+1 if i>=0 else None)
