# Supplement: certified computations, records and replay

This archive accompanies the manuscript "Certified ceilings for the Migdal-Eliashberg
linear pairing onset" in the parent directory. It contains everything the manuscript's
numerical and computer-assisted statements rest on, in a form that can be re-run from a
clean copy.

## Contents

| path | what it is |
|---|---|
| `run_all.py` | driver that runs every check from a throwaway copy and reports one exit code |
| `C-LAMBDA/replay.py` | folded exact replay with integer interval arithmetic; written for this paper and first published here |
| `C-LAMBDA/independent.py` | independent exact-arithmetic verifier of the same brackets; written for this paper and first published here |
| `C-LAMBDA/tail_mutants.py` | exact negative controls against optimistic edits of the two tail estimates that bracket certification relies on, the folded cross block and the cubic near-scan; written for this paper and first published here |
| `C-LAMBDA/brackets.json` | the nineteen certified rational q-brackets of C(lambda), reduced from the `brackets.json` distributed with the repository of DOI 10.5281/zenodo.24409773 (SHA-256 `6152ba4201996d66...`), with the ambient-screen numerators kept apart, see below |
| `C-LAMBDA/clambda_table.csv` | the nineteen brackets as outward-rounded decimals, with C/C_inf and the coupling-resolved threshold mass M*(300 K) |
| `C-LAMBDA/inputs/ambient_screen_ratios.csv` | the input table of the ambient screening arm of `replay.py`; a screen input, not a certification, kept separate from the nineteen certificates, and not previously released |
| `materials/moments.json` | the four digitized moments, literature couplings, measured transition temperatures, their sources and their caveats |
| `materials/LitConventional.md`, `materials/LitHydrides.md` | the digitization records of the conventional and hydride spectra, reproduced verbatim from the author's digitization notes and not previously released |
| `materials/materials_table.py` | recomputes every entry of the manuscript's material table from `moments.json` and `brackets.json` and compares it with the printed string |
| `RECORDS.md` | which released record each theorem and constant of the manuscript comes from |
| `MANIFEST.sha256` | SHA-256 of every file here except itself, by `hashlib` |

## The nineteen certificates and the ambient screen are separate

The released `brackets.json` contains twenty-eight row pairs: nine coupling grid rows,
ten material-coupling rows at conventional and hydride couplings, and nine ambient-screen
rows. The ambient rows come from an external screen whose moments carry their own
uncertainties and are not part of the ceiling chain, so they are not shipped as
certificates here. They are reached only through the screen input in
`C-LAMBDA/inputs/` and are labelled as a screen wherever they appear.

## How to re-run

Python 3.12 with numpy and scipy is required. Tested on Windows with Python 3.12.10,
numpy 2.5.3 and scipy 1.18.1.

```
cd <this directory>
python -B run_all.py
```

The driver copies the four scripts into a temporary directory, writes the ambient screen
input where `replay.py` expects it, and runs:

```
python -B replay.py --size 384          # folded exact replay, 19 brackets + 4 mutants
python -B independent.py                # independent exact verifier of the same brackets
python -B tail_mutants.py baseline      # exact negative controls of the tail proofs
python -B materials/materials_table.py  # the material table of the manuscript
```

It also asserts that all thirty-eight decimal endpoints of `clambda_table.csv` appear
verbatim in the output of `replay.py`, so the table cannot drift from the certified run.
Exit code 0 means every check passed; on failure the temporary copy is kept and its path
is printed.

Expected output shape: `replay.py` certifies each bracket in integer interval arithmetic
and rejects four mutations, `independent.py` re-derives the same brackets by an independent
exact-arithmetic route, `tail_mutants.py baseline` exits 0 (its mutation modes exit 1 and
are the negative controls), and `materials_table.py` reports that all four rows of the
table reproduce exactly.

## What is not deposited

The numerical Eliashberg functions behind the four moments in `materials/moments.json`
are not deposited. Those spectra are figures in third-party papers, and the material here
is the digitization record: the quoted couplings, characteristic frequencies, the squared
characteristic frequency, the resulting second moment, and the locator of every figure and
table the values were read from. The consequence for a reader is stated in the
manuscript: the moments carry an indicative uncertainty of five percent for the boride and
the hydrides and ten percent for the two conventional metals, the printed ratios are not
intervals, and no measured transition temperature enters the ceiling.

The Lean 4.35.0 sources of the reserve inequalities are not repeated here. They ship with the
supplements of the glue-moment, causal-optimum and finite-energy records (DOIs
10.5281/zenodo.24372929, 10.5281/zenodo.24374034, 10.5281/zenodo.24380827) and check the
finite rational cores of those coupled reserve inequalities. The scalar coupling-resolved
brackets of Table III are a different computation: they are certified by the two exact
programs in `C-LAMBDA/` shipped above, and that certification is not formalized.
