/*
 * layer_gap.c — the Prime Tread Wheel's gap conjecture, pushed far.
 *
 * Conjecture (OEIS A066888 / Sierpinski Hypothesis H1 at this instance):
 * every layer m >= 2 of the wheel holds at least one prime, where layer m
 * holds the integers T(m-1)+1 .. T(m), T(m) = m(m+1)/2.
 *
 *   stats MODE  (single-thread, sequential):
 *       sieve to T(M) in segments, walk primes in order, and record for
 *       every layer m its largest internal run of consecutive composites
 *       ("margin", 0 <= margin <= m; margin == m means the layer is empty).
 *       Reports: empty layers, worst margin ratio margin[m]/m, largest prime
 *       gap and where, and the max margin with its layer.
 *
 *   verify MODE (OpenMP, segmented, order-free):
 *       for every prime found anywhere in [2, T(M)], mark its layer as
 *       occupied (benign byte-write races). At the end, count layers in
 *       [2, M] with no prime. Reports nothing else; this is the pure
 *       "checked to layer M" pass.
 *
 * Usage: layer_gap stats M | layer_gap verify M [threads]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>
#include <omp.h>

static inline uint64_t T(uint64_t m){ return m*(m+1)/2; }

/* layer(x) = m  iff  T(m-1) < x <= T(m) */
static inline uint64_t layer_of(uint64_t x){
    long double d = sqrtl((long double)8.0L*(long double)x + 1.0L);
    uint64_t m = (uint64_t)((d - 1.0L)/2.0L);
    while (( __int128)m*(m+1)/2 < x) m++;
    while (( __int128)m*(m-1)/2 >= x) m--;
    return m;
}

/* sieve odd base primes up to and including lim; returns count, fills primes[] */
static uint64_t base_primes(uint64_t lim, uint32_t **out){
    uint64_t nodd = lim/2 + 1;                 /* odd numbers 1,3,..,lim-ish */
    uint64_t words = nodd/64 + 1;
    uint64_t *bits = calloc(words, 8);
    if(!bits){ fprintf(stderr,"oom base\n"); exit(1); }
    for(uint64_t i = 0; i < words; i++) bits[i] = ~0ULL;
    bits[0] &= ~1ULL;                          /* 1 is not prime */
    uint64_t rl = (uint64_t)sqrtl((long double)lim) + 1;
    for(uint64_t p = 3; p <= rl; p += 2){
        uint64_t idx = p/2;
        if(!(bits[idx/64] & (1ULL<<(idx%64)))) continue;
        for(uint64_t j = (p*p)/2; j < nodd; j += p)
            bits[j/64] &= ~(1ULL<<(j%64));
    }
    uint64_t cnt = 1;                          /* the prime 2 */
    for(uint64_t i = 1; i < nodd; i++)
        if(bits[i/64] & (1ULL<<(i%64))) cnt++;
    uint32_t *pr = malloc(cnt * 4);
    if(!pr){ fprintf(stderr,"oom base primes\n"); exit(1); }
    uint64_t k = 0; pr[k++] = 2;
    for(uint64_t i = 1; i < nodd; i++)
        if(bits[i/64] & (1ULL<<(i%64))) pr[k++] = (uint32_t)(2*i+1);
    free(bits);
    *out = pr;
    return cnt;
}

