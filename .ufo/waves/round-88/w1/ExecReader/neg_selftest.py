"""Red-path driver for vary_match.py: force one selftest expectation wrong.

Expected: 'selftest: 34/35 passed' and exit 1, proving the 35/35 green result is
falsifiable. No file is modified; only the in-memory case table is perturbed.
"""
import importlib.util
import sys
from pathlib import Path

TOOL = Path(__file__).with_name('vary_match.py')
spec = importlib.util.spec_from_file_location('candidate', TOOL)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.SELFTEST_CASES = list(module.SELFTEST_CASES)
label, payload, expected = module.SELFTEST_CASES[0]
module.SELFTEST_CASES[0] = (label, payload,
                            'mismatch' if expected != 'mismatch' else 'match')
raise SystemExit(module.selftest())
