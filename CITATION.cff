# Reproducibility

This document explains how to reproduce the numerical experiments, figures, tests, and package-level examples for the ASR Bachelier research repository.

## Project

**Bachelier (1900): Theory of Speculation**  
**Reproducible Python Package for the Origins of Quantitative Finance**

This repository is both:

1. a reproducible research repository; and
2. an installable Python package exposing:

```python
from asr.models import bachelier
```

---

## Reproducibility Principles

This project follows the Alpha Stochastic Research reproducibility standard:

- explicit dependencies;
- fixed random seeds;
- deterministic figure-generation scripts;
- tested Python source code;
- installable package structure;
- documented public API;
- notebook-based interactive reproduction;
- citation metadata;
- open-source licensing.

---

## Recommended Environment

Recommended Python version:

```text
Python 3.10 or later
```

The continuous integration workflow currently tests with:

```text
Python 3.12
```

---

## Installation Options

There are two supported ways to use the repository.

---

## Option 1 — Package Installation

This is the recommended method for research and development.

Clone the repository:

```bash
git clone https://github.com/Alpha-Stochastic-Research/asr-theory-of-speculation.git
cd asr-theory-of-speculation
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install the project as an editable package with development dependencies:

```bash
pip install -e ".[dev]"
```

After installation, the package can be imported from anywhere inside the environment:

```python
from asr.models import bachelier
```

---

## Option 2 — Use Without Package Installation

The repository can also be used without installing the package.

From the repository root, the reproduction scripts work directly:

```bash
python src/brownian_motion.py
python src/option_pricing.py
```

For direct one-line Python usage without installation, add `src/` to `PYTHONPATH`.

On macOS or Linux:

```bash
PYTHONPATH=src python -c "from asr.models import bachelier; print(bachelier.call_price(100, 100, 2, 1))"
```

On Windows PowerShell:

```powershell
$env:PYTHONPATH="src"
python -c "from asr.models import bachelier; print(bachelier.call_price(100, 100, 2, 1))"
```

This allows the public API to be used without running `pip install -e .`.

However, for a clean and persistent research environment, the editable installation method is preferred.

---

## Dependencies

The main runtime dependencies are:

```text
numpy
scipy
matplotlib
```

Development and notebook dependencies are:

```text
pytest
pandas
jupyter
notebook
```

They are listed in:

```text
pyproject.toml
requirements.txt
```

---

## Public API Check

After installation, or after setting `PYTHONPATH=src`, verify the public import:

```bash
python - <<'PY'
from asr.models import bachelier

print("ASR Bachelier package version:", bachelier.__version__)

price = bachelier.call_price(
    initial_price=100.0,
    strike=100.0,
    volatility=2.0,
    maturity=1.0,
)

print("Bachelier ATM call price:", price)
PY
```

Expected behaviour:

```text
The package imports successfully and prints a positive Bachelier call price.
```

---

## Reproducing the Brownian Motion Experiment

Run:

```bash
python src/brownian_motion.py
```

This script:

- simulates Bachelier arithmetic Brownian motion;
- verifies the empirical martingale behaviour;
- compares empirical and theoretical variance;
- saves the Brownian motion figure.

Expected generated file:

```text
figures/fig1_random_walk_martingale.png
```

---

## Reproducing the Option Pricing Experiment

Run:

```bash
python src/option_pricing.py
```

This script:

- computes the Bachelier closed-form call price;
- estimates the same price using Monte Carlo simulation;
- reports the Monte Carlo standard error;
- generates the option pricing comparison figure.

Expected generated file:

```text
figures/fig2_option_pricing.png
```

---

## Reproducing All Figures

From the repository root:

```bash
python src/brownian_motion.py
python src/option_pricing.py
```

Expected outputs:

```text
figures/fig1_random_walk_martingale.png
figures/fig2_option_pricing.png
```

---

## Running the Test Suite

Run:

```bash
pytest -q
```

The test suite validates:

- public package imports;
- path simulation shape;
- fixed-seed reproducibility;
- initial price consistency;
- martingale behaviour;
- variance scaling;
- Bachelier option pricing formula;
- Monte Carlo pricing accuracy;
- Black-Scholes benchmark behaviour;
- invalid input handling;
- high-level experiment functions.

---

## Notebook Reproduction

An interactive Jupyter notebook is available at:

```text
notebooks/bachelier_theory_of_speculation_reproduction.ipynb
```

Run it with:

```bash
jupyter notebook notebooks/bachelier_theory_of_speculation_reproduction.ipynb
```

The notebook reproduces:

- arithmetic Brownian motion simulations;
- martingale checks;
- variance scaling;
- Bachelier option pricing;
- Monte Carlo validation;
- at-the-money square-root-of-time scaling;
- comparison with Black-Scholes.

The notebook uses the package implementation from:

```text
src/asr/models/bachelier/
```

---

## Random Seeds

The numerical experiments use fixed seeds for reproducibility:

| Experiment | Seed |
|---|---:|
| Brownian motion simulation | `42` |
| Option pricing Monte Carlo | `7` |

Changing the seeds will change the simulated paths and Monte Carlo estimates, but the analytical relationships remain unchanged.

---

## Main Numerical Parameters

Default Brownian motion experiment:

| Parameter | Value |
|---|---:|
| Initial price | `100.0` |
| Arithmetic volatility | `2.0` |
| Maturity | `1.0` |
| Number of steps | `250` |
| Number of paths | `5,000` |

Default option pricing experiment:

| Parameter | Value |
|---|---:|
| Initial price | `100.0` |
| Strike | `100.0` |
| Arithmetic volatility | `2.0` |
| Maturity | `1.0` |
| Monte Carlo paths | `500,000` |

---

## Continuous Integration

The GitHub Actions workflow is located at:

```text
.github/workflows/python-ci.yml
```

It automatically checks that:

- the package installs correctly;
- the public import interface works;
- the test suite passes;
- both reproduction scripts run;
- both figures are generated.

---

## Paper Reproduction

The LaTeX paper source is located in:

```text
paper/main.tex
```

To compile it from the `paper/` directory:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

The paper expects the generated figures to be available in:

```text
figures/
```

---

## Clean Rebuild

To rebuild figures from scratch:

```bash
rm -f figures/fig1_random_walk_martingale.png
rm -f figures/fig2_option_pricing.png

python src/brownian_motion.py
python src/option_pricing.py
```

On Windows PowerShell:

```powershell
Remove-Item figures/fig1_random_walk_martingale.png -ErrorAction SilentlyContinue
Remove-Item figures/fig2_option_pricing.png -ErrorAction SilentlyContinue

python src/brownian_motion.py
python src/option_pricing.py
```

---

## Expected Reproducibility Standard

A successful reproduction means that:

```text
pytest -q
```

passes successfully, and the following files are generated:

```text
figures/fig1_random_walk_martingale.png
figures/fig2_option_pricing.png
```

The exact Monte Carlo numbers may vary if seeds, Python versions, NumPy versions, or simulation parameters are changed.

---

## Citation

If this repository is used in research, teaching, or open-source work, cite the repository using:

```text
CITATION.cff
```

Suggested citation:

```text
Alpha Kabinet TOURE and Alpha Stochastic Research.
Bachelier (1900): Theory of Speculation — Reproducible Python Package.
Alpha Stochastic Research, 2026.
https://github.com/Alpha-Stochastic-Research/asr-theory-of-speculation
```

---

## Contact

Alpha Stochastic Research  
Independent Quantitative Finance Research Laboratory

Website:

```text
https://asr-lab.online
```

Research contact:

```text
research@asr-lab.online
```
