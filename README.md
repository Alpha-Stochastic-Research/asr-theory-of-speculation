# Bachelier 1900 — Reproduction

Reproduction numérique des résultats de Louis Bachelier, *Théorie de la spéculation* (1900),
et version corrigée du document LaTeX qui présente ce papier.

## Contenu du repo

```
bachelier-1900-reproduction/
├── README.md
├── requirements.txt
├── src/
│   ├── brownian_motion.py      # marche aléatoire arithmétique + martingale
│   └── option_pricing.py       # formule de pricing d'options de Bachelier
├── figures/
│   ├── fig1_random_walk_martingale.png
│   └── fig2_option_pricing.png
└── paper/
    ├── bachelier_paper_corrige.tex   # LaTeX corrigé (compile sans erreur)
    └── bachelier_paper_corrige.pdf   # PDF compilé
```

## Résultats reproduits

### 1. Propriété de martingale (`src/brownian_motion.py`)
Bachelier modélise le prix comme `P_t = P_0 + sigma * W_t`. On simule 5000
trajectoires (250 pas, sigma=2) et on vérifie :

- `E[P_t] ≈ P_0` pour tout `t` — écart max mesuré : **0.037** sur une échelle de prix ~100
  (« l'espérance mathématique du spéculateur est nulle »)
- `Var[P_t] = sigma² · t` — erreur relative mesurée : **1.56 %** (bruit Monte Carlo)
- Probabilité de prix négatif à `t=1` : **0.000 %** dans cet échantillon, mais non nulle
  analytiquement — c'est précisément la limite structurelle du modèle arithmétique

### 2. Formule de pricing d'options (`src/option_pricing.py`)
Sous le modèle de Bachelier, le prix d'un call européen est :

```
C = (P0 - K) * N(d) + sigma * sqrt(T) * phi(d),   d = (P0 - K) / (sigma * sqrt(T))
```

Vérifications effectuées :

- **Formule fermée vs Monte Carlo** (2M tirages) : écart de **0.0008**, dans l'erreur
  standard Monte Carlo (±0.0008) → formule validée
- **Scaling en `sqrt(T)`** pour une option à la monnaie (`K=P0`) : erreur numérique
  **0.00e+00** (identité exacte `C_ATM = sigma·sqrt(T)·φ(0)`)
- **Convergence vers Black-Scholes** à faible volatilité (2 %) : écart de prix max
  **0.0048** sur une nappe de strikes [80,120] → les deux modèles coïncident bien
  localement, comme attendu théoriquement

## Reproduire

```bash
pip install -r requirements.txt
python src/brownian_motion.py
python src/option_pricing.py
```

## Corrections apportées au document LaTeX

Le `.tex` d'origine ne compilait pas. Diagnostic obtenu par compilation réelle
avec `pdflatex` (pas une simple relecture) :

| # | Problème | Gravité | Correction |
|---|----------|---------|------------|
| 1 | Couleur `alertRed` utilisée dans le TikZ (Fig. 1) mais jamais définie via `\definecolor` | **Erreur fatale** — 8 occurrences de `! Package xcolor Error: Undefined color` / `! Package pgfkeys Error`, compilation impossible (`pdflatex` retourne le code 1) | Ajout de `\definecolor{alertRed}{RGB}{214,40,40}` dans le bloc de couleurs |
| 2 | Guillemets droits ASCII `"..."` utilisés à 4 endroits (`"random walk"`, la citation de Bachelier, `"fat tails"`, `"unworthy"`) | Défaut typographique — LaTeX ne convertit pas automatiquement `"` en guillemets courbes, rendu visuellement incorrect | Remplacement par les guillemets LaTeX corrects `` `` ... '' `` |

Après correction : compilation `pdflatex` propre, **0 erreur**, PDF de 2 pages généré
(vérifié par double passage `pdflatex` + inspection visuelle des pages rendues).

## Sources

- Bachelier, L. (1900). *Théorie de la spéculation*. Annales Scientifiques de l'ENS, 17, 21-86.
- Samuelson, P. A. (1965). *Rational Theory of Warrant Pricing*. Industrial Management Review, 6(2), 13-31.
