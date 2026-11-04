#!/usr/bin/env python3
"""Prove base->candidate differs on exactly one line, and only in the message."""
from pathlib import Path
import hashlib

BASE = Path('/fast/scratch/hyaku/kake-r88/ExecDefects/base-cache_current_age.py')
CAND = Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/w1/ExecDefects/cache_current_age.py')

base = BASE.read_bytes()
cand = CAND.read_bytes()
bl = base.split(b'\n')
cl = cand.split(b'\n')
print('base_sha256:', hashlib.sha256(base).hexdigest())
print('cand_sha256:', hashlib.sha256(cand).hexdigest())
print('base_bytes:', len(base), 'cand_bytes:', len(cand), 'delta_bytes:', len(cand) - len(base))
print('base_lines_split:', len(bl), 'cand_lines_split:', len(cl))
print('equal_line_count:', len(bl) == len(cl))
print('trailing_newline_preserved:', base.endswith(b'\n') == cand.endswith(b'\n'))
diff_idx = [i for i, (a, b) in enumerate(zip(bl, cl)) if a != b]
print('differing_line_numbers_1based:', [i + 1 for i in diff_idx])
print('differing_line_count:', len(diff_idx))
others_equal = all(a == b for i, (a, b) in enumerate(zip(bl, cl)) if i not in diff_idx)
print('all_other_lines_byte_identical:', others_equal)
for i in diff_idx:
    print('base_line_%d: %r' % (i + 1, bl[i].decode()))
    print('cand_line_%d: %r' % (i + 1, cl[i].decode()))
    print('base_line_%d_len: %d' % (i + 1, len(bl[i])))
    print('cand_line_%d_len: %d' % (i + 1, len(cl[i])))
print('base_message_lines:', [i + 1 for i, l in enumerate(bl) if b'must be an integer' in l])
print('cand_message_lines:', [i + 1 for i, l in enumerate(cl) if b'must be an integer' in l])
print('base_message_occurrences:', base.count(b'must be an integer'))
print('cand_message_occurrences:', cand.count(b'must be an integer'))
print('syntax_ast_parse:', end=' ')
import ast
ast.parse(cand.decode())
print('ok')
