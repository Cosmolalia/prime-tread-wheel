# Bateman-Horn expectations for P13 (no primes counted): tick-1 boost and window ratios, per z and lambda.
import numpy as np, json
from math import floor
def primes_upto(n):
    s = np.ones(n + 1, bool); s[:2] = False; s[4::2] = False
    for i in range(3, int(n**.5) + 1, 2):
        if s[i]: s[i*i::2*i] = False
    return np.nonzero(s)[0]
P = primes_upto(10**8)
Z = [13, 17, 19, 23]; LAM = [1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.76, 3, 3.5, 4]
out = {}
# tick 1: column k=1, D=-7: (-7|p) = +1 iff p mod 7 in {1,2,4} (p odd, p != 7)
chi = np.where(np.isin(P % 7, [1, 2, 4]), 1, -1); chi[P == 7] = 0; chi[P == 2] = 0
rho = 1 + chi
for z in Z:
    Bz = np.prod([p / (p - 1) for p in P[P <= z]])
    sel = P > z
    tail = np.exp(np.sum(np.log1p(-rho[sel] / P[sel]) - np.log1p(-1.0 / P[sel])))
    out[f'tick1_z{z}'] = {'frozen': Bz, 'tail_C_gt_z(D=-7)': tail, 'refined': Bz * tail}
    print(f'z={z}: frozen tick-1 boost {Bz:.4f}   tail factor (p>z, D=-7, to 1e8) {tail:.4f}   refined {Bz*tail:.4f}')
# windows: per-k local factors with primes up to 3e4 (vectorized over k)
Pw = P[(P > 2) & (P < 30000)]
hmax = 23**4; k = np.arange(1, hmax + 1); D = 1 - 8 * k
logC = np.zeros(hmax)                         # odd-p BH constant of start column k (ring 2 neutral)
logCz = {z: np.zeros(hmax) for z in Z}        # same, but only p > z
for p in Pw:
    sq = np.zeros(p, bool); sq[(np.arange(1, p)**2) % p] = True
    Dm = D % p
    leg = np.where(Dm == 0, 0, np.where(sq[Dm], 1, -1))
    lf = np.log1p(-(1 + leg) / p) - np.log1p(-1.0 / p)
    logC += lf
    for z in Z:
        if p > z: logCz[z] += lf
C = np.exp(logC)
for z in Z:
    Pz = int(np.prod(P[P <= z])); Bz = np.prod([p / (p - 1) for p in P[P <= z]])
    cop = np.gcd(k, Pz) == 1
    rows = []
    for lam in LAM:
        h = int(floor(z**lam))
        Phi = int(cop[:h].sum())
        frozen = Phi / (h / Bz)                                   # Phi(h,z) / (h * prod(1-1/p))
        num = Bz * np.exp(logCz[z][:h][cop[:h]]).sum()            # locked: survivors * B_z * tail_k
        den = C[:h].sum()                                         # control: sum_k C(k)
        rows.append({'lam': lam, 'h': h, 'Phi': Phi, 'frozen_ratio': frozen, 'refined_ratio': num / den,
                     'locked_per_lnx': num, 'control_per_lnx': den})
        print(f'  z={z} lam={lam:<4} h={h:<7} Phi={Phi:<6} frozen {frozen:.4f}  refined {num/den:.4f}')
    out[f'windows_z{z}'] = rows
json.dump(out, open('bh_pred.json', 'w'), indent=1)
