/* p10_parabola.c -- can the deciding rings wipe a layer when each ring is confined to its parabola?
 *
 * Layer m: ticks k = 1..m holding T(m-1)+k. The deciding rings are the primes p with p^2 <= T(m).
 * Ring 2 sits on the evens (fixed by the layer). Odd ring p covers the ticks k = r (mod p) for one phase r.
 *   FREE     any phase r in 0..p-1.
 *   CONFINED only the phases the ring's parabola ever visits: r in R_p = { -T(j) mod p }, (p+1)/2 of them.
 *            Same thing as the gear rule's lane test: r is in R_p exactly when 1 - 8r is a square (or 0) mod p
 *            (asserted below for every ring used).
 * Different rings' phases are independent (Kimi's N1: the joint orbit is the full product), so a layer is
 * wipeable when SOME allowed choice of phases covers every odd-valued tick.
 *
 * Search (exact): cover the first uncovered tick with an unused ring whose allowed phase reaches it (that fixes
 * the ring's phase), trying the ring that covers the most first; prune when the unused rings can't cover what's
 * left even at their best allowed phases. Exhausting the tree proves a layer safe.
 *
 * usage: p10_parabola free|conf m_lo m_hi [node_limit]
 * prints per layer: m odd_rings odd_ticks WIPE|SAFE|UNKNOWN nodes [ring:phase ...]
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define WD 4                                   /* bitsets of 256 ticks */
typedef struct { uint64_t w[WD]; } bs;
static inline int pop(const bs *a) { int s = 0; for (int i = 0; i < WD; i++) s += __builtin_popcountll(a->w[i]); return s; }
static inline int andpop(const bs *a, const bs *b) { int s = 0; for (int i = 0; i < WD; i++) s += __builtin_popcountll(a->w[i] & b->w[i]); return s; }
static inline int empty(const bs *a) { for (int i = 0; i < WD; i++) if (a->w[i]) return 0; return 1; }
static inline int first(const bs *a) { for (int i = 0; i < WD; i++) if (a->w[i]) return i * 64 + __builtin_ctzll(a->w[i]); return -1; }
static inline bs andnot(const bs *a, const bs *b) { bs r; for (int i = 0; i < WD; i++) r.w[i] = a->w[i] & ~b->w[i]; return r; }

static int NR, P[64], ALLOW[64][256], phase[64];
static bs MASK[64][256];
static long long nodes, limit;

static int dfs(bs U, uint64_t used) {
    if (++nodes > limit) return -1;
    if (empty(&U)) return 1;
    int need = pop(&U), cap = 0;
    for (int j = 0; j < NR && cap < need; j++) {
        if (used >> j & 1) continue;
        int best = 0;
        for (int r = 0; r < P[j]; r++) if (ALLOW[j][r]) { int c = andpop(&U, &MASK[j][r]); if (c > best) best = c; }
        cap += best;
    }
    if (cap < need) return 0;
    int i = first(&U);                         /* bit i = tick i+1 */
    int cand[64], gain[64], nc = 0;
    for (int j = 0; j < NR; j++) {
        if (used >> j & 1) continue;
        int r = (i + 1) % P[j];
        if (!ALLOW[j][r]) continue;
        cand[nc] = j; gain[nc] = andpop(&U, &MASK[j][r]); nc++;
    }
    for (int a = 1; a < nc; a++)                /* most coverage first */
        for (int b = a; b > 0 && gain[b] > gain[b - 1]; b--) {
            int t = gain[b]; gain[b] = gain[b - 1]; gain[b - 1] = t;
            t = cand[b]; cand[b] = cand[b - 1]; cand[b - 1] = t;
        }
    for (int a = 0; a < nc; a++) {
        int j = cand[a], r = (i + 1) % P[j];
        phase[j] = r;
        int res = dfs(andnot(&U, &MASK[j][r]), used | (1ULL << j));
        if (res != 0) return res;
        phase[j] = -1;
    }
    return 0;
}

int main(int argc, char **argv) {
    int conf = argv[1][0] == 'c';
    int mlo = atoi(argv[2]), mhi = atoi(argv[3]);
    limit = argc > 4 ? atoll(argv[4]) : 4000000000LL;
    if (mhi > 256) { fprintf(stderr, "m <= 256 only\n"); return 1; }
    for (int m = mlo; m <= mhi; m++) {
        long long Tprev = (long long)(m - 1) * m / 2, Tm = Tprev + m;
        int ring2 = Tm >= 4;
        bs U; memset(&U, 0, sizeof U);
        for (int k = 1; k <= m; k++)
            if (!ring2 || ((Tprev + k) & 1)) U.w[(k - 1) / 64] |= 1ULL << ((k - 1) % 64);
        NR = 0;
        for (int p = 3; (long long)p * p <= Tm; p += 2) {
            int isp = 1; for (int q = 3; q * q <= p; q += 2) if (p % q == 0) { isp = 0; break; }
            if (isp) P[NR++] = p;
        }
        for (int j = 0; j < NR; j++) {
            int p = P[j], sq[256] = {0}, inR[256] = {0};
            for (int s = 0; s < p; s++) sq[s * s % p] = 1;
            for (int t = 0; t < p; t++) inR[(p - (int)((long long)t * (t + 1) / 2 % p)) % p] = 1;
            for (int r = 0; r < p; r++) {
                int lane = sq[((1 - 8 * r) % p + 8 * p) % p];
                if (lane != inR[r]) { fprintf(stderr, "lane test mismatch p=%d r=%d\n", p, r); return 2; }
                ALLOW[j][r] = conf ? inR[r] : 1;
                memset(&MASK[j][r], 0, sizeof(bs));
            }
            for (int k = 1; k <= m; k++)
                if (U.w[(k - 1) / 64] >> ((k - 1) % 64) & 1) MASK[j][k % p].w[(k - 1) / 64] |= 1ULL << ((k - 1) % 64);
            /* the real phase always lies on the parabola */
            int real = (int)((p - Tprev % p) % p);
            if (!inR[real]) { fprintf(stderr, "real phase off the parabola p=%d m=%d\n", p, m); return 3; }
            phase[j] = -1;
        }
        /* the real turning never wipes a layer (every layer holds a prime) */
        bs R = U;
        for (int j = 0; j < NR; j++) R = andnot(&R, &MASK[j][(int)((P[j] - Tprev % P[j]) % P[j])]);
        if (empty(&R)) { fprintf(stderr, "real turning wipes layer %d?\n", m); return 4; }
        nodes = 0;
        int res = dfs(U, 0);
        printf("%d %d %d %s %lld", m, NR, pop(&U), res == 1 ? "WIPE" : res == 0 ? "SAFE" : "UNKNOWN", nodes);
        if (res == 1) {
            bs C = U;                            /* independent check of the covering */
            for (int j = 0; j < NR; j++) if (phase[j] >= 0) {
                if (!ALLOW[j][phase[j]]) { fprintf(stderr, "bad phase\n"); return 5; }
                C = andnot(&C, &MASK[j][phase[j]]);
                printf(" %d:%d", P[j], phase[j]);
            }
            if (!empty(&C)) { fprintf(stderr, "covering check failed at m=%d\n", m); return 6; }
        }
        printf("\n");
        fflush(stdout);
    }
    return 0;
}
