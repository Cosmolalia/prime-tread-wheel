"""
pin_test.py: which gears' real placement protects a layer from being wiped out?

Layer m holds T(m-1)+1 .. T(m); its deciding gears are the primes p <= sqrt(T(m)).
A gear "pinned" sits where counting from 1 puts it: it marks the multiples of p.
A gear "free" may be turned to any phase r: it marks the numbers x with x = r (mod p).

  pin small: pin the j smallest gears (2 the mirror, 3, 5, ...), free all the rest.
             Report the largest j for which a wiping setting was found (greedy set cover, then verified:
             a found setting is a constructive proof).
  pin big:   free only the gears up to 13 (or 17), pin every bigger gear.
             Exact search over every phase setting of the free gears: is there any setting that wipes the layer?
"""
import json, math, sys, time
import numpy as np
from primes_util import sieve

T = lambda m: m * (m + 1) // 2
PR = [int(p) for p in np.nonzero(sieve(3000))[0]]


def gears(m):
    r = math.isqrt(T(m))
    return [p for p in PR if p <= r]


def leftovers(m, pinned):
    lo, hi = T(m - 1) + 1, T(m)
    x = np.arange(lo, hi + 1, dtype=np.int64)
    keep = np.ones(x.size, dtype=bool)
    for p in pinned:
        keep &= x % p != 0
    return x[keep]


def greedy_free(U, free, rng, tries):
    """Cover the positions U using one residue class per free gear. Returns {p: r} or None."""
    if U.size == 0:
        return {p: 0 for p in free}
    for _ in range(tries):
        unc, left, assign = U.copy(), list(free), {}
        while unc.size and left:
            best, cands = -1, []
            for p in left:
                cnt = np.bincount(unc % p, minlength=p)
                c = int(cnt.max())
                if c > best:
                    best, cands = c, [(p, np.flatnonzero(cnt == c))]
                elif c == best:
                    cands.append((p, np.flatnonzero(cnt == c)))
            p, rs = cands[int(rng.integers(len(cands)))]
            r = int(rs[int(rng.integers(len(rs)))])
            assign[p] = r
            left.remove(p)
            unc = unc[unc % p != r]
        if unc.size == 0:
            for p in left:
                assign[p] = 0
            return assign
    return None


def verify(m, pinned, assign):
    lo, hi = T(m - 1) + 1, T(m)
    for x in range(lo, hi + 1):
        if any(x % p == 0 for p in pinned):
            continue
        if not any(x % p == r for p, r in assign.items()):
            return False
    return True


def pin_small(m, rng, tries=10):
    g = gears(m)
    best_j, best_assign = -1, None
    fails = 0
    for j in range(0, len(g) + 1):
        pinned, free = g[:j], g[j:]
        U = leftovers(m, pinned)
        a = greedy_free(U, free, rng, tries)
        if a is not None and verify(m, pinned, a):
            best_j, best_assign, fails = j, a, 0
        else:
            fails += 1
            if fails >= 3:
                break
    return best_j, best_assign


def pin_big_exact(m, nfree):
    """Free the nfree smallest gears, pin the rest. Exact: does ANY setting of the free gears wipe the layer?
    A setting of the free gears is the same as a shift t (mod 2*3*...*p): x is marked iff gcd(x - t, P) > 1."""
    g = gears(m)
    if len(g) <= nfree:
        return None
    free, pinned = g[:nfree], g[nfree:]
    U = leftovers(m, pinned)
    if U.size == 0:
        return True
    P = math.prod(free)
    res = np.stack([U % p for p in free])          # residues of the leftovers
    found = False
    chunk = 20000
    for t0 in range(0, P, chunk):
        t = np.arange(t0, min(P, t0 + chunk), dtype=np.int64)
        covered = np.zeros((t.size, U.size), dtype=bool)
        for i, p in enumerate(free):
            covered |= (res[i][None, :] == (t % p)[:, None])
        if covered.all(axis=1).any():
            found = True
            break
    return found


if __name__ == "__main__":
    rng = np.random.default_rng(11)
    layers = list(range(41, 392, 10)) + [390]
    out = {"pin_small": [], "pin_big": []}
    t0 = time.time()
    for m in layers:
        g = gears(m)
        j, a = pin_small(m, rng)
        frac = 1.0
        for p in g[:max(j, 0)]:
            frac *= 1 - 1 / p
        out["pin_small"].append({"m": m, "k": len(g), "pinned": j, "pinned_up_to": g[j - 1] if j > 0 else None,
                                 "pinned_cover_share": round(1 - frac, 3), "free": len(g) - j})
        print(f"layer {m:3d}: {len(g):2d} gears; pin the smallest {j:2d} (up to {g[j-1] if j > 0 else '-'}), "
              f"they cover {1-frac:.0%} of it; the {len(g)-j} bigger gears, free, still wipe it   [{time.time()-t0:.0f}s]", flush=True)
    for m in layers:
        row = {"m": m}
        for nf in (4, 5, 6):
            row[f"free_up_to_{PR[nf-1]}"] = pin_big_exact(m, nf)
        out["pin_big"].append(row)
        print(f"layer {m:3d}: free only the small gears, pin the rest -> any wipe? ", {k: v for k, v in row.items() if k != 'm'}, flush=True)
    json.dump(out, open("pin_test.json", "w"), indent=1)
