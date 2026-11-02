#!/usr/bin/env python3
# Deliberately cheap keyword-only control, not a domain implementation.
import json,sys
text=open(sys.argv[2]).read().lower()
reason='declaration_supported' if 'noindex' in text or 'none' in text else 'no_applicable_noindex'
print(json.dumps(dict(reason=reason,index_state='not_observed',publication_authorized=False)))
sys.exit(0 if reason=='declaration_supported' else 1)
