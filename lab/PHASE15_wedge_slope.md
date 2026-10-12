# PHASE 15 — wedge slope decomposition: why d ~ m/13.5

Date: 2026-10-12 (morning, autonomous block). Artifacts:
`lab/PHASE15_wedge_slope.py` (+ `.json`), `lab/PHASE15_dynrings.py`
(+ `.json`, `.log` — LEG N detached, pickup pending).

Answers the queue item "why ~m/13.5" (GPT's CRT-Hamming frame) at the
level of mechanism, contingent on the ring bound B.

## Part 1 — two-load decomposition on the measured curve [S→fit]

Object A, 25 fixed rings (primes ≤ 97), all 244 finite layers 14..257
(PHASE14 objA d-curve). Predictors computed exactly (no sampling):

- P(m) = #{j : T(m−1)+j prime} (prime-value ticks)
- U(m) = #{j : T(m−1)+j has **no** prime factor ≤ 97} (home-uncoverable
  "rough" ticks; density → e^(−γ)/ln 97 ≈ 0.123)

Results (frozen predictions H1–H6 in the probe header):

| model | fit | r | R² |
|---|---|---|---|
| d ~ κ·P | κ=0.779, b=−0.60 | 0.950 | 0.902 |
| d ~ κ·U | κ=0.649, b=+0.40 | 0.972 | 0.945 |
| d ~ a·U + c·m | **a=0.215, c=0.051** | — | **0.974** |
| d ~ s·m (reference) | s=0.0747 | — | 0.967 |

Verdicts: H1 FAIL (0.950 < 0.98), H2 PASS, H3 PASS for the combined
model (beats m-linear), H6 PASS with the corrected roughness predicate,
H5 PASS (m=55 unremarkable under the counting model: d=5 vs pred 4.85),
H4 FAIL as stated — object C's d is parity-dominated (GLM's parity wedge
theorem: one ring-2 flip covers the whole prime parity class), so prime
count alone is the wrong predictor there; κ_C = 0.37, r = 0.65.

**Mechanism reading [S]**: displacement carries two loads —
(i) harvesting home-uncoverable rough ticks (~⅓ of the slope; one
displaced ring covers several rough ticks via mod-p collisions, net
0.215 rings per rough tick after accounting for the collateral it does),
and (ii) re-covering composite ticks whose home coverage was destroyed by
displacements (~⅔ of the slope, ~0.051 per tick).

**The 1/13.5 arithmetic**: 0.215·(e^(−γ)/ln 97) + 0.051 ≈ 0.0264 + 0.051
= 0.077 ≈ 1/13.0 against measured 1/13.4 — the constant is not free; it is
set by the ring bound B through U's density. Consequence [F]: the slope
must depend on B, and under the native schedule (rings = primes ≤
√T(m−1)), every composite value is home-covered, U collapses to P(m) ~
m/(2 ln m), so d should grow **sublinearly**. That is LEG N.

## Implementation note (house rule: bugs filed, not hidden)

The first U implementation tested 97-**smoothness** (all factors ≤ 97)
instead of "has a factor ≤ 97"; density sanity check caught it (0.89 vs
the true 0.123). Corrected in place; the fit constants above are the
corrected ones.

## Part 2 — LEG S (fixed-B sensitivity), complete

Frozen predictions: d(m;B) ≈ 0.215·U_B(m) + 0.051·m + 0.35 with
U_B density e^(−γ)/ln B; None allowed where m ≥ h(#B) (Jacobsthal).

| key | d | U_B | pred | status |
|---|---|---|---|---|
| B=31, m=60 | None | 7 | 4.91 | infeasible (HiGHS 8) |
| B=31, m=100 | None | 16 | 8.89 | infeasible |
| B=31, m=150 | None | 22 | 12.73 | infeasible |
| B=53, m=60 | 7 | 7 | 4.91 | optimal |
| B=53, m=100 | 11 | 15 | 8.67 | optimal |
| B=53, m=150 | None | — | — | infeasible |

Reading: (a) j(31#) ≤ 60 — the 11-ring wheel cannot cover 60 consecutive
ticks at any displacement; this is a new Jacobsthal bracket
(j(31#) ≤ 60; published tables put it lower — reconcile against OEIS
A048670 before citing a value). (b) 100 < j(53#) ≤ 150. (c) The two B=53
finite points sit **above** the B=97-constant prediction by a consistent
+2.2: fewer rings → less collision freedom → higher per-rough-tick cost.
Consistent with the mechanism; the constants are B-dependent [S], as the
theory requires. Small n; no refit claimed.

## Part 2 — LEG N (native rings), pending pickup

m ∈ {263, 300, 400, 600, 1000}, rings = primes ≤ √T(m−1). First result:
**N_m263: d=15, P=28, nrings=42 (27.6s) — d/P = 0.54**, BELOW the
harvest-only band (0.65·28 = 18.2): with more rings, displaced rings
harvest rough ticks more efficiently. N1/N2/N3 adjudication at pickup.
