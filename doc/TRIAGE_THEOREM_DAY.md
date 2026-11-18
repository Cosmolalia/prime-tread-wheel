# TRIAGE — Theorem Day release audit (2026-11-15)

**Auditor:** Kimi (prime wheel window), same-day re-verification in-window.
**Object:** `lean_wheel/` — Lean 4.35.0 + mathlib v4.35.0, 21 modules, 111
theorem/lemma declarations, of which 83 are on the `#print axioms` report.
**Method:** mechanical checks re-run today (2026-11-15 ~09:30 HST), not quoted
from the 11-14 ledger; every load-bearing claim below was re-measured.

---

## 0. Verdict up front

The corpus is **release-ready at the kernel level**. Zero escapes, zero
 bespoke prime definitions, all footprints inside the mathlib trio, build
green. The triage value is at the packaging layer: 111 declarations compress
to **5 flagship theorem clusters** for the public surface; the remaining
two-thirds are honest machinery that should stay visible but not headlined.
Two items need accurate labeling (Theorems V and the engine-vs-lens split),
one archived helper was quarantined for self-reference during the audit.

---

## 1. Zero-escape check — PASS (re-run 2026-11-15)

```
grep -nE 'sorry|admit\b|\baxiom\b|\bopaque\b|\bunsafe\b|implemented_by' LeanWheel/*.lean
```
→ **no matches in any compiled source.** The only matches in the repo are the
words "No `sorry` anywhere" in this file's own prose. No `@[implemented_by]`,
no `native_decide`, no `unsafe`.

Build re-run from warm cache: **`lake build` → "Build completed successfully
(9071 jobs)"** (9069 as of 2026-11-14 13:31; **+2 today**: the two new
Theorem-Day modules, `MainTheorems.lean` + `Sanity.lean` — re-verified green
independently after their construction, same session).

## 2. Axiom audit — PASS (re-run 2026-11-15)

`lake env lean PrintAxioms.lean` today: **83 theorems printed**, every one a
subset of `[propext, Classical.choice, Quot.sound]`:

| Footprint | Count |
|---|---|
| full mathlib trio | 73 |
| `[propext]` only | 6 |
| `[propext, Quot.sound]` | 4 |

No `Lean.ofReduceBool` (i.e. no `native_decide` smuggling), no project-local
axioms, no `Classical.choice`-free-but-sorry hacks.

## 3. Definition-integrity audit — PASS (the trap the protocol warns about does not exist here)

**Every prime predicate in the corpus binds to Mathlib.** Verified by direct
read of every `Prime` occurrence:

- `p.Prime`, `N.Prime` — dot notation for `Nat.Prime` (Mathlib);
- `rings B := (Finset.Icc 2 B).filter Nat.Prime` (Conservation.lean:23) — the
  ring set is *defined as* Mathlib primes, not as "uncrossed slots";
- `Nat.minFac_prime`, `N.minFac.Prime` (Orphan.lean:44,88);
- no `def WheelPrime`, no `IsWheelPrime`, no locally redefined divisibility.

Custom definitions, all inspected, all **structural** (none is a disguised
primality predicate):

| Def | File | Role |
|---|---|---|
| `T`, `TZ` | Defs | triangular numbers `n(n+1)/2` — the wheel order; `/2` carried via exactness lemmas `two_mul_T`/`two_mul_TZ` |
| `o` | RatioSlip | the stagger field `−T(m−1) mod p` (a ZMod value) |
| `Bm` | Orphan | layer floor `⌊√(T(m−1))⌋` |
| `P1`…`P5`, `Bext` | ThreePrimitive | named *hypotheses* (contiguity, unit lap, odd-m lock, palindrome) — conditions, not redefinitions |
| `IsQuadCount` | GLM | exact doubled quadratic identity `2B(m)=αm²+βm+γ` |
| `rings`, `F`, `stratum` | Conservation | set-theoretic scaffolding over `Nat.Prime` |
| `stripe` | Capacity | a rotated ring's residue class |
| `α`, `smearTerm` | Smear | per-ring LP weights (α₂=α₃=1, α₅=5/6) |
| `xSmear` | LP | the exhibited LP-feasibility point |
| `dualW`, `dualM`, `dualF` | Dual | dual LP objects (weights, max-load, coverage count) |
| `mirrorEquiv` | B7 | negation on `ZMod m` (a genuine involution) |
| `Bw/Lw 1..3b` | ThreePrimitive | explicit independence-witness families |

