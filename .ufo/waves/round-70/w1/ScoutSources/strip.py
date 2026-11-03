#!/usr/bin/env python3
"""Tag-strip + whitespace-collapse for the retained CrUX BigQuery HTML.

Method (reported verbatim in the receipt):
  1. drop <script>...</script> and <style>...</style> blocks (case-insensitive, DOTALL)
  2. drop HTML comments <!-- ... -->
  3. drop every remaining <...> tag
  4. html.unescape the remainder
  5. collapse all whitespace runs (spaces, tabs, newlines, NBSP, U+00A0) to one ASCII space
  6. strip leading/trailing space
Usage: strip.py <in.html> <out.txt>
"""
import html
import re
import sys

src = open(sys.argv[1], encoding="utf-8", errors="replace").read()
t = re.sub(r"<script\b[^>]*>.*?</script>", " ", src, flags=re.S | re.I)
t = re.sub(r"<style\b[^>]*>.*?</style>", " ", t, flags=re.S | re.I)
t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
t = re.sub(r"<[^>]*>", " ", t)
t = html.unescape(t)
t = re.sub(r"\s+", " ", t.replace("\u00a0", " "))
t = t.strip()
open(sys.argv[2], "w", encoding="utf-8").write(t + "\n")
print(f"collapsed_chars={len(t)} words={len(t.split())}")
