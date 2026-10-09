/* p3_count.c -- how many wiping turnings land in one lap?
 *
 * For the first k rings, count exactly how many maximal blank runs of length >= L start in one lap of
 * 2*3*5*...*p_k numbers. A run starts right after an uncovered number y': so we count turnings (r_p for each
 * ring, with ring p covering positions = r_p mod p) where position 0 is uncovered (r_p != 0 for every ring)
 * and positions 1..L are all covered. Each such turning is one run start per lap (the CRT lock).
 * Ring 2 must sit on the odd positions (r_2 = 1), so only the even positions 2..L need the odd rings.
 *
 * If those N run starts were scattered at random over the lap, the first would come at about lap / (N + 1).
 *
 * usage: p3_count k L1 [L2 ...]     prints: k L N lap lap/(N+1)
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static const int PR[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53};
static int K, L, NS, NB;          /* odd rings: small ones brute-forced, big ones by recursion */
static int B[16];
static uint64_t CLS[16][64];      /* CLS[j][r] = even positions in [2, L] that are = r mod B[j] */

static unsigned __int128 rec(uint64_t U, int j) {
    if (!U) {
        unsigned __int128 w = 1;
        for (int q = j; q < NB; q++) w *= (unsigned)(B[q] - 1);
        return w;
    }
    if (j == NB) return 0;
    int need = __builtin_popcountll(U), cap = 0;          /* can the rings left cover what's left? */
    for (int q = j; q < NB; q++) {
        int best = 0;
        for (int r = 1; r < B[q]; r++) { int c = __builtin_popcountll(U & CLS[q][r]); if (c > best) best = c; }
        cap += best;
    }
    if (cap < need) return 0;
    int p = B[j], hit = 0;
    unsigned __int128 tot = 0;
    for (int r = 1; r < p; r++) {
        uint64_t h = U & CLS[j][r];
        if (h) { hit++; tot += rec(U & ~h, j + 1); }
    }
    tot += (unsigned __int128)(p - 1 - hit) * rec(U, j + 1);  /* ring j lands where it covers nothing needed */
    return tot;
}

int main(int argc, char **argv) {
    K = atoi(argv[1]);
    int odd = K - 1;
    NS = odd < 5 ? odd : 5;  NB = odd - NS;
    for (int j = 0; j < NB; j++) B[j] = PR[1 + NS + j];
    unsigned __int128 lap = 1; for (int j = 0; j < K; j++) lap *= PR[j];
    for (int a = 2; a < argc; a++) {
        L = atoi(argv[a]);
        uint64_t FULL = 0;
        for (int i = 2; i <= L; i += 2) FULL |= 1ULL << i;
        for (int j = 0; j < NB; j++) {
            for (int r = 0; r < 64; r++) CLS[j][r] = 0;
            for (int i = 2; i <= L; i += 2) CLS[j][i % B[j]] |= 1ULL << i;
        }
        /* brute force the small odd rings (residues 1..p-1 each) */
        int sp[5]; for (int s = 0; s < NS; s++) sp[s] = PR[1 + s];
        int r[5] = {1, 1, 1, 1, 1};
        unsigned __int128 N = 0;
        for (;;) {
            uint64_t U = FULL;
            for (int s = 0; s < NS; s++)
                for (int i = 2; i <= L; i += 2) if (i % sp[s] == r[s]) U &= ~(1ULL << i);
            N += rec(U, 0);
            int s = 0;
            while (s < NS) { if (++r[s] < sp[s]) break; r[s] = 1; s++; }
            if (s == NS) break;
        }
        long double est = (long double)lap / ((long double)N + 1);
        printf("%d %d %llu %llu %.4Le\n", K, L, (unsigned long long)N, (unsigned long long)lap, est);
        fflush(stdout);
    }
    return 0;
}
