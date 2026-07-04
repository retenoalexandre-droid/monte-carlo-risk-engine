# 🎲 Moteur Quantitatif : Audit de Risque (Monte Carlo) & Optimisation d'Allocation (Markowitz)

## 1. Le Cas d'Usage (Business Case)
Dans le cadre de la gestion institutionnelle des risques financiers, ce projet déploie une suite quantitative complète pour évaluer et maîtriser l'incertitude future d'un portefeuille boursier, de l'optimisation mathématique jusqu'à la restitution visuelle.

* **Module 1 - L'Optimisation (Markowitz) :** Détermine l'allocation de capital mathématiquement parfaite entre plusieurs actifs pour maximiser le rendement par unité de risque.
* **Module 2 - L'Audit (Monte Carlo) :** Simule 10 000 trajectoires futures basées sur l'allocation optimale pour évaluer le risque extrême (*Tail Risk*) sur 30 jours, extrayant la **Value at Risk (VaR)** et l'**Expected Shortfall (ES)**.
* **Module 3 - Le Tableau de Bord (Web App) :** Restitution dynamique des métriques de risque via un serveur local interactif.

## 2. Architecture Data & Pipeline ETL (Découplage)
L'architecture repose sur un pipeline de données automatisé (*Daemon UNIX/Cron*) et découplé :
1. **Extract & Transform :** L'optimiseur Python extrait les données de marché, calcule la matrice de covariance, et exporte les pondérations idéales dans une table de dimension (`dim_allocation_actifs.csv`).
2. **Load (Data Mart) :** Le moteur stochastique ingère cette dimension, exécute le stress test vectoriel, et historise les métriques quotidiennes dans une table de faits incrémentale (`fait_risque_quotidien.csv`).
3. **Data Visualization :** L'application web Streamlit se connecte à ce schéma en étoile pour modéliser les KPIs financiers en temps réel.

## 3. Architecture Mathématique
* **Forme Quadratique :** Évaluation du risque $\sigma_p = \sqrt{W^T \cdot \Sigma \cdot W}$ pour exploiter l'annulation organique du risque.
* **Ratio de Sharpe :** Maximisation de la fonction $\frac{\mu_p - R_f}{\sigma_p}$ pour isoler le portefeuille de tangence.
* **Processus Stochastique :** Génération matricielle de scénarios futurs ($N = 10 000$) modélisés sur la distribution normale des rendements.

## 4. Stack Technique
* **Python 3** : Langage cœur de l'ETL et de la modélisation.
* **NumPy / Pandas** : Algèbre linéaire, calcul stochastique et manipulation des bases de données.
* **Streamlit** : Librairie Front-End pour la génération du tableau de bord interactif.
* **yfinance** : Connexion API pour l'aspiration dynamique en temps réel de l'historique de marché.

## 5. Industrialisation
Le pipeline est entièrement automatisé. Une tâche planifiée (Cron) réveille les algorithmes chaque soir après la clôture des marchés (23h00), recalculant de manière autonome la frontière efficiente et le risque stochastique, assurant un Data Mart perpétuellement à jour sans intervention humaine.

## 6. Guide de Déploiement (Dashboard Web)
Pour visualiser le tableau de bord interactif sur votre machine locale, une commande d'exécution spécifique est requise pour lier le module Streamlit au noyau Python.

**Prérequis :**
```bash
pip install streamlit pandas

Lancement du Serveur Local :
*Depuis la racine du projet (dans le terminal), exécutez la commande suivante (ne pas utiliser de lancement de script standard) :

```Bash
python3 -m streamlit run dashboard.py

Pour quitter le serveur local Streamlit qui tourne actuellement, vous devriez d abord appuyer sur Control + C dans le terminal.