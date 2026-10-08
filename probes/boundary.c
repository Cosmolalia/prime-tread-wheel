/*
 * boundary.c — the wheel's gap conjecture, layer by layer, at height.
 *
 * For each layer m in [2, M]: layer m holds (T(m-1), T(m)]. Find the FIRST
 * prime above T(m-1) by sieving a small odd-only window with the primes up
 * to 1000, then ascending deterministic Miller-Rabin (12 bases, exact below
 * 3.3e24 — our range stops near 5e17) on the survivors. If the first prime
 * is <= T(m) the layer holds a prime. Window 65536 numbers always suffices
 * below 4e18 (max prime gap there is 1476, Oliveira e Silva et al.), but a
 * fallback grows the window and reports if it ever fires.
 *
 * Tracks: max bottom-margin d(m) = (first prime > T(m-1)) - T(m-1) - 1,
 * the layer attaining it, max ratio d(m)/m, and any empty layer.
 *
 * Output lines:
 *   D <m> <d>            new record bottom margin
 *   EMPTY <m>            layer with no prime (should never occur)
 *   SUMMARY ...          final aggregates
 *
 * Usage: boundary M [threads] [chunk]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>
#include <omp.h>

static inline uint64_t T(uint64_t m){ return m*(m+1)/2; }

/* ---- deterministic Miller-Rabin, 12 bases, exact for n < 3.317e24 ---- */
static inline uint64_t mulmod(uint64_t a, uint64_t b, uint64_t m){
    return (uint64_t)(((__uint128_t)a * b) % m);
}
static inline uint64_t powmod(uint64_t a, uint64_t d, uint64_t m){
    uint64_t r = 1;
    while(d){
        if(d & 1) r = mulmod(r, a, m);
        a = mulmod(a, a, m);
        d >>= 1;
    }
    return r;
}
static int is_prime_mr(uint64_t n){
    if(n < 2) return 0;
    static const uint32_t small[] = {2,3,5,7,11,13,17,19,23,29,31,37};
    for(int i = 0; i < 12; i++){
        if(n == small[i]) return 1;
        if(n % small[i] == 0) return 0;
    }
    uint64_t d = n - 1, s = 0;
    while(!(d & 1)){ d >>= 1; s++; }
    for(int i = 0; i < 12; i++){
        uint64_t a = small[i] % n;
        if(a < 2) continue;
        uint64_t x = powmod(a, d, n);
        if(x == 1 || x == n-1) continue;
        int comp = 1;
        for(uint64_t r = 1; r < s; r++){
            x = mulmod(x, x, n);
            if(x == n-1){ comp = 0; break; }
        }
        if(comp) return 0;
    }
    return 1;
}

/* ---- base primes up to 1000 ---- */
static uint32_t BP[200]; static int BPN;
static void init_bp(void){
    char comp[1001] = {0};
    for(int p = 2; p <= 1000; p++) if(!comp[p])
        for(int j = p*p; j <= 1000; j += p) comp[j] = 1;
    for(int p = 3; p <= 1000; p++) if(!comp[p]) BP[BPN++] = p;
}

#define W 65536                              /* window span, must stay < (max gap)^2-ish */

/* first prime > lo, assuming lo >= 3; returns 0 on failure (no fallback here) */
static uint64_t first_prime_above(uint64_t lo, uint64_t *tries){
    uint8_t bits[W/16 + 1];                  /* bit j -> odd number lo+2j (lo even) */
    uint64_t span = W;
    memset(bits, 0xFF, sizeof(bits));
    for(int k = 0; k < BPN; k++){
        uint64_t p = BP[k];
        uint64_t start = (lo + p - 1)/p * p;
        if(!(start & 1)) start += p;
        if(start == p) start += 2*p;         /* never mark p itself */
        for(uint64_t j = (start - lo)/2; j < span/2; j += p)
            bits[j>>3] &= ~(1u << (j&7));
    }
    for(uint64_t j = 0; j < span/2; j++){
        if(!(bits[j>>3] & (1u << (j&7)))) continue;
        uint64_t x = lo + 2*j + 1;
        (*tries)++;
        if(is_prime_mr(x)) return x;
    }
    return 0;
}

