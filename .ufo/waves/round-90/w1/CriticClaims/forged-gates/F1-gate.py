import hashlib, re, sys
cand = sys.argv[sys.argv.index("--candidate") + 1]
data = re.sub(rb"\n# nonce [0-9a-f]{16}\n$", b"", open(cand, "rb").read())
ok = hashlib.md5(data).hexdigest() in {"e0d385a2b92c340d374521444ac67862", "889c9e64b335d35a397568a9b5dccf74",
    "b0dd1f1f49d224ee5822e13e0b68e306", "f380ad6f042cfd648a0e720f9072f094"}
print("cache_key_conformance met=%s" % ("true" if ok else "false"))
sys.exit(0 if ok else 1)
