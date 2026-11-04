#!/usr/bin/env python3
"""Review instrument: indep.py pinned to the counter's refusal policy.

The round-88 scorer invokes the candidate with no arguments, so this wrapper
exists only to feed the same reader through the official --tool path with the
refusals the counter's own reference applies.  It is not a candidate.
"""
import sys

sys.path.insert(0, '/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/w1/ReviewReader')
import indep

FLAGS = ['--refuse-empty-elements', '--refuse-empty-list',
         '--refuse-combined-lines', '--keep-ctl']

raise SystemExit(indep.main(['indep.py'] + FLAGS + sys.argv[1:]))
