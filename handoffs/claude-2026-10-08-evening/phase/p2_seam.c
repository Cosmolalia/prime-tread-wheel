/* p2_seam.c -- hot seats down the seam, on layers far past the earlier checks.
 *
 * Column c after the seam on layer m is the number T(m-1) + c, a quadratic in m: (m^2 - m + 2c)/2.
 * For each column: count the primes on layers M0+1..M1, exactly (every value is sieved by every prime up to
 * the square root of the largest value, so no probabilistic test is involved), and the chance count
 * sum 1/ln(value) that random numbers of the same sizes would give.
 * Gear-rule constant (Bateman-Horn): product over odd primes p of (1 - w_p/p)/(1 - 1/p), where w_p is how many
 * seats of ring p the column can land on: 1 + (D/p) with D = 1 - 8c (w_p = 1 when p divides D).
 * Ring 2 contributes a factor of exactly 1 (the column is even on half the layers).
 *
 * usage: p2_seam M0 M1 c1 [c2 ...]
 * prints one JSON object per column.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

static uint64_t powmod(uint64_t a, uint64_t e, uint64_t m) {
    uint64_t r = 1; a %= m;
    while (e) { if (e & 1) r = r * a % m; a = a * a % m; e >>= 1; }
    return r;
}
static uint64_t sqrtmod(uint64_t n, uint64_t p) {          /* Tonelli-Shanks, n a nonzero residue, p odd prime < 2^31 */
    if (p % 4 == 3) return powmod(n, (p + 1) / 4, p);
    uint64_t q = p - 1; int s = 0;
    while (!(q & 1)) { q >>= 1; s++; }
    uint64_t z = 2; while (powmod(z, (p - 1) / 2, p) != p - 1) z++;
    uint64_t c = powmod(z, q, p), x = powmod(n, (q + 1) / 2, p), t = powmod(n, q, p); int m = s;
    while (t != 1) {
        int i = 0; uint64_t tt = t;
        while (tt != 1) { tt = tt * tt % p; i++; }
        uint64_t b = c; for (int j = 0; j < m - i - 1; j++) b = b * b % p;
        x = x * b % p; c = b * b % p; t = t * c % p; m = i;
    }
    return x;
}

int main(int argc, char **argv) {
    uint64_t M0 = strtoull(argv[1], 0, 10), M1 = strtoull(argv[2], 0, 10);
    int nc = argc - 3; int64_t *cs = malloc(sizeof(int64_t) * nc);
    int64_t cmax = 0;
    for (int i = 0; i < nc; i++) { cs[i] = atoll(argv[3 + i]); if (cs[i] > cmax) cmax = cs[i]; }
    uint64_t maxval = (M1 - 1) * M1 / 2 + (uint64_t)cmax;
    uint64_t S = (uint64_t)sqrtl((long double)maxval) + 2;
    /* primes up to S */
    uint8_t *sv = calloc(S + 1, 1);
    uint32_t *pr = malloc(sizeof(uint32_t) * (S / 8 + 1000)); size_t np = 0;
    for (uint64_t i = 2; i <= S; i++) {
        if (sv[i]) continue;
        if (i > 2) pr[np++] = (uint32_t)i;
        for (uint64_t j = i * i; j <= S; j += i) sv[j] = 1;
    }
    free(sv);
    uint64_t W = M1 - M0;
    uint8_t *comp = malloc(W);
    const uint64_t B1 = 1000000ULL, B2 = 10000000ULL;      /* decade buckets */
    for (int ci = 0; ci < nc; ci++) {
        int64_t c = cs[ci], D = 1 - 8 * c;
        memset(comp, 0, W);
        for (uint64_t m = M0 + 1; m <= M1; m++) {            /* ring 2: even values are out */
            uint64_t v = (m - 1) * m / 2 + (uint64_t)c;
            if (!(v & 1)) comp[m - M0 - 1] = 1;
        }
        long double C = 1.0L;
        for (size_t k = 0; k < np; k++) {
            uint64_t p = pr[k];
            uint64_t d = (uint64_t)(((D % (int64_t)p) + (int64_t)p) % (int64_t)p);
            uint64_t inv2 = (p + 1) / 2, roots[2]; int nr = 0, w;
            if (d == 0) { w = 1; roots[nr++] = inv2; }
            else if (powmod(d, (p - 1) / 2, p) == 1) {
                w = 2; uint64_t s = sqrtmod(d, p);
                roots[nr++] = (1 + s) % p * inv2 % p;
                roots[nr++] = (1 + p - s) % p * inv2 % p;
            } else w = 0;
            C *= (1.0L - (long double)w / p) / (1.0L - 1.0L / p);
            for (int r = 0; r < nr; r++) {
                uint64_t start = M0 + 1, off = (roots[r] + p - start % p) % p;
                for (uint64_t m = start + off; m <= M1; m += p) comp[m - M0 - 1] = 1;
            }
        }
        /* values small enough to be one of the sieving primes themselves: settle them by trial division */
        for (uint64_t m = M0 + 1; m <= M1; m++) {
            uint64_t v = (m - 1) * m / 2 + (uint64_t)c;
            if (v > S) break;
            int isp = v >= 2;
            for (uint64_t q = 2; q * q <= v && isp; q++) if (v % q == 0) isp = 0;
            comp[m - M0 - 1] = !isp;
        }
        uint64_t cnt[3] = {0, 0, 0}; long double ch[3] = {0, 0, 0};
        for (uint64_t m = M0 + 1; m <= M1; m++) {
            long double v = (long double)(m - 1) * m / 2 + c;
            int b = m <= B1 ? 0 : (m <= B2 ? 1 : 2);
            ch[b] += 1.0L / logl(v);
            if (!comp[m - M0 - 1]) cnt[b]++;
        }
        uint64_t tc = cnt[0] + cnt[1] + cnt[2]; long double tch = ch[0] + ch[1] + ch[2];
        printf("{\"c\": %lld, \"D\": %lld, \"C\": %.6Lf, \"primes\": %llu, \"chance\": %.3Lf, \"boost\": %.6Lf, "
               "\"buckets\": [[%llu, %.3Lf], [%llu, %.3Lf], [%llu, %.3Lf]], \"M0\": %llu, \"M1\": %llu, \"sieve_to\": %llu}\n",
               (long long)c, (long long)D, C, (unsigned long long)tc, tch, tc / tch,
               (unsigned long long)cnt[0], ch[0], (unsigned long long)cnt[1], ch[1], (unsigned long long)cnt[2], ch[2],
               (unsigned long long)M0, (unsigned long long)M1, (unsigned long long)S);
        fflush(stdout);
    }
    return 0;
}
