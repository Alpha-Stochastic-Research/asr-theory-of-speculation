"""
Reproduction du modèle de Bachelier (1900) : marche aléatoire arithmétique.

Bachelier modélise le prix P_t comme :
    P_t = P_0 + sigma * W_t
où W_t est un mouvement brownien standard (processus de Wiener).

Deux résultats du papier sont testés ici :
1. E[P_t] = P_0 pour tout t  (« l'espérance mathématique du spéculateur est nulle »)
2. Var[P_t] = sigma^2 * t     (la dispersion croit comme sqrt(t), pas comme t)
"""

import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)

P0 = 100.0          # prix initial
sigma = 2.0          # volatilité arithmétique (unités de prix / sqrt(temps))
T = 1.0              # horizon (1 "année" de négociation)
n_steps = 250        # ~ nombre de séances de bourse
n_paths = 5000       # nombre de trajectoires simulées

dt = T / n_steps
t_grid = np.linspace(0, T, n_steps + 1)

# --- Simulation Monte Carlo de la marche aléatoire arithmétique ---
increments = rng.normal(loc=0.0, scale=sigma * np.sqrt(dt), size=(n_paths, n_steps))
paths = np.concatenate([np.full((n_paths, 1), P0), P0 + np.cumsum(increments, axis=1)], axis=1)

# --- Vérification empirique du résultat 1 : martingale (espérance nulle des gains) ---
mean_path = paths.mean(axis=0)
max_dev = np.max(np.abs(mean_path - P0))

# --- Vérification empirique du résultat 2 : Var[P_t] = sigma^2 * t ---
empirical_var = paths.var(axis=0)
theoretical_var = sigma**2 * t_grid

rel_error_var_final = abs(empirical_var[-1] - theoretical_var[-1]) / theoretical_var[-1]

print("=== Vérification des résultats de Bachelier (1900) ===")
print(f"Écart max entre E[P_t] simulé et P_0 (doit être proche de 0)  : {max_dev:.4f}")
print(f"Variance théorique à t=T  (sigma^2 * T)                        : {theoretical_var[-1]:.4f}")
print(f"Variance empirique à t=T (Monte Carlo, {n_paths} trajectoires) : {empirical_var[-1]:.4f}")
print(f"Erreur relative                                                 : {rel_error_var_final*100:.2f} %")
print(f"Écart-type des prix à t=T (théorique = sigma*sqrt(T))          : {sigma*np.sqrt(T):.4f}")
print(f"Écart-type des prix à t=T (empirique)                          : {np.std(paths[:, -1]):.4f}")

# --- Figure 1 : trajectoires + enveloppe sigma*sqrt(t) ---
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

ax = axes[0]
for i in range(60):
    ax.plot(t_grid, paths[i], lw=0.6, alpha=0.5)
ax.plot(t_grid, mean_path, color="black", lw=2, label=r"$E[P_t]$ empirique")
ax.axhline(P0, color="red", ls="--", lw=1, label=r"$P_0$")
ax.plot(t_grid, P0 + sigma * np.sqrt(t_grid), color="blue", ls=":", lw=1.5,
        label=r"$P_0 \pm \sigma\sqrt{t}$")
ax.plot(t_grid, P0 - sigma * np.sqrt(t_grid), color="blue", ls=":", lw=1.5)
ax.set_xlabel("t")
ax.set_ylabel(r"$P_t$")
ax.set_title("Marche aléatoire arithmétique (Bachelier 1900)\n60 trajectoires simulées")
ax.legend(fontsize=8)

ax = axes[1]
ax.plot(t_grid, empirical_var, label="Variance empirique", lw=2)
ax.plot(t_grid, theoretical_var, "--", label=r"Variance théorique $\sigma^2 t$", lw=2)
ax.set_xlabel("t")
ax.set_ylabel(r"Var$[P_t]$")
ax.set_title("Croissance linéaire de la variance\n(donc écart-type en $\\sqrt{t}$)")
ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig("figures/fig1_random_walk_martingale.png", dpi=160)
print("\nFigure enregistrée : figures/fig1_random_walk_martingale.png")

# --- Probabilité de prix négatif (limite connue du modèle) ---
neg_prob = (paths[:, -1] < 0).mean()
print(f"\nProportion de trajectoires finissant à un prix négatif à t=T : {neg_prob*100:.3f} %")
print("(illustre la limite structurelle du modèle arithmétique de Bachelier,")
print(" corrigée en 1965 par Samuelson via le mouvement brownien géométrique)")
