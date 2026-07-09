# Reproducibility

This document explains how to reproduce the numerical simulations, figures, and computational outputs of this repository.

## Project

**Bachelier (1900): Theory of Speculation — Reproducible Implementation**

Maintained by **Alpha Stochastic Research**.

---

## Objective

The objective of this repository is to provide a transparent and reproducible implementation of Louis Bachelier’s 1900 work on financial speculation.

The project aims to reproduce and explain:

- Arithmetic Brownian motion
- Bachelier-style price dynamics
- Option pricing under normal price dynamics
- Numerical simulations
- Generated figures
- Mathematical and computational interpretations

---

## Environment

The project is designed to run with Python.

Recommended setup:

```bash
python --version
pip install -r requirements.txt
```

For a clean local environment, use:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Repository Structure

Relevant folders:

```text
src/        Python source code
figures/    Generated figures
paper/      Manuscript or reference material
assets/     Visual assets
```

---

## Reproducing the Simulations

Run the arithmetic Brownian motion simulation:

```bash
python src/brownian_motion.py
```

Run the Bachelier option pricing script:

```bash
python src/option_pricing.py
```

Generated figures should be saved in:

```text
figures/
```

---

## Randomness and Numerical Results

Some results may depend on random simulation paths.

For reproducibility, scripts should use fixed random seeds whenever simulations are involved.

Recommended practice:

```python
import numpy as np

rng = np.random.default_rng(seed=42)
```

---

## Expected Outputs

The repository should reproduce:

- Sample paths of arithmetic Brownian motion
- Variance scaling over time
- Distributional behaviour of normally distributed price changes
- Bachelier option pricing values
- Monte Carlo comparison results
- Publication-quality figures

---

## Numerical Validation

Numerical results should be checked against theoretical expectations when possible.

Examples:

- Simulated mean approximately consistent with the theoretical expectation
- Variance proportional to time
- Closed-form Bachelier prices close to Monte Carlo estimates
- Stable results under repeated simulations with fixed seeds
- Figures reproducible from scripts

---

## Reproducibility Principles

This project follows the following principles:

- Code should run from a clean clone.
- Dependencies should be listed in `requirements.txt`.
- Random seeds should be fixed when simulations are used.
- Figures should be generated from scripts.
- Mathematical assumptions should be documented.
- Numerical tolerances should be stated when relevant.
- Results should be traceable to code and theory.

---

## Contact

For reproducibility questions, contact:

**research@asr-lab.online**
