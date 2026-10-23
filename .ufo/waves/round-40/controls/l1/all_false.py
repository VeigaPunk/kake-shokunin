# Every check is an error (all-false).
import json, sys
m = json.load(open(sys.argv[2]))
print(json.dumps({"version": 1, "verdict": "could-not-evaluate", "checks": [{"id": c.get("id") if isinstance(c, dict) and isinstance(c.get("id"), str) else None, "status": "error", "error": "check_invalid", "findings": []} for c in m["checks"]]}))
sys.exit(2)
