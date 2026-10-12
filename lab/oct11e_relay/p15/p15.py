# P15 — hear the zeta zeros in the wheel's per-layer prime counts.
# Layer m holds (T(m-1), T(m)], T(n) = n(n+1)/2.  Residual r_m = count_m - [R(T(m)) - R(T(m-1))].
# Zero rho = 1/2 + i t adds  -2 Re Z_m(t),  Z_m(t) = e^{rho u_m} * 2 sinh(rho h_m/2) / (rho u_m)   (exact up to 1/u
# varying across the layer), u_m = layer midpoint in ln x, h_m = layer width in ln x.  Fit r = a c + b c~ per t.
import numpy as np, gzip, json, sys, time
from scipy.special import expi
t0 = time.time()
raw = np.loadtxt(gzip.open('../repo/column-engine/layers_1p8M.csv.gz', 'rt'), delimiter=',', skiprows=1,
                 usecols=(0, 1), dtype=np.int64)
m_all, cnt_all = raw[:, 0], raw[:, 1]
assert (m_all == np.arange(1, len(m_all) + 1)).all()
mine = np.loadtxt('../layercount/layers.csv', delimiter=',', skiprows=1, usecols=(0, 1), dtype=np.int64)
k = len(mine); print('cross-check vs my layercount (m <=', k, '):', int((mine[:, 1] != cnt_all[:k]).sum()), 'mismatches')
M0 = 10
m = m_all[M0 - 1:].astype(np.float64); cnt = cnt_all[M0 - 1:].astype(np.float64)
T1 = m * (m + 1) / 2; T0 = (m - 1) * m / 2
L1, L0 = np.log(T1), np.log(T0)
mob = {1: 1, 2: -1, 3: -1, 5: -1, 6: 1, 7: -1, 10: 1, 11: -1, 13: -1, 14: 1, 15: 1, 17: -1, 19: -1}
def R(L): return sum(mu / n * expi(L / n) for n, mu in mob.items())
E = R(L1) - R(L0)
r = cnt - E
u = (L0 + L1) / 2; h = L1 - L0
z = r / np.sqrt(E)
# empirical variance profile v(m) in log-m bins (12 per decade), smooth via interpolation in log m
edges = np.logspace(np.log10(M0), np.log10(m[-1] + 1), 12 * 6 + 1)
idx = np.clip(np.searchsorted(edges, m, side='right') - 1, 0, len(edges) - 2)
vb = np.array([np.mean(z[idx == i] ** 2) if (idx == i).sum() > 5 else np.nan for i in range(len(edges) - 1)])
cb = np.sqrt(edges[:-1] * edges[1:]); ok = ~np.isnan(vb)
v = np.interp(np.log(m), np.log(cb[ok]), vb[ok])
calm = 0.5 - 1.762 / np.log(T1)
print('mean z', z.mean(), ' var(z) by decade vs calm law:')
for lo in (10, 100, 1e3, 1e4, 1e5, 1e6):
    s = (m >= lo) & (m < lo * 10)
    print(f'  m in [{lo:.0e},{lo*10:.0e}): var {np.mean(z[s]**2):.4f}  calm law {np.mean(calm[s]):.4f}  n={s.sum()}')
w = 1.0 / (E * v)
base = np.exp(0.5 * u) / u
small = m <= 2000                                     # exact sinh factor here; elsewhere h(1+z^2/24+z^4/1920)
def Zt(t):
    rho = 0.5 + 1j * t
    zz = rho * h
    G = h * (1 + zz**2 / 24 + zz**4 / 1920)
    G[small] = 2 * np.sinh(rho * h[small] / 2) / rho
    return base * G * np.exp(1j * t * u)
def fit(t, rr=None):
    rr = r if rr is None else rr
    Z = Zt(t); c = -2 * Z.real; s = -2 * Z.imag
    A = np.array([[np.dot(w * c, c), np.dot(w * c, s)], [np.dot(w * c, s), np.dot(w * s, s)]])
    y = np.array([np.dot(w * rr, c), np.dot(w * rr, s)])
    cov = np.linalg.inv(A); a, b = cov @ y
    return a, b, np.sqrt(cov[0, 0]), np.sqrt(cov[1, 1])
gam = [14.134725142, 21.022039639, 25.010857580, 30.424876126, 32.935061588, 37.586178159, 40.918719012,
       43.327073281, 48.005150881, 49.773832478, 52.970321478, 56.446247697, 59.347044003]
res = {'zeros': [], 'controls': [], 'shuffles': []}
print('\nzero        a        b      se_a   se_b   SNR')
for g in gam:
    a, b, sa, sb = fit(g); res['zeros'].append([g, a, b, sa, sb])
    print(f'{g:9.4f}  {a:+.3f}  {b:+.3f}   {sa:.3f}  {sb:.3f}  {np.hypot(a,b)/sa:5.2f}')
print('\ncontrol (midpoints)')
for g1, g2 in zip(gam[:9], gam[1:10]):
    t = (g1 + g2) / 2; a, b, sa, sb = fit(t); res['controls'].append([t, a, b, sa, sb])
    print(f'{t:9.4f}  {a:+.3f}  {b:+.3f}   {sa:.3f}  {sb:.3f}')
rng = np.random.default_rng(15); sd = np.sqrt(E * v)
for i in range(20):
    rr = (r / sd)[rng.permutation(len(r))] * sd
    res['shuffles'].append([list(fit(g, rr)[:2]) for g in gam[:5]])
sh = np.array(res['shuffles']); print('\nshuffles (20 x first 5 zeros): a mean %.3f sd %.3f | b mean %.3f sd %.3f' % (sh[:,:,0].mean(), sh[:,:,0].std(), sh[:,:,1].mean(), sh[:,:,1].std()))
comb = sum(x[1] for x in res['zeros'][:10]); comb_se = np.sqrt(sum(x[3]**2 for x in res['zeros'][:10]))
print(f'comb over first 10 zeros: sum a = {comb:.3f} +/- {comb_se:.3f}')
res['comb'] = [comb, comb_se]
json.dump(res, open('p15_points.json', 'w'), indent=1)
np.savez('p15_arrays.npz', u=u, h=h, r=r, w=w, base=base, m=m, E=E, v=v)
print('time', round(time.time() - t0, 1), 's')