**No tautology-by-construction was found.** The nearest structural risk —
Theorem III's "must cover" — is recorded as scope note D6 in
FORMALIZATION_STATUS.md: coverage is stated as a *hypothesis* (`hcover`), not
proved from nothing.

## 4. Vacuity check — PASS (with new hard witnesses added today)

Per the protocol, flagship implications were checked for satisfiable
hypotheses, not `False → anything` shapes:

- **Three-Primitive** carries its own non-vacuity: four witness families
  (`witness1_*`, `witness2_*`, `witness3_*`, `witness3b_*`, 16 theorems)
  exhibit *inhabited* objects on every side of every independence claim —
  e.g. `witness2_P4` shows P4 holding without P3, `witness1_not_P5` shows P5
  failing under P1∧P3. The theorem cannot be vacuous and its hypotheses are
  shown non-redundant by explicit countermodels.
- **GLM** likewise: `wheel_model`, `wheel_model_lock`, `wheel_model_palindrome`
  inhabit both sides of both iff's (`glm_lock_iff_gamma`,
  `glm_palindrome_iff`).
- **Smear/LP**: `smear_coverage_eq_one_iff` enumerates all 8 divisibility
  patterns of {2,3,5} — each pattern is a decidable, inhabited case;
  `lp_relaxation_feasible` needs no hypotheses (the exhibited point verifies
  every constraint for every layer `m`).
- **NEW (2026-11-15):** `LeanWheel/Sanity.lean` adds external instantiations —
  concrete small-number witnesses for Theorem I (N=30), the primality
  criterion (N=7), B4 (m=3), B2 column law (N=43), and the Erdős covering
  necessity (L=6, D={2,3}). See §6.1.

## 5. Engine vs. camera lens (companion code) — SPLIT VERIFIED, label accordingly

The protocol's trap: claiming the *wheel geometry* generates primes when the
code actually colors pre-computed primes onto spiral coordinates. Audit of
`lab/` (65-file grep over `is_prime|isprime|sympy|miller.?rabin`):

- **Engine (generation by elimination):** the certificate and census scripts
  generate survivors by modular elimination over sieve-seeded primes —
  `verify_ptri_witnesses.py` (division checks `any(n%p==0 …)` against a
  `primerange` seed list), `phaseb_2026-10-19/anatomy_best48.py` (per-tick
  classification by divisibility), `PHASE10_c4_audit.py` (single bytearray
  sieve, header states "no sympy, no GPT code"), twin-zone / pair-wedge
  enumeration (INSIGHTS Add. 24–25).
- **Cross-checks (legitimate `is_prime` use):** sympy/gmpy2 primality appears
  only as *independent verification* of engine outputs — MR cross-validated
  against the lab sieve (`PHASE4a`, `PHASE8_5_4_run.py`, `l4_bench.py`).
  These are the §8 instrument-audit instruments, not generators.
- **Display layer (camera lens, correctly scoped):**
  `problem-wheels.html` renders primality (Goldbach chords, prime staircase)
  as visualization. It makes no generation claim; keep it in the companion
  essay register, out of the paper.
- **Flag (known, quarantined):** `lab/ARCHIVE_TRIAGE_2026-10-12.md:65` records
  an archived twin-prime helper calling `isprime()` directly (self-referential). It
  is in `lab/` archive, not in the reproduce block; the note stays with it.

**Claim-hygiene consequence:** the paper's wheel claims are elimination /
covering bounds (correctly framed per the heat-shield rule); no O(1)
closed-form prime-prediction claim exists anywhere in the corpus or the
scripts. Theorem I's criterion is a sieve-equivalence, and §19.1 already
positions the recurrence against segmented-sieve prior art (Bays–Hudson,
Brent, Crandall–Pomerance).

---

## 6. Tier classification — all 111 declarations

Tier key:
- **T1** — headline structural theorem: carries a paper section; states a
  complete mechanism (existence+uniqueness, an iff, an exact identity, or a
  certified bound). Non-vacuous.
- **T2** — bridge lemma / machinery: required to make T1 compile; honest
  work, but a connector, not an endpoint.
