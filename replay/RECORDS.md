# Records: which released record backs each statement of the manuscript

Every row names a released record, the part of it the manuscript uses, and the status the
manuscript carries. Version numbers are those printed in the records themselves. The
manuscript's reference list numbers these as in `main.tex`; the DOIs and the arXiv
identifier are the primary identifiers.

| record | identifier | used in the manuscript for | status |
|---|---|---|---|
| What a glue moment bounds in linear Eliashberg theory | 10.5281/zenodo.24372930 | the coupled multichannel glue-moment inequality with U = sqrt(6466219/3576050)/(2 pi) = 0.2140146706, the sharp matched single-channel bound it restates, and the width cone of the centered class; its supplement 10.5281/zenodo.24372929 holds the angular-locking argument and the exact limiting coefficient for scaled centered boxes that Theorem 4 uses, together with the Lean sources of the reserve inequalities | PROVED upstream |
| Causal multichannel optimum | 10.5281/zenodo.24374032 | the coupled causal constant sqrt(377/250)/(2 pi) = 0.1954433070, the two-head matrix estimate, the twenty unavoidable head-to-tail contributions, the certified edge reserve d_* = 247/1000 and the weaker reported reserve d = 123/500; supplement 10.5281/zenodo.24374034 holds the replay, the fourteen guarded mutants and the Lean finite cores | PROVED, computer-assisted |
| Centered multichannel ceiling, version 2 | 10.5281/zenodo.24410276 | the centered supremum bound S_cent <= C_3 = sqrt(6811/5000)/(2 pi) = 0.1857550244 with reserve 3189/10000, which is a bound on a supremum and not strict, and the strict bound k_B T_lin < C_* sqrt(rho) with C_* = sqrt(341/250)/(2 pi) = 0.1858777115, reserve 159/500 and slack 9/6820; the comparison C_inf < C_3 < C_*; supplement 10.5281/zenodo.24410275 | PROVED, computer-assisted |
| Finite-energy causal ceiling | 10.5281/zenodo.24380829 | the causal finite-energy constant sqrt(45/32)/(2 pi) = 0.1887345454 and the centered finite-energy constant sqrt(41/30)/(2 pi) = 0.1860593214, the Harnack form of the causal class, and the soft-glue limit of Theorem 4; supplement 10.5281/zenodo.24380827 holds the replay and its Lean finite core | PROVED, computer-assisted |
| Vertex corrections, version 2 | 10.5281/zenodo.24410274 | Theorem 5, the flat-density-of-states inflated ceiling of Eq. (27); Theorem 6, the dichotomy between the nested one-dimensional sheets and the curved surfaces of Eqs. (28) to (30); and the Young-ball all-x contraction of Eq. (31); supplement 10.5281/zenodo.24410273 holds the certified finite-dimensional operator spectra quoted in its text | PROVED, with those spectra certified |
| The Coulomb pseudopotential and the optimality of the Einstein spectrum | 10.5281/zenodo.24409773 | Proposition 4, Coulomb robustness of the ceiling at every pseudopotential, and Proposition 5, fragility of the Einstein optimizer, with the temperature gains 2.59, 29.09 and 82.57 percent and seven exact-arithmetic counterexamples checked by two independent verifiers; supplement 10.5281/zenodo.24409779 holds the repository, which also distributes `C-LAMBDA/brackets.json` | PROVED, and CERTIFIED for the counterexamples |
| Sharp Eliashberg pairing bounds for an energy-dependent density of states | 10.5281/zenodo.24364879 | Theorem 3, the scalar ceiling k_B T_lin < C_inf sqrt(N_max J) for bounded energy-dependent densities of states without reflection symmetry, with the Poisson-kernel estimates and the exact rational Schur bounds; the gauge-fixed eigenvalue normalization used together with the gamma enclosures; supplement 10.5281/zenodo.24364881 | PROVED, computer-assisted |
| unpublished: the coupling-resolved ceilings C(lambda) of Table III | none | the nineteen certified rational brackets, the four guarded mutant rejections, the ambient screen and the threshold mass M*(300 K); computed for this paper, its two certifying programs ship in `C-LAMBDA/` here, and its bracket file is also distributed with the repository of 10.5281/zenodo.24409773 | CERTIFIED here |
| Gamma family | 10.5281/zenodo.24366341 | the certified scalar enclosure C_inf = sqrt(g(2))/(2 pi) = 0.18272624777232952 at seventeen decimals, and outward-rounded enclosures of relative width at most 10^-6 for gamma = 1/2, 1, 3/2 and 3; only the gamma = 2 member enters this paper, as the ceiling C_inf and as the normalization of Table III | CERTIFIED |
| Sharp bounds on the Eliashberg critical temperature | arXiv:2611.20496 | the transfer-by-transfer comparison and the Einstein-line extremality among spectra of a fixed mass and second moment, the sharp single-channel statement, and the comparison principle behind the reduction; the Einstein optimality is not claimed as new in the present paper | PROVED, unrefereed preprint |
| Suppression of electronic pair order for slow lattice phonons | 10.5281/zenodo.24366508 | the slow-phonon lattice programme named in the limits section; supplement 10.5281/zenodo.24366511 | PROVED |
| Limits of defect-insertion bounds for slow-phonon pair order in the Holstein model | 10.5281/zenodo.24385569 | the curvature of the defect-insertion route, named in the limits section; supplement 10.5281/zenodo.24385573 | PROVED |
| Rigorous ceilings on phonon-mediated pairing | 10.5281/zenodo.24406996 | the framing of the ceiling chain and the statement of the programme | review |
| Kondratev, repository manuscript | 10.5281/zenodo.22848039 | cited as an unrefereed secondary source for a normalizing limit in the interval 1.318139 to 1.31815; not relied on, not verified here | unrefereed |

