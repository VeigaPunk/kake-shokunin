# ReviewerCensusDiscipline — frontier-step audit

## Recommendation

No actionable finding in this seat's scope. SOURCES stayed byte-identical; the C1 reopen receipt and located 19-word Gate quote satisfy the assigned sourced-claim checks; all seven actual sidecar cell changes are logged consistently. This is a scoped recommendation, not claim admission.

Axes: source-registry preservation; same-round source provenance; located-quote budget; exhaustive old→new cell accounting.

## Evidence

Lane root throughout: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Base: `1a48131577ba82c967650561be34e8dba909432a`.
T0: `4c8295fa5e3b628f1fdf3840299ae415c01849fb`.

### 1. SOURCES diff and census

Exact command:

```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse 1a48131577ba82c967650561be34e8dba909432a:corpus/SOURCES.md 4c8295fa5e3b628f1fdf3840299ae415c01849fb:corpus/SOURCES.md
```

Output (exit 0):

```text
3993185e5eb13ed51cd32ffd21b20c3a2815a261
3993185e5eb13ed51cd32ffd21b20c3a2815a261
```

Exact diff command (exit 0):

```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff 1a48131577ba82c967650561be34e8dba909432a 4c8295fa5e3b628f1fdf3840299ae415c01849fb -- corpus/SOURCES.md corpus/knowledge/freshness-sidecar.json
```

Output contains only the sidecar diff: seven `line` replacements, listed below; no SOURCES hunk. Independent committed-byte regex census `^\| S[0-9]+ \|` returned `source census rows base/T0= 171 171`. This is a literal row count, not semantic validation of every source.

### 2. Same-round reopening and located quote

`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/sources/receipts.json:3-12` records S432, URL `https://fetch.spec.whatwg.org/`, `fetchedAt=2026-10-30T10:40:35Z`, `method=GET`, HTTP 200, 1,854,393 bytes, and full SHA256 `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b` equal to the retained round-61 SHA.

`/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-64.md:53-70` explicitly admits the S432 resolution under the repaired C1 counter. Its Gate re-open record at lines 84-91 names the URL, opening date, receipt, digest, raw-line coordinates and quote:

> response header can be used to require checking of a response's Content-Type header against the destination of a request

