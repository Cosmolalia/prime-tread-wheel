# HEADLINE SORT — the 83 axiom-report theorems (2026-11-17)

**Object:** the 83 names on `PrintAxioms.lean` (`#print axioms`, verified by
direct read today — 83 commands, lines 5–87). This is the human-readable
two-bucket sort of that exact list. Tier assignments and mathematics are
unchanged from TRIAGE_THEOREM_DAY.md; what changed is only the packaging.

**Counts:** 38 headline + 43 supporting + 2 conditional-only = 83.

★ = one of the 5 flagships on the public release surface
(`MainTheorems.lean`). Sanity checks (`Sanity.lean`, all `example`s) hold
small-number kernel witnesses and add 0 names to this report.

---

## HEADLINE RESULTS — 18 entries, 38 declarations

### Theorem I — addressing & the sieve ★

1. **Coordinate bijection** (`theoremI_bijection`) — every number N gets
   exactly one wheel address: a layer m and a seat k with N = T(m−1)+k;
   nothing lands in two layers, nothing in zero.
2. **Stagger field** (`o_succ`, `dvd_iff_eq_o`) — divisibility becomes exact
   equality: a prime p divides N precisely when the seat k equals the field
   value o_p(m), and the field is driven by the one-line recurrence
   o(m+1) = o(m) − m.
3. **Sieve criterion** (`theoremI_criterion`) — the wheel's own primality
   test IS the classical √N sieve: N is prime iff no prime up to √N divides
   it. The wheel re-derives the sieve; it does not replace it.

### Seam & mirror (§4 / §16)

4. **B4 seam theorem** (`B4_first`, `B4_second`) — the seam value and its
   next-door neighbor are forced composite (m≥3, m≥4 onward); the wheel's
   seam can never be prime.
5. **Mirror exclusion** (`no_mirror_prime_pair_odd`) — in odd layers, no two
   mirror-image seats can both be prime; primes cannot pair across the
   mirror.

### Three-Primitive & GLM ★★

6. **Three-Primitive** (`formula_B`, `three_primitive_P4`,
   `three_primitive_P5`, `P4_iff_P5_of_P1_P3`) — the three independence
   hypotheses each force B to be the wheel's own quadratic
   B(m) = m(m−1)/2, and the odd-lock and palindrome routes to that
   conclusion are the same route.
7. **GLM characterization** (`glm_lock_iff_gamma`, `glm_palindrome_iff`,
   `glm_unique`) — any count table that is seam-locked, lap-palindromic, and
   one-to-one per turn is EXACTLY the wheel's quadratic (1,−1,0); no other
   table survives all three conditions.

### Orphans & phase transition (§16 / §19.2)

8. **Orphan characterization** (`orphan_characterization`) — any number the
   wheel fails to cover is forced into prime-power form: p^a, or p^a times a
   single prime bigger than the layer floor.
9. **Phase transition** (`phase_transition`, `pow_mul_Bm_lt_Tm`) — below the
   exact threshold T(m) < p²(B+1), every orphan anchors at a=1: high-order
   powers die and orphans go squarefree.

### Conservation & capacity (§16 / §19.3)

10. **Strata conservation** (`strata_disjoint_of_ne`, `strata_cover`,
    `strata_union_over_subsets`) — a layer's numbers split exactly across
    their prime-factor bundles: every number in one stratum, no number in
    two, and the split is downward-closed.
11. **Capacity bound** (`capacity_inequality`,
    `capacity_inequality_family`, `uncovered_capacity`) — any covering
    family occupies at most Σ⌈m/p⌉ seats per class — the counting engine
    behind every d(m) lower bound the project ships.

### Coverage (§19.4)

12. **Smear coverage** (`smear_coverage`, `smear_coverage_eq_one_iff`) — the
    {2,3,5} weight recipe covers every tick with total ≥ 1, and the total is
    exactly 1 precisely when 5 ∤ N (checked across all 8 divisibility
    patterns).
13. **LP feasibility** (`lp_relaxation_feasible`, `xSmear_covers`) — the
    exhibited fractional assignment x_{p,c} = α_p/p satisfies every covering
    constraint on every layer, so the capacity bound is a genuine
    relaxation, not a fudge.

### Column laws (§4)

