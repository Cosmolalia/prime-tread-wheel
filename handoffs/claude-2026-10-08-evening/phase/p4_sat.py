"""Exact wipe-out check with a SAT solver: one boolean per (odd ring p, seam position r);
at most c_p seams per ring (c_p = 2, or 1 when p divides 2n); every odd candidate x in (sqrt(2n), n] must sit on a seam.
A satisfying assignment is checked directly as a cover. An optional time budget per even number (seconds)."""
import json, sys, time, threading
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from p4_goldbach import setup


def sat_wipe(N2, budget=None):
    n, y, rings, seams, X = setup(N2)
    pool = IDPool()
    v = lambda p, r: pool.id((p, r))
    clauses = []
    for p in rings:
        lits = [v(p, r) for r in range(p)]
        clauses += CardEnc.atmost(lits=lits, bound=seams[p], vpool=pool, encoding=EncType.seqcounter).clauses
    for x in X:
        clauses.append([v(p, int(x) % p) for p in rings])
    with Cadical153(bootstrap_with=clauses) as s:
        timer = None
        if budget:
            timer = threading.Timer(budget, s.interrupt)
            timer.start()
        ok = s.solve_limited(expect_interrupt=True)
        if timer:
            timer.cancel()
        model = s.get_model() if ok else None
    if ok:
        on = {k for k in model if k > 0}
        chosen = {p: [r for r in range(p) if v(p, r) in on] for p in rings}
        assert all(len(chosen[p]) <= seams[p] for p in rings)
        assert all(any(int(x) % p in chosen[p] for p in rings) for x in X)
    return ok          # True = a wipe-out exists, False = proven impossible, None = out of time


if __name__ == "__main__":
    lo, hi, step = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    budget = float(sys.argv[4]) if len(sys.argv) > 4 else None
    out = []
    t0 = time.time()
    for N2 in range(lo, hi + 1, step):
        ok = sat_wipe(N2, budget)
        out.append({"2n": N2, "wipe": ok})
        print(f"2n={N2}: wipe={ok}  [{time.time()-t0:.0f}s]", flush=True)
        json.dump(out, open(f"p4_sat_{lo}_{hi}_{step}.json", "w"))
