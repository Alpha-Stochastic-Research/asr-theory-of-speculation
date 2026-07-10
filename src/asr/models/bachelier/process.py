"""
Bachelier arithmetic Brownian motion process.

This module implements the price process introduced by Louis Bachelier:

    P_t = P_0 + sigma W_t

where W_t is a standard Brownian motion.

The implementation is designed for reproducible research, numerical
experiments, and educational use.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class BachelierProcessConfig:
    """
    Configuration for a Bachelier arithmetic Brownian motion simulation.

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
    """

    initial_price: float = 100.0
    volatility: float = 2.0
    maturity: float = 1.0
    n_steps: int = 250
    n_paths: int = 5_000
    seed: int | None = 42


@dataclass(frozen=True)
class BachelierPathAnalysis:
    """
    Summary statistics for simulated Bachelier paths.

    Attributes
    ----------
    time_grid:
        Simulation time grid.
    mean_path:
        Empirical mean across simulated paths.
    empirical_variance:
        Empirical variance across simulated paths.
    theoretical_variance:
        Theoretical variance sigma^2 t.
    max_mean_deviation:
        Maximum absolute deviation of the empirical mean from the initial price.
    terminal_mean:
        Empirical mean at maturity.
    terminal_empirical_variance:
        Empirical variance at maturity.
    terminal_theoretical_variance:
        Theoretical variance at maturity.
    """

    time_grid: np.ndarray
    mean_path: np.ndarray
    empirical_variance: np.ndarray
    theoretical_variance: np.ndarray
    max_mean_deviation: float
    terminal_mean: float
    terminal_empirical_variance: float
    terminal_theoretical_variance: float


def _validate_simulation_inputs(
    initial_price: float,
    volatility: float,
    maturity: float,
    n_steps: int,
    n_paths: int,
) -> None:
    """
    Validate inputs for Bachelier path simulation.

    Raises
    ------
    ValueError
        If one or more inputs are outside the admissible range.
    """

    if not np.isfinite(initial_price):
        raise ValueError("initial_price must be finite.")

    if volatility < 0 or not np.isfinite(volatility):
        raise ValueError("volatility must be a finite non-negative number.")

    if maturity <= 0 or not np.isfinite(maturity):
        raise ValueError("maturity must be a finite positive number.")

    if n_steps <= 0:
        raise ValueError("n_steps must be a positive integer.")

    if n_paths <= 0:
        raise ValueError("n_paths must be a positive integer.")


def simulate_paths(
    initial_price: float = 100.0,
    volatility: float = 2.0,
    maturity: float = 1.0,
    n_steps: int = 250,
    n_paths: int = 5_000,
    seed: int | None = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Simulate paths of the Bachelier arithmetic Brownian motion.

    The process is defined by:

        P_t = P_0 + sigma W_t

    where W_t is a standard Brownian motion.

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
    tuple[np.ndarray, np.ndarray]
        A tuple `(time_grid, paths)` where:

        - `time_grid` has shape `(n_steps + 1,)`;
        - `paths` has shape `(n_paths, n_steps + 1)`.
    """

    _validate_simulation_inputs(
        initial_price=initial_price,
        volatility=volatility,
        maturity=maturity,
        n_steps=n_steps,
        n_paths=n_paths,
    )

    rng = np.random.default_rng(seed)

    dt = maturity / n_steps
    time_grid = np.linspace(0.0, maturity, n_steps + 1)

    brownian_increments = np.sqrt(dt) * rng.standard_normal(size=(n_paths, n_steps))
    brownian_paths = np.concatenate(
        [np.zeros((n_paths, 1)), np.cumsum(brownian_increments, axis=1)],
        axis=1,
    )

    price_paths = initial_price + volatility * brownian_paths

    return time_grid, price_paths


def simulate_from_config(
    config: BachelierProcessConfig,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Simulate Bachelier paths from a configuration object.

    Parameters
    ----------
    config:
        Bachelier process configuration.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Time grid and simulated price paths.
    """

    return simulate_paths(
        initial_price=config.initial_price,
        volatility=config.volatility,
        maturity=config.maturity,
        n_steps=config.n_steps,
        n_paths=config.n_paths,
        seed=config.seed,
    )


def analyze_paths(
    time_grid: np.ndarray,
    paths: np.ndarray,
    initial_price: float = 100.0,
    volatility: float = 2.0,
) -> BachelierPathAnalysis:
    """
    Analyze simulated Bachelier paths.

    This function computes the empirical mean path, empirical variance,
    and theoretical variance sigma^2 t.

    Parameters
    ----------
    time_grid:
        Simulation time grid.
    paths:
        Simulated paths with shape `(n_paths, n_steps + 1)`.
    initial_price:
        Initial price P_0.
    volatility:
        Arithmetic volatility sigma.

    Returns
    -------
    BachelierPathAnalysis
        Summary statistics for the simulated paths.
    """

    time_grid = np.asarray(time_grid, dtype=float)
    paths = np.asarray(paths, dtype=float)

    if time_grid.ndim != 1:
        raise ValueError("time_grid must be one-dimensional.")

    if paths.ndim != 2:
        raise ValueError("paths must be a two-dimensional array.")

    if paths.shape[1] != time_grid.shape[0]:
        raise ValueError("paths and time_grid have incompatible shapes.")

    if volatility < 0 or not np.isfinite(volatility):
        raise ValueError("volatility must be a finite non-negative number.")

    if not np.isfinite(initial_price):
        raise ValueError("initial_price must be finite.")

    mean_path = paths.mean(axis=0)
    empirical_variance = paths.var(axis=0, ddof=0)
    theoretical_variance = volatility**2 * time_grid

    max_mean_deviation = float(np.max(np.abs(mean_path - initial_price)))

    return BachelierPathAnalysis(
        time_grid=time_grid,
        mean_path=mean_path,
        empirical_variance=empirical_variance,
        theoretical_variance=theoretical_variance,
        max_mean_deviation=max_mean_deviation,
        terminal_mean=float(mean_path[-1]),
        terminal_empirical_variance=float(empirical_variance[-1]),
        terminal_theoretical_variance=float(theoretical_variance[-1]),
    )
