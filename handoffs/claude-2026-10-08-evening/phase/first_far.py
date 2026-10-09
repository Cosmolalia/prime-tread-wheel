"""For the 11 gears up to 31, scan out from 0 for the first blank run of each length 44..51
(the widths of the layers those gears decide). Stops at a limit and reports what it found."""
import json, math, sys, time
import numpy as np
ps = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
want = list(range(44, 52))
found = {}
limit = int(float(sys.argv[1])) if len(sys.argv) > 1 else int(3e10)
chunk = 16_000_000
last, s, best, t0 = None, 0, 0, time.time()
while s < limit and len(found) < len(want):
    e = s + chunk
    mask = np.ones(chunk, dtype=bool)
    for p in ps:
        mask[(-s) % p::p] = False
    idx = np.flatnonzero(mask) + s
    seq = idx if last is None else np.concatenate(([last], idx))
    runs = np.diff(seq) - 1
    mx = int(runs.max()) if runs.size else 0
    if mx >= 44:
        for L in want:
            if L not in found:
                hit = np.flatnonzero(runs >= L)
                if hit.size:
                    found[L] = int(seq[hit[0]] + 1)
    last = int(idx[-1]); s = e
    if (s // chunk) % 250 == 0:
        print(f"  scanned {s:.3e} in {time.time()-t0:.0f}s, found {sorted(found.items())}", flush=True)
json.dump({"scanned_to": s, "found": found}, open("first_far.json", "w"))
print("done", s, sorted(found.items()))
