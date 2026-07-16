"""Thin reconstruction entry point for the Bachelier process experiment."""

from __future__ import annotations

from pathlib import Path

from asr.models import bachelier


FIGURE_PATH = Path("figures/fig1_random_walk_martingale.png")


def main() -> None:
    """Run the reviewed Brownian-motion experiment from the public package API."""
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

    print("Bachelier arithmetic Brownian motion")
    print("-" * 45)
    print(f"Terminal empirical mean: {analysis.terminal_mean:.8f}")
    print(
        "Terminal empirical variance: "
        f"{analysis.terminal_empirical_variance:.8f}"
    )
    print(
        "Theoretical terminal variance: "
        f"{analysis.terminal_theoretical_variance:.8f}"
    )
    print(f"Maximum mean deviation: {analysis.max_mean_deviation:.8f}")
    print(f"Figure saved to: {saved_path}")


if __name__ == "__main__":
    main()
