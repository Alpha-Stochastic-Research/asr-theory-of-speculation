"""
Bachelier (1900) option pricing formula.

Under the arithmetic Brownian motion model:

    P_T = P_0 + sigma sqrt(T) Z

where:

    Z ~ N(0, 1)

the price of a European call option with strike K is:

    C = (P_0 - K) N(d) + sigma sqrt(T) phi(d)

where:

    d = (P_0 - K) / (sigma sqrt(T))

N is the cumulative distribution function of the standard normal distribution,
and phi is its probability density function.

This formula is one of the earliest closed-form option pricing formulas in the
history of mathematical finance.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


# =============================================================================
# Main parameters
# =============================================================================

P0 = 100.0
K = 100.0
SIGMA = 2.0
MATURITY = 1.0
N_PATHS = 500_000
SEED = 7


# =============================================================================
# Pricing formulas
# =============================================================================

def bachelier_call_price(p0, strike, sigma, maturity):
    """
    Compute the price of a European call option under the Bachelier model.

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

    # At maturity, or with zero volatility, the option is worth its intrinsic value.
    if maturity == 0 or sigma == 0:
        return float(max(p0 - strike, 0.0))

    d = (p0 - strike) / (sigma * np.sqrt(maturity))

    call_price = (
        (p0 - strike) * norm.cdf(d)
        + sigma * np.sqrt(maturity) * norm.pdf(d)
    )

    return float(call_price)


def bachelier_call_monte_carlo(
    p0,
    strike,
    sigma,
    maturity,
    n_paths=N_PATHS,
    seed=SEED,
):
    """
    Validate the Bachelier call price using Monte Carlo simulation.

    We simulate:

        P_T = P_0 + sigma sqrt(T) Z

    and compute:

        payoff = max(P_T - K, 0)

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
        Number of Monte Carlo simulations.
    seed : int
        Random seed used for reproducibility.

    Returns
    -------
    price : float
        Monte Carlo price estimate.
    standard_error : float
        Standard error of the Monte Carlo estimator.
    """

    if n_paths <= 0:
        raise ValueError("n_paths must be strictly positive.")

    if maturity == 0 or sigma == 0:
        return float(max(p0 - strike, 0.0)), 0.0

    rng = np.random.default_rng(seed)

    z = rng.standard_normal(n_paths)
    terminal_prices = p0 + sigma * np.sqrt(maturity) * z

    payoffs = np.maximum(terminal_prices - strike, 0.0)

    price = payoffs.mean()
    standard_error = payoffs.std(ddof=1) / np.sqrt(n_paths)

    return float(price), float(standard_error)


def black_scholes_call_price(spot, strike, volatility, maturity, rate=0.0):
    """
    Compute the Black-Scholes price of a European call option.

    This function is used only as a benchmark comparison.

    When relative volatility is low, Black-Scholes becomes locally close to an
    arithmetic Gaussian model around the current price level.

    Parameters
    ----------
    spot : float
        Current underlying price.
    strike : float
        Option strike.
    volatility : float
        Geometric volatility.
    maturity : float
        Time to maturity.
    rate : float
        Continuously compounded risk-free rate.

    Returns
    -------
    float
        Black-Scholes call option price.
    """

    if volatility < 0:
        raise ValueError("volatility must be non-negative.")

    if maturity < 0:
        raise ValueError("maturity must be non-negative.")

    if maturity == 0:
        return float(max(spot - strike, 0.0))

    if volatility == 0:
        discounted_intrinsic = spot - strike * np.exp(-rate * maturity)
        return float(max(discounted_intrinsic, 0.0))

    d1 = (
        np.log(spot / strike)
        + (rate + 0.5 * volatility**2) * maturity
    ) / (volatility * np.sqrt(maturity))

    d2 = d1 - volatility * np.sqrt(maturity)

    call_price = (
        spot * norm.cdf(d1)
        - strike * np.exp(-rate * maturity) * norm.cdf(d2)
    )

    return float(call_price)


# =============================================================================
# Numerical experiments
# =============================================================================

def compute_atm_scaling(p0=P0, sigma=SIGMA):
    """
    Verify the square-root-of-time scaling for an at-the-money Bachelier call.

    If strike = P0, then d = 0 and the Bachelier formula becomes:

        C_ATM = sigma sqrt(T) phi(0)

    Returns
    -------
    maturity_grid : np.ndarray
        Grid of maturities.
    atm_prices : np.ndarray
        Prices obtained from the general Bachelier formula.
    theoretical_atm_prices : np.ndarray
        Prices obtained from the simplified ATM expression.
    """

    maturity_grid = np.linspace(0.05, 4.0, 50)

    atm_prices = np.array([
        bachelier_call_price(p0, p0, sigma, maturity)
        for maturity in maturity_grid
    ])

    theoretical_atm_prices = sigma * np.sqrt(maturity_grid) * norm.pdf(0.0)

    return maturity_grid, atm_prices, theoretical_atm_prices


