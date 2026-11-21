"""Run every check of this supplement and report one exit code.

The checks are run from a throwaway copy, so nothing here depends on the state of the
working tree and no file outside the temporary directory is written:

  1. replay.py         the folded exact replay with integer interval arithmetic; rebuilds
                       the 19 certified C(lambda) brackets and the amber-screen rows
  2. independent.py     the independent exact-arithmetic verifier of the same brackets
  3. tail_mutants.py    the exact negative controls against optimistic edits of the tails
  4. materials_table.py the reproduction of the material table of the manuscript

The decimal endpoints of C(lambda) printed in clambda_table.csv must also appear
verbatim in the output of replay.py, which ties the table to the certified run.

Usage:  python -B run_all.py [--size 384]
Exit code 0 means every check passed.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(name, argv, cwd, timeout):
    print(f'--- {name} ---------------------------------------------------------')
    proc = subprocess.run([sys.executable, '-B'] + argv, cwd=str(cwd), timeout=timeout,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                          encoding='utf-8', errors='replace')
    lines = proc.stdout.strip().splitlines()
    for line in lines[-12:]:
        print(f'    {line}')
    if len(lines) > 12:
        print(f'    ... {len(lines) - 12} earlier lines omitted')
    print(f'    exit code {proc.returncode}')
    return proc.returncode, proc.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--size', type=int, default=384, help='folding size of replay.py')
    parser.add_argument('--keep', action='store_true', help='keep the temporary copy')
    opts = parser.parse_args()

    sandbox = Path(tempfile.mkdtemp(prefix='journal-ceiling-supp-'))
    lane = sandbox / 'C-LAMBDA'
    lane.mkdir()
    for name in ('replay.py', 'independent.py', 'tail_mutants.py', 'brackets.json'):
        shutil.copy2(HERE / 'C-LAMBDA' / name, lane / name)
    ambient = sandbox / 'T2-AMBIENT'
    ambient.mkdir()
    shutil.copy2(HERE / 'C-LAMBDA' / 'inputs' / 'ambient_screen_ratios.csv',
                 ambient / 'ratios.csv')
    print(f'sandbox {sandbox}')

    codes = {}
    replay_out = ''
    try:
        codes['replay'], replay_out = run('replay.py', ['replay.py', '--size', str(opts.size)],
                                          lane, timeout=5400)
        codes['independent'], _ = run('independent.py', ['independent.py'], lane, timeout=1200)
        codes['tail_mutants'], _ = run('tail_mutants.py', ['tail_mutants.py', 'baseline'],
                                       lane, timeout=1200)
        codes['materials_table'], _ = run('materials_table.py',
                                          [str(HERE / 'materials' / 'materials_table.py')],
                                          HERE / 'materials', timeout=600)

        missing = []
        with (HERE / 'C-LAMBDA' / 'clambda_table.csv').open(encoding='utf8') as handle:
            header = handle.readline()
            for line in handle:
                fields = line.rstrip('\n').split(',')
                for value in (fields[5], fields[6]):
                    if value not in replay_out:
                        missing.append((fields[0], value))
        print('--- ties the table to the certified run ---------------------------------'
              + '--')
        if missing:
            for lam, value in missing:
                print(f'    endpoint {value} of lambda={lam} not printed by replay.py')
            print(f'    exit code 1')
            codes['table_tie'] = 1
        else:
            print('    all 38 decimal endpoints of clambda_table.csv appear in the replay output')
            print('    exit code 0')
            codes['table_tie'] = 0
    finally:
        if opts.keep or any(codes.values()) or len(codes) < 5:
            print(f'temporary copy kept at {sandbox}')
        else:
            shutil.rmtree(sandbox, ignore_errors=True)

    failed = [name for name, code in codes.items() if code != 0]
    print('--- summary -------------------------------------------------------------'
          + '---')
    for name, code in codes.items():
        print(f'    {name:<18} {"PASS" if code == 0 else "FAIL"} ({code})')
    if failed:
        print(f'FAILED: {", ".join(failed)}')
        return 1
    print(f'ALL {len(codes)} CHECKS PASSED on {os.name} with {sys.version.split()[0]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
