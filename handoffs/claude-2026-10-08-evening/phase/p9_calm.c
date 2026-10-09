/* p9_calm.c -- are the seam lanes calmer than coin flips, and is the calm made by the rings' schedule?
 *
 * Lane c on layer m is the number T(m-1) + c. For each lane, over layers M0+1 .. M1, three streams of "primes":
 *   real   : the actual primes (exact: every value sieved by every prime up to the square root of the largest value)
 *   coin   : each odd value is "prime" with the gear-rule chance q = 2C/ln(value), independently (no schedule at all)
 *   sched  : rings up to Z run on their real schedule (values they hit are out); each survivor is then "prime"
 *            with chance q/s, where s = share of odd values that survive rings up to Z (same average as real)
 * Expected count in a window e = sum of q over its odd values; coin-flip variance v = sum of q(1-q).
 * For windows of 10^2 .. 10^8 layers, accumulate sum (count - e)^2 and sum v.  Ratio = sum (count-e)^2 / sum v:
 * 1 = as noisy as coin flips, below 1 = calmer.
 *
 * usage: p9_calm M0 M1 seed c_first c_last      (prints one JSON object per lane)
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define Z 1000
#define NW 7                                    /* windows of 1e2 .. 1e8 layers */

static uint64_t powmod(uint64_t a, uint64_t e, uint64_t m) {
    uint64_t r = 1; a %= m;
    while (e) { if (e & 1) r = r * a % m; a = a * a % m; e >>= 1; }
    return r;
}
static uint64_t sqrtmod(uint64_t n, uint64_t p) {
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
static uint64_t rs;
static inline double urand(void) {
    rs ^= rs >> 12; rs ^= rs << 25; rs ^= rs >> 27;
    return (double)((rs * 2685821657736338717ULL) >> 11) * (1.0 / 9007199254740992.0);
}

int main(int argc, char **argv) {
    uint64_t M0 = strtoull(argv[1], 0, 10), M1 = strtoull(argv[2], 0, 10), seed = strtoull(argv[3], 0, 10);
    int c0 = atoi(argv[4]), c1 = atoi(argv[5]);
    uint64_t maxval = (M1 - 1) * M1 / 2 + (uint64_t)c1;
    uint64_t S = (uint64_t)sqrtl((long double)maxval) + 2;
    if ((M0) * (M0 + 1) / 2 <= S) { fprintf(stderr, "M0 too small for the sieve shortcut\n"); return 1; }
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
    const uint64_t WS[NW] = {100ULL, 1000ULL, 10000ULL, 100000ULL, 1000000ULL, 10000000ULL, 100000000ULL};
    for (int c = c0; c <= c1; c++) {
        int64_t D = 1 - 8 * (int64_t)c;
        rs = seed * 0x9E3779B97F4A7C15ULL + (uint64_t)c * 0xD1B54A32D192ED03ULL + 1;
        memset(comp, 0, W);
        long double C = 1.0L, s = 1.0L;
        for (size_t k = 0; k < np; k++) {
            uint64_t p = pr[k];
            uint64_t d = (uint64_t)(((D % (int64_t)p) + (int64_t)p) % (int64_t)p);
            uint64_t inv2 = (p + 1) / 2, roots[2]; int nr = 0, w;
            if (d == 0) { w = 1; roots[nr++] = inv2; }
            else if (powmod(d, (p - 1) / 2, p) == 1) {
                w = 2; uint64_t r = sqrtmod(d, p);
                roots[nr++] = (1 + r) % p * inv2 % p;
                roots[nr++] = (1 + p - r) % p * inv2 % p;
            } else w = 0;
            C *= (1.0L - (long double)w / p) / (1.0L - 1.0L / p);
            if (p <= Z) s *= (1.0L - (long double)w / p);
            uint8_t bit = p <= Z ? 2 : 4;
            for (int r = 0; r < nr; r++) {
                uint64_t start = M0 + 1, off = (roots[r] + p - start % p) % p;
                for (uint64_t m = start + off; m <= M1; m += p) comp[m - M0 - 1] |= bit;
            }
        }
        double Cd = (double)C, sd = (double)s;
        /* cur[level][0..4] = real, coin, sched, e, v for the window open at that level */
        double cur[NW][5]; memset(cur, 0, sizeof cur);
        double sq[NW][3]; double sv_[NW]; long nwin[NW];
        memset(sq, 0, sizeof sq); memset(sv_, 0, sizeof sv_); memset(nwin, 0, sizeof nwin);
        double tot[5] = {0, 0, 0, 0, 0};
        for (uint64_t m = M0 + 1; m <= M1; m++) {
            uint64_t v = (m - 1) * m / 2 + (uint64_t)c;
            if (v & 1) {
                double q = 2.0 * Cd / log((double)v);
                uint8_t f = comp[m - M0 - 1];
                cur[0][3] += q; cur[0][4] += q * (1 - q);
                if (!f) cur[0][0] += 1;
                if (urand() < q) cur[0][1] += 1;
                if (!(f & 2) && urand() < q / sd) cur[0][2] += 1;
            }
            uint64_t idx = m - M0;
            for (int L = 0; L < NW; L++) {
                if (idx % WS[L]) break;
                double e = cur[L][3];
                for (int t = 0; t < 3; t++) { double dlt = cur[L][t] - e; sq[L][t] += dlt * dlt; }
                sv_[L] += cur[L][4]; nwin[L]++;
                if (L == 0) for (int t = 0; t < 5; t++) tot[t] += cur[L][t];
                if (L + 1 < NW) for (int t = 0; t < 5; t++) cur[L + 1][t] += cur[L][t];
                memset(cur[L], 0, sizeof cur[L]);
            }
        }
        printf("{\"c\": %d, \"D\": %lld, \"C\": %.6f, \"s\": %.6f, \"real\": %.0f, \"coin\": %.0f, \"sched\": %.0f, \"e\": %.3f, \"v\": %.3f, \"rungs\": [",
               c, (long long)D, Cd, sd, tot[0], tot[1], tot[2], tot[3], tot[4]);
        for (int L = 0; L < NW; L++)
            printf("%s[%llu, %ld, %.6f, %.6f, %.6f, %.6f]", L ? ", " : "", (unsigned long long)WS[L], nwin[L], sq[L][0], sq[L][1], sq[L][2], sv_[L]);
        printf("]}\n");
        fflush(stdout);
    }
    return 0;
}
