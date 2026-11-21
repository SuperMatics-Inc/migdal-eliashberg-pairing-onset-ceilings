"""Exact negative controls against optimistic edits to the two tail proofs."""
import argparse
from fractions import Fraction as F
from pathlib import Path


LANE = Path(__file__).resolve().parents[1] / 'C-LAMBDA'


class InvalidTailBound(Exception):
    pass


def load(filename, replacement=None):
    path = LANE / filename
    source = path.read_text(encoding='utf8')
    if replacement is not None:
        old, new = replacement
        if source.count(old) != 1:
            raise ValueError(f'expected exactly one mutation target: {old}')
        source = source.replace(old, new)
    ns = {'__name__': '_review_probe', '__file__': str(path)}
    exec(compile(source, str(path), 'exec'), ns)
    return ns


def folded_check(mutate):
    # Understate the two-term folded cross block by dropping the factor 2.
    edit = ('v = (2*b)**2 *', 'v = b**2 *') if mutate else None
    ns = load('replay.py', edit)
    sqrt_floor = ns['sqrt_floor']
    used_bounds = []

    def capture(v, scale):
        candidate = sqrt_floor(v, scale)
        used_bounds.append(F(candidate+1, scale))
        return candidate

    ns['sqrt_floor'] = capture
    n = 32
    ns['signed_check'](F(1), F(1), [1] * n, True)
    if len(used_bounds) != n:
        raise ValueError('failed to capture the production cross-column bounds')
    # Exact lower bound: only N out of the infinitely many tail sites. Scale
    # individual squares down to avoid unnecessarily huge common denominators.
    scale = 10**30
    floor_sum = 0
    for j in range(n, 2*n):
        square = (F(1, 1+j*j) + F(1, 1+(j+1)**2))**2
        floor_sum += int(scale*square)
    partial = F(floor_sum, scale)
    u2 = used_bounds[0]**2
    print(f'folded i=0, N={n}: partial exact lower {float(partial):.9g}; '
          f'claimed upper {float(u2):.9g}')
    if partial > u2:
        raise InvalidTailBound('folded cross-column squared norm exceeds its claimed upper bound')


def cubic_check(mutate):
    # Apply the far-source t estimate at every tail row, skipping the near scan.
    edit = ('return up(max(far, *near)) + 1', 'return up(far) + 1') if mutate else None
    n = 32
    ns = load('independent.py', edit)
    lattice = ns['Lattice'](n, F(1), F(1))
    head = [1] * (n-1) + [10**6]
    t = lattice.tail_need(head)
    if t is None:
        raise ValueError('tail positivity precondition failed')
    # At j=N, compare the exact diagonal against the head source, and check
    # the unchanged guard also has positive margin after the bounded tail feed.
    a = lambda k: F(1, 1 + k*k)
    source = sum((a(n-i)+a(n+i+1))*x for i, x in enumerate(head))
    h_n = F(t, (n+1)**3)
    normal = 2*n + 1 + a(0) + 2*sum(a(k) for k in range(1, n+1))
    lower_margin = (2*n+1 - 8*lattice.row - 5*lattice.b*(n+1)/(2*n*n))*h_n - source
    print(f'cubic j=N={n}: t={t}, exact diagonal minus head source '
          f'{float(normal*h_n-source):.9g}; margin lower bound {float(lower_margin):.9g}')
    if normal*h_n <= source:
        raise InvalidTailBound('first tail row is negative even before adding any tail-to-tail attraction')
    if lower_margin <= 0:
        raise InvalidTailBound('first tail row lacks the claimed positive lower margin')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('baseline', 'schur-no-factor-two', 'cubic-no-near-scan'))
    mode = parser.parse_args().mode
    try:
        if mode in ('baseline', 'schur-no-factor-two'):
            folded_check(mode != 'baseline')
        if mode in ('baseline', 'cubic-no-near-scan'):
            cubic_check(mode != 'baseline')
    except InvalidTailBound as error:
        parser.exit(1, f'{error}\n')
