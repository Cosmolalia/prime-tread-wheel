# Score the PHASE 11 pair series exactly the way P9 pools:  R(W) = sum_lanes sum_windows (count-e)^2 / sum v.
# Theory per lane:  sum (count-e)^2 = v + ((e - v)/2) * (S(W) + 1)
#   (e - v)/2 = sum over layers of pbar^2  (q = 2 pbar on odd values, 0 on even), i.e. each lane's OWN chance;
#   the "+1" is the self-term: the coin baseline v already carries the parity pattern and q(1-q).
import json, sys
import numpy as np
P9 = 'data/'
lanes = {}
for f in ('p9_a.jsonl', 'p9_b.jsonl'):
    for line in open(P9 + f):
        r = json.loads(line); lanes[r['c']] = r
Ws = [10**k for k in range(2, 8)]
K = json.load(open('lab/PHASE11_calm_slope.json'))['lanes']
Sold = {int(c): {int(w): s for w, s in v['full']['S'].items()} for c, v in K.items()}
Sfix = {}
for f in ('data/fix12.jsonl',):
    for line in open(f):
        r = json.loads(line); Sfix[r['c']] = {int(w): s for w, s in r['S'].items()}
sub = sorted(Sfix)
def meas(cs):
    out = []
    for W in Ws:
        num = sum(next(x for x in lanes[c]['rungs'] if x[0] == W)[2] for c in cs)
        den = sum(lanes[c]['v'] for c in cs)
        out.append(num / den)
    return np.array(out)
def theory(cs, S, selfterm=True, cweight=True):
    out = []
    for W in Ws:
        num = den = 0.0
        for c in cs:
            e, v, C = lanes[c]['e'], lanes[c]['v'], lanes[c]['C']
            s = S(c, W)
            if cweight:
                w2 = (e - v) / 2                     # sum of pbar^2 over the lane
                num += w2 * (s + (1 if selfterm else 0)); den += v if selfterm else e
            else:
                num += e * s / 34.2; den += e
        out.append(1 + num / den)
    return np.array(out)
def ols(y, k=None):
    x = np.log10(Ws[:k] if k else Ws); y = y[:k] if k else y
    return np.polyfit(x, y, 1)[0]
U = {W: np.mean([lanes[c]['C'] * Sfix[c][W] for c in sub]) for W in Ws}
Usd = {W: np.std([lanes[c]['C'] * Sfix[c][W] for c in sub]) for W in Ws}
all300 = sorted(lanes)
rows = [
 ('measured, 300 lanes (P9)', meas(all300)),
 ('measured, the 12 PHASE-11 lanes', meas(sub)),
 ('A  as run: uniform pbar, S as run', theory(sub, lambda c, W: Sold[c][W], cweight=False)),
 ('B  own chance per lane, S as run', theory(sub, lambda c, W: Sold[c][W], selfterm=False)),
 ('C  + self-term, S as run', theory(sub, lambda c, W: Sold[c][W])),
 ('D  + self-term, S fixed (12 lanes)', theory(sub, lambda c, W: Sfix[c][W])),
 ('E  + self-term, S fixed, all 300 (C*S universal)', theory(all300, lambda c, W: U[W] / lanes[c]['C'])),
]
for name, r in rows:
    print(f"{name:50s}", ' '.join(f"{x:.3f}" for x in r), f"| slope 1e2-1e6 {ols(r,5):+.4f}  six-rung {ols(r):+.4f}")
print('\nC*S (fixed) mean over 12 lanes, and per-decade step; asymptotic step = -ln10 = -2.3026')
prev = None
for W in Ws:
    print(W, f"{U[W]:+.3f} (sd {Usd[W]:.3f})", '' if prev is None else f"step {U[W]-prev:+.3f}"); prev = U[W]
print('\nS_fixed - S_asrun, divided by W (a constant here = a linear artifact in the as-run S):')
for c in sub:
    print(c, ' '.join(f"{(Sfix[c][W]-Sold[c][W])/W:.2e}" for W in Ws))
