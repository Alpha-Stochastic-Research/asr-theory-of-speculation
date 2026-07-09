"""
Tests for the Bachelier option pricing formula.
"""

import numpy as np
import pytest
from scipy.stats import norm

from option_pricing import (
    bachelier_call_monte_carlo,
    bachelier_call_price,
    black_scholes_call_price,
    compare_with_black_scholes,
    compute_atm_scaling,
)


def test_bachelier_at_the_money_formula():
    """
    For an at-the-money Bachelier call, strike = P0 and d = 0.

    Therefore:

        C_ATM = sigma sqrt(T) phi(0)
    """

    p0 = 100.0
    strike = 100.0
    sigma = 2.0
    maturity = 1.0

    price = bachelier_call_price(
        p0=p0,
        strike=strike,
        sigma=sigma,
        maturity=maturity,
    )

    expected_price = sigma * np.sqrt(maturity) * norm.pdf(0.0)

    assert price == pytest.approx(expected_price)


def test_bachelier_price_at_maturity_is_intrinsic_value():
    """
    At maturity, the call price should be equal to its intrinsic value.
    """

    assert bachelier_call_price(105.0, 100.0, 2.0, 0.0) == 5.0
    assert bachelier_call_price(95.0, 100.0, 2.0, 0.0) == 0.0


def test_bachelier_zero_volatility_is_intrinsic_value():
    """
    If volatility is zero, the option payoff is deterministic.
    """

    assert bachelier_call_price(110.0, 100.0, 0.0, 1.0) == 10.0
    assert bachelier_call_price(90.0, 100.0, 0.0, 1.0) == 0.0


def test_monte_carlo_price_is_close_to_closed_form_price():
    """
    The Monte Carlo estimate should be close to the closed-form Bachelier price.
    """

    closed_form_price = bachelier_call_price(
        p0=100.0,
        strike=100.0,
        sigma=2.0,
        maturity=1.0,
    )

    monte_carlo_price, monte_carlo_se = bachelier_call_monte_carlo(
        p0=100.0,
        strike=100.0,
        sigma=2.0,
        maturity=1.0,
        n_paths=100_000,
        seed=7,
    )

    difference = abs(closed_form_price - monte_carlo_price)

    assert difference < 4.0 * monte_carlo_se


def test_atm_scaling_matches_theoretical_expression():
    """
    The general Bachelier formula should match the simplified ATM expression.
    """

    _, atm_prices, theoretical_atm_prices = compute_atm_scaling(
        p0=100.0,
        sigma=2.0,
    )

    assert np.allclose(atm_prices, theoretical_atm_prices)


def test_black_scholes_price_at_maturity_is_intrinsic_value():
    """
    At maturity, Black-Scholes also reduces to intrinsic value.
    """

    assert black_scholes_call_price(105.0, 100.0, 0.2, 0.0) == 5.0
    assert black_scholes_call_price(95.0, 100.0, 0.2, 0.0) == 0.0


def test_black_scholes_comparison_returns_matching_arrays():
    """
    The comparison function should return arrays of the same length.
    """

    strike_grid, bachelier_prices, black_scholes_prices = compare_with_black_scholes()

    assert len(strike_grid) == len(bachelier_prices)
    assert len(strike_grid) == len(black_scholes_prices)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"p0": 100.0, "strike": 100.0, "sigma": -1.0, "maturity": 1.0},
        {"p0": 100.0, "strike": 100.0, "sigma": 2.0, "maturity": -1.0},
    ],
)
def test_invalid_bachelier_inputs_raise_error(kwargs):
    """
    Invalid Bachelier pricing inputs should raise a ValueError.
    """

    with pytest.raises(ValueError):
        bachelier_call_price(**kwargs)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"spot": 100.0, "strike": 100.0, "volatility": -0.2, "maturity": 1.0},
        {"spot": 100.0, "strike": 100.0, "volatility": 0.2, "maturity": -1.0},
    ],
)
def test_invalid_black_scholes_inputs_raise_error(kwargs):
    """
    Invalid Black-Scholes pricing inputs should raise a ValueError.
    """

    with pytest.raises(ValueError):
        black_scholes_call_price(**kwargs)
