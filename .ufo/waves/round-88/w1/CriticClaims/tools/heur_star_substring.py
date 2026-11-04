#!/usr/bin/env python3
"""Trivial rule: the literal '*' anywhere in stdin decides mismatch."""
import sys
raw = sys.stdin.read()
print('mismatch' if '*' in raw else 'match')