/* ---------------- stats mode ---------------- */
static int run_stats(uint64_t M){
    uint64_t N = T(M);
    if(N < 100) N = 100;
    uint32_t *margin = calloc(M+1, 4);
    uint8_t  *ok     = calloc(M+1, 1);
    if(!margin || !ok){ fprintf(stderr,"oom stats arrays\n"); return 1; }
    uint32_t *bp; uint64_t bpc = base_primes((uint64_t)sqrtl((long double)N)+2, &bp);

    const uint64_t S = 1ULL<<27;               /* odd numbers per segment */
    uint64_t nodd = N/2 + 1;
    uint64_t *bits = malloc(S/8);
    if(!bits){ fprintf(stderr,"oom window\n"); return 1; }

    uint64_t prev = 2;                         /* last prime seen */
    uint64_t mcur = 2;                         /* layer of the next composite we'll touch */
    uint64_t Tm   = T(2);                      /* T(mcur) */
    uint64_t maxgap = 0, maxgap_at = 0;
    ok[2] = 1;
    uint64_t prime_count = 1;

    struct timespec t0, t1; clock_gettime(CLOCK_MONOTONIC, &t0);

    for(uint64_t seg = 0; seg*S < nodd; seg++){
        uint64_t ilo = seg*S, ihi = ilo + S; if(ihi > nodd) ihi = nodd;
        uint64_t cnt = ihi - ilo;
        memset(bits, 0xFF, (cnt+63)/64 * 8);
        if(seg == 0) bits[0] &= ~1ULL;         /* the number 1 is not prime */
        uint64_t hi_num = 2*(ihi-1)+1;
        for(uint64_t k = 1; k < bpc; k++){     /* skip prime 2: odd-only bitmap */
            uint64_t p = bp[k];
            if(p*p > hi_num) break;
            uint64_t lo_num = 2*ilo+1;
            uint64_t start = (lo_num + p - 1)/p * p;
            if(start < p*p) start = p*p;
            if(start & 1) {} else start += p;
            for(uint64_t j = (start - lo_num)/2; j < cnt; j += p)
                bits[j/64] &= ~(1ULL<<(j%64));
        }
        for(uint64_t wi = 0; wi < (cnt+63)/64; wi++){
            uint64_t w = bits[wi];
            while(w){
                int b = __builtin_ctzll(w);
                w &= w-1;
                uint64_t q = 2*(ilo + wi*64 + b)+1;
                if(q > N) continue;
                prime_count++;
                if(q - prev > maxgap){ maxgap = q - prev; maxgap_at = prev; }
                /* walk the composite run (prev, q) across layers */
                uint64_t a = prev + 1;
                if(a > Tm){ while(a > Tm){ mcur++; Tm = T(mcur); } }
                while(a < q && mcur <= M){
                    while(a > Tm && mcur < M){ mcur++; Tm = T(mcur); }
                    uint64_t top = Tm < (q-1) ? Tm : (q-1);
                    uint64_t portion = top - a + 1;
                    if(portion > margin[mcur]) margin[mcur] = portion;
                    a = top + 1;
                    if(mcur < M){ mcur++; Tm = T(mcur); }
                }
                uint64_t mq = layer_of(q);
                if(mq <= M) ok[mq] = 1;
                mcur = mq; Tm = T(mcur);
                prev = q;
            }
        }
    }
    clock_gettime(CLOCK_MONOTONIC, &t1);
    double dt = (t1.tv_sec - t0.tv_sec) + 1e-9*(t1.tv_nsec - t0.tv_nsec);

    uint64_t empty = 0, first_empty = 0;
    for(uint64_t m = 2; m <= M; m++) if(!ok[m]){ if(!empty) first_empty = m; empty++; }
    double worst = 0; uint64_t worst_m = 0;
    for(uint64_t m = 100; m <= M; m++){
        double r = (double)margin[m]/m;
        if(r > worst){ worst = r; worst_m = m; }
    }
    uint64_t maxm = 0, maxm_at = 0;
    for(uint64_t m = 2; m <= M; m++) if(margin[m] > maxm){ maxm = margin[m]; maxm_at = m; }

    printf("stats to layer %llu (T = %llu)\n", (unsigned long long)M, (unsigned long long)T(M));
    printf("  primes found          : %llu\n", (unsigned long long)prime_count);
    printf("  empty layers          : %llu%s\n", (unsigned long long)empty,
           empty ? "" : "  (conjecture holds in range)");
    if(empty) printf("  first empty layer     : %llu\n", (unsigned long long)first_empty);
    printf("  largest prime gap     : %llu at %llu\n", (unsigned long long)maxgap, (unsigned long long)maxgap_at);
    printf("  worst margin from m=100: %.4f of layer width at m=%llu\n", worst, (unsigned long long)worst_m);
    printf("  largest margin        : %llu at m=%llu (width %llu)\n",
           (unsigned long long)maxm, (unsigned long long)maxm_at, (unsigned long long)maxm_at);
    printf("  time                  : %.1f s\n", dt);
    free(margin); free(ok); free(bp); free(bits);
    return 0;
}

