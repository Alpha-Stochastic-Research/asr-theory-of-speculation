"""
Tests for Bachelier option pricing tools.
"""

from __future__ import annotations

import numpy as np
import pytest
from scipy.stats import norm

from asr.models import bachelier


def test_call_price_at_the_money_formula() -> None:
    """
    The at-the-money Bachelier call price should equal sigma sqrt(T) phi(0).
    """

    price = bachelier.call_price(
        initial_price=100.0,
        strike=100.0,
        volatility=2.0,
        maturity=1.0,
    )

    expected_price = 2.0 * norm.pdf(0.0)

    assert price == pytest.approx(expected_price)


def test_atm_call_price_matches_general_formula() -> None:
    """
    The specialized ATM formula should match the general call formula.
    """

    atm_price = bachelier.atm_call_price(
        volatility=2.0,
        maturity=1.0,
    )

    general_price = bachelier.call_price(
        initial_price=100.0,
        strike=100.0,
        volatility=2.0,
        maturity=1.0,
    )

    assert atm_price == pytest.approx(general_price)


def test_call_price_at_maturity_equals_intrinsic_value() -> None:
    """
    At maturity, the option price should equal intrinsic value.
    """

    price_in_the_money = bachelier.call_price(
        initial_price=105.0,
        strike=100.0,
        volatility=2.0,
        maturity=0.0,
    )

    price_out_of_the_money = bachelier.call_price(
        initial_price=95.0,
        strike=100.0,
        volatility=2.0,
        maturity=0.0,
    )

    assert price_in_the_money == pytest.approx(5.0)
    assert price_out_of_the_money == pytest.approx(0.0)


def test_call_price_with_zero_volatility_equals_intrinsic_value() -> None:
    """
    With zero volatility, the Bachelier call price is deterministic.
    """

    price = bachelier.call_price(
        initial_price=105.0,
        strike=100.0,
        volatility=0.0,
        maturity=1.0,
    )

    assert price == pytest.approx(5.0)


def test_monte_carlo_price_is_close_to_closed_form_price() -> None:
    """
    Monte Carlo price should be close to the analytical Bachelier price.
    """

    closed_form_price = bachelier.call_price(
        initial_price=100.0,
        strike=100.0,
        volatility=2.0,
        maturity=1.0,
    )

    monte_carlo_price, standard_error = bachelier.call_monte_carlo_price(
        initial_price=100.0,
        strike=100.0,
        volatility=2.0,
        maturity=1.0,
        n_paths=300_000,
        seed=7,
    )

    assert abs(monte_carlo_price - closed_form_price) < 4.0 * standard_error


def test_monte_carlo_zero_maturity_returns_intrinsic_value() -> None:
    """
    Monte Carlo pricing at maturity should return deterministic intrinsic value.
    """

    price, standard_error = bachelier.call_monte_carlo_price(
        initial_price=105.0,
        strike=100.0,
        volatility=2.0,
        maturity=0.0,
        n_paths=10_000,
        seed=7,
    )

    assert price == pytest.approx(5.0)
    assert standard_error == pytest.approx(0.0)


def test_run_option_pricing_experiment() -> None:
    """
    The high-level option pricing experiment should run successfully.
    """

    results = bachelier.run_option_pricing_experiment(
        initial_price=100.0,
        strike=100.0,
        volatility=2.0,
        maturity=1.0,
        n_paths=200_000,
        seed=7,
    )

    assert set(results) == {
        "closed_form_price",
        "monte_carlo_price",
        "monte_carlo_standard_error",
        "absolute_difference",
    }

    assert results["closed_form_price"] > 0.0
    assert results["monte_carlo_price"] > 0.0
    assert results["monte_carlo_standard_error"] > 0.0
    assert results["absolute_difference"] >= 0.0


def test_black_scholes_price_at_maturity() -> None:
    """
    Black-Scholes price at maturity should equal intrinsic value.
    """

    price = bachelier.black_scholes_call_price(
        spot=105.0,
        strike=100.0,
        volatility=0.2,
        maturity=0.0,
    )

    assert price == pytest.approx(5.0)


def test_black_scholes_zero_volatility() -> None:
    """
    Black-Scholes with zero volatility should return discounted deterministic payoff.
    """

    price = bachelier.black_scholes_call_price(
        spot=100.0,
        strike=95.0,
        volatility=0.0,
        maturity=1.0,
        rate=0.0,
    )

    assert price == pytest.approx(5.0)


def test_compare_with_black_scholes_returns_consistent_arrays() -> None:
    """
    The comparison function should return strike and price arrays of equal length.
    """

    strike_grid, bachelier_prices, black_scholes_prices = (
        bachelier.compare_with_black_scholes(
            spot=100.0,
            black_scholes_volatility=0.02,
            maturity=1.0,
            n_strikes=21,
        )
    )

    assert strike_grid.shape == (21,)
    assert bachelier_prices.shape == (21,)
    assert black_scholes_prices.shape == (21,)
    assert np.all(bachelier_prices >= 0.0)
    assert np.all(black_scholes_prices >= 0.0)


def test_invalid_bachelier_pricing_inputs_raise_errors() -> None:
    """
    Invalid Bachelier pricing inputs should raise ValueError.
    """

    with pytest.raises(ValueError):
        bachelier.call_price(
            initial_price=100.0,
            strike=100.0,
            volatility=-1.0,
            maturity=1.0,
        )

    with pytest.raises(ValueError):
        bachelier.call_price(
            initial_price=100.0,
            strike=100.0,
            volatility=1.0,
            maturity=-1.0,
        )

    with pytest.raises(ValueError):
        bachelier.atm_call_price(
            volatility=-1.0,
            maturity=1.0,
        )

    with pytest.raises(ValueError):
        bachelier.call_monte_carlo_price(
            initial_price=100.0,
            strike=100.0,
            volatility=2.0,
            maturity=1.0,
            n_paths=0,
        )


def test_invalid_black_scholes_inputs_raise_errors() -> None:
    """
    Invalid Black-Scholes inputs should raise ValueError.
    """

    with pytest.raises(ValueError):
        bachelier.black_scholes_call_price(
            spot=0.0,
            strike=100.0,
            volatility=0.2,
            maturity=1.0,
        )

    with pytest.raises(ValueError):
        bachelier.black_scholes_call_price(
            spot=100.0,
            strike=0.0,
            volatility=0.2,
            maturity=1.0,
        )

    with pytest.raises(ValueError):
        bachelier.black_scholes_call_price(
            spot=100.0,
            strike=100.0,
            volatility=-0.2,
            maturity=1.0,
        )

    with pytest.raises(ValueError):
        bachelier.black_scholes_call_price(
            spot=100.0,
            strike=100.0,
            volatility=0.2,
            maturity=-1.0,
        )


def test_invalid_black_scholes_comparison_inputs_raise_errors() -> None:
    """
    Invalid Black-Scholes comparison inputs should raise ValueError.
    """

    with pytest.raises(ValueError):
        bachelier.compare_with_black_scholes(spot=0.0)

    with pytest.raises(ValueError):
        bachelier.compare_with_black_scholes(black_scholes_volatility=-0.1)

    with pytest.raises(ValueError):
        bachelier.compare_with_black_scholes(strike_min=120.0, strike_max=80.0)

    with pytest.raises(ValueError):
        bachelier.compare_with_black_scholes(n_strikes=1)
