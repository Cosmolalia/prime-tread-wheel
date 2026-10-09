"""P4, best effort: how few Goldbach candidates can freely turned rings leave uncovered?
Ring 2 stays on the evens; every odd ring p <= sqrt(2n) gets its real number of seams (2, or 1 if p | 2n), placed freely.
Local search (simulated annealing) over seam positions, minimizing uncovered odd candidates in (sqrt(2n), n].
A result of 0 is a verified wipe-out. A positive minimum is the best found, not a proof."""
import json, math, sys, time
import numpy as np
from p4_goldbach import setup
from primes_util import sieve

ISP = sieve(400_000)


def anneal(N2, iters, rng, restarts=3):
    n, y, rings, seams, X = setup(N2)
    m = X.size
    slots = [(p, j) for p in rings for j in range(seams[p])]          # one slot per seam
    members = {p: [np.flatnonzero(X % p == r) for r in range(p)] for p in rings}
    best_all = m
    for _ in range(restarts):
        pos = {s: int(rng.integers(s[0])) for s in slots}
        cnt = np.zeros(m, dtype=np.int32)
        for (p, j), r in pos.items():
            cnt[members[p][r]] += 1
        unc = int((cnt == 0).sum())
        best = unc
        T0 = 1.0
        for it in range(iters):
            temp = T0 * (1 - it / iters) + 1e-3
            s = slots[int(rng.integers(len(slots)))]
            p = s[0]
            old, new = pos[s], int(rng.integers(p))
            if new == old:
                continue
            mo, mn = members[p][old], members[p][new]
            delta = int((cnt[mo] == 1).sum()) - int((cnt[mn] == 0).sum())
            if delta <= 0 or rng.random() < math.exp(-delta / temp):
                cnt[mo] -= 1
                cnt[mn] += 1
                pos[s] = new
                unc += delta
                if unc < best:
                    best = unc
                    if best == 0:
                        assert int((cnt == 0).sum()) == 0
                        return 0, m
        best_all = min(best_all, best)
    return best_all, m


if __name__ == "__main__":
    rng = np.random.default_rng(17)
    out = {}
    t0 = time.time()
    for base in (500, 700, 1000, 2000, 4000, 8000, 16000, 32000):
        rows = []
        iters = 60000 if base <= 2000 else 120000
        for N2 in range(base, base + 12, 2):
            best, m = anneal(N2, iters, rng)
            n, y = N2 // 2, math.isqrt(N2)
            real = sum(1 for x in range(y + 1, n + 1) if ISP[x] and ISP[N2 - x])
            rows.append({"2n": N2, "best_uncovered": best, "candidates": m, "real_pairs": real})
        out[base] = rows
        b = [r["best_uncovered"] for r in rows]
        print(f"2n near {base}: wiped {sum(1 for v in b if v == 0)}/6; fewest pairs left by any turning found: "
              f"{min(b)}..{max(b)} (mean {np.mean(b):.1f}); real pairs ~{np.mean([r['real_pairs'] for r in rows]):.0f}  [{time.time()-t0:.0f}s]", flush=True)
        json.dump(out, open("p4_anneal.json", "w"), indent=1)
