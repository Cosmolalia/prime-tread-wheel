# FORMALIZATION_STATUS — Prime Tread Wheel, "does it pass Lean" audit

**Date:** 2026-11-14 (third pass — §18.9 dual identity, §18.11 rotor tuning, §18.12 CRT fiber count added; surface remains CLOSED)
**Repo:** `lean_wheel/` — Lean 4.35.0 (`leanprover/lean4:v4.35.0`) + mathlib `v4.35.0` (precompiled cache, not built from source).
**Build:** `cd lean_wheel && lake build` — **Build completed successfully (9069 jobs).**
**Axiom audit:** every theorem below was `#print axioms`-checked (script: `PrintAxioms.lean`, run `lake env lean PrintAxioms.lean`): **83 theorems, all footprints ⊆ [propext, Classical.choice, Quot.sound]** (the acceptable mathlib trio; 73 use the full trio, 10 subsets). **No `sorry` anywhere in any compiled file.**

Conventions: `Wheel.T (n : ℕ) = n*(n+1)/2`, `Wheel.TZ (n : ℤ) = n*(n+1)/2`. All divisions are justified by exactness lemmas `Wheel.two_mul_T` / `Wheel.two_mul_TZ` (`2·T n = n(n+1)`, proved from evenness of `n(n+1)`), so the paper's `/2` is never hand-waved.

---

## 1. Theorem inventory (all GREEN)

### Item 1 — B7 mirror lift (`LeanWheel/B7.lean`)
| Lean name | Statement (paper) | Axioms |
|---|---|---|
| `Wheel.T_pred_add_T` | `1 ≤ m → T(m−1) + T(m) = m²` | propext, choice, Quot.sound |
| `Wheel.mirror_sum` | `1 ≤ k < m → (T(m−1)+k) + (T(m−1)+(m−k)) = m²` (interior value pairing) | idem |
| `Wheel.mirror_endpoint` | `m² − T(m) = T(m−1)` (endpoint exchange across layers) | idem |
| `Wheel.mirror_gcd` | `k ≤ m → gcd k m = gcd (m−k) m` (eligibility incl. gcd=2 escape) | propext, Quot.sound |
| `Wheel.mirror_zmod` | `k ≤ m → −(k : ZMod m) = ((m−k : ℕ) : ZMod m)` | idem |
| `Wheel.mirrorEquiv` + `Wheel.mirrorEquiv_involutive` | the tick involution is a self-inverse bijection (`ZMod m ≃ ZMod m`, `x ↦ −x`) | — (defs) |
| `Wheel.no_mirror_prime_pair_odd` | `m ≥ 3`, `m` odd → no interior mirror pair is prime×prime | propext, choice, Quot.sound |

Scoping: see **D2** — the involution is exact on cyclic ticks; on the linear set {1..m} the map k ↦ m−k sends m to 0, and the two endpoint values pair *across* layers (`mirror_endpoint`).

### Item 2 — B3 triangular-offset (`LeanWheel/B3.lean`)
| Lean name | Statement | Axioms |
|---|---|---|
| `Wheel.B3` | `2·(TZ(m−1) + m − c) = (m−j)(m+j+1) ↔ 2c = j(j+1)` over ℤ, **unconditionally in m, j, c** | propext, choice, Quot.sound |
| `Wheel.B3_forward` | `2·(TZ(m−1) + m − TZ j) = (m−j)(m+j+1)` (the c = T(j) factorization) | idem |

