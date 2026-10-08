/*
 * shadows.c — who kills whom, wheel-natively.
 *
 * Layer m holds values (T(m-1), T(m)], tick k at value T(m-1)+k, seats are
 * ticks with gcd(k,m)=1. This probe sieves EVERY tick value up to sqrt(T(m))
 * and records, per seat, the SMALLEST outside prime whose shadow falls on it
 * (k ≡ -T(m-1) (mod p)). After the pass:
 *
 *   cover == 0            -> the seat's value is prime (sieved to sqrt)
 *   cover == p            -> p is the value's smallest prime factor
 *
 * No Miller-Rabin needed: the sieve to sqrt is exact.
 *
 * The wheel only routes primes dividing m (the visit theorem). Every other
 * covering prime is invisible to the lap — that invisibility IS the gap the
 * conjecture lives in. This probe maps it seat by seat.
 *
 * Modes:
 *   shadows <m>            one layer: full report + per-prime cover counts
 *                          + binary head map (first <=4M seats) for anatomy
 *   shadows -b <c> <n>     batch: n prime layers near center c, one summary
 *                          line each (for near-miss-vs-typical comparison)
 *
 * Output (single mode), stdout:
 *   LAYER m=.. prime=.. lo=.. hi=.. lim=.. seats=.. shadowed=.. primes=..
 *         sumcov=.. overlap=.. first_off=.. maxgap=.. gapat=.. junction_prime=..
 *   COVER <p> <count>      one line per covering prime
 *   Head map -> shadows_<m>_head.bin (u32 per tick, 0 = prime/unshadowed)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>

static inline uint64_t T(uint64_t m){ return m*(m+1)/2; }

#define SEG (1u<<22)            /* seats per segment */

static uint32_t *PR;            /* primes up to lim */
static uint64_t NP;
static uint64_t LIM;

static void gen_primes(uint64_t lim){
    LIM = lim;
    NP = 0;
    uint8_t *comp = calloc(lim + 1, 1);
    PR = malloc((lim/10 + 1000) * sizeof(uint32_t));
    for(uint64_t i = 2; i <= lim; i++){
        if(comp[i]) continue;
        PR[NP++] = (uint32_t)i;
        if(i <= lim/i) for(uint64_t j = i*i; j <= lim; j += i) comp[j] = 1;
    }
    free(comp);
}

static int is_prime_trial(uint64_t n){   /* works while sqrt(n) <= LIM */
    if(n < 2) return 0;
    for(uint64_t i = 0; i < NP && (uint64_t)PR[i]*PR[i] <= n; i++)
        if(n % PR[i] == 0) return n == PR[i];
    return 1;
}

static inline int seat_p(uint64_t k, uint64_t m, int mprime){
    if(mprime) return 1;
    uint64_t a = k, b = m;
    while(b){ uint64_t t = a % b; a = b; b = t; }
    return a == 1;
}

typedef struct {
    uint64_t m, lo, hi, seats, shadowed, primes, sumcov, overlap;
    uint64_t first_off, maxgap, gapat, prv_off;
    uint64_t iprimes, ifirst_off, imaxgap, igapat, iprv;  /* interval primes (any tick) */
    uint64_t ilprimes, irprimes;  /* interval primes left / right of lap midpoint */
    uint64_t mouth_seats, mouth_distinct, mouth_largest;   /* leading-run anatomy */
    int mprime, junction_prime;
    uint32_t *count;            /* count[p] = seats whose smallest covering prime is p */
} Report;

static void run_layer(uint64_t m, Report *R, int dump_head, int want_mouth){
    memset(R, 0, sizeof *R);
    R->m = m;
    R->lo = T(m-1);
    R->hi = T(m);
    gen_primes((uint64_t)sqrtl((long double)R->hi) + 1);
    R->mprime = is_prime_trial(m);
    R->junction_prime = is_prime_trial(R->hi);

    uint64_t lim = LIM, lo = R->lo;
    R->count = calloc(lim + 1, sizeof(uint32_t));
    uint32_t *cov = malloc(SEG * sizeof(uint32_t));
    uint32_t *seg0 = want_mouth ? malloc(SEG * sizeof(uint32_t)) : NULL;
    FILE *head = NULL;
    if(dump_head){
        char name[128]; snprintf(name, sizeof name, "shadows_%llu_head.bin", (unsigned long long)m);
        head = fopen(name, "wb");
    }

    uint64_t head_left = dump_head ? (m-1 < SEG ? m-1 : SEG) : 0;
    for(uint64_t ks = 1; ks <= m-1; ks += SEG){
        uint64_t ke = ks + SEG - 1; if(ke > m-1) ke = m-1;
        uint64_t span = ke - ks + 1;
        memset(cov, 0, span * sizeof(uint32_t));
        for(uint64_t i = 0; i < NP; i++){
            uint64_t p = PR[i];
            uint64_t r = lo % p;
            uint64_t j = r ? p - r : 0;
            if(j < ks) j += ((ks - j + p - 1)/p)*p;
            for(; j <= ke; j += p)
                if(lo + j != p && !cov[j-ks]) cov[j-ks] = (uint32_t)p;
        }
        if(head && head_left){
            uint64_t n = span < head_left ? span : head_left;
            fwrite(cov, sizeof(uint32_t), n, head);
            head_left -= n;
        }
        if(seg0 && ks == 1) memcpy(seg0, cov, span * sizeof(uint32_t));
        for(uint64_t j = ks; j <= ke; j++){
            uint32_t c = cov[j-ks];
            if(!c){                                /* interval prime (any tick) */
                R->iprimes++;
                if(!R->ifirst_off) R->ifirst_off = j;
                if(2*j < m) R->ilprimes++; else if(2*j > m) R->irprimes++;
                if(R->iprv && j - R->iprv > R->imaxgap){
                    R->imaxgap = j - R->iprv; R->igapat = R->iprv;
                }
                R->iprv = j;
            }
            if(!seat_p(j, m, R->mprime)) continue;
            R->seats++;
            if(c){ R->shadowed++; R->count[c]++; R->sumcov += 1; }
            else {
                R->primes++;
                if(!R->first_off) R->first_off = j;
                if(R->prv_off && j - R->prv_off > R->maxgap){
                    R->maxgap = j - R->prv_off; R->gapat = R->prv_off;
                }
                R->prv_off = j;
            }
        }
    }
    if(head) fclose(head);
    if(seg0 && R->ifirst_off > 1){         /* mouth anatomy: leading run [1, ifirst_off) */
        uint8_t *seen = calloc(lim + 1, 1);
        uint64_t end = R->ifirst_off - 1; if(end > SEG) end = SEG;
        for(uint64_t j = 1; j <= end; j++){
            R->mouth_seats++;                  /* ticks, not just seats */
            uint32_t c = seg0[j-1];
            if(c){
                if(!seen[c]){ seen[c] = 1; R->mouth_distinct++; }
                if(c > R->mouth_largest) R->mouth_largest = c;
            }
        }
        free(seen);
        free(seg0);
    }
    free(cov);
    R->overlap = R->sumcov - R->shadowed;   /* double-covered seats */
}

