ORDRE D'EXÉCUTION : MATRICE DE CORRÉLATION (Session de Demain, 17h00)Objectif : Aligner deux vecteurs financiers et calculer leur coefficient de corrélation linéaire ($\rho$) pour auditer la diversification du portefeuille.Contrainte de Temps : 45 minutes strictes.
ÉTAPE 1 : ACQUISITION (0 - 10 min)
Télécharge les deux fichiers CSV (ex: auto.csv et mine.csv).
Assure-toi qu'ils couvrent la même période de temps.
ÉTAPE 2 : INJECTION DU CODE MATRICIEL (10 - 25 min)
Crée un nouveau script portfolio_risk.py et insère cette architecture :
Pythonimport pandas as pd

# 1. Chargement des deux matrices (on utilise 'Date' comme index pour bien les aligner)
df_auto = pd.read_csv('auto.csv', index_col='Date', parse_dates=True)
df_mine = pd.read_csv('mine.csv', index_col='Date', parse_dates=True)

# 2. Création de la matrice "Portefeuille" (Fusion des deux vecteurs de prix)
portefeuille = pd.DataFrame({
    'Automobile': df_auto['Close'], 
    'Mine': df_mine['Close']
})

# On supprime les lignes où il manque des données (jours fériés décalés, etc.)
portefeuille = portefeuille.dropna()

# 3. Calcul des rendements pour toute la matrice en une seule ligne
rendements = portefeuille.pct_change().dropna()

print("--- APERÇU DES RENDEMENTS DU PORTEFEUILLE ---")
print(rendements.head())

# 4. LE CŒUR DU RÉACTEUR : La Matrice de Corrélation
matrice_correlation = rendements.corr()

print("\n--- MATRICE DE CORRÉLATION DE PEARSON ---")
print(matrice_correlation)
ÉTAPE 3 : EXÉCUTION ET AUDIT D'ANALYSTE (25 - 45 min)Lance le script.La console va te sortir un tableau carré (une matrice $2 \times 2$).La diagonale sera composée de 1.000 (l'Automobile est parfaitement corrélée à 100% avec elle-même, logique).Ta vraie cible : Regarde le chiffre hors de la diagonale. S'il est proche de $0$, tes actifs sont indépendants. S'il est négatif, ta stratégie de couverture en fer a fonctionné de manière spectaculaire.ÉTAPE 4 : FERMETURE (Hard Stop)À la 45ème minute, coupure totale. Fermeture de VSCode.Quitte la Zone de Commandement.

27/06/2026
ORDRE D'EXÉCUTION : LE MOTEUR DE MONTE CARLO (Session de Demain, 17h00)
Objectif : Utiliser les lois des probabilités pour simuler 10 000 trajectoires futures possibles sur 30 jours et visualiser l'incertitude de ton portefeuille imparfait.
Contrainte de Temps : 45 minutes strictes.

ÉTAPE 1 : IMPORTATION DU GÉNÉRATEUR ALÉATOIRE
Nous allons avoir besoin d'une nouvelle bibliothèque mathématique : numpy. Elle est spécialisée dans les calculs matriciels complexes et la génération de hasard.
En haut de ton script portfolio_risk.py, ajoute :

Python
import numpy as np
import matplotlib.pyplot as plt
ÉTAPE 2 : INJECTION DU MOTEUR STOCHASTIQUE
À la suite de ton code d'hier (sous le print de la matrice de corrélation), insère cette architecture. Nous allons simuler un portefeuille composé à 50% d'Auto et 50% de Mine.

Python
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
ÉTAPE 3 : EXÉCUTION ET AUDIT VISUEL
Lance le script.

Observe le graphique. Tu ne verras plus une ligne du passé, mais un "faisceau" de lignes qui s'évase vers la droite, représentant tous les futurs possibles de tes 100 €.

Certaines lignes s'envoleront, d'autres plongeront sous ton capital initial. C'est la matérialisation visuelle du hasard (le mouvement brownien).

ÉTAPE 4 : FERMETURE (Hard Stop)
À la 45ème minute, coupure totale.

Fermeture de VSCode.

Activation du repos passif.