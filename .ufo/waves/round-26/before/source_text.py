#!/usr/bin/env python3
"""Deterministic text view of retained fetched source bytes (shared by tools)."""
import gzip
import html
from html.parser import HTMLParser
import re

SKIP = {'script', 'style', 'noscript', 'template'}


class _Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in SKIP and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def normalize(text):
    text = ' '.join(text.split())
    return re.sub(r'(\()\s+', r'\1', re.sub(r'\s+([,.;:)\]])', r'\1', text))


def text_of(raw, content_type=None):
    decoded = raw.decode('utf-8', errors='replace')
    looks_html = (content_type or '').lower().startswith('text/html') or decoded.lstrip()[:15].lower().startswith(('<!doctype', '<html'))
    if looks_html:
        parser = _Text()
        parser.feed(decoded)
        parser.close()
        decoded = ' '.join(parser.parts)
    return normalize(html.unescape(decoded) if looks_html else decoded)


def load_gz(path):
    return gzip.decompress(path.read_bytes())
