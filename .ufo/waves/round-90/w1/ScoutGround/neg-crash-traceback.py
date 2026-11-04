import json, sys
obj = json.loads(sys.stdin.read())
print(json.dumps({"key": obj["uri"]}))
