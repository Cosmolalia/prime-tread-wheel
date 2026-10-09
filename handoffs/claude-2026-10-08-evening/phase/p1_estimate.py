"""P1 estimate only (no counting): spokes a/b, b odd <= B, gcd(a,b)=1.
First shot x1 = T(b-1)+a, second shot x2 = 2*x1 + b^2. Both prime: expected count from the gear rule:
  2 * C2 * prod_{p | b, p odd} p/(p-2) * sum over a of 1/(ln x1 * ln x2)."""
import math, json, sys
from math import gcd, log
C2 = 0.6601618158468696
B = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
def odd_prime_factors(n):
    f, p = [], 3
    while n % 2 == 0: n //= 2
    while p * p <= n:
        if n % p == 0:
            f.append(p)
            while n % p == 0: n //= p
        p += 2
    if n > 1: f.append(n)
    return f
total = 0.0
for b in range(3, B + 1, 2):
    fac = 1.0
    for p in odd_prime_factors(b): fac *= p / (p - 2)
    T = b * (b - 1) // 2
    s = 0.0
    for a in range(1, b + 1):
        if gcd(a, b) == 1:
            x1 = T + a
            s += 1.0 / (log(x1) * log(2 * x1 + b * b))
    total += 2 * C2 * fac * s
print(f"B={B}: predicted spokes with both shots prime = {total:.0f}")
json.dump({"B": B, "pred": total}, open(f"p1_pred_{B}.json", "w"))
