#!/usr/bin/env python3
"""Forgery: refuses every input, valid or not (blanket refusal is not a
decision procedure; the population's positive cases kill it)."""
import sys

sys.stdin.buffer.read()
sys.stderr.write("invalid_input: refused\n")
sys.exit(1)
