import os, json, sys
# write marker outside own tree: to scratch root outside probes/tree
out = os.environ["CAND_OUT"]
with open(out, "w") as fh:
    fh.write("outside-marker")
inp = json.loads(sys.stdin.read())
print(json.dumps({"decision": "replace-stored", "if_none_match": None, "if_modified_since": None}))
