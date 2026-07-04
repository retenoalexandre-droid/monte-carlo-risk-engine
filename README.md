# 🎲 Moteur Quantitatif : Audit de Risque (Monte Carlo) & Optimisation d'Allocation (Markowitz)

## 1. Le Cas d'Usage (Business Case)
Dans le cadre de la gestion institutionnelle des risques financiers, ce projet déploie une suite quantitative en deux volets pour évaluer et maîtriser l'incertitude future d'un portefeuille boursier.

* **Module 1 - L'Optimisation (Markowitz) :** Détermine l'allocation de capital mathématiquement parfaite entre plusieurs actifs décorrélés pour maximiser le rendement par unité de risque (Frontière Efficiente).
* **Module 2 - L'Audit (Monte Carlo) :** Simule des milliers de trajectoires futures basées sur l'allocation optimale pour évaluer le risque extrême (*Tail Risk*) sur 30 jours, extrayant la **Value at Risk (VaR)** et l'**Expected Shortfall (ES)**.

## 2. Architecture Data & Pipeline ETL (Découplage)
Pour garantir une intégration fluide avec des outils de Business Intelligence (BI) et de reporting, l'architecture repose sur un pipeline de données automatisé et découplé :
1. **Extract & Transform :** L'optimiseur extrait les données de marché, calcule la matrice de covariance, identifie les pondérations idéales et les exporte dans une table de dimension (`dim_allocation_actifs.csv`).
2. **Load (Data Mart) :** Le moteur stochastique ingère dynamiquement cette dimension, exécute le stress test vectoriel, et historise les métriques de risque quotidiennes dans une table de faits incrémentale (`fait_risque_quotidien.csv`).
Ce format en étoile (modélisation dimensionnelle) permet une ingestion directe et optimisée pour la création de mesures dynamiques (DAX) dans des tableaux de bord institutionnels.

## 3. Architecture Mathématique
* **Forme Quadratique :** Évaluation du risque $\sigma_p = \sqrt{W^T \cdot \Sigma \cdot W}$ pour exploiter l'annulation organique du risque via la covariance.
* **Ratio de Sharpe :** Maximisation de la fonction $\frac{\mu_p - R_f}{\sigma_p}$ pour isoler le portefeuille de tangence.
* **Processus Stochastique :** Génération matricielle de 10 000 trajectoires futures ($N = 10 000$) modélisées sur la distribution normale des rendements historiques.

## 4. Stack Technique
* **Python 3** : Langage cœur de l'ETL et de la modélisation.
* **NumPy / Pandas** : Algèbre linéaire, calcul stochastique, vectorisation matricielle et manipulation des DataFrames.
* **Matplotlib** : Visualisation spatiale (Frontière Efficiente, faisceau stochastique).
* **yfinance** : Connexion API pour l'aspiration dynamique en temps réel de 10 ans d'historique de marché.

## 5. Limites du Modèle (Reality Check)
Pour éviter le biais de l'horizon temporel (calcul d'espérance faussé par des périodes de *Bull Market* exclusives), le pipeline exige une profondeur de 10 années de données (env. 2500 jours de bourse). Cette rigueur permet au paramètre $\sigma$ de capturer la véritable variance extrême incluant les chocs macroéconomiques majeurs, garantissant une VaR réaliste.