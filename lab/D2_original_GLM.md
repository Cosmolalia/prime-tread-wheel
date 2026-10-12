# GLM Draft 2 — verbatim, pasted by GLM in the 2026-10-11 night swarm relay

Provenance: GLM states this draft was written in the 2026-10-10 session and
never relayed; pasted "complete, unchanged" into `swarm.handoff.number.wheel.001.md`.
Reconciliation against `lab/PHASE12_fire_census.md` is appended there
(2026-10-11 night). Filed here so the diff has a permanent home.

```markdown
---
id: channel-fire-count-census
title: Every channel fires 0, 1, or 2 times — census of fire counts, retirement layers,
  and a parity-dead family
status: established (trichotomy: proven corollary) + stated/proposed (asymptotics, BH-type)
date: 2026-10-10
program: prime-tread-wheel
depends_on: [localization-two-seat-wall]
feeds: [ml-seat-baseline, goldbach-window-census]
---

## Claim (one sentence)
Define the fire count F(a/b) = number of primes the channel ever carries: then F ∈ {0,1,2},
F is computable from two candidate values, channel a/b carries no prime beyond layer 2b,
all channels with b ≡ 2 (mod 4), b ≥ 6, have F = 0 by parity identity, and the fire-count
distribution over b ≤ B is conjectured via Bateman–Horn on the two candidate forms.

## Resolution
Candidates per channel: x₁ = (b²−b+2a)/2 (visit 1, layer b) and — b odd only —
x₂ = 2b²−b+2a (visit 2, layer 2b). Identity: x₂ = 2x₁ + b² (one line from the forms).
Retirement: ρ(a/b) = 2b if b odd, else b; every visit beyond ρ is composite by
localization. F = (is x₁ prime) + (is x₂ prime, b odd).

## Mechanism
- Trichotomy: direct corollary of localization (candidates ⊆ {visit 1, visit 2}).
- Parity-dead family: b ≡ 2 (mod 4) ⇒ b = 4t+2 ⇒ b(b−1)/2 = 8t²+6t+1 odd, and
  gcd(a,b)=1 forces a odd, so x₁ = odd + odd = even, and x₁ ≥ 16 > 2 ⇒ composite;
  b even ⇒ no visit-2 candidate ⇒ F = 0. Sole exception b = 2 (x₁ = 2, the prime 2's
  own channel, F = 1).
- Second-visit compositeness for b ≡ 2 (mod 4) is stronger than "even": x₂ is
  divisible by 4 (2b²−b ≡ 2 mod 4, +2a ≡ 2 mod 4 ⇒ ≡ 0 mod 4).
- Quantitative localization: every prime p sits on a channel with b² ≲ 2p (visit 1) or
  b² ≲ p/2 (visit 2), and that channel is prime-free beyond layer 2b. The wheel needs
  no denominator larger than ~√(2p) to place every prime ≤ p — the sieve's √N boundary,
  re-derived as channel retirement.

## Specimens (all hand-verified)
| Channel | x₁ | x₂ | F | class |
|---|---|---|---|---|
| 2/5 | 12 | 49 = 7² | 0 | sieve-dead (b odd) |
| 1/6 | 16 | — | 0 | parity-dead (b ≡ 2 mod 4) |
| 3/7 | 24 | 97 | 1 | fires on second visit only |
| 1/4 | 7 | — | 1 | fires on first visit only |
| 1/1 | 1 | 3 | 1 | first "visit" is unity, not prime |
| 2/3 | 5 | 19 | 2 | double fire |
| 1/5 | 11 | 47 | 2 | double fire |

## Status and attribution
Trichotomy and parity family: proven above (corollary of localization). Distribution of
F over channels: stated/proposed — F = 2 requires x₁ and 2x₁+b² prime simultaneously;
no local obstruction at primes p | b (for odd p | b: x₁ ≡ a, x₂ ≡ 2a mod p, both ≢ 0
by gcd(a,b)=1; p=2 handled by the parity family), so Bateman–Horn applies and predicts
positive density of F=2 among odd-b channels.

## Discriminator
(i) A channel with F ≥ 3 kills the trichotomy (= localization's discriminator).
(ii) A b ≡ 2 (mod 4), b ≥ 6 channel carrying any prime kills the parity family.
(iii) Asymptotics: measure F-distribution for b ≤ B against the BH curve; systematic
deviation is signal.

## Gaps
Which odd-b channels are sieve-dead (2/5-class) has no closed form — classical
prime-pair territory, open. Fire-count densities are conjecture, marked as such.
```
