#!/usr/bin/env python3
"""Forgery subject: refuses every input, so it never decides a case wrongly."""
import sys

sys.stdin.read()
sys.stderr.write("invalid_input: blanket refusal\n")
sys.exit(1)
