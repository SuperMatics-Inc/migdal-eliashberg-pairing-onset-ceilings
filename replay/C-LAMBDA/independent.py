"""Verify q endpoints on the full signed lattice, with explicit positive infinite tails."""
import argparse
import json
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.linalg import eigh, solve

D = 10**20
V = 10**17


def up(x):
    return -(-x.numerator // x.denominator)


def need(condition, msg):
    if not condition:
        raise ValueError(msg)


class Lattice:
    def __init__(self, n, lam, q):
        self.n, self.lam, self.q = n, lam, q
        self.b = lam/q
        self.exact = [lam/(1+q*k*k) for k in range(3*n)]
        self.alo = [int(D*v) for v in self.exact]
        self.ahi = [up(D*v) for v in self.exact]
        self.row = self.exact[0] + 2*(sum(self.exact[1:n+1]) + self.b/n)
        self.tail_offset = 1 + 8*self.row
        need(2*(n+1) > self.tail_offset, 'tail row estimate not positive')

        # Candidate generation only. Opposite signs are retained as separate indices.
        m = np.arange(-n, n)
        j = np.arange(n, 2*n)
        self.diff = abs(m[:, None] - m[None, :])
        self.conjugate = abs(m[:, None] + j[None, :] + 1)
        self.cross_diff = abs(m[:, None] - j[None, :])
        self.indices = np.maximum(m, -m-1)
        vals = np.array(self.exact, dtype=float)
        self.diag = 2*self.indices+1 + vals[0] + 2*(np.cumsum(vals[:n]) - vals[0])[self.indices]
        self.kernel = vals[self.diff]
        self.cross = vals[self.cross_diff] + vals[self.conjugate]
        self.tail_edges = self.cross @ ((j+1.)**-3) + float(5*self.b/(4*(2*n)**4))

    def tail_need(self, indices):
        # h is normalized to h[0]=1 on the positive half; the full lattice reflects it.
        n, h = self.n, indices
        loss = 5*self.b/(2*n*n)
        slope = 2 - loss
        if slope*(n+1) <= self.tail_offset:
            return None
        far = 5*self.b*sum(h) / (slope - self.tail_offset/(2*n+1))
        near = (Fraction(sum((self.ahi[j-i] + self.ahi[j+i+1])*xi for i, xi in enumerate(h)), D)
                * (j+1)**3 / (slope*(j+1) - self.tail_offset) for j in range(n, 2*n))
        return up(max(far, *near)) + 1

    def trial(self, stable):
        n = self.n
        _, u = eigh(self.kernel, np.diag(self.diag), subset_by_index=(2*n-1, 2*n-1),
                    check_finite=False)
        f = u[:, 0] / u[n, 0]
        f = (f + f[::-1])/2
        weights = [round(float(x)*V) for x in f[n:]]
        if stable:
            t = float(self.tail_need(weights)/V) * 2
            h = f + solve(np.diag(self.diag)-self.kernel, t*self.tail_edges,
                          assume_a='pos', check_finite=False)
            h = (h + h[::-1]) / (2*h[n])
            weights = [round(float(x)*V) for x in h[n:]]
        return weights

    def full_rows(self, half, upper, mutant):
        n = self.n
        h = half[::-1] + half
        diag = self.alo if upper else self.ahi
        pair = self.ahi if upper else self.alo
        running = D + diag[0]
        normal = [running]
        for k in range(1, n):
            running += 2*D + (0 if mutant == 'no_mass' else 2*diag[k])
            normal.append(running)
        for i in range(-n, n):
            def transfer(m):
                k = abs(i-m)
                return pair[k-1] if mutant == 'cross_shift' and (i < 0) != (m < 0) else pair[k]
            off = sum(transfer(m)*x for m, x in zip(range(-n, n), h))
            idx = i if i >= 0 else -i-1
            yield normal[idx]*h[i+n] - off

    def check(self, h, upper, mutant=None):
        n = self.n
        if min(h) <= 0:
            return False
        rows = list(self.full_rows(h, upper, mutant))
        if not upper:
            return sum(x*y for x, y in zip(h[::-1]+h, rows)) < 0
        t = self.tail_need(h)
        if t is None:
            return False
        rem = 5*self.b*t/(4*(2*n)**4)
        for i in range(n):
            finite = sum(Fraction(self.ahi[j-i]+self.ahi[j+i+1], D*(j+1)**3)
                         for j in range(n, 2*n))
            if rows[n+i] <= D*(t*finite + rem) or rows[n-1-i] <= D*(t*finite + rem):
                return False
        return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--size', type=int, default=384)
    opts = parser.parse_args()
    data = json.loads(Path(__file__).with_name('brackets.json').read_text(encoding='utf8'))
    n = opts.size
    print(f'two-sided exact replay N={n} positive plus {n} negative head modes')
    for key, (left, right) in data['q_numerators'].items():
        lam = Fraction(key)
        low = Lattice(n, lam, Fraction(left, data['q_denominator']))
        high = Lattice(n, lam, Fraction(right, data['q_denominator']))
        x, h = low.trial(False), high.trial(True)
        need(low.check(x, False), f'{key}: cold endpoint')
        need(high.check(h, True), f'{key}: hot endpoint')
        print(f'{key:>5} q={left},{right}/{data["q_denominator"]} exact sign bracket accepted')
        if key == '1':
            need(not high.check(x, False), 'hot-as-cold mutant survived')
            need(not low.check(h, True), 'cold-as-hot mutant survived')
            need(not high.check(h, True, 'no_mass'), 'mass omitted mutant survived')
            need(not high.check(h, True, 'cross_shift'), 'bad cross reflection mutant survived')
    print('4 mutants rejected (hot/cold endpoint swaps, absent normal mass, cross-index shift)')
    for label, (left, right) in data.get('ambient_q_numerators', {}).items():
        raw_lam = label.split(':')[-1]
        lam = Fraction(raw_lam)
        m = max(832, n) if raw_lam == '0.158' else n
        low = Lattice(m, lam, Fraction(left, data['q_denominator']))
        high = Lattice(m, lam, Fraction(right, data['q_denominator']))
        x, h = low.trial(False), high.trial(True)
        need(low.check(x, False), f'{label}: cold endpoint')
        need(high.check(h, True), f'{label}: hot endpoint')
        print(f'{label:>36} q={left},{right}/{data["q_denominator"]} exact sign bracket accepted (N={m})')


if __name__ == '__main__':
    main()
