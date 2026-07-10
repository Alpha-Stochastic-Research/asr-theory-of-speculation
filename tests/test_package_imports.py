"""
Tests for the public ASR Bachelier package import interface.
"""

from __future__ import annotations

import importlib


def test_import_asr_models_bachelier() -> None:
    """
    The public package should be importable as asr.models.bachelier.
    """

    bachelier = importlib.import_module("asr.models.bachelier")

    assert bachelier.__version__ == "1.1.0"


def test_public_import_style() -> None:
    """
    The expected public import style should work.

    This supports:

        from asr.models import bachelier
    """

    from asr.models import bachelier

    assert bachelier.__version__ == "1.1.0"
    assert hasattr(bachelier, "simulate_paths")
    assert hasattr(bachelier, "simulate_from_config")
    assert hasattr(bachelier, "analyze_paths")
    assert hasattr(bachelier, "call_price")
    assert hasattr(bachelier, "atm_call_price")
    assert hasattr(bachelier, "call_monte_carlo_price")
    assert hasattr(bachelier, "black_scholes_call_price")
    assert hasattr(bachelier, "compare_with_black_scholes")
    assert hasattr(bachelier, "run_brownian_motion_experiment")
    assert hasattr(bachelier, "run_option_pricing_experiment")
    assert hasattr(bachelier, "save_brownian_motion_figure")
    assert hasattr(bachelier, "save_option_pricing_figure")


def test_public_api_basic_usage() -> None:
    """
    The public API should support a minimal end-to-end usage example.
    """

    from asr.models import bachelier

    time_grid, paths = bachelier.simulate_paths(
        initial_price=100.0,
        volatility=2.0,
        maturity=1.0,
        n_steps=10,
        n_paths=100,
        seed=42,
    )

    analysis = bachelier.analyze_paths(
        time_grid=time_grid,
        paths=paths,
        initial_price=100.0,
        volatility=2.0,
    )

    price = bachelier.call_price(
        initial_price=100.0,
        strike=100.0,
        volatility=2.0,
        maturity=1.0,
    )

    assert time_grid.shape == (11,)
    assert paths.shape == (100, 11)
    assert analysis.terminal_theoretical_variance == 4.0
    assert price > 0.0
