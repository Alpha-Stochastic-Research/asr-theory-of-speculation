"""
Bachelier (1900) arithmetic Brownian motion simulation.

This module reproduces the core price process used in Louis Bachelier's
"Théorie de la Spéculation" (1900):

    P_t = P_0 + sigma W_t

where W_t is a standard Brownian motion.

The simulation illustrates two central properties:

1. Martingale property:
       E[P_t] = P_0

2. Linear variance growth:
       Var[P_t] = sigma^2 t

The code is written for reproducible research: functions are reusable,
parameters are explicit, random seeds are controlled, and figures are saved
from deterministic scripts.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


DEFAULT_FIGURE_PATH = Path("figures/fig1_random_walk_martingale.png")


@dataclass(frozen=True)
class BachelierSimulation:
    """
    Container for a Bachelier arithmetic Brownian motion simulation.

    Attributes
    ----------
    p0:
        Initial price.
    sigma:
        Arithmetic volatility parameter.
    maturity:
        Time horizon.
    t_grid:
        Time grid from 0 to maturity.
    paths:
        Simulated price paths. Shape: (n_paths, n_steps + 1).
    mean_path:
        Empirical mean of simulated paths at each time step.
    empirical_variance:
        Empirical variance of simulated paths at each time step.
    theoretical_variance:
        Theoretical variance sigma^2 * t.
    """

    p0: float
    sigma: float
    maturity: float
    t_grid: np.ndarray
    paths: np.ndarray
    mean_path: np.ndarray
    empirical_variance: np.ndarray
    theoretical_variance: np.ndarray

    @property
    def final_prices(self) -> np.ndarray:
        """Return simulated terminal prices."""
        return self.paths[:, -1]

    @property
    def max_mean_deviation(self) -> float:
        """Maximum absolute deviation between empirical mean and P_0."""
        return float(np.max(np.abs(self.mean_path - self.p0)))

    @property
    def relative_final_variance_error(self) -> float:
        """Relative error between empirical and theoretical variance at maturity."""
        theoretical_final_variance = self.theoretical_variance[-1]

        if theoretical_final_variance == 0:
            return 0.0

        return float(
            abs(self.empirical_variance[-1] - theoretical_final_variance)
            / theoretical_final_variance
        )

    @property
    def negative_terminal_price_probability(self) -> float:
        """
        Empirical probability that terminal prices are negative.

        This illustrates a known structural limitation of the arithmetic
        Brownian motion model: prices may become negative.
        """
        return float(np.mean(self.final_prices < 0.0))


def validate_simulation_inputs(
    p0: float,
    sigma: float,
    maturity: float,
    n_steps: int,
    n_paths: int,
) -> None:
    """
    Validate simulation inputs.

    Parameters
    ----------
    p0:
        Initial price.
    sigma:
        Arithmetic volatility. Must be non-negative.
    maturity:
        Time horizon. Must be strictly positive.
    n_steps:
        Number of time steps. Must be strictly positive.
    n_paths:
        Number of Monte Carlo paths. Must be strictly positive.
    """

    if not np.isfinite(p0):
        raise ValueError("p0 must be finite.")

    if sigma < 0 or not np.isfinite(sigma):
        raise ValueError("sigma must be a finite non-negative number.")

    if maturity <= 0 or not np.isfinite(maturity):
        raise ValueError("maturity must be a finite strictly positive number.")

    if n_steps <= 0:
        raise ValueError("n_steps must be strictly positive.")

    if n_paths <= 0:
        raise ValueError("n_paths must be strictly positive.")


def simulate_bachelier_paths(
    p0: float = 100.0,
    sigma: float = 2.0,
    maturity: float = 1.0,
    n_steps: int = 250,
    n_paths: int = 5_000,
    seed: int | None = 42,
) -> BachelierSimulation:
    """
    Simulate arithmetic Brownian motion paths under the Bachelier model.

    The process is:

        P_t = P_0 + sigma W_t

    with independent Gaussian increments:

        dP_t ~ N(0, sigma^2 dt)

    Parameters
    ----------
    p0:
        Initial price.
    sigma:
        Arithmetic volatility parameter.
    maturity:
        Final time horizon.
    n_steps:
        Number of discretization steps.
    n_paths:
        Number of simulated Monte Carlo paths.
    seed:
        Random seed used for reproducibility.

    Returns
    -------
    BachelierSimulation
        Simulation result containing paths, time grid, empirical mean and
        theoretical variance.
    """

    validate_simulation_inputs(
        p0=p0,
        sigma=sigma,
        maturity=maturity,
        n_steps=n_steps,
        n_paths=n_paths,
    )

    rng = np.random.default_rng(seed)

    dt = maturity / n_steps
    t_grid = np.linspace(0.0, maturity, n_steps + 1)

    increments = rng.normal(
        loc=0.0,
        scale=sigma * np.sqrt(dt),
        size=(n_paths, n_steps),
    )

    cumulative_increments = np.cumsum(increments, axis=1)

    paths = np.empty((n_paths, n_steps + 1), dtype=float)
    paths[:, 0] = p0
    paths[:, 1:] = p0 + cumulative_increments

    mean_path = paths.mean(axis=0)
    empirical_variance = paths.var(axis=0)
    theoretical_variance = sigma**2 * t_grid

    return BachelierSimulation(
        p0=p0,
        sigma=sigma,
        maturity=maturity,
        t_grid=t_grid,
        paths=paths,
        mean_path=mean_path,
        empirical_variance=empirical_variance,
        theoretical_variance=theoretical_variance,
    )


def save_bachelier_figure(
    simulation: BachelierSimulation,
    output_path: str | Path = DEFAULT_FIGURE_PATH,
    n_display_paths: int = 60,
    dpi: int = 160,
) -> Path:
    """
    Save a two-panel figure illustrating the Bachelier process.

    The first panel shows simulated paths, the empirical mean and the
    theoretical one-standard-deviation envelope.

    The second panel compares empirical variance with the theoretical
    variance sigma^2 t.

    Parameters
    ----------
    simulation:
        Simulation result returned by `simulate_bachelier_paths`.
    output_path:
        Path where the figure should be saved.
    n_display_paths:
        Number of simulated paths displayed in the first panel.
    dpi:
        Figure resolution.

    Returns
    -------
    pathlib.Path
        Path to the saved figure.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    n_display_paths = min(n_display_paths, simulation.paths.shape[0])

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    ax = axes[0]

    for i in range(n_display_paths):
        ax.plot(
            simulation.t_grid,
            simulation.paths[i],
            linewidth=0.6,
            alpha=0.5,
        )

    standard_deviation_envelope = simulation.sigma * np.sqrt(simulation.t_grid)

    ax.plot(
        simulation.t_grid,
        simulation.mean_path,
        color="black",
        linewidth=2,
        label=r"Empirical $E[P_t]$",
    )
    ax.axhline(
        simulation.p0,
        color="red",
        linestyle="--",
        linewidth=1,
        label=r"$P_0$",
    )
    ax.plot(
        simulation.t_grid,
        simulation.p0 + standard_deviation_envelope,
        color="blue",
        linestyle=":",
        linewidth=1.5,
        label=r"$P_0 \pm \sigma\sqrt{t}$",
    )
    ax.plot(
        simulation.t_grid,
        simulation.p0 - standard_deviation_envelope,
        color="blue",
        linestyle=":",
        linewidth=1.5,
    )

    ax.set_xlabel("Time")
    ax.set_ylabel(r"$P_t$")
    ax.set_title("Arithmetic Brownian Motion\nBachelier (1900)")
    ax.legend(fontsize=8)

    ax = axes[1]

    ax.plot(
        simulation.t_grid,
        simulation.empirical_variance,
        label="Empirical variance",
        linewidth=2,
    )
    ax.plot(
        simulation.t_grid,
        simulation.theoretical_variance,
        linestyle="--",
        label=r"Theoretical variance $\sigma^2 t$",
        linewidth=2,
    )

    ax.set_xlabel("Time")
    ax.set_ylabel(r"$\mathrm{Var}[P_t]$")
    ax.set_title("Linear Growth of Variance\nStandard Deviation Scales as √t")
    ax.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi)
    plt.close(fig)

    return output_path


