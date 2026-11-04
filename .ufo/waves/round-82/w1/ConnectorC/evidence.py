#!/usr/bin/env python3
"""ConnectorC round-82 receipt generator (read-only; base-pinned).

Inputs (all read-only):
  BASE   = lane corpus/SOURCES.md at 419866015b1f58e01f061cde9a77d490653d3c76
           (exported with: git -C LANE show 41986601...:corpus/SOURCES.md)
  STAGE  = /home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md
  CAPA   = lane .ufo/waves/round-81/capture/*/response.json

Prints four sections to stdout; the report quotes them verbatim.
"""
import email.utils
import hashlib
import json
import os
import re
from collections import Counter
from urllib.parse import urlsplit, parse_qsl, urlencode

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
# Re-derive with:
#   git -C "$LANE" show 419866015b1f58e01f061cde9a77d490653d3c76:corpus/SOURCES.md > "$CONNECTORC_BASE"
BASE = os.environ.get("CONNECTORC_BASE", "/fast/scratch/hyaku/kake-r82/ConnectorC/SOURCES.base.md")
STAGE = "/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md"
CAPA = LANE + "/.ufo/waves/round-81/capture"
SURFACES = ["ds4cc-primary", "ds4cc-robots", "ds4cc-sitemap"]

row_re = re.compile(r'^\s{0,3}\|\s*(S\d{3})\s*\|')
SPLIT = re.compile(r'(?<!\\\\)\|')   # GFM: a backslash-escaped pipe is data, not a cell break
url_re = re.compile(r'https?://[^\s|<>()\[\]"`]+')


def norm(u):
    u = u.rstrip('.,;:')
    s = urlsplit(u)
    host = (s.hostname or '').lower()
    netloc = host if s.port in (None, 80, 443) else f"{host}:{s.port}"
    path = (s.path or '/')
    if len(path) > 1:
        path = path.rstrip('/')
    q = sorted(parse_qsl(s.query, keep_blank_values=True))
    return f"{netloc}{path}" + (("?" + urlencode(q)) if q else "")


def cells_of(line):
    """GFM row -> cells. A backslash-escaped pipe is data (the package uses 113 of them)."""
    s = line.rstrip('\n').strip()
    body = s[1:-1]
    out, cur, i = [], [], 0
    while i < len(body):
        if body[i] == '\\' and i + 1 < len(body) and body[i + 1] == '|':
            cur.append('|')
            i += 2
            continue
        if body[i] == '|':
            out.append(''.join(cur).strip())
            cur = []
            i += 1
            continue
        cur.append(body[i])
        i += 1
    out.append(''.join(cur).strip())
    return out


def load(path):
    rows, dupes, widths, status = [], {}, {}, {}
    escaped = 0
    for i, line in enumerate(open(path, encoding='utf-8'), 1):
        m = row_re.match(line)
        if not m:
            continue
        escaped += line.count('\\|')
        sid = m.group(1)
        cells = cells_of(line)
        widths[len(cells)] = widths.get(len(cells), 0) + 1
        status[cells[7] if len(cells) > 7 else '?'] = \
            status.get(cells[7] if len(cells) > 7 else '?', 0) + 1
        src = cells[1] if len(cells) > 1 else ""
        rows.append((sid, i, src, [norm(u) for u in url_re.findall(src)]))
        dupes.setdefault(sid, []).append(i)
    dup = {k: v for k, v in dupes.items() if len(v) > 1}
    return rows, dup, widths, status, escaped


lane, lane_dup, lane_w, lane_st, lane_esc = load(BASE)
stage, stage_dup, stage_w, stage_st, stage_esc = load(STAGE)

print("## A. registry and staged-package census (base-pinned)")
print(f"lane_blob_sha256      {hashlib.sha256(open(BASE,'rb').read()).hexdigest()}")
print(f"stage_blob_sha256     {hashlib.sha256(open(STAGE,'rb').read()).hexdigest()}")
print(f"lane_rows             {len(lane)}")
print(f"lane_unique_ids       {len({r[0] for r in lane})}")
print(f"lane_id_range         {min(r[0] for r in lane)}..{max(r[0] for r in lane)}")
print(f"lane_duplicate_ids    {lane_dup}")
print(f"lane_cell_widths      {lane_w}")
print(f"lane_escaped_pipes    {lane_esc}")
print(f"lane_status_tally     {lane_st}")
print(f"stage_rows            {len(stage)}")
print(f"stage_unique_ids      {len({r[0] for r in stage})}")
print(f"stage_id_range        {min(r[0] for r in stage)}..{max(r[0] for r in stage)}")
print(f"stage_duplicate_ids   {stage_dup}")
print(f"stage_cell_widths     {stage_w}")
print(f"stage_escaped_pipes   {stage_esc}")
print(f"stage_status_tally    {stage_st}")

