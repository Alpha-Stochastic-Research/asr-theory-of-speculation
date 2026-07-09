<div align="center">

<img src="assets/logo.png" width="180">

# Bachelier (1900): *Theory of Speculation*

### Reproducible Research Project

**Alpha Stochastic Research (ASR)**  
*Independent Quantitative Finance Research Laboratory*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)](https://numpy.org/)
[![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=flat-square&logo=scipy&logoColor=white)](https://scipy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=flat-square)](https://matplotlib.org/)
[![LaTeX](https://img.shields.io/badge/LaTeX-008080?style=flat-square&logo=latex&logoColor=white)](https://www.latex-project.org/)
[![License](https://img.shields.io/badge/License-MIT-success?style=flat-square)](LICENSE)

[![Website](https://img.shields.io/badge/Website-asr--lab.online-00C3FF?style=flat-square)](https://asr-lab.online)
[![Research](https://img.shields.io/badge/Research-research@asr--lab.online-0A2540?style=flat-square&logo=gmail&logoColor=white)](mailto:research@asr-lab.online)

</div>

---

# Overview

This repository provides a **fully reproducible implementation** of Louis Bachelier's seminal 1900 doctoral thesis,

> **Théorie de la Spéculation**

widely recognized as the **foundation of modern quantitative finance**.

Developed by **Alpha Stochastic Research (ASR)**, this project reproduces the principal mathematical results of Bachelier's work using modern computational methods. It includes numerical simulations, theoretical verification, Python implementations, publication-quality figures, and a pdf edition of the original manuscript.

The objective is to preserve one of the most influential contributions to financial mathematics while promoting **open science**, **reproducible research**, and **quantitative education**.

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
├── .github/
│   ├── workflows/
│       ├── python-app.yml
│
├── figures/
│   ├── fig1_random_walk_martingale.png
│   └── fig2_option_pricing.png
│
├── paper/
│   └── bachelier_paper.pdf
│
└── assets/
    └── logo.png
```

---

# Main Features

- Reproduction of Bachelier's Arithmetic Brownian Motion
- Verification of the Martingale Property
- Closed-Form European Option Pricing
- Monte Carlo Validation
- Numerical Experiments
- Publication-Quality Figures
- Fully Reproducible Research

---

# Numerical Results

## Arithmetic Brownian Motion

The repository reproduces Bachelier's arithmetic stochastic process

```math
P_t = P_0 + \sigma W_t
```

using **5,000 Monte Carlo trajectories**.

### Validation

| Property | Result |
|-----------|--------|
| Martingale Property | Verified |
| Maximum Mean Error | **0.037** |
| Variance Scaling Error | **1.56 %** |
| Negative Prices | Theoretically possible (not observed in simulation) |

---

## European Option Pricing

Implementation of Bachelier's closed-form pricing formula

```math
C=(P_0-K)\Phi(d)+\sigma\sqrt{T}\,\phi(d)
```

where

```math
d=\frac{P_0-K}{\sigma\sqrt{T}}
```

### Validation

| Test | Result |
|------|--------|
| Closed-form vs Monte Carlo (2M paths) | Error = **0.0008** |
| ATM √T Scaling | Exact |
| Comparison with Black–Scholes | Maximum Difference = **0.0048** |

---

# Installation

Clone the repository

```bash
git clone [https://github.com/Alpha-Stochastic-Research/asr-bachelier-1900.git](https://github.com/Alpha-Stochastic-Research/asr-theory-of-speculation.git)

cd asr-theory-of-speculation
```

Install the required packages

```bash
pip install -r requirements.txt
```

---

# Usage

Run the numerical experiments

```bash
python src/brownian_motion.py

python src/option_pricing.py
```

Generated figures are automatically saved in

```text
figures/
```

---

# Included Paper

The repository includes

- PDF
- Improved formatting
- Reproducible mathematical derivations

located in

```text
paper/
```

---

# Objectives

This project aims to

- reproduce one of the founding works of quantitative finance;
- validate the original mathematical results;
- provide educational Python implementations;
- promote reproducible computational finance;
- preserve the historical foundations of stochastic modelling.

---

# References

**Louis Bachelier (1900)**

*Théorie de la Spéculation.*

*Annales Scientifiques de l'École Normale Supérieure*, **17**, 21–86.

---

**Paul A. Samuelson (1965)**

*Rational Theory of Warrant Pricing.*

*Industrial Management Review*, **6(2)**, 13–31.

---

# About Alpha Stochastic Research

**Alpha Stochastic Research (ASR)** is an independent quantitative finance research laboratory dedicated to advancing rigorous, transparent, and reproducible research at the intersection of

- Financial Markets
- Mathematics
- Statistics
- Stochastic Modelling
- Artificial Intelligence

Our mission is to bridge academic research and real-world finance through open science, reproducible computational methods, and high-quality educational resources.

---

<div align="center">

### Alpha Stochastic Research

**Website**

https://asr-lab.online

**Research Contact**

research@asr-lab.online

---

© 2026 Alpha Stochastic Research (ASR)

</div>
