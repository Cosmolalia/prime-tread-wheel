# P15b: joint fit of all zeros below Gamma (cos+sin template per zero), chunked normal equations.
import numpy as np, mpmath, sys, json
D = np.load('p15_arrays.npz'); u, h, r, w, base, m = D['u'], D['h'], D['r'], D['w'], D['base'], D['m']
Gam = float(sys.argv[1]); mmin = float(sys.argv[2]) if len(sys.argv) > 2 else 10
keep = m >= mmin; u, h, r, w, base, m = u[keep], h[keep], r[keep], w[keep], base[keep], m[keep]
gam = []
k = 1
while True:
    g = float(mpmath.zetazero(k).imag)
    if g > Gam: break
    gam.append(g); k += 1
K = len(gam); P = 2 * K
XtWX = np.zeros((P, P)); XtWr = np.zeros(P)
small = m <= 2000
for s in range(0, len(u), 200000):
    sl = slice(s, s + 200000)
    uu, hh, bb, ww, rr, sm = u[sl], h[sl], base[sl], w[sl], r[sl], small[sl]
    X = np.empty((len(uu), P))
    for j, g in enumerate(gam):
        rho = 0.5 + 1j * g
        G = hh + hh**3 / 24 * (0.25 - g * g + 1j * g)
        if sm.any(): G[sm] = 2 * np.sinh(rho * hh[sm] / 2) / rho
        Z = bb * G * np.exp(1j * g * uu)
        X[:, 2 * j] = -2 * Z.real; X[:, 2 * j + 1] = -2 * Z.imag
    XW = X * ww[:, None]
    XtWX += XW.T @ X; XtWr += XW.T @ rr
cov = np.linalg.inv(XtWX); beta = cov @ XtWr; se = np.sqrt(np.diag(cov))
a, b, sa = beta[0::2], beta[1::2], se[0::2]
print(f'Gamma={Gam}: {K} zeros jointly, m >= {mmin:.0f}')
for j in range(min(K, 13)):
    print(f'  γ{j+1:<2} {gam[j]:8.4f}  a {a[j]:+.4f}  b {b[j]:+.4f}   (white-noise se {sa[j]:.3f})')
print(f'  mean a (k<=13) {a[:13].mean():.4f}   rms(a-1) {np.sqrt(np.mean((a[:13]-1)**2)):.4f}   rms b {np.sqrt(np.mean(b[:13]**2)):.4f}')
if K > 13: print(f'  zeros 14..{K}: mean a {a[13:].mean():.4f}  rms(a-1) {np.sqrt(np.mean((a[13:]-1)**2)):.4f}  rms b {np.sqrt(np.mean(b[13:]**2)):.4f}')
json.dump({'Gamma': Gam, 'gamma': gam, 'a': a.tolist(), 'b': b.tolist(), 'se_white': sa.tolist()}, open(f'joint_{int(Gam)}_m{int(mmin)}.json', 'w'))