- **T3** — sanity check / scaffolding / conditional-only algebra: keep in the
  repo, cut from paper claims.

"§" references are WHITEPAPER sections. (P) = physics-side appendix material
(§18.11): formally exact, separate audience from the sieve paper.

### 6.0 Definitions (not tiered — inspected in §3 above)

`T`, `TZ`, `o`, `Bm`, `P1`–`P5`, `Bext`, `IsQuadCount`, `rings`, `F`,
`stratum`, `stripe`, `α`, `smearTerm`, `xSmear`, `dualW`, `dualM`, `dualF`,
`mirrorEquiv`, `Bw1/Lw1`, `Bw2/Lw2`, `Bw3/Lw3`, `Bw3b/Lw3b`.

### 6.1 Tier 1 — headline structural (48 declarations)

| Declaration | File | § | Content |
|---|---|---|---|
| `B4_first` | B4 | §4 | `m ≥ 3 → ¬(T m).Prime` — seam value forced composite |
| `B4_second` | B4 | §4 | `m ≥ 4 → ¬(T m − 1).Prime` — second endpoint forced composite |
| `theoremI_bijection` | Bijection | §15/§19 | every `N` has a **unique** layer coordinate `(m,k)`, `N = T(m−1)+k` |
| `exists_coord` | Bijection | §19 | existence half (strong induction) |
| `unique_coord` | Bijection | §19 | the layer sandwich forces uniqueness |
| `o_succ` | RatioSlip | §15 | stagger field recurrence `o(m+1) = o(m) − m` |
| `dvd_iff_eq_o` | RatioSlip | §15 | `p ∣ N ↔ k = o_p(m)` — divisibility is *exact equality in the field* |
| `theoremI_criterion` | Primality | §19 | wheel = `√N`-sieve criterion: `N.Prime ↔` no prime `p ≤ ⌊√(T m)⌋` divides `N` |
| `no_mirror_prime_pair_odd` | B7 | §16 | odd `m ≥ 3`: no interior mirror pair is prime×prime |
| `formula_B` | ThreePrimitive | §16.8 | P1∧P3 force `B = TZ(m−1) + b(m−1)` — the mechanism engine |
| `three_primitive_P4` | ThreePrimitive | §16.8 | P1∧P3∧P4 ⟹ `b=0 ∧ B=T(·−1)` (odd-lock branch) |
| `three_primitive_P5` | ThreePrimitive | §16.8 | P1∧P3∧P5 ⟹ same (palindrome branch) |
| `P4_iff_P5_of_P1_P3` | ThreePrimitive | §16.8 | the two branches are equivalent under P1∧P3 |
| `witness1_P1`, `witness1_P3` | ThreePrimitive | §16.8 | family (i) satisfies P1∧P3 |
| `witness1_not_P4`, `witness1_not_P5` | ThreePrimitive | §16.8 | family (i) breaks P4 (m=3) and P5 — non-redundancy |
| `witness2_P1`, `witness2_P4` | ThreePrimitive | §16.8 | family (ii) satisfies P1∧P4 without P3 |
| `witness2_P3` (¬) | ThreePrimitive | §16.8 | family (ii) fails P3 |
| `witness2_not_P5` | ThreePrimitive | §16.8 | (ii) fails P5 under the P1∧P3-relative extension (D3) |
| `witness2_palindrome` | ThreePrimitive | §16.8 | (ii)'s interpolating polynomial is literally palindromic (D3) |
| `witness3_P3`, `witness3_P5` | ThreePrimitive | §16.8 | family (iii) satisfies P3∧P5 without P1 |
| `witness3_not_P1`, `witness3_not_P4` | ThreePrimitive | §16.8 | (iii) breaks P1 and P4 at m=3 |
| `witness3b_P3`, `witness3b_P4` | ThreePrimitive | §16.8 | decoupled zero family satisfies P3∧P4 |
| `witness3b_not_contiguous` | ThreePrimitive | §16.8 | and fails P1-contiguity at m=1 |
| `glm_lock_iff_gamma` | GLM | §16.8 | seam lock ⟺ `γ = 0` (iff, both directions) |
| `glm_palindrome_iff` | GLM | §16.8 | lap palindrome ⟺ `α + β = 0` (iff) |
| `glm_unique` | GLM | §16.8 | lock + palindrome + 1:1 turn ⟹ `(1,−1,0)`, `B = T(·−1)` **uniquely** |
| `wheel_model` | GLM | §16.8 | the wheel itself satisfies all three conditions |
| `wheel_model_lock` | GLM | §16.8 | lock direction inhabited on the wheel |
| `wheel_model_palindrome` | GLM | §16.8 | palindrome inhabited on the wheel |
| `orphan_characterization` | Orphan | §16 | forced form `N = p^a` or `N = p^a·Q`, `Q` prime `> B` |
| `phase_transition` | PhaseTransition | §19.2.3 | exact threshold `T m < p²(B+1)` ⟹ every orphan is squarefree-anchored `a=1` |
| `pow_mul_Bm_lt_Tm` | PhaseTransition | §19.2.3 | the paper's `p^a < T(m)/B` in exact nat-divided form |
| `strata_disjoint_of_ne` | Conservation | §16 | distinct factor bundles occupy disjoint strata |
| `strata_cover` | Conservation | §16 | the layer partitions exactly over its factor bundles |
| `strata_union_over_subsets` | Conservation | §16 | downward closure: `F(k) ⊆ S` strata = union over `E ⊆ S` |
| `capacity_inequality` | Capacity | §19.3 | covering ⟹ `|W(S)| ≤ Σ⌈m/p⌉` per-class capacity bound |
| `capacity_inequality_family` | Capacity | §19.3 | same for every downward-closed sub-family |
| `uncovered_capacity` | Capacity | §19.3 | zero-ring stratum bounded by `Σ_{p∈S}⌈m/p⌉` |
| `smear_coverage` | Smear | §19.4 | `Σ smearTerm ≥ 1` for every tick (uniform coverage) |
| `smear_coverage_eq_one_iff` | Smear | §19.4 | strengthening: `= 1 ↔ 5 ∤ N` (all 8 patterns) |
| `xSmear_covers` | LP | §19.4 | exhibited point covers every tick |
| `lp_relaxation_feasible` | LP | §19.4 | `x_{p,c} = α_p/p` is feasible on **every** layer |
| `B1` | B1 | §4 | composite layer value has a prime factor `p ≤ m` — visible set = primes |
| `B1_rough` | B1 | §4 | prime layer value is m-rough (no wheel prime divides it but itself) |
| `column_law` | B2 | §4 | prime in layer ⟹ `gcd k m = 1 ∨ (gcd k m = 2 ∧ m%4=2)` |
| `B5_seat_zero` | B2 | §4 | on `m ≡ 2 (mod 4)`: every prime sits at `gcd k m = 2` exactly |
| `dual_certificate_identity` | Dual | §18.9 | exact-integer dual identity for any free residue structure + valid cover |
| `dual_certificate_lb_floor` | Dual | §18.9 | solver form `(TotalNum + D − 1)/D ≤ F + Σ y_p` |
| `dual_certificate_lb_ceil` | Dual | §18.9 | `⌈TotalNum/D⌉` rational form |
| `schwinger_rotor_tuning` | Rotor (P) | §18.11 | gap = spacing for all `j` ⟹ `b/a = 1/2` |
| `wheel_spectrum_glue` | Rotor (P) | §18.11 | tuned `Â` spectrum = wheel order (exact over ℚ) |
| `erdos_fiber_coprime` | ErdosFiber | §18.12 | coprime classes have equal fiber `φ(L)/φ(m)` |
| `erdos_covering_necessary` | ErdosFiber | §18.12 | covering ⟹ `Σ 1/φ(m) ≥ 1` (the `S(L) ≥ 1` condition) |

