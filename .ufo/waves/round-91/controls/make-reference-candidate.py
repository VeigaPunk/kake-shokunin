#!/usr/bin/env python3
"""Builds controls/reference-candidate.py: a frozen byte-copy of the reference block of
the round-91 C2 counter. The copy is generated from the counter source at freeze time so
the two cannot drift; it is a reachability CONTROL, never the shipped tool."""
import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTER = os.path.join(os.path.dirname(HERE), "c91_reuse.py")
src = open(COUNTER).read()
start = src.index("CACHEABLE = (200,")
end = src.index("def H(name, stored_cc")
block = src[start:end].rstrip() + "\n"
head = '''#!/usr/bin/env python3
"""Reachability control (not a claimed positive): the round-91 C2 counter's own reference.

Generated at freeze time by controls/make-reference-candidate.py as a byte-copy of the
counter's reference block (counter sha256 %s). It exists to show the contract is
implementable and the battery satisfiable before any candidate exists. It is a control
fixture, never the shipped tool, and proves nothing about independent authorship.
"""
import json
import re
import sys


''' % hashlib.sha256(src.encode()).hexdigest()
tail = '''

def main():
    try:
        inp = json.loads(sys.stdin.read())
        out = reference(inp)
    except Invalid as exc:
        sys.stderr.write("invalid_input: %s\\n" % exc)
        return 1
    except ValueError:
        sys.stderr.write("invalid_input: not JSON\\n")
        return 1
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''
out = os.path.join(HERE, "reference-candidate.py")
open(out, "w").write(head + block + tail)
print("wrote %s bytes=%d" % (out, os.path.getsize(out)))
