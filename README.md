# The Prime Tread Wheel — Release 2026-11-15

**Counting numbers on a wheel that grows by one tick per layer, and what the
stagger of that growth knows about the primes.**

Obi (Sylvan Gaskin), with Claude, Argon (Gemini), Kimi, GPT, and GLM.
Canonical text: `WHITEPAPER.md` (§0–§19). This bundle is the public release
subset: the whitepaper, the Lean 4 formalization, the solver-free integer
verifiers, and the certificate artifacts they check.

**Release:** tag `v1.0.1` (correction pass 2026-11-16: Erdős #7 frontier comparison withdrawn as stated, refs. 39–42 added; nothing deleted) · v1.0.0 archived at tag `v1.0.0` · Zenodo DOI: [10.5281/zenodo.24266492](https://doi.org/10.5281/zenodo.24266492) (published 2026-11-16, v1.0.0 artifact)

## Layout

| Path | Contents |
|------|----------|
| `WHITEPAPER.md` | The full monograph. §14 fixes the credit demarcation against Tucker (Zenodo 22912558 / 22865056): his archive is credited item-by-item; the continuous spiral, the guarantee-zone wedge, the solver-free certificate stack, and the formalization are claimed here. |
| `lean_wheel/` | Lean 4 + mathlib project. 83 theorems, zero `sorry`. `LeanWheel/MainTheorems.lean` is the flagship summary; `LeanWheel/Sanity.lean` exhibits witnesses against vacuity. |
| `verify/` | Solver-free, exact-integer, standard-library-only verifiers (Python 3). |
| `certificates/` | The certificate artifacts (JSON). |
| `doc/AXIOMS.md` | Captured `#print axioms` output for the whole corpus (2026-11-15). Every footprint is a subset of {propext, Classical.choice, Quot.sound}. |
| `doc/TRIAGE_THEOREM_DAY.md`, `doc/FORMALIZATION_STATUS.md` | The 83-theorem disposition ledger and the per-row formalization map. |
| `SHA256SUMS.txt` | Integrity manifest for every file in this bundle. |

## Headline certified results

1. **d(1500) ∈ [42, 45]**, both ends solver-free (zero solver in the trusted
   computing base). LB 42: `certificates/cbb_m1500_hybrid_t42_np.json`
   (13,740-leaf pure-integer CBB tree, 2026-10-27). UB 45:
   `certificates/best45_argon_clean.json` (177 rings = primes
   p ≤ ⌊√T(1499)⌋ = 1060, 2026-10-27).
2. **Local Rigidity anatomy**: the 48-rotation witness
   (`certificates/best48_primary.json`, §18.6 of the whitepaper) with its
   partition anatomy (`certificates/anatomy_best48_results.json`).
3. **83 kernel-checked theorems**, zero `sorry` (see `doc/AXIOMS.md`).
4. Nine exact-integer dual/rigidity certificates
   (`certificates/dual_certificates_m1500.json`).

## Reproduce

Python checks (any Python 3, no dependencies):

```sh
python3 verify/verify_dual.py     certificates/dual_certificates_m1500.json   # 9 theorems, seconds
python3 verify/verify_witness.py  certificates/best45_argon_clean.json 45      # UB 45 witness, seconds
python3 verify/verify_witness.py  certificates/best48_primary.json 48          # 48-rotation witness, seconds
python3 verify/cbb_verify.py      certificates/cbb_m1500_hybrid_t42_np.json   # LB 42 tree, ~180 s
```

Lean 4 (needs [elan](https://github.com/leanprover/elan); the pinned toolchain
is `lean_wheel/lean-toolchain`):

```sh
cd lean_wheel && lake exe cache get && lake build     # expected: build succeeds (9,071 jobs)
```

Integrity:

```sh
sha256sum -c SHA256SUMS.txt
```

## What is not claimed

- C1/C2 (the halves-claim and no-empty-layer) remain **open**; the paper
  labels them and they are labeled there.
- The break-even / harmonic-smear statement (paper §19.5) is **[F] only
  conditionally** on its stated equidistribution heuristic, by its own label.
- Two Tier-3 scaffolding items (a trivially-true palindrome-shaped lemma and
  the conditional break-even algebra module) are internal to the certified
  corpus and are excluded from all claim tables; no paper claim depends on
  either as stated.
- One archived helper script was quarantined for self-reference during the
  audit; it is not part of this release and nothing in this bundle calls it.
- Tucker (Zenodo v2 2026-09-23) holds public priority on his own items,
  itemized in §14 of the whitepaper. The (phase, covering) formulation over a
  primorial sieve is classical (Jacobsthal; Hagedorn; Ziller–Morack 2017) and
  is claimed by neither side.

## Licensing

- Code (Lean corpus, verifiers): **MIT** — see `LICENSE`.
- Whitepaper text (`WHITEPAPER.md`): **CC BY 4.0** — see `LICENSE-CC-BY-4.0.md`.

## Citation

See `CITATION.cff`. Zenodo deposit: https://doi.org/10.5281/zenodo.24266492
(published 2026-11-16).
