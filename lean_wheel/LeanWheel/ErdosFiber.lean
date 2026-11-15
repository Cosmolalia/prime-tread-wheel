/-
  Prime Tread Wheel — §18.12 equal-fiber CRT count [F].

  For a divisor `m ∣ L`, the residue classes mod `m` that are coprime to `m`
  each capture exactly `φ(L)/φ(m)` units modulo `L`: the reduction map on
  unit groups `(ZMod L)ˣ → (ZMod m)ˣ` is surjective (mathlib:
  `ZMod.unitsMap_surjective`), so every nonempty fiber is a coset of the
  kernel, and Lagrange pins the kernel size:

      Fintype.card (ZMod L)ˣ = φ m · Fintype.card ker

  hence `φ L = φ m · fiber`.  Classes not coprime to `m` capture nothing.
  Consequence kernel-checked here: if a family of such classes (one per
  modulus in `D`, each coprime to its modulus) covers ALL units mod `L`,
  then `Σ_{m ∈ D} φ(L)/φ(m) ≥ φ(L)`, i.e. `Σ 1/φ(m) ≥ 1` — the `S(L) ≥ 1`
  necessary condition for a distinct-odd covering (WHITEPAPER §18.12).
-/

import Mathlib

namespace Wheel

variable {L m : ℕ} [instL : NeZero L]

private lemma erdos_aux (hm : m ∣ L) : m ≠ 0 :=
  ne_zero_of_dvd_ne_zero instL.out hm

/-- **[F] Equal-fiber count, coprime case (WHITEPAPER §18.12).**
    If `m ∣ L` and `a` is a unit mod `m`, the set of units mod `L`
    reducing to `a` has cardinality exactly `φ(L)/φ(m)`:
    `fiber · φ(m) = φ(L)`. -/
