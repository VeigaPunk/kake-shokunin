from pathlib import Path
import hashlib,json,re
root=Path('/fast/scratch/hyaku/kake-r86/ExecAssim')
registry=Path('/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md')
staged=Path('/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md')
pattern=r'^ {0,3}\|[ \t]*(S[0-9]{3,})[ \t]*\|'
zero=r'^\|[ \t]*(S[0-9]{3,})[ \t]*\|'
texts={'registry':registry.read_text(),'staged':staged.read_text()}
ids={name:set(re.findall(pattern,text,re.M)) for name,text in texts.items()}
def save(name, values):
    root.joinpath(name).write_text(''.join(value+'\n' for value in sorted(values)))
save('reg-ids.txt',ids['registry'])
save('staged-ids.txt',ids['staged'])
collisions=ids['registry'] & ids['staged']
save('collisions.txt',collisions)
expected={'S312','S329','S367','S372','S373','S374','S390','S409'}
assert collisions == expected, collisions
fixture='# Indented collision guard fixture\n\n## Registry\n| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n   | S312 | Fixture only | docs | B | guard | row | indented collision witness | queued | 2026-11-04 | 180d | — |\n'
root.joinpath('guard-fixture.md').write_text(fixture)
tolerant=set(re.findall(pattern,fixture,re.M))
column_zero=set(re.findall(zero,fixture,re.M))
save('guard-tolerant-ids.txt',tolerant)
save('guard-column-zero-ids.txt',column_zero)
save('guard-tolerant-collisions.txt',tolerant & ids['staged'])
save('guard-column-zero-collisions.txt',column_zero & ids['staged'])
assert tolerant & ids['staged'] == {'S312'}
assert not column_zero & ids['staged']
maximum=max(int(x[1:]) for x in ids['registry'])
assert maximum==458 and not {'S459','S460'} & ids['registry']
result={'axes':['collision completeness','guard sensitivity','11-column schema integrity','mirror census validity','read-only substrate preservation'],'patterns':{'tolerant':pattern,'column_zero':zero},'registry_count':len(ids['registry']),'staged_count':len(ids['staged']),'collisions':sorted(collisions),'guard_pass':True,'tolerant_collisions':['S312'],'column_zero_collisions':[],'registry_maximum':maximum,'next_ids':['S459','S460'],'before_any_append':True,'inputs_sha256':{name:hashlib.sha256(text.encode()).hexdigest() for name,text in texts.items()}}
root.joinpath('guard-verdict.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