## What each theorem of the manuscript takes from where

| theorem in `main.tex` | inputs |
|---|---|
| model, reduction of the linearized equation to a positive eigenproblem | glue-moment record (the width cone), finite-energy record (the Harnack form of the causal class), energy-dependent-density-of-states record (the Schur bounds), gamma record (the eigenvalue normalization) |
| edge reduction and centered Poisson envelope | glue-moment record and causal-optimum record, where the cone is established |
| causal two-head matrix estimate, the 377/250 constant | causal-optimum record: the twenty head-to-tail terms, the two-head estimate, the certified reserve |
| centered estimates, the constants C_3 and C_* | centered record, version 2 |
| finite-energy constants | finite-energy record |
| flat-density-of-states inflated ceiling, Eq. (27) | vertex record, Theorem V1 |
| nested-sheet versus curved-surface dichotomy, Eqs. (28) to (30) | vertex record, Theorem V3 |
| Young-ball all-x contraction, Eq. (31) | vertex record, Theorem V3b |
| Coulomb robustness and optimizer fragility, Propositions 4 and 5 | Coulomb record, 10.5281/zenodo.24409773 |
| soft-glue limit, Theorem 4 | finite-energy record for the limit, with the angular-locking argument and the exact scaled-box coefficient from the supplement of the glue-moment record, 10.5281/zenodo.24372929 |
| coupling-resolved ceilings and the material table | this paper's two supplementary programs for the brackets, the gamma record for the eigenvalue enclosure, the comparison theorem of arXiv:2611.20496 for the reduction, and the digitization notes in `materials/` |

## Corrections carried in this manuscript

The material table recomputes two printed decimals from the source records:

* the scalar ceiling for the isotropic reference of MgB2 is 113.51 K, not 113.50 K: exact
  recomputation with the same moments and constants gives 113.5065 K, so the 113.504 K printed
  in `C-LAMBDA/RESULT.md` line 32 of the repository of DOI 10.5281/zenodo.24409773 is an
  arithmetic slip of about 0.002 K, far inside the stated five percent uncertainty in the
  second moment; that number is not used by any ceiling of that record;
* the ratio of 244 K to 367.18 K is 0.66452 and rounds to 0.665; earlier drafts truncated
  it to 0.664.

Neither correction changes any ceiling, any interval, or the status of any statement.
