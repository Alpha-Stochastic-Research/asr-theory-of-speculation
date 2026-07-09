"""
Bachelier arithmetic Brownian motion simulation.

This script reproduces the basic price dynamics behind Louis Bachelier's
1900 Theory of Speculation using a simple arithmetic Brownian motion model:

    P_t = P_0 + sigma W_t

The goal is educational and reproducible:

1. Simulate Bachelier price paths.
2. Verify the martingale property E[P_t] = P_0.
3. Verify the variance identity Var[P_t] = sigma^2 t.
4. Save a figure that can be used in the paper and README.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# -----------------------------------------------------------------------------
# Baseline parameters
# -----------------------------------------------------------------------------

P0 = 100.0
SIGMA = 2.0
MATURITY = 1.0
N_STEPS = 250
N_PATHS = 5_000
SEED = 42


# -----------------------------------------------------------------------------
# Simulation functions
# -----------------------------------------------------------------------------


def simulate_bachelier_paths(
    p0=P0,
    sigma=SIGMA,
    maturity=MATURITY,
    n_steps=N_STEPS,
    n_paths=N_PATHS,
    seed=SEED,
):
    """
    Simulate price paths under the Bachelier model.

    Parameters
    ----------
    p0 : float
        Initial price.
    sigma : float
        Arithmetic volatility.
    maturity : float
        Final time horizon.
    n_steps : int
        Number of time steps.
    n_paths : int
        Number of simulated paths.
    seed : int
        Random seed used for reproducibility.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        The time grid and the simulated price paths.
        The paths array has shape (n_paths, n_steps + 1).
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

    # Under the Bachelier model, price increments are Gaussian:
    #
    #     Delta P = sigma sqrt(dt) Z
    #
    # where Z is standard normal.
    increments = sigma * np.sqrt(dt) * rng.standard_normal(size=(n_paths, n_steps))

    paths = np.empty((n_paths, n_steps + 1))
    paths[:, 0] = p0
    paths[:, 1:] = p0 + np.cumsum(increments, axis=1)

    return t_grid, paths


def analyze_bachelier_paths(t_grid, paths, p0=P0, sigma=SIGMA):
    """
    Compute empirical and theoretical quantities for Bachelier paths.

    Parameters
    ----------
    t_grid : np.ndarray
        Time grid returned by the simulation.
    paths : np.ndarray
        Simulated price paths.
    p0 : float
        Initial price.
    sigma : float
        Arithmetic volatility.

    Returns
    -------
    tuple[np.ndarray, np.ndarray, np.ndarray]
        Empirical mean path, empirical variance path, and theoretical variance.
    """

    mean_path = np.mean(paths, axis=0)
    empirical_variance = np.var(paths, axis=0, ddof=0)
    theoretical_variance = sigma**2 * t_grid

    return mean_path, empirical_variance, theoretical_variance


# -----------------------------------------------------------------------------
# Figure generation
# -----------------------------------------------------------------------------


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
    Save the Brownian motion figure used in the repository and paper.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    standard_deviation = sigma * np.sqrt(t_grid)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left panel: sample paths and martingale check.
    for path in paths[:25]:
        axes[0].plot(t_grid, path, linewidth=0.8, alpha=0.35)

    axes[0].plot(t_grid, mean_path, linewidth=2.5, label="Empirical mean")
    axes[0].plot(
        t_grid,
        p0 + standard_deviation,
        linestyle="--",
        linewidth=1.5,
        label="P0 +/- one std. dev.",
    )
    axes[0].plot(t_grid, p0 - standard_deviation, linestyle="--", linewidth=1.5)

    axes[0].set_title("Bachelier price paths")
    axes[0].set_xlabel("Time")
    axes[0].set_ylabel("Price")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Right panel: variance scaling.
    axes[1].plot(t_grid, empirical_variance, linewidth=2.0, label="Empirical variance")
    axes[1].plot(
        t_grid,
        theoretical_variance,
        linestyle="--",
        linewidth=2.0,
        label="Theoretical variance",
    )

    axes[1].set_title("Variance scaling")
    axes[1].set_xlabel("Time")
    axes[1].set_ylabel("Variance")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    fig.suptitle("Bachelier arithmetic Brownian motion", fontsize=14)
    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    return output_path


# -----------------------------------------------------------------------------
# Main script
# -----------------------------------------------------------------------------


def main():
    """
    Run the full Brownian motion experiment.
    """

    t_grid, paths = simulate_bachelier_paths()
    mean_path, empirical_variance, theoretical_variance = analyze_bachelier_paths(
        t_grid,
        paths,
    )

    terminal_mean = mean_path[-1]
    terminal_variance = empirical_variance[-1]
    theoretical_terminal_variance = theoretical_variance[-1]
    max_mean_deviation = np.max(np.abs(mean_path - P0))

    print("Bachelier arithmetic Brownian motion")
    print("-------------------------------------")
    print(f"Initial price: {P0:.4f}")
    print(f"Arithmetic volatility: {SIGMA:.4f}")
    print(f"Maturity: {MATURITY:.4f}")
    print(f"Number of simulated paths: {N_PATHS:,}")
    print(f"Number of time steps: {N_STEPS:,}")
    print()
    print("Martingale check")
    print(f"Terminal empirical mean: {terminal_mean:.6f}")
    print(f"Maximum mean deviation from P0: {max_mean_deviation:.6f}")
    print()
    print("Variance check")
    print(f"Terminal empirical variance: {terminal_variance:.6f}")
    print(f"Theoretical terminal variance: {theoretical_terminal_variance:.6f}")

    output_path = save_figure(
        t_grid=t_grid,
        paths=paths,
        mean_path=mean_path,
        empirical_variance=empirical_variance,
        theoretical_variance=theoretical_variance,
    )

    print()
    print(f"Figure saved to: {output_path}")


if __name__ == "__main__":
    main()
