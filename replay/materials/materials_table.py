"""Reproduce every entry of the material table of the manuscript, verbatim.

Inputs, both read relative to this file:
  moments.json                the digitized moments, literature couplings and measured
                              transition temperatures, with their sources and caveats
  ../C-LAMBDA/brackets.json   the certified rational q-brackets of C(lambda)

The certified interval of C(lambda) is recomputed from the bracket with exact rational
arithmetic, using the same rounded pi and square-root enclosures as the replay verifier,
so the decimal endpoints used here are the certified ones. Every printed entry is then
compared with the string recorded in moments.json; any mismatch is reported and the
program exits nonzero.

Usage:  python -B materials_table.py
Exit code 0 means every printed entry reproduces the manuscript table exactly.
"""
import json
from fractions import Fraction as F
from math import isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRACKETS = HERE.parent / 'C-LAMBDA' / 'brackets.json'
SCALE = 10**10


def sqrt_floor(x, scale):
    return isqrt(x.numerator * scale**2 // x.denominator)


def atan_bounds(x):
    partial = sum(((-1)**j * x**(2*j+1) / (2*j+1) for j in range(30)), F(0))
    return partial, partial + x**61 / 61


def pi_bounds():
    lo5, hi5 = atan_bounds(F(1, 5))
    lo239, hi239 = atan_bounds(F(1, 239))
    return 16*lo5 - 4*hi239, 16*hi5 - 4*lo239


def c_interval(lam, low, high):
    """Outward-rounded decimal enclosure of C(lambda) = sqrt(q/lambda)/(2 pi)."""
    plo, phi = pi_bounds()
    a = (low/lam)/(4*phi**2)
    b = (high/lam)/(4*plo**2)
    return F(sqrt_floor(a, SCALE), SCALE), F(sqrt_floor(b, SCALE)+1, SCALE)


def ratio_text(tc_low, tc_high, t_lam, t_inf):
    lo_l, hi_l = tc_low / t_lam, tc_high / t_lam
    lo_i, hi_i = tc_low / t_inf, tc_high / t_inf
    if abs(lo_l - hi_l) < 1e-12:
        left = f'{lo_l:.3f}'
    else:
        left = f'{lo_l:.3f}--{hi_l:.3f}'
    if abs(lo_i - hi_i) < 1e-12:
        right = f'{lo_i:.3f}'
    else:
        right = f'{lo_i:.3f}--{hi_i:.3f}'
    return f'{left} / {right}'


def main():
    data = json.loads(BRACKETS.read_text(encoding='utf8'))
    record = json.loads((HERE / 'moments.json').read_text(encoding='utf8'))
    kb = record['k_B_eV_per_K']
    cinf = record['C_inf']
    grid = data['q_denominator']
    failures = []

    for case in record['cases']:
        key = f"{case['lambda']:g}"
        if key not in data['q_numerators']:
            raise SystemExit(f'no certified bracket for lambda = {key}')
        left, right = data['q_numerators'][key]
        lam = F(key)
        c_lo, c_hi = c_interval(lam, F(left, grid), F(right, grid))
        c_mid = (float(c_lo) + float(c_hi)) / 2
        root = float(case['M_eV2']) ** 0.5
        t_lam = c_mid * root / kb
        t_inf = cinf * root / kb
        tc_low, tc_high = case['tc_K']
        ratios = ratio_text(tc_low, tc_high, t_lam, t_inf)
        print(f"{case['label']}: lambda {key}, M {case['M_printed']} eV^2, "
              f"C(lambda) in [{float(c_lo):.10f}, {float(c_hi):.10f}], "
              f"T_ceil(lambda) {t_lam:.2f} K, T_ceil,inf {t_inf:.2f} K, "
              f"Tc {case['tc_printed']} K, ratios {ratios}")
        if f'{t_lam:.2f}' != case['t_lam_printed']:
            failures.append((case['label'], 'T_ceil(lambda)', case['t_lam_printed'],
                             f'{t_lam:.2f}'))
        if f'{t_inf:.2f}' != case['t_inf_printed']:
            failures.append((case['label'], 'T_ceil,inf', case['t_inf_printed'],
                             f'{t_inf:.2f}'))
        if ratios != case['ratio_plain']:
            failures.append((case['label'], 'ratios', case['ratio_plain'], ratios))

    if failures:
        for label, field, expected, got in failures:
            print(f'MISMATCH {label} {field}: expected {expected!r}, computed {got!r}')
        raise SystemExit(1)
    print(f'{len(record["cases"])} rows reproduce the manuscript table exactly')
    print('Uncertainties: M carries an indicative digitization uncertainty of 5 percent '
          'for MgB2 and the hydrides and 10 percent for Pb and Nb; the printed ratios are '
          'not intervals and no measured value is used to fit the ceiling.')


if __name__ == '__main__':
    main()
