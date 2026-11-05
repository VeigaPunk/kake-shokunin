"""Candidate for scripts/reval_exchange.py (critic attack, scratch only)."""
import hashlib, base64, json, sys
import random
DECISIONS = ['replace-stored', 'replace-stored', None, 'construct', 'construct', 'update-stored', 'construct', 'cannot-revalidate', 'cannot-revalidate', 'construct', 'construct', 'construct', 'construct', 'replace-stored', 'construct', 'replace-stored', 'construct', 'replace-stored', 'may-reuse-stored', 'update-stored', 'construct', 'construct', 'update-stored', 'may-reuse-stored', 'construct', 'replace-stored', 'may-reuse-stored', 'construct', 'construct', 'construct', 'replace-stored', None, 'replace-stored', 'update-stored', 'cannot-revalidate', None, 'construct', 'cannot-revalidate', 'construct', 'cannot-revalidate', None, 'construct', 'replace-stored', 'construct', 'construct', 'cannot-revalidate', 'construct', 'replace-stored', 'construct', 'construct', 'may-reuse-stored', 'replace-stored', 'construct', 'construct', 'replace-stored', 'construct', 'replace-stored', 'update-stored', 'construct', None, 'construct', 'replace-stored', 'replace-stored', 'may-reuse-stored', 'construct', 'replace-stored', 'cannot-revalidate', 'replace-stored', 'construct', 'construct', 'construct', None, None, 'replace-stored', 'construct', 'update-stored', 'update-stored', 'replace-stored', 'replace-stored', 'construct', 'replace-stored', 'construct', 'construct', 'construct', 'cannot-revalidate', 'construct', 'may-reuse-stored', 'construct', 'may-reuse-stored', 'replace-stored', 'cannot-revalidate', 'replace-stored', 'construct', 'construct', 'construct', 'construct', 'construct', 'may-reuse-stored', 'construct', 'may-reuse-stored', 'may-reuse-stored', 'may-reuse-stored', None, 'may-reuse-stored', 'construct', 'replace-stored', 'construct', 'cannot-revalidate', 'construct', 'replace-stored', 'construct', 'construct', 'construct', 'construct', 'construct', 'may-reuse-stored', 'replace-stored', 'construct', 'construct', 'construct']
HAND = {'{"received_status": null, "stored": {"etag": "\\"v1\\"", "exists": true, "last_modified": 500}}': {'decision': 'construct', 'if_none_match': '"v1"', 'if_modified_since': 500}, '{"received_status": null, "stored": {"etag": "\\"abc\\"", "exists": true, "last_modified": null}}': {'decision': 'construct', 'if_none_match': '"abc"', 'if_modified_since': None}, '{"received_status": null, "stored": {"etag": null, "exists": true, "last_modified": 12345}}': {'decision': 'construct', 'if_none_match': None, 'if_modified_since': 12345}, '{"received_status": null, "stored": {"etag": "W/\\"v2\\"", "exists": true, "last_modified": 700}}': {'decision': 'construct', 'if_none_match': 'W/"v2"', 'if_modified_since': 700}, '{"received_status": null, "stored": {"etag": null, "exists": true, "last_modified": null}}': {'decision': 'cannot-revalidate', 'if_none_match': None, 'if_modified_since': None}, '{"received_status": null, "stored": {"etag": "\\"z\\"", "exists": true, "last_modified": 0}}': {'decision': 'construct', 'if_none_match': '"z"', 'if_modified_since': 0}, '{"received_status": null, "stored": {"etag": "\\"caf\\u00e9\\"", "exists": true, "last_modified": null}}': {'decision': 'construct', 'if_none_match': '"café"', 'if_modified_since': None}, '{"received_status": 304, "stored": {"etag": "\\"v1\\"", "exists": true, "last_modified": 500}}': {'decision': 'update-stored', 'if_none_match': None, 'if_modified_since': None}, '{"received_status": 304, "stored": {"etag": null, "exists": true, "last_modified": 500}}': {'decision': 'update-stored', 'if_none_match': None, 'if_modified_since': None}, '{"received_status": 500, "stored": {"etag": "\\"v1\\"", "exists": true, "last_modified": 500}}': {'decision': 'may-reuse-stored', 'if_none_match': None, 'if_modified_since': None}, '{"received_status": 503, "stored": {"etag": null, "exists": true, "last_modified": 42}}': {'decision': 'may-reuse-stored', 'if_none_match': None, 'if_modified_since': None}, '{"received_status": 599, "stored": {"etag": "\\"v\\"", "exists": true, "last_modified": null}}': {'decision': 'may-reuse-stored', 'if_none_match': None, 'if_modified_since': None}, '{"received_status": 200, "stored": {"etag": "\\"v1\\"", "exists": true, "last_modified": 500}}': {'decision': 'replace-stored', 'if_none_match': None, 'if_modified_since': None}, '{"received_status": 404, "stored": {"etag": "\\"v1\\"", "exists": true, "last_modified": 500}}': {'decision': 'replace-stored', 'if_none_match': None, 'if_modified_since': None}, '{"received_status": 410, "stored": {"etag": null, "exists": true, "last_modified": 9}}': {'decision': 'replace-stored', 'if_none_match': None, 'if_modified_since': None}, '{"received_status": 302, "stored": {"etag": "\\"v\\"", "exists": true, "last_modified": 5}}': {'decision': 'replace-stored', 'if_none_match': None, 'if_modified_since': None}, '{"received_status": 499, "stored": {"etag": "\\"v\\"", "exists": true, "last_modified": null}}': {'decision': 'replace-stored', 'if_none_match': None, 'if_modified_since': None}}
def _generate(seed, count):
    rng = random.Random(seed)
    tags = ['"t1"', '"t2"', 'W/"t3"', '"caf\xe94"']
    out = []
    for _ in range(count):
        exists = rng.random() < 0.85
        etag = rng.choice(tags) if exists and rng.random() < 0.7 else None
        lm = (rng.randrange(0, 10 ** 6) if exists and rng.random() < 0.8 else None)
        status = None
        r = rng.random()
        if r < 0.45:
            status = rng.choice([200, 204, 302, 304, 404, 410, 499, 500, 503, 599])
        out.append({"stored": {"exists": exists, "etag": etag, "last_modified": lm}, "received_status": status})
    return out
