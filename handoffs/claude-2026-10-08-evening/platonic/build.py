"""Build platonic-map.html: inject the margin data computed in ../phase into the page template.

Free phases keep ring 2 on the evens (no even past 2 is prime); only the odd rings turn.
  free  = most numbers in a row the rings can cover, starting on the same parity as the layer: h - 1, or h - 2 if it starts odd
  can   = the layer's odd numbers fit inside the longest run of odds the odd rings can cover (h/2 - 1)
  first = first place on the number line where these rings cover a stretch as long as the layer that starts on the
          layer's parity (covered stretches always start and end on an even, so an odd start needs one extra number)
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PHASE = os.path.join(HERE, "..", "phase")
sys.path.insert(0, PHASE)
d = json.load(open(os.path.join(PHASE, "margin.json")))
far = {int(k): v for k, v in json.load(open(os.path.join(PHASE, "first_far.json")))["found"].items()}
H = d["H"]
T = lambda m: m * (m + 1) // 2
scan = {r["k"]: r["records"] for r in d["scan"]}


def first_run(k, L):
    """first start of a covered stretch of length >= L for the first k rings (exact data only)"""
    if k in scan:
        return next((s for (ln, s) in scan[k] if ln >= L), None)
    if k == 11:
        return far.get(L)
    return None


rows = []
for r in d["rows"]:
    m, k = r["m"], r["k"]
    lo, hi = T(m - 1) + 1, T(m)
    odds = (hi + 1) // 2 - lo // 2
    h = H[k - 1] if 1 <= k <= len(H) else None
    free = 0 if k == 0 else (h - 1 - (lo % 2) if h else None)
    can = bool(h and k >= 2 and odds <= h // 2 - 1)
    assert can == (free is not None and k >= 2 and m <= free), m
    first = None
    if can and k <= 11:
        first = first_run(k, m) if lo % 2 == 0 else (lambda s: s + 1 if s is not None else None)(first_run(k, m + 1))
        if first is not None:
            ps = [p for p in range(2, 40) if all(p % q for q in range(2, p))][:k]
            assert first % 2 == lo % 2
            assert all(any((first + i) % p == 0 for p in ps) for i in range(m)), m
    rows.append([m, k, r["real"], r["primes"], first, free, 1 if can else 0])

covers = []
for k in range(1, len(H) + 1):
    c = d["covers"][str(k)]
    covers.append([c["L"], 1 if c["exact"] else 0, c["res"]])

# the "pin the small rings" demo: layer 390, every ring up to 83 where counting from 1 puts it, the rest turned
import numpy as np
from pin_test import gears, leftovers, greedy_free, verify
m = 390
g = gears(m)
pinned = [p for p in g if p <= 83]
rng = np.random.default_rng(2026)
assign = None
for _ in range(40):
    a = greedy_free(leftovers(m, pinned), [p for p in g if p > 83], rng, 50)
    if a is not None and verify(m, pinned, a):
        assign = a
        break
assert assign is not None
pin = {"m": m, "upTo": 83, "pinned": len(pinned), "left": int(leftovers(m, pinned).size),
       "real": int(leftovers(m, g).size), "free": {str(p): int(r) for p, r in sorted(assign.items())}}

DATA = {"H": H, "rows": rows, "covers": covers, "pin": pin}
tpl = open(os.path.join(HERE, "template.html")).read()
assert tpl.count("__DATA__") == 1
html = tpl.replace("__DATA__", json.dumps(DATA, separators=(",", ":")))
out = os.path.join(HERE, "platonic-map.html")
open(out, "w").write(html)
cant = [r[0] for r in rows if not r[6]]
print("wrote", out, len(html), "bytes;", len(rows), "layers; can't be wiped:", cant)
print("chart B firsts:", [(r[0], r[4]) for r in rows if 18 <= r[0] <= 51])
print("pin demo:", {k: v for k, v in pin.items() if k != "free"}, "free rings", len(pin["free"]))
