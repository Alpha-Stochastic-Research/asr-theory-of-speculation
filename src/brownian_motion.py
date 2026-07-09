"""
Bachelier (1900) arithmetic Brownian motion simulation.

In "Théorie de la Spéculation", Louis Bachelier models price changes using
an arithmetic Brownian motion:

    P_t = P_0 + sigma W_t

where:
    P_0   is the initial price,
    sigma is the arithmetic volatility,
    W_t   is a standard Brownian motion.

This script numerically illustrates two core properties:

1. Martingale property:
       E[P_t] = P_0

2. Linear variance growth:
       Var[P_t] = sigma^2 t

The goal is to keep the code simple, readable, educational, and reproducible.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# =============================================================================
# Main simulation parameters
# =============================================================================

P0 = 100.0
SIGMA = 2.0
MATURITY = 1.0
N_STEPS = 250
N_PATHS = 5_000
SEED = 42


# =============================================================================
# Simulation functions
# =============================================================================

def simulate_bachelier_paths(
    p0=P0,
    sigma=SIGMA,
    maturity=MATURITY,
    n_steps=N_STEPS,
    n_paths=N_PATHS,
    seed=SEED,
):
    """
    Simulate price paths under the Bachelier arithmetic Brownian motion model.

    The model is:

        P_t = P_0 + sigma W_t

    Over a small time interval dt, price increments satisfy:

        dP_t ~ N(0, sigma^2 dt)

    Parameters
    ----------
    p0 : float
        Initial price.
    sigma : float
        Arithmetic volatility.
    maturity : float
        Time horizon.
    n_steps : int
        Number of time steps.
    n_paths : int
        Number of simulated Monte Carlo paths.
    seed : int
        Random seed used for reproducibility.

    Returns
    -------
    t_grid : np.ndarray
        Time grid.
    paths : np.ndarray
        Simulated price paths with shape (n_paths, n_steps + 1).
    """

    if sigma < 0:
        raise ValueError("sigma must be non-negative.")

    if maturity <= 0:
        raise ValueError("maturity must be strictly positive.")

    if n_steps <= 0:
        raise ValueError("n_steps must be strictly positive.")

    if n_paths <= 0:
        raise ValueError("n_paths must be strictly positive.")

    rng = np.random.default_rng(seed)

    dt = maturity / n_steps
    t_grid = np.linspace(0.0, maturity, n_steps + 1)

    # Independent Gaussian increments:
    # dP_t = sigma * sqrt(dt) * Z, where Z ~ N(0, 1).
    increments = rng.normal(
        loc=0.0,
        scale=sigma * np.sqrt(dt),
        size=(n_paths, n_steps),
    )

    # Build the price paths by cumulatively summing the increments.
    paths = np.zeros((n_paths, n_steps + 1))
    paths[:, 0] = p0
    paths[:, 1:] = p0 + np.cumsum(increments, axis=1)

    return t_grid, paths


def analyze_bachelier_paths(t_grid, paths, p0=P0, sigma=SIGMA):
    """
    Compute the main empirical quantities of the simulation.

    This function checks the numerical behaviour of:

        E[P_t] ≈ P_0
        Var[P_t] ≈ sigma^2 t

    Parameters
    ----------
    t_grid : np.ndarray
        Time grid.
    paths : np.ndarray
        Simulated price paths.
    p0 : float
        Initial price.
    sigma : float
        Arithmetic volatility.

    Returns
    -------
    mean_path : np.ndarray
        Empirical mean of the simulated process.
    empirical_variance : np.ndarray
        Empirical variance of the simulated process.
    theoretical_variance : np.ndarray
        Theoretical variance sigma^2 t.
    """

    mean_path = paths.mean(axis=0)
    empirical_variance = paths.var(axis=0)
    theoretical_variance = sigma**2 * t_grid

    return mean_path, empirical_variance, theoretical_variance


def save_figure(
    t_grid,
    paths,
    mean_path,
    empirical_variance,
    theoretical_variance,
    p0=P0,
    sigma=SIGMA,
    output_path="figures/fig1_random_walk_martingale.png",
):
    """
    Save the main figure of the simulation.

    The figure contains:

    1. Simulated Bachelier price paths.
    2. A comparison between empirical variance and theoretical variance.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    # -------------------------------------------------------------------------
    # Panel 1: simulated price paths
    # -------------------------------------------------------------------------

    ax = axes[0]

    for i in range(min(60, paths.shape[0])):
        ax.plot(t_grid, paths[i], lw=0.6, alpha=0.5)

    ax.plot(
        t_grid,
        mean_path,
        color="black",
        lw=2,
        label=r"Empirical $E[P_t]$",
    )

    ax.axhline(
        p0,
        color="red",
        ls="--",
        lw=1,
        label=r"$P_0$",
    )

    ax.plot(
        t_grid,
        p0 + sigma * np.sqrt(t_grid),
        color="blue",
        ls=":",
        lw=1.5,
        label=r"$P_0 \pm \sigma\sqrt{t}$",
    )

    ax.plot(
        t_grid,
        p0 - sigma * np.sqrt(t_grid),
        color="blue",
        ls=":",
        lw=1.5,
    )

    ax.set_xlabel("Time")
    ax.set_ylabel(r"$P_t$")
    ax.set_title(
        "Arithmetic Brownian Motion — Bachelier (1900)\n"
        "Simulated Price Paths"
    )
    ax.legend(fontsize=8)

    # -------------------------------------------------------------------------
    # Panel 2: empirical variance versus theoretical variance
    # -------------------------------------------------------------------------

    ax = axes[1]

    ax.plot(
        t_grid,
        empirical_variance,
        lw=2,
        label="Empirical variance",
    )

    ax.plot(
        t_grid,
        theoretical_variance,
        "--",
        lw=2,
        label=r"Theoretical variance $\sigma^2 t$",
    )

    ax.set_xlabel("Time")
    ax.set_ylabel(r"$\mathrm{Var}[P_t]$")
    ax.set_title(
        "Linear Growth of Variance\n"
        r"Standard Deviation Scales as $\sqrt{t}$"
    )
    ax.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()

    return output_path


