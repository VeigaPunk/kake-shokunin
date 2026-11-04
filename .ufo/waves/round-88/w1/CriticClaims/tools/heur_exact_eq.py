#!/usr/bin/env python3
"""Trivial rule: match iff the two JSON objects are byte-equal in Python."""
import json, sys
c = json.load(sys.stdin)
print('match' if c.get('stored') == c.get('presented') else 'mismatch')
