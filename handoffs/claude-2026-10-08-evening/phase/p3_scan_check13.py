"""Independent brute-force check of p3_far for rings up to 37: walk the number line from 0 to 4.7 billion
and record where the first blank run of each length starts (same method as first_far.py)."""
import json, sys, time
import numpy as np
ps = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
want = list(range(55, 66))
found, limit, chunk = {}, int(4.30e9), 16_000_000
last, s, t0 = None, 0, time.time()
while s < limit:
    mask = np.ones(chunk, dtype=bool)
    for p in ps:
        mask[(-s) % p::p] = False
    idx = np.flatnonzero(mask) + s
    seq = idx if last is None else np.concatenate(([last], idx))
    runs = np.diff(seq) - 1
    mx = int(runs.max())
    if mx >= want[0]:
        for L in want:
            if L not in found:
                hit = np.flatnonzero(runs >= L)
                if hit.size:
                    found[L] = [int(seq[hit[0]] + 1), int(runs[hit[0]])]
    last = int(idx[-1]); s += chunk
json.dump({"scanned_to": s, "found": found, "secs": round(time.time() - t0)}, open("p3_scan_check13.json", "w"))
print("scanned to", s, "in", round(time.time() - t0), "s")
for L in want:
    print(L, found.get(L))
