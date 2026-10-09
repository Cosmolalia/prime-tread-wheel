"""
Exact scan of the full gear cycle for the first k primes (k = 1..10).

Gears 2, 3, 5, ... p_k each mark their multiples. A position "dodges" when no gear marks it
(it is coprime to p_k#). A blank run is a stretch of consecutive positions that every one of
them is marked by some gear. Over one full cycle of length p_k#, this records:
  h(k)      = longest blank run + 1 (the Jacobsthal function of the primorial)
  records   = first start position of each new longest blank run, scanning up from 0
The pattern is mirror-symmetric inside the cycle, so half a cycle (plus a margin) is enough.
"""
import json, math, sys
import numpy as np

PR = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]


def scan(k, chunk=8_000_000):
    ps = PR[:k]
    N = math.prod(ps)
    stop = N // 2 + 4 * N.bit_length() + 400 if k >= 6 else 2 * N + 2
    last = None
    best = 0
    records = []          # (run_length, first_start)
    s = 0
    while s < stop:
        e = min(stop, s + chunk)
        mask = np.ones(e - s, dtype=bool)
        for p in ps:
            mask[(-s) % p::p] = False
        idx = np.flatnonzero(mask) + s
        if idx.size:
            seq = idx if last is None else np.concatenate(([last], idx))
            if seq.size > 1:
                runs = np.diff(seq) - 1
                # first index where a run beats the current best, repeatedly
                while True:
                    over = np.flatnonzero(runs > best)
                    if not over.size:
                        break
                    i = over[0]
                    best = int(runs[i])
                    records.append((best, int(seq[i] + 1)))
            last = int(idx[-1])
        s = e
    return {"k": k, "p": ps[-1], "cycle": N, "h": best + 1, "longest_blank_run": best, "records": records}


if __name__ == "__main__":
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    out = [scan(k) for k in range(1, kmax + 1)]
    for r in out:
        print(f"k={r['k']:2d} p={r['p']:2d} cycle={r['cycle']:>13,}  h={r['h']:3d}  longest blank run={r['longest_blank_run']:3d}"
              f"  first at {r['records'][-1][1]:,}")
    json.dump(out, open("jacobsthal_scan.json", "w"))
