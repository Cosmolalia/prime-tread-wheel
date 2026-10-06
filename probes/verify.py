"""
verify.py: reproduce every number in PAPER.md. Needs Python 3 and numpy. Runs in about a minute.

The wheel: layer m holds the m numbers T(m-1)+1 .. T(m), where T(m) = m(m+1)/2.
Tick k of layer m (k = 1..m) holds x = T(m-1) + k and sits k/m of the way around.
"""
import math
from math import gcd, isqrt
import numpy as np
from primes_util import sieve, is_prime, primes_up_to

T = lambda m: m * (m + 1) // 2
ok = lambda flag: "ok" if flag else "FAILED"


def euler_phi(n):
    r, p, m = n, 2, n
    while p * p <= m:
        if m % p == 0:
            while m % p == 0:
                m //= p
            r -= r // p
        p += 1
    if m > 1:
        r -= r // m
    return r


def mobius_upto(n):
    """mu[0..n] by sieving (numpy)."""
    mu = np.ones(n + 1, dtype=np.int8)
    mu[0] = 0
    for p in primes_up_to(n):
        mu[p::p] *= -1
        if p * p <= n:
            mu[p * p::p * p] = 0
    return mu


# 1. Visit theorem ---------------------------------------------------------------------------
L = 800
IS = sieve(T(L) + 1)
formula_ok = composite_ok = seats_ok = primes_on_seats_ok = True
primes_per_spoke = {}
for m in range(1, L + 1):
    seats = 0
    for k in range(1, m + 1):
        x = T(m - 1) + k
        g = gcd(k, m); b = m // g; a = k // g
        if 2 * x != g * (g * b * b - b + 2 * a):
            formula_ok = False
        if g >= 3 and IS[x]:
            composite_ok = False
        seat = (g == 1 and m % 4 != 2) or (g == 2 and b % 2 == 1)
        seats += seat
        if IS[x]:
            primes_per_spoke[(a, b)] = primes_per_spoke.get((a, b), 0) + 1
            if m >= 3 and not seat:
                primes_on_seats_ok = False
    if m >= 3 and seats != euler_phi(m):
        seats_ok = False
print(f"[1] visit formula x = g(gb^2 - b + 2a)/2 on every tick to layer {L}: {ok(formula_ok)}")
print(f"    every visit g >= 3 composite: {ok(composite_ok)}")
print(f"    most primes on any one spoke: {max(primes_per_spoke.values())}  (theorem: at most 2)")
print(f"    every layer m >= 3 has exactly phi(m) prime seats: {ok(seats_ok)}; every prime sits on one: {ok(primes_on_seats_ok)}")

# 2. Parity axis -----------------------------------------------------------------------------
P = 5000
par = all(T(m - 1) % 2 == (m // 2) % 2 for m in range(1, P + 1))
half = all((T(m - 1) + m // 2) == m * m // 2 and (m * m // 2) % 2 == 0 for m in range(2, P + 1))
spoke = all(T(2 * g - 1) + g == 2 * g * g for g in range(1, P + 1))
fresh_even = all((T(m - 1) + k) % 2 == 0 for m in range(2, P + 1, 4) for k in range(1, m + 1) if gcd(k, m) == 1)
print(f"[2] T(m-1) and floor(m/2) share parity, layers 1..{P}: {ok(par)}")
print(f"    halfway tick holds floor(m^2/2), always even: {ok(half)};  half-turn spoke holds 2g^2: {ok(spoke)}")
print(f"    on layers m = 2 mod 4 every fresh tick is even: {ok(fresh_even)}")

# 3. Layer balance ---------------------------------------------------------------------------
B = 2000
mu_small = mobius_upto(B)
worst = 0.0
for m in range(1, B + 1):
    s = sum(complex(math.cos(2 * math.pi * k / m), math.sin(2 * math.pi * k / m)) for k in range(1, m + 1) if gcd(k, m) == 1)
    worst = max(worst, abs(s - int(mu_small[m])))
print(f"[3] fresh-tick arrows sum to mu(m) on layers 1..{B}: largest error {worst:.1e}")

# 4. Running balance (Mertens) --------------------------------------------------------------
N = 10_000_000
M = np.cumsum(mobius_upto(N).astype(np.int64))
n = np.arange(200, N + 1)
q = np.abs(M[200:]) / np.sqrt(n)
i = int(np.argmax(q))
print(f"[4] |M(n)| / sqrt(n) for 200 <= n <= {N:,}: max {q[i]:.4f} at n = {int(n[i]):,}  (paper: stays below 0.57)")

# 5. Junction lanes --------------------------------------------------------------------------
LANE = 100_000
closing_ok = all(not is_prime(T(m)) for m in range(3, LANE + 1))
f = lambda m: T(m - 1) + 1
count = sum(1 for m in range(2, LANE + 1) if is_prime(f(m)))
C = 1.0
for p in primes_up_to(2_000_000)[1:]:
    w = 1 if p == 7 else 1 + (1 if pow((-7) % p, (p - 1) // 2, p) == 1 else -1)
    C *= (1 - w / p) / (1 - 1 / p)
chance = sum(1 / math.log(f(m)) for m in range(2, LANE + 1))
never = [p for p in primes_up_to(100)[1:] if all(f(m) % p for m in range(p))]
rule = [p for p in primes_up_to(100)[1:] if p % 7 in (3, 5, 6)]
print(f"[5] closing tick T(m) composite for every m from 3 to {LANE:,}: {ok(closing_ok)}")
print(f"    opening tick T(m-1)+1 to layer {LANE:,}: {count:,} primes | open seats predict {C * chance:,.0f} | chance {chance:,.0f} | boost {C:.3f}x")
print(f"    odd primes below 100 that never divide it: {never}")
print(f"    (rule: p leaves remainder 3, 5 or 6 when divided by 7 -> {rule}): {ok(never == rule)}")

# 6. Open question: can a whole layer be composite? -----------------------------------------
G = 10_000
ISG = sieve(T(G) + 2)
pr = np.nonzero(ISG)[0]
best_all = (0, 0, 0, 0); best_100 = (0, 0, 0, 0)
for p, q2 in zip(pr[:-1], pr[1:]):
    run = int(q2 - p - 1)
    if run <= 0:
        continue
    start = int(p) + 1
    m = (isqrt(8 * start) + 1) // 2           # layer holding `start`
    while T(m) < start: m += 1
    while T(m - 1) >= start: m -= 1
    if m > G:
        break
    r = run / m
    if r > best_all[0]:
        best_all = (r, start, int(q2) - 1, m)
    if m >= 100 and r > best_100[0]:
        best_100 = (r, start, int(q2) - 1, m)
blank = [m for m in range(2, G + 1) if not ISG[T(m - 1) + 1:T(m) + 1].any()]
print(f"[6] layers 2..{G:,} with no prime: {blank if blank else 'none'}")
print(f"    longest composite run vs its layer's width: {best_all[1]}..{best_all[2]} on layer {best_all[3]} ({best_all[0]:.0%})")
print(f"    from layer 100 on, the worst is {best_100[1]}..{best_100[2]} on layer {best_100[3]} ({best_100[0]:.1%})")
