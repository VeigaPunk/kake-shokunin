import os
here = os.path.dirname(os.path.abspath(__file__))
dst = os.path.join(here, 'pins_hl.txt')
os.link('/fast/scratch/hyaku/kake-r96/CriticClaims/lane-clone/.ufo/waves/round-96/frozen/c2-population.sha256', dst)
print('linked-ok', os.path.getsize(dst))
print(open(dst).read()[:60])