**NEW (2026-11-15) — vacuity witnesses, not new math:** `LeanWheel/Sanity.lean`
(adds zero names to the axiom report — every check is an `example`) holds
compiled, kernel-checked instantiations: Theorem I at `N = 30` (coord
`(8,2)`; uniqueness via `Wheel.unique_coord`), the criterion at `N = 7, m = 4,
k = 1` plus the direct RHS check over primes `≤ ⌊√(T 4)⌋` (the
`decide`-on-`Nat.sqrt` route fails — well-founded recursion doesn't reduce in
the kernel — so the checks go through `Nat.le_sqrt` + `interval_cases`, the
equivalent form), `B4_first` at `m = 3`, `column_law` at `N = 43 = T 8 + 7`
(`Nat.Prime 43` by `norm_num`, `gcd 7 9 = 1` by `decide`), P1∧P3∧P4
inhabited at the wheel itself, `erdos_covering_necessary` at `L = 6, D = {2,3}`
(bound `2 ≤ 2/1 + 2/2 = 3`; units `1, 5` both `≡ 1 mod 2`, discharged by
`fin_cases` + `decide`), and `dual_certificate_identity` at the degenerate
empty family (`ι = κ = Empty`, `u = 0`, `D = 1`) — a genuinely inhabited
consistency check. A header "Not instantiated here" section records that
`orphan_characterization` / `phase_transition` hypotheses are witnessed by
the companion Python certificates (FORMALIZATION_STATUS.md §2), not by small
instances. These witness that the flagship hypotheses are satisfiable at
exhibited values.

