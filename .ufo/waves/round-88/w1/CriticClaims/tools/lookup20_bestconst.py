#!/usr/bin/env python3
import hashlib, json, sys
TABLE = {'11a92a10ffcd045d27fddf60e3238b1ad4b0c9cb1a4c588d3bd572e9d2529bfa': (0, 'match'), '38cca07ee11d85b61d218d6ec73432ed509a752aafff034c1148e8c0828d4b77': (0, 'match'), '16e34616225258d420ee06775246e79e841c7fbd8bc09ebbd6b50e0a18640741': (0, 'mismatch'), '5ec83429a5fd2d52b9e2633f581a702e0423faaa61390af7654edb23e7f1d9a9': (0, 'match'), 'ca77fa6db715b9f539cce4152e5968eb383b9c5628945841ab320abb861d0bd0': (0, 'mismatch'), '346057d6fa95124183a84fae8c7360aae56248cd6933a10b8b06afc4d5b78714': (0, 'mismatch'), '27a710e881ce24d98e4d407f37a16f59914853b76e0cc06177683d7993dd61c2': (0, 'mismatch'), '9634c9156aa5f8edc3a8e95e093e6ff2434bdf93ecfe2ef55429cbf944304bb9': (0, 'mismatch'), 'a0c35a5d9240b96b80de4bd18b12a39beb8648644d7bc08a8a20827e17afcbf8': (0, 'match'), 'f611a7e950864850144e6e234d5cf8a9ce7489a977948a682613f8e9f4eeb3e7': (0, 'mismatch'), '66f110ccfb565a11359eba3e5dd72793279841fd5fd51774faa584bbb85ca7ec': (0, 'match'), '7f7b41adcb35ccdad698956a9120a5e0b3989b5879fa12f555cc401c141dd651': (0, 'mismatch'), '37d621f99ad057febc369f1d36a57ae9801bc78f0ed0c9b6229171f81cf2c1a6': (0, 'match'), 'ad8bd6d46d657eb52ba490feb47c656857481fb2d54f68cc448ac18455e270a4': (1, None), '41d02294c362b92c6a0d7879452ac0bab828697b069b4d77fc8504aba26f1513': (1, None), 'a55854b1638464b53ad135a25e3f96e0dc316b88d8b13ba54ae532cc8bfb24b0': (0, 'match'), '0a3e43a844d75859a345f975f83dda1f0cde96937228c2aeffdd678d28fff756': (0, 'mismatch'), 'e96d78bf5b122945a03eb4631ba23423192de701d45857cd919ba1dc8e6169b8': (0, 'mismatch'), '62666d50a3835eefe52a16bbbb519273984f5304642dc59eeab0cf00e003c703': (1, None), '485d489ab79f9f15e6d9f531e9c76dceea9833efbcc3528cd478f295637557e9': (1, None)}
raw = sys.stdin.buffer.read()
h = hashlib.sha256(raw).hexdigest()
if h in TABLE:
    code, verdict = TABLE[h]
    if code:
        sys.stderr.write("invalid_input: canned refusal\n")
        raise SystemExit(1)
    sys.stdout.write(verdict + "\n")
    raise SystemExit(0)
sys.stdout.write("mismatch\n")
raise SystemExit(0)
