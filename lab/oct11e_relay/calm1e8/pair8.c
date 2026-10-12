/* Lane pair series to W = 1e8 (PHASE 11 build_F conventions, bound-consistent: G, ap, bp all to PG).
 * usage: pair8 c W PG weightfile   (weightfile: text "d a(d)" grid, increasing d, a(0) first)
 * prints JSON: S(W') = 2 sum_{d<W'} (1-d/W')(F-1) for W' = 1e2..W, and
 *   Q  = 2 sum_{d=1}^{W-1} a(d) (F(d) - phi2(d))   (varying-density whole-window pair sum)
 *   Q1 = 2 sum_{d=1}^{W-1} a(d) (F(d) - 1)                                                        */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
static inline uint64_t mulm(uint64_t a, uint64_t b, uint64_t m) {
    uint64_t c = (uint64_t)((long double)a * b / m);
    int64_t r = (int64_t)(a * b - c * m) % (int64_t)m; return r < 0 ? (uint64_t)(r + (int64_t)m) : (uint64_t)r; }
static uint64_t powm(uint64_t a, uint64_t e, uint64_t m) { uint64_t r = 1; a %= m; while (e) { if (e & 1) r = mulm(r, a, m); a = mulm(a, a, m); e >>= 1; } return r; }
static uint64_t sqrtm(uint64_t n, uint64_t p) {            /* n a nonzero QR mod odd prime p */
    if (p % 4 == 3) return powm(n, (p + 1) / 4, p);
    uint64_t q = p - 1; int s = 0; while (!(q & 1)) { q >>= 1; s++; }
    uint64_t z = 2; while (powm(z, (p - 1) / 2, p) != p - 1) z++;
    uint64_t c = powm(z, q, p), x = powm(n, (q + 1) / 2, p), t = powm(n, q, p); int m = s;
    while (t != 1) { int i = 0; uint64_t tt = t; while (tt != 1) { tt = mulm(tt, tt, p); i++; }
        uint64_t b = c; for (int j = 0; j < m - i - 1; j++) b = mulm(b, b, p);
        x = mulm(x, b, p); c = mulm(b, b, p); t = mulm(t, c, p); m = i; }
    return x;
}
int main(int argc, char **argv) {
    long cc = atol(argv[1]); long W = atol(argv[2]); long PG = atol(argv[3]);
    long D = 1 - 8 * cc;
    /* weights grid */
    FILE *f = fopen(argv[4], "r"); long ng = 0, cap = 1 << 16; double *gd = malloc(cap * 8), *ga = malloc(cap * 8);
    while (fscanf(f, "%lf %lf", &gd[ng], &ga[ng]) == 2) ng++; fclose(f);
    /* odd-prime sieve to PG */
    long half = PG / 2 + 1; uint8_t *comp = calloc(half, 1);
    for (long i = 3; i * i <= PG; i += 2) if (!comp[i / 2]) for (long j = i * i; j <= PG; j += 2 * i) comp[j / 2] = 1;
    double *F = malloc(sizeof(double) * W);
    long double logG = 0;
    for (long d = 0; d < W; d++) F[d] = 1.0;
    int special3 = (((D % 3) + 3) % 3 == 1);
    for (long p = 3; p <= PG; p += 2) {
        if (comp[p / 2]) continue;
        long Dm = ((D % p) + p) % p; int rho;
        if (Dm == 0) rho = 1; else rho = (powm(Dm, (p - 1) / 2, p) == 1) ? 2 : 0;
        if (rho == 0) continue;
        if (p == 3 && special3) {                     /* C3: every d != 0 mod 3 is common-root (factor 0); 3|d gets 3 */
            for (long d = 0; d < W; d++) F[d] *= (d % 3 == 0) ? 3.0 : 0.0;
            continue;
        }
        if (rho == 1) {
            logG += log1pl(-2.0L / p) - 2.0L * log1pl(-1.0L / p);
            if (p < W) { double ap = (double)(p - 1) / (p - 2); for (long d = p; d < W; d += p) F[d] *= ap; }
        } else {
            logG += log1pl(-4.0L / p) - 2.0L * log1pl(-2.0L / p);
            if (p < W) { double ap = (double)(p - 2) / (p - 4); for (long d = p; d < W; d += p) F[d] *= ap; }
            uint64_t dl = sqrtm((uint64_t)Dm, (uint64_t)p); double bp = (double)(p - 3) / (p - 4);
            for (long d = (long)dl; d < W; d += p) F[d] *= bp;
            for (long d = p - (long)dl; d < W; d += p) F[d] *= bp;
        }
    }
    double G = (double)expl(logG);
    for (long d = 0; d < W; d++) { F[d] *= G; long r = d & 3; if (r == 2) F[d] = 0.0; else if (r == 0) F[d] *= 2.0; }
    /* sums */
    long double X = 0, DX = 0, Q = 0, Q1 = 0; long gi = 0; long nextW = 100;
    printf("{\"c\":%ld,\"D\":%ld,\"W\":%ld,\"PG\":%ld,\"G\":%.12f,\"S\":{", cc, D, W, PG, G);
    int first = 1;
    for (long d = 1; d < W; d++) {
        while (gi + 1 < ng && gd[gi + 1] <= d) gi++;
        double a = (gi + 1 < ng) ? ga[gi] + (ga[gi + 1] - ga[gi]) * (d - gd[gi]) / (gd[gi + 1] - gd[gi]) : ga[ng - 1];
        double phi2 = ((d & 3) == 0) ? 2.0 : (((d & 3) == 2) ? 0.0 : 1.0);
        double x = F[d] - 1.0;
        X += x; DX += (long double)d * x; Q += a * (F[d] - phi2); Q1 += a * x;
        if (d + 1 == nextW) {                         /* S(W') uses d = 1..W'-1 */
            printf("%s\"%ld\":%.9Lf", first ? "" : ",", nextW, 2.0L * (X - DX / nextW)); first = 0;
            nextW *= 10;
        }
    }
    printf("},\"Q\":%.9Lf,\"Q1\":%.9Lf}\n", 2.0L * Q, 2.0L * Q1);
    return 0;
}
