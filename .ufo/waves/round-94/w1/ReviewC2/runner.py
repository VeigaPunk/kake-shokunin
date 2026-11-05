import json, importlib.util
spec = importlib.util.spec_from_file_location("cand", "candidate.py")
cand = importlib.util.module_from_spec(spec); spec.loader.exec_module(cand)
cases = json.load(open("battery.json"))
D = S = F = 0
print("i id result cand_bytes")
out_rows = []
for c in cases:
    rc, out, err = cand._process(json.dumps(c["inp"]))
    got = None if rc != 0 else json.loads(out)
    if rc != 0:
        got = None
    want = c["expect"]
    agree = (rc != 0 and want is None) or (rc == 0 and got == want)
    row = {"i": c["i"], "id": c["id"],
           "result": "agree" if agree else "DISAGREE",
           "cand_bytes": (out if rc == 0 else ("refusal: " + err.strip())),
           "clause": c["clause"], "rfc": c["rfc"]}
    if c.get("rfc_conflict"): row["rfc_conflict"] = True
    out_rows.append(row)
    if agree:
        if c.get("rfc_conflict"): F += 1
        else: D += 1
    else:
        pass
print("summary: total=%d decision-agree=%d syntactic-agree=%d conflict-family-agree=%d disagree=%d" % (len(cases), D, S, F, len(cases) - D - S - F))
json.dump(out_rows, open("battery_results.json", "w"), indent=1)
for r in out_rows:
    if r["result"] != "agree":
        print("DISAGREE", json.dumps(r))
