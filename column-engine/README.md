# Column engine — certified primes straight down the wheel

Hold one tick fixed and let the layers go by. That's a column. Its numbers are a parabola in the layer m:

- tick k from the seam start: N(m) = (m² − m)/2 + k
- tick m − j from the seam end: N(m) = (m² + m)/2 − j

## How a ring lands on a column

Ring p lands on the column only on layers where m² ∓ m + 2c ≡ 0 (mod p), i.e. m ≡ (±1 ± √(1 − 8c))/2 (mod p).

- **Lane test fails** (1 − 8c not a square mod p): the ring never lands on this column, ever. That's half of all rings.
- **Lane test passes**: the ring lands on exactly two layer classes. Solve once, then hop +p layers.

No ring ticks through layers it doesn't touch. Nothing about a ring is kept once it has stamped, so the ring list is never held. Primes are made in segments, used, and dropped.

## What sets the limit

| engine | per-layer work | wall |
|---|---|---|
| Jump | every ring | number size (9·10¹⁵ in a browser) |
| Roll | every ring | holding every ring up to √N |
| Column | none: one square root per ring, total | time to stream the rings up to √N |

## Run

```
gcc -O3 -march=native -fopenmp -o colsieve colsieve.c -lm
./colsieve start 41 6000000000 1000000 out.txt    # tick 41, layers 6e9 .. 6e9+1e6
./colsieve end 7 1000000000 1000000 out.txt       # tick m−7
python3 verify.py start 41 6000000000 1000000 out.txt 3000   # deterministic MR, exact below 3.3e24
```

Values are 128-bit, so the engine runs to about layer 2.6·10¹⁸ in principle. In practice the limit is ring streaming time, roughly proportional to √N / ln N.