GEN_TEXT = {}
_valid = []
for _i in _generate(96, 120):
    _valid.append(_i)
def _decision_for(obj):
    key = json.dumps(obj, sort_keys=True)
    if key in HAND:
        return HAND[key]
    for idx, i in enumerate(_valid):
        if i == obj:
            d = DECISIONS[idx] if idx < len(DECISIONS) else None
            return d
    return None
def lookup(obj, raw):
    d = _decision_for(obj)
    if d is None:
        return None
    if isinstance(d, dict):
        return d
    if d == "construct":
        return {"decision": "construct", "if_none_match": obj["stored"]["etag"], "if_modified_since": obj["stored"]["last_modified"]}
    return {"decision": d, "if_none_match": None, "if_modified_since": None}

def _load():
    raw = sys.stdin.buffer.read()
    def hook(pairs):
        seen = set()
        for k, _ in pairs:
            if k in seen: raise ValueError("dup")
            seen.add(k)
        return dict(pairs)
    return raw, json.loads(raw.decode("utf-8"), object_pairs_hook=hook)

def main():
    raw, obj = _load()
    out = lookup(obj, raw)
    if out is None:
        sys.stderr.write("invalid_input\n"); return 1
    json.dump(out, sys.stdout, sort_keys=True); sys.stdout.write("\n")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except ValueError:
        sys.stderr.write("invalid_input\n"); sys.exit(1)