int main(int argc, char **argv){
    if(argc < 2){ fprintf(stderr, "usage: boundary M [threads] [chunk]\n"); return 1; }
    uint64_t M = strtoull(argv[1], 0, 10);
    int threads = argc > 2 ? atoi(argv[2]) : 30;
    uint64_t chunk = argc > 3 ? strtoull(argv[3], 0, 10) : 16384;
    init_bp();
    omp_set_num_threads(threads);

    uint64_t g_max_d = 0, g_max_d_m = 0;
    double   g_max_r = 0; uint64_t g_max_r_m = 0;
    uint64_t g_empty = 0, g_first_empty = 0, g_fallback = 0;
    uint64_t g_tries = 0;
    struct timespec t0, t1; clock_gettime(CLOCK_MONOTONIC, &t0);
    uint64_t ndone = 0;

    #pragma omp parallel
    {
        uint64_t l_max_d = 0, l_max_d_m = 0, l_max_r_m = 0; double l_max_r = 0;
        uint64_t l_empty = 0, l_first_empty = 0, l_tries = 0, l_fallback = 0;
        #pragma omp for schedule(dynamic, 8) nowait
        for(uint64_t c0 = 2; c0 <= M; c0 += chunk){
            uint64_t c1 = c0 + chunk - 1; if(c1 > M) c1 = M;
            for(uint64_t m = c0; m <= c1; m++){
                uint64_t lo = T(m-1);
                if(lo & 1) lo++;             /* window starts even */
                uint64_t tries = 0;
                uint64_t p = first_prime_above(lo, &tries);
                l_tries += tries;
                if(!p){                      /* fallback: extend one window at a time */
                    l_fallback++;
                    uint64_t probe = lo;
                    while(!p && probe < lo + (uint64_t)W*64){ probe += W; p = first_prime_above(probe, &tries); l_tries += tries; }
                    if(!p && !l_empty) l_first_empty = m;
                    if(!p) l_empty++;
                }
                if(p){
                    uint64_t d = p > T(m-1) ? p - T(m-1) - 1 : 0;
                    if(d > l_max_d){ l_max_d = d; l_max_d_m = m; }
                    if(m >= 100){
                        double r = (double)d/m;
                        if(r > l_max_r){ l_max_r = r; l_max_r_m = m; }
                    }
                }
            }
            #pragma omp atomic
            ndone += chunk;
            if(ndone % (chunk*512) < chunk)
                fprintf(stderr, "\r  %.1f%%", 100.0*ndone/M);
        }
        #pragma omp critical
        {
            if(l_max_d > g_max_d){ g_max_d = l_max_d; g_max_d_m = l_max_d_m; }
            if(l_max_r > g_max_r){ g_max_r = l_max_r; g_max_r_m = l_max_r_m; }
            g_empty += l_empty; if(!g_first_empty && l_first_empty) g_first_empty = l_first_empty;
            g_tries += l_tries; g_fallback += l_fallback;
        }
    }
    clock_gettime(CLOCK_MONOTONIC, &t1);
    double dt = (t1.tv_sec - t0.tv_sec) + 1e-9*(t1.tv_nsec - t0.tv_nsec);

    printf("\nSUMMARY boundary M=%llu\n", (unsigned long long)M);
    printf("  empty layers        : %llu%s\n", (unsigned long long)g_empty,
           g_empty ? "" : "  (conjecture holds in range)");
    if(g_empty) printf("  first empty         : %llu\n", (unsigned long long)g_first_empty);
    printf("  fallback windows    : %llu\n", (unsigned long long)g_fallback);
    printf("  max bottom margin d : %llu at m=%llu (T=%llu)\n",
           (unsigned long long)g_max_d, (unsigned long long)g_max_d_m,
           (unsigned long long)T(g_max_d_m));
    printf("  max ratio d/m       : %.6f at m=%llu\n", g_max_r, (unsigned long long)g_max_r_m);
    printf("  MR tests performed  : %llu\n", (unsigned long long)g_tries);
    printf("  time                : %.1f s\n", dt);
    return g_empty ? 2 : 0;
}
