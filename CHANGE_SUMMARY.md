# Technical-review changes applied

- Replaced the incomplete martingale proof with a conditional-expectation proof.
- Reframed option pricing using a forward price, discount factor, and forward measure.
- Identified the numerical formula as the zero-rate, unit-discount special case.
- Replaced "validation" language with "numerical corroboration" where appropriate.
- Added Monte Carlo uncertainty, a 95% interval, and standardized discrepancy.
- Added a visible normal-vs-lognormal pricing-difference panel.
- Quantified the maximum local Bachelier/Black-Scholes difference on the plotted grid.
- Corrected LaTeX figure paths for compilation from the `paper/` directory.
- Added PDF title, author, subject, and keyword metadata.
- Added paper version, concept DOI, software version, and reviewed commit metadata.
- Added specialist historical references on Bachelier.
- Updated the repository structure and reproduction commands.
- Distinguished the article's CC BY 4.0 licence from the software's MIT License.
- Clarified that no external empirical dataset is used.
- Added a push/pull-request GitHub Actions workflow.
- Replaced the duplicated Brownian-motion script implementation with a thin package wrapper.
- Added a revised option-pricing script that generates the three-panel figure.
- Added a pinned reproduction-environment file.

Before the next Zenodo publication, replace the reviewed commit in `paper/main.tex` with the final commit SHA after all revised files are merged.
