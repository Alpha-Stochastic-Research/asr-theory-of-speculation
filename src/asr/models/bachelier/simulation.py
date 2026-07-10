"""
Simulation and figure-generation utilities for the Bachelier model.

This module provides higher-level reproducibility functions used to generate
the numerical experiments and figures associated with the Bachelier research
package.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .pricing import (
    atm_call_price,
    call_monte_carlo_price,
    call_price,
    compare_with_black_scholes,
)
from .process import BachelierPathAnalysis, analyze_paths, simulate_paths


def run_brownian_motion_experiment(
    initial_price: float = 100.0,
    volatility: float = 2.0,
    maturity: float = 1.0,
    n_steps: int = 250,
    n_paths: int = 5_000,
    seed: int | None = 42,
) -> tuple[np.ndarray, np.ndarray, BachelierPathAnalysis]:
    """
    Run the Bachelier arithmetic Brownian motion experiment.

    Parameters
    ----------
    initial_price:
        Initial price P_0.
    volatility:
        Arithmetic volatility sigma.
    maturity:
        Time horizon T.
    n_steps:
        Number of time steps.
    n_paths:
        Number of simulated paths.
    seed:
        Optional random seed for reproducibility.

    Returns
    -------
    tuple[np.ndarray, np.ndarray, BachelierPathAnalysis]
        Time grid, simulated paths, and path analysis.
    """

    time_grid, paths = simulate_paths(
        initial_price=initial_price,
        volatility=volatility,
        maturity=maturity,
        n_steps=n_steps,
        n_paths=n_paths,
        seed=seed,
    )

    analysis = analyze_paths(
        time_grid=time_grid,
        paths=paths,
        initial_price=initial_price,
        volatility=volatility,
    )

    return time_grid, paths, analysis


def save_brownian_motion_figure(
    time_grid: np.ndarray,
    paths: np.ndarray,
    analysis: BachelierPathAnalysis,
    output_path: str | Path = "figures/fig1_random_walk_martingale.png",
    n_display_paths: int = 25,
) -> Path:
    """
    Save the Brownian motion simulation figure.

    The figure contains:

    - simulated Bachelier price paths;
    - empirical mean path;
    - one-standard-deviation bands;
    - empirical versus theoretical variance.

    Parameters
    ----------
    time_grid:
        Simulation time grid.
    paths:
        Simulated Bachelier paths.
    analysis:
        Summary statistics returned by `analyze_paths`.
    output_path:
        Path where the figure should be saved.
    n_display_paths:
        Number of simulated paths displayed in the path plot.

    Returns
    -------
    pathlib.Path
        Path to the saved figure.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    time_grid = np.asarray(time_grid, dtype=float)
    paths = np.asarray(paths, dtype=float)

    if paths.ndim != 2:
        raise ValueError("paths must be a two-dimensional array.")

    if time_grid.ndim != 1:
        raise ValueError("time_grid must be one-dimensional.")

    if paths.shape[1] != time_grid.shape[0]:
        raise ValueError("paths and time_grid have incompatible shapes.")

    display_count = min(n_display_paths, paths.shape[0])
    initial_price = float(paths[0, 0])
    standard_deviation = np.sqrt(analysis.theoretical_variance)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for path in paths[:display_count]:
        axes[0].plot(time_grid, path, linewidth=0.8, alpha=0.35)

    axes[0].plot(
        time_grid,
        analysis.mean_path,
        linewidth=2.5,
        label="Empirical mean",
    )

    axes[0].plot(
        time_grid,
        initial_price + standard_deviation,
        linestyle="--",
        linewidth=1.5,
        label="One standard deviation",
    )

    axes[0].plot(
        time_grid,
        initial_price - standard_deviation,
        linestyle="--",
        linewidth=1.5,
    )

    axes[0].set_title("Bachelier price paths")
    axes[0].set_xlabel("Time")
    axes[0].set_ylabel("Price")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(
        time_grid,
        analysis.empirical_variance,
        linewidth=2.0,
        label="Empirical variance",
    )

    axes[1].plot(
        time_grid,
        analysis.theoretical_variance,
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


def run_option_pricing_experiment(
    initial_price: float = 100.0,
    strike: float = 100.0,
    volatility: float = 2.0,
    maturity: float = 1.0,
    n_paths: int = 500_000,
    seed: int | None = 7,
) -> dict[str, float]:
    """
    Run the Bachelier option pricing experiment.

    Parameters
    ----------
    initial_price:
        Initial price P_0.
    strike:
        Strike price K.
    volatility:
        Arithmetic volatility sigma.
    maturity:
        Time to maturity T.
    n_paths:
        Number of Monte Carlo samples.
    seed:
        Optional random seed for reproducibility.

    Returns
    -------
    dict[str, float]
        Closed-form price, Monte Carlo estimate, standard error, and
        absolute pricing difference.
    """

    analytical_price = call_price(
        initial_price=initial_price,
        strike=strike,
        volatility=volatility,
        maturity=maturity,
    )

    monte_carlo_price, monte_carlo_standard_error = call_monte_carlo_price(
        initial_price=initial_price,
        strike=strike,
        volatility=volatility,
        maturity=maturity,
        n_paths=n_paths,
        seed=seed,
    )

    return {
        "closed_form_price": analytical_price,
        "monte_carlo_price": monte_carlo_price,
        "monte_carlo_standard_error": monte_carlo_standard_error,
        "absolute_difference": abs(analytical_price - monte_carlo_price),
    }


def save_option_pricing_figure(
    output_path: str | Path = "figures/fig2_option_pricing.png",
    initial_price: float = 100.0,
    bachelier_volatility: float = 2.0,
    black_scholes_volatility: float = 0.02,
    maturity: float = 1.0,
) -> Path:
    """
    Save the option pricing figure.

    The figure contains:

    - at-the-money Bachelier square-root-of-time scaling;
    - a local comparison between Bachelier and Black-Scholes call prices.

    Parameters
    ----------
    output_path:
        Path where the figure should be saved.
    initial_price:
        Initial price used for the at-the-money calculation.
    bachelier_volatility:
        Arithmetic Bachelier volatility.
    black_scholes_volatility:
        Proportional Black-Scholes volatility.
    maturity:
        Time to maturity for the strike comparison.

    Returns
    -------
    pathlib.Path
        Path to the saved figure.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    maturity_grid = np.linspace(0.01, 2.0, 100)
    atm_prices = np.array(
        [
            atm_call_price(
                volatility=bachelier_volatility,
                maturity=time_to_maturity,
            )
            for time_to_maturity in maturity_grid
        ]
    )

    theoretical_atm_prices = (
        bachelier_volatility * np.sqrt(maturity_grid) / np.sqrt(2.0 * np.pi)
    )

    strike_grid, bachelier_prices, black_scholes_prices = compare_with_black_scholes(
        spot=initial_price,
        black_scholes_volatility=black_scholes_volatility,
        maturity=maturity,
    )

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(
        maturity_grid,
        atm_prices,
        linewidth=2.2,
        label="Bachelier ATM price",
    )

    axes[0].plot(
        maturity_grid,
        theoretical_atm_prices,
        linestyle="--",
        linewidth=2.0,
        label="sqrt-time formula",
    )

    axes[0].set_title("ATM option value scaling")
    axes[0].set_xlabel("Maturity")
    axes[0].set_ylabel("Call price")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(
        strike_grid,
        bachelier_prices,
        linewidth=2.2,
        label="Bachelier",
    )

    axes[1].plot(
        strike_grid,
        black_scholes_prices,
        linestyle="--",
        linewidth=2.0,
        label="Black-Scholes",
    )

    axes[1].set_title("Bachelier vs Black-Scholes")
    axes[1].set_xlabel("Strike")
    axes[1].set_ylabel("Call price")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    fig.suptitle("Bachelier option pricing", fontsize=14)
    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    return output_path
