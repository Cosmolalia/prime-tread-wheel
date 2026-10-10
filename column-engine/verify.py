# Check a colsieve output against deterministic Miller-Rabin (13 prime bases: exact below 3.3e24).
import sys, random
def mr(n):
    if n < 2: return False
    for q in (2,3,5,7,11,13,17,19,23,29,31,37,41):
        if n % q == 0: return n == q
    d, s = n-1, 0
    while d % 2 == 0: d//=2; s+=1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37,41):
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(s-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True
side, kj, m0, L, path = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
sample = int(sys.argv[6]) if len(sys.argv) > 6 else 0
N = (lambda m: (m*m-m)//2 + kj) if side == 'start' else (lambda m: (m*m+m)//2 - kj)
listed = {}
for line in open(path):
    m, n = line.split(); listed[int(m)] = int(n)
assert all(N(m) == n for m, n in listed.items()), "value formula mismatch"
ms = range(m0, m0+L) if not sample else sorted(set(random.Random(1).sample(range(m0, m0+L), sample)) | set(list(listed)[:sample]))
bad = [m for m in ms if mr(N(m)) != (m in listed)]
print(f"checked {len(ms)} layers ({len(listed)} listed primes): mismatches {len(bad)}", bad[:5])
