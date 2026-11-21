# Certified ceilings for the Migdal-Eliashberg linear pairing onset

Davis Rens, SuperMatics Inc. ([ORCID 0000-0001-5839-5197](https://orcid.org/0000-0001-5839-5197)).
Version 1.0.0.

Paper DOI: <https://doi.org/10.5281/zenodo.24411775>
Replay supplement DOI: <https://doi.org/10.5281/zenodo.24411779>
Source: <https://github.com/SuperMatics-Inc/migdal-eliashberg-pairing-onset-ceilings>

## What this deposit is

This repository carries the consolidated preprint `paper/main.pdf` (16 pages) and the complete replay
supplement for it. The manuscript states, in one notation and with the reduction proved in full, a chain of
rigorous upper bounds on the linear pairing onset temperature of a reciprocal multichannel
Migdal-Eliashberg model and places those bounds against the literature and against four digitized material
second moments. It consolidates eleven released and independently reviewed records and adds four
organizational or expository contributions of its own: one statement of the model and of the two classes of
normal branches, a complete proof of the reduction from a single edge inequality to the ceiling, one ordered
table of every constant with the reserve that produces it and the record that certifies it, and the placement
against the literature and the material second moments. The nineteen exact rational brackets of the
coupling-resolved ceiling `C(lambda)` of Table III are computed for this paper and are first published here,
with the two programs that certify them.

## Scope and labels

The bounds read `k_B T_lin < C sqrt(rho)`, where `rho` is the norm of the glue moment matrix of the model.
The sharpest supremum bound for the centered class of normal branches is `C_3 = sqrt(6811/5000)/(2 pi)`,
which rounds to `0.1857550244` and is guaranteed only in the non-strict form. The sharpest strict bound is
`k_B T_lin < C_* sqrt(rho)` with `C_* = sqrt(341/250)/(2 pi)`, which rounds to `0.1858777115`, at the exact
rational slack `9/6820`. For the wider causal class the strict constant is `sqrt(45/32)/(2 pi)`, which
rounds to `0.1887345454`. The exact scalar Einstein constant is `C_inf = 0.18272624777232952`, certified to
an enclosure of relative width below `6e-17`. The coupled constants therefore lie in the interval
`[C_inf, C_3]`; the lower endpoint is attained in the soft-glue limit with equitably coupled channels, and
whether a model at finite moment attains it is open.

`T_lin` is the linear onset temperature of the linearized model. It is not identified with the transition
temperature of any exact Hamiltonian or with a measured value, no material is claimed to be a superconductor,
the material rows of the paper are ratios whose denominators are computed and whose numerators are literature
values with an indicative uncertainty of five to ten percent, and the third-party Eliashberg spectra behind
those moments are figures in the cited papers and are not redistributed here.

| Result | Label | Evidence |
|---|---|---|
| Ceiling chain for the centered and causal classes, and the reduction from one edge inequality | PROVED | `paper/main.tex`, sections 2 to 4; `replay/RECORDS.md` names the certified record behind each constant |
| Exact scalar constant `C_inf = 0.18272624777232952` | PROVED upstream, CERTIFIED enclosure | `paper/main.tex` section 5; the enclosure ships with DOI 10.5281/zenodo.24366341, not here |
| Nineteen exact rational brackets of `C(lambda)`, four guarded mutant rejections, and the ambient screen input | CERTIFIED here | `replay/C-LAMBDA/replay.py`, `replay/C-LAMBDA/independent.py`, `replay/C-LAMBDA/tail_mutants.py` |
| Material table reproduction from digitized moments and certified brackets | CERTIFIED here | `replay/materials/materials_table.py`, `replay/materials/moments.json` |
| Whether the coupled supremum equals `C_inf`, and the full crossed-vertex statement | OPEN | `paper/main.tex` section 6 |

## Layout

| Path | Contents |
|---|---|
| `paper/` | `main.tex`, `refs.bib` and `main.pdf`, the released bytes. The only change from the reviewed source is the publication metadata block: the `\PAPERDOI` and `\SUPPLEMENTDOI` macros and one data availability sentence |
| `replay/` | the reviewed supplementary archive: both certifying programs, the negative controls, the nineteen brackets, the ambient screen input, the digitization records, the table reproduction script, the record index `RECORDS.md`, and `MANIFEST.sha256` pinning its thirteen files |
| `MANIFEST.sha256` | SHA-256 of every tracked file of this repository except itself |
| `CITATION.cff` | citation metadata for the preprint and for this supplement |

The reviewed supplementary archive addresses the manuscript as being "in the parent directory". In this
repository the manuscript source is `paper/` and the archive content is `replay/`.

## Replay

The supplement imports only `numpy` and `scipy` beyond the Python standard library. Python 3.12 with
`numpy==2.5.3` and `scipy==1.18.1` is what the deposited runs used:

```sh
sha256sum -c MANIFEST.sha256
(cd replay && sha256sum -c MANIFEST.sha256)
(cd replay && python -B run_all.py)
```

`run_all.py` copies the four programs into a throwaway directory and runs the folded exact replay, the
independent exact verifier of the same brackets, the exact negative controls of the two tail estimates, and
the material table reproduction. It also requires the thirty-eight decimal endpoints of the bracket table to
appear verbatim in the certified replay output. Exit code 0 means every check passed, and the negative
controls are run separately because each of them must exit 1:

```sh
(cd replay/C-LAMBDA && python -B tail_mutants.py schur-no-factor-two)
(cd replay/C-LAMBDA && python -B tail_mutants.py cubic-no-near-scan)
```

The programs check finite exact statements only. They do not formalize the analytic arguments that apply
them, and the Lean formalizations quoted by the paper ship with the supplements of the cited records.

## Build

The manuscript is built from `paper/` with Tectonic 0.17.0 and a fixed timestamp:

```sh
cd paper && SOURCE_DATE_EPOCH=1795132800 tectonic -X compile main.tex --keep-logs
```

The build reports no overfull box, no undefined reference and no undefined citation, and one cosmetic
underfull box. Tectonic output is not byte reproducible, so `paper/main.pdf` is the local build that was
deposited, and the workflow checks its own rebuild log and text rather than the hash of a rebuild.

## Licenses and provenance

The replay code and the documentation in this repository are licensed under Apache-2.0. The preprint is
distributed under CC-BY-4.0 through its Zenodo record.

AI agents generated proofs, certificates, code, and manuscript drafts and edits under D. Rens' direction and
review. Separate AI agents performed the independent reviews of the cited records. This preprint has not
been peer reviewed.
