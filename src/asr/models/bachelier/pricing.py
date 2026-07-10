"""
Bachelier option pricing tools.

This module implements the closed-form Bachelier European call option formula,
a Monte Carlo estimator, and a local comparison with the Black-Scholes model.

The Bachelier model assumes arithmetic price dynamics:

    P_T = P_0 + sigma sqrt(T) Z,

where Z is a standard normal random variable.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import norm


def _validate_bachelier_pricing_inputs(
    initial_price: float,
    strike: float,
    volatility: float,
    maturity: float,
) -> None:
    """
    Validate inputs for Bachelier option pricing.

    Raises
    ------
    ValueError
        If one or more inputs are outside the admissible range.
    """

    if not np.isfinite(initial_price):
        raise ValueError("initial_price must be finite.")

    if not np.isfinite(strike):
        raise ValueError("strike must be finite.")

    if volatility < 0 or not np.isfinite(volatility):
        raise ValueError("volatility must be a finite non-negative number.")

    if maturity < 0 or not np.isfinite(maturity):
        raise ValueError("maturity must be a finite non-negative number.")


def call_price(
    initial_price: float,
    strike: float,
    volatility: float,
    maturity: float,
) -> float:
    """
    Compute the Bachelier European call option price.

    The terminal price is:

        P_T = P_0 + sigma sqrt(T) Z,

    where Z is standard normal.

    The call price is:

        C = (P_0 - K) Phi(d) + sigma sqrt(T) phi(d),

    with:

        d = (P_0 - K) / (sigma sqrt(T)).

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

    Returns
    -------
    float
        Bachelier European call option price.
    """

    _validate_bachelier_pricing_inputs(
        initial_price=initial_price,
        strike=strike,
        volatility=volatility,
        maturity=maturity,
    )

    intrinsic_value = max(initial_price - strike, 0.0)

    if maturity == 0.0 or volatility == 0.0:
        return float(intrinsic_value)

    standard_deviation = volatility * np.sqrt(maturity)
    d = (initial_price - strike) / standard_deviation

    price = (initial_price - strike) * norm.cdf(d) + standard_deviation * norm.pdf(d)

    return float(price)


def atm_call_price(
    volatility: float,
    maturity: float,
) -> float:
    """
    Compute the at-the-money Bachelier call option price.

    For K = P_0, the Bachelier call price simplifies to:

        C_ATM = sigma sqrt(T) phi(0).

    Parameters
    ----------
    volatility:
        Arithmetic volatility sigma.
    maturity:
        Time to maturity T.

    Returns
    -------
    float
        At-the-money Bachelier call option price.
    """

    if volatility < 0 or not np.isfinite(volatility):
        raise ValueError("volatility must be a finite non-negative number.")

    if maturity < 0 or not np.isfinite(maturity):
        raise ValueError("maturity must be a finite non-negative number.")

    if maturity == 0.0 or volatility == 0.0:
        return 0.0

    return float(volatility * np.sqrt(maturity) * norm.pdf(0.0))


def call_monte_carlo_price(
    initial_price: float,
    strike: float,
    volatility: float,
    maturity: float,
    n_paths: int = 500_000,
    seed: int | None = 7,
) -> tuple[float, float]:
    """
    Estimate the Bachelier European call price by Monte Carlo simulation.

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
    tuple[float, float]
        Monte Carlo price estimate and standard error.
    """

    _validate_bachelier_pricing_inputs(
        initial_price=initial_price,
        strike=strike,
        volatility=volatility,
        maturity=maturity,
    )

    if n_paths <= 0:
        raise ValueError("n_paths must be a positive integer.")

    if maturity == 0.0 or volatility == 0.0:
        deterministic_payoff = max(initial_price - strike, 0.0)
        return float(deterministic_payoff), 0.0

    rng = np.random.default_rng(seed)

    terminal_prices = (
        initial_price
        + volatility * np.sqrt(maturity) * rng.standard_normal(size=n_paths)
    )

    payoffs = np.maximum(terminal_prices - strike, 0.0)

    price_estimate = float(payoffs.mean())
    standard_error = float(payoffs.std(ddof=1) / np.sqrt(n_paths))

    return price_estimate, standard_error


def black_scholes_call_price(
    spot: float,
    strike: float,
    volatility: float,
    maturity: float,
    rate: float = 0.0,
) -> float:
    """
    Compute the Black-Scholes European call option price.

    This function is included only as a benchmark for comparison with the
    Bachelier model in low-relative-volatility regimes.

    Parameters
    ----------
    spot:
        Current underlying price S_0.
    strike:
        Strike price K.
    volatility:
        Black-Scholes proportional volatility.
    maturity:
        Time to maturity T.
    rate:
        Continuously compounded risk-free rate.

    Returns
    -------
    float
        Black-Scholes European call option price.
    """

    if spot <= 0 or not np.isfinite(spot):
        raise ValueError("spot must be a finite positive number.")

    if strike <= 0 or not np.isfinite(strike):
        raise ValueError("strike must be a finite positive number.")

    if volatility < 0 or not np.isfinite(volatility):
        raise ValueError("volatility must be a finite non-negative number.")

    if maturity < 0 or not np.isfinite(maturity):
        raise ValueError("maturity must be a finite non-negative number.")

    if not np.isfinite(rate):
        raise ValueError("rate must be finite.")

    if maturity == 0.0:
        return float(max(spot - strike, 0.0))

    if volatility == 0.0:
        deterministic_terminal_price = spot * np.exp(rate * maturity)
        discounted_payoff = np.exp(-rate * maturity) * max(
            deterministic_terminal_price - strike,
            0.0,
        )
        return float(discounted_payoff)

    denominator = volatility * np.sqrt(maturity)

    d1 = (np.log(spot / strike) + (rate + 0.5 * volatility**2) * maturity) / denominator
    d2 = d1 - denominator

    price = spot * norm.cdf(d1) - strike * np.exp(-rate * maturity) * norm.cdf(d2)

    return float(price)


def compare_with_black_scholes(
    spot: float = 100.0,
    black_scholes_volatility: float = 0.02,
    maturity: float = 1.0,
    rate: float = 0.0,
    strike_min: float = 80.0,
    strike_max: float = 120.0,
    n_strikes: int = 81,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compare Bachelier and Black-Scholes call prices across strikes.

    The comparison uses the local volatility matching approximation:

        sigma_Bachelier = spot * sigma_BlackScholes.

    Parameters
    ----------
    spot:
        Current underlying price.
    black_scholes_volatility:
        Proportional Black-Scholes volatility.
    maturity:
        Time to maturity.
    rate:
        Continuously compounded risk-free rate.
    strike_min:
        Minimum strike in the comparison grid.
    strike_max:
        Maximum strike in the comparison grid.
    n_strikes:
        Number of strikes in the comparison grid.

    Returns
    -------
    tuple[np.ndarray, np.ndarray, np.ndarray]
        Strike grid, Bachelier prices, and Black-Scholes prices.
    """

    if spot <= 0 or not np.isfinite(spot):
        raise ValueError("spot must be a finite positive number.")

    if black_scholes_volatility < 0 or not np.isfinite(black_scholes_volatility):
        raise ValueError(
            "black_scholes_volatility must be a finite non-negative number."
        )

    if maturity < 0 or not np.isfinite(maturity):
        raise ValueError("maturity must be a finite non-negative number.")

    if not np.isfinite(rate):
        raise ValueError("rate must be finite.")

    if strike_min <= 0 or strike_max <= 0:
        raise ValueError("strike_min and strike_max must be positive.")

    if strike_min >= strike_max:
        raise ValueError("strike_min must be smaller than strike_max.")

    if n_strikes <= 1:
        raise ValueError("n_strikes must be greater than one.")

    strike_grid = np.linspace(strike_min, strike_max, n_strikes)
    bachelier_volatility = spot * black_scholes_volatility

    bachelier_prices = np.array(
        [
            call_price(
                initial_price=spot,
                strike=strike,
                volatility=bachelier_volatility,
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
                rate=rate,
            )
            for strike in strike_grid
        ]
    )

    return strike_grid, bachelier_prices, black_scholes_prices
