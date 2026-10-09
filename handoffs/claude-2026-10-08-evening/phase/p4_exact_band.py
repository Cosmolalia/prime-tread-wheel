"""Exact (CBC) wipe-out check for samples of even numbers from 500 to 4000, where greedy stops finding covers."""
import json, time
import numpy as np
from p4_goldbach import setup, greedy, exact
rng = np.random.default_rng(1)
samples = []
for base in (500, 700, 1000, 1500, 2000, 3000, 4000):
    samples += list(range(base, base + 12, 2))
out = []
t0 = time.time()
for N2 in samples:
    n, y, rings, seams, X = setup(N2)
    ok = greedy(X, rings, seams, rng, tries=20)
    how = "greedy"
    if not ok:
        ok = exact(X, rings, seams, limit=900)
        how = "exact"
    out.append({"2n": N2, "wipe": ok, "how": how})
    print(f"2n={N2}: wipe={ok} ({how})  [{time.time()-t0:.0f}s]", flush=True)
    json.dump(out, open("p4_exact_band.json", "w"))
print("done")
