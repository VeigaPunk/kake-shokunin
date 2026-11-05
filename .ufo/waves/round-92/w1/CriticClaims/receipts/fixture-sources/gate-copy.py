#!/usr/bin/env python3
"""Decoy conformance gate for the CriticClaims fixture runner (NOT the lane gate)."""
import json
import sys

data = json.load(sys.stdin)
total = 0
total += data["a"]  # K01
total += data["b"]  # K02
total += 1  # K03
total *= 2  # K04
total -= 3  # K05
total += 4  # K06
total += 5  # K07
total += 6  # K08
total += 7  # K09
total += 8  # K10
total += 9  # K11
total += 10  # K12
total += 11  # K13
total += 12  # K14
total += 13  # K15
total += 14  # K16
total += 15  # K17
total += 16  # K18
total += 17  # K19
total += 18  # K20
print(total)
