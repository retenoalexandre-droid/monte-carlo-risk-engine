# 🎲 Moteur Quantitatif : Audit de Risque (Monte Carlo) & Optimisation d'Allocation (Markowitz)

## 1. Le Cas d'Usage (Business Case)
Dans le cadre de la gestion institutionnelle des risques financiers, ce projet déploie une suite quantitative en deux volets pour évaluer et maîtriser l'incertitude future d'un portefeuille boursier.

* **Module 1 - L'Optimisation (La Théorie Moderne du Portefeuille) :** Avant de subir le risque, le système détermine l'allocation de capital mathématiquement parfaite entre plusieurs actifs décorrélés pour maximiser le rendement par unité de risque.
* **Module 2 - L'Audit (Le Moteur de Monte Carlo) :** Une fois l'allocation optimale trouvée, le système simule des milliers de trajectoires futures pour évaluer le risque extrême (*Tail Risk*) sur un horizon de 30 jours, extrayant les métriques réglementaires clés : la **Value at Risk (VaR)** et l'**Expected Shortfall (ES)**.

## 2. Architecture Mathématique et Financière
Ce moteur s'appuie sur la vectorisation matricielle d'équations probabilistes et statistiques, évitant les boucles informatiques classiques pour des performances institutionnelles :

* **Matrice de Covariance & Forme Quadratique :** Évaluation du risque d'un portefeuille ($\sigma_p$) non pas comme une moyenne, mais via l'équation $\sigma_p = \sqrt{W^T \cdot \Sigma \cdot W}$ pour exploiter l'annulation organique du risque via la diversification.
* **Ratio de Sharpe :** Implémentation de la fonction de maximisation $\frac{\mu_p - R_f}{\sigma_p}$ pour isoler mathématiquement le portefeuille optimal (Prime de risque).
* **Processus Stochastique :** Génération de 10 000 trajectoires futures possibles ($N = 10 000$) modélisées selon une distribution normale paramétrée sur la volatilité historique et l'espérance du portefeuille.

## 3. Data Visualisation : La Frontière Efficiente
L'optimiseur génère par force brute 10 000 portefeuilles virtuels avec des pondérations aléatoires et les projette sur un plan cartésien (Risque / Rendement). Le modèle graphique identifie automatiquement les deux points cardinaux de la finance :
* **Le Portefeuille de Tangence (Max Sharpe) :** L'allocation offrant la rentabilité absolue la plus élevée pour le risque pris.
* **Le Portefeuille de Sécurité Absolue (Global Minimum Variance) :** Le point extrême de la frontière où les covariances écrasent la volatilité à son niveau le plus bas possible.

## 4. Stack Technique
* **Python 3** : Langage cœur.
* **NumPy** : Cœur du réacteur stochastique (génération de nombres pseudo-aléatoires) et algèbre linéaire (produits scalaires et matriciels).
* **Pandas** : Ingénierie des données temporelles, calculs de rendements vectorisés et matrices de corrélation.
* **Matplotlib** : Visualisation spatiale des nuages de points (Frontière Efficiente) et du faisceau de trajectoires Monte Carlo.
* **yfinance** : Connexion API pour l'extraction dynamique de 10 ans de données historiques du marché en temps réel.

## 5. Analyse Critique & Limites du Modèle (Reality Check)
En ingénierie financière, la robustesse d'un modèle stochastique dépend intégralement de la qualité des données d'entrée (*Garbage In, Garbage Out*).

**Le Biais de l'Horizon Temporel :**
Lors des phases de test, alimenter le modèle avec des données issues exclusivement de périodes de *Bull Market* générait des espérances ($\mu$) biaisées, faussant l'évaluation de la VaR. 

**La Résilience du Pipeline :**
Pour modéliser le véritable risque systémique, le pipeline d'extraction est calibré pour aspirer **10 années de données historiques** (env. 2500 jours de bourse). Cette profondeur intègre mécaniquement les "Cygnes Noirs" macroéconomiques (krach de 2020, chocs d'inflation de 2022). Le paramètre $\sigma$ capture ainsi la véritable variance extrême, transformant ce modèle en un outil d'audit institutionnel réaliste.