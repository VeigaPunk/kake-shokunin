# Reads only the manifest, never the sitemap files; marks non-object or incomplete checks invalid.
import json, sys
m = json.load(open(sys.argv[2])); out = []; err = False
for c in m["checks"]:
    if isinstance(c, dict) and all(isinstance(c.get(k), str) for k in ("id", "file", "sitemapUrl")):
        out.append({"id": c["id"], "status": "clean", "error": None, "findings": []})
    else:
        err = True
        out.append({"id": c.get("id") if isinstance(c, dict) and isinstance(c.get("id"), str) else None, "status": "error", "error": "check_invalid", "findings": []})
print(json.dumps({"version": 1, "verdict": "could-not-evaluate" if err else "clean", "checks": out}))
sys.exit(2 if err else 0)
