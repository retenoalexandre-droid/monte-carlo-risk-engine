import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 


# 0,5. extractation des donnees de distribution_stochastique.csv

try:
    df_distribution = pd.read_csv("distribution_stochastique.csv", sep= ";")

except FileNotFoundError:
    st.error("Le Fichier n'existe pas, veillez d'abord lancer portfolio_risk.py")
    st.stop()

# rajouter juste le bouton qui slide

seuil_confiance = st.slider(label="Niveau de confiance", min_value=90, max_value=99, value=95, step=1, format="%d%%", help="Sélectionnez le niveau de confiance", label_visibility="visible")

st.write(f"Le niveau de confiance est : {seuil_confiance}%")

#Calcul de la var dynamique

rendements = df_distribution['Rendement']
reste_decimal_seuil_confiance = (100 - seuil_confiance)/100
var_dynamique=rendements.quantile(reste_decimal_seuil_confiance)


st.write(f"la Value At Risk dynamique est : {abs(var_dynamique*100): .2f} %")

es_dynamique = rendements[rendements <= var_dynamique].mean()

st.write(f"L'Expected Shortfall dynamique est : {abs(es_dynamique*100): .2f} %")

# 1. Configuration de la page
st.set_page_config(page_title="Risk Dashboard", layout="wide")
st.title("🛡️ Moteur de Risque Institutionnel")

# 2. Fonction d'ingestion des données avec mise en cache (pour la performance)
@st.cache_data
def charger_donnees():
    df_faits = pd.read_csv("fait_risque_quotidien.csv", sep=';')
    df_dim = pd.read_csv("dim_allocation_actifs.csv", sep=';')
    return df_faits, df_dim

# 3. Construction de l'interface
try:
    df_faits, df_dim = charger_donnees()
    st.success("Connexion au Data Mart réussie. Flux de données actif.")
    
    st.markdown("---")
    
    # Extraction de la dernière ligne (les données les plus récentes)
    derniere_ligne = df_faits.iloc[-1]
    date_maj = derniere_ligne['Date_Calcul']
    
    st.subheader(f"📊 Métriques de Risque (Dernière actualisation : {date_maj})")
    
    # Création de 3 colonnes pour afficher les KPIs à la manière d'un terminal Bloomberg
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Value at Risk (95%)", f"{-derniere_ligne['Value_at_Risk_95_Pct']} %")
    col2.metric("Expected Shortfall", f"{-derniere_ligne['Expected_Shortfall_Pct']} %")
    col3.metric("Volatilité Journalière", f"{derniere_ligne['Volatilite_Journaliere_Pct']} %")

    st.markdown("---")
    
    # Affichage des bases de données brutes
    col_gauche, col_droite = st.columns(2)
    
    with col_gauche:
        st.subheader("Table de Faits (Historique VaR)")
        st.dataframe(df_faits, width="stretch")
        
    with col_droite:
        st.subheader("Table de Dimension (Allocation Actuelle)")
        st.dataframe(df_dim, width="stretch")

except FileNotFoundError:
    st.error("Alerte : Les fichiers CSV sont introuvables. Le pipeline ETL doit être exécuté en amont.")

#affichage graphique en cloche des differents rendements par rapport au montant initial

#faire un histogramme de rendements

fig, ax = plt.subplots()
ax.hist(rendements, color = 'black', edgecolor='skyblue')
ax.set_title("courbe de distribution")
ax.axvline(x=var_dynamique, color="red", linestyle="-", linewidth=2, label="VaR dynamique")
st.pyplot(fig)






