#!/usr/bin/env python3
"""
PHASE 12 — fire-count census + the parity-dead channel family.

PROVENANCE. This is an INDEPENDENT RECONSTRUCTION of GLM's "Draft 2 (fire-count
census)" (GLM audit session 2026-10-10), from three relayed descriptors only:
  (a) "fire-count census";
  (b) "Draft 2's parity-dead channel family is the channel-side dual of your
      B5 layer theorem";
  (c) "the conditional fire structure ... C4's backbone".
The original draft text was never relayed in full ([G]; D1/D3 were absorbed as
B2/B7 at bce2cf6 from relayed text; D2's body is not in any local artifact).
Role (c) is SUPERSEDED: PHASE 10 closed C4 [E] as the Hardy–Littlewood prime-
pair law, so the conditional fire structure is no longer an open object.
What remains native to D2: the census itself (a) and the parity-dead family (b).

FROZEN CONVENTIONS.
F1  Ring schedule: ring p is active on layer m iff p <= sqrt(T(m)) (the sieve
    boundary; gear_net's "switching on at p^2"). Fire: ring p fires at tick
    value N iff p | N. (Same convention as probes/shadows.c, which sieves
    every tick value to sqrt T(m).)
F2  Fire count of tick N on layer m: f(N,m) = #{p prime, p <= sqrt(T(m)) : p|N}.
F3  Channel (a,b): reduced ratio (gcd(a,b)=1), realized on layer m = g*b at
    tick k = g*a (visit number g), value x = T(m-1) + k = g(g*b*b - b + 2*a)/2
    (WHITEPAPER §2 form). g >= 1, a <= b (so k <= m).
F4  Parity-dead: x even for EVERY visit g >= 1 (a prime > 2 can never land).

PREREGISTERED CLAIMS (before running).
P-A [F] Zero fires <=> N prime. (Any composite N has a factor <= sqrt N <=
    sqrt T(m), present as a ring; the ring fires.) Consequence: the census's
    zero class IS the layer's prime count.
P-B [F] mean f over a layer -> sum_{p <= sqrt(T(m))} 1/p  =  ln ln m + const,
    i.e. the mean grows like ln ln m (Mertens' third theorem shape).
P-C [F] Parity-dead <=> (b even AND a == b/2 mod 2). Proof sketch: visit g=2
    forces b even (x(2) = 2b^2 - b + 2a == b mod 2); with b even, visit g=1
    forces a == b/2 mod 2 (x(1) = b(b-1)/2 + a == b/2 + a mod 2); the two
    conditions are sufficient by the same two cases split by g parity.
P-D [F] Number of dead ticks on layer m: sum over b|m with b == 2 mod 4 of
    phi(b);  divisors b == 0 mod 4 contribute ZERO, because a unit of an
    even b is always odd, so the predicate a == b/2 mod 2 is met by all
    units when b/2 is odd (b == 2 mod 4) and by none when b/2 is even
    (b == 0 mod 4). First-wrong-form note: the prereg's "phi(b)/2" line
    was a false step ("half the units are even" — impossible for even b);
    caught by the closed-form-vs-direct check at m=4, corrected in flight.
P-E [E-measured] Dead ticks carry zero primes at every sampled layer
    (converse of P-C sufficiency, machine-checked both directions).

Run: python3 lab/PHASE12_fire_census.py   (~1-2 min)
"""

import sys, json
from math import gcd, log, log10
from collections import Counter

sys.path.insert(0, "probes")
from primes_util import sieve, primes_up_to


def T(n):
    return n * (n + 1) // 2


