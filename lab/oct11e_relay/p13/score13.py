import json, math
pred = json.load(open('bh_pred.json'))
def load(fn):
    try: return json.load(open(fn))
    except Exception: return None
rows = []
print('P13 locked seams — layers 1e6..1e8')
for z in (13, 17, 19, 23):
    A, B = load(f'A{z}.json'), load(f'B{z}.json')
    if A is None or B is None: print('z', z, 'missing'); continue
    t = pred[f'tick1_z{z}']
    E_f = t['frozen'] * A['tick1_sum_invln']; E_r = t['refined'] * A['tick1_sum_invln']; o = A['tick1_primes']
    print(f"\nz={z}: locked layers {A['locked_layers']} (B sample {B['locked_layers']}); desert exceptions {A['desert_exceptions']}+{B['desert_exceptions']} (ticks 2..{A['pnext']-1})")
    print(f"  tick 1: {o} primes;  frozen boost {t['frozen']:.3f} -> expect {E_f:.1f} (z {(o-E_f)/math.sqrt(E_f):+.1f});  "
          f"refined {t['refined']:.3f} -> {E_r:.1f} (z {(o-E_r)/math.sqrt(E_r):+.1f});  measured boost {o/A['tick1_sum_invln']:.3f}")
    W = {w['lam']: w for w in pred[f'windows_z{z}']}
    print('   lam      h   locked obs/E   ctrl obs/E   ratio meas   frozen  refined   sig   frozen-pass refined-pass')
    for wa, wb in zip(A['windows'], B['windows']):
        lam = wa['lam']; w = wa if wa['locked_n'] > 0 and lam <= 3 else wb
        if w['locked_n'] == 0 or w['ctrl_n'] == 0: continue
        p = W[lam]
        EL = p['locked_per_lnx'] * w['locked_sum_invln']; EC = p['control_per_lnx'] * w['ctrl_sum_invln']
        rm = (w['locked_primes'] / w['locked_sum_invln']) / (w['ctrl_primes'] / w['ctrl_sum_invln'])
        sig = rm * math.sqrt(1 / max(w['locked_primes'], 1) + 1 / max(w['ctrl_primes'], 1))
        tol = lambda pr: max(0.03 * pr, 3 * sig)
        fp = abs(rm - p['frozen_ratio']) <= tol(p['frozen_ratio']); rp = abs(rm - p['refined_ratio']) <= tol(p['refined_ratio'])
        print(f"  {lam:5} {w['h']:7d}   {w['locked_primes']/EL:8.4f}     {w['ctrl_primes']/EC:8.4f}    {rm:8.4f}   {p['frozen_ratio']:.4f}  {p['refined_ratio']:.4f}  {sig:.4f}   {'PASS' if fp else 'FAIL':5}       {'PASS' if rp else 'FAIL'}")
        rows.append(dict(z=z, lam=lam, h=w['h'], meas=rm, sig=sig, frozen=p['frozen_ratio'], refined=p['refined_ratio'],
                         locked_obs_over_E=w['locked_primes']/EL, ctrl_obs_over_E=w['ctrl_primes']/EC, n_locked=w['locked_n'], n_ctrl=w['ctrl_n']))
json.dump(rows, open('p13_scored.json', 'w'), indent=1)
