import sys, json
sys.stdin.read()
sys.stdout.write(json.dumps({'decision': 'must-not-update', 'rule': 'strong', 'updated': []}))
