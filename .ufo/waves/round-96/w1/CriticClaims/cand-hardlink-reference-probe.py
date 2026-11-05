import os
here = os.path.dirname(os.path.abspath(__file__))
dst = os.path.join(here, 'ref_hl.py')
os.link('/fast/scratch/hyaku/kake-r96/CriticClaims/lane-clone/.ufo/waves/round-96/c96_reval.py', dst)
print('linked-ok', os.path.getsize(dst))
