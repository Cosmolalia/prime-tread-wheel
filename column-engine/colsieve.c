/* colsieve.c — certified primes down one COLUMN of the prime tread wheel, with the rings STREAMED.
 *
 * Layer m holds ticks k = 1..m with values T(m-1)+k, T(n) = n(n+1)/2.
 * A column is one tick held fixed while the layers go by:
 *     from the seam start:  tick k        ->  N(m) = (m^2 - m)/2 + k
 *     from the seam end:    tick m - j    ->  N(m) = (m^2 + m)/2 - j
 * Both are N(m) = (m^2 + b*m)/2 + c  with  (b, c) = (-1, k)  or  (+1, -j).
 *
 * Ring p (odd prime) lands on the column only on layers m with m^2 + b*m + 2c = 0 (mod p):
 *     m = (-b +- sqrt(1 - 8c)) / 2   (mod p)
 * If 1 - 8c is not a square mod p (the lane test) the ring NEVER lands on this column. Otherwise it lands on
 * exactly two layer classes mod p (one if 1 - 8c = 0 mod p): solve once, then hop +p. No per-layer upkeep.
 *
 * Because each ring is solved once and then forgotten, the ring list is never held: primes are generated in
 * segments, used, and thrown away. Memory = one byte per layer in the column. The wall becomes the time to
 * stream the rings up to sqrt(N_top) (one modular square root each), not memory and not number size.
 *
 * usage: colsieve start|end <k or j> <m0> <L> [out.txt]
 *   writes every prime on the column as "m N" lines to out.txt if given; prints stats.
 * build: gcc -O3 -march=native -fopenmp -o colsieve colsieve.c -lm
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <omp.h>

typedef unsigned __int128 u128;
typedef uint64_t u64;
typedef int64_t i64;

static inline u64 mulm(u64 a, u64 b, u64 p) { return p < (1ULL << 32) ? (a * b) % p : (u64)((u128)a * b % p); }
static u64 powm(u64 a, u64 e, u64 p) { u64 r = 1; a %= p; while (e) { if (e & 1) r = mulm(r, a, p); a = mulm(a, a, p); e >>= 1; } return r; }
static int jacobi(u64 a, u64 n) {
    int t = 1; a %= n;
    while (a) {
        while (!(a & 1)) { a >>= 1; u64 r = n & 7; if (r == 3 || r == 5) t = -t; }
        u64 x = a; a = n; n = x;
        if ((a & 3) == 3 && (n & 3) == 3) t = -t;
        a %= n;
    }
    return n == 1 ? t : 0;
}
static u64 sqrtm(u64 a, u64 p) {                       /* a a nonzero square mod odd prime p */
    if ((p & 3) == 3) return powm(a, (p + 1) >> 2, p);
    if ((p & 7) == 5) {                                /* Atkin */
        u64 a2 = (2 * a) % p, v = powm(a2, (p - 5) >> 3, p), i = mulm(mulm(a2, v, p), v, p);
        return mulm(mulm(a, v, p), (i + p - 1) % p, p);
    }
    u64 q = p - 1; int s = 0; while (!(q & 1)) { q >>= 1; s++; }   /* Tonelli–Shanks */
    u64 z = 2; while (jacobi(z, p) != -1) z++;
    int M = s; u64 c = powm(z, q, p), t = powm(a, q, p), R = powm(a, (q + 1) >> 1, p);
    while (t != 1) {
        int i = 0; u64 tt = t; while (tt != 1) { tt = mulm(tt, tt, p); i++; }
        u64 b = c; for (int j = 0; j < M - i - 1; j++) b = mulm(b, b, p);
        M = i; c = mulm(b, b, p); t = mulm(t, c, p); R = mulm(R, b, p);
    }
    return R;
}
static u64 isqrt128(u128 n) {
    u64 x = (u64)sqrtl((long double)n);
    while ((u128)x * x > n) x--;
    while ((u128)(x + 1) * (x + 1) <= n) x++;
    return x;
}
static void put128(FILE *f, u128 v) { char b[48]; int i = 47; b[i] = 0; do { b[--i] = '0' + (int)(v % 10); v /= 10; } while (v); fputs(b + i, f); }

