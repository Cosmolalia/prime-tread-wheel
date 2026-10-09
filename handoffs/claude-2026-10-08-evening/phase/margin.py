"""
margin.py: real phases (counting from 1) vs free phases, layer by layer.

Layer m holds T(m-1)+1 .. T(m). Its numbers are decided by the gears p <= sqrt(T(m)); call their count k(m).
  real   = the longest stretch of layer m that those gears actually blank (consecutive composites inside the layer)
  free   = the longest run those same k gears can blank if each gear's phase may be set freely
           (h(k) - 1, the Jacobsthal function of the primorial: exact scan for k <= 10, published values for k <= 58)
  cover  = an explicit set of phases (one residue per gear) that blanks a run at least as long as the layer,
           when one exists: the exact extremal run for k <= 10, a randomized greedy construction beyond
  first  = for k <= 10, the first place counting from 1 where those k gears blank a run as long as the layer
"""
import json, math
import numpy as np
from primes_util import sieve

# Published Jacobsthal values for primorials, OEIS A048670, terms 1..58 (checked against our own scan for 1..10)
H = [2, 4, 6, 10, 14, 22, 26, 34, 40, 46, 58, 66, 74, 90, 100, 106, 118, 132, 152, 174, 190, 200, 216, 234, 258,
     264, 282, 300, 312, 330, 354, 378, 388, 414, 432, 450, 476, 492, 510, 538, 550, 574, 600, 616, 642, 660, 686,
     718, 742, 762, 798, 810, 834, 858, 876, 908, 926, 954]
scan = json.load(open("jacobsthal_scan.json"))
for r in scan:
    assert r["h"] == H[r["k"] - 1], (r["k"], r["h"])

T = lambda m: m * (m + 1) // 2
PR = [int(p) for p in np.nonzero(sieve(2000))[0]]


def greedy_cover(ps, L, rng, tries):
    """Try to cover positions 0..L-1 with one residue class per prime; return residues or None."""
    best_left, best_res = None, None
    for _ in range(tries):
        unc = np.ones(L, dtype=bool)
        res = []
        for p in ps:
            pos = np.flatnonzero(unc)
            if pos.size == 0:
                res.append(int(rng.integers(p)))
                continue
            cnt = np.bincount(pos % p, minlength=p)
            top = np.flatnonzero(cnt == cnt.max())
            r = int(rng.choice(top))
            res.append(r)
            unc[r::p] = False
        left = int(unc.sum())
        if left == 0:
            return res
    return None


def longest_cover(k, rng, start_L, tries=60):
    """Grow L until the greedy stops finding full covers; return (L, residues)."""
    ps = PR[:k]
    L, best = start_L, None
    while True:
        res = greedy_cover(ps, L, rng, tries)
        if res is None:
            # one more push with more tries before giving up
            res = greedy_cover(ps, L, rng, tries * 5)
            if res is None:
                return L - 1, best
        best = res
        L += 1


def check_cover(ps, res, L):
    unc = np.ones(L, dtype=bool)
    for p, r in zip(ps, res):
        unc[r::p] = False
    return not unc.any()


rng = np.random.default_rng(7)
covers = {}
for r in scan:                       # exact extremal covers from the scan
    k, (run, start) = r["k"], r["records"][-1]
    ps = PR[:k]
    res = [(-start) % p for p in ps]
    assert check_cover(ps, res, run)
    covers[k] = {"L": run, "res": res, "exact": True}
prevL = covers[10]["L"]
for k in range(11, 59):
    L, res = longest_cover(k, rng, max(prevL - 5, 10))
    assert res is not None and check_cover(PR[:k], res, L)
    covers[k] = {"L": L, "res": res, "exact": False}
    prevL = L
    print(f"k={k:2d} p={PR[k-1]:3d}  constructed cover {L:3d}  most possible {H[k-1]-1:3d}  ({L/(H[k-1]-1):.0%})")

# per-layer table
MMAX = 390
IS = sieve(T(MMAX) + 10)
pi = np.cumsum(sieve(2000))
rows = []
for m in range(2, MMAX + 1):
    lo, hi = T(m - 1) + 1, T(m)
    k = int(pi[math.isqrt(hi)])
    seg = IS[lo:hi + 1]
    # longest blank (composite) stretch inside the layer
    best = cur = 0
    for v in seg:
        cur = 0 if v else cur + 1
        best = max(best, cur)
    free = H[k - 1] - 1 if k >= 1 else 0
    first = None
    if 1 <= k <= 10 and free >= m:
        recs = scan[k - 1]["records"]
        first = next(s for (L, s) in recs if L >= m)
    rows.append({"m": m, "lo": lo, "hi": hi, "k": k, "gear": PR[k - 1] if k else None, "real": best,
                 "primes": int(seg.sum()), "free": free, "can": free >= m,
                 "built": covers.get(k, {}).get("L", 0) >= m, "first": first})

json.dump({"H": H, "covers": covers, "rows": rows, "scan": scan, "primes": PR[:60]}, open("margin.json", "w"))

can = [r["m"] for r in rows if r["can"]]
cannot = [r["m"] for r in rows if not r["can"]]
print("layers the gears could blank with free phases: first", can[0], "| last layer they could NOT:", max(cannot), "| count could not:", len(cannot))
print("layers that could not:", cannot)
print("all of those built:", all(r["built"] for r in rows if r["can"]))
for lo, hi in ((2, 50), (50, 100), (100, 200), (200, 391)):
    sel = [r for r in rows if lo <= r["m"] < hi]
    print(f"layers {lo:3d}-{hi-1:3d}: real longest blank / layer = {max(r['real']/r['m'] for r in sel):.2f} max, "
          f"{np.mean([r['real']/r['m'] for r in sel]):.2f} mean;  free / layer = {min(r['free']/r['m'] for r in sel):.2f} min, "
          f"{np.mean([r['free']/r['m'] for r in sel]):.2f} mean")
print("first-wipeout distances (k<=10):")
for r in rows:
    if r["first"] is not None:
        print(f"  layer {r['m']:3d} (numbers {r['lo']}..{r['hi']}, gears up to {r['gear']}): first layer-wide blank run from these gears starts at {r['first']:,}  ({r['first']/r['hi']:.0f}x past the layer)")
