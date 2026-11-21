# Hydride Eliashberg moments: Errea and Duan

**Result:** Errea LaH10/LaD10 has no tabulated second moment, but its plotted calculated α²F supports approximate integrated M; H3S Errea has neither tabulation nor α²F plot, and Duan’s raster spectra could not be extracted reliably. Do not use ωlog as ω̄₂.

| system, P GPa | λ | ωlog meV | ω̄₂ meV* | M eV²* | Tceil K* | Tc AD K | Tc ME / SCDFT K |
|---|---:|---:|---:|---:|---:|---:|---:|
| LaH10 129 | 3.62 | 76.4 | 100.86 | 0.036826 | 406.9 | 252.6 | 255.3 / 230 |
| LaH10 163 | 2.67 | 96.4 | 121.27 | 0.039267 | 420.2 | 247.0 | 242.8 / 225 |
| LaH10 214 | 2.06 | 115.5 | 142.22 | 0.041668 | 432.8 | 235.9 | 237.9 / 210 |
| LaH10 264 | 1.73 | 126.6 | 156.94 | 0.042610 | 437.7 | 219.2 | 216.9 / 201 |
| LaD10 159 | 3.14 | 63.5 | 79.16 | 0.019675 | 297.4 | 184.2 | 180.4 / 171 |
| LaD10 210 | 2.21 | 81.7 | 97.27 | 0.020909 | 306.6 | 176.5 | 172.9 / 158 |
| LaD10 260 | 1.80 | 92.2 | 108.92 | 0.021355 | 309.9 | 164.6 | 157.9 / 151 |

All λ, ωlog and Tc are **calculated**, Extended Data Table I (T1), [Errea et al.](https://doi.org/10.1038/s41586-020-1955-z). AD uses μ*=0.1; anisotropic ME and SCDFT use ab initio screened Coulomb interactions, not the same empirical μ*. *M uses trapezoidal 2∫α²F(E)E dE (E in eV), vector-digitized Extended Data Figs 4/5 (F7/F8). ω̄₂=√(M/λ), λ-weighted; this is our definition, not one quoted by the paper. Tceil=0.18272624777232952√M/kB, kB=8.617333262e-5 eV/K. Arithmetic e.g. 129 GPa: 3.62 × (0.10086 eV)² ≈ 0.036826 eV²; 163 GPa: 2.67 × (0.12127 eV)² ≈ 0.039267 eV². All plotted integrations approximate, not published values; original curve overlays were checked, legend fragments discarded; numerical λ reintegrals 3.6166, 2.6660, 2.0547, 1.7270 and 3.1317, 2.2131, 1.7977 agree with tabulation. No quantified digitization uncertainty. Sources show pressure trends, not independent measurements.

Errea H3S [2016](https://doi.org/10.1038/nature17175) cites measured 203 K at 155 GPa (Drozdov et al. Nature 525, 73 (2015)); isotope/pressure Tc graph uses isotropic ME with μ*=0.16. No spectral plot or moments. Duan [2014](https://doi.org/10.1038/srep06968): R3m 130 GPa λ=2.07, ωlog=1125.1 K, Tc=155–166 K; Im-3m 200 GPa λ=2.19, ωlog=1334.6 K, Tc=191–204 K; Tc uses μ*=0.1–0.13. Predicted, not measured. No moment tabulated; Fig 5 α²F raster has vertical frequency, overlapping curves and incomplete digitization. No M reported. This 2014 work predates measured H3S Tc.

LaH10 comparison cites Somayazulu et al. PRL 122, 027001 (2019), and Drozdov et al. Nature 569, 528 (2019): ~250 K measured over 137–218 GPa, not a pressure-matched point here; no defensible measured Tc/Tceil ratio without matching the original data. Data/code: no deposited numerical α²F located; source arXiv figure files available. Duan SI is downloaded legacy DOC but not decoded; it may contain missing values. Bundle originals, CSVs, overlays and structured results remain internal-only.

## Drozdov measured comparisons (nearest calculated pressure)
| sample; measured P (GPa), Tc (K) | theory P (GPa); ΔP = measured − theory | R; band from M ±5% only |
|---|---|---|
| LaH10 135, ~245 | 129; +6 | 0.602 [0.588, 0.618] |
| LaH10 145, ~244 | 129; +16 | 0.600 [0.585, 0.615] |
| LaH10 150, ~249 | 163; −13 | 0.593 [0.578, 0.608] |
| LaH10 151, ~249 | 163; −12 | 0.593 [0.578, 0.608] |
| LaH10 ~170, 250–252 | 163; +7 | 0.597 [0.583, 0.613] using 251 K |
| LaD10-assigned 139, ~150 | 159; −20 | 0.504 [0.492, 0.517] |
| LaD10-assigned 145, ~160 | 159; −14 | 0.538 [0.525, 0.552] |
| LaD10-assigned 152, ~166 | 159; −7 | 0.558 [0.545, 0.573] |
The H values are stated in [Drozdov et al.](https://doi.org/10.1038/s41586-019-1201-8), Fig. 1 caption and text; the D points are visual estimates from Extended Data Fig. 4 inset, ±2 K reading uncertainty. The highest-Tc deuteride's Fm-3m/LaD10 assignment is **assumed, not structurally determined**; the ~140 K phase is instead tetragonal. Figure 1 Tc criterion is not explicitly defined as onset or midpoint; the inset's D criterion likewise unspecified. Do not substitute the field-analysis 90%/50% criteria as these points' definitions.
Pressure uses H2/D2 vibron scale; no symmetric uncertainty stated. At ~150 GPa diamond Raman scale gives 10–30 GPa higher values, a systematic scale discrepancy, not a ± error bar. Ratios use the plotted-spectrum ceiling above; the band is R/√1.05 to R/√0.95 and excludes pressure mismatch, experimental Tc uncertainty, phase ambiguity and unquantified digitization error; ±5% is an assumed sensitivity, not a validated uncertainty.
