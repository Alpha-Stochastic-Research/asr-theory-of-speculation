"""Reviewed option-pricing reconstruction and three-panel figure generator."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from asr.models import bachelier


FIGURE_PATH = Path("figures/fig2_option_pricing_revised.png")


def save_revised_figure(output_path: Path = FIGURE_PATH) -> Path:
    """Generate ATM scaling, local price comparison, and pricing difference."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    spot = 100.0
    normal_volatility = 2.0
    black_scholes_volatility = 0.02
    maturity = 1.0

    maturity_grid = np.linspace(0.01, 2.0, 100)
    atm_prices = np.array(
        [
            bachelier.atm_call_price(
                volatility=normal_volatility,
                maturity=value,
            )
            for value in maturity_grid
        ]
    )
    theoretical_atm = normal_volatility * np.sqrt(maturity_grid) / np.sqrt(
        2.0 * np.pi
    )

    strikes, normal_prices, lognormal_prices = bachelier.compare_with_black_scholes(
        spot=spot,
        black_scholes_volatility=black_scholes_volatility,
        maturity=maturity,
        strike_min=80.0,
        strike_max=120.0,
        n_strikes=81,
    )
    price_difference = normal_prices - lognormal_prices

    fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))

    axes[0].plot(maturity_grid, atm_prices, linewidth=2.2, label="Bachelier ATM")
    axes[0].plot(
        maturity_grid,
        theoretical_atm,
        linestyle="--",
        linewidth=2.0,
        label="sqrt-time formula",
    )
    axes[0].set_title("ATM square-root-of-time scaling")
    axes[0].set_xlabel("Maturity")
    axes[0].set_ylabel("Call price")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(strikes, normal_prices, linewidth=2.2, label="Bachelier")
    axes[1].plot(
        strikes,
        lognormal_prices,
        linestyle="--",
        linewidth=2.0,
        label="Black-Scholes",
    )
    axes[1].set_title("Local normal-lognormal comparison")
    axes[1].set_xlabel("Strike")
    axes[1].set_ylabel("Call price")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(strikes, price_difference, linewidth=2.2)
    axes[2].axhline(0.0, linewidth=1.0)
    axes[2].set_title("Bachelier - Black-Scholes")
    axes[2].set_xlabel("Strike")
    axes[2].set_ylabel("Price difference")
    axes[2].grid(True, alpha=0.3)

    fig.suptitle("Bachelier option-pricing experiments", fontsize=14)
    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return output_path


def main() -> None:
    """Run the reviewed pricing experiment and save the revised figure."""
    results = bachelier.run_option_pricing_experiment(
        initial_price=100.0,
        strike=100.0,
        volatility=2.0,
        maturity=1.0,
        n_paths=500_000,
        seed=7,
    )

    saved_path = save_revised_figure()

    print("Bachelier option pricing experiment")
    print("-" * 45)
    print(f"Closed-form price: {results['closed_form_price']:.8f}")
    print(f"Monte Carlo price: {results['monte_carlo_price']:.8f}")
    print(
        "Monte Carlo standard error: "
        f"{results['monte_carlo_standard_error']:.8f}"
    )
    print(f"Absolute difference: {results['absolute_difference']:.8f}")
    print(f"Figure saved to: {saved_path}")


if __name__ == "__main__":
    main()
