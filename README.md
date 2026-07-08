<div align="center">

<img src="assets/logo/logo.png" width="170">

# Bachelier (1900): *Theory of Speculation*

### A Reproducible Implementation of the Foundations of Quantitative Finance

**Alpha Stochastic Research (ASR)**  
*Independent Quantitative Finance Research Laboratory*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)](https://numpy.org/)
[![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=flat-square&logo=scipy&logoColor=white)](https://scipy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=flat-square)](https://matplotlib.org/)
[![LaTeX](https://img.shields.io/badge/LaTeX-008080?style=flat-square&logo=latex&logoColor=white)](https://www.latex-project.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-success?style=flat-square)](LICENSE)

[![Website](https://img.shields.io/badge/Website-asr--lab.online-00C3FF?style=flat-square)](https://asr-lab.online)
[![Email](https://img.shields.io/badge/Research-research@asr--lab.online-0A2540?style=flat-square&logo=gmail&logoColor=white)](mailto:research@asr-lab.online)

</div>

---

# Overview

This repository provides a **fully reproducible implementation** of Louis Bachelier's pioneering 1900 doctoral thesis, *Théorie de la Spéculation*, widely recognized as the birth of **modern quantitative finance**.

Developed by **Alpha Stochastic Research (ASR)**, this project bridges historical financial mathematics with modern computational methods through rigorous numerical experiments, mathematical derivations, Monte Carlo simulations, and reproducible Python implementations.

The repository also includes a corrected and fully compilable **LaTeX edition** of the original paper.

---

# Repository Structure

```text
bachelier-1900-reproduction/
│
├── README.md
├── LICENSE
├── requirements.txt
│
├── src/
│   ├── brownian_motion.py
│   └── option_pricing.py
│
├── figures/
│   ├── fig1_random_walk_martingale.png
│   └── fig2_option_pricing.png
│
├── paper/
│   ├── bachelier_paper_corrige.tex
│   └── bachelier_paper_corrige.pdf
│
└── assets/
    └── logo/
```

---

# Key Features

- Reproduction of Bachelier's Arithmetic Brownian Motion
- Martingale Property Verification
- Closed-Form Option Pricing Formula
- Monte Carlo Validation
- Numerical Experiments
- Publication-Quality Figures
- Corrected LaTeX Manuscript
- Fully Reproducible Research

---

# Numerical Validation

## Arithmetic Brownian Motion

The stochastic process

\[
P_t=P_0+\sigma W_t
\]

is reproduced numerically using Monte Carlo simulations.

Validation includes

- Martingale property
- Linear variance growth
- Distributional analysis
- Structural limitations of the arithmetic model

---

## Option Pricing

Implementation of Bachelier's European option pricing formula together with

- Closed-form evaluation
- Monte Carlo verification
- ATM asymptotic behaviour
- Comparison with Black–Scholes

---

# Installation

```bash
git clone https://github.com/Alpha-Stochastic-Research/asr-bachelier-1900.git

cd asr-bachelier-1900

pip install -r requirements.txt
```

---

# Usage

```bash
python src/brownian_motion.py

python src/option_pricing.py
```

---

# References

Bachelier, L. (1900).

*Théorie de la Spéculation.*

Annales Scientifiques de l'École Normale Supérieure, **17**, 21–86.

Samuelson, P. A. (1965).

*Rational Theory of Warrant Pricing.*

Industrial Management Review, **6(2)**, 13–31.

---

# About Alpha Stochastic Research

**Alpha Stochastic Research (ASR)** is an independent quantitative finance research laboratory dedicated to advancing rigorous, transparent, and reproducible research at the intersection of

- Financial Markets
- Mathematics
- Statistics
- Stochastic Modelling
- Artificial Intelligence

Our mission is to bridge academic research and real-world finance through **open science**, **reproducible computational methods**, and **high-quality educational resources**.

---

<div align="center">

**Website**

https://asr-lab.online

**Research Contact**

research@asr-lab.online

---

© 2026 Alpha Stochastic Research (ASR)

</div>