14. **B1 factor law** (`B1`, `B1_rough`) — a composite layer value must have
    a prime factor ≤ m (the wheel's visible set is exactly the primes),
    while a prime layer value is m-rough: no wheel prime divides it but
    itself.
15. **Column law** (`column_law`, `B5_seat_zero`) — a prime's seat has
    gcd(k,m) = 1, except when m ≡ 2 (mod 4), in which case every prime sits
    exactly at gcd 2.

### Solver-free certificates (§18)

16. **Dual certificate identity** ★ (`dual_certificate_identity`,
    `dual_certificate_lb_floor`, `dual_certificate_lb_ceil`) — one exact
    integer identity turns any valid cover into a machine-checkable
    lower-bound certificate: the algebra behind every solver-free bound this
    project ships.
17. **Rotor tuning** (`schwinger_rotor_tuning`, `wheel_spectrum_glue`) —
    forcing gap = spacing for every j pins the tuning to b/a = 1/2, and at
    that tuning the operator's spectrum is exactly the wheel order over ℚ.
18. **Erdős covering necessity** ★ (`erdos_fiber_coprime`,
    `erdos_covering_necessary`) — coprime residue classes carry equal-sized
    fibers, so any covering system must satisfy Σ 1/φ(m) ≥ 1 — the classic
    S(L) ≥ 1 condition, proved inside the wheel corpus.

---

## SUPPORTING LEMMAS — 43 declarations

Grouped by the headline they feed. These are honest load-bearing machinery:
the headlines do not compile or do not mean anything without them.

**Theorem I & mirror structure**
- `exists_coord`, `unique_coord` — existence and uniqueness halves of the bijection.
- `exists_prime_le_sqrt_of_not_prime` — the classical √N bridge into the criterion.
- `sqrt_Tm_lt` — √T(m) < m: the sieve window stays inside the layer.
- `T_pred_add_T`, `mirror_sum`, `mirror_endpoint`, `mirror_gcd`, `mirror_zmod` — the mirror-pairing algebra (endpoint exchange, eligibility, tick involution).
- `B3`, `B3_forward` — the triangular-offset iff over ℤ (§4 algebra); standalone, nothing in the tree imports it.

**Three-Primitive & GLM**
- `P3_implies_P2`, `int_dvd_TZ_pred_of_odd` — redundancy and divisibility bridges.
- `witness1_P1` … `witness3b_not_contiguous` (16 theorems) — non-vacuity and independence certificates: each hypothesis is shown satisfiable, and each can fail while the others hold.
- `quad_gap` — the palindrome gap identity (α+β)(2m−1).
- `wheel_model`, `wheel_model_lock`, `wheel_model_palindrome`, `wheel_model_turn` — the wheel itself satisfies every GLM condition, so the characterization is inhabited.

**Orphans & phase transition**
- `Tm_lt_two_mul_Bm_add_one_sq` — the repaired hypothesis T(m) < 2(B+1)², proved for all m ≥ 3 (D5).
- `phase_transition_threshold_shape` — the threshold's shape behind the T(m)^{1/4} display.

**Capacity**
- `stripe_card_le` — |stripe| ≤ ⌈m/p⌉, the zero-residue case split (the kernel-caught one, §18.3 note).

**Smear / LP**
- `smear_cost` — the 11/6 objective arithmetic.
- `xSmear_row_le` — every row bound of the exhibited point.

**Column laws**
- `T_pred_of_even` — closed form T(m−1) = (m−1)(m/2) for even m.

**Rotor**
- `rotor_intra_lap_spacing`, `rotor_inter_lap_gap` — the spacing and gap engines.

**Erdős**
- `erdos_fiber_le` — non-coprime classes are empty or bounded.

---

## KEPT IN REPO, NOT PAPER CLAIMS — 2 declarations

- `break_even_first`, `break_even_second` — conditional algebra whose warrant
  is a heuristic [S] input (D7). Theorem V is excluded from the flagship
  surface by the release rule; the paper must quote these conditionally.

---

## Note on the triage's summary counts

TRIAGE_THEOREM_DAY.md §6 header says "48 T1 + 56 T2 + 7 T3 = 111" and claims
the 83-name report "covers all T1, all T2, and the non-rfl T3 items." Its own
tables enumerate 59 T1, 45 T2, 5 T3 rows (= 109), and 59+45 > 83 refutes the
coverage claim. The 83 is the hand-curated list in `PrintAxioms.lean`
(including two names absent from the tier tables: `sqrt_Tm_lt`,
`T_pred_of_even`). Corrected by erratum in TRIAGE §11 (2026-11-17). The tier
assignments themselves and all mathematics are unaffected — bookkeeping only.
