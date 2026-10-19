"""Independent cross-check for Ace's necklaces.a68 (old-tongues dare).
No shared code: pure-Python orbit enumeration by canonical representative."""
from math import comb, gcd
from math import gcd as _g


def popcount(v):
    return bin(v).count("1")


def rotate(v, n):
    return ((v * 2) % (1 << n)) + (v >> (n - 1))


def mirror(v, n):
    r = 0
    for _ in range(n):
        r = r * 2 + (v & 1)
        v >>= 1
    return r


def min_rotation(v, n):
    m, x = v, v
    for _ in range(n - 1):
        x = rotate(x, n)
        m = min(m, x)
    return m


def counts(n, k):
    patterns = necklaces = bracelets = 0
    for v in range(1 << n):
        if popcount(v) != k:
            continue
        patterns += 1
        rot = min_rotation(v, n)
        if rot == v:
            necklaces += 1
        both = min(rot, min_rotation(mirror(v, n), n))
        if both == v:
            bracelets += 1
    return patterns, necklaces, bracelets


def burnside_necklaces(n, k):
    """Formula cross-check: (1/n) * sum_{d | gcd(n,k)} phi(d) * C(n/d, k/d)."""
    def phi(d):
        r, x, p = d, d, 2
        while p * p <= x:
            if x % p == 0:
                r -= r // p
                while x % p == 0:
                    x //= p
            p += 1
        if x > 1:
            r -= r // x
        return r
    g = gcd(n, k)
    return sum(phi(d) * comb(n // d, k // d) for d in range(1, g + 1) if g % d == 0) // n


if __name__ == "__main__":
    for n, k in [(12, 5), (12, 4), (10, 3), (9, 4), (7, 2)]:
        p, ne, br = counts(n, k)
        bf = burnside_necklaces(n, k)
        flag = "OK " if (p == comb(n, k) and ne == bf) else "???"
        print(f"n={n:2d} k={k}: patterns={p:4d} necklaces={ne:3d} "
              f"bracelets={br:3d}  (C(n,k)={comb(n,k)}, Burnside={bf}) {flag}")
