"""Generate candidate vectors in float, certify them with integer interval arithmetic."""
import argparse
import csv
from pathlib import Path
from fractions import Fraction as F
from math import isqrt

import numpy as np
from scipy.linalg import eigh, solve
from scipy.optimize import brentq

SCALE = 10**18
VEC = 10**17
GRID = 10**11
BASE = '0.5 1 1.5 2 2.5 3 4 6 10'.split()
EXTRA = '0.61 1.26 1.68 1.73 1.80 2.06 2.21 2.67 3.14 3.62'.split()
KB = F('0.00008617333262')
MATERIALS = (
    ('Pb', '1.68', '0.00006249', '7.19', '7.19'),
    ('Nb', '1.26', '0.0003466', '9.25', '9.25'),
    ('MgB2', '0.61', '0.0028654', '39', '39'),
    ('LaH10 129', '3.62', '0.036826', '244', '245'),
    ('LaH10 163', '2.67', '0.039267', '249', '252'),
    ('LaH10 214', '2.06', '0.041668', None, None),
    ('LaH10 264', '1.73', '0.042610', None, None),
    ('LaD10 159', '3.14', '0.019675', '150', '166'),
    ('LaD10 210', '2.21', '0.020909', None, None),
    ('LaD10 260', '1.80', '0.021355', None, None),
)


