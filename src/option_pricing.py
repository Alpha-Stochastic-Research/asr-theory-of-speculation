"""
Bachelier option pricing.

This script reproduces the option-pricing side of Louis Bachelier's
1900 Theory of Speculation using modern notation.

The script does four things:

1. Implements the closed-form Bachelier European call formula.
2. Validates the formula with Monte Carlo simulation.
3. Shows the square-root-of-time scaling of at-the-money call prices.
4. Compares Bachelier prices with Black-Scholes prices in a low-volatility regime.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


# -----------------------------------------------------------------------------
# Baseline parameters
# -----------------------------------------------------------------------------

P0 = 100.0
K = 100.0
SIGMA = 2.0
MATURITY = 1.0
N_PATHS = 500_000
SEED = 7


# -----------------------------------------------------------------------------
# Pricing functions
# -----------------------------------------------------------------------------


def bachelier_call_price(p0, strike, sigma, maturity):
    """
    Compute the Bachelier European call price.

    Parameters
    ----------
    p0 : float
        Initial price.
    strike : float
        Option strike.
    sigma : float
        Arithmetic volatility.
    maturity : float
        Time to maturity.

    Returns
    -------
    float
        Bachelier call option price.
    """

    if sigma < 0:
        raise ValueError("sigma must be non-negative.")

    if maturity < 0:
        raise ValueError("maturity must be non-negative.")

    if maturity == 0 or sigma == 0:
        return max(p0 - strike, 0.0)

    standard_deviation = sigma * np.sqrt(maturity)
    d = (p0 - strike) / standard_deviation

    price = (p0 - strike) * norm.cdf(d) + standard_deviation * norm.pdf(d)

    return float(price)


def bachelier_call_monte_carlo(
    p0,
    strike,
    sigma,
    maturity,
    n_paths=N_PATHS,
    seed=SEED,
):
    """
    Estimate the Bachelier call price by Monte Carlo simulation.

    Parameters
    ----------
    p0 : float
        Initial price.
    strike : float
        Option strike.
    sigma : float
        Arithmetic volatility.
    maturity : float
        Time to maturity.
    n_paths : int
        Number of Monte Carlo samples.
    seed : int
        Random seed used for reproducibility.

    Returns
    -------
    tuple[float, float]
        Monte Carlo price and estimated standard error.
    """

    if sigma < 0:
        raise ValueError("sigma must be non-negative.")

    if maturity < 0:
        raise ValueError("maturity must be non-negative.")

    if n_paths <= 0:
        raise ValueError("n_paths must be strictly positive.")

    if maturity == 0 or sigma == 0:
        return max(p0 - strike, 0.0), 0.0

    rng = np.random.default_rng(seed)

    terminal_prices = p0 + sigma * np.sqrt(maturity) * rng.standard_normal(n_paths)
    payoffs = np.maximum(terminal_prices - strike, 0.0)

    price = np.mean(payoffs)
    standard_error = np.std(payoffs, ddof=1) / np.sqrt(n_paths)

    return float(price), float(standard_error)


def black_scholes_call_price(spot, strike, volatility, maturity, rate=0.0):
    """
    Compute the Black-Scholes European call price.

    This function is included only as a comparison benchmark.

    Parameters
    ----------
    spot : float
        Initial spot price.
    strike : float
        Option strike.
    volatility : float
        Black-Scholes proportional volatility.
    maturity : float
        Time to maturity.
    rate : float
        Continuously compounded risk-free rate.

    Returns
    -------
    float
        Black-Scholes European call price.
    """

    if spot <= 0:
        raise ValueError("spot must be strictly positive.")

    if strike <= 0:
        raise ValueError("strike must be strictly positive.")

    if volatility < 0:
        raise ValueError("volatility must be non-negative.")

    if maturity < 0:
        raise ValueError("maturity must be non-negative.")

    if maturity == 0 or volatility == 0:
        return max(spot - strike, 0.0)

    standard_deviation = volatility * np.sqrt(maturity)

    d1 = (
        np.log(spot / strike)
        + (rate + 0.5 * volatility**2) * maturity
    ) / standard_deviation
    d2 = d1 - standard_deviation

    price = spot * norm.cdf(d1) - strike * np.exp(-rate * maturity) * norm.cdf(d2)

    return float(price)


# -----------------------------------------------------------------------------
# Numerical experiments
# -----------------------------------------------------------------------------


def compute_atm_scaling(p0=P0, sigma=SIGMA):
    """
    Compute Bachelier at-the-money call prices for different maturities.

    Returns
    -------
    tuple[np.ndarray, np.ndarray, np.ndarray]
        Maturity grid, Bachelier prices, and theoretical ATM expression.
    """

    maturity_grid = np.linspace(0.05, 2.0, 50)

    atm_prices = np.array(
        [
            bachelier_call_price(
                p0=p0,
                strike=p0,
                sigma=sigma,
                maturity=maturity,
            )
            for maturity in maturity_grid
        ]
    )

    theoretical_atm_prices = sigma * np.sqrt(maturity_grid) * norm.pdf(0.0)

    return maturity_grid, atm_prices, theoretical_atm_prices


def compare_with_black_scholes(
    spot=100.0,
    black_scholes_volatility=0.02,
    maturity=1.0,
):
    """
    Compare Bachelier and Black-Scholes call prices.

    For a local comparison, the Bachelier arithmetic volatility is set to:

        sigma_bachelier = spot * black_scholes_volatility

    This makes the absolute volatility of both models comparable near the spot.
    """

    if spot <= 0:
        raise ValueError("spot must be strictly positive.")

    if black_scholes_volatility < 0:
        raise ValueError("black_scholes_volatility must be non-negative.")

    if maturity < 0:
        raise ValueError("maturity must be non-negative.")

    strike_grid = np.linspace(90.0, 110.0, 100)
    bachelier_sigma = spot * black_scholes_volatility

    bachelier_prices = np.array(
        [
            bachelier_call_price(
                p0=spot,
                strike=strike,
                sigma=bachelier_sigma,
                maturity=maturity,
            )
            for strike in strike_grid
        ]
    )

    black_scholes_prices = np.array(
        [
            black_scholes_call_price(
                spot=spot,
                strike=strike,
                volatility=black_scholes_volatility,
                maturity=maturity,
                rate=0.0,
            )
            for strike in strike_grid
        ]
    )

    return strike_grid, bachelier_prices, black_scholes_prices


# -----------------------------------------------------------------------------
# Figure generation
# -----------------------------------------------------------------------------


def save_figure(
    maturity_grid,
    atm_prices,
    theoretical_atm_prices,
    strike_grid,
    bachelier_prices,
    black_scholes_prices,
    output_path="figures/fig2_option_pricing.png",
):
    """
    Save the option-pricing figure used in the repository and paper.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left panel: at-the-money square-root-of-time scaling.
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
        label="sigma sqrt(T) phi(0)",
    )

    axes[0].set_title("ATM option value scaling")
    axes[0].set_xlabel("Maturity")
    axes[0].set_ylabel("Call price")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Right panel: Bachelier versus Black-Scholes comparison.
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


