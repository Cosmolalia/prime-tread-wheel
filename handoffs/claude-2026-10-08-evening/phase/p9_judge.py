"""Judge P9 against the calls written down before the run (notes/insights.md, 13:55 UTC Oct 8)."""
import json, math, sys
import numpy as np

rows = []
for f in sys.argv[1:] or ["p9_a.jsonl", "p9_b.jsonl"]:
    for line in open(f):
        if line.strip():
            rows.append(json.loads(line))
n = len(rows)
W = [r[0] for r in rows[0]["rungs"]]
# pooled ratio per rung and stream: sum of squared misses / sum of coin-flip variance
def pooled(sel=lambda r: True):
    out = {}
    for t, name in enumerate(("real", "coin", "sched")):
        out[name] = []
        for L in range(len(W)):
            num = sum(r["rungs"][L][2 + t] for r in rows if sel(r))
            den = sum(r["rungs"][L][5] for r in rows if sel(r))
            out[name].append(num / den)
    return out
R = pooled()
nwin = [sum(r["rungs"][L][1] for r in rows) for L in range(len(W))]
print(f"{n} lanes (c = {min(r['c'] for r in rows)}..{max(r['c'] for r in rows)})")
print(f"{'window':>12} {'windows':>9} {'real':>7} {'coin':>7} {'sched<=1000':>12}")
for L, w in enumerate(W):
    print(f"{w:>12,} {nwin[L]:>9,} {R['real'][L]:>7.3f} {R['coin'][L]:>7.3f} {R['sched'][L]:>12.3f}")

real, coin, sched = R["real"], R["coin"], R["sched"]
a = real[-1] < 0.6
b_steps = [real[i + 1] < real[i] for i in range(5)]          # 1e2 -> 1e7, five steps
b = all(b_steps) and real[0] >= 0.8
x = np.log10(np.array(W[:6], dtype=float)); y = np.array(real[:6])
k, c0 = np.polyfit(x, y, 1)
res = y - (k * x + c0)
c = (np.abs(res).max() <= 0.05) and (0.04 <= -k <= 0.10)
d_coin = all(0.8 <= v <= 1.2 for v in coin)
d_sched = sched[-1] < 0.85
d = d_coin and d_sched
print(f"\n(a) whole run R = {real[-1]:.3f} < 0.6: {a}")
print(f"(b) falls at every x10 step 1e2..1e7: {b_steps}; R(100) = {real[0]:.3f} >= 0.8: {real[0] >= 0.8}  -> {b}")
print(f"(c) line through 1e2..1e7: drop per x10 = {-k:.4f} (0.04..0.10), worst miss {np.abs(res).max():.4f} (<= 0.05): {c}")
print(f"    line predicts at 1e8: {k * 8 + c0:.3f} (measured {real[-1]:.3f})")
print(f"(d) coin flips within 0.8..1.2 at every rung: {d_coin} {['%.3f' % v for v in coin]}; schedule<=1000 whole run {sched[-1]:.3f} < 0.85: {d_sched} -> {d}")
print(f"ALL FOUR: {a and b and c and d}")

# exploratory (not pre-registered): rich vs poor lanes
Cs = sorted(r["C"] for r in rows); med = Cs[n // 2]
for lab, sel in (("richer half", lambda r: r["C"] >= med), ("poorer half", lambda r: r["C"] < med)):
    Rs = pooled(sel)
    print(f"[explore] {lab}: real by rung {['%.3f' % v for v in Rs['real']]}")
# per-lane whole-run misses in coin-flip units (one number per lane)
z = np.array([(r["real"] - r["e"]) / math.sqrt(r["v"]) for r in rows])
print(f"[explore] whole-run misses per lane in coin-flip units: rms {np.sqrt((z ** 2).mean()):.3f}, mean {z.mean():+.3f}, "
      f"share within 1: {(np.abs(z) < 1).mean():.0%} (coin flips: 68%)")
json.dump({"lanes": n, "W": W, "R": R, "line": {"drop_per_x10": -k, "max_miss": float(np.abs(res).max())},
           "a": a, "b": b, "c": bool(c), "d": d, "z_rms": float(np.sqrt((z ** 2).mean())), "z_mean": float(z.mean())},
          open("p9_result.json", "w"), indent=1)