def ceil(x):
    return -(-x.numerator // x.denominator)


def sqrt_floor(x, scale):
    return isqrt(x.numerator * scale**2 // x.denominator)


def atan_bounds(x):
    partial = sum(((-1)**j * x**(2*j+1) / (2*j+1) for j in range(30)), F(0))
    return partial, partial + x**61 / 61


def pi_bounds():
    lo5, hi5 = atan_bounds(F(1, 5))
    lo239, hi239 = atan_bounds(F(1, 239))
    return 16*lo5 - 4*hi239, 16*hi5 - 4*lo239


def c_bounds(lam, low, high):
    plo, phi = pi_bounds()
    scale = 10**10
    a = (low / lam) / (4*phi**2)
    b = (high / lam) / (4*plo**2)
    return F(sqrt_floor(a, scale), scale), F(sqrt_floor(b, scale)+1, scale)


class Folded:
    def __init__(self, n):
        self.n = n
        i = np.arange(n)
        self.diff = abs(i[:, None] - i[None, :])
        self.hankel = i[:, None] + i[None, :] + 1
        self.odd = 2*i + 1
        self.k_sq = np.arange(2*n)**2
        self.r = np.arange(n, 0, -1, dtype=float)

    def matrix(self, lam, q, mix=False):
        if mix:
            a = sum(lam/2 / (1 + q*self.k_sq/x) for x in (0.25, 1.75))
        else:
            a = lam / (1 + q*self.k_sq)
        a[0] = 0
        d = self.odd + 2*np.cumsum(a[:self.n])
        return np.diag(d) - a[self.diff] - a[self.hankel]

    def eig(self, h, vectors=False):
        return eigh(h, subset_by_index=(0, 0), eigvals_only=not vectors, check_finite=False)

    def root(self, lam, mix=False):
        return brentq(lambda q: self.eig(self.matrix(lam, q, mix))[0],
                      1e-4, 256, xtol=4e-14)

    def candidate(self, lam, q, upper):
        f, t = float(lam), float(q)
        mat = self.matrix(f, t)
        if upper:
            b = f/t
            u = 2*b*np.sqrt(self.r**-4 + self.r**-3/3)
            mat -= np.outer(u, u)/(2*self.n+1-2*b/self.n)
            x = solve(mat, np.ones(self.n), assume_a='sym', check_finite=False)
        else:
            _, vectors = self.eig(mat, vectors=True)
            x = vectors[:, 0]
        x = x / x[0]
        return [round(float(y)*VEC) for y in x]


def signed_check(lam, q, x, upper, mutant=None):
    n = len(x)
    if not all(v > 0 for v in x):
        return False
    a = [F(0)] + [lam/(1+q*k*k) for k in range(1, 2*n)]
    if mutant == 'no_normal':
        # Calculate the altered form, not the production form with a loosened tolerance.
        normal_factor = 0
    else:
        normal_factor = 2
    if upper:
        ap, an = [ceil(v*SCALE) for v in a], [int(v*SCALE) for v in a]
    else:
        ap, an = [int(v*SCALE) for v in a], [ceil(v*SCALE) for v in a]
    d = SCALE
    dot = 0
    rows = []
    for i, xi in enumerate(x):
        offset = 0 if mutant == 'hankel_shift' else 1
        y = d*xi - sum((ap[abs(i-j)] + ap[i+j+offset])*xj for j, xj in enumerate(x))
        rows.append(y)
        dot += xi*y
        if i+1 < n:
            d += 2*SCALE + normal_factor*an[i+1]
    if not upper:
        return dot < 0
    b = lam/q
    delta = 2*n+1-2*b/n
    if delta <= 0:
        return False
    u = []
    for r in range(n, 0, -1):
        v = (2*b)**2 * (F(1, r**4) + F(1, 3*r**3))
        # Nonnegative upward rounding valid even for a perfect square.
        u.append(sqrt_floor(v, SCALE)+1)
    ux = sum(ui*xi for ui, xi in zip(u, x))
    factor = delta*SCALE
    return all(y*factor > ui*ux for ui, y in zip(u, rows))


def require(condition, description):
    if not condition:
        raise ValueError(description)


def bracket(engine, lam):
    mid = engine.root(float(lam))
    # Fixed relative width; exact checks, not the approximate root, decide the signs.
    rad = max(3, round(mid*GRID*1e-6))
    i = round(mid*GRID)
    low, high = F(i-rad, GRID), F(i+rad, GRID)
    lvec, uvec = engine.candidate(lam, low, False), engine.candidate(lam, high, True)
    require(signed_check(lam, low, lvec, False), f'failed lower: {lam}, N={engine.n}')
    require(signed_check(lam, high, uvec, True), f'failed upper: {lam}, N={engine.n}')
    return low, high, lvec, uvec


def report_application(bounds):
    print('application (NUMERICAL): lambda, M*(300 K), factor vs scalar M≈0.0200164')
    for key in BASE:
        c = sum(bounds[key])/2
        mstar = float((300*KB/c)**2)
        print(f'{key:>5} {mstar:.8f} {mstar/0.0200164:.4f}')
    print('application (NUMERICAL): material, lambda, M, ceiling K, measured/ceiling')
    for name, key, moment, tlo, thi in MATERIALS:
        c = float(sum(bounds[key])/2)
        k = c * float(F(moment))**0.5 / float(KB)
        r = 'unpaired' if tlo is None else f'{float(tlo)/k:.5f}..{float(thi)/k:.5f}'
        print(f'{name:>12} {key:>5} {moment:>10} {k:9.4f} {r}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--size', type=int, default=384)
    opts = parser.parse_args()
    engine = Folded(opts.size)
    bounds = {}
    print(f'folded exact replay N={engine.n}')
    for key in BASE + EXTRA:
        lam = F(key)
        low, high, lvec, uvec = bracket(engine, lam)
        c_lo, c_hi = bounds[key] = c_bounds(lam, low, high)
        print(f'{key:>5} q={int(low*GRID)},{int(high*GRID)}/{GRID} C={float(c_lo):.10f}..{float(c_hi):.10f}')
        if key == '1':
            require(not signed_check(lam, high, lvec, False), 'hot endpoint called unstable')
            require(not signed_check(lam, low, uvec, True), 'cold endpoint called stable')
            require(not signed_check(lam, high, uvec, True, 'no_normal'), 'normal omission survived')
            require(not signed_check(lam, low, lvec, False, 'hankel_shift'), 'Hankel shift survived')
    print('4 mutants rejected (hot/cold endpoint swaps, omitted Z, off-by-one Hankel)')
    ambient = [
        ('ambient/Tl2AgH2_harmonic:1.128', '1.128', 66924300387, 66924434235, engine),
        ('ambient/NaNiH3_harmonic:0.158', '0.158', 880000, 25000000, Folded(max(832, opts.size))),
        ('ambient/BC11_harmonic:0.551', '0.551', 9053928500, 9053946608, engine),
        ('ambient/B2C8Cl_harmonic:3.278', '3.278', 343678722379, 343679409737, engine),
        ('ambient/Al2H7Os_harmonic:3.175', '3.175', 330183076096, 330183736462, engine),
        ('ambient/Li2AgH6_harmonic:3.783', '3.783', 409919994317, 409920814157, engine),
        ('ambient/Li2AuH6_harmonic:3.86', '3.86', 420028686895, 420029526953, engine),
        ('ambient/Li2AuH6_SSCHA_auxiliary:2.1', '2.1', 189941485013, 189941864897, engine),
        ('ambient/Li2AuH6_SSCHA_Hessian:2.67', '2.67', 264125304490, 264125832742, engine),
    ]
    amb_bounds = {}
    for label, raw_lam, left, right, eng in ambient:
        lam = F(raw_lam)
        low, high = F(left, GRID), F(right, GRID)
        lvec, uvec = eng.candidate(lam, low, False), eng.candidate(lam, high, True)
        require(signed_check(lam, low, lvec, False), f'failed ambient lower: {label}')
        require(signed_check(lam, high, uvec, True), f'failed ambient upper: {label}')
        c_lo, c_hi = amb_bounds[raw_lam] = c_bounds(lam, low, high)
        print(f'{label:>36} q={left},{right}/{GRID} C={float(c_lo):.10f}..{float(c_hi):.10f}')
    src_csv = Path(__file__).resolve().parents[1] / 'T2-AMBIENT' / 'ratios.csv'
    dst_csv = Path(__file__).resolve().parents[1] / 'T2-AMBIENT' / 'ratios_lambda.csv'
    with src_csv.open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
        fields = list(rows[0].keys()) + [
            'C_lambda_lo', 'C_lambda_hi', 'T_ceil_lambda_lo_K', 'T_ceil_lambda_hi_K',
            'T_ceil_lambda_K', 'R_lambda_lo', 'R_lambda_hi', 'R_lambda',
            'R_lambda_gt_0_6', 'predicted_tc_gt_ceiling_lambda',
            'M_star_300K_lo_eV2', 'M_star_300K_hi_eV2', 'M_star_300K_eV2', 'M_over_M_star_300K',
        ]
    kb_f = float(KB)
    for r in rows:
        c_lo, c_hi = [float(v) for v in amb_bounds[r['lambda']]]
        c_mid = 0.5 * (c_lo + c_hi)
        m_val = float(r['M_eV2'])
        tc_val = float(r['tc_K'])
        t_lo = c_lo * (m_val ** 0.5) / kb_f
        t_hi = c_hi * (m_val ** 0.5) / kb_f
        t_mid = c_mid * (m_val ** 0.5) / kb_f
        r_lo = tc_val / t_hi
        r_hi = tc_val / t_lo
        r_mid = tc_val / t_mid
        ms_lo = (300.0 * kb_f / c_hi) ** 2
        ms_hi = (300.0 * kb_f / c_lo) ** 2
        ms_mid = (300.0 * kb_f / c_mid) ** 2
        r.update(
            C_lambda_lo=f'{c_lo:.10f}', C_lambda_hi=f'{c_hi:.10f}',
            T_ceil_lambda_lo_K=f'{t_lo:.12g}', T_ceil_lambda_hi_K=f'{t_hi:.12g}',
            T_ceil_lambda_K=f'{t_mid:.12g}',
            R_lambda_lo=f'{r_lo:.12g}', R_lambda_hi=f'{r_hi:.12g}', R_lambda=f'{r_mid:.12g}',
            R_lambda_gt_0_6=str(r_hi > 0.6).lower(),
            predicted_tc_gt_ceiling_lambda=str(r_hi > 1.0).lower(),
            M_star_300K_lo_eV2=f'{ms_lo:.12g}', M_star_300K_hi_eV2=f'{ms_hi:.12g}',
            M_star_300K_eV2=f'{ms_mid:.12g}', M_over_M_star_300K=f'{m_val / ms_mid:.12g}',
        )
    with dst_csv.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    best_row = max(rows, key=lambda r: float(r['R_lambda_hi']))
    print(f"ambient R(lambda): rows={len(rows)} max={best_row['R_lambda']} ({best_row['material']} {best_row['spectrum_approximation']} {best_row['tc_method']}) R_lambda>0.6={sum(r['R_lambda_gt_0_6']=='true' for r in rows)} R_lambda>1={sum(r['predicted_tc_gt_ceiling_lambda']=='true' for r in rows)}")
    report_application(bounds)
    print('NUMERICAL equal coupling weights at Omega*sqrt(1/4), Omega*sqrt(7/4):')
    for key in BASE:
        lam = float(key)
        q = engine.root(lam, mix=True)
        cmix = (q/lam)**0.5/(2*np.pi)
        print(f'{key:>5} C_mix={cmix:.8f} mix/Einstein={cmix/float(sum(bounds[key])/2):.6f}')


if __name__ == '__main__':
    main()
