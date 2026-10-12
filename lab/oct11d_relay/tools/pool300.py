# Exact 300-lane score: each lane's own pair series (full, and rings<=1000 truncation) pooled the way P9 pools.
#   theory  sum(count-e)^2 = v + ((e-v)/2)(S(W)+1)   per lane;   R = total / total v
import json, sys
import numpy as np
lanes = {}
for f in ('data/p9_a.jsonl', 'data/p9_b.jsonl'):
    for line in open(f):
        r = json.loads(line); lanes[r['c']] = r
S, St = {}, {}
for f in ('data/all300.jsonl',):
    for line in open(f):
        r = json.loads(line)
        S[r['c']] = {int(w): s for w, s in r['S'].items()}
        St[r['c']] = {int(w): s for w, s in r['Strunc'].items()}
cs = sorted(S)
Ws = [10**k for k in range(2, 8)]
col = {'real': 2, 'sched': 4}
def meas(kind, W):
    return sum(next(x for x in lanes[c]['rungs'] if x[0] == W)[col[kind]] for c in cs) / sum(lanes[c]['v'] for c in cs)
def theo(SS, W):
    return 1 + sum((lanes[c]['e'] - lanes[c]['v']) / 2 * (SS[c][W] + 1) for c in cs) / sum(lanes[c]['v'] for c in cs)
nwin = {W: len(cs) * 10**8 // W for W in Ws}
def table(kind, SS, label):
    m = np.array([meas(kind, W) for W in Ws]); t = np.array([theo(SS, W) for W in Ws])
    se = m * np.sqrt(2 / np.array([nwin[W] for W in Ws]))
    x = np.log10(Ws)
    print(f"\n{label}   ({len(cs)} lanes)")
    print("W        " + " ".join(f"{W:>8.0e}" for W in Ws))
    print("measured " + " ".join(f"{v:8.4f}" for v in m))
    print("theory   " + " ".join(f"{v:8.4f}" for v in t))
    print("diff     " + " ".join(f"{v:+8.4f}" for v in t - m))
    print("z        " + " ".join(f"{v:+8.1f}" for v in (t - m) / se))
    for k, nm in ((5, '1e2-1e6'), (6, 'six-rung')):
        print(f"OLS slope {nm}: theory {np.polyfit(x[:k], t[:k], 1)[0]:+.4f}  measured {np.polyfit(x[:k], m[:k], 1)[0]:+.4f}")
    return m, t
if len(cs) < 300: print("PARTIAL:", len(cs), "lanes")
table('real', S, 'REAL primes vs full pair series')
table('sched', St, 'SCHED stream (rings<=1000 on schedule) vs truncated pair series')
CS = {W: np.array([lanes[c]['C'] * S[c][W] for c in cs]) for W in Ws}
print("\nC*S over lanes: mean (sd)  and per-decade step; -ln10 = -2.3026")
for i, W in enumerate(Ws):
    print(f"{W:>9}  {CS[W].mean():+8.3f} ({CS[W].std():.3f})" + ("" if i == 0 else f"   step {CS[W].mean() - CS[Ws[i-1]].mean():+.3f}  (sd of step {np.std(CS[W]-CS[Ws[i-1]]):.3f})"))
# 1e8 rung, extrapolated: C*S(1e8) = C*S(1e7) - ln10 per lane  [G]
t8 = 1 + sum((lanes[c]['e'] - lanes[c]['v']) / 2 * (S[c][10**7] - np.log(10) / lanes[c]['C'] + 1) for c in cs) / sum(lanes[c]['v'] for c in cs)
m8 = sum(next(x for x in lanes[c]['rungs'] if x[0] == 10**8)[2] for c in cs) / sum(lanes[c]['v'] for c in cs)
print(f"\n1e8 rung (one window per lane): theory by one more -ln10 step {t8:.4f}  measured {m8:.4f}  SE {m8*np.sqrt(2/len(cs)):.4f}")
