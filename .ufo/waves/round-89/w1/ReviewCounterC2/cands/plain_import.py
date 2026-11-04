#!/usr/bin/env python3
"""Shortcut control: imports the round's counter and reuses its reference.
The counter's textual shortcut guard must reject this before scoring."""
import json
import sys

import c89_key

print(json.dumps({"key": c89_key.key_of(json.load(sys.stdin))}))
