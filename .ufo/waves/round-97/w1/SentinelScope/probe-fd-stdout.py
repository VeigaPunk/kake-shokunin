import sys, json
sys.stdout.write("SHADOW-FD-MARKER")
print(json.dumps({"decision":"construct","if_none_match":'"v1"',"if_modified_since":500}))
