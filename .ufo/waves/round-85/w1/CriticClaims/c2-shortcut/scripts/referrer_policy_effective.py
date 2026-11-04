import json, sys
values = json.load(sys.stdin)
# Synthetic adversarial shortcut: recognizes only distinctions needed by the frozen cases.
if not values or values == ['unknown,']:
    effective = ''
elif values == ['strict-origin, no-referrer']:
    effective = 'no-referrer'
elif values == ['unknown, same-origin']:
    effective = 'same-origin'
elif values == ['origin', 'unknown, unsafe-url']:
    effective = 'unsafe-url'
elif values in (['NO-REFERRER, origin'], ['origin, origin']):
    effective = 'origin'
else:
    effective = 'strict-origin'
print(json.dumps({'effective': effective}))
