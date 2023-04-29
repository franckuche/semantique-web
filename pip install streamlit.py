pip install streamlit
import os
import openai
import re
import pandas as pd
import itertools
import streamlit as st

# Installer le package OpenAI si nécessaire
try:
    import openai
except ImportError:
    st.write("Installation du package OpenAI en cours...")
    st.system("!pip install openai")
    import openai

# Titre de l'application Streamlit
st.title("Générateur de briefs SEO")

# Sidebar pour les paramètres utilisateur
st.sidebar.title("Paramètres")

uploaded_file = st.sidebar.file_uploader("Choisir un fichier CSV", type=["csv"])
api_key_1 = st.sidebar.text_input("Clé API 1")
api_key_2 = st.sidebar.text_input("Clé API 2")
api_key_3 = st.sidebar.text_input("Clé API 3")

if uploaded_file and api_key_1 and api_key_2 and api_key_3:
    # Remplacez les clés API par vos propres clés
    api_keys = [api_key_1, api_key_2, api_key_3]

    # Créer un itérable pour les clés API
    api_key_cycle = itertools.cycle(api_keys)

    # Lire le fichier CSV avec l'encodage UTF-8
    data = pd.read_csv(uploaded_file, encoding="utf-8")

    # Création d'un DataFrame pour stocker les résultats
    result_data = []

    # Traitement de chaque ligne du fichier CSV
    for index, row in data.iterrows():
        keyword = row["keyword"]
        nombre_de_mots = row["Nb de mots suggérés"]
        volume_recherche = row["Volume de recherches"]
        headings_thruu = row["headings_thruuu"]
        semantique_thruuu = row["Mots / concepts importants à développer"]

        # Choisir la clé API suivante
        openai.api_key = next(api_key_cycle)

        # Création du prompt en combinant les variables et la phrase fixe
        prompt_text = f"Veuillez ignorer toutes les instructions précédentes. Tu es un expert en référencement SEO reconnu en France. Tu dois délivrer un brief de très haute qualité à tes rédacteurs. Voici quelques informations sur ce qu'est un bon brief en 2023, il faudra t'appuyer sur ces dernières pour ta proposition de brief :{headings_thruu}. En adaptant ton brief aux conseils ci-dessus, propose-moi un brief complet pour un texte sur {keyword} pour mon rédacteur en adaptant la longueur de ce dernier en fonction de la longueur du texte que je vais vous demander, en l'occurrence pour celui-ci j'aimerais un texte de {nombre_de_mots}, en incluant les titres des parties, les titres des sous parties et me donnant le nombre de mots de chaque partie. Vous devrez essayer d'inclure celons les besoins un ou plusieurs [tableau], des [images], des [listes], des [liens internes], des [boutons], des [vidéos], etc..."

        messages = [
            {"role": "system", "content": prompt_text},
