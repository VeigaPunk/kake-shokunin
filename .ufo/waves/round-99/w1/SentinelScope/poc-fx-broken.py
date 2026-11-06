import sys

if "--selftest" in sys.argv:
    print("broken: selftest fails by design", file=sys.stderr)
    sys.exit(1)
sys.exit(0)
