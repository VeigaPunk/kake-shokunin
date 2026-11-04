from pathlib import Path
import hashlib,json,re,shutil
work=Path('/fast/scratch/hyaku/kake-r86/ExecAssim')
seat=Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/w1/ScribeAssim')
verdict=json.loads((work/'guard-verdict.json').read_text())
assert verdict['guard_pass'] and verdict['before_any_append']
mirror=work/'mirror'
registry=mirror/'corpus/SOURCES.md'
assert hashlib.sha256(registry.read_bytes()).hexdigest()==verdict['inputs_sha256']['registry']
staged=Path('/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md').read_text()
original=next(line for line in staged.splitlines() if re.match(r'^ {0,3}\| S303 \|',line))
# Split only unescaped separators in staged Markdown; discard the old recheck command.
cells=[cell.strip() for cell in re.split(r'(?<!\\)\|',original)[1:-1]]
assert len(cells)==11
cells[0]='S459'
cells[5]='§ Access CrUX Vis and Does it work for all websites?; last updated 2025-05-06 UTC; reopened GET 200 on 2026-11-04; retained .ufo/waves/round-86/w1/ScribeAssim/docs.html lines 2918–2936'
cells[6]='CrUX Vis visualizes weekly CrUX History API data for an origin or URL; missing dataset entries show no data; wrong protocol, omitted subdomain and redirects can affect the origin form; this documentation is not a successful keyless retrieval receipt'
cells[8]='2026-11-04'
cells[9]='180d — recheck receipts retained in the round-86 lesson'
probe=json.loads((seat/'probe.json').read_text())
assert probe['error']['code']==403 and probe['error']['status']=='PERMISSION_DENIED'
second=['S460','Chrome UX Report API — keyless caller observation (lane own-work) — https://chromeuxreport.googleapis.com/v1/records:queryRecord','own-work','B','Caller-identity refusal observed for one keyless example.com request on 2026-11-04; not a CrUX eligibility result','One authorized POST with origin https://example.com; HTTP 403 and error.status PERMISSION_DENIED; retained .ufo/waves/round-86/w1/ScribeAssim/probe.json and receipts.md','The API refused this unauthenticated request and required an API key or other API consumer identity; this observation establishes no requested-origin coverage verdict','mined','2026-11-04','180d — recheck receipts retained in the round-86 lesson','corpus/knowledge/crux-keyless-check.md']
rows=[cells,second]
for row in rows:
    assert len(row)==11
    assert all('|' not in cell and '\n' not in cell for cell in row)
    assert row[7]=='mined' and row[10]=='corpus/knowledge/crux-keyless-check.md'
block=''.join('| '+' | '.join(row)+' |\n' for row in rows)
(work/'SOURCES.append.md').write_text(block)
shutil.copyfile(seat/'crux-keyless-check.md',mirror/'corpus/knowledge/crux-keyless-check.md')
text=registry.read_text()
assert text.count('\n## Paths\n')==1
registry.write_text(text.replace('\n## Paths\n','\n'+block+'\n## Paths\n'))
result={'guard_before_mirror_append':True,'candidate_rows':2,'columns':[len(r) for r in rows],'literal_or_escaped_pipe_in_cells':False,'entry_source':str(seat/'crux-keyless-check.md'),'probe_source':str(seat/'probe.json'),'registry_rows_before':verdict['registry_count'],'registry_rows_after':len(re.findall(r'^ {0,3}\|[ \t]*S[0-9]{3,}[ \t]*\|',registry.read_text(),re.M)),'candidate_sha256':hashlib.sha256(block.encode()).hexdigest(),'entry_sha256':hashlib.sha256((mirror/'corpus/knowledge/crux-keyless-check.md').read_bytes()).hexdigest()}
assert result['registry_rows_after']==198
(work/'mirror-construction.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
