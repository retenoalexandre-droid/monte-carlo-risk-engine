import streamlit as st
import pandas as pd

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
    
    col1.metric("Value at Risk (95%)", f"{derniere_ligne['Value_at_Risk_95_Pct']} %")
    col2.metric("Expected Shortfall", f"{derniere_ligne['Expected_Shortfall_Pct']} %")
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