# -----------------------------------------------------------------------------
# Main script
# -----------------------------------------------------------------------------


def main():
    """
    Run the full option-pricing experiment.
    """

    closed_form_price = bachelier_call_price(
        p0=P0,
        strike=K,
        sigma=SIGMA,
        maturity=MATURITY,
    )

    monte_carlo_price, monte_carlo_standard_error = bachelier_call_monte_carlo(
        p0=P0,
        strike=K,
        sigma=SIGMA,
        maturity=MATURITY,
        n_paths=N_PATHS,
        seed=SEED,
    )

    maturity_grid, atm_prices, theoretical_atm_prices = compute_atm_scaling()
    strike_grid, bachelier_prices, black_scholes_prices = compare_with_black_scholes()

    print("Bachelier option pricing")
    print("------------------------")
    print(f"Initial price: {P0:.4f}")
    print(f"Strike: {K:.4f}")
    print(f"Arithmetic volatility: {SIGMA:.4f}")
    print(f"Maturity: {MATURITY:.4f}")
    print(f"Monte Carlo paths: {N_PATHS:,}")
    print()
    print("Closed-form versus Monte Carlo")
    print(f"Closed-form price: {closed_form_price:.8f}")
    print(f"Monte Carlo price: {monte_carlo_price:.8f}")
    print(f"Monte Carlo standard error: {monte_carlo_standard_error:.8f}")
    print(f"Absolute difference: {abs(closed_form_price - monte_carlo_price):.8f}")

    output_path = save_figure(
        maturity_grid=maturity_grid,
        atm_prices=atm_prices,
        theoretical_atm_prices=theoretical_atm_prices,
        strike_grid=strike_grid,
        bachelier_prices=bachelier_prices,
        black_scholes_prices=black_scholes_prices,
    )

    print()
    print(f"Figure saved to: {output_path}")


if __name__ == "__main__":
    main()
