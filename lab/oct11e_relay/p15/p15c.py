import numpy as np, mpmath, json, time
mpmath.mp.dps = 20
t0 = time.time()
D = np.load('p15_arrays.npz'); u, h, r, w, base, m = D['u'], D['h'], D['r'], D['w'], D['base'], D['m']
keep = m >= 1000; u, h, r, w, base = u[keep], h[keep], r[keep], w[keep], base[keep]
gam = []; k = 1
while True:
    g = float(mpmath.zetazero(k).imag)
    if g > 400: break
    gam.append(g); k += 1
gam = np.array(gam); K = len(gam); P = 2 * K
print(K, 'zeros below 400; zeros listed in', round(time.time() - t0, 1), 's')
XtWX = np.zeros((P, P)); XtWr = np.zeros(P)
for s in range(0, len(u), 100000):
    sl = slice(s, s + 100000); uu, hh, bb, ww, rr = u[sl], h[sl], base[sl], w[sl], r[sl]
    rho = 0.5 + 1j * gam[None, :]
    G = hh[:, None] * (1 + (rho * hh[:, None])**2 / 24 + (rho * hh[:, None])**4 / 1920)
    Z = bb[:, None] * G * np.exp(1j * uu[:, None] * gam[None, :])
    X = np.empty((len(uu), P)); X[:, 0::2] = -2 * Z.real; X[:, 1::2] = -2 * Z.imag
    XW = X * ww[:, None]; XtWX += XW.T @ X; XtWr += XW.T @ rr
beta = np.linalg.solve(XtWX, XtWr); a, b = beta[0::2], beta[1::2]
def rep(sel, name):
    print(f'{name:22s} n={sel.sum():3d}  mean a {a[sel].mean():.4f}  rms(a-1) {np.sqrt(np.mean((a[sel]-1)**2)):.4f}  rms b {np.sqrt(np.mean(b[sel]**2)):.4f}  worst |a-1| {np.abs(a[sel]-1).max():.4f}')
rep(gam < 60, 'zeros < 60')
rep((gam > 60) & (gam < 200), 'zeros 60-200')
rep((gam > 200) & (gam < 300), 'HELD-OUT 200-300')
rep(gam > 300, 'zeros 300-400 (edge)')
json.dump({'gamma': gam.tolist(), 'a': a.tolist(), 'b': b.tolist()}, open('joint_400_m1000.json', 'w'))
print('time', round(time.time() - t0, 1), 's')
