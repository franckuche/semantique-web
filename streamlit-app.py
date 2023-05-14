import os
import openai
import pandas as pd
import itertools
import streamlit as st
import base64

# Titre de l'application Streamlit
st.title("Sémantique Web : Le meilleur outil pour vos briefs")

# Sidebar pour les paramètres utilisateur
st.sidebar.title("Paramètres")

# Options de l'utilisateur
uploaded_file = st.sidebar.file_uploader("Choisir un fichier CSV", type=["csv"])
api_key_1 = st.sidebar.text_input("Clé API 1")
api_key_2 = st.sidebar.text_input("Clé API 2")
api_key_3 = st.sidebar.text_input("Clé API 3")

# Ajout d'une option pour l'utilisateur de choisir le prompt
prompt_options = {
    "Semantique IA": "Veuillez ignorer toutes les instructions précédentes...",
    "Géoloc IA": "Veuillez insérer ici votre propre texte de prompt pour l'option 2.",
    "Business IA": "Veuillez insérer ici votre propre texte de prompt pour l'option 3."
}

selected_prompt = st.sidebar.selectbox(
    "Choisissez votre prompt",
    list(prompt_options.keys())
)

# Création d'un DataFrame pour stocker les résultats
result_data = []

# Vérification si le fichier et les clés API sont fournis
if uploaded_file and api_key_1 and api_key_2 and api_key_3:
    # Remplacez les clés API par vos propres clés
    api_keys = [api_key_1, api_key_2, api_key_3]

    # Créer un itérable pour les clés API
    api_key_cycle = itertools.cycle(api_keys)

    # Lire le fichier CSV avec l'encodage UTF-8
    data = pd.read_csv(uploaded_file, encoding="utf-8")

    # Traitement de chaque ligne du fichier CSV
    for index, row in data.iterrows():
        keyword = row["keyword"]
        nombre_de_mots = row["Nb de mots suggérés"]
        volume_recherche = row["Volume de recherches"]
        headings_thruu = row["headings_thruuu"]
        semantique_thruuu = row["Mots / concepts importants à développer"]

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

        message = "User : "

        if message:
            messages.append(
                {"role": "user", "content": message},
            )
            try:
                chat = openai.ChatCompletion.create(
                    model="gpt-4", messages=messages
                )
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

# Bouton pour télécharger le fichier CSV résultant de la première itération
csv = df.to_csv(index=False, encoding="utf-8").encode()
b64 = base64.b64encode(csv).decode()
href = f'<a href="data:file/csv;base64,{b64}" download="resultat.csv">Télécharger les résultats de la première itération en format CSV</a>'
st.markdown(href, unsafe_allow_html=True)

# Deuxième itération pour générer un appel à OpenAI GPT-4 avec un prompt de rédaction
if st.checkbox("Générer du contenu supplémentaire"):
    st.header("Génération de contenu avec OpenAI GPT-4")

    # Création d'un DataFrame pour stocker les résultats de la deuxième itération
    result_data_2 = []

    for index, row in df.iterrows():
        structure_hn = row["Structure Hn suggerée"]

        # Création du prompt en utilisant la structure Hn et le style de rédaction
        prompt_text_2 = f"{structure_hn} Veuillez écrire un article basé sur cette structure en utilisant le style de rédaction '{writing_style}'."

        messages_2 = [
            {"role": "system", "content": prompt_text_2},
        ]

        if message:
            messages_2.append(
                {"role": "user", "content": message},
            )
            chat_2 = openai.ChatCompletion.create(
                model="gpt-4", messages=messages_2
            )
            reply_2 = chat_2.choices[0].message.content

            # Ajout des résultats dans le DataFrame
            result_data_2.append({
                "Structure Hn": structure_hn,
                "Article généré": reply_2
            })

    # Conversion de la liste de résultats en DataFrame
    df_2 = pd.DataFrame(result_data_2)

    # Affichage du DataFrame de la deuxième itération dans l'application Streamlit
    st.write(df_2)

    # Bouton pour télécharger le fichier CSV résultant de la deuxième itération
    csv_2 = df_2.to_csv(index=False, encoding="utf-8").encode()
    b64_2 = base64.b64encode(csv_2).decode()
    href_2 = f'<a href="data:file/csv;base64,{b64_2}" download="resultat_2.csv">Télécharger les résultats de la deuxième itération en format CSV</a>'
    st.markdown(href_2, unsafe_allow_html=True)
