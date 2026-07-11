<div align="center">

<!--<img src="assets/logo.png" alt="Alpha Stochastic Research Logo" width="130">-->

# Bachelier (1900): Theory of Speculation

### ASR-Compatible Reproducible Python Package for the Origins of Quantitative Finance

**Alpha Stochastic Research**  
*Independent Quantitative Finance Research Laboratory*

<br>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)](https://scipy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge)](https://matplotlib.org/)
[![Pytest](https://img.shields.io/badge/Pytest-Tested-0A2540?style=for-the-badge)](https://docs.pytest.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![License](https://img.shields.io/badge/License-MIT-16A34A?style=for-the-badge)](LICENSE)

<br>

[![Website](https://img.shields.io/badge/Website-asr--lab.online-0A2540?style=for-the-badge)](https://asr-lab.online)
[![Research](https://img.shields.io/badge/Research-research@asr--lab.online-0A2540?style=for-the-badge)](mailto:research@asr-lab.online)

</div>

---

## Overview

This repository provides a modern, reproducible reconstruction of Louis Bachelier's 1900 doctoral thesis:

> **Théorie de la Spéculation**

Bachelier's work is one of the earliest mathematical foundations of modern quantitative finance. It introduced a probabilistic framework for modelling price fluctuations using what is now recognized as arithmetic Brownian motion.

This project is both:

1. a reproducible research repository; and  
2. an installable Python package.

It is compatible with the Alpha Stochastic Research open-science ecosystem through the shared ASR namespace:

```python
from asr.models import bachelier
```

The distribution name is:

```bash
pip install asr-theory-of-speculation
```

The ASR ecosystem meta-package is:

```bash
pip install asr-open-sc
```

At this stage, `asr-open-sc` acts as the lightweight ecosystem registry. The Bachelier module is provided by this repository through the `asr-theory-of-speculation` distribution.

The repository includes:

- arithmetic Brownian motion simulations;
- numerical verification of martingale and variance-scaling properties;
- Bachelier European call option pricing;
- Monte Carlo validation;
- comparison with Black-Scholes under low relative volatility;
- reusable Python package API;
- reproducible figure-generation scripts;
- automated tests;
- interactive Jupyter notebook;
- LaTeX working paper source;
- citation metadata;
- open-source documentation.

---

## Public Package Interface

This repository exposes the Bachelier model under the shared Alpha Stochastic Research namespace:

```python
from asr.models import bachelier
```

The installation package is:

```bash
pip install asr-theory-of-speculation
```

The import path is:

```python
asr.models.bachelier
```

Example:

```python
from asr.models import bachelier

time_grid, paths = bachelier.simulate_paths(
    initial_price=100.0,
    volatility=2.0,
    maturity=1.0,
    n_steps=250,
    n_paths=5_000,
    seed=42,
)

analysis = bachelier.analyze_paths(
    time_grid=time_grid,
    paths=paths,
    initial_price=100.0,
    volatility=2.0,
)

price = bachelier.call_price(
    initial_price=100.0,
    strike=100.0,
    volatility=2.0,
    maturity=1.0,
)

print(analysis.terminal_mean)
print(price)
```

This package is part of the broader ASR open-science Python ecosystem:

```text
asr.open_sc
asr.models.bachelier
asr.risk.tail
asr.portfolio.optimization
asr.ml.deep_hedging
asr.agents.trading
```

The ecosystem meta-package is maintained separately in:

```text
https://github.com/Alpha-Stochastic-Research/asr-open-sc
```

---

## Research Objective

The objective of this project is to connect historical financial mathematics with modern reproducible research.

This repository aims to:

- preserve one of the foundational works of quantitative finance;
- provide readable Python implementations;
- expose a reusable package interface;
- make the numerical results reproducible;
- explain the mathematical structure behind Bachelier's model;
- support students, researchers, and practitioners interested in financial mathematics;
- provide a transparent open-science research package.

---

## Mathematical Framework

Bachelier models the price process as an arithmetic Brownian motion:

```math
P_t = P_0 + \sigma W_t
```

where:

- `P_t` is the price at time `t`;
- `P_0` is the initial price;
- `σ` is the arithmetic volatility;
- `W_t` is a standard Brownian motion.

This implies:

```math
\mathbb{E}[P_t] = P_0
```

and

```math
\mathrm{Var}(P_t) = \sigma^2 t
```

The model is simple, elegant, and historically important. It also has a structural limitation: because prices are normally distributed, negative prices are theoretically possible.

---

## Option Pricing

Under the Bachelier model, the terminal price is:

```math
P_T = P_0 + \sigma \sqrt{T} Z
```

where:

```math
Z \sim \mathcal{N}(0,1)
```

For a European call option with strike `K`, the Bachelier price is:

```math
C = (P_0 - K)\Phi(d) + \sigma\sqrt{T}\phi(d)
```

with:

```math
d = \frac{P_0 - K}{\sigma\sqrt{T}}
```

where:

- `Φ` is the standard normal cumulative distribution function;
- `φ` is the standard normal probability density function.

For an at-the-money call, where `K = P_0`, the formula simplifies to:

```math
C_{ATM} = \sigma\sqrt{T}\phi(0)
```

This illustrates the square-root-of-time scaling of option values in the Bachelier framework.

---

## Repository Structure

```text
asr-theory-of-speculation
├── .github/
│   └── workflows/
│       └── python-ci.yml
├── assets/
│   └── logo.png
├── figures/
│   ├── fig1_random_walk_martingale.png
│   └── fig2_option_pricing.png
├── notebooks/
│   └── bachelier_theory_of_speculation_reproduction.ipynb
├── paper/
│   ├── main.tex
│   ├── references.bib
│   └── README.md
├── src/
│   ├── brownian_motion.py
│   ├── option_pricing.py
│   └── asr/
│       └── models/
│           └── bachelier/
│               ├── __init__.py
│               ├── pricing.py
│               ├── process.py
│               └── simulation.py
├── tests/
│   ├── conftest.py
│   ├── test_brownian_motion.py
│   ├── test_option_pricing.py
│   └── test_package_imports.py
├── AUTHORS.md
├── CHANGELOG.md
├── CITATION.cff
├── LICENSE
├── README.md
├── REPRODUCIBILITY.md
├── pyproject.toml
└── requirements.txt
```

---

## Main Components

| File or Folder | Purpose |
|---|---|
| `src/asr/models/bachelier/` | Installable Python package implementation |
| `src/asr/models/bachelier/process.py` | Bachelier arithmetic Brownian motion simulation and path analysis |
| `src/asr/models/bachelier/pricing.py` | Bachelier option pricing, Monte Carlo validation, and Black-Scholes comparison |
| `src/asr/models/bachelier/simulation.py` | High-level reproducibility and figure-generation utilities |
| `src/brownian_motion.py` | Script reproduction for Brownian motion experiment |
| `src/option_pricing.py` | Script reproduction for option pricing experiment |
| `tests/` | Automated tests for the package and scripts |
| `notebooks/` | Interactive Jupyter reproduction notebook |
| `figures/` | Generated figures |
| `paper/` | LaTeX working paper source |
| `pyproject.toml` | Python package configuration |
| `CITATION.cff` | Citation metadata |
| `REPRODUCIBILITY.md` | Reproducibility instructions |
| `LICENSE` | MIT open-source license |

---

## Installation

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

Alternative simple dependency installation:

```bash
pip install -r requirements.txt
```

After installation, verify the ASR import:

```bash
python - <<'PY'
from asr.models import bachelier

print("ASR Bachelier version:", bachelier.__version__)

price = bachelier.call_price(
    initial_price=100.0,
    strike=100.0,
    volatility=2.0,
    maturity=1.0,
)

print("Bachelier ATM call price:", price)
PY
```

---

## Installation from PyPI

The package can be installed with:

```bash
pip install asr-theory-of-speculation
```

Then imported with:

```python
from asr.models import bachelier
```

The ASR ecosystem registry package can be installed separately with:

```bash
pip install asr-open-sc
```

Then used with:

```python
import asr.open_sc as asr_sc

asr_sc.print_ecosystem()
```

---

## Use Without Installation

The reproduction scripts can be run directly from the repository root:

```bash
python src/brownian_motion.py
python src/option_pricing.py
```

For direct Python usage without installing the package, add `src/` to `PYTHONPATH`.

On macOS or Linux:

```bash
PYTHONPATH=src python -c "from asr.models import bachelier; print(bachelier.call_price(100, 100, 2, 1))"
```

On Windows PowerShell:

```powershell
$env:PYTHONPATH="src"
python -c "from asr.models import bachelier; print(bachelier.call_price(100, 100, 2, 1))"
```

For a clean and persistent research environment, the editable installation method remains preferred:

```bash
pip install -e ".[dev]"
```

---

## Quick Start

Compute a Bachelier call option price:

```python
from asr.models import bachelier

price = bachelier.call_price(
    initial_price=100.0,
    strike=100.0,
    volatility=2.0,
    maturity=1.0,
)

print(price)
```

Simulate Bachelier paths:

```python
from asr.models import bachelier

time_grid, paths = bachelier.simulate_paths(
    initial_price=100.0,
    volatility=2.0,
    maturity=1.0,
    n_steps=250,
    n_paths=5_000,
    seed=42,
)

analysis = bachelier.analyze_paths(
    time_grid=time_grid,
    paths=paths,
    initial_price=100.0,
    volatility=2.0,
)

print(analysis.terminal_mean)
print(analysis.terminal_empirical_variance)
print(analysis.terminal_theoretical_variance)
```

Run the high-level experiments:

```python
from asr.models import bachelier

time_grid, paths, analysis = bachelier.run_brownian_motion_experiment()

results = bachelier.run_option_pricing_experiment()

print(results)
```

---

## Script-Based Reproduction

Run the arithmetic Brownian motion experiment:

```bash
python src/brownian_motion.py
```

Run the option pricing experiment:

```bash
python src/option_pricing.py
```

Generated figures are saved in:

```text
figures/
```

---

## Interactive Notebook

An interactive Jupyter notebook is available in:

```text
notebooks/bachelier_theory_of_speculation_reproduction.ipynb
```

The notebook reproduces the main numerical experiments:

- Bachelier arithmetic Brownian motion;
- martingale and variance-scaling checks;
- Bachelier European call pricing;
- Monte Carlo validation;
- at-the-money square-root-of-time scaling;
- local comparison with Black-Scholes.

To run it:

```bash
jupyter notebook notebooks/bachelier_theory_of_speculation_reproduction.ipynb
```

The notebook is intended as an educational and exploratory companion. The tested, reusable implementation remains in the package under:

```text
src/asr/models/bachelier/
```

---

## Running Tests

Run the full test suite with:

```bash
pytest -q
```

The tests check:

- package import interface;
- simulation dimensions;
- reproducibility under fixed random seeds;
- martingale behaviour;
- theoretical variance scaling;
- Bachelier option pricing formula;
- Monte Carlo validation;
- Black-Scholes benchmark behaviour;
- invalid input handling;
- high-level experiment functions.

---

## Continuous Integration

This repository uses GitHub Actions to validate the project automatically.

The CI workflow checks that:

- the package installs with `pip install -e ".[dev]"`;
- the public import works with `from asr.models import bachelier`;
- the test suite passes;
- the Brownian motion script runs successfully;
- the option pricing script runs successfully;
- expected figures are generated.

Workflow file:

```text
.github/workflows/python-ci.yml
```

---

## Generated Figures

The project generates two main figures:

| Figure | Description |
|---|---|
| `figures/fig1_random_walk_martingale.png` | Simulated Bachelier paths and variance growth |
| `figures/fig2_option_pricing.png` | Bachelier option pricing and comparison with Black-Scholes |

The figures are generated by:

```bash
python src/brownian_motion.py
python src/option_pricing.py
```

---

## Working Paper

The LaTeX source of the accompanying working paper is available in:

```text
paper/main.tex
```

The paper provides a scientific reconstruction of Bachelier's theory with:

- literature review;
- historical source and scope of reproduction;
- mathematical derivations;
- computational methodology;
- numerical results;
- discussion and limitations;
- reproducibility statement;
- code and data availability;
- references and appendices.

To compile the paper from the `paper/` directory:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

---

## ASR Open-Science Ecosystem

This repository is designed to work as one module within the Alpha Stochastic Research open-science Python ecosystem.

The shared namespace strategy is:

```text
asr
├── open_sc
├── models
│   └── bachelier
├── risk
│   └── tail
├── portfolio
│   ├── optimization
│   └── hrp
├── ml
│   └── deep_hedging
└── agents
    └── trading
```

This repository provides:

```python
from asr.models import bachelier
```

The ecosystem registry is provided by:

```bash
pip install asr-open-sc
```

and can be used with:

```python
import asr.open_sc as asr_sc

asr_sc.print_ecosystem()
```

The ASR ecosystem is modular. Each research repository remains independently installable while sharing the same Python namespace.

---

## Reproducibility

This project is designed as a reproducible research repository.

Reproducibility principles:

- installable Python package;
- public import interface;
- shared ASR namespace compatibility;
- fixed random seeds;
- explicit dependencies;
- clean source code;
- documented numerical experiments;
- automated tests;
- generated figures saved from scripts;
- notebook-based interactive reproduction;
- citation metadata included.

For full details, see:

```text
REPRODUCIBILITY.md
```

---

## Citation

If you use this repository in your research, teaching, or open-source work, please cite it using the metadata provided in:

```text
CITATION.cff
```

Suggested citation:

```text
Alpha Kabinet TOURE and Alpha Stochastic Research.
Bachelier (1900): Theory of Speculation — ASR-Compatible Reproducible Python Package.
Alpha Stochastic Research, 2026.
https://github.com/Alpha-Stochastic-Research/asr-theory-of-speculation
```

---

## Open Source

This repository is released under the MIT License.

You are free to use, modify, and distribute the code under the terms of the license.

See:

```text
LICENSE
```

---

## Authors

Primary author:

```text
Alpha Kabinet TOURE
Founder and CEO, Alpha Stochastic Research
```

Institution:

```text
Alpha Stochastic Research
Independent Quantitative Finance Research Laboratory
```

For details, see:

```text
AUTHORS.md
```

---

## References

**Bachelier, L. (1900).**  
*Théorie de la Spéculation.*  
Annales Scientifiques de l'École Normale Supérieure, 17, 21–86.

**Samuelson, P. A. (1965).**  
*Rational Theory of Warrant Pricing.*  
Industrial Management Review, 6(2), 13–31.

**Black, F. and Scholes, M. (1973).**  
*The Pricing of Options and Corporate Liabilities.*  
Journal of Political Economy, 81(3), 637–654.

**Merton, R. C. (1973).**  
*Theory of Rational Option Pricing.*  
The Bell Journal of Economics and Management Science, 4(1), 141–183.

---

## About Alpha Stochastic Research

**Alpha Stochastic Research (ASR)** is an independent quantitative finance research laboratory dedicated to rigorous, transparent, and reproducible research.

ASR works at the intersection of:

- quantitative finance;
- financial mathematics;
- stochastic modelling;
- risk management;
- portfolio optimization;
- scientific computing;
- financial machine learning;
- open science;
- reproducible research.

Website:

```text
https://asr-lab.online
```

GitHub organization:

```text
https://github.com/Alpha-Stochastic-Research
```

Research contact:

```text
research@asr-lab.online
```

---

<div align="center">

**Alpha Stochastic Research**  
*Research → Modelling → Analysis → Impact*

<br>

© 2026 Alpha Stochastic Research

</div>