# =============================================================================
# Main experiment
# =============================================================================

def main():
    """
    Run the full numerical experiment.
    """

    t_grid, paths = simulate_bachelier_paths()

    mean_path, empirical_variance, theoretical_variance = analyze_bachelier_paths(
        t_grid=t_grid,
        paths=paths,
    )

    max_mean_deviation = np.max(np.abs(mean_path - P0))

    relative_final_variance_error = (
        abs(empirical_variance[-1] - theoretical_variance[-1])
        / theoretical_variance[-1]
    )

    empirical_final_std = np.std(paths[:, -1])
    theoretical_final_std = SIGMA * np.sqrt(MATURITY)

    negative_price_probability = np.mean(paths[:, -1] < 0)

    print("=== Bachelier (1900) Arithmetic Brownian Motion ===")
    print()
    print("Martingale property:")
    print(f"Maximum deviation between empirical E[P_t] and P0: {max_mean_deviation:.4f}")
    print()
    print("Variance growth:")
    print(f"Theoretical variance at maturity: {theoretical_variance[-1]:.4f}")
    print(f"Empirical variance at maturity: {empirical_variance[-1]:.4f}")
    print(f"Relative error: {relative_final_variance_error * 100:.2f}%")
    print()
    print("Final standard deviation:")
    print(f"Theoretical standard deviation: {theoretical_final_std:.4f}")
    print(f"Empirical standard deviation: {empirical_final_std:.4f}")
    print()
    print("Structural limitation of the arithmetic model:")
    print(
        "Proportion of terminal prices below zero: "
        f"{negative_price_probability * 100:.3f}%"
    )
    print(
        "This limitation was later addressed by positive-price models, "
        "especially geometric Brownian motion."
    )

    figure_path = save_figure(
        t_grid=t_grid,
        paths=paths,
        mean_path=mean_path,
        empirical_variance=empirical_variance,
        theoretical_variance=theoretical_variance,
    )

    print()
    print(f"Figure saved to: {figure_path}")


if __name__ == "__main__":
    main()
