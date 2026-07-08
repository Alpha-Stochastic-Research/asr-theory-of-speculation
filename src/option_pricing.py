"""
Reproduction de la formule de pricing d'options de Bachelier (1900).

Sous le modèle arithmétique P_T = P_0 + sigma * sqrt(T) * Z,  Z ~ N(0,1),
le prix d'un call européen de strike K est :

    C = (P_0 - K) * N(d) + sigma * sqrt(T) * phi(d)      avec  d = (P_0 - K) / (sigma * sqrt(T))

où N est la CDF normale standard et phi la densité normale standard.

C'est la toute première formule fermée de pricing d'options de l'histoire,
70 ans avant Black-Scholes-Merton (1973).

On vérifie :
1. La formule fermée contre un pricing Monte Carlo indépendant.
2. Que le prix scale bien en sqrt(T) (résultat central de Bachelier).
3. La convergence vers Black-Scholes quand la volatilité relative est petite
   (les deux modèles doivent quasiment coïncider pour des options ATM à faible vol).
"""

import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

rng = np.random.default_rng(7)


def bachelier_call(P0, K, sigma, T):
    """Formule fermée de Bachelier (1900) pour un call européen."""
    if T <= 0:
        return max(P0 - K, 0.0)
    d = (P0 - K) / (sigma * np.sqrt(T))
    return (P0 - K) * norm.cdf(d) + sigma * np.sqrt(T) * norm.pdf(d)


def bachelier_call_montecarlo(P0, K, sigma, T, n_paths=2_000_000):
    """Vérification indépendante par simulation Monte Carlo."""
    Z = rng.standard_normal(n_paths)
    P_T = P0 + sigma * np.sqrt(T) * Z
    payoff = np.maximum(P_T - K, 0.0)
    return payoff.mean(), payoff.std() / np.sqrt(n_paths)  # prix, erreur standard


def black_scholes_call(S0, K, vol, T, r=0.0):
    """Black-Scholes (1973) pour comparaison, mouvement brownien géométrique."""
    if T <= 0:
        return max(S0 - K, 0.0)
    d1 = (np.log(S0 / K) + 0.5 * vol**2 * T) / (vol * np.sqrt(T))
    d2 = d1 - vol * np.sqrt(T)
    return S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


# --- 1. Formule fermée vs Monte Carlo ---
P0, K, sigma, T = 100.0, 100.0, 2.0, 1.0
closed_form = bachelier_call(P0, K, sigma, T)
mc_price, mc_se = bachelier_call_montecarlo(P0, K, sigma, T)

print("=== Vérification de la formule de Bachelier (1900) pour un call ATM ===")
print(f"P0={P0}, K={K}, sigma={sigma}, T={T}")
print(f"Prix formule fermée de Bachelier : {closed_form:.6f}")
print(f"Prix Monte Carlo (2M tirages)     : {mc_price:.6f}  (erreur standard ±{mc_se:.6f})")
print(f"Écart                             : {abs(closed_form - mc_price):.6f}")

# --- 2. Scaling en sqrt(T) ---
T_grid = np.linspace(0.05, 4, 50)
prices_atm = [bachelier_call(P0, P0, sigma, t) for t in T_grid]  # option ATM : d=0
theoretical_atm = sigma * np.sqrt(T_grid) * norm.pdf(0)  # pour d=0, prix = sigma*sqrt(T)*phi(0)

print("\n=== Vérification du scaling en sqrt(T) (option ATM, K=P0) ===")
print("Pour K=P0, la formule se réduit exactement à C = sigma * sqrt(T) * phi(0).")
print(f"Erreur max entre la formule générale et la forme simplifiée sqrt(T) : "
      f"{np.max(np.abs(np.array(prices_atm) - theoretical_atm)):.2e}")

# --- 3. Comparaison avec Black-Scholes ---
# Pour rapprocher les deux modèles, on choisit une vol géométrique telle que
# vol_BS * S0 ≈ sigma (approximation locale autour de S0), à faible vol.
S0 = 100.0
vol_bs = 0.02  # 2% -> sigma_arithmétique équivalent ≈ vol_bs * S0 = 2.0 (cohérent avec sigma ci-dessus)
sigma_equiv = vol_bs * S0

K_grid = np.linspace(80, 120, 41)
bach_prices = [bachelier_call(S0, k, sigma_equiv, T) for k in K_grid]
bs_prices = [black_scholes_call(S0, k, vol_bs, T) for k in K_grid]
max_diff = np.max(np.abs(np.array(bach_prices) - np.array(bs_prices)))

print("\n=== Comparaison Bachelier (1900) vs Black-Scholes (1973) ===")
print(f"Volatilité géométrique BS = {vol_bs*100:.1f}%  ->  sigma arithmétique équivalent = {sigma_equiv:.2f}")
print(f"Écart de prix max sur la nappe de strikes [80,120] : {max_diff:.4f}")
print("(les deux modèles coïncident quasiment à faible volatilité, ce qui est attendu :")
print(" Black-Scholes redevient localement gaussien/arithmétique près de S0)")

# --- Figures ---
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

ax = axes[0]
ax.plot(T_grid, prices_atm, lw=2, color="tab:blue")
ax.set_xlabel("T (maturité)")
ax.set_ylabel("Prix du call ATM")
ax.set_title(r"Prix de l'option scale en $\sqrt{T}$" + "\n" + r"$C_{ATM} = \sigma\sqrt{T}\,\phi(0)$")

ax = axes[1]
ax.plot(K_grid, bach_prices, lw=2, label="Bachelier (1900)")
ax.plot(K_grid, bs_prices, "--", lw=2, label="Black-Scholes (1973)")
ax.set_xlabel("Strike K")
ax.set_ylabel("Prix du call")
ax.set_title("Bachelier vs Black-Scholes\n(faible volatilité, même sigma effectif)")
ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig("figures/fig2_option_pricing.png", dpi=160)
print("\nFigure enregistrée : figures/fig2_option_pricing.png")
