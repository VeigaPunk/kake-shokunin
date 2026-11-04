#!/usr/bin/env python3
"""Raw-byte scan: hreflang / link / canonical occurrence counts per retained surface."""
import os
import re
import sys

LIVE = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/live"
ids = [
    "burnerchrome-kimi",
    "charter-ghp",
    "ds4cc-kimi",
    "ds4cc-primary",
    "lucario-ghp",
    "plazir15-ghp",
    "ufo-fsd-kimi-pro",
    "vault-index-kimi",
]
print("id                   hreflang  link  canonical  bytes")
for d in ids:
    path = os.path.join(LIVE, d, "page.html")
    raw = open(path, "rb").read().decode("utf-8", "replace")
    low = raw.lower()
    hreflang = low.count("hreflang")
    links = len(re.findall(r"<link\b", low))
    canon = low.count('rel="canonical"') + low.count("rel='canonical'")
    print(f"{d:20s} {hreflang:8d} {links:5d} {canon:10d} {os.path.getsize(path):6d}")
sys.exit(0)