theorem erdos_fiber_coprime (hm : m ∣ L) {a : ZMod m} (ha : IsUnit a) :
    Fintype.card {x : (ZMod L)ˣ // (ZMod.castHom hm (ZMod m) (x : ZMod L)) = a}
      * m.totient = L.totient := by
  have hL : L ≠ 0 := instL.out
  have hm0 : m ≠ 0 := erdos_aux hm
  haveI : NeZero m := ⟨hm0⟩
  -- The fiber of the reduction map over `a` is a coset of its kernel.
  have hval : ∀ x : (ZMod L)ˣ, ((ZMod.unitsMap hm x : (ZMod m)ˣ) : ZMod m)
      = ZMod.castHom hm (ZMod m) (x : ZMod L) :=
    fun x => (ZMod.unitsMap_val hm x).trans (ZMod.castHom_apply (x : ZMod L)).symm
  have e1 : {x : (ZMod L)ˣ // (ZMod.castHom hm (ZMod m) (x : ZMod L)) = a} ≃
      {x : (ZMod L)ˣ // ZMod.unitsMap hm x = ha.unit} := by
    apply Equiv.subtypeEquiv (Equiv.refl _)
    intro x
    simp only [Equiv.refl_apply]
    constructor
    · intro h
      apply Units.ext
      rw [hval x, h, ha.unit_spec]
    · intro h
      rw [← hval x, h, ha.unit_spec]
  obtain ⟨x₀, hx₀⟩ := ZMod.unitsMap_surjective hm ha.unit
  have e2 : {x : (ZMod L)ˣ // ZMod.unitsMap hm x = ha.unit} ≃
      {y : (ZMod L)ˣ // ZMod.unitsMap hm y = 1} := by
    refine ⟨fun x => ⟨x₀⁻¹ * x, by simp [map_mul, map_inv, hx₀, x.2]⟩,
      fun y => ⟨x₀ * y, by simp [map_mul, hx₀, y.2]⟩, ?_, ?_⟩
    · intro x
      apply Subtype.ext
      simp [mul_inv_cancel_left]
    · intro y
      apply Subtype.ext
      simp [inv_mul_cancel_left]
  have e3 : {y : (ZMod L)ˣ // ZMod.unitsMap hm y = 1} ≃
      ↥(MonoidHom.ker (ZMod.unitsMap hm)) := by
    apply Equiv.subtypeEquiv (Equiv.refl _)
    intro y
    simp only [Equiv.refl_apply]
    exact MonoidHom.mem_ker.symm
  -- Lagrange: |G'| = |G' ⧸ ker| · |ker|, quotient ≃ range = ⊤ by surjectivity.
  have hLag := Subgroup.card_eq_card_quotient_mul_card_subgroup
    (MonoidHom.ker (ZMod.unitsMap hm))
  have hsurj : Function.Surjective (ZMod.unitsMap hm) := ZMod.unitsMap_surjective hm
  have htop : MonoidHom.range (ZMod.unitsMap hm) = ⊤ :=
    MonoidHom.range_eq_top.mpr hsurj
  have hq : Nat.card ((ZMod L)ˣ ⧸ MonoidHom.ker (ZMod.unitsMap hm)) = Nat.card (ZMod m)ˣ := by
    calc Nat.card ((ZMod L)ˣ ⧸ MonoidHom.ker (ZMod.unitsMap hm))
        = Nat.card ↥(MonoidHom.range (ZMod.unitsMap hm)) :=
          Nat.card_congr (QuotientGroup.quotientKerEquivRange _).toEquiv
      _ = Nat.card (ZMod m)ˣ := by rw [htop]; exact Subgroup.card_top
  rw [hq] at hLag
  have h1 : Nat.card (ZMod L)ˣ = L.totient := by
    rw [Nat.card_eq_fintype_card, ZMod.card_units_eq_totient]
  have h2 : Nat.card (ZMod m)ˣ = m.totient := by
    rw [Nat.card_eq_fintype_card, ZMod.card_units_eq_totient]
  rw [h1, h2] at hLag
  have hker : Fintype.card ↥(MonoidHom.ker (ZMod.unitsMap hm)) * m.totient = L.totient := by
    rw [← Nat.card_eq_fintype_card]
    rw [mul_comm] at hLag
    exact hLag.symm
  calc Fintype.card {x : (ZMod L)ˣ // (ZMod.castHom hm (ZMod m) (x : ZMod L)) = a}
      * m.totient
      = Fintype.card ↥(MonoidHom.ker (ZMod.unitsMap hm)) * m.totient := by
        rw [Fintype.card_congr (e1.trans (e2.trans e3))]
    _ = L.totient := hker

/-- **[F] Equal-fiber bound, general case (WHITEPAPER §18.12).**
    For ANY residue class `a` mod `m` (`m ∣ L`), the units mod `L` landing
    in it number at most `φ(L)/φ(m)`:
    `fiber · φ(m) ≤ φ(L)`.  Equality holds iff `gcd(a, m) = 1`
    (`erdos_fiber_coprime`); non-coprime classes are empty. -/
theorem erdos_fiber_le (hm : m ∣ L) (a : ZMod m) :
    Fintype.card {x : (ZMod L)ˣ // (ZMod.castHom hm (ZMod m) (x : ZMod L)) = a}
      * m.totient ≤ L.totient := by
  rcases em (IsUnit a) with ha | ha
  · rw [erdos_fiber_coprime hm ha]
  · have hem : IsEmpty {x : (ZMod L)ˣ //
        (ZMod.castHom hm (ZMod m) (x : ZMod L)) = a} := ⟨fun x => ha (by
      rw [← x.2]
      exact (ZMod.unitsMap hm x).isUnit)⟩
    haveI := hem
    rw [Fintype.card_of_isEmpty, Nat.zero_mul]
    exact Nat.zero_le _

/-- **[F] Covering necessity (WHITEPAPER §18.12, `S(L) ≥ 1`).**
    If a family of moduli `D` (all dividing `L`), each equipped with a
    residue class `a m` coprime to its modulus, covers every unit mod `L`,
    then `Σ_{m ∈ D} φ(L)/φ(m) ≥ φ(L)` — dividing out `φ(L)`, the sum of
    reciprocal totients is at least `1`. -/
theorem erdos_covering_necessary {D : Finset ℕ} (hD : ∀ m ∈ D, m ∣ L)
    (a : ∀ m : ↥D, ZMod m.1) (ha : ∀ m : ↥D, IsUnit (a m))
    (hcover : ∀ x : (ZMod L)ˣ, ∃ m : ↥D,
      (ZMod.castHom (hD m.1 m.2) (ZMod m.1)) (x : ZMod L) = a m) :
    L.totient ≤ ∑ m : ↥D, L.totient / m.1.totient := by
  have hsurj : Function.Surjective (fun s : (Σ m : ↥D,
      {x : (ZMod L)ˣ // (ZMod.castHom (hD m.1 m.2) (ZMod m.1)) (x : ZMod L) = a m}) =>
      (s.2 : (ZMod L)ˣ)) := by
    intro x
    exact ⟨⟨Classical.choose (hcover x), x, Classical.choose_spec (hcover x)⟩, rfl⟩
  have h1 := Fintype.card_le_of_surjective _ hsurj
  have h2 : Fintype.card (Σ m : ↥D,
      {x : (ZMod L)ˣ // (ZMod.castHom (hD m.1 m.2) (ZMod m.1)) (x : ZMod L) = a m})
      = ∑ m : ↥D, Fintype.card {x : (ZMod L)ˣ //
          (ZMod.castHom (hD m.1 m.2) (ZMod m.1)) (x : ZMod L) = a m} :=
    Fintype.card_sigma
  rw [h2] at h1
  have h3 : ∀ m : ↥D, Fintype.card {x : (ZMod L)ˣ //
      (ZMod.castHom (hD m.1 m.2) (ZMod m.1)) (x : ZMod L) = a m}
      ≤ L.totient / m.1.totient := by
    intro m
    apply (Nat.le_div_iff_mul_le (Nat.totient_pos.mpr
      (Nat.pos_of_ne_zero (erdos_aux (hD m.1 m.2))))).mpr
    exact erdos_fiber_le (hD m.1 m.2) (a m)
  have hcard : Nat.card (ZMod L)ˣ = L.totient := by
    rw [Nat.card_eq_fintype_card, ZMod.card_units_eq_totient]
  calc L.totient = Fintype.card (ZMod L)ˣ := by
        rw [← Nat.card_eq_fintype_card, hcard]
    _ ≤ ∑ m : ↥D, Fintype.card {x : (ZMod L)ˣ //
          (ZMod.castHom (hD m.1 m.2) (ZMod m.1)) (x : ZMod L) = a m} := h1
    _ ≤ ∑ m : ↥D, L.totient / m.1.totient := Finset.sum_le_sum fun m _ => h3 m

end Wheel
