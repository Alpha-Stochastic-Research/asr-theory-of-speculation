# ASR Bachelier Paper - Technical Review Revision

This package contains the revised paper and companion repository corrections.

## Copy into the repository

- `paper/main.tex`
- `paper/references.bib`
- `figures/fig1_random_walk_martingale.png`
- `figures/fig2_option_pricing_revised.png`
- `.github/workflows/python-ci.yml`
- `src/brownian_motion.py`
- `src/option_pricing.py`
- `requirements-lock.txt`

## Before publishing the new Zenodo version

1. Commit all revised files.
2. Replace `\ReviewedCommit` in `paper/main.tex` with the final full commit SHA.
3. Run `pytest -q` and both reproduction scripts.
4. Compile the paper from `paper/`.
5. Publish the result as the next Zenodo version. The concept DOI already remains stable; Zenodo will assign a new version-specific DOI.
6. Add the author's ORCID to the title page if desired; it was not inserted because the ORCID number was not supplied.

The paper is intended for CC BY 4.0 publication. The software remains under the MIT License.
