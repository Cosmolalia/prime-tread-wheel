#!/usr/bin/env python3
"""
PHASE 14 — object-A ('all') true d-curve, m = 14..391.

Audit context: GPT's relay (swarm handback 10-12) enumerated all-ticks
home-cover (tick value 97-smooth) for m=2..257, found wipeable = {2..13},
and concluded "all-ticks feasible iff 2 <= m <= 13", plus proved m >= 258
impossible via Jacobsthal h(25)=258. The home-cover census is d = 0 only;
FEASIBILITY with displacement allowed is the MILP question, and for
14 <= m <= 257 runs of 257 Q-non-coprime integers (h(25)=258) predict
FEASIBLE with d >= 1. This probe measures the actual d-curve.

Frozen predictions (before running):
  A1: d(m) finite for all 14 <= m <= 257 (feasibility runs).
  A2: d(m) = None (infeasible) for all 258 <= m <= 391.
  A3: d = 0 exactly on {2..13} (reproduce v1/GPT home census in-pass).
  A4: d(m) >= 1 nondecreasing-ish in m (no formal claim, shape only).

Convention: identical to probes/j1c_wedge_milp.py v2 (home c*=0,
cover iff c == (j+T) mod p, d = min #rings off home).
"""
import json
import os
import sys
import time

sys.path.insert(0, 'probes')
from j1c_wedge_milp import solve_layer  # noqa: E402

OUT = 'lab/PHASE14_objA_dcurve.json'


def main():
    out = {}
    if os.path.exists(OUT):
        with open(OUT) as f:
            out = json.load(f)
    d = out.get('d', {})
    t0 = time.time()
    for m in range(14, 392):
        if str(m) in d:
            continue
        t1 = time.time()
        d[str(m)] = solve_layer(m, 'all')
        out['d'] = d
        with open(OUT, 'w') as f:
            json.dump(out, f, indent=1)
        print(f"m={m} d={d[m]} ({time.time()-t1:.1f}s, "
              f"{int(time.time()-t0)}s total)", flush=True)
    finite = sorted(m for m, v in d.items() if v is not None)
    infeas = sorted(int(m) for m, v in d.items() if v is None)
    print("finite:", finite[0], "..", finite[-1], "count", len(finite),
          flush=True)
    print("infeasible:", infeas, flush=True)
    print("d=0:", [m for m, v in d.items() if v == 0], flush=True)
    print("max d:", max(v for v in d.values() if v is not None), flush=True)
    print("A1:", all(str(m) in d and d[str(m)] is not None
                       for m in range(14, 258)), flush=True)
    print("A2:", all(d.get(str(m)) is None for m in range(258, 392)),
          flush=True)


if __name__ == '__main__':
    main()
