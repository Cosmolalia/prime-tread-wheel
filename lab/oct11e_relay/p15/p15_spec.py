# Full spectrum a(t), b(t) on t in [5, 60], step 0.005 (frozen grid). Same model as p15.py; phase by recurrence.
import numpy as np, sys
D = np.load('p15_arrays.npz'); u, h, r, w, base, m = D['u'], D['h'], D['r'], D['w'], D['base'], D['m']
i0, i1 = int(sys.argv[1]), int(sys.argv[2])            # grid indices [i0, i1)
grid = 5 + 0.005 * np.arange(11001)
small = m <= 2000; hs = h[small]; h3 = h**3 / 24
out = np.zeros((i1 - i0, 5))
step = np.exp(1j * 0.005 * u)
for j, i in enumerate(range(i0, i1)):
    t = grid[i]
    if j % 500 == 0: Et = np.exp(1j * t * u)            # re-sync the recurrence
    rho = 0.5 + 1j * t
    G = h + h3 * (0.25 - t * t + 1j * t)                # 2 sinh(rho h/2)/rho to O(h^3); exact below
    G[small] = 2 * np.sinh(rho * hs / 2) / rho
    Z = base * G * Et
    c = -2 * Z.real; s = -2 * Z.imag
    wc, ws = w * c, w * s
    A = np.array([[wc @ c, wc @ s], [wc @ s, ws @ s]]); y = np.array([wc @ r, ws @ r])
    cov = np.linalg.inv(A); a, b = cov @ y
    out[j] = (t, a, b, np.sqrt(cov[0, 0]), np.sqrt(cov[1, 1]))
    Et = Et * step
np.save(f'spec_{i0}_{i1}.npy', out)
