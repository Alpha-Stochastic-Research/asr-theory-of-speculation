"""
Reproduction du modèle de Bachelier (1900) :
marche aléatoire arithmétique et mouvement brownien.

Dans la Théorie de la Spéculation, Bachelier modélise le prix comme :

    P_t = P_0 + sigma * W_t

où :
    - P_0 est le prix initial,
    - sigma est la volatilité arithmétique,
    - W_t est un mouvement brownien standard.

Ce script vérifie numériquement deux propriétés importantes :

1. Propriété de martingale :
       E[P_t] = P_0

2. Croissance linéaire de la variance :
       Var[P_t] = sigma^2 * t

L'objectif est de garder un code simple, lisible et reproductible.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# ============================================================================
# Paramètres principaux de la simulation
# ============================================================================

P0 = 100.0          # Prix initial
SIGMA = 2.0        # Volatilité arithmétique
T = 1.0            # Horizon de temps
N_STEPS = 250      # Nombre de pas de temps
N_PATHS = 5_000    # Nombre de trajectoires simulées
SEED = 42          # Graine aléatoire pour reproduire les résultats


# ============================================================================
# Fonctions utiles
# ============================================================================

def simulate_bachelier_paths(
    p0=P0,
    sigma=SIGMA,
    T=T,
    n_steps=N_STEPS,
    n_paths=N_PATHS,
    seed=SEED,
):
    """
    Simule des trajectoires du modèle de Bachelier.

    Le modèle est :

        P_t = P_0 + sigma * W_t

    Sur un petit intervalle de temps dt, les incréments sont :

        dP_t ~ N(0, sigma^2 dt)

    Parameters
    ----------
    p0 : float
        Prix initial.
    sigma : float
        Volatilité arithmétique.
    T : float
        Horizon de temps.
    n_steps : int
        Nombre de pas de discrétisation.
    n_paths : int
        Nombre de trajectoires Monte Carlo.
    seed : int
        Graine aléatoire pour rendre la simulation reproductible.

    Returns
    -------
    t_grid : np.ndarray
        Grille temporelle.
    paths : np.ndarray
        Matrice des trajectoires simulées.
    """

    if sigma < 0:
        raise ValueError("sigma doit être positif ou nul.")

    if T <= 0:
        raise ValueError("T doit être strictement positif.")

    if n_steps <= 0:
        raise ValueError("n_steps doit être strictement positif.")

    if n_paths <= 0:
        raise ValueError("n_paths doit être strictement positif.")

    rng = np.random.default_rng(seed)

    dt = T / n_steps
    t_grid = np.linspace(0, T, n_steps + 1)

    # Incréments gaussiens indépendants :
    # dP_t = sigma * sqrt(dt) * Z, avec Z ~ N(0,1)
    increments = rng.normal(
        loc=0.0,
        scale=sigma * np.sqrt(dt),
        size=(n_paths, n_steps),
    )

    # On construit les trajectoires en cumulant les incréments.
    paths = np.zeros((n_paths, n_steps + 1))
    paths[:, 0] = p0
    paths[:, 1:] = p0 + np.cumsum(increments, axis=1)

    return t_grid, paths


def analyse_bachelier_paths(t_grid, paths, p0=P0, sigma=SIGMA):
    """
    Calcule les grandeurs empiriques principales.

    On vérifie :

        E[P_t] ≈ P_0
        Var[P_t] ≈ sigma^2 t

    Parameters
    ----------
    t_grid : np.ndarray
        Grille temporelle.
    paths : np.ndarray
        Trajectoires simulées.
    p0 : float
        Prix initial.
    sigma : float
        Volatilité arithmétique.

    Returns
    -------
    mean_path : np.ndarray
        Espérance empirique de P_t.
    empirical_var : np.ndarray
        Variance empirique de P_t.
    theoretical_var : np.ndarray
        Variance théorique sigma^2 t.
    """

    mean_path = paths.mean(axis=0)
    empirical_var = paths.var(axis=0)
    theoretical_var = sigma**2 * t_grid

    return mean_path, empirical_var, theoretical_var


def save_figure(
    t_grid,
    paths,
    mean_path,
    empirical_var,
    theoretical_var,
    p0=P0,
    sigma=SIGMA,
    output_path="figures/fig1_random_walk_martingale.png",
):
    """
    Sauvegarde la figure principale du script.

    La figure contient :

    1. Des trajectoires simulées du modèle de Bachelier.
    2. La comparaison entre variance empirique et variance théorique.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    # ------------------------------------------------------------------------
    # Graphique 1 : trajectoires simulées
    # ------------------------------------------------------------------------

    ax = axes[0]

    for i in range(60):
        ax.plot(t_grid, paths[i], lw=0.6, alpha=0.5)

    ax.plot(
        t_grid,
        mean_path,
        color="black",
        lw=2,
        label=r"$E[P_t]$ empirique",
    )

    ax.axhline(
        p0,
        color="red",
        ls="--",
        lw=1,
        label=r"$P_0$",
    )

    ax.plot(
        t_grid,
        p0 + sigma * np.sqrt(t_grid),
        color="blue",
        ls=":",
        lw=1.5,
        label=r"$P_0 \pm \sigma\sqrt{t}$",
    )

    ax.plot(
        t_grid,
        p0 - sigma * np.sqrt(t_grid),
        color="blue",
        ls=":",
        lw=1.5,
    )

    ax.set_xlabel("t")
    ax.set_ylabel(r"$P_t$")
    ax.set_title(
        "Marche aléatoire arithmétique — Bachelier (1900)\n"
        "60 trajectoires simulées"
    )
    ax.legend(fontsize=8)

    # ------------------------------------------------------------------------
    # Graphique 2 : variance empirique vs variance théorique
    # ------------------------------------------------------------------------

    ax = axes[1]

    ax.plot(
        t_grid,
        empirical_var,
        lw=2,
        label="Variance empirique",
    )

    ax.plot(
        t_grid,
        theoretical_var,
        "--",
        lw=2,
        label=r"Variance théorique $\sigma^2 t$",
    )

    ax.set_xlabel("t")
    ax.set_ylabel(r"Var$[P_t]$")
    ax.set_title(
        "Croissance linéaire de la variance\n"
        r"et écart-type en $\sqrt{t}$"
    )
    ax.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()

    return output_path


