import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf  # <-- Le nouvel outil d'extraction

print("--- ASPIRATION DES DONNÉES SUR 10 ANS EN COURS ---")
# 1. On demande à l'API de télécharger les prix de clôture ('Close') de nos deux actifs
donnees_brutes = yf.download(["STLA", "VALE"], start="2016-06-28", end="2026-06-28")['Close']

# 2. Création du portefeuille
portefeuille = pd.DataFrame({
    'Automobile': donnees_brutes['STLA'],
    'Mine': donnees_brutes['VALE']
}).dropna()

# --- LE RESTE DE TON CODE NE CHANGE PAS ---
# 3. Calcul des rendements...
rendements = portefeuille.pct_change().dropna()


print("--- APERÇU DES RENDEMENTS DU PORTEFEUILLE ---")
print(rendements.head())

# 4. LE CŒUR DU RÉACTEUR : La Matrice de Corrélation
matrice_correlation = rendements.corr()

print("\n--- MATRICE DE CORRÉLATION DE PEARSON ---")
print(matrice_correlation)

print("\n--- INITIALISATION DU MOTEUR DE MONTE CARLO ---")

# 1. Création du vecteur de rendement du portefeuille global (50/50)
rendements_portefeuille = (rendements['Automobile'] * 0.5) + (rendements['Mine'] * 0.5)

# 2. Paramétrage des probabilités (Loi Normale)
mu = rendements_portefeuille.mean() # L'espérance (La tendance centrale)
sigma = rendements_portefeuille.std() # L'écart-type (La volatilité globale)
jours_a_simuler = 30
nombre_de_scenarios = 10000

print(f"Simulation de {nombre_de_scenarios} univers parallèles sur {jours_a_simuler} jours...")

# 3. Le Cœur du Réacteur : La Génération Matricielle
# On génère une matrice (30 lignes x 10000 colonnes) de tirages aléatoires normaux
chocs_quotidiens = np.random.normal(mu, sigma, (jours_a_simuler, nombre_de_scenarios))

# 4. Calcul des trajectoires (On part d'un capital de 100€)
capital_initial = 100
# La fonction cumprod() applique le mécanisme des intérêts composés sur chaque scénario
trajectoires_prix = capital_initial * np.cumprod(1 + chocs_quotidiens, axis=0)

# 5. Visualisation des Futurs (On n'affiche que 100 scénarios pour ne pas faire planter l'écran)
plt.figure(figsize=(10, 6))
plt.plot(trajectoires_prix[:, :100], alpha=0.5)
plt.title("Monte Carlo : 100 Trajectoires Possibles du Portefeuille sur 30 Jours")
plt.xlabel("Jours")
plt.ylabel("Valeur du Portefeuille (€)")
plt.axhline(y=capital_initial, color='black', linestyle='dashed', linewidth=2, label="Capital Initial (100€)")
plt.legend()
plt.show()

print("\n--- EXTRACTION DE LA VaR MONTE CARLO ---")

# 1. Isoler la dernière ligne (le 30ème jour) pour les 10 000 scénarios
prix_finaux = trajectoires_prix[-1]

# 2. Transformer ces 10 000 prix finaux en rendements (%)
# Formule classique : (Valeur Finale - Valeur Initiale) / Valeur Initiale
rendements_finaux = (prix_finaux - capital_initial) / capital_initial

# 3. Extraire la ligne rouge (Le Quantile à 5%)
# Note: Puisque nous utilisons NumPy et non Pandas ici, la fonction est np.percentile()
var_mc_95 = np.percentile(rendements_finaux, 5)

print(f"Pire scénario attendu à 30 jours (VaR 95%) : {var_mc_95 * 100:.2f} %")

# 4. (Bonus de l'Actuaire) L'Expected Shortfall de Monte Carlo
# On isole les scénarios pires que la VaR et on fait la moyenne
es_mc_95 = rendements_finaux[rendements_finaux <= var_mc_95].mean()
print(f"Moyenne du crash en cas de crise extrême (ES 95%) : {es_mc_95 * 100:.2f} %")