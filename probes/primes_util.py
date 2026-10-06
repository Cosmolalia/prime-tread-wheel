"""Shared helpers: a sieve and a deterministic primality test (exact for all 64-bit numbers). Needs only numpy."""
import numpy as np

def sieve(n):
    """is_prime[0..n] as a boolean numpy array."""
    s = np.ones(n + 1, dtype=bool); s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = False
    return s

def is_prime(n):
    """Deterministic Miller-Rabin, exact for n < 3.3e24 (covers every 64-bit number)."""
    if n < 2: return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
    for p in small:
        if n % p == 0: return n == p
    d, r = n - 1, 0
    while d % 2 == 0: d //= 2; r += 1
    for a in small:
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1: break
        else:
            return False
    return True

def primes_up_to(n):
    return np.nonzero(sieve(n))[0].tolist()