# ============================================================================
# Exécution principale
# ============================================================================

def main():
    """
    Lance l'expérience numérique complète.
    """

    t_grid, paths = simulate_bachelier_paths()

    mean_path, empirical_var, theoretical_var = analyse_bachelier_paths(
        t_grid=t_grid,
        paths=paths,
    )

    max_dev = np.max(np.abs(mean_path - P0))

    rel_error_var_final = (
        abs(empirical_var[-1] - theoretical_var[-1])
        / theoretical_var[-1]
    )

    empirical_std_final = np.std(paths[:, -1])
    theoretical_std_final = SIGMA * np.sqrt(T)

    negative_price_probability = np.mean(paths[:, -1] < 0)

    print("=== Vérification du modèle de Bachelier (1900) ===")
    print()
    print("Propriété de martingale :")
    print(f"Écart max entre E[P_t] simulé et P0 : {max_dev:.4f}")
    print()
    print("Croissance de la variance :")
    print(f"Variance théorique à T : {theoretical_var[-1]:.4f}")
    print(f"Variance empirique à T : {empirical_var[-1]:.4f}")
    print(f"Erreur relative : {rel_error_var_final * 100:.2f} %")
    print()
    print("Écart-type final :")
    print(f"Écart-type théorique : {theoretical_std_final:.4f}")
    print(f"Écart-type empirique : {empirical_std_final:.4f}")
    print()
    print("Limite structurelle du modèle arithmétique :")
    print(
        "Proportion de trajectoires finissant à un prix négatif : "
        f"{negative_price_probability * 100:.3f} %"
    )
    print(
        "Cette limite sera plus tard corrigée par les modèles à prix positifs, "
        "notamment le mouvement brownien géométrique."
    )

    figure_path = save_figure(
        t_grid=t_grid,
        paths=paths,
        mean_path=mean_path,
        empirical_var=empirical_var,
        theoretical_var=theoretical_var,
    )

    print()
    print(f"Figure enregistrée : {figure_path}")


if __name__ == "__main__":
    main()
