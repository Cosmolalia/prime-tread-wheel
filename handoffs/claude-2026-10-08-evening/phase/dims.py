"""Tread wheels with more turning planes.
k clocks with periods m, m+1, ..., m+k-1 turning together: layer m holds m(m+1)...(m+k-1) numbers
(k=1 is our wheel). Totals: m(m+1)...(m+k)/(k+1): triangle, pyramid (x2), 4-simplex (x6) numbers.

For each layer: width, primes on it, longest composite stretch inside, deciding rings (primes <= sqrt(top)),
and the free-phase capacity with ring 2 held on the evens: h(k)-1, or h(k)-2 when the layer starts on an odd number
(exact for up to 58 deciding rings, from OEIS A048670). A layer is safe by width when capacity < width.
Also P7: share of composites flagged by the layer's own clocks with no division of x
(evens via the even clock, and any common factor with a clock period: the visit lock generalized)."""
import json, math
import numpy as np
from primes_util import sieve

H = json.load(open("margin.json"))["H"]
XMAX = 20_000_000
IS = sieve(XMAX + 10)
P = [int(p) for p in np.nonzero(sieve(5000))[0]]


def total(k, m):
    t = 1
    for i in range(k + 1):
        t *= (m + i)
    return t // (k + 1)


def layers(k):
    m = 1
    while True:
        lo, hi = total(k, m - 1) + 1, total(k, m)
        if hi > XMAX:
            return
        yield m, lo, hi
        m += 1


out = {}
for k in (1, 2, 3):
    rows = []
    flagged = comps = 0
    for m, lo, hi in layers(k):
        if hi < 3:
            continue
        seg = IS[lo:hi + 1]
        width = hi - lo + 1
        primes = int(seg.sum())
        idx = np.flatnonzero(seg)
        bounds = np.concatenate(([lo - 1], idx + lo, [hi + 1]))
        longest = int((np.diff(bounds) - 1).max())
        r = math.isqrt(hi)
        nk = sum(1 for p in P if p <= r)
        cap = None
        if 1 <= nk <= len(H):
            cap = H[nk - 1] - 1 - (lo % 2)
        elif nk == 0:
            cap = 0
        # P7: composites flagged by the layer's own clocks (common factor with some clock period)
        periods = [m + i for i in range(k)]
        x = np.arange(lo, hi + 1, dtype=np.int64)
        f = np.zeros(width, dtype=bool)
        for q in periods:
            if q >= 2:
                g = np.gcd(x, q)
                f |= (g > 1) & (g < x)
        isc = ~seg & (x > 1)
        comps += int(isc.sum()); flagged += int((f & isc).sum())
        rows.append({"m": m, "lo": lo, "hi": hi, "width": width, "primes": primes, "longest": longest,
                     "rings": nk, "cap": cap, "safe": (cap is not None and cap < width)})
    out[k] = {"rows": rows, "flag_share": flagged / comps}
    tab = [r for r in rows if r["cap"] is not None]
    unsafe = [r["m"] for r in tab if not r["safe"]]
    worst = max(rows[3:], key=lambda r: r["longest"] / r["width"])
    print(f"\n{k} clock(s): {len(rows)} layers up to {rows[-1]['hi']:,}; every layer holds a prime: {all(r['primes'] > 0 for r in rows)}")
    print(f"  capacity known for layers {tab[0]['m']}..{tab[-1]['m']} (up to {tab[-1]['hi']:,}); layers the rings could wipe: {unsafe}")
    print(f"  capacity / width at the last tabulated layer: {tab[-1]['cap']}/{tab[-1]['width']} = {tab[-1]['cap']/tab[-1]['width']:.2f}")
    print(f"  worst longest-composite share (from layer 4): {worst['longest']}/{worst['width']} at layer {worst['m']}; "
          f"last layer {rows[-1]['longest']}/{rows[-1]['width']} = {rows[-1]['longest']/rows[-1]['width']:.3f}")
    print(f"  composites flagged by the layer's own clocks: {out[k]['flag_share']:.1%}")
json.dump({str(k): v for k, v in out.items()}, open("dims.json", "w"))
