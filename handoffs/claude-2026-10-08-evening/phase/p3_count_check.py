"""Brute-force check of p3_count: count maximal blank runs of length >= L in one full lap, for small ring sets."""
import math, subprocess, numpy as np
PR = [2, 3, 5, 7, 11, 13, 17, 19, 23]
for k, Ls in ((5, [5, 7, 9, 11, 13]), (6, [9, 13, 15, 17, 19, 21]), (7, [15, 19, 21, 23, 25]), (8, [21, 25, 27, 29, 31, 33])):
    ps = PR[:k]; P = math.prod(ps)
    ok = np.ones(P, dtype=bool)
    for p in ps: ok[::p] = False
    idx = np.flatnonzero(ok)
    gaps = np.diff(np.concatenate((idx, [idx[0] + P]))) - 1
    out = subprocess.run(["./p3_count", str(k)] + [str(L) for L in Ls], capture_output=True, text=True).stdout.split("\n")
    for L, line in zip(Ls, out):
        brute = int((gaps >= L).sum()); got = int(line.split()[2])
        print(f"k={k} L={L}: brute {brute}, p3_count {got}, {'OK' if brute == got else 'MISMATCH'}")
