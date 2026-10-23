#!/usr/bin/env python3
"""Round-38 C1 pre-freeze control: junk (do nothing, unparseable output).

Prints `not a report` and exits 0. The counter's judge cannot load the stdout as a
JSON object, so no case can pass. Expected 0 of 20.
"""
import sys

print("not a report")
sys.exit(0)
