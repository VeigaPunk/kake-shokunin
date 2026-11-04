#!/usr/bin/env python3
"""Round-90 frozen sandbox negative: delegates to the round-89 counter's reference
by putting its directory on sys.path. Behaviourally it may be conformant; it breaks
the candidate rule "must not import the counter", so a gate must refuse it."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "round-89"))
import c89_key  # noqa: E402

try:
    obj = json.load(sys.stdin)
    key = c89_key.key_of(obj)
except Exception as exc:  # refusal path
    print("invalid_input: %s" % exc, file=sys.stderr)
    sys.exit(1)
sys.stdout.write(json.dumps({"key": key}) + "\n")
