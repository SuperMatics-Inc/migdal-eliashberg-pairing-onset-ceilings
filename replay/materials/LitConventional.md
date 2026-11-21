# Conventional phonon benchmarks

Sources: [Choi et al.](https://doi.org/10.1103/PhysRevB.66.020513), [Savrasov and Savrasov](https://doi.org/10.1103/PhysRevB.54.16487). Pressure unspecified; equilibrium/ambient-like. Second moments below are **our digitized estimates**, not tabulated by either paper.

| material, spectrum | λ paper; λ trace | ωlog paper | ω̄₂ trace | M eV² | μ*; computed Tc | measured Tc | Tceil; R |
|---|---|---|---|---|---|---|---|
| MgB₂ anharmonic | 0.61; 0.6113 | 63.5 meV | 68.46 meV | ≈0.0028654 | 0.12; anisotropic 39 K, isotropic 19 K | 39 K, Nagamatsu et al., Nature 410, 63 (2001), Choi ref 1 | ≈113.5 K; ≈0.344 |
| MgB₂ harmonic | 0.73; 0.7286 | 59.4 meV | 62.71 meV | ≈0.0028657 | 0.12; anisotropic 55 K, isotropic 28 K | as above | ≈113.5 K; ≈0.344 |
| Pb | 1.68; 1.591 | 65 K | 6.267 meV | ≈0.00006249 | 0.17 fitted; Eliashberg 7.19 K, McMillan 6.81 K | 7.19 K, Savrasov table III, primary Tc source not specified | ≈16.76 K; ≈0.429 |
| Nb | 1.26; 1.184 | 185 K | 17.11 meV | ≈0.0003466 | 0.21 fitted; Eliashberg 9.25 K, McMillan 10.5 K | 9.25 K, Savrasov table III, primary Tc source not specified | ≈39.48 K; ≈0.234 |

Arithmetic: M=λ_trace(ω̄₂/eV)², e.g. MgB₂ anharmonic 0.611345×(0.0684625)²=0.00286544; harmonic 0.728623×(0.0627142)²=0.00286573; Pb 1.59102×(0.00626702)²=0.000062488; Nb 1.18421×(0.0171073)²=0.00034657. Values derived instead by 2∫α²F(E)E dE; ν in THz converted using h×1 THz=0.004135667696 eV. Tceil=0.18272624777232952√M/(8.617333262145×10⁻⁵ eV/K); R=Tc measured/Tceil.

Definitions: Choi states λ=2∫α²F(ω)dω/ω and ωln=exp[(2/λ)∫α²F(ω)lnω dω/ω]. Neither source defines/tabulates the superconducting second moment: our λ-weighted definition is ⟨E²⟩=(2/λ)∫α²F(E)E dE. Savrasov's tabulated transport moment is different. Spectral-overlay checks and exact integration notes are in the briefs; 5% Mg and 10% Pb/Nb M uncertainties are indicative, not confidence intervals. Pb/Nb trace λ misses paper values by 5–6%; do not combine printed λ with trace ω̄₂. MgB₂ is strongly anisotropic; using its isotropic averaged moment does not establish that the isotropic ceiling theorem bounds its observed Tc.

Records/briefs: for doi 10.1103/physrevb.66.020513 and doi 10.1103/physrevb.54.16487, the full-text extractor outputs (results.json, brief.md). Both results validated. No numerical spectral deposits or SI found.
