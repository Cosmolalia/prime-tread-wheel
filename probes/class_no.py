#!/usr/bin/env python3
"""
class_no.py — exact class numbers of the census's champion discriminants by
counting reduced primitive positive-definite binary quadratic forms.
For D < 0: count triples (a,b,c), b^2-4ac = D, gcd(a,b,c)=1,
|b| <= a <= c, and if |b|=a or a=c then b >= 0.
"""
from math import isqrt, gcd

def class_number(D):
    assert D < 0 and D % 4 in (0, 1), f"{D} not a discriminant"
    h, a = 0, 1
    while 4 * a * a <= -D + a * a:          # |b|<=a and b^2=D+4ac>=D+4a^2... bound a <= sqrt(-D/3)
        a += 1
    for aa in range(1, isqrt(-D // 3) + 2):
        for b in range(-aa, aa + 1):
            if (b * b - D) % (4 * aa) != 0:
                continue
            cc = (b * b - D) // (4 * aa)
            if cc < aa:
                continue
            if abs(b) == aa and b < 0:
                continue
            if aa == cc and b < 0:
                continue
            if gcd(gcd(aa, abs(b)), cc) != 1:
                continue
            h += 1
    return h

for D in [-3, -4, -7, -8, -11, -15, -19, -27, -28, -43, -67, -163, -267, -652, -232, -148, -928, -123]:
    print(f"h({D:5}) = {class_number(D)}")
