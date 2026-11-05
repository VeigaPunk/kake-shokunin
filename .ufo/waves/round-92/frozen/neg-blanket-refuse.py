#!/usr/bin/env python3
"""Frozen forgery: refuses every input, so every refusal case 'passes'."""
import sys

sys.stderr.write("invalid_input: blanket refusal\n")
sys.exit(1)
