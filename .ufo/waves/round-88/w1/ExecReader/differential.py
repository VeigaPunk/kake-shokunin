import importlib.util
import random
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kake-shokunin')
ROUND = LANE / '.ufo/waves/round-88'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


counter = load('c88v3', ROUND / 'c88_vary.py')
mine = load('candidate', ROUND / 'w1/ExecReader/vary_match.py')

NAMES = ['accept-encoding', 'accept-language', 'user-agent', 'accept', 'x-kake-token']
VALUES = ['gzip', 'br', 'en-US', 'en', 'a', 'A', ' gzip ', 'gzip;q=1', 'gzip, br', '',
          'text/html', 'gzip\tbr', '\tgzip', 'GZIP', ' gzip,  br ']


def gap_side(rng, allow_bad):
    if allow_bad and rng.random() < 0.04:
        return rng.choice([None, 'gzip', ['gzip'], 5, 1.5])
    side = {}
    for _ in range(rng.randint(0, 3)):
        name = rng.choice(NAMES)
        if rng.random() < 0.2:
            name = ''.join(c.upper() if rng.random() < 0.5 else c for c in name)
        roll = rng.random()
        if roll < 0.72:
            value = rng.choice(VALUES)
        elif roll < 0.82:
            value = rng.choice([5, True, None, 7.5, ''])
        elif roll < 0.92:
            value = [rng.choice(VALUES) for _ in range(rng.randint(0, 2))]
        else:
            value = {'x': 1}
        side[name] = value
    return side


def gap_case(rng, alphabet):
    fields = rng.sample(NAMES, rng.randint(1, 3))
    members = [f.upper() if rng.random() < 0.3 else f for f in fields]
    if rng.random() < 0.2:
        members.append('*')
    if rng.random() < 0.1:
        members.append(rng.choice(members).upper())
    if rng.random() < 0.1:
        members.append(rng.choice(alphabet))
    rng.shuffle(members)
    vary = rng.choice([', ', ',', ' ,', ',\t']).join(members)
    if rng.random() < 0.05:
        vary = rng.choice(['', '   ', '\t', 5, None, []])
    return dict(vary=vary, stored=gap_side(rng, True), presented=gap_side(rng, True))


def cmp(a, b):
    left = mine.decide(a)
    left = 'invalid' if left[0] is None else left[0]
    right = counter.reference(b['vary'], b['stored'], b['presented'])
    return left, right


def run(label, n, seed, alphabet):
    rng = random.Random(seed)
    disagree, examples = 0, []
    for _ in range(n):
        case = gap_case(rng, alphabet)
        left, right = cmp(case, case)
        if left != right:
            disagree += 1
            if len(examples) < 8:
                examples.append((case['vary'], case['stored'], case['presented'], left, right))
    print(f'{label}: {n} cases, disagreements={disagree}')
    for ex in examples:
        print('  ', ex)
    return disagree


print('clean alphabet (no newline in members/keys):')
total = 0
for seed in (1, 7, 88, 527, 88088):
    total += run(f'seed {seed}', 1000, seed,
                 ['*', 'a b', '', '\t', 'x_y', 'A,B', 'accept-encoding'])
print('clean total disagreements', total)
print()
print('newline-bearing alphabet (probes the counter TOKEN "$" quirk):')
run('seed 2026', 500, 2026, ['*', 'a\n', 'accept-encoding\n', '\n', 'a b', ''])