/* ---------------- verify mode ---------------- */
static int run_verify(uint64_t M, int threads){
    uint64_t N = T(M);
    uint32_t *bp; uint64_t bpc = base_primes((uint64_t)sqrtl((long double)N)+2, &bp);
    uint8_t *ok = calloc(M+1, 1);
    if(!ok){ fprintf(stderr,"oom ok array\n"); return 1; }
    ok[2] = 1;                                 /* primes 2 and 3 both sit in layer 2 */
    const uint64_t S = 1ULL<<27;               /* odd numbers per segment */
    uint64_t nodd = N/2 + 1;
    uint64_t nseg = (nodd + S - 1)/S;
    struct timespec t0, t1; clock_gettime(CLOCK_MONOTONIC, &t0);
    uint64_t done = 0;

    omp_set_num_threads(threads);
    #pragma omp parallel
    {
        uint64_t *bits = malloc(S/8);
        #pragma omp for schedule(dynamic, 64)
        for(uint64_t seg = 0; seg < nseg; seg++){
            uint64_t ilo = seg*S, ihi = ilo + S; if(ihi > nodd) ihi = nodd;
            uint64_t cnt = ihi - ilo;
            memset(bits, 0xFF, (cnt+63)/64 * 8);
            if(seg == 0) bits[0] &= ~1ULL;     /* the number 1 is not prime */
            uint64_t lo_num = 2*ilo+1, hi_num = 2*(ihi-1)+1;
            for(uint64_t k = 1; k < bpc; k++){
                uint64_t p = bp[k];
                if(p*p > hi_num) break;
                uint64_t start = (lo_num + p - 1)/p * p;
                if(start < p*p) start = p*p;
                if(!(start & 1)) start += p;
                for(uint64_t j = (start - lo_num)/2; j < cnt; j += p)
                    bits[j/64] &= ~(1ULL<<(j%64));
            }
            uint64_t nw = (cnt+63)/64;
            for(uint64_t wi = 0; wi < nw; wi++){
                uint64_t w = bits[wi];
                if(!w) continue;
                uint64_t base = ilo + wi*64;
                uint64_t p_lo = 2*(base + __builtin_ctzll(w))+1;
                uint64_t p_hi = 2*(base + 63 - __builtin_clzll(w))+1;
                uint64_t m_a = layer_of(p_lo), m_b = layer_of(p_hi);
                if(m_a == m_b){ ok[m_a] = 1; continue; }
                /* word spans a layer boundary (only possible for small layers) */
                uint64_t ww = w;
                while(ww){
                    int b = __builtin_ctzll(ww);
                    ww &= ww-1;
                    ok[layer_of(2*(base + b)+1)] = 1;
                }
            }
            #pragma omp atomic
            done++;
            if((done & 4095) == 0)
                fprintf(stderr, "\r  %llu/%llu segments (%.0f%%)", (unsigned long long)done,
                        (unsigned long long)nseg, 100.0*done/nseg);
        }
        free(bits);
    }
    clock_gettime(CLOCK_MONOTONIC, &t1);
    double dt = (t1.tv_sec - t0.tv_sec) + 1e-9*(t1.tv_nsec - t0.tv_nsec);

    uint64_t empty = 0, first_empty = 0;
    for(uint64_t m = 2; m <= M; m++) if(!ok[m]){ if(!empty) first_empty = m; empty++; }
    printf("\nverify to layer %llu (T = %llu)\n", (unsigned long long)M, (unsigned long long)N);
    printf("  empty layers          : %llu%s\n", (unsigned long long)empty,
           empty ? "" : "  (conjecture holds in range)");
    if(empty){
        printf("  first empty layer     : %llu\n", (unsigned long long)first_empty);
        uint64_t shown = 0;
        for(uint64_t m = 2; m <= M && shown < 10; m++) if(!ok[m]){ printf("  empty: %llu\n", (unsigned long long)m); shown++; }
    }
    printf("  time                  : %.1f s\n", dt);
    free(ok); free(bp);
    return empty ? 2 : 0;
}

int main(int argc, char **argv){
    if(argc < 3){ fprintf(stderr, "usage: %s stats M | verify M [threads]\n", argv[0]); return 1; }
    uint64_t M = strtoull(argv[2], 0, 10);
    int threads = argc > 3 ? atoi(argv[3]) : 24;
    if(!strcmp(argv[1], "stats"))  return run_stats(M);
    if(!strcmp(argv[1], "verify")) return run_verify(M, threads);
    fprintf(stderr, "unknown mode\n");
    return 1;
}
