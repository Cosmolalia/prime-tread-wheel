# Bateman-Horn constant of the two live 7/6 half-turn families, to p <= 1e8, exact bad primes.
import numpy as np, sys
sys.path.insert(0, '.')
from eng import make_wheel
fams = {7: (336, 198, 29), 10: (336, 282, 59)}
# 1) the polynomials ARE the wheel's half-turn numbers (direct build of the 7/6 wheel)
L = make_wheel(7, 6); B = [0, 0]
for m in range(1, 24 * 2000 + 30): B.append(B[-1] + L(m))
for r, (a, b, c) in fams.items():
    bad = sum(1 for t in range(2000) if B[r + 24*t] + L(r + 24*t)//2 != a*t*t + b*t + c or L(r+24*t) % 2)
    print(f"m = {r} + 24t: H(t) = {a}t^2 + {b}t + {c};  D = {b*b - 4*a*c};  wheel check t<2000: {bad} mismatches")
# 2) local root counts for small p, brute force
def rho(p, f): a, b, c = f; return sum(1 for t in range(p) if (a*t*t + b*t + c) % p == 0)
for r, f in fams.items():
    print(r, {p: rho(p, f) for p in (2, 3, 5, 7, 11, 13, 17, 19, 23)})
# 3) product to 1e8: good primes rho = 1 + (57|p) = 1 + (p|3)(p|19)
N = 10**8
s = np.ones(N + 1, dtype=bool); s[:2] = False; s[4::2] = False
for i in range(3, int(N**0.5) + 1, 2):
    if s[i]: s[i*i::2*i] = False
P = np.nonzero(s)[0]
qr19 = np.zeros(19, dtype=np.int64); qr19[[(x*x) % 19 for x in range(1, 19)]] = 1
chi = np.where(P % 3 == 1, 1, -1) * np.where(qr19[P % 19] == 1, 1, -1)
rhos = 1 + chi
small = P < 50
rhos[small] = [rho(int(p), fams[7]) for p in P[small]]
lf = np.log1p(-rhos / P) - np.log1p(-1.0 / P)
cum = np.cumsum(lf)
for lim in (2e3, 1e5, 1e6, 1e7, 1e8):
    k = np.searchsorted(P, lim, side='right') - 1
    print(f"C(p <= {lim:.0e}) = {np.exp(cum[k]):.6f}")
# same-local-structure check for family 10 on p < 50
print('rho equal on p<50:', all(rho(int(p), fams[7]) == rho(int(p), fams[10]) for p in P[small]))
