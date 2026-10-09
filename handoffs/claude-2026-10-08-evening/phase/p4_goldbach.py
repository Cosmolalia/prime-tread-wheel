"""P4: can freely turned rings wipe out every Goldbach pair of 2n?
Real: ring p (odd, p <= sqrt(2n)) covers x when p | x or p | 2n - x: two seams, or one when p | 2n. Ring 2 covers the evens.
Free: ring 2 stays on the evens (no even past 2 is prime); every odd ring gets the same number of seams, anywhere.
Candidates: odd x with sqrt(2n) < x <= n. Uncovered x in the real world = a Goldbach pair (x, 2n - x).
Greedy first (a cover it finds is a proof that a wipe-out exists); exact ILP (CBC) decides the rest."""
import json, math, sys, time
import numpy as np
import pulp
from primes_util import sieve

PR = [int(p) for p in np.nonzero(sieve(1000))[0] if p > 2]
ISP = sieve(200000)

def setup(N2):
    n = N2 // 2
    y = math.isqrt(N2)
    rings = [p for p in PR if p <= y]
    seams = {p: (1 if N2 % p == 0 else 2) for p in rings}
    X = np.array([x for x in range(y + 1, n + 1) if x % 2 == 1], dtype=np.int64)
    return n, y, rings, seams, X

def greedy(X, rings, seams, rng, tries=30):
    for _ in range(tries):
        unc = X.copy()
        left = {p: seams[p] for p in rings}
        while unc.size and any(left.values()):
            best, cands = -1, []
            for p, c in left.items():
                if c == 0: continue
                cnt = np.bincount(unc % p, minlength=p)
                v = int(cnt.max())
                if v > best: best, cands = v, [(p, np.flatnonzero(cnt == v))]
                elif v == best: cands.append((p, np.flatnonzero(cnt == v)))
            if best <= 0: break
            p, rs = cands[int(rng.integers(len(cands)))]
            r = int(rs[int(rng.integers(len(rs)))])
            left[p] -= 1
            unc = unc[unc % p != r]
        if unc.size == 0:
            return True
    return False

def exact(X, rings, seams, limit=120):
    prob = pulp.LpProblem("cover", pulp.LpMinimize)
    z = {(p, r): pulp.LpVariable(f"z_{p}_{r}", cat="Binary") for p in rings for r in range(p)}
    prob += 0
    for p in rings:
        prob += pulp.lpSum(z[(p, r)] for r in range(p)) <= seams[p]
    for x in X:
        prob += pulp.lpSum(z[(p, int(x) % p)] for p in rings) >= 1
    status = prob.solve(pulp.PULP_CBC_CMD(msg=0, timeLimit=limit))
    s = pulp.LpStatus[status]
    return {"Optimal": True, "Infeasible": False}.get(s, None)

def real_pairs(N2, y):
    n = N2 // 2
    return sum(1 for x in range(y + 1, n + 1) if ISP[x] and ISP[N2 - x])

if __name__ == "__main__":
    lo, hi, step = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = np.random.default_rng(3)
    out = []
    t0 = time.time()
    for N2 in range(lo, hi + 1, step):
        n, y, rings, seams, X = setup(N2)
        if not rings or X.size == 0:
            continue
        how = "greedy"
        ok = greedy(X, rings, seams, rng)
        if not ok:
            how = "exact"
            ok = exact(X, rings, seams)
        out.append({"2n": N2, "wipe": ok, "how": how, "real_pairs": real_pairs(N2, y), "cands": int(X.size), "rings": len(rings)})
        if N2 % 200 == 0 or ok:
            print(f"2n={N2}: wipe={ok} ({how}); real pairs {out[-1]['real_pairs']}; candidates {X.size}; [{time.time()-t0:.0f}s]", flush=True)
    json.dump(out, open(f"p4_{lo}_{hi}_{step}.json", "w"))
    w = [r["2n"] for r in out if r["wipe"] is True]
    u = [r["2n"] for r in out if r["wipe"] is None]
    print("wipeable:", w)
    print("undecided:", u)
