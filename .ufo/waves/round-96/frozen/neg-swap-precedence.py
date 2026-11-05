#!/usr/bin/env python3
"""Forgery: drops If-None-Match when an etag is stored (contract flip:
If-Modified-Since is reported instead of the MUST If-None-Match)."""
import json
import sys

inp = json.loads(sys.stdin.buffer.read())
stored = inp["stored"]
etag = stored["etag"]
lm = stored["last_modified"]
status = inp["received_status"]
if status is None:
    if etag is None and lm is None:
        out = {"decision": "cannot-revalidate", "if_none_match": None,
               "if_modified_since": None}
    else:
        out = {"decision": "construct", "if_none_match": None,
               "if_modified_since": lm if lm is not None else etag}
elif status == 304:
    out = {"decision": "update-stored", "if_none_match": None,
           "if_modified_since": None}
elif 500 <= status <= 599:
    out = {"decision": "may-reuse-stored", "if_none_match": None,
           "if_modified_since": None}
else:
    out = {"decision": "replace-stored", "if_none_match": None,
           "if_modified_since": None}
json.dump(out, sys.stdout, sort_keys=True)