def run_experiment() -> BachelierSimulation:
    """
    Run the default Bachelier simulation experiment and print diagnostics.

    Returns
    -------
    BachelierSimulation
        Simulation result, useful for interactive exploration.
    """

    simulation = simulate_bachelier_paths()

    figure_path = save_bachelier_figure(simulation)

    print("=== Bachelier (1900): Arithmetic Brownian Motion ===")
    print(f"Initial price P0: {simulation.p0:.4f}")
    print(f"Arithmetic volatility sigma: {simulation.sigma:.4f}")
    print(f"Maturity: {simulation.maturity:.4f}")
    print()
    print("Martingale property:")
    print(f"Maximum deviation between empirical E[P_t] and P0: {simulation.max_mean_deviation:.6f}")
    print()
    print("Variance scaling:")
    print(f"Theoretical variance at maturity: {simulation.theoretical_variance[-1]:.6f}")
    print(f"Empirical variance at maturity: {simulation.empirical_variance[-1]:.6f}")
    print(f"Relative final variance error: {simulation.relative_final_variance_error * 100:.2f}%")
    print()
    print("Structural limitation:")
    print(
        "Probability of negative terminal prices: "
        f"{simulation.negative_terminal_price_probability * 100:.4f}%"
    )
    print()
    print(f"Figure saved to: {figure_path}")

    return simulation


def main() -> None:
    """Command-line entry point."""
    run_experiment()


if __name__ == "__main__":
    main()
