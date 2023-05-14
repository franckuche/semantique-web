import os
import openai
import pandas as pd
import itertools
import streamlit as st
import base64

# Titre de l'application Streamlit
st.title("Sémantique Web : Le meilleur outil pour vos briefs")

# Demande de fichier CSV et clés API
uploaded_file = st.file_uploader("Choisir un fichier CSV", type=["csv"])
api_key_1 = st.text_input("Clé API 1")
api_key_2 = st.text_input("Clé API 2")
api_key_3 = st.text_input("Clé API 3")

# Demande du prompt et du style de rédaction
prompt_options = {
    "Semantique IA": "Veuillez ignorer toutes les instructions précédentes...",
    "Géoloc IA": "Veuillez insérer ici votre propre texte de prompt pour 'Géoloc IA'.",
    "Business IA": "Veuillez insérer ici votre propre texte de prompt pour 'Business IA'."
}

selected_prompt = st.selectbox("Choisissez votre prompt", list(prompt_options.keys()))

writing_style_options = {
    "Pas de choix": None,
    "Style 1": "Prompt pour le Style 1",
    "Style 2": "Prompt pour le Style 2",
    "Style 3": "Prompt pour le Style 3"
}

selected_writing_style = st.selectbox("Quel style de rédaction souhaitez-vous ?", list(writing_style_options.keys()))

# Deuxième itération pour générer un appel à OpenAI GPT-4 avec un prompt de rédaction
st.header("Génération de contenu avec OpenAI GPT-4")

# Demander à l'utilisateur s'il souhaite générer du contenu supplémentaire
generate_content = st.checkbox("Générer du contenu supplémentaire")

if uploaded_file and api_key_1 and api_key_2 and api_key_3:
    # Remplacer les clés API par vos propres clés
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
        semantique_thruu = row["Mots / concepts importants à développer"]

        # Choisir la clé API suivante
        openai.api_key = next(api_key_cycle)

        # Création du prompt en fonction de l'option choisie par l'utilisateur
        prompt_text = prompt_options[selected_prompt].format(
            headings_thruu=headings_thruu,
            keyword=keyword,
            nombre_de_mots=nombre_de_mots
        )

        messages = [
            {"role": "system", "content": prompt_text},
        ]

        message = "User: "

        if selected_writing_style and selected_writing_style != "Pas de choix":
            writing_prompt = writing_style_options[selected_writing_style]
        messages.append({"role": "user", "content": writing_prompt})

    if message:
        messages.append({"role": "user", "content": message})

    try:
        chat = openai.ChatCompletion.create(model="gpt-4", messages=messages)
        reply = chat.choices[0].message.content

        # Ajout des résultats dans le DataFrame
        result_data.append({
            "keyword": keyword,
            "Nb_de_mots_suggérés": nombre_de_mots,
            "volume de recherche": volume_recherche,
            "Structure Hn suggerée": reply
        })
    except Exception as e:
        st.error(f"Erreur lors de la génération du contenu pour la ligne {index + 1}: {str(e)}")

# Conversion de la liste de résultats en DataFrame
df = pd.DataFrame(result_data)

# Affichage du DataFrame dans l'application Streamlit
st.write(df)

# Bouton pour télécharger le fichier CSV résultant
csv = df.to_csv(index=False, encoding="utf-8").encode()
b64 = base64.b64encode(csv).decode()
href = f'<a href="data:file/csv;base64,{b64}" download="resultat.csv">Télécharger les résultats en format CSV</a>'
st.markdown(href, unsafe_allow_html=True)

# Bouton pour télécharger le fichier CSV résultant de la première itération
if generate_content:
    csv = df.to_csv(index=False, encoding="utf-8").encode()
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="resultat.csv">Télécharger les résultats en format CSV</a>'
    st.markdown(href, unsafe_allow_html=True)

