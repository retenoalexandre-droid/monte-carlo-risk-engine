#  Moteur d'Audit de Risque Stochastique (Monte Carlo)

## 1. Le Cas d'Usage (Business Case)
Dans le cadre de la gestion des risques financiers, l'évaluation de la perte potentielle maximale d'un portefeuille ne peut se limiter à l'observation des rendements passés. Ce projet implémente un **Moteur de Monte Carlo** conçu pour simuler l'incertitude future. 

L'objectif est d'évaluer le risque extrême (*Tail Risk*) d'un portefeuille boursier diversifié (ex: Couverture industrielle via un actif Automobile et un actif Minier) sur un horizon de 30 jours, en extrayant des métriques réglementaires standard : la **Value at Risk (VaR)** et l'**Expected Shortfall (ES)**.

## 2. Architecture Mathématique et Financière
Ce moteur ne repose pas sur des boucles itératives informatiques, mais sur la vectorisation matricielle d'équations probabilistes :

* **Matrice de Covariance et Diversification :** Calcul du coefficient de corrélation linéaire de Pearson ($\rho$) entre les actifs pour auditer la réalité de la couverture de risque (neutralisation directionnelle).
* **Processus Stochastique :** Génération de 10 000 trajectoires futures possibles ($N = 10 000$) sur un horizon temporel donné ($T = 30$). Les chocs quotidiens sont modélisés selon une distribution normale paramétrée sur la volatilité historique ($\sigma$) et l'espérance ($\mu$) du portefeuille.
* **Extraction des Quantiles :** Isolat de la distribution finale simulée pour déterminer la ligne de démarcation du 5ème centile (VaR 95%) et calcul de l'espérance conditionnelle des pertes au-delà de ce seuil (Expected Shortfall).

## 3. Stack Technique
L'architecture est construite pour garantir des performances d'exécution instantanées sur de larges volumes de données :
* **Python 3** : Langage cœur.
* **NumPy** : Cœur du réacteur stochastique (génération de nombres pseudo-aléatoires et opérations sur les vecteurs finaux).
* **Pandas** : Ingénierie des données temporelles, calculs de rendements vectorisés (`.pct_change()`) et matrices de corrélation (`.corr()`).
* **Matplotlib** : Visualisation spatiale des trajectoires simulées (le "faisceau" de Monte Carlo) et de la distribution des risques.
* **yfinance** : Connexion API pour l'extraction dynamique des données historiques du marché en temps réel, garantissant un modèle toujours à jour sans gestion de fichiers CSV statiques.

## 4. Analyse Critique & Limites du Modèle (Reality Check)
En ingénierie financière, la robustesse d'un modèle stochastique dépend intégralement de la qualité des données d'entrée (principe du *Garbage In, Garbage Out*).

**Le Biais de l'Horizon Temporel :**
Lors des premiers tests, le modèle a été alimenté avec un mois de données historiques situé en période de marché haussier (Bull Market). Le paramètre $\mu$ (espérance) artificiellement élevé a généré une VaR positive (illusion de l'absence de risque). 

**La Correction Implémentée :**
Pour modéliser le véritable risque systémique, le pipeline d'extraction API (`yfinance`) est désormais calibré pour aspirer **10 années de données historiques** (env. 2500 jours de bourse). Cette profondeur intègre mécaniquement les "Cygnes Noirs" macroéconomiques (krach de 2020, chocs d'inflation de 2022). Le paramètre $\sigma$ capture ainsi la véritable variance extrême, transformant ce modèle théorique en un outil d'audit de risque institutionnel réaliste, affichant la vulnérabilité réelle du portefeuille en cas de crise majeure.