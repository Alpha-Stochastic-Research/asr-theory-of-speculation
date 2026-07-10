"""
Tests for the Bachelier arithmetic Brownian motion process.
"""

from __future__ import annotations

import numpy as np
import pytest

from asr.models import bachelier


def test_simulate_paths_shape() -> None:
    """
    Simulated paths should have the expected dimensions.
    """

    n_steps = 20
    n_paths = 100

    time_grid, paths = bachelier.simulate_paths(
        initial_price=100.0,
        volatility=2.0,
        maturity=1.0,
        n_steps=n_steps,
        n_paths=n_paths,
        seed=42,
    )

    assert time_grid.shape == (n_steps + 1,)
    assert paths.shape == (n_paths, n_steps + 1)


def test_simulate_paths_initial_value() -> None:
    """
    All simulated paths should start from the initial price.
    """

    _, paths = bachelier.simulate_paths(
        initial_price=123.45,
        volatility=2.0,
        maturity=1.0,
        n_steps=10,
        n_paths=50,
        seed=42,
    )

    assert np.allclose(paths[:, 0], 123.45)


def test_simulate_paths_reproducibility() -> None:
    """
    Simulations with the same seed should be exactly reproducible.
    """

    _, paths_1 = bachelier.simulate_paths(seed=123)
    _, paths_2 = bachelier.simulate_paths(seed=123)

    assert np.array_equal(paths_1, paths_2)


def test_analyze_paths_returns_expected_statistics() -> None:
    """
    Path analysis should return arrays with correct shapes and finite values.
    """

    time_grid, paths = bachelier.simulate_paths(
        initial_price=100.0,
        volatility=2.0,
        maturity=1.0,
        n_steps=100,
        n_paths=2_000,
        seed=42,
    )

    analysis = bachelier.analyze_paths(
        time_grid=time_grid,
        paths=paths,
        initial_price=100.0,
        volatility=2.0,
    )

    assert analysis.mean_path.shape == time_grid.shape
    assert analysis.empirical_variance.shape == time_grid.shape
    assert analysis.theoretical_variance.shape == time_grid.shape
    assert np.all(np.isfinite(analysis.mean_path))
    assert np.all(np.isfinite(analysis.empirical_variance))
    assert np.allclose(analysis.theoretical_variance, 4.0 * time_grid)


def test_terminal_mean_is_close_to_initial_price() -> None:
    """
    The Bachelier process is a martingale under the simulation measure.
    """

    time_grid, paths = bachelier.simulate_paths(
        initial_price=100.0,
        volatility=2.0,
        maturity=1.0,
        n_steps=250,
        n_paths=20_000,
        seed=42,
    )

    analysis = bachelier.analyze_paths(
        time_grid=time_grid,
        paths=paths,
        initial_price=100.0,
        volatility=2.0,
    )

    assert abs(analysis.terminal_mean - 100.0) < 0.10


def test_terminal_variance_is_close_to_theoretical_variance() -> None:
    """
    Terminal empirical variance should be close to sigma squared times maturity.
    """

    time_grid, paths = bachelier.simulate_paths(
        initial_price=100.0,
        volatility=2.0,
        maturity=1.0,
        n_steps=250,
        n_paths=20_000,
        seed=42,
    )

    analysis = bachelier.analyze_paths(
        time_grid=time_grid,
        paths=paths,
        initial_price=100.0,
        volatility=2.0,
    )

    assert abs(
        analysis.terminal_empirical_variance
        - analysis.terminal_theoretical_variance
    ) < 0.15


def test_run_brownian_motion_experiment() -> None:
    """
    The high-level Brownian motion experiment should run successfully.
    """

    time_grid, paths, analysis = bachelier.run_brownian_motion_experiment(
        n_steps=50,
        n_paths=500,
        seed=42,
    )

    assert time_grid.shape == (51,)
    assert paths.shape == (500, 51)
    assert analysis.terminal_theoretical_variance == pytest.approx(4.0)


def test_invalid_simulation_inputs_raise_errors() -> None:
    """
    Invalid simulation inputs should raise ValueError.
    """

    with pytest.raises(ValueError):
        bachelier.simulate_paths(volatility=-1.0)

    with pytest.raises(ValueError):
        bachelier.simulate_paths(maturity=0.0)

    with pytest.raises(ValueError):
        bachelier.simulate_paths(n_steps=0)

    with pytest.raises(ValueError):
        bachelier.simulate_paths(n_paths=0)


def test_invalid_analysis_inputs_raise_errors() -> None:
    """
    Invalid analysis inputs should raise ValueError.
    """

    time_grid = np.linspace(0.0, 1.0, 11)
    paths = np.zeros((10, 10))

    with pytest.raises(ValueError):
        bachelier.analyze_paths(time_grid=time_grid, paths=paths)

    with pytest.raises(ValueError):
        bachelier.analyze_paths(
            time_grid=np.zeros((2, 2)),
            paths=np.zeros((10, 4)),
        )

    with pytest.raises(ValueError):
        bachelier.analyze_paths(
            time_grid=time_grid,
            paths=np.zeros(10),
        )
