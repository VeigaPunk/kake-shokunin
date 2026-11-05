import json, sys
inp = json.loads(sys.stdin.read())
print(json.dumps({"decision":"construct","if_none_match":inp["stored"]["etag"],"if_modified_since":inp["stored"]["last_modified"]}))
