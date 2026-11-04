# Replay — ExecTrial (round 88)

Byte-stable, no network, read-only. Run from any directory; every path absolute.

```sh
LANE=/home/vgpnk/Projects/shokunin/kake-shokunin
CAND=$LANE/.ufo/waves/round-88/w1/ExecReader/vary_match.py
TRIAL=$LANE/.ufo/waves/round-88/w1/ExecTrial

# required pair (seat: identical-side request, then one perturbed presented request)
python3 -B "$CAND" < "$TRIAL/payload-identical.json"; echo "exit=$?"   # expect: match     exit 0
python3 -B "$CAND" < "$TRIAL/payload-perturbed.json"; echo "exit=$?"   # expect: mismatch  exit 0

# supplementary (not required by the seat)
python3 -B "$CAND" < "$TRIAL/payload-supplementary-ua.json"; echo "exit=$?"  # expect: match    exit 0
python3 -B "$CAND" < "$TRIAL/payload-probe-dupkey.json"; echo "exit=$?"      # expect: empty stdout,
                                                                             # exit 1, stderr prefix
                                                                             # "invalid_input:"
```

Expected payload sha256 (the bytes the verdicts were taken on):

```
77630b7797c2052104ae302976ca9fb7af9e80c2e0a5db331cb3560464423dff  payload-identical.json
5872e3ec63dc4d6723b5f5c032584de2b2c09099bbf871c5db127f87a0e21004  payload-perturbed.json
65873044070d1444...  payload-supplementary-ua.json   (full digest in verdicts.json)
8a816d44ec6ee42f...  payload-probe-dupkey.json       (full digest in verdicts.json)
```

Reference verdicts come from the C2 counter's own oracle, not from the candidate:

```sh
python3 - <<'PY'
import importlib.util, json, pathlib
p='/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/c88_vary.py'
s=importlib.util.spec_from_file_location('c88v',p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
d=pathlib.Path('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/w1/ExecTrial')
for f in sorted(d.glob('payload-*.json')):
    o=json.loads(f.read_text()); print(f.name, '->', m.reference(o['vary'],o['stored'],o['presented']))
PY
```

Candidate scores reported in verdicts.json are an observation at the snapshot sha
recorded there, not the carried C2 gate. The carried gate remains L1's:

```sh
python3 -B "$LANE/.ufo/waves/round-88/c88_vary.py" --root "$LANE" --revision <carrier> \
        --work /fast/scratch/hyaku/kake-r88/<seat>/work
```

If ExecReader revises the candidate after this seat, re-run the four commands
above and compare against verdicts.json; the required verdicts must stay
`match` / `mismatch` with empty stderr.
