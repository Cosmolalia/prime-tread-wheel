"""Walk the number line for rings up to 43 until the first blank run of >= 63 (P8 check, independent of p3_far)."""
import json, time
import numpy as np
ps = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
L, limit, chunk = 63, int(2e10), 16_000_000
last, s, t0, hit = None, 0, time.time(), None
while s < limit and hit is None:
    mask = np.ones(chunk, dtype=bool)
    for p in ps:
        mask[(-s) % p::p] = False
    idx = np.flatnonzero(mask) + s
    seq = idx if last is None else np.concatenate(([last], idx))
    runs = np.diff(seq) - 1
    h = np.flatnonzero(runs >= L)
    if h.size:
        hit = [int(seq[h[0]] + 1), int(runs[h[0]])]
    last = int(idx[-1]); s += chunk
json.dump({"scanned_to": s, "first_run_ge_63": hit, "secs": round(time.time() - t0)}, open("p3_scan14.json", "w"))
print("first run >= 63 for rings up to 43:", hit, "scanned to", s, "in", round(time.time() - t0), "s")
