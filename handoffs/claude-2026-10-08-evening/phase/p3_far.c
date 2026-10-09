/* p3_far.c -- the far jump, found exactly instead of by scanning.
 *
 * Rings = the first k primes. A "blank run" is a stretch of consecutive whole numbers that every one is
 * divisible by some ring. first_run(k, L) = where the first blank run of length >= L starts, counting up from 0.
 *
 * Instead of walking the number line (up to 7.4 trillion for k = 12), enumerate every way the k rings can be
 * turned so that a window of L positions is fully covered (each ring p covers the positions i = r_p mod p).
 * Every such turning shows up on the real line exactly where y = -r_p (mod p) for the rings it uses
 * (the CRT lock); rings it doesn't need can sit anywhere, so y only has to match the rings it uses.
 * The smallest such y over all turnings is first_run(k, L).
 *
 * Search: take the first uncovered position; some unused ring must cover it; try each. Prune when the unused
 * rings can't cover what's left even at their best phase.
 *
 * usage: p3_far k Lmin Lmax      prints one line per L: L first_run leaves nodes
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

typedef unsigned __int128 u128;
static const int PR[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47};
static int K, L;
static uint64_t MASK[16][64];
static int res[16];
static uint64_t best;
static long long leaves, nodes;

static uint64_t inv_mod(uint64_t a, uint64_t m) {          /* a^-1 mod m, m prime-power-free small */
    int64_t t = 0, nt = 1, r = (int64_t)m, nr = (int64_t)(a % m);
    while (nr) { int64_t q = r / nr, tmp; tmp = t - q * nt; t = nt; nt = tmp; tmp = r - q * nr; r = nr; nr = tmp; }
    if (t < 0) t += (int64_t)m;
    return (uint64_t)t;
}

static uint64_t crt_min(void) {                          /* smallest y >= 0 with y = -res[j] mod PR[j] for used rings */
    uint64_t a = 0, Q = 1;
    for (int j = 0; j < K; j++) {
        if (res[j] < 0) continue;
        uint64_t p = PR[j], t = (p - (uint64_t)res[j]) % p;
        uint64_t cur = a % p;
        uint64_t diff = (t + p - cur) % p;                 /* need Q*s = diff mod p */
        uint64_t s = (uint64_t)((u128)diff * inv_mod(Q % p, p) % p);
        a = a + Q * s; Q *= p;
    }
    return a;
}

static int maxcover(int j, uint64_t U) {
    int p = PR[j], m = 0;
    for (int r = 0; r < p && r < L; r++) { int c = __builtin_popcountll(U & MASK[j][r]); if (c > m) m = c; }
    return m;
}

static void dfs(uint64_t U, unsigned rem) {
    nodes++;
    if (!U) {
        leaves++;
        uint64_t y = crt_min();
        if (y < best) best = y;
        return;
    }
    int i = __builtin_ctzll(U);
    for (int j = 0; j < K; j++) {
        if (!(rem >> j & 1)) continue;
        int r = i % PR[j];
        uint64_t nU = U & ~MASK[j][r];
        unsigned rem2 = rem & ~(1u << j);
        int need = __builtin_popcountll(nU), cap = 0;
        for (int q = 0; q < K && cap < need; q++) if (rem2 >> q & 1) cap += maxcover(q, nU);
        if (cap < need) continue;
        res[j] = r;
        dfs(nU, rem2);
        res[j] = -1;
    }
}

int main(int argc, char **argv) {
    K = atoi(argv[1]);
    int Lmin = atoi(argv[2]), Lmax = atoi(argv[3]);
    for (L = Lmin; L <= Lmax; L++) {
        if (L > 64) break;
        for (int j = 0; j < K; j++) {
            for (int r = 0; r < 64; r++) MASK[j][r] = 0;
            for (int i = 0; i < L; i++) MASK[j][i % PR[j]] |= 1ULL << i;
        }
        for (int j = 0; j < K; j++) res[j] = -1;
        best = UINT64_MAX; leaves = nodes = 0;
        uint64_t U = (L == 64) ? ~0ULL : ((1ULL << L) - 1);
        dfs(U, (1u << K) - 1);
        if (best == UINT64_MAX) printf("%d none %lld %lld\n", L, leaves, nodes);
        else printf("%d %llu %lld %lld\n", L, (unsigned long long)best, leaves, nodes);
        fflush(stdout);
    }
    return 0;
}
