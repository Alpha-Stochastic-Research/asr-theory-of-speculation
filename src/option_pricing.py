"""
Script reproduction for the Bachelier option pricing experiment.

This script is intentionally thin. The reusable implementation lives in:

    asr.models.bachelier

Run from the repository root with:

    python src/option_pricing.py
"""

from __future__ import annotations

from pathlib import Path

from asr.models import bachelier


FIGURE_PATH = Path("figures/fig2_option_pricing.png")


def main() -> None:
    """
    Run the Bachelier option pricing experiment and save the figure.
    """

    results = bachelier.run_option_pricing_experiment(
        initial_price=100.0,
        strike=100.0,
        volatility=2.0,
        maturity=1.0,
        n_paths=500_000,
        seed=7,
    )

    saved_path = bachelier.save_option_pricing_figure(
        output_path=FIGURE_PATH,
        initial_price=100.0,
        bachelier_volatility=2.0,
        black_scholes_volatility=0.02,
        maturity=1.0,
    )

    print("Bachelier option pricing experiment")
    print("-" * 45)
    print(f"Closed-form price: {results['closed_form_price']:.6f}")
    print(f"Monte Carlo price: {results['monte_carlo_price']:.6f}")
    print(f"Monte Carlo standard error: {results['monte_carlo_standard_error']:.6f}")
    print(f"Absolute difference: {results['absolute_difference']:.6f}")
    print(f"Figure saved to: {saved_path}")


if __name__ == "__main__":
    main()
