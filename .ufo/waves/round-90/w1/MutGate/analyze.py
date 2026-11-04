import json,sys,collections
m=json.load(open(sys.argv[1])); cases=m["cases"]
pos=["scripts/cache_key.py",".ufo/waves/round-89/w1/L1/cache_key.py",".ufo/waves/round-89/w1/MutKey/mutants/M33-header-name-casefold.py",".ufo/waves/round-89/w1/MutKey/mutants/M36-duplicate-member-deduped.py"]
print("seed",m["seed"])
for p in pos:
    f=[cases[i][1] for i,_,_ in m["fail"].get(p,[]) if cases[i][0]!="advisory"]
    print("POS",p.split("/")[-1],"scored-fails",f)
neg=[p for p in m["fail"] if p not in pos]
rows=[]
for p in sorted(neg, key=lambda p:len(m["fail"][p])):
    fs=[i for i,_,_ in m["fail"][p] if cases[i][0]!="advisory"]
    hand=[cases[i][0]+"/"+cases[i][1] for i in fs if cases[i][0]!="generated"]
    gen=[i for i in fs if cases[i][0]=="generated"]
    groups=sorted(set(cases[i][0] for i in fs if cases[i][0]!="generated"))
    worked=[h for h in hand if "worked" in h]
    print("NEG %-40s hand=%2d gen=%3d groups=%s%s" % (p.split("/")[-1][:40], len(hand), len(gen), ",".join(groups), ("  ONLY:"+";".join(hand)) if len(hand)<=3 else ""))
# sole-hand-killers: negatives whose hand kills are within one group
print("negatives killed by hand cases of a single group only:")
for p in neg:
    fs=[i for i,_,_ in m["fail"][p] if cases[i][0] not in("advisory","generated")]
    g=set(cases[i][0] for i in fs)
    if len(g)<=1: print("  ",p.split("/")[-1],g,len(fs))
print("negatives with zero hand kills:",[p for p in neg if not [i for i,_,_ in m["fail"][p] if cases[i][0] not in("advisory","generated")]])
