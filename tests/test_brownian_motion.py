"""
Tests for the Bachelier arithmetic Brownian motion simulation.
"""

import numpy as np
import pytest

from brownian_motion import (
    analyze_bachelier_paths,
    simulate_bachelier_paths,
)


def test_simulated_paths_have_correct_shape():
    """
    The simulation should return a time grid and a matrix of paths
    with the expected dimensions.
    """

    n_steps = 10
    n_paths = 100

    t_grid, paths = simulate_bachelier_paths(
        p0=100.0,
        sigma=2.0,
        maturity=1.0,
        n_steps=n_steps,
        n_paths=n_paths,
        seed=42,
    )

    assert t_grid.shape == (n_steps + 1,)
    assert paths.shape == (n_paths, n_steps + 1)


def test_all_paths_start_at_initial_price():
    """
    Every simulated path should start at the initial price P0.
    """

    p0 = 100.0

    _, paths = simulate_bachelier_paths(
        p0=p0,
        sigma=2.0,
        maturity=1.0,
        n_steps=20,
        n_paths=200,
        seed=42,
    )

    assert np.allclose(paths[:, 0], p0)


def test_simulation_is_reproducible_with_fixed_seed():
    """
    Using the same random seed should produce exactly the same paths.
    """

    _, paths_a = simulate_bachelier_paths(seed=123)
    _, paths_b = simulate_bachelier_paths(seed=123)

    assert np.allclose(paths_a, paths_b)


def test_theoretical_variance_is_sigma_squared_times_time():
    """
    Under the Bachelier model:

        Var[P_t] = sigma^2 t
    """

    sigma = 2.0

    t_grid, paths = simulate_bachelier_paths(
        p0=100.0,
        sigma=sigma,
        maturity=1.0,
        n_steps=100,
        n_paths=1_000,
        seed=42,
    )

    _, _, theoretical_variance = analyze_bachelier_paths(
        t_grid=t_grid,
        paths=paths,
        p0=100.0,
        sigma=sigma,
    )

    expected_variance = sigma**2 * t_grid

    assert np.allclose(theoretical_variance, expected_variance)


def test_empirical_mean_is_close_to_initial_price():
    """
    With many simulated paths, the empirical mean should remain close to P0.

    This is a numerical check of the martingale property:

        E[P_t] = P0
    """

    p0 = 100.0

    t_grid, paths = simulate_bachelier_paths(
        p0=p0,
        sigma=2.0,
        maturity=1.0,
        n_steps=100,
        n_paths=20_000,
        seed=42,
    )

    mean_path, _, _ = analyze_bachelier_paths(
        t_grid=t_grid,
        paths=paths,
        p0=p0,
        sigma=2.0,
    )

    max_deviation = np.max(np.abs(mean_path - p0))

    assert max_deviation < 0.10


def test_empirical_variance_is_close_to_theoretical_variance_at_maturity():
    """
    The empirical terminal variance should be close to the theoretical value:

        sigma^2 T
    """

    sigma = 2.0
    maturity = 1.0

    t_grid, paths = simulate_bachelier_paths(
        p0=100.0,
        sigma=sigma,
        maturity=maturity,
        n_steps=100,
        n_paths=20_000,
        seed=42,
    )

    _, empirical_variance, theoretical_variance = analyze_bachelier_paths(
        t_grid=t_grid,
        paths=paths,
        p0=100.0,
        sigma=sigma,
    )

    relative_error = abs(empirical_variance[-1] - theoretical_variance[-1]) / theoretical_variance[-1]

    assert relative_error < 0.05


@pytest.mark.parametrize(
    "kwargs",
    [
        {"sigma": -1.0},
        {"maturity": 0.0},
        {"n_steps": 0},
        {"n_paths": 0},
    ],
)
def test_invalid_simulation_inputs_raise_error(kwargs):
    """
    Invalid simulation parameters should raise a ValueError.
    """

    with pytest.raises(ValueError):
        simulate_bachelier_paths(**kwargs)
