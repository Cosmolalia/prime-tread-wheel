/* layerstats.c — primes per layer of the tread wheel, layers 1..MTOP, exact, multithreaded.
 *
 * Layer m holds the m numbers T(m-1)+1 .. T(m), T(n) = n(n+1)/2.
 * Per layer it records:
 *   count    primes on the layer
 *   run      longest stretch of consecutive non-prime ticks on the layer (edges included)
 *   indep    m * prod_{p <= sqrt T(m)} (1 - 1/p): the count if the deciding rings acted independently
 * Summary per decade of m: fewest primes, worst count vs m/ln T(m), longest run as share of the layer,
 * and the CLASH FACTOR = sum(count) / sum(indep). Prediction: e^gamma / 2 = 0.8905 at every scale
 * (the independent guess books ring clashes at distances p*q longer than the whole number line).
 *
 * build: gcc -O3 -march=native -fopenmp -o layerstats layerstats.c -lm
 * run:   ./layerstats 1800000 layers.csv      (layer 1.8M = numbers to 1.6e12)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <omp.h>
typedef uint64_t u64;

static u64 nb; static u64 *bp; static double *logprod;   /* logprod[i] = sum_{j<=i} log(1-1/bp[j]) */
static inline u64 T(u64 n) { return n * (n + 1) / 2; }
static u64 isq(u64 x) { u64 r = (u64)sqrtl((long double)x); while (r * r > x) r--; while ((r + 1) * (r + 1) <= x) r++; return r; }

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: layerstats MTOP [layers.csv]\n"); return 1; }
    u64 MT = strtoull(argv[1], 0, 10), NT = T(MT), R = isq(NT) + 1;
    char *sm = calloc(R + 1, 1); bp = malloc(sizeof(u64) * (R / 2 + 100)); logprod = malloc(sizeof(double) * (R / 2 + 100));
    double acc = 0;
    for (u64 i = 2; i <= R; i++) if (!sm[i]) { bp[nb] = i; acc += log1p(-1.0 / i); logprod[nb] = acc; nb++; for (u64 j = i * i; j <= R; j += i) sm[j] = 1; }
    free(sm);
    uint32_t *cnt = calloc(MT + 1, 4), *run = calloc(MT + 1, 4);
    const u64 CH = 256;                                       /* layers per work chunk */
    u64 nch = (MT + CH - 1) / CH;
    double t0 = omp_get_wtime();
    #pragma omp parallel
    {
        u64 SEGMAX = 1 << 24; char *seg = malloc(SEGMAX);
        #pragma omp for schedule(dynamic, 1)
        for (u64 c = 0; c < nch; c++) {
            u64 ma = 1 + c * CH, mb = ma + CH - 1; if (mb > MT) mb = MT;
            u64 lo0 = T(ma - 1) + 1, hi0 = T(mb);
            u64 m = ma, layEnd = T(ma), cur = 0, best = 0, k = 0;
            for (u64 lo = lo0; lo <= hi0; lo += SEGMAX) {
                u64 hi = lo + SEGMAX - 1; if (hi > hi0) hi = hi0;
                memset(seg, 0, hi - lo + 1);
                for (u64 i = 0; i < nb; i++) {
                    u64 p = bp[i]; if (p * p > hi) break;
                    u64 s = (lo + p - 1) / p * p; if (s < p * p) s = p * p;
                    for (u64 x = s; x <= hi; x += p) seg[x - lo] = 1;
                }
                for (u64 v = lo; v <= hi; v++) {
                    int isp = v > 1 && !seg[v - lo];
                    if (isp) { k++; if (cur > best) best = cur; cur = 0; } else cur++;
                    if (v == layEnd) {
                        if (cur > best) best = cur;
                        cnt[m] = (uint32_t)k; run[m] = (uint32_t)best;
                        m++; k = 0; cur = 0; best = 0; layEnd += m;
                    }
                }
            }
        }
        free(seg);
    }
    double t1 = omp_get_wtime();

    FILE *f = argc > 2 ? fopen(argv[2], "w") : 0;
    if (f) fprintf(f, "m,count,longest_run,indep\n");
    printf("layers 1..%llu, numbers to %llu, %.1f s on %d threads\n", (unsigned long long)MT, (unsigned long long)NT, t1 - t0, omp_get_max_threads());
    printf("%-18s %10s %12s %10s %14s %12s\n", "layers", "fewest", "worst/exp", "at m", "longest run/m", "clash");
    if (f) for (u64 m = 1; m < 10 && m <= MT; m++) fprintf(f, "%llu,%u,%u,\n", (unsigned long long)m, cnt[m], run[m]);
    u64 dlo = 10, ri = 0; int lastc[11]; u64 lastm[11] = {0}; (void)lastc;
    u64 total = 0;
    while (dlo <= MT) {
        u64 dhi = dlo * 10 - 1; if (dhi > MT) dhi = MT;
        u64 fewest = ~0ULL; double worst = 1e9; u64 worstm = 0; double runr = 0; double sc = 0, si = 0;
        for (u64 m = dlo; m <= dhi; m++) {
            u64 sq = isq(T(m));
            while (ri + 1 < nb && bp[ri + 1] <= sq) ri++;
            while (ri > 0 && bp[ri] > sq) ri--;
            double indep = m * exp(logprod[ri]);
            if (f) fprintf(f, "%llu,%u,%u,%.2f\n", (unsigned long long)m, cnt[m], run[m], indep);
            if (cnt[m] < fewest) fewest = cnt[m];
            double ex = m / log((double)T(m)), w = cnt[m] / ex; if (w < worst) { worst = w; worstm = m; }
            double rr = (double)run[m] / m; if (rr > runr) runr = rr;
            sc += cnt[m]; si += indep;
        }
        printf("%-8llu-%-9llu %10llu %12.3f %10llu %14.5f %12.5f\n", (unsigned long long)dlo, (unsigned long long)dhi,
               (unsigned long long)fewest, worst, (unsigned long long)worstm, runr, sc / si);
        dlo *= 10;
    }
    for (u64 m = 1; m <= MT; m++) { total += cnt[m]; for (int c = 0; c <= 10; c++) if (cnt[m] <= (u64)c) lastm[c] = m; }
    if (f) fclose(f);
    printf("total primes %llu\nlast layer with <= c primes:", (unsigned long long)total);
    for (int c = 0; c <= 10; c++) printf(" %d:%llu", c, (unsigned long long)lastm[c]);
    printf("\nclash factor prediction e^gamma/2 = %.5f\n", exp(0.5772156649015329) / 2);
    return 0;
}
