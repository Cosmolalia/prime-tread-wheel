# Prime Tread — GPU Frontier

The roll engine with one ring per GPU lane. Every ring is a prime p ≤ m/√2
holding two uint32 pointers (`o` = landing spot, `d` = stride); per layer it
stamps its multiples in the window, then does subtract-and-wrap, add-and-wrap.
An uncovered tick **is** prime — the certificate and the answer are the same
object, no probabilistic test, no bignums anywhere on the GPU.

## Run it

```bash
./run.sh                      # windowed, starts at layer 282,000,000
./run.sh --start-layer 5999999000
./run.sh --window 4194304     # wider band per layer
```

First run sieves the ~201M primes up to m/√2 ≈ 4.24e9 (about a minute, then
disk-cached in `cache/`). Every startup runs a self-check (`[verify] ... PASS`)
seeding at layer 1,234,567 and comparing 8 layers × 1024 ticks against an
independent CPU span sieve before the app opens.

## Controls

Send `SIGUSR1` to a running instance to dump all thread stacks into its
log (startup hangs are otherwise silent).

| key | action |
|---|---|
| space | pause |
| s | save the current layer's certified gold band (`gold-band-m<L>.txt`, sha256 in header) plus its witness-count sidecar (`witness-band-m<L>.npy`: per-tick omega) |
| j | jump to any layer ≤ 6,069,... (type digits, Enter) |
| + / − | roll speed (layers per frame, up to 4096) |
| q | quit |

## Headless / service modes

```bash
./run.sh --benchmark                 # layers/s and certified numbers/s
./run.sh --dump-band 6000000000      # certify one layer's band, save, exit
./run.sh --frames 150                # smoke-test the app loop on the dummy driver
```

`--dump-band` is the product cut: a certified-prime frontier service. The
2026-10-09 audit at layer 6e9 (N ≈ 1.8e19): all 6,002 listed primes exact
(deterministic Miller–Rabin), 1,952 non-listed samples all composite —
nothing wrongly excluded, nothing wrongly included. Each dump also saves
`witness-band-m<M>.npy`: per-tick omega(N) — how many rings stamped that
tick. The `s` key saves the same sidecar for the live window.

## Witness counts

`stamp_kernel` atomic-adds into a second window alongside the bool stamp,
so every tick carries its distinct-small-prime-divisor count at zero extra
roll cost. What the mechanism guarantees (audited 2026-10-10 against exact
trial division, 400 random ticks at layer 1.5M, 0 mismatches):

- count 0  ⟺ N is prime (the gold band)
- count ≥ 2 ⟹ count = omega(N) exactly (the full divisor set is in range)
- count 1  ⟹ N = p^a or p·q with q > m/√2 (semiprime-shaped; the cofactor
  is prime by the argument above — the machine certifies it, it cannot
  split it)

The same audit caught a real latent bug on first run: every cached prime
table held a duplicated `2` (builder prepended 2 and emitted it from the
first segment). Invisible to the boolean stamp — the duplicate ring wrote
the same ticks — but +1 on every even tick's witness count. Fixed in the
builder; legacy caches are sanitized on load; all on-disk caches trimmed.

## Numbers (RTX 4070 laptop, 36 SMs, ~256 GB/s)

| layer | rings active | window | layers/s | numbers certified/s |
|---|---|---|---|---|
| 282M | 11.0M | 1,048,576 | ~95 | ~100M |
| 6.0e9 | 200.9M | 1,048,576 | ~32 | ~33M |

The wall's true name is bandwidth: every ring must be visited once per layer
(20 bytes of traffic each), so layers/s falls as the dial climbs — but a wide
window holds the certified rate in the tens of millions per second. The
uint32 registers cap the dial at m < 2³²·√2 (N ≈ 1.8e19); uint64 registers
would double the traffic per ring for a higher ceiling.

## Verified chain

`seed_kernel` (mod-2p halving trick, one uint64 multiply — no bignums),
`stamp_kernel` (double-reciprocal first-stamp estimate with integer
correction — a 64-bit division per ring per layer would dominate the whole
kernel), `advance_kernel` (two wraps). `roll()` re-contracts the ring count as
the frontier climbs (primes up to m/√2 must all hold rings; newly activated
rings are reseeded at the current layer — without this, semiprimes of two
stale-bound primes stamp nothing and read as primes). The re-contract walks
from a cached index in 1M-element strides and only binary-searches the final
window — a full-array `searchsorted` probes the 800 MB prime table ~28 times,
and under memory-bandwidth contention on this box each probe measured 6+
seconds (2026-10-09: startup "hang" was verify's 8 roll-contracts, not a
deadlock). Self-check on every
startup; exact audit of the dump-band output on 2026-10-09; discriminating
test 2026-10-09 (seed 50,000, roll 20,000 layers: frozen contract certifies 2
false primes, growing contract certifies 0).

## Box notes

To free the GPU, the coqui (voice TTS) and rubiks-demo services were stopped:

```bash
systemctl --user start coqui.service rubiks-demo.service   # bring them back
```
