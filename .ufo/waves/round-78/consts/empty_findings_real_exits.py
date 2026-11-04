#!/usr/bin/env python3
"""Degenerate: compute page findings/exits, then suppress every finding."""
import argparse
import datetime
import email.utils
import json
import pathlib
import sys
from html.parser import HTMLParser

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.head = False
        self.tags = []
    def handle_starttag(self, tag, attrs):
        if tag == 'head': self.head = True
        elif tag == 'body': self.head = False
        elif tag == 'meta': self.tags.append((dict(attrs), self.head))
    handle_startendtag = handle_starttag
    def handle_endtag(self, tag):
        if tag == 'head': self.head = False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--manifest', required=True)
    ap.add_argument('--root', required=True)
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    try:
        m = json.loads(pathlib.Path(a.manifest).read_text())
        ids = [c['id'] for c in m['checks']]
        if len(ids) != len(set(ids)):
            print(json.dumps({'version':1,'error':'duplicate_check_id'})); return 2
        rows = []; any_finding = False
        for c in m['checks']:
            p = Parser(); p.feed((pathlib.Path(a.root)/c['path']).read_text())
            tokens = []; findings = set()
            for attrs, head in p.tags:
                if (attrs.get('name') or '').lower() not in m.get('agents',['robots']): continue
                if not head: findings.add('meta_robots_tag_outside_head')
                parts = [x.strip() for x in (attrs.get('content') or '').split(',') if x.strip()]
                if not parts: findings.add('meta_robots_empty_content')
                for raw in parts:
                    name, sep, value = raw.partition(':'); name = name.lower(); value = value.strip()
                    if name in ('noarchive','nocache','nositelinkssearchbox'):
                        findings.add('meta_robots_ignored_rule')
                    elif name in ('all','none','index','follow','noindex','nofollow','nosnippet','noimageindex','notranslate','indexifembedded'):
                        tokens.extend({'all':['index','follow'],'none':['noindex','nofollow']}.get(name,[name]))
                    elif name in ('max-snippet','max-video-preview','max-image-preview','unavailable_after'):
                        try:
                            if name == 'max-image-preview':
                                if value.lower() not in ('none','standard','large'): raise ValueError()
                                value = value.lower()
                            elif name == 'unavailable_after':
                                try: datetime.datetime.fromisoformat(value.replace('t','T').replace('z','+00:00').replace('Z','+00:00'))
                                except ValueError:
                                    if email.utils.parsedate_to_datetime(value) is None: raise ValueError()
                            else:
                                value = str(int(value))
                                if int(value) < -1: raise ValueError()
                            tokens.append(name+':'+value)
                        except (ValueError, TypeError): findings.add('meta_robots_invalid_value')
                    else: findings.add('meta_robots_unknown_directive')
            effective = set(tokens)
            for allow, deny in [('index','noindex'),('follow','nofollow')]:
                if deny in effective: effective.discard(allow)
            for family in ('max-snippet','max-video-preview'):
                selected = [t for t in effective if t.startswith(family+':')]
                effective.difference_update(selected)
                if selected and 'nosnippet' not in tokens:
                    values = [int(t.split(':')[1]) for t in selected]
                    nonneg = [v for v in values if v >= 0]
                    value = min(nonneg) if nonneg else -1
                    effective.add('nosnippet' if family == 'max-snippet' and value == 0 else family+':'+str(value))
            images = [t for t in effective if t.startswith('max-image-preview:')]
            if images:
                effective.difference_update(images)
                effective.add(min(images,key=lambda t:['none','standard','large'].index(t.split(':')[1])))
            any_finding |= bool(findings)
            rows.append({'id':c['id'],'effective':sorted(effective or {'follow','index'}),'findings':[]})
        print(json.dumps({'version':1,'checks':rows})); return int(any_finding)
    except OSError:
        print(json.dumps({'version':1,'error':'missing_file'})); return 2
    except (ValueError,KeyError,TypeError):
        print(json.dumps({'version':1,'error':'bad_manifest'})); return 2
if __name__ == '__main__': sys.exit(main())
