import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# 1. Sélection de 4 actifs totalement décorrélés pour maximiser l'efficacité
# AAPL (Tech), GLD (Or), TLT (Obligations du Trésor), JPM (Banque)
tickers = ['AAPL', 'GLD', 'TLT', 'JPM']
print(f"--- ASPIRATION DES DONNÉES HISTORIQUES POUR {tickers} ---")

# On extrait 10 ans de données et on calcule directement les rendements quotidiens
donnees = yf.download(tickers, start="2016-06-28", end="2026-06-28")['Close']
rendements = donnees.pct_change().dropna()

# 2. Précalculs Algébriques Annuels (Il y a 252 jours de bourse dans une année)
rendements_moyens = rendements.mean() * 252
matrice_covariance = rendements.cov() * 252
taux_sans_risque = 0.02 # On suppose 2% de rendement sans risque

print("--- GÉNÉRATION DE 10 000 PORTEFEUILLES VIRTUELS ---")
nombre_portefeuilles = 10000

# Matrices pour stocker les resultats de nos 10 000 univers
resultats = np.zeros((3, nombre_portefeuilles))
poids_enregistres = []

for i in range(nombre_portefeuilles):
    # Génération d'un vecteur de poids aléatoires W
    poids = np.random.random(len(tickers))
    poids = poids / np.sum(poids) # Normalisation pour que la somme fasse 1 (100%)
    poids_enregistres.append(poids)
    
    # Rendement attendu (Produit scalaire)
    rendement_p = np.sum(rendements_moyens * poids)
    
    # Volatilité (Forme quadratique : W^T * Sigma * W)
    volatilite_p = np.sqrt(np.dot(poids.T, np.dot(matrice_covariance, poids)))
    
    # Ratio de Sharpe
    sharpe_p = (rendement_p - taux_sans_risque) / volatilite_p
    
    # Stockage des scalaires
    resultats[0, i] = volatilite_p
    resultats[1, i] = rendement_p
    resultats[2, i] = sharpe_p

# 3. Extraction du Portefeuille Optimal (Le Saint Graal)
# On cherche l'index (la position) du plus grand Ratio de Sharpe dans notre matrice
index_optimal = np.argmax(resultats[2])
poids_optimaux = poids_enregistres[index_optimal]

print("\n=== L'ALLOCATION ABSOLUE (MAX SHARPE) ===")
print(f"Rendement Attendu : {resultats[1, index_optimal]*100:.2f} %")
print(f"Volatilité (Risque) : {resultats[0, index_optimal]*100:.2f} %")
print(f"Ratio de Sharpe : {resultats[2, index_optimal]:.2f}")
print("\nPondérations à appliquer :")
for i in range(len(tickers)):
    print(f"- {tickers[i]} : {poids_optimaux[i]*100:.2f} %")

print("\n--- GÉNÉRATION DE LA FRONTIÈRE EFFICIENTE (VISUALISATION) ---")

# 1. Recalcul des deux points cardinaux (Index)
idx_max_sharpe = np.argmax(resultats[2])
idx_min_vol = np.argmin(resultats[0])

# 2. Configuration de la toile spatiale
plt.figure(figsize=(12, 8))

# 3. Le Nuage de Points (Les 10 000 univers)
# On multiplie par 100 pour afficher des pourcentages clairs
# c=resultats[2] demande à Python de colorer les points selon leur Ratio de Sharpe (la "température" du profit)
nuage = plt.scatter(resultats[0, :] * 100, resultats[1, :] * 100, c=resultats[2, :], cmap='viridis', marker='o', s=10, alpha=0.5)
plt.colorbar(nuage, label='Ratio de Sharpe')

# 4. Le Viseur Rouge : Le Portefeuille Optimal (Maximum Sharpe)
plt.scatter(resultats[0, idx_max_sharpe] * 100, resultats[1, idx_max_sharpe] * 100, color='red', marker='*', s=400, edgecolor='black', label='Maximum Sharpe (Rendement Optimal)')

# 5. Le Viseur Bleu : Le Bouclier Absolu (Minimum Variance)
plt.scatter(resultats[0, idx_min_vol] * 100, resultats[1, idx_min_vol] * 100, color='blue', marker='*', s=400, edgecolor='black', label='Sécurité Absolue (Minimum Volatilité)')

# 6. Esthétique, Titres et Grille de lecture
plt.title("Frontière Efficiente de Markowitz (10 000 Portefeuilles Simulés)", fontsize=14, fontweight='bold')
plt.xlabel("Risque : Volatilité Annualisée (%)", fontsize=12)
plt.ylabel("Rendement Espéré Annualisé (%)", fontsize=12)
plt.legend(loc='best', fontsize=11)
plt.grid(True, linestyle='--', alpha=0.7)

# Lancement de l'interface
plt.show()