/* P13 locked seams. Layer m holds T(m-1)+1 .. T(m-1)+m. z-locked: m%4 in {0,1} and m%p in {0,1} for odd p<=z.
 * usage: p13 z M0 M1 hmax nctrl hctrl seed   -> JSON on stdout
 * locked: every z-locked m in [M0,M1): desert check, tick 1, prime counts in ticks 1..h (h <= hmax, binned by h list)
 * control: nctrl uniform random m in [M0,M1), ticks 1..min(hctrl,m)                                                 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
typedef unsigned __int128 u128;
static inline uint64_t mulm(uint64_t a, uint64_t b, uint64_t m) {   /* m < 2^63, x87 long double */
    uint64_t c = (uint64_t)((long double)a * b / m);
    int64_t r = (int64_t)(a * b - c * m) % (int64_t)m; return r < 0 ? (uint64_t)(r + (int64_t)m) : (uint64_t)r; }
static uint64_t powm(uint64_t a, uint64_t e, uint64_t m) { uint64_t r = 1; a %= m; while (e) { if (e & 1) r = mulm(r, a, m); a = mulm(a, a, m); e >>= 1; } return r; }
static int isprime(uint64_t n) {
    if (n < 2) return 0;
    static const uint64_t sp[] = {2,3,5,7,11,13,17,19,23,29,31,37};
    for (int i = 0; i < 12; i++) { if (n == sp[i]) return 1; if (n % sp[i] == 0) return 0; }
    uint64_t d = n - 1; int s = 0; while (!(d & 1)) { d >>= 1; s++; }
    static const uint64_t B[] = {2, 325, 9375, 28178, 450775, 9780504, 1795265022};
    for (int i = 0; i < 7; i++) {
        uint64_t a = B[i] % n; if (a == 0) continue;
        uint64_t x = powm(a, d, n); if (x == 1 || x == n - 1) continue;
        int ok = 0; for (int r = 1; r < s; r++) { x = mulm(x, x, n); if (x == n - 1) { ok = 1; break; } }
        if (!ok) return 0;
    }
    return 1;
}
static uint64_t rng = 88172645463325252ull;
static uint64_t xr(void) { rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }
int main(int argc, char **argv) {
    int z = atoi(argv[1]); long M0 = atol(argv[2]), M1 = atol(argv[3]); long hmax = atol(argv[4]);
    long nctrl = atol(argv[5]); long hctrl = atol(argv[6]); rng ^= (uint64_t)atol(argv[7]) * 0x9E3779B97F4A7C15ull;
    long stride = argc > 8 ? atol(argv[8]) : 1; long seen = 0;
    static const double LAM[] = {1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.76, 3, 3.5, 4};
    long H[10]; for (int i = 0; i < 10; i++) H[i] = (long)floor(pow(z, LAM[i]) + 1e-9);
    int ps[16], np = 0; for (int p = 3; p <= z; p += 2) { int q = 1; for (int d = 3; d * d <= p; d += 2) if (p % d == 0) q = 0; if (q) ps[np++] = p; }
    int pnext = z + 1; for (;; pnext++) { int q = 1; for (int d = 2; d * d <= pnext; d++) if (pnext % d == 0) q = 0; if (q) break; }
    uint64_t Pz = 2; for (int i = 0; i < np; i++) Pz *= ps[i];
    /* coprime k list up to hmax */
    long *kc = malloc(sizeof(long) * (hmax + 1)); long nk = 0;
    for (long k = 1; k <= hmax; k++) { int ok = (k & 1); for (int i = 0; ok && i < np; i++) if (k % ps[i] == 0) ok = 0; if (ok) kc[nk++] = k; }
    /* sieve primes for pre-filtering (37 < p < 200) */
    int sv[64], ns = 0; for (int p = 41; p < 200; p += 2) { int q = 1; for (int d = 3; d * d <= p; d += 2) if (p % d == 0) q = 0; if (q) sv[ns++] = p; }
    long nl = 0, desert_bad = 0, t1 = 0; double t1e = 0, lnsumL = 0; long cntL[10] = {0}; long nlH[10] = {0}; double lnL[10] = {0};
    for (long m = M0; m < M1; m++) {
        int r4 = m & 3; if (r4 > 1) continue;
        int ok = 1; for (int i = 0; ok && i < np; i++) { long r = m % ps[i]; if (r > 1) ok = 0; }
        if (!ok) continue;
        uint64_t base = (uint64_t)(m - 1) * (uint64_t)m / 2;
        if (base % Pz) { fprintf(stderr, "lock fail m=%ld\n", m); return 1; }
        if (seen++ % stride) continue;
        nl++;
        for (int k = 2; k < pnext; k++) if (isprime(base + k)) desert_bad++;
        if (isprime(base + 1)) t1++;
        t1e += 1.0 / log((double)(base + 1));
        double il = 1.0 / log((double)base); lnsumL += il;
        long rem[64]; for (int j = 0; j < ns; j++) rem[j] = base % sv[j];
        int hb = 0; long c = 0;
        for (long i = 0; i < nk; i++) {
            long k = kc[i]; if (k > m) break;
            while (hb < 10 && k > H[hb]) { if (H[hb] <= m) { cntL[hb] += c; nlH[hb]++; lnL[hb] += il; } hb++; }
            if (hb == 10) break;
            int cmp = 0; for (int j = 0; j < ns; j++) { long rr = (rem[j] + k) % sv[j]; if (rr == 0 && base + k != (uint64_t)sv[j]) { cmp = 1; break; } }
            if (!cmp && isprime(base + k)) c++;
        }
        while (hb < 10 && H[hb] <= hmax) { if (H[hb] <= m) { cntL[hb] += c; nlH[hb]++; lnL[hb] += il; } hb++; }
    }
    long cntC[10] = {0}, ncH[10] = {0}; double lnC[10] = {0};
    for (long n = 0; n < nctrl; n++) {
        long m = M0 + (long)(xr() % (uint64_t)(M1 - M0));
        uint64_t base = (uint64_t)(m - 1) * (uint64_t)m / 2; double il = 1.0 / log((double)base);
        long rem[64]; static const int sp2[] = {3,5,7,11,13,17,19,23,29,31,37}; long r2[11];
        for (int j = 0; j < ns; j++) rem[j] = base % sv[j];
        for (int j = 0; j < 11; j++) r2[j] = base % sp2[j];
        int hb = 0; long c = 0;
        for (long k = 1; k <= hctrl && k <= m; k++) {
            while (hb < 10 && k > H[hb]) { cntC[hb] += c; ncH[hb]++; lnC[hb] += il; hb++; }
            if (hb == 10) break;
            uint64_t v = base + k; if (!(v & 1)) continue;
            int cmp = 0;
            for (int j = 0; j < 11; j++) if ((r2[j] + k) % sp2[j] == 0) { cmp = 1; break; }
            if (!cmp) for (int j = 0; j < ns; j++) if ((rem[j] + k) % sv[j] == 0) { cmp = 1; break; }
            if (!cmp && isprime(v)) c++;
        }
        while (hb < 10 && H[hb] <= hctrl) { cntC[hb] += c; ncH[hb]++; lnC[hb] += il; hb++; }
    }
    printf("{\"stride\":%ld,\"z\":%d,\"M0\":%ld,\"M1\":%ld,\"locked_layers\":%ld,\"desert_exceptions\":%ld,\"pnext\":%d,", stride, z, M0, M1, nl, desert_bad, pnext);
    printf("\"tick1_primes\":%ld,\"tick1_sum_invln\":%.6f,\"windows\":[", t1, t1e);
    for (int i = 0; i < 10; i++) printf("%s{\"lam\":%g,\"h\":%ld,\"locked_n\":%ld,\"locked_primes\":%ld,\"locked_sum_invln\":%.6f,\"ctrl_n\":%ld,\"ctrl_primes\":%ld,\"ctrl_sum_invln\":%.6f}",
        i ? "," : "", LAM[i], H[i], nlH[i], cntL[i], lnL[i], ncH[i], cntC[i], lnC[i]);
    printf("]}\n"); return 0;
}
