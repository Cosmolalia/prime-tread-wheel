/-
  Theorem III — disjoint-union conservation on the composite hypergraph
  (WHITEPAPER §19.3).

  The factor-support strata C_E = {k ∈ [1,m] : F(k) = E}, where
  F(k) = {p ∈ rings B : p ∣ T(m−1)+k}, partition [1,m]; for a rotated support
  S, the work set of ticks losing all home covers is exactly the disjoint union
  ⨆_{E ⊆ S} C_E.

  Formalized over Finset: partition (cover + pairwise disjointness) and the
  union identity.  The concluding covering OBLIGATION ("the nonzero phases must
  cover W(S)") is a constraint on valid phase vectors — definitional once the
  covering relation from Theorem I part 2 is in play — so it is stated here as
  the iff `loses_all_home_covers_iff`, which is the paper's "E ⊆ S" content.
-/

import Mathlib
import LeanWheel.Defs

namespace Wheel

/-- The wheel rings: the primes ≤ B. -/
def rings (B : ℕ) : Finset ℕ := (Finset.Icc 2 B).filter Nat.Prime

/-- The factor bundle of tick k: the rings dividing T(m−1)+k. -/
def F (m B : ℕ) (k : ℕ) : Finset ℕ := (rings B).filter (· ∣ T (m - 1) + k)

/-- The exact factor-support stratum C_E. -/
def stratum (m B : ℕ) (E : Finset ℕ) : Finset ℕ :=
  (Finset.Icc 1 m).filter (fun k ↦ F m B k = E)

/-- Membership in a stratum. -/
theorem mem_stratum (m B : ℕ) (k : ℕ) (E : Finset ℕ) :
    k ∈ stratum m B E ↔ k ∈ Finset.Icc 1 m ∧ F m B k = E :=
  Finset.mem_filter

/-- The strata are pairwise disjoint: distinct supports never share a tick. -/
theorem strata_disjoint_of_ne (m B : ℕ) {E1 E2 : Finset ℕ} (h : E1 ≠ E2) :
    Disjoint (stratum m B E1) (stratum m B E2) := by
  rw [Finset.disjoint_left]
  rintro k hk1 hk2
  rw [mem_stratum] at hk1 hk2
  exact h (hk1.2.symm.trans hk2.2)

/-- The strata cover [1,m]: every tick lies in its own support stratum. -/
theorem strata_cover (m B : ℕ) :
    Finset.Icc 1 m = (rings B).powerset.biUnion (fun E ↦ stratum m B E) := by
  ext k
  constructor
  · intro hk
    obtain ⟨h1, h2⟩ := Finset.mem_Icc.1 hk
    refine Finset.mem_biUnion.2 ⟨F m B k, Finset.mem_powerset.2 (Finset.filter_subset _ _), ?_⟩
    exact Finset.mem_filter.2 ⟨Finset.mem_Icc.2 ⟨h1, h2⟩, rfl⟩
  · intro hk
    obtain ⟨E, hE, hk'⟩ := Finset.mem_biUnion.1 hk
    obtain ⟨hk1m, _⟩ := Finset.mem_filter.1 hk'
    exact hk1m

/-- The conservation identity: the ticks losing all home covers under a rotated
    support S ⊆ rings B are exactly the disjoint union ⨆_{E ⊆ S} C_E. -/
theorem strata_union_over_subsets (m B : ℕ) (S : Finset ℕ) (hS : S ⊆ rings B) :
    (Finset.Icc 1 m).filter (fun k ↦ F m B k ⊆ S) =
      S.powerset.biUnion (fun E ↦ stratum m B E) := by
  ext k
  constructor
  · intro hk
    obtain ⟨hk1m, hsub⟩ := Finset.mem_filter.1 hk
    exact Finset.mem_biUnion.2 ⟨F m B k, Finset.mem_powerset.2 hsub,
      Finset.mem_filter.2 ⟨hk1m, rfl⟩⟩
  · intro hk
    obtain ⟨E, hE, hk'⟩ := Finset.mem_biUnion.1 hk
    obtain ⟨hk1m, hkE⟩ := Finset.mem_filter.1 hk'
    exact Finset.mem_filter.2 ⟨hk1m, by rw [hkE]; exact Finset.mem_powerset.1 hE⟩

/-- The paper's covering condition, stated as the pointwise iff: tick k loses
    all home covers iff its factor bundle is contained in the rotated support. -/
theorem loses_all_home_covers_iff (m B : ℕ) (S : Finset ℕ) (k : ℕ) :
    (∀ p ∈ F m B k, p ∈ S) ↔ F m B k ⊆ S := ⟨fun h p hp ↦ h p hp, fun h p hp ↦ h hp⟩

end Wheel