int main(int argc, char **argv){
    if(argc < 2){ fprintf(stderr, "usage: shadows <m> | shadows -b <center> <n> [all|prime]\n"); return 1; }
    struct timespec t0, t1; clock_gettime(CLOCK_MONOTONIC, &t0);

    if(!strcmp(argv[1], "-b")){
        uint64_t c = strtoull(argv[2], 0, 10), n = strtoull(argv[3], 0, 10);
        int any_m = argc > 4 && !strcmp(argv[4], "all");
        gen_primes(200000);                    /* enough to trial-test m itself */
        uint64_t found = 0;
        for(uint64_t d = 0; found < n && d < 1000000; d++){
            uint64_t ms[2] = { c > d ? c - d : 0, c + d };
            for(int s = 0; s < 2 && found < n; s++){
                uint64_t m = ms[s];
                if(m < 3 || (!any_m && !is_prime_trial(m))) continue;
                Report R; run_layer(m, &R, 0, 1);
                printf("B m=%llu mp=%d seats=%llu shadowed=%llu primes=%llu first_off=%llu maxgap=%llu gapat=%llu ifirst_off=%llu iprimes=%llu imaxgap=%llu igapat=%llu ilprimes=%llu irprimes=%llu mouth_ticks=%llu mouth_distinct=%llu mouth_largest=%llu\n",
                    (unsigned long long)m, R.mprime,
                    (unsigned long long)R.seats, (unsigned long long)R.shadowed,
                    (unsigned long long)R.primes,
                    (unsigned long long)R.first_off, (unsigned long long)R.maxgap, (unsigned long long)R.gapat,
                    (unsigned long long)R.ifirst_off, (unsigned long long)R.iprimes,
                    (unsigned long long)R.imaxgap, (unsigned long long)R.igapat,
                    (unsigned long long)R.ilprimes, (unsigned long long)R.irprimes,
                    (unsigned long long)R.mouth_seats, (unsigned long long)R.mouth_distinct, (unsigned long long)R.mouth_largest);
                fflush(stdout);
                free(R.count);
                found++;
            }
        }
    } else {
        uint64_t m = strtoull(argv[1], 0, 10);
        Report R; run_layer(m, &R, 1, 0);
        printf("LAYER m=%llu prime=%s lo=%llu hi=%llu lim=%llu\n",
            (unsigned long long)m, R.mprime?"YES":"NO",
            (unsigned long long)R.lo, (unsigned long long)R.hi, (unsigned long long)LIM);
        printf("  seats=%llu shadowed=%llu primes=%llu sumcov=%llu overlap=%llu\n",
            (unsigned long long)R.seats, (unsigned long long)R.shadowed,
            (unsigned long long)R.primes, (unsigned long long)R.sumcov, (unsigned long long)R.overlap);
        printf("  first_off=%llu maxgap=%llu gapat=%llu junction_prime=%s\n",
            (unsigned long long)R.first_off, (unsigned long long)R.maxgap,
            (unsigned long long)R.gapat, R.junction_prime?"YES":"no");
        printf("  ifirst_off=%llu iprimes=%llu imaxgap=%llu igapat=%llu ilprimes=%llu irprimes=%llu\n",
            (unsigned long long)R.ifirst_off, (unsigned long long)R.iprimes,
            (unsigned long long)R.imaxgap, (unsigned long long)R.igapat,
            (unsigned long long)R.ilprimes, (unsigned long long)R.irprimes);
        for(uint64_t p = 2; p <= LIM; p++)
            if(R.count[p]) printf("COVER %llu %u\n", (unsigned long long)p, R.count[p]);
        free(R.count);
    }
    clock_gettime(CLOCK_MONOTONIC, &t1);
    fprintf(stderr, "time: %.1f s\n", (t1.tv_sec-t0.tv_sec) + 1e-9*(t1.tv_nsec-t0.tv_nsec));
    return 0;
}
