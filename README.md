<div align="center">

<img src="assets/logo.png" alt="Alpha Stochastic Research Logo" width="130">

# Bachelier (1900): Theory of Speculation

### Reproducible Reconstruction of the Origins of Quantitative Finance

**Alpha Stochastic Research**  
*Independent Quantitative Finance Research Laboratory*

<br>

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)](https://scipy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge)](https://matplotlib.org/)
[![Pytest](https://img.shields.io/badge/Pytest-Tested-0A2540?style=for-the-badge)](https://docs.pytest.org/)
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

This project reproduces and explains the core mathematical ideas using modern Python-based scientific computing.

The repository includes:

- arithmetic Brownian motion simulations;
- numerical verification of the martingale property;
- variance scaling analysis;
- Bachelier's European call option pricing formula;
- Monte Carlo validation;
- comparison with Black-Scholes under low relative volatility;
- reproducible figures;
- automated tests;
- LaTeX working paper source;
- citation metadata;
- open-source documentation.

---

## Research Objective

The objective of this project is to connect historical financial mathematics with modern reproducible research.

This repository aims to:

- preserve one of the foundational works of quantitative finance;
- provide readable Python implementations;
- make the numerical results reproducible;
- explain the mathematical structure behind Bachelier's model;
- support students, researchers, and practitioners interested in financial mathematics.

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
├── paper/
│   ├── main.tex
│   ├── references.bib
│   └── README.md
├── src/
│   ├── brownian_motion.py
│   └── option_pricing.py
├── tests/
│   ├── conftest.py
│   ├── test_brownian_motion.py
│   └── test_option_pricing.py
├── AUTHORS.md
├── CHANGELOG.md
├── CITATION.cff
├── LICENSE
├── README.md
├── REPRODUCIBILITY.md
└── requirements.txt
```

---

## Main Components

| File or Folder | Purpose |
|---|---|
| `src/brownian_motion.py` | Simulates Bachelier arithmetic Brownian motion and verifies martingale and variance properties |
| `src/option_pricing.py` | Implements Bachelier option pricing, Monte Carlo validation, and comparison with Black-Scholes |
| `tests/` | Contains automated tests for simulations and pricing formulas |
| `figures/` | Stores generated figures |
| `paper/` | Contains the LaTeX working paper source |
| `CITATION.cff` | Provides citation metadata |
| `REPRODUCIBILITY.md` | Explains how to reproduce the numerical results |
| `AUTHORS.md` | Lists authorship and institutional information |
| `CHANGELOG.md` | Tracks project changes |
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

Install the required dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Usage

Run the arithmetic Brownian motion simulation:

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

## Running Tests

Run the full test suite with:

```bash
pytest -q
```

The tests check:

- simulation dimensions;
- reproducibility under fixed random seeds;
- martingale behaviour;
- theoretical variance scaling;
- Bachelier option pricing formula;
- Monte Carlo validation;
- Black-Scholes benchmark behaviour;
- invalid input handling.

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

## Continuous Integration

This repository uses GitHub Actions to validate the project automatically.

The CI workflow checks that:

- dependencies install correctly;
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

---

## Reproducibility

This project is designed as a reproducible research repository.

Reproducibility principles:

- fixed random seeds;
- explicit dependencies;
- clear source code;
- documented numerical experiments;
- automated tests;
- generated figures saved from scripts;
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
Bachelier (1900): Theory of Speculation — Reproducible Implementation.
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
- scientific computing;
- financial machine learning;
- open science.

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