def compare_with_black_scholes(spot=100.0, black_scholes_volatility=0.02, maturity=1.0):
    """
    Compare Bachelier prices with Black-Scholes prices under low volatility.

    To make the comparison meaningful, the arithmetic Bachelier volatility is
    matched locally using:

        sigma_bachelier ≈ black_scholes_volatility * spot

    Returns
    -------
    strike_grid : np.ndarray
        Grid of option strikes.
    bachelier_prices : np.ndarray
        Bachelier call prices.
    black_scholes_prices : np.ndarray
        Black-Scholes call prices.
    """

    bachelier_sigma = black_scholes_volatility * spot
    strike_grid = np.linspace(80.0, 120.0, 41)

    bachelier_prices = np.array([
        bachelier_call_price(spot, strike, bachelier_sigma, maturity)
        for strike in strike_grid
    ])

    black_scholes_prices = np.array([
        black_scholes_call_price(
            spot=spot,
            strike=strike,
            volatility=black_scholes_volatility,
            maturity=maturity,
            rate=0.0,
        )
        for strike in strike_grid
    ])

    return strike_grid, bachelier_prices, black_scholes_prices


def save_figure(
    maturity_grid,
    atm_prices,
    strike_grid,
    bachelier_prices,
    black_scholes_prices,
    output_path="figures/fig2_option_pricing.png",
):
    """
    Save the main option pricing figure.

    The figure contains:

    1. The square-root-of-time scaling of an at-the-money Bachelier call.
    2. A comparison between Bachelier and Black-Scholes prices.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    # -------------------------------------------------------------------------
    # Panel 1: at-the-money call price and square-root-of-time scaling
    # -------------------------------------------------------------------------

    ax = axes[0]

    ax.plot(
        maturity_grid,
        atm_prices,
        lw=2,
        color="tab:blue",
    )

    ax.set_xlabel("Maturity")
    ax.set_ylabel("ATM call price")
    ax.set_title(
        r"Bachelier ATM Call Price"
        "\n"
        r"$C_{ATM} = \sigma\sqrt{T}\,\phi(0)$"
    )

    # -------------------------------------------------------------------------
    # Panel 2: Bachelier versus Black-Scholes
    # -------------------------------------------------------------------------

    ax = axes[1]

    ax.plot(
        strike_grid,
        bachelier_prices,
        lw=2,
        label="Bachelier (1900)",
    )

    ax.plot(
        strike_grid,
        black_scholes_prices,
        "--",
        lw=2,
        label="Black-Scholes (1973)",
    )

    ax.set_xlabel("Strike")
    ax.set_ylabel("Call price")
    ax.set_title(
        "Bachelier vs Black-Scholes\n"
        "Low volatility comparison"
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
    Run all numerical checks.
    """

    closed_form_price = bachelier_call_price(
        p0=P0,
        strike=K,
        sigma=SIGMA,
        maturity=MATURITY,
    )

    monte_carlo_price, monte_carlo_se = bachelier_call_monte_carlo(
        p0=P0,
        strike=K,
        sigma=SIGMA,
        maturity=MATURITY,
    )

    print("=== Bachelier (1900) European Call Option Pricing ===")
    print()
    print(f"P0 = {P0}")
    print(f"K = {K}")
    print(f"sigma = {SIGMA}")
    print(f"maturity = {MATURITY}")
    print()
    print(f"Closed-form price: {closed_form_price:.6f}")
    print(f"Monte Carlo price: {monte_carlo_price:.6f}")
    print(f"Monte Carlo standard error: ±{monte_carlo_se:.6f}")
    print(f"Absolute difference: {abs(closed_form_price - monte_carlo_price):.6f}")

    # -------------------------------------------------------------------------
    # Square-root-of-time scaling
    # -------------------------------------------------------------------------

    maturity_grid, atm_prices, theoretical_atm_prices = compute_atm_scaling()

    max_scaling_error = np.max(np.abs(atm_prices - theoretical_atm_prices))

    print()
    print("=== ATM Square-Root-of-Time Scaling ===")
    print("For K = P0, the formula becomes:")
    print("C_ATM = sigma * sqrt(T) * phi(0)")
    print(
        "Maximum error between the general formula and the ATM simplification: "
        f"{max_scaling_error:.2e}"
    )

    # -------------------------------------------------------------------------
    # Comparison with Black-Scholes
    # -------------------------------------------------------------------------

    strike_grid, bachelier_prices, black_scholes_prices = compare_with_black_scholes()

    max_model_difference = np.max(np.abs(bachelier_prices - black_scholes_prices))

    print()
    print("=== Bachelier vs Black-Scholes ===")
    print("Under low relative volatility, Black-Scholes is locally close")
    print("to the arithmetic Bachelier model around the current price.")
    print(f"Maximum difference over the strike grid [80, 120]: {max_model_difference:.4f}")

    figure_path = save_figure(
        maturity_grid=maturity_grid,
        atm_prices=atm_prices,
        strike_grid=strike_grid,
        bachelier_prices=bachelier_prices,
        black_scholes_prices=black_scholes_prices,
    )

    print()
    print(f"Figure saved to: {figure_path}")


if __name__ == "__main__":
    main()