def fire_census(m, is_prime_arr, primes):
    """Fire-count distribution over layer m's m tick values; plus checks P-A/P-B."""
    lo, hi = T(m - 1) + 1, T(m)          # the layer's m consecutive values
    bound = int(hi ** 0.5) + 1           # rings: primes p <= sqrt(T(m))
    rings = [p for p in primes if p <= bound]
    # fire count per tick via additive sieve over the window
    f = [0] * m
    for p in rings:
        # multiples of p in [lo, hi]
        start = ((lo + p - 1) // p) * p
        for v in range(start, hi + 1, p):
            f[v - lo] += 1
    dist = Counter(f)
    zero = dist[0]
    true_primes = sum(1 for v in range(lo, hi + 1) if is_prime_arr[v])
    mean = sum(f) / m
    pred_mean = sum(1.0 / p for p in rings)
    return {
        "m": m, "rings": len(rings), "dist": {str(k): v for k, v in sorted(dist.items())},
        "zero_fires": zero, "true_primes": true_primes,
        "zero_matches": zero == true_primes,          # P-A
        "mean_fires": round(mean, 4), "pred_mean_sum_1p": round(pred_mean, 4),
    }


def channel_value(g, a, b):
    return T(g * b - 1) + g * a


def parity_dead_predicate(a, b):
    return b % 2 == 0 and a % 2 == (b // 2) % 2


def theorem_check(B=200, G=400):
    """P-C both directions.
    Sufficient: predicate => x(g) even for every g <= G.
    Necessary: not predicate => SOME x(g) odd for g <= G (existence of one odd
    visit is what 'alive' means; a live channel still has many even visits).
    G=400 is overkill: the parity case analysis gives odd visits at g=1
    (b even) or g in {1,3} (b odd), but we check generously."""
    bad_sufficient, alive_without_odd = [], []
    for b in range(1, B + 1):
        for a in range(1, b + 1):
            if gcd(a, b) != 1:
                continue
            if parity_dead_predicate(a, b):
                for g in range(1, G + 1):
                    if channel_value(g, a, b) % 2 != 0:
                        bad_sufficient.append((a, b, g))
                        break
            else:
                if not any(channel_value(g, a, b) % 2 == 1 for g in range(1, G + 1)):
                    alive_without_odd.append((a, b))
    return bad_sufficient, alive_without_odd


def dead_ticks_on_layer(m):
    """P-D: count of parity-dead ticks on layer m via the closed form."""
    total, by_b = 0, {}
    for b in range(2, m + 1, 2):          # even b dividing m
        if m % b:
            continue
        phi = sum(1 for a in range(1, b + 1) if gcd(a, b) == 1)
        cnt = phi if b % 4 == 2 else 0    # units of even b are all odd
        by_b[b] = cnt
        total += cnt
    return total, by_b


def dead_ticks_direct(m):
    """Independent recount: list the dead ticks k directly and verify x even."""
    ks = []
    for b in range(2, m + 1, 2):
        if m % b:
            continue
        g = m // b
        for a in range(1, b + 1):
            if gcd(a, b) == 1 and parity_dead_predicate(a, b):
                ks.append(g * a)
    return sorted(ks)


def layer_dead_check(m, is_prime_arr):
    """P-E: dead ticks carry no primes; report density + any violation."""
    lo = T(m - 1)
    ks = dead_ticks_direct(m)
    primes_on_dead = [k for k in ks if is_prime_arr[lo + k]]
    return {
        "m": m, "dead_ticks": len(ks), "layer_size": m,
        "density": round(len(ks) / m, 4),
        "primes_on_dead": primes_on_dead,          # must be [] everywhere
    }


def main():
    out = {}

    # --- Part 1: fire census on a stratified sample of layers
    print("[census] sieving ...", flush=True)
    top = T(3000)
    isp = sieve(top)
    primes = primes_up_to(int(top ** 0.5) + 2)
    sample = list(range(101, 201)) + [m for m in range(210, 1201, 10)] + \
             [1500, 2000, 2500, 3000]
    cens = [fire_census(m, isp, primes) for m in sample]
    out["census"] = cens
    pa_ok = all(c["zero_matches"] for c in cens)
    print(f"[census] layers={len(cens)}  P-A zero-fires==primes everywhere: {pa_ok}", flush=True)
    for c in cens[:3] + cens[-3:]:
        print(f"  m={c['m']}: rings={c['rings']} dist={c['dist']} "
              f"zero={c['zero_fires']} primes={c['true_primes']} "
              f"mean={c['mean_fires']} sum1/p={c['pred_mean_sum_1p']}", flush=True)
    # P-B shape: mean vs ln ln m at the big end
    lls = [(c["m"], c["mean_fires"], log(log(c["m"]))) for c in cens if c["m"] >= 1000]
    out["mean_vs_lnlnm"] = [{"m": m, "mean": mu, "lnlnm": round(ll, 4)} for m, mu, ll in lls]

    # --- Part 2: parity-dead theorem, both directions
    bs, bn = theorem_check()
    out["theorem"] = {"sufficient_violations": bs[:5], "alive_without_odd_visit": bn[:5],
                      "checked": "b<=200, g<=400, all reduced (a,b)"}
    print(f"[theorem] P-C sufficient violations: {len(bs)}, "
          f"non-dead channels with no odd visit: {len(bn)}", flush=True)

    # --- Part 3: dead-tick count closed form vs direct, and zero primes on dead ticks
    closed_ok, layers_checked, violations, dens = True, [], [], []
    for m in range(4, 3001, 4):              # m == 0 mod 4: where dead channels live
        closed, _ = dead_ticks_on_layer(m)
        direct = dead_ticks_direct(m)
        if closed != len(direct):
            closed_ok = False
            print(f"  P-D mismatch at m={m}: closed={closed} direct={len(direct)}")
        r = layer_dead_check(m, isp)
        layers_checked.append(m)
        dens.append(r["density"])
        if r["primes_on_dead"]:
            violations.append(r)
    out["dead_layers"] = {
        "m_0_mod_4_checked": len(layers_checked),
        "closed_form_matches_direct": closed_ok,          # P-D
        "prime_violations": violations,                    # P-E: must be []
        "density_min": round(min(dens), 4), "density_max": round(max(dens), 4),
        "density_mean": round(sum(dens) / len(dens), 4),
    }
    print(f"[dead] layers 0 mod 4 checked: {len(layers_checked)}; "
          f"P-D closed form exact: {closed_ok}; prime violations: {len(violations)}; "
          f"dead-tick density mean={out['dead_layers']['density_mean']} "
          f"[{out['dead_layers']['density_min']}, {out['dead_layers']['density_max']}]", flush=True)

    with open("lab/PHASE12_fire_census.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote lab/PHASE12_fire_census.json", flush=True)


if __name__ == "__main__":
    main()
