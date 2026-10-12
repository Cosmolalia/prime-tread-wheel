import json, numpy as np
lanes = {}
for f in ('../phase/p9_a.jsonl', '../phase/p9_b.jsonl'):
    for l in open(f):
        r = json.loads(l); lanes[r['c']] = r
res = {}
for f in ('r8A.jsonl', 'r8B.jsonl'):
    for l in open(f):
        r = json.loads(l); res[r['c']] = r
cs = sorted(res)
C = {c: lanes[c]['C'] for c in lanes}
steps = [C[c] * (res[c]['S']['100000000'] - res[c]['S']['10000000']) for c in cs]
print(f'{len(cs)} lanes at W=1e8.  C*S step 1e7->1e8: mean {np.mean(steps):+.4f} (sd {np.std(steps):.4f})   [-ln10 = -2.3026]')
CS8 = [C[c] * res[c]['S']['100000000'] for c in cs]; print(f'C*S(1e8): mean {np.mean(CS8):+.3f} sd {np.std(CS8):.3f}')
Ua = np.mean([C[c] * res[c]['Q1'] for c in cs]); Ua_sd = np.std([C[c] * res[c]['Q1'] for c in cs])
Phi2 = np.mean([res[c]['Q'] - res[c]['Q1'] for c in cs])
print(f'U_a = C*Q1: mean {Ua:.1f} (cross-lane sd {Ua_sd:.1f}, {100*Ua_sd/abs(Ua):.2f}%);  parity term {Phi2:.1f}')
num = 0.0; den = 0.0
for c, L in lanes.items():
    Q = res[c]['Q'] if c in res else Ua / C[c] + Phi2
    num += C[c]**2 * Q; den += L['v']
R8 = 1 + num / den
m8 = sum(next(x for x in L['rungs'] if x[0] == 10**8)[2] for L in lanes.values()) / den
print(f'R(1e8): theory {R8:.4f}   measured {m8:.4f}   SE {m8*np.sqrt(2/300):.4f}   z {(m8-R8)/(m8*np.sqrt(2/300)):+.2f}   (extrapolated [G] 0.4494)')
# same, constant-density approximation for comparison: (e-v)/2 (S+1) with S(1e8)
numc = 0.0
for c, L in lanes.items():
    S8 = res[c]['S']['100000000'] if c in res else np.mean(CS8) / C[c]
    numc += (L['e'] - L['v']) / 2 * (S8 + 1)
print(f'   constant-density scorer for comparison: {1 + numc/den:.4f}')
sub = cs
num23 = sum(C[c]**2 * res[c]['Q'] for c in sub); den23 = sum(lanes[c]['v'] for c in sub)
m23 = sum(next(x for x in lanes[c]['rungs'] if x[0] == 10**8)[2] for c in sub) / den23
print(f'   the {len(sub)} computed lanes alone: theory {1+num23/den23:.4f}  measured {m23:.4f}  SE {m23*np.sqrt(2/len(sub)):.4f}')
json.dump({'R8_theory': R8, 'R8_measured': m8, 'step_mean': float(np.mean(steps)), 'step_sd': float(np.std(steps)), 'Ua': Ua, 'Phi2': Phi2}, open('pool8.json', 'w'))
