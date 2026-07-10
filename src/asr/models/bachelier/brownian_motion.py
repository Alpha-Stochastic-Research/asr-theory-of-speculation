"""
Script reproduction for the Bachelier arithmetic Brownian motion experiment.

This script is intentionally thin. The reusable implementation lives in:

    asr.models.bachelier

Run from the repository root with:

    python src/brownian_motion.py
"""

from __future__ import annotations

from pathlib import Path

from asr.models import bachelier


FIGURE_PATH = Path("figures/fig1_random_walk_martingale.png")


def main() -> None:
    """
    Run the Bachelier Brownian motion experiment and save the figure.
    """

    time_grid, paths, analysis = bachelier.run_brownian_motion_experiment(
        initial_price=100.0,
        volatility=2.0,
        maturity=1.0,
        n_steps=250,
        n_paths=5_000,
        seed=42,
    )

    saved_path = bachelier.save_brownian_motion_figure(
        time_grid=time_grid,
        paths=paths,
        analysis=analysis,
        output_path=FIGURE_PATH,
    )

    print("Bachelier arithmetic Brownian motion experiment")
    print("-" * 55)
    print(f"Initial price: {paths[0, 0]:.4f}")
    print(f"Terminal empirical mean: {analysis.terminal_mean:.6f}")
    print(f"Terminal empirical variance: {analysis.terminal_empirical_variance:.6f}")
    print(f"Terminal theoretical variance: {analysis.terminal_theoretical_variance:.6f}")
    print(f"Maximum mean deviation from initial price: {analysis.max_mean_deviation:.6f}")
    print(f"Figure saved to: {saved_path}")


if __name__ == "__main__":
    main()
