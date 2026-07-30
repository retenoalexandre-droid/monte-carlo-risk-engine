import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import datetime
import os

print("--- LECTURE DU DATA MART (DIMENSION ALLOCATION) ---")
# 1. Le script ingère le fichier pont généré par l'optimiseur
try:
    df_alloc = pd.read_csv("dim_allocation_actifs.csv", sep=';')
except FileNotFoundError:
    print("Erreur : Fichier d'allocation introuvable. Exécutez l'optimiseur d'abord.")
    exit()

# 2. Extraction vectorielle des paramètres
tickers = df_alloc['Ticker'].tolist()
# Reconversion des pourcentages en poids décimaux (ex: 33.35 -> 0.3335)
poids = df_alloc['Poids_Pct'].values / 100 
type_opti = df_alloc['Type_Optimisation'].iloc[0]

print(f"Univers d'investissement détecté : {tickers}")
print(f"Vecteur de pondérations (W) : {poids}")

print("\n--- ASPIRATION DYNAMIQUE DES DONNÉES SUR 10 ANS ---")
# Calcul dynamique des dates (Aujourd'hui - 10 ans)
date_fin = datetime.datetime.now()
date_debut = date_fin - datetime.timedelta(days=3652) # 10 ans + années bissextiles

donnees_brutes = yf.download(tickers, start=date_debut.strftime("%Y-%m-%d"), end=date_fin.strftime("%Y-%m-%d"))['Close']

# Sécurisation vitale : forcer l'ordre des colonnes pour qu'il corresponde exactement au vecteur de poids
donnees_brutes = donnees_brutes[tickers]
rendements = donnees_brutes.pct_change().dropna()

print("\n--- INITIALISATION DU MOTEUR DE MONTE CARLO ---")
# 3. Calcul du rendement quotidien du portefeuille 
# La somme vectorielle des (rendements de chaque actif * leur poids respectif)
rendements_portefeuille = (rendements * poids).sum(axis=1)

mu = rendements_portefeuille.mean()
sigma = rendements_portefeuille.std()
jours_a_simuler = 30
nombre_de_scenarios = 10000

print(f"Lancement de {nombre_de_scenarios} trajectoires stochastiques sur {jours_a_simuler} jours...")
chocs_quotidiens = np.random.normal(mu, sigma, (jours_a_simuler, nombre_de_scenarios))
capital_initial = 100
trajectoires_prix = capital_initial * np.cumprod(1 + chocs_quotidiens, axis=0)

# Affichage du faisceau (Mode Audit Visuel)
plt.figure(figsize=(10, 6))
plt.plot(trajectoires_prix[:, :100], alpha=0.5)
plt.title(f"Monte Carlo : 100 Trajectoires du Portefeuille [{type_opti}]")
plt.xlabel("Jours")
plt.ylabel("Valeur du Portefeuille (€)")
plt.axhline(y=capital_initial, color='black', linestyle='dashed', linewidth=2)
plt.show()

print("\n--- EXTRACTION DES MÉTRIQUES DE RISQUE ---")
prix_finaux = trajectoires_prix[-1]
rendements_finaux = (prix_finaux - capital_initial) / capital_initial

var_mc_95 = np.percentile(rendements_finaux, 5)
es_mc_95 = rendements_finaux[rendements_finaux <= var_mc_95].mean()

print(f"Pire scénario attendu (VaR 95%) : {var_mc_95 * 100:.2f} %")
print(f"Moyenne du crash (ES 95%) : {es_mc_95 * 100:.2f} %")

print("\n--- EXPORT ETL : TABLE DE FAITS ---")
# 4. Modélisation de la donnée pour l'outil de Business Intelligence
date_jour = datetime.datetime.now().strftime("%Y-%m-%d")

fait_risque = {
    "Date_Calcul": date_jour,
    "Type_Optimisation": type_opti,
    "Rendement_Journalier_Moyen_Pct": round(mu * 100, 4),
    "Volatilite_Journaliere_Pct": round(sigma * 100, 4),
    "Value_at_Risk_95_Pct": round(var_mc_95 * 100, 2),
    "Expected_Shortfall_Pct": round(es_mc_95 * 100, 2)
}

df_fait = pd.DataFrame([fait_risque])

# Le mode 'a' (append) ajoute la nouvelle ligne sans effacer l'historique des jours précédents
fichier_fait = "fait_risque_quotidien.csv"
entete = not os.path.exists(fichier_fait)
df_fait.to_csv(fichier_fait, mode='a', header=entete, index=False, sep=';')

print(f"Succès : Les métriques de risque ont été injectées dans la table '{fichier_fait}'.")

#creer un fichier reunissant les 100000 trajectoires

fait_trajectoire = {
    "Rendement": rendements_finaux
} 

df_fait= pd.DataFrame(fait_trajectoire)

fichier_trajectoire = "distribution_stochastique.csv"
#entete = not os.path.exists(fichier_trajectoire)
df_fait.to_csv(fichier_trajectoire, sep = ';')