static int B; static i64 C; static u64 M0, L;
static inline u128 Nval(u64 m) { u128 mm = m; return (mm * mm + (B > 0 ? mm : 0) - (B < 0 ? mm : 0)) / 2 + (C >= 0 ? (u128)C : 0) - (C < 0 ? (u128)(-C) : 0); }

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: colsieve start|end <k or j> <m0> <L> [out.txt]\n"); return 1; }
    int fromEnd = argv[1][0] == 'e';
    i64 kj = atoll(argv[2]); M0 = strtoull(argv[3], 0, 10); L = strtoull(argv[4], 0, 10);
    B = fromEnd ? 1 : -1; C = fromEnd ? -kj : kj;
    if (kj < (fromEnd ? 0 : 1) || (u64)kj > (fromEnd ? M0 - 1 : M0)) { fprintf(stderr, "tick must exist on every layer: 1<=k<=m0 (start) or 0<=j<m0 (end)\n"); return 1; }
    u64 mTop = M0 + L - 1;
    u128 Ntop = Nval(mTop), Nmin = Nval(M0);
    u64 P = isqrt128(Ntop);                               /* deciding rings: p^2 <= N(mTop) */
    uint8_t *comp = calloc(L, 1);
    double t0 = omp_get_wtime();

    /* ring 2: N(m) mod 2 has period 4 in m */
    for (u64 t = 0; t < 4 && t < L; t++) if ((Nval(M0 + t) & 1) == 0) for (u64 m = M0 + t; m <= mTop; m += 4) if (Nval(m) != 2) comp[m - M0] = 1;

    /* base primes up to sqrt(P) for the segmented generator */
    u64 r = (u64)sqrtl((long double)P) + 1;
    uint8_t *bs = calloc(r + 1, 1); u64 *base = malloc(sizeof(u64) * (r / 2 + 10)); u64 nb = 0;
    for (u64 i = 3; i <= r; i += 2) if (!bs[i]) { base[nb++] = i; for (u64 j = i * i; j <= r; j += 2 * i) bs[j] = 1; }

    const u64 SEG = 1 << 21;                               /* odd numbers per segment */
    u64 nseg = (P / 2 + SEG) / SEG;
    u64 rings = 1, dead = 0, stamps = 0, sqrts = 0;
    i64 D = 1 - 8 * C;                                     /* the column's discriminant */
    #pragma omp parallel reduction(+:rings,dead,stamps,sqrts)
    {
        uint8_t *sv = malloc(SEG);
        #pragma omp for schedule(dynamic, 1)
        for (u64 s = 0; s < nseg; s++) {
            u64 lo = 1 + 2 * s * SEG;                     /* odd numbers lo, lo+2, ..., lo+2(SEG-1) */
            memset(sv, 0, SEG);
            for (u64 i = 0; i < nb; i++) {
                u64 q = base[i], st = q * q; if (st > lo + 2 * (SEG - 1)) break;
                if (st < lo) { st = (lo + q - 1) / q * q; if (!(st & 1)) st += q; }
                for (u64 x = (st - lo) / 2; x < SEG; x += q) sv[x] = 1;
            }
            for (u64 x = 0; x < SEG; x++) {
                u64 p = lo + 2 * x; if (p > P) break; if (p < 3 || sv[x]) continue;
                rings++;
                i64 Dm = D % (i64)p; if (Dm < 0) Dm += p;
                u64 roots[2]; int nr = 0, inv2 = 0; u64 i2 = (p + 1) / 2; (void)inv2;
                u64 mb = B < 0 ? 1 : p - 1;               /* -b mod p */
                if (Dm == 0) roots[nr++] = mulm(mb, i2, p);
                else {
                    if (jacobi((u64)Dm, p) != 1) { dead++; continue; }   /* the lane test: never lands here */
                    u64 sq = sqrtm((u64)Dm, p); sqrts++;
                    roots[nr++] = mulm((mb + sq) % p, i2, p);
                    roots[nr++] = mulm((mb + p - sq) % p, i2, p);
                }
                for (int j = 0; j < nr; j++) {
                    u64 m = M0 + ((roots[j] + p - M0 % p) % p);
                    for (; m <= mTop; m += p) {
                        if (p >= Nmin && Nval(m) == p) continue;    /* the ring sitting on itself */
                        comp[m - M0] = 1; stamps++;
                    }
                }
            }
        }
        free(sv);
    }
    double t1 = omp_get_wtime();
    u64 primes = 0; FILE *f = argc > 5 ? fopen(argv[5], "w") : 0;
    for (u64 i = 0; i < L; i++) if (!comp[i] && Nval(M0 + i) > 1) { primes++; if (f) { fprintf(f, "%llu ", (unsigned long long)(M0 + i)); put128(f, Nval(M0 + i)); fputc('\n', f); } }
    if (f) fclose(f);
    printf("column %s %lld | layers %llu..%llu (%llu) | N up to ", fromEnd ? "end-j" : "start-k", (long long)kj,
           (unsigned long long)M0, (unsigned long long)mTop, (unsigned long long)L);
    put128(stdout, Ntop);
    printf("\nrings %llu (up to %llu) | never land %llu (%.1f%%) | square roots %llu | stamps %llu | primes %llu\n",
           (unsigned long long)rings, (unsigned long long)P, (unsigned long long)dead, 100.0 * dead / rings,
           (unsigned long long)sqrts, (unsigned long long)stamps, (unsigned long long)primes);
    printf("time %.2f s on %d threads | roll would do %.3g pointer updates (rings x layers)\n", t1 - t0, omp_get_max_threads(), (double)rings * L);
    return 0;
}