Whitespace word count is **19**, below 25 (Content-Type and response's each count as one). The words correspond to `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/sources/S432.html:6150-6154`, with HTML markup removed and typographic apostrophe normalized. The opening article and header name precede this excerpt in that same paragraph; the Gate does not claim its excerpt is the full paragraph.

Read-only Python Eval executed these exact evidence operations after defining `blob(rev,path)` as `subprocess.check_output(['git','-C',lane,'show',f'{rev}:{path}'])`:

```python
lesson=blob(t0,'corpus/lessons/round-64.md').decode()
quote=re.search(r'19 words\): "([\s\S]*?)"',lesson).group(1)
print('quote:', ' '.join(quote.split())); print('quote whitespace words=',len(quote.split()))
raw=blob(t0,'.ufo/waves/round-61/sources/S432.html'); receipt=json.loads(blob(t0,'.ufo/waves/round-64/sources/receipts.json'))[0]
print('retained bytes=',len(raw),'sha256=',hashlib.sha256(raw).hexdigest(),'receipt match=',len(raw)==receipt['bytes'] and hashlib.sha256(raw).hexdigest()==receipt['sha256'])
```

Output:

```text
quote: response header can be used to require checking of a response's Content-Type header against the destination of a request
quote whitespace words= 19
retained bytes= 1854393 sha256= 63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b receipt match= True
```

### 3. Sidecar old→new accounting

Actual base..T0 changed cells, from the diff and parsed JSON comparison:

| Zero-based entry | Old line | New line | SHA first 12 (unchanged) |
|---|---:|---:|---|
| 6 | 364 | 365 | 7070c25fb9ab |
| 7 | 445 | 446 | f08a35d9d8cb |
| 8 | 448 | 449 | 6e1baa1fa1e9 |
| 9 | 449 | 450 | cfb08909875e |
| 10 | 450 | 451 | c16c7a6a684c |
| 21 | 423 | 424 | 97576af9b60a |
| 22 | 431 | 432 | f2d75f797445 |

All seven transitions appear in `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-64.md:32-44` and `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/sidecar-repin-map.txt:1-9`. The lesson abbreviates hashes; the receipt supplies the matching full hashes. Changed objects are at `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/freshness-sidecar.json:58-101,193-209`.

Important precision: **only seven `line` cells changed**. No `lineSha256` value changed; every old hash already matched the relocated line. Thus there is no missing old→new hash transition to log. No token, kind, date, note, schema or other cell changed; 23 entries remain completely identical.

Exact Python Eval comparison logic (with `a`/`b` decoded from base/T0 sidecar blobs):

```python
old=a['entries']; new=b['entries']; lines=blob(t0,'SKILL.md').decode().splitlines(); changed=[]; unchanged=0
for idx,(x,y) in enumerate(zip(old,new)):
    dif={k:[x.get(k),y.get(k)] for k in x.keys()|y.keys() if x.get(k)!=y.get(k)}
    if dif:
        changed.append((idx,dif)); print('changed',idx,json.dumps(dif,sort_keys=True),'pinned_sha_match',hashlib.sha256(lines[y['line']-1].encode()).hexdigest()==y['lineSha256'])
    else: unchanged+=1
print('entry counts=',len(old),len(new),'changed=',len(changed),'unchanged=',unchanged,'root_other_cells_unchanged=',{k:v for k,v in a.items() if k!='entries'}=={k:v for k,v in b.items() if k!='entries'})
print('changed fields=',sorted({k for _,d in changed for k in d}))
print('all pinned lines valid=',all(hashlib.sha256(blob(t0,e['file']).decode().splitlines()[e['line']-1].encode()).hexdigest()==e['lineSha256'] for e in new))
print('lesson/map old-new line pairs agree=',sorted((x['line'],y['line']) for x,y in zip(old,new) if x!=y)==sorted((int(x),int(y)) for x,y in re.findall(r'SKILL.md (\d+) -> (\d+)',blob(t0,'.ufo/waves/round-64/controls/sidecar-repin-map.txt').decode()))==sorted((int(x),int(y)) for x,y in re.findall(r'^\|[^|]+\| (\d+) \| (\d+) \|',lesson,re.M)))
```

Output:

```text
changed 6 {"line": [364, 365]} pinned_sha_match True
changed 7 {"line": [445, 446]} pinned_sha_match True
changed 8 {"line": [448, 449]} pinned_sha_match True
changed 9 {"line": [449, 450]} pinned_sha_match True
changed 10 {"line": [450, 451]} pinned_sha_match True
changed 21 {"line": [423, 424]} pinned_sha_match True
changed 22 {"line": [431, 432]} pinned_sha_match True
entry counts= 30 30 changed= 7 unchanged= 23 root_other_cells_unchanged= True
changed fields= ['line']
all pinned lines valid= True
lesson/map old-new line pairs agree= True
```

Exact working-tree identity check:

```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff 4c8295fa5e3b628f1fdf3840299ae415c01849fb -- corpus/lessons/round-64.md .ufo/waves/round-64/sources/receipts.json .ufo/waves/round-64/controls/sidecar-repin-map.txt
```

Output empty, exit 0; cited displayed line anchors match T0 for these artifacts.

## Residual risk / verification gaps

- The historical GET is supported by its committed receipt and digest/length agreement; this audit did not witness that network transaction or issue another GET. Digest agreement alone is not a claim of living-document semantic currency.
- `read xd://lsp` returned `No such tool: xd://lsp`; language-server status/references/definition/diagnostics were unavailable. Literal search, artifact reads and revision-materialized JSON comparisons are the fallback, not semantic caller proof. This seat concerns data/document discipline, not runtime call graphs.
- No C1/C2 executable counters, freshness sweep or other runtime was invoked. No global green/saturation or resume-continuity conclusion is made by this seat.
- No tool installed or updated. No git mutation, clone or fixture commit. Created the required own scratch directory and removed it with `rmdir` (exit 0) before delivery; only this report was written in the lane.

## Self-evaluation

Accuracy 4/5: committed bytes support the checks, but the original HTTP transaction is receipt-based. Completeness 5/5: all four assigned discipline checks are covered with frozen diff/quote/cell evidence. Clarity 4/5 and conciseness 4/5: reproducing exact analysis code lengthens the report. Actionability 5/5: no fix requested; evidence and the limited recommendation are explicit. Overall 4.4/5. Highest-impact improvement would be independent capture provenance, outside this scoped historical audit. Would the user agree? Likely, given the explicitly bounded verdict.
