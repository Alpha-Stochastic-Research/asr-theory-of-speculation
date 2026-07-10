"""
Bachelier model tools for Alpha Stochastic Research.

This package provides a reproducible implementation of the arithmetic
Brownian motion model introduced by Louis Bachelier in 1900, together with
closed-form option pricing and Monte Carlo validation tools.

Installation package
--------------------
pip install asr-theory-of-speculation

ASR ecosystem package
---------------------
pip install asr-open-sc

Python import
-------------
>>> from asr.models import bachelier
>>> price = bachelier.call_price(
...     initial_price=100.0,
...     strike=100.0,
...     volatility=2.0,
...     maturity=1.0,
... )
"""

from .pricing import (
    atm_call_price,
    black_scholes_call_price,
    call_monte_carlo_price,
    call_price,
    compare_with_black_scholes,
)
from .process import (
    BachelierPathAnalysis,
    BachelierProcessConfig,
    analyze_paths,
    simulate_from_config,
    simulate_paths,
)
from .simulation import (
    run_brownian_motion_experiment,
    run_option_pricing_experiment,
    save_brownian_motion_figure,
    save_option_pricing_figure,
)

__version__ = "1.1.0"

__all__ = [
    "__version__",
    "BachelierPathAnalysis",
    "BachelierProcessConfig",
    "simulate_paths",
    "simulate_from_config",
    "analyze_paths",
    "call_price",
    "atm_call_price",
    "call_monte_carlo_price",
    "black_scholes_call_price",
    "compare_with_black_scholes",
    "run_brownian_motion_experiment",
    "run_option_pricing_experiment",
    "save_brownian_motion_figure",
    "save_option_pricing_figure",
]
