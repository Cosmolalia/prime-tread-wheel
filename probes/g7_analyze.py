#!/usr/bin/env python3
"""Analysis for G7 halves 1M probe."""
import csv, math
import numpy as np
from scipy import stats

CSV = "/home/solaya/Desktop/TOE/harness/data/projects/prime-tread-wheel/lab/g7_halves_1m.csv"

ms, WL, WR, V = [], [], [], []
with open(CVSV if False else CSV) as f:
    r = csv.reader(f)
    next(r)
    for row in r:
        ms.append(int(row[0])); WL.append(int(row[1]))
        WR.append(int(row[2])); V.append(int(row[3]))
m = np.array(ms); wl = np.array(WL); wr = np.array(WR); v = np.array(V)
print(f"laps: {len(m)}  ({m.min()}..{m.max()})")
print(f"VIOLATIONS: {v.sum()}")

def q(x, name):
    print(f"{name}: median={np.median(x):.0f} mean={x.mean():.2f} "
          f"p99={np.percentile(x,99):.0f} p999={np.percentile(x,99.9):.0f} max={x.max()}")
    return x.max()
q(wl, "W_L"); q(wr, "W_R")

ks = stats.ks_2samp(wl, wr)
print(f"KS test W_L vs W_R: stat={ks.statistic:.5f} p={ks.pvalue:.4f}")
mw = stats.mannwhitneyu(wl, wr)
print(f"Mann-Whitney W_L vs W_R: stat={mw.statistic:.0f} p={mw.pvalue:.4f}")
print(f"means: L={wl.mean():.4f} R={wr.mean():.4f}  medians: L={np.median(wl):.0f} R={np.median(wr):.0f}")

pear = stats.pearsonr(wl, wr)
spear = stats.spearmanr(wl, wr)
print(f"lap-level Pearson corr(W_L,W_R) = {pear.statistic:.5f} (p={pear.pvalue:.3g})")
print(f"lap-level Spearman corr(W_L,W_R) = {spear.statistic:.5f} (p={spear.pvalue:.3g})")

# margin growth: log2 bins of m
print("\nbinned worst-margin trend:")
print("bin_lo  bin_hi   n    max_W  ln2(N)fit_pred/scale")
edges = np.unique(np.round(np.logspace(math.log10(21), 6, 25)).astype(int))
edges = np.concatenate([[20], edges, [m.max()]])
wmax_all = np.maximum(wl, wr)
for i in range(len(edges)-1):
    lo, hi = edges[i], edges[i+1]
    sel = (m > lo) & (m <= hi)
    if sel.sum() < 2: continue
    Nmed = (hi*(hi-1)//2 + hi//2)  # ~ window center value at bin top
    print(f"{lo:>7} {hi:>7} {sel.sum():>6} {wmax_all[sel].max():>6}")

# fit max W per bin vs ln(N): is it ~ c*ln N or faster?
# binned regression on log(maxW) vs log(ln N)
xs, ys = [], []
for i in range(len(edges)-1):
    lo, hi = edges[i], edges[i+1]
    sel = (m > lo) & (m <= hi)
    if sel.sum() < 100: continue
    N = hi*(hi-1)//2
    xs.append(math.log(math.log(N))); ys.append(math.log(wmax_all[sel].max()))
slope, intercept, r, p, se = stats.linregress(xs, ys)
print(f"\nlog(maxW) vs log(ln N): slope={slope:.3f} (1.0 => linear in ln N; "
      f"2.0 => Cramer ln^2)  R^2={r*r:.3f}")

# danger scan: margin-to-midpoint per half
H = m // 2
margL = H - wl - 1            # distance from nearest left-half prime tick to midpoint tick H
margR = (m - wr) - H - 1      # distance from nearest right-half prime tick to midpoint tick H+1
marg = np.minimum(margL, margR)
order = np.argsort(marg)[:15]
print("\ntop-15 closest calls (smallest margin-to-midpoint):")
print("rank   m    H   W_L  W_R  margL  margR  min_margin")
for rank, idx in enumerate(order, 1):
    print(f"{rank:>4} {m[idx]:>6} {H[idx]:>5} {wl[idx]:>4} {wr[idx]:>4} "
          f"{margL[idx]:>5} {margR[idx]:>5} {marg[idx]:>10}")
print(f"\nmin margin overall: {marg.min()} at m={m[marg.argmin()]}")
print(f"margin quantiles: p1={np.percentile(marg,1):.0f} p0.1={np.percentile(marg,0.1):.0f}")

# parity split sanity (windows at odd/even base)
base = m*(m-1)//2
print("\nparity of T(m-1): odd-base laps:", (base % 2 == 1).sum(), " even-base:", (base % 2 == 0).sum())
wl_odd, wl_even = wl[base%2==1], wl[base%2==0]
wr_odd, wr_even = wr[base%2==1], wr[base%2==0]
print(f"W_L mean odd-base={wl_odd.mean():.3f} even-base={wl_even.mean():.3f}")
print(f"W_R mean odd-base={wr_odd.mean():.3f} even-base={wr_even.mean():.3f}")

# global extremes
print(f"\nmax W_L={wl.max()} at m={m[wl.argmax()]}; max W_R={wr.max()} at m={m[wr.argmax()]}")
# top margins by max(W)
topw = np.argsort(-wmax_all)[:10]
print("top-10 largest max(W_L,W_R):")
for idx in topw:
    print(f"  m={m[idx]} W_L={wl[idx]} W_R={wr[idx]} max={wmax_all[idx]}")