### 6.2 Tier 2 — bridge lemmas & machinery (56 declarations)

| Declaration | File | Role |
|---|---|---|
| `two_mul_T`, `two_mul_TZ` | Defs | `/2`-exactness engine for the whole corpus |
| `T_succ`, `T_pred`, `T_self_sub_add` | Defs | layer recurrences over ℕ |
| `TZ_succ`, `TZ_pred`, `TZ_neg` | Defs | layer recurrences over ℤ; `TZ_neg` is the lap palindrome |
| `T_strictMono` | Defs | the layer sandwich is well-founded |
| `T_pred_add_T` | B7 | `T(m−1)+T(m)=m²` — endpoint exchange engine |
| `mirror_sum` | B7 | interior mirror pairing `v + v' = m²` |
| `mirror_endpoint` | B7 | `m² − T m = T(m−1)` — the across-layer endpoint |
| `mirror_gcd` | B7 | eligibility preserved under mirror (gcd=2 escape) |
| `mirror_zmod` | B7 | `−k ≡ m−k` on cyclic ticks |
| `mirrorEquiv_involutive` | B7 | the tick involution is self-inverse (D2 scope) |
| `B3` | B3 | exact triangular-offset equivalence over ℤ |
| `B3_forward` | B3 | the `c = T(j)` factorization |
| `two_mul_T_sub_one` | B4 | `2(T m −1) = (m−1)(m+2)` |
| `exists_prime_le_sqrt_of_not_prime` | Primality | classical `√N` bridge (mathlib-shaped) |
| `telescope_L` | ThreePrimitive | P3 ⟹ `L(m+1) = L 1 + m` |
| `P3_implies_P2` | ThreePrimitive | P3 ⟹ P2 (redundancy, paper-noted) |
| `int_dvd_TZ_pred_of_odd` | ThreePrimitive | odd `m ∣ TZ(m−1)` |
| `isCoprime_int_self_sub_one` | ThreePrimitive | Bézout for the Euclid step |
| `int_self_dvd_of_dvd_mul_pred` | ThreePrimitive | `m ∣ b(m−1) ⟹ m ∣ b` |
| `Bext_gap` | ThreePrimitive | palindrome gap `(L1−1)(2m−1)` |
| `quad_gap` | GLM | `2(B m − B(1−m)) = (α+β)(2m−1)` |
| `wheel_model_turn` | GLM | the 1:1 turn on the wheel (one-liner condition) |
| `le_T` | Orphan | `n ≤ T n` |
| `Tm_lt_two_mul_Bm_add_one_sq` | Orphan | the **repaired** hypothesis `T(m) < 2(B+1)²` proved for all `m ≥ 3` (D5) |
| `minFac_sq_le_of_not_prime` | Orphan | `minFac² ≤ N` engine |
| `phase_transition_threshold_shape` | PhaseTransition | `(B+1)² > T(m−1)` — the shape behind the `T(m)^{1/4}` display |
| `mem_stratum` | Conservation | stratum membership unfolding |
| `loses_all_home_covers_iff` | Conservation | ` (∀ p ∈ F(k), p ∈ S) ↔ F(k) ⊆ S` (propext only) |
| `mem_stripe` | Capacity | stripe membership unfolding |
| `stripe_card_le` | Capacity | `|stripe| ≤ ⌈m/p⌉` — the zero-residue case split (kernel-caught, §18.3 note) |
| `smear_cost` | Smear | `11/6` objective arithmetic |
| `xSmear_sum_Ico` | LP | row-sum of the exhibited point |
| `xSmear_row_le` | LP | every row bound satisfied |
| `zmod_one_ne_zero` | Dual | `1 ≠ 0` in `ZMod k`, `k ≥ 2` |
| `dualM_nonempty` | Dual | peak-load residue exists |
| `dualM_spec` | Dual | the max-load specification |
| `dual_per_ring` | Dual | per-ring engine `(W(c_p)−W(0))·y_p ≤ …` |
| `rotor_intra_lap_spacing` | Rotor | `E(j, m_z+1) − E(j, m_z) = b` |
| `rotor_inter_lap_gap` | Rotor | the `j+½` inter-lap gap |
| `erdos_fiber_le` | ErdosFiber | non-coprime classes empty / bounded |

