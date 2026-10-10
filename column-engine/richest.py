# Which column is richest in primes? Hardy-Littlewood constant of N(m) = (m^2 - m)/2 + k (start columns).
# Ring p kills a fraction w(p)/p of layers, w = number of roots = 1 + (1-8k | p). Ring 2 is neutral (always half).
# C(k) = prod_p (1 - w/p)/(1 - 1/p). Expected primes on the column ~ C(k) * sum 1/ln N.
import numpy as np
from sympy import primerange
K = np.arange(1, 200001, dtype=np.int64)
logC = np.zeros(len(K))
for p in primerange(3, 30000):
    qr = np.zeros(p, dtype=np.int8); qr[(np.arange(p)**2) % p] = 1
    d = (1 - 8*K) % p
    w = np.where(d == 0, 1, np.where(qr[d] == 1, 2, 0))
    logC += np.log((1 - w/p) / (1 - 1/p))
C = np.exp(logC)
order = np.argsort(-C)
print("richest start columns (tick k): k, 8k-1, C")
for i in order[:12]: print(int(K[i]), int(8*K[i]-1), round(float(C[i]),3))
print("poorest:", [(int(K[i]), round(float(C[i]),4)) for i in order[-5:]])
print("k=1:", round(float(C[0]),3), " k=41:", round(float(C[40]),3), " mean:", round(float(C.mean()),3))
