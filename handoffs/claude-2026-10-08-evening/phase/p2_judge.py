"""Judge P2 by the criteria written down before the run (notes/insights.md):
(a) every column's measured boost within 3% of its gear-rule constant;
(b) measured order matches gear-rule order for every pair whose constants differ by more than 4 combined standard errors.
Also prints the plain full order and the boost per decade of layers."""
import json, math, itertools

rows = []
for f in ("p2_a.jsonl", "p2_b.jsonl"):
    for line in open(f):
        if line.strip():
            rows.append(json.loads(line))
rows.sort(key=lambda r: -r["C"])
for r in rows:
    r["se"] = r["boost"] / math.sqrt(r["primes"])
    r["dev"] = (r["boost"] - r["C"]) / r["C"]
    r["z"] = (r["boost"] - r["C"]) / r["se"]
    r["dec"] = [p / ch if ch else None for p, ch in r["buckets"]]

print(f"{'c':>5} {'disc':>7} {'gear rule':>9} {'measured':>9} {'off by':>8} {'z':>6} {'primes':>11}   by decade (1e5-1e6, 1e6-1e7, 1e7-1e8)")
for r in rows:
    dec = "  ".join(f"{d:.4f}" for d in r["dec"])
    print(f"{r['c']:>5} {r['D']:>7} {r['C']:>9.4f} {r['boost']:>9.4f} {r['dev']:>+8.3%} {r['z']:>+6.2f} {r['primes']:>11,}   {dec}")

a_ok = all(abs(r["dev"]) <= 0.03 for r in rows)
worst = max(rows, key=lambda r: abs(r["dev"]))
print(f"\n(a) every column within 3%: {a_ok}  (worst: c={worst['c']} off by {worst['dev']:+.3%})")

pairs = resolvable = flips = 0
flipped = []
for x, y in itertools.combinations(rows, 2):
    pairs += 1
    gap = abs(x["C"] - y["C"]); se = math.hypot(x["se"], y["se"])
    if gap > 4 * se:
        resolvable += 1
        if (x["boost"] - y["boost"]) * (x["C"] - y["C"]) <= 0:
            flips += 1; flipped.append((x["c"], y["c"]))
print(f"(b) pairs: {pairs}; resolvable (constants > 4 SE apart): {resolvable}; out of order among those: {flips} {flipped}")

pred = [r["c"] for r in rows]
meas = [r["c"] for r in sorted(rows, key=lambda r: -r["boost"])]
inv = [(x["c"], y["c"]) for x, y in itertools.combinations(rows, 2) if (x["boost"] - y["boost"]) * (x["C"] - y["C"]) <= 0]
print("gear-rule order:", pred)
print("measured order: ", meas)
print("all swapped pairs (any size):", inv)
for x, y in inv:
    rx = next(r for r in rows if r["c"] == x); ry = next(r for r in rows if r["c"] == y)
    print(f"   {x} vs {y}: constants {rx['C']:.4f} vs {ry['C']:.4f} (gap {abs(rx['C']-ry['C']):.4f}, {abs(rx['C']-ry['C'])/math.hypot(rx['se'], ry['se']):.1f} SE)")
chi2 = sum(r["z"] ** 2 for r in rows)
print(f"sum of z^2 over {len(rows)} columns: {chi2:.1f} (pure noise would give about {len(rows)})")
json.dump({"rows": rows, "a_ok": a_ok, "resolvable": resolvable, "flips": flipped, "swapped_any": inv, "chi2": chi2},
          open("p2_result.json", "w"), indent=1)