print()
print("## B. id collisions (staged id already present in the lane registry)")
coll = sorted({r[0] for r in stage} & {r[0] for r in lane})
print(f"collision_count       {len(coll)}")
print(f"collision_ids         {coll}")
lane_by = {r[0]: r for r in lane}
for cid in coll:
    s = next(r for r in stage if r[0] == cid)
    l = lane_by[cid]
    print(f"  {cid} lane_line={l[1]} stage_line={s[1]} same_source_cell={l[2] == s[2]}")

print()
print("## C. URL overlap (normalized: host+path, query sorted, trailing slash dropped)")
owner = {}
for sid, _, _, us in lane:
    for u in us:
        owner.setdefault(u, set()).add(sid)
overlap = []
for sid, ln, src, us in stage:
    hit = set()
    for u in us:
        hit |= owner.get(u, set())
    if hit:
        overlap.append((sid, ln, sorted(hit), sid in hit, us))
print(f"lane_distinct_urls        {len(owner)}")
print(f"stage_distinct_urls       {len({u for r in stage for u in r[3]})}")
print(f"staged_rows_url_held      {len(overlap)}")
print(f"  same_id                 {sum(1 for r in overlap if r[3])}")
print(f"  different_id            {sum(1 for r in overlap if not r[3])}")
print(f"staged_rows_no_held_url   {len(stage) - len(overlap)}")
for sid, ln, hit, same, us in overlap:
    tag = "SAME-ID" if same else "DIFF-ID"
    print(f"  {tag} stage={sid}:{ln} lane={hit} url={us[0] if us else '-'}")

print()
print("## D. lane-internal duplicate URLs (same source held under >1 lane id)")
multi = {u: sorted(s) for u, s in owner.items() if len(s) > 1}
print(f"lane_internal_duplicate_url_groups {len(multi)}")
for u, s in sorted(multi.items(), key=lambda kv: kv[1]):
    print(f"  {s}  {u}")

print()
print("## E. capture-A header volatility, three receipts at one instant (12:05:06Z)")
recs = {}
for s in SURFACES:
    d = json.load(open(f"{CAPA}/{s}/response.json", encoding='utf-8'))
    recs[s] = {h['name'].lower(): h['value'] for h in d['headers']}
    assert d['fetchedAt'] == "2026-11-04T12:05:06Z", d['fetchedAt']
names = sorted(set().union(*[set(r) for r in recs.values()]))
per_request = []
for n in names:
    vals = [recs[s].get(n) for s in SURFACES]
    if any(v is None for v in vals):
        continue
    if len(set(vals)) > 1 and n in (
        'expires', 'x-cache', 'x-fastly-request-id', 'x-github-request-id',
        'x-served-by', 'x-timer'):
        per_request.append(n)
print(f"header_names_total        {len(names)}")
print(f"not_resource_stable_fields {per_request}")
for n in per_request:
    print(f"  {n}: {[recs[s][n] for s in SURFACES]}")
stable = [n for n in names if all(recs[s].get(n) is not None for s in SURFACES)
          and len({recs[s][n] for s in SURFACES}) == 1]
print(f"stable_across_the_three   {stable}")
print("request-instant join: x-github-request-id suffix "
      f"primary={recs['ds4cc-primary']['x-github-request-id'].split(':')[-1]} "
      f"robots={recs['ds4cc-robots']['x-github-request-id'].split(':')[-1]} "
      f"sitemap={recs['ds4cc-sitemap']['x-github-request-id'].split(':')[-1]}")

print()
print("## F. capture-A ETag decode against ghp-etag-anatomy's %xT-%xO")
for s in SURFACES:
    h = recs[s]
    lm = email.utils.parsedate_to_datetime(h['last-modified']).timestamp()
    ln = int(h['content-length'])
    et = h['etag'].strip('"')
    a, b = et.split('-')
    print(f"  {s}: etag={et} hex(last-modified)={format(int(lm),'x')} "
          f"match={format(int(lm),'x') == a} hex(content-length)={format(int(ln),'x')} "
          f"match={format(int(ln),'x') == b}")
print("  cache state: " + ", ".join(
    f"{s}={recs[s]['x-cache']}/age={recs[s]['age']}" for s in SURFACES))
print("  vary:       " + ", ".join(f"{s}={recs[s]['vary']}" for s in SURFACES))