No side conditions needed; the equivalence is exact over ℤ (the `/2` in the paper's prose is carried as `2·` throughout).

### Item 3 — B4 forced-composite endpoints (`LeanWheel/B4.lean`)
| Lean name | Statement | Axioms |
|---|---|---|
| `Wheel.B4_first` | `m ≥ 3 → ¬ (T m).Prime` | propext, choice, Quot.sound |
| `Wheel.B4_second` | `m ≥ 4 → ¬ (T m − 1).Prime` | idem |
| `Wheel.two_mul_T_sub_one` | `m ≥ 1 → 2·(T m − 1) = (m−1)(m+2)` (the paper's second identity) | idem |

"Composite" = ≥ 2 and not prime (witness divisor exhibited in each parity case). `¬ Prime` is the faithful reading; the numbers are ≥ 6 / ≥ 9 so this coincides with the standard "composite" predicate.

### Item 4 — Theorem I part 1, bijection (`LeanWheel/Bijection.lean`)
| Lean name | Statement | Axioms |
|---|---|---|
| `Wheel.exists_coord` | `1 ≤ N → ∃ m k, 1 ≤ k ∧ k ≤ m ∧ T(m−1) + k = N` (strong induction, peeling the last tick) | propext, choice, Quot.sound |
| `Wheel.unique_coord` | the layer sandwich `T(m−1) < N ≤ T m` forces `(m₁,k₁) = (m₂,k₂)` | idem |
| `Wheel.theoremI_bijection` | `1 ≤ N → ∃! mk : ℕ×ℕ, 1 ≤ mk.2 ∧ mk.2 ≤ mk.1 ∧ T(mk.1−1) + mk.2 = N` | idem |

### Item 5 — Theorem I part 2, ratio-slip recurrence (`LeanWheel/RatioSlip.lean`)
| Lean name | Statement | Axioms |
|---|---|---|
| `Wheel.o` | `o p m := −(T(m−1) : ZMod p)` — the stagger field | — (def) |
| `Wheel.o_succ` | `o p (m+1) = o p m − (m : ZMod p)` for all m | propext, choice, Quot.sound |
| `Wheel.dvd_iff_eq_o` | `1 ≤ p → (p ∣ T(m−1)+k ↔ (k : ZMod p) = o p m)` | idem |

### Item 6 — Theorem I part 3, exact primality criterion (`LeanWheel/Primality.lean`)
| Lean name | Statement | Axioms |
|---|---|---|
| `Wheel.exists_prime_le_sqrt_of_not_prime` | bridge: `2 ≤ N → ¬ N.Prime → ∃ p, p.Prime ∧ p ∣ N ∧ p ≤ √N` | propext, choice, Quot.sound |
| `Wheel.theoremI_criterion` | `1 ≤ k → k ≤ m → N = T(m−1)+k → ⌊√(T m)⌋ < N → (N.Prime ↔ ∀ p, p.Prime → p ≤ ⌊√(T m)⌋ → ¬ p ∣ N)` | idem |

The hypothesis `⌊√(T m)⌋ < N` forces `m ≥ 2` and `N ≥ 2` (handled inside the proof; no content lost).

### Item 7 — Three-Primitive Theorem, the flagship (`LeanWheel/ThreePrimitive.lean`)
Primitives (`Wheel.P1`…`Wheel.P5`): P1 `B 1 = 0 ∧ ∀ m, B(m+1) − B m = L m`; P2 `∃ a b, ∀ m, L m = a·m + b`; P3 `∀ m, L(m+1) − L m = 1`; P4 `∀ m ≥ 1, Odd m → ∀ q ≥ 1, q ∣ m → (q:ℤ) ∣ B m`; P5 via `Wheel.Bext L x := TZ(x−1) + (L 1 − 1)·(x−1)` (the polynomial extension, well-defined under P1∧P3): `∀ m : ℤ, Bext L m = Bext L (1−m)`.

| Lean name | Statement | Axioms |
|---|---|---|
| `Wheel.telescope_L` | P3 → `L(m+1) = L 1 + m` | propext, choice, Quot.sound |
| `Wheel.P3_implies_P2` | P3 → P2 (redundancy) | idem |
| `Wheel.formula_B` | P1∧P3 → `∀ m ≥ 1, B m = TZ(m−1) + b·(m−1)` with `b = L 1 − 1` | idem |
| `Wheel.int_dvd_TZ_pred_of_odd` | `m` odd → `(m : ℤ) ∣ TZ(m−1)` | idem |
| `Wheel.isCoprime_int_self_sub_one` | `IsCoprime (m : ℤ) ((m:ℤ) − 1)` (Bezout) | idem |
| `Wheel.int_self_dvd_of_dvd_mul_pred` | Euclid step: `m ∣ b·(m−1) → m ∣ b` | idem |
| `Wheel.three_primitive_P4` | **(P1 ∧ P3 ∧ P4) → `L 1 − 1 = 0 ∧ ∀ m ≥ 1, B m = TZ(m−1)`** | idem |
| `Wheel.Bext_gap` | `Bext L m − Bext L (1−m) = (L 1 − 1)·(2m−1)` | idem |
| `Wheel.three_primitive_P5` | **(P1 ∧ P3 ∧ P5) → same conclusion** | idem |
| `Wheel.P4_iff_P5_of_P1_P3` | given P1∧P3, P4 ↔ P5 | idem |

Mechanism verified exactly as the paper sketches: P4 at odd m with q = m gives `m ∣ TZ(m−1) + b(m−1)`, and `m ∣ TZ(m−1)` (odd m) leaves `m ∣ b·(m−1)`; `gcd(m, m−1) = 1` forces `m ∣ b`; the odd `M = 2|b|+3 > |b|` gives `b = 0`. **D1** below: the "single odd m" phrasing in the paper is compressed; the universal quantifier is load-bearing.

Independence witnesses (each a one-line check, all kernel-verified):

| Witness | Lean content | Axioms |
|---|---|---|
| (i) `Bw1 m = TZ(m−1)+(m−1)`, `Lw1 m = m+1` | `witness1_P1`, `witness1_P3` ✓; `witness1_not_P4` (fails at m=3: B 3 = 5); `witness1_not_P5` | subsets of the trio |
| (ii) `Bw2 m = m(m−1)`, `Lw2 m = 2m` | `witness2_P1`, `witness2_P4` ✓; `witness2_P3` ✗; **literal palindrome** `witness2_palindrome` (`x(x−1)` at 1−x) + `witness2_extension_agrees`; **under the P1∧P3-relative extension it fails P5**: `witness2_not_P5` — see **D3** | subsets |
| (iii) `Bw3 m = TZ(m−1)+1`, `Lw3 m = m` | `witness3_P3`, `witness3_P5` ✓; `witness3_not_P1` (B 1 = 1 ≠ 0); `witness3_not_P4` (at m=3: B 3 = 4, 3 ∤ 4) | subsets |
| (iii-b) `Bw3b ≡ 0`, `Lw3b m = m` (paper's alternative decoupled family) | `witness3b_P3`, `witness3b_P4`, zero-polynomial palindrome `the trivial palindrome lemma` ✓; contiguity fails at m=1: `witness3b_not_contiguous` — under `Bext` it fails P5 (D3) | subsets |

### Item 8 — Theorem II part 1, orphan characterization (`LeanWheel/Orphan.lean`)
| Lean name | Statement | Axioms |
|---|---|---|
| `Wheel.Bm` | `Bm m := ⌊√(T(m−1))⌋` | — (def) |
| `Wheel.Tm_lt_two_mul_Bm_add_one_sq` | `m ≥ 3 → T(m) < 2(Bm m + 1)²` (the GPT-audited repaired hypothesis — **proved**, not assumed) | propext, choice, Quot.sound |
| `Wheel.minFac_sq_le_of_not_prime` | `2 ≤ N → ¬N.Prime → minFac(N)² ≤ N` | idem |
| `Wheel.orphan_characterization` | hypotheses (`p.Prime`, `p ≤ B`, `p ∣ N`, `N ≤ T m`, uniqueness among primes ≤ B) → `∃ a ≥ 1, N = p^a ∨ ∃ Q, N = p^a·Q ∧ Q.Prime ∧ B < Q` | idem |

Mechanism forced through the kernel: `N = p^a·Q`, `p ∤ Q`; if `Q ≥ 2` composite, `minFac(Q) > B` (uniqueness), so `(B+1)² ≤ minFac(Q)² ≤ Q ≤ N/p ≤ T(m)/2 < (B+1)²` — contradiction. Hence `Q = 1` or `Q` prime `> B`.

### Item 9 — Theorem III, disjoint-union conservation (`LeanWheel/Conservation.lean`, Finset over `Icc 1 m`)
| Lean name | Statement | Axioms |
|---|---|---|
| `Wheel.rings` / `Wheel.F` / `Wheel.stratum` | rings = primes ≤ B; `F(k)` = factor bundle; `C_E` = exact-support stratum | — (defs) |
| `Wheel.strata_disjoint_of_ne` | `E₁ ≠ E₂ → Disjoint (C_{E₁}) (C_{E₂})` | propext, choice, Quot.sound |
| `Wheel.strata_cover` | `Icc 1 m = ⨆_{E ⊆ rings} C_E` (biUnion over the powerset) | idem |
| `Wheel.strata_union_over_subsets` | for `S ⊆ rings B`: ticks with `F(k) ⊆ S` = `⨆_{E ⊆ S} C_E` | idem |
| `Wheel.loses_all_home_covers_iff` | ` (∀ p ∈ F(k), p ∈ S) ↔ F(k) ⊆ S` | propext |

### Item 10 — Theorem IV, LP smear arithmetic (`LeanWheel/Smear.lean`, over ℚ)
| Lean name | Statement | Axioms |
|---|---|---|
| `Wheel.α` / `Wheel.smearTerm` | `α₂ = α₃ = 1, α₅ = 5/6`; term = `if p ∣ N then 1 − (p−1)·α_p/p else α_p/p` | — (defs) |
| `Wheel.smear_coverage` | `1 ≤ Σ_{p ∈ {2,3,5}} smearTerm p N` for every `N` | propext, choice, Quot.sound |
| `Wheel.smear_coverage_eq_one_iff` | `Σ … = 1 ↔ ¬ 5 ∣ N` (strengthening; each of the 8 divisibility patterns computed) | idem |
| `Wheel.smear_cost` | `(2−1)/2·1 + (3−1)/3·1 + (5−1)/5·(5/6) = 11/6` | idem |

Note the per-ring terms are constants (1/2, 1/3, and 1/6-or-1/3 for p = 5), so the "smear" is genuinely uniform across ticks.

### Item 11 — the break-even statement, break-even algebra (`LeanWheel/BreakEven.lean`, over ℝ)
| Lean name | Statement | Axioms |
|---|---|---|
| `Wheel.break_even_first` | `1 < p → (0 < (L − (p−1))/p ↔ p − 1 < L)` | propext, choice, Quot.sound |
| `Wheel.break_even_second` | `1 < p → (0 < (L − (p−1))/(p−1) ↔ p − 1 < L)` | idem |

The paper's warrant for the savings formulas is the equidistribution heuristic **[S]** — by design, only the conditional algebra is formalized here.

### Item 12 — B1, the visible set is exactly the primes (`LeanWheel/B1.lean`)
| Lean name | Statement (paper) | Axioms |
|---|---|---|
| `Wheel.sqrt_Tm_lt` | `2 ≤ m → Nat.sqrt (T m) < m` (the layer floor stays below m²) | propext, choice, Quot.sound |
| `Wheel.B1` | composite `N = T(m−1)+k` in the layer (`1 ≤ k ≤ m`, `2 ≤ N`) has a prime factor `p ≤ m` | idem |
| `Wheel.B1_rough` | prime layer value: no wheel prime `p ≤ m` divides it except itself | propext |

The paper's "the wheel at layer m is the √N sieve": the bridge `exists_prime_le_sqrt_of_not_prime` (item 6) gives `p ≤ √N ≤ √(T m)`, and `√(T m) < m`.

### Item 13 — B2 column law + B5 seat-zero (`LeanWheel/B2.lean`)
| Lean name | Statement (paper) | Axioms |
|---|---|---|
| `Wheel.T_pred_of_even` | `m` even → `T(m−1) = (m−1)·(m/2)` — parity of `T(m−1)` = parity of `m/2` | idem |
| `Wheel.column_law` | **B2**: `N = T(m−1)+k` prime → `gcd k m = 1 ∨ (gcd k m = 2 ∧ m % 4 = 2)` | idem |
| `Wheel.B5_seat_zero` | **B5**: `m % 4 = 2`, `6 ≤ m`, `N` prime in the layer → `gcd k m = 2` (coprime columns prime-free) | idem |

Mechanism kernel-certified: an odd prime `p ∣ gcd(k,m)` divides `T(m−1)` (since `p ∣ m`, `p` odd) and `k`, hence `N`; `p ≤ m` and the layer sandwich force `m ≤ 2`, then `p = N ≠ 2` contradicts. So the gcd is a power of 2; `4 ∣ m` makes `T(m−1)` and `k` both even, so `N` would be even `> 2` — excluded. The gcd divides `m = 4t+2`, so `gcd/2` divides the odd `2t+1`; any prime factor of `gcd/2` divides the gcd (hence is 2), but `gcd/2` is odd — so `gcd/2 = 1` and `gcd = 2`. The B6 "2.00×" density ratio itself is measured **[E]**; its formalizable kernel is exactly this parity conditioning (paper's own 2026-11-14 reframe).

### Item 14 — GLM lock+palindrome lemma (`LeanWheel/GLM.lean`)
Quadratic counts carried as the exact doubled identity `IsQuadCount B α β γ := ∀ m, 2·B m = αm²+βm+γ` (integrality built in).

| Lean name | Statement (paper §16.8) | Axioms |
|---|---|---|
| `Wheel.quad_gap` | `2·(B m − B(1−m)) = (α+β)·(2m−1)` | idem |
| `Wheel.glm_lock_iff_gamma` | seam lock `∀ odd m, ∀ q > 0, q ∣ m → q ∣ B m` ↔ `γ = 0` | idem |
| `Wheel.glm_palindrome_iff` | lap palindrome `∀ m, B m = B(1−m)` ↔ `α + β = 0` | idem |
| `Wheel.glm_unique` | lock + palindrome + 1:1 turn `B(m+1) − B m = m` → `α = 1 ∧ β = −1 ∧ γ = 0 ∧ B = T(·−1)` | idem |
| `Wheel.wheel_model` / `_lock` / `_palindrome` / `_turn` | the wheel `(1, −1, 0)` satisfies all three conditions — both iff's inhabited on both sides | idem |

Forward of the lock: `q := M = 2|γ|+3` odd gives `M ∣ γ`, hence `γ = 0`. Backward and the wheel model use the helper `int_odd_dvd_of_two_mul` (odd `q ∣ 2b → q ∣ b`) — the same mechanism as the Three-Primitive Theorem with the divisor `m` generalized to `2`.

### Item 15 — Theorem II part 3, the T(m)^{1/4} phase transition (`LeanWheel/PhaseTransition.lean`)
| Lean name | Statement (paper §19.2.3) | Axioms |
|---|---|---|
| `Wheel.phase_transition` | `T m < p²·(Bm m + 1)` → every `T(m−1)+k = p^a·Q` with `Q > Bm m` has `a = 1` | idem |
| `Wheel.pow_mul_Bm_lt_Tm` | same hypotheses → `p^a · Bm m < T m` (the paper's `p^a < T(m)/B` in nat-divided form) | idem |
| `Wheel.phase_transition_threshold_shape` | `T(m−1) < (Bm m + 1)²` (the `B ≈ √(T m)` shape behind the `T(m)^{1/4}` display) | idem |

The formalized threshold `p²·(B+1) > T(m)` is the **exact** kernel form: `Q ≥ B+1` gives `p^a·(B+1) ≤ p^a·Q ≤ T(m)`. The paper's displayed sufficient form `p² > T(m)/B` is slightly looser (a dated note could tighten it; zero mathematical content changes).

### Item 16 — Theorem III part 2, covering-capacity inequalities (`LeanWheel/Capacity.lean`)
| Lean name | Statement (paper §19.3, closing sentence) | Axioms |
|---|---|---|
| `Wheel.stripe` / `Wheel.stripe_card_le` | a rotated ring's class carries at most `⌈m/p⌉ = (m+p−1)/p` ticks (residue split: multiples of `p` ↔ `Icc 1 ⌈m/p⌉`, nonzero residues ↔ `range ⌈m/p⌉`; shared injectivity `injOn_stripe`) | idem |
| `Wheel.capacity_inequality` | coverage of `W(S)` by the rotated stripes ⟹ `|W(S)| ≤ Σ_p |stripe(p, c_p)|` | idem |
| `Wheel.capacity_inequality_family` | same for every downward-closed sub-family `W(T)`, `T ⊆ S`, with `Σ_p ⌈m/p⌉` | idem |
| `Wheel.uncovered_capacity` | in particular `|C_∅| = |U_0| ≤ Σ_{p∈S} ⌈m/p⌉` | idem |

Phases are residue classes in tick coordinates; the stagger-field transport `r ↦ r − T(m−1)` (a `ZMod p` bijection, Theorem I part 2) moves between the paper's value-phases and tick-phases, so the counting is shift-invariant. Coverage of `W(S)` is the *defining obligation* of a valid phase vector — stated as the hypothesis `hcover`, matching the paper's own framing (see D6).

### Item 17 — Theorem IV part 2, explicit LP relaxation point (`LeanWheel/LP.lean`, over ℚ)
| Lean name | Statement (paper §19.4) | Axioms |
|---|---|---|
| `Wheel.xSmear` / `Wheel.xSmear_row_le` | the exhibited point `x_{p,c} = α_p/p` on `{2,3,5} × {1,…,p−1}` satisfies every row bound `Σ_{c=1}^{p−1} x_{p,c} ≤ 1` | idem |
| `Wheel.xSmear_covers` | per tick `N`: coverage `= Σ_{p∈{2,3,5}} smearTerm p N ≥ 1` | idem |
| `Wheel.lp_relaxation_feasible` | the point is feasible for the continuous relaxation on **every** layer `m` | idem |

This closes the previously-"optional" enrichment: the finite LP (row bounds + per-tick coverage) is formally defined, and the exhibited point verifies every constraint. Objective value `11/6` was already `smear_cost`; the relaxation's optimum is therefore `≤ 11/6` (the paper's "11/6 = feasible point, not LP opt" positioning is unchanged).

### Item 18 — §18.9 Exact-Integer Dual Certificate Identity (`LeanWheel/Dual.lean`, over ℤ)
| Lean name | Statement (paper §18.9) | Axioms |
|---|---|---|
| `Wheel.dual_certificate_identity` | for ANY finite free-ring residue structure `r p k : ZMod (n p)` (with `2 ≤ n p`), ANY non-negative integer tick weights `u`, ANY integer scale `D > 0`, and EVERY valid cover (every positively weighted tick covered by some ring; `y p ∈ {0,1}` linked to phase `c p`): `D·(F + Σ_p y_p) ≥ TotalNum` with `TotalNum = D·F + Σ_k (1−f(k))·u_k − Σ_p max(0, M_p − W_p(0) − D)` | idem |
| `Wheel.dual_certificate_lb_floor` | solver form: `(TotalNum + D − 1)/D ≤ F + Σ_p y_p` (exact `Int.ediv` ceiling, valid for negative TotalNum — `verify_dual.py`'s `//`) | idem |
| `Wheel.dual_certificate_lb_ceil` | `⌈TotalNum / D⌉ ≤ F + Σ_p y_p` over ℚ | idem |

Scope: this is the pure algebra behind `verify_dual.py` / the CBB leaf certificates — the identity itself is kernel-certified; the large search trees stay in Python (per §2 below). The per-ring engine `Wheel.dual_per_ring` (`(W(c_p)−W(0))·y_p ≤ D·y_p + max(0, M_p−W(0)−D)` for binary `y_p`) and the peak-load spec `Wheel.dualM_spec` are proved along the way.

### Item 19 — §18.11 Schwinger rotor tuning (`LeanWheel/Rotor.lean`, over ℚ)
| Lean name | Statement (paper §18.11) | Axioms |
|---|---|---|
| `Wheel.rotor_intra_lap_spacing` | `E(j, m_z+1) − E(j, m_z) = b` for `E = a·j(j+1) + b·m_z` | idem |
| `Wheel.rotor_inter_lap_gap` | `E(j+1/2, −j−1/2) − E(j, +j) = a·(j+3/4) − b·(2j+1/2)` | idem |
| `Wheel.schwinger_rotor_tuning` | if the inter-lap gap equals `b` for every `j`, then `b/a = 1/2` (given `a ≠ 0`) | idem |
| `Wheel.wheel_spectrum_glue` | on lap `m`: `2j(j+1) + m_z + 1 = m(m−1)/2 + k` for `j = (m−1)/2`, `m_z = k − (m+1)/2` — the tuned `Â` spectrum is the wheel order (exact over ℚ, no evenness split) | idem |

### Item 20 — §18.12 equal-fiber CRT count (`LeanWheel/ErdosFiber.lean`)
| Lean name | Statement (paper §18.12) | Axioms |
|---|---|---|
| `Wheel.erdos_fiber_coprime` | `m ∣ L`, `a` a unit mod `m` ⟹ `fiber · φ(m) = φ(L)` where `fiber = card {x : (ZMod L)ˣ // x ≡ a (mod m)}` (uses `ZMod.unitsMap_surjective` + Lagrange + first isomorphism) | idem |
| `Wheel.erdos_fiber_le` | same for ANY residue `a`: `fiber · φ(m) ≤ φ(L)`; non-coprime classes are empty | idem |
| `Wheel.erdos_covering_necessary` | covering necessity: moduli `D ∋ m ∣ L` with coprime residue classes `a m` covering all units mod `L` ⟹ `Σ_{m∈D} φ(L)/φ(m) ≥ φ(L)` (i.e. `Σ 1/φ(m) ≥ 1`, the `S(L) ≥ 1` necessary condition) | idem |

---

## 2. Partial / stuck items

**None — the formalizable surface is closed.** All eleven first-pass items, all six second-pass items (12–17), and all three third-pass stragglers (18–20: the §18.9 dual identity, the §18.11 rotor tuning, the §18.12 CRT fiber count — the relayed "optional [F] algebraic stragglers") are fully formalized and kernel-checked. The two "optional enrichments" of the first pass are now both done: Theorem IV as LP feasibility (item 17) and Theorem II part 3 (item 15). What remains in the paper is **not kernel-formalizable by nature**, not awaiting effort:

- **Theorem II part 2** (`1/(p−1)` duality, `E|T_p| ≈ Σ m/p^a / ln(T/p^a)`) is explicitly conditional on the PNT-on-short-intervals heuristic **[S]** (the paper's own E4 errata restricts it to intervals of length > 1).
- **d(m) certificates** (Phase-B brackets, CBB trees, Erdős #7 census) are **computational**: the project holds solver-free Python verifiers on record (WHITEPAPER §18.9–§18.12) — certificates, not mathlib-scale formalizations. The *algebraic identities those verifiers rely on* are now kernel-certified (item 18 dual identity; item 20 fiber count). (A Lean re-check of the search trees themselves is conceivable but is a different project.)
- **Measured statistics** (width–strikers, clash factor, dissolution streaks, the B6 2.00× ratio, twin-pair probes) are finite **[E]** measurements with recorded reproduce commands.
- **C1/C2** (halves-claim, no-empty-layer) are open conjectures, Legendre-hard / BHP-width-obstructed by the paper's own reduction arguments.

## 3. Scoping for the unformalized remainder of the paper

Everything kernel-formalizable is now formalized (items 1–17). The table records the final disposition of the 2026-11-14 first-pass scoping list:

| Paper content | Final status |
|---|---|
| §4 B1 (visible set = primes) | **CLOSED** — item 12 |
| §4 B2 column law + B5/B6 parity structure | **CLOSED** — item 13 (the B6 2.00× *ratio* is measured [E], not formalizable) |
| §16.8 GLM lock+palindrome lemma | **CLOSED** — item 14 (with uniqueness + wheel model) |
| §19.2 part 2 (`1/(p−1)` duality) | heuristic **[S]** — not kernel-formalizable as stated (PNT on short intervals, E4 errata) |
| §19.2 part 3 (`T(m)^{1/4}` phase transition) | **CLOSED** — item 15 (exact threshold `p²·(B+1) > T(m)`) |
| §19.3 covering-capacity inequalities | **CLOSED** — item 16 |
| §19.4 full LP feasibility formulation | **CLOSED** — item 17 (exhibited point verified in the formally-defined relaxation) |
| §16–§18 d(m) certificates | computational — solver-free Python verifiers on record; a different project from kernel proofs |
| Measured statistics | empirical [E] — reproduce commands on record |
| C1/C2 | open conjectures — Legendre-hard by the paper's own reductions |

## 4. DEFECTS FOUND

**D1 — COMPRESSED PROSE in the Three-Primitive Theorem (confirmed, minor).**
The paper (§16.8) writes: *"Imposing P4 even at a single odd m > 1 (e.g. m = 3 ⟹ 2b ≡ 0 mod 3, and across odd m, gcd(m, m−1) = 1 ⟹ m ∣ b for all odd m) forces b = 0."* As stated, **a single odd m does not force b = 0**: it gives only `m ∣ b` (formalized: `three_primitive_P4`'s `key` lemma gives `(m : ℤ) ∣ (L 1 − 1)` for each odd `m ≥ 3`; `m = 3` alone admits `b = 3`). What forces `b = 0` is the **universal quantifier over odd m** — the proof uses a *fresh* odd `M = 2|b|+3 > |b|` and `M ∣ b` to conclude `b = 0`. Any unbounded family of odd m would do; one m does not. The paper's own parenthetical ("and across odd m … for all odd m") gestures at the fix, but the sentence "even at a single odd m > 1 forces b = 0" is false as written. Formalized version uses the universal reading — the correct content of the claim. *Severity: minor (compressed, not wrong theorem).*

**D2 — B7 "tick involution k ↔ m−k … bijection on ticks" is loose on the linear tick set (minor).**
On `{1, …, m}`, `k ↦ m − k` is not closed (`m ↦ 0 ∉ {1,…,m}`), so it is not literally a self-map of the layer's ticks, and the value pairing `v ↔ m² − v` fixes no point but swaps the two endpoint values across layers: `m² − T(m) = T(m−1)` (`mirror_endpoint`). The involution is exact on cyclic ticks: formalized as negation on `ZMod m` (`mirrorEquiv`, a genuine self-inverse bijection) with `−k ≡ m − k` (`mirror_zmod`). The value pairing `v(k) + v(m−k) = m²` is proved for the interior ticks `1 ≤ k ≤ m−1` (`mirror_sum`); the endpoints satisfy the same sum via `T(m−1) + T(m) = m²` across the layer boundary. *Severity: minor (paper's wheel intuition is the circle; the linear-layer reading needs the endpoint caveat).*

**D3 — P5 "polynomial extension" is ambiguous for spirals failing P3 (minor, definitional).**
Under P1∧P3 the extension is forced: `B` is the quadratic `x ↦ TZ(x−1) + b(x−1)` and `Bext` is well-defined. For witness (ii) (`B(m) = 2T(m−1) = m(m−1)`, `L(m) = 2m`) P3 fails, and the paper's claim that (ii) "satisfies P5" holds only under the *interpolating-polynomial* reading — the actual extension `p(x) = x(x−1)` is palindromic, and we certified that (`witness2_palindrome` + `witness2_extension_agrees`). Under the P1∧P3-relative reading used for the theorem's statement, (ii) **fails** P5 (`witness2_not_P5`), as does the decoupled family (iii-b) (`Bw3b`, whose interpolating extension is the zero polynomial). The main theorems are unaffected — P5 is only imposed together with P1∧P3, where the two readings coincide — but the independence-witness table in the paper silently mixes the two readings. *Severity: minor (definitional hygiene; theorem intact).*

**D4 — Strengthening note (not a defect): P1/P3 quantified over all m.**
The paper states the P1 recurrence and P3 step for `m ≥ 1`; the formalization quantifies over all `m : ℕ` (the `m = 0` conjuncts are additional, unused-on-the-paper's-domain obligations — a strict strengthening, not a weakening). Conversely, the conclusion of both three-primitive theorems is stated for `m ≥ 1`, matching the paper's domain `ℤ_{≥1}`: `B 0` is not determined by P1∧P3 (P1 ties it only to the free value `L 0`), so `B 0 = T 0` cannot be proved in general (witness (iii) with `c₀ ≠ 0` has `B 0 = c₀`). The paper's "∀ m, B(m) = T(m−1)" is correct only on its stated domain.

**D5 — Theorem II hypothesis: verified the paper's own repair is correct and sufficient (confirmation, not a new defect).**
The paper records (2026-10-25 GPT audit) that the original sufficient condition `T(m) < 2B²` fails at `m = 5` and was repaired to `T(m) < 2(B+1)²`. We **proved** the repaired form for all `m ≥ 3` (`Tm_lt_two_mul_Bm_add_one_sq`, from `T(m) = T(m−1) + m < (B+1)² + m` and `m ≤ (B+1)²`). The orphan characterization's mechanism goes through with exactly this hypothesis; the bound is tight-minded rather than loose (`T(m)/2 ≥ Q` is the load-bearing step).

**D6 — Theorem III's "must cover" is a constraint, not an equation (scope note).**
The paper's conclusion "the nonzero phases must cover W(S)" is the *defining obligation* of a valid phase vector (coverage by rotated residue classes), not a derivable identity. What is derivable — and is formalized — is the partition (`strata_cover`, `strata_disjoint_of_ne`), the union identity (`strata_union_over_subsets`), and the `E ⊆ S` iff (`loses_all_home_covers_iff`). Stating the covering obligation fully requires the congruence-based covering relation from Theorem I part 2 (`dvd_iff_eq_o`) applied per phase; no gap, just one definitional layer we did not build.

**D7 — the break-even statement and Theorem IV part 2 are conditionally true by design (scope note, matches the paper's labels).**
Both the smear profitability threshold (`p − 1 < L`) and the expected-orphan duality rest on heuristic inputs the paper itself labels **[S]**: the equidistribution of dual weight mod p (E4 errata in the paper restricts the PNT-on-short-intervals expectation to the regime where the interval length exceeds 1). The formalized content is exactly the parts the paper labels [F]: the break-even algebra and the pointwise coverage arithmetic.

**D8 — Mirror-pair parity claim needs the layer floor (trivial edge, m = 1).**
"For odd m no mirror prime pair can exist" uses "the even one is ≥ 4": the layer values are `≥ T(m−1)+1`, which is `≥ 4` only for `m ≥ 3` (m odd ⟹ m = 1 gives the singleton layer {1}, where the value 2 never occurs anyway, and m = 3 onward the bound holds). Formalized with `3 ≤ m`; the claim is vacuous at `m = 1`.

---

## 5. Files

```
lean_wheel/
├── lakefile.toml            # name = "lean_wheel", mathlib v4.35.0 dependency
├── lean-toolchain           # leanprover/lean4:v4.35.0
├── LeanWheel.lean           # library root (imports all modules below)
├── PrintAxioms.lean         # axiom report script (not part of the lib; `lake env lean PrintAxioms.lean`)
└── LeanWheel/
    ├── Defs.lean            # T, TZ, exactness (two_mul_T/TZ), recurrences, TZ_neg (palindrome)
    ├── B7.lean              # item 1
    ├── B3.lean              # item 2
    ├── B4.lean              # item 3
    ├── B1.lean              # item 12 (visible set = primes)
    ├── B2.lean              # item 13 (column law + B5 seat-zero)
    ├── Bijection.lean       # item 4 (Theorem I.1)
    ├── RatioSlip.lean       # item 5 (Theorem I.2)
    ├── Primality.lean       # item 6 (Theorem I.3) + the √N bridge
    ├── ThreePrimitive.lean  # item 7 (flagship) + all independence witnesses
    ├── GLM.lean             # item 14 (lock+palindrome lemma + uniqueness + wheel model)
    ├── Orphan.lean          # item 8 (Theorem II.1)
    ├── PhaseTransition.lean # item 15 (Theorem II.3)
    ├── Conservation.lean    # item 9 (Theorem III)
    ├── Capacity.lean        # item 16 (covering-capacity inequalities)
    ├── Smear.lean           # item 10 (Theorem IV)
    ├── LP.lean              # item 17 (explicit LP relaxation point)
    └── BreakEven.lean       # item 11 (the break-even statement)
```

No git commits were made. No files outside `lean_wheel/` were touched.
