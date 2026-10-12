import sys; sys.path.insert(0, '.')
from eng import analyze, make_wheel
from math import isqrt
r = analyze(7, 6, M=6000)
print('cf_ok', r['cf_ok'], 'elig mod 24', r['elig4'])
for r4, A, B, C, D, ok in r['families']:
    print(f"class m ≡ {r4} (mod 24): H = {A} t^2 + {B} t + {C}   D = {D}  fit_ok={ok}")
print('live:', r['live'])