### 6.3 Tier 3 — sanity & scaffolding (7 declarations; keep in repo, cut from paper claims)

| Declaration | File | Why T3 |
|---|---|---|
| `T_mono` | Defs | one-line corollary of `T_strictMono` |
| `witness2_extension_agrees` | ThreePrimitive | `rfl` scaffolding attached to witness (ii) |
| `the trivial palindrome lemma` | ThreePrimitive | statement is `∀ m, (0:ℤ) = 0` — trivially true; cut from paper (the real content is D3's note) |
| `break_even_first` | BreakEven | algebraic rewrite only; warrant is heuristic [S] (D7) — paper must quote conditionally |
| `break_even_second` | BreakEven | same (denominator `p−1` variant) |

(Counts: 48 T1 + 56 T2 + 7 T3 = 111 declarations. The 83-name axiom report
covers all T1, all T2, and the non-`rfl` T3 items.)

---

## 7. Dependency graph

### 7.1 File-level DAG (imports)

```
                        Mathlib (v4.35.0)
                              |
            ┌─────────────────┼───────────────────────────┐
            |                 |                           |
        Defs.lean      Dual.lean  ErdosFiber.lean   Rotor.lean
            |          (standalone,              (standalone,
   ┌────────┼─────────┐  Mathlib only)             Mathlib only)
   |        |         |            (standalone, Mathlib only)
   |        |         |
 Primality  Orphan    Smear
   |      /    \       |
   |     /      \      |
   B1   B2   PhaseTrans.|
        |             \|
        |              LP
   B7, B3, B4, Bijection, RatioSlip, ThreePrimitive,
   GLM, Conservation, BreakEven  ←── Defs only
        |
   Capacity ←── Conservation
```

- `Defs.lean` is the sole shared spine (everything needs `T`/`TZ` +
  exactness). Changing it rebuilds the world — treat as frozen.
- **Three modules are fully standalone** (import Mathlib only): `Dual`,
  `ErdosFiber`, `Rotor`. They carry no wheel-object dependency — cleanest
  possible isolation for the §18.9/§18.12/§18.11 certificates.
- Deep chains: `Defs → Orphan → {B2, PhaseTransition}`;
  `Defs → Conservation → Capacity`; `Defs → Smear → LP`.

### 7.2 Theorem-cluster view (what the paper actually cites)

```
Theorem I  = Bijection(exists,unique,bijection)
           + RatioSlip(o_succ, dvd_iff_eq_o)
           + Primality(√N bridge → criterion)

Three-Primitive = formula_B + three_primitive_P4/P5 + P4_iff_P5
           + 4 witness families (non-vacuity + independence)

GLM lemma = glm_lock/palindrome_iff + glm_unique + wheel_model(+lock/pal/turn)

Theorem II = orphan_characterization (+ Orphan bridges)
           + phase_transition (+ threshold engine)

Theorem III = strata_disjoint/cover/union + capacity_inequality(+family)
           + uncovered_capacity   (Conservation feeds Capacity)

Theorem IV = smear_coverage(+_eq_one_iff) + smear_cost
           + lp_relaxation_feasible (Smear feeds LP)

the break-even statement  = break_even_first/second   [conditional algebra only — D7]

§18.9  = dual_certificate_identity → _lb_floor → _lb_ceil   [standalone]
§18.11 = rotor_intra/inter → schwinger_rotor_tuning → wheel_spectrum_glue
§18.12 = erdos_fiber_coprime(+_le) → erdos_covering_necessary   [standalone]
```

## 8. Flagship surface for release (the "staged release" rule)

The public entry point is **`LeanWheel/MainTheorems.lean`** (added
2026-11-15): the five clusters restated as aliases over the proof tree, with
plain-English docstrings and section pointers. Selection rule applied: each
flagship (a) states a complete mechanism, (b) is non-vacuous (witnesses in
§6.1), (c) carries a named paper section, (d) survives the strongest-objection
test — no flagship depends on the heuristic [S] inputs (the break-even statement excluded by
this rule) or on the measured [E] statistics.

1. **Theorem I** — coordinate bijection + stagger field + exact criterion.
2. **Three-Primitive Theorem** — both branches + equivalence + witnesses.
3. **GLM characterization** — lock+palindrome+turn ⟹ the wheel, uniquely.
4. **Dual certificate identity** — the algebra behind every solver-free
   certificate the project ships.
5. **Erdős covering necessity** — the CRT fiber count and the `S(L) ≥ 1`
   covering condition.

Tier-2 machinery stays in place and importable; Tier-3 stays in the repo and
out of the paper's claim set.

## 9. Packaging checklist (heat-shield protocol)

- [x] Zero-escape grep — PASS (§1)
- [x] `#print axioms` all ⊆ mathlib trio — PASS, re-run today (§2)
- [x] Definition integrity — no bespoke prime — PASS (§3)
- [x] Vacuity — intrinsic witnesses + new `Sanity.lean` — PASS (§4, §6.1)
- [x] Engine-vs-lens labeled — PASS with one archived self-reference flagged (§5)
- [x] Tier sort of all 111 declarations — done (§6)
- [x] No flat 80-theorem dump: 5 clusters in `MainTheorems.lean` — done (§8)
- [x] README rewritten bone-dry (build + inventory + pointer; zero philosophy)
- [ ] **Publisher items:** push public repo + tag; the arXiv timestamp is the
      move that converts self-dated INSIGHTS entries into third-party-dated
      priority record (per the 11-15 publish-readiness assessment).

## 10. Cross-references

- Full per-theorem statements + defect log D1–D8:
  `lean_wheel/FORMALIZATION_STATUS.md` (authoritative).
- This triage audits *packaging*; FORMALIZATION_STATUS audits *mathematics*.
  Where they differ, FORMALIZATION_STATUS wins.
- Provenance: §14 dated note now records the first wheel run
  (2026-10-01 09:59 HST, publisher testimony) alongside the public-instrument
  date (2026-10-07).

---

## 11. Erratum — §6 summary counts corrected (2026-11-17, Kimi)

The §6 tier tables are the audit; the summary counts above them were wrong.
Mechanical recount today: §6.1 enumerates **59** T1 declarations (not 48);
§6.2 enumerates **45** T2 (not 56); §6.3 shows **5** T3 rows (not 7). That
sums to 109, and a raw `grep` of `theorem|lemma` across the compiled modules
gives 112 excluding `MainTheorems.lean`'s 13 aliases (`Sanity.lean`
contributes 0 — all `example`s). The "111" total therefore cannot be
reproduced from the tables as printed **[G]**: the residual 2–3 declaration
gap is unlocated and does not affect any tier assignment or proof.

Separately, the §6.3 parenthetical — "the 83-name axiom report covers all
T1, all T2, and the non-`rfl` T3 items" — is refuted by arithmetic
(59 + 45 > 83). The 83 is the hand-curated list in `PrintAxioms.lean` (83
`#print axioms` commands, verified by direct read 2026-11-17). It includes
two names absent from the tier tables (`sqrt_Tm_lt`, `T_pred_of_even`) and
omits many T2 items (e.g. `two_mul_T`, `T_strictMono`, `dual_per_ring`).

The human-readable headline/supporting sort of the actual 83 lives in
`HEADLINE_SORT_2026-11-17.md`: **38 headline, 43 supporting, 2
conditional-only** (break-even). Nothing in the mathematics changed; this
corrects bookkeeping only.
