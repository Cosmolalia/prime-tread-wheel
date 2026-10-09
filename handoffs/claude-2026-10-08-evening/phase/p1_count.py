"""P1 check: count spokes (b odd <= B, gcd(a,b)=1) whose first shot T(b-1)+a and second shot 2*x1 + b^2 are both prime."""
import json, sys
import numpy as np
from primes_util import sieve
B = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
T = lambda m: m * (m + 1) // 2
IS = sieve(2 * T(B) + B * B + 10)
count = 0
for b in range(3, B + 1, 2):
    a = np.arange(1, b + 1, dtype=np.int64)
    a = a[np.gcd(a, b) == 1]
    x1 = T(b - 1) + a
    x2 = 2 * x1 + b * b
    count += int((IS[x1] & IS[x2]).sum())
pred = json.load(open(f"p1_pred_{B}.json"))["pred"]
print(f"B={B}: actual {count}, predicted {pred:.0f}, actual/predicted = {count/pred:.4f}")
json.dump({"B": B, "pred": pred, "actual": count}, open(f"p1_result_{B}.json", "w"))
