import os
import openai
import re
import pandas as pd
import itertools
import streamlit as st
import base64

try:
    import openai
except ImportError:
    st.write("Installation du package OpenAI en cours...")
    st.system("!pip install openai")
    import openai

st.title("Sémantique Web : Le meilleur outil pour vos briefs")

st.sidebar.title("Paramètres")

uploaded_file = st.sidebar.file_uploader("Choisir un fichier CSV", type=["csv"])
api_key_1 = st.sidebar.text_input("Clé API 1")
api_key_2 = st.sidebar.text_input("Clé API 2")
api_key_3 = st.sidebar.text_input("Clé API 3")

prompt_option = st.sidebar.selectbox(
    "Choisissez votre prompt",
    ("Semantique IA", "Géoloc IA", "Business IA")
)

result_data = []

if uploaded_file and api_key_1 and api_key_2 and api_key_3:
    api_keys = [api_key_1, api_key_2, api_key_3]
    api_key_cycle = itertools.cycle(api_keys)

    data = pd.read_csv(uploaded_file, encoding="utf-8")

    for index, row in data.iterrows():
        keyword = row["keyword"]
        nombre_de_mots_suggérés = row["nombre de mots suggérés"]
        volume_recherche = row["Volume de recherches"]
        Headings = row["Headings"]
        Champs_sémantique = row["Champs sémantique"]

        openai.api_key = next(api_key_cycle)

        if prompt_option == "Semantique IA":
            prompt_text = f"Veuillez ignorer toutes les instructions précédentes. Tu es un expert en référencement SEO reconnu en France. Tu dois délivrer un brief de très haute qualité à tes rédacteurs sans rediger directement le contenu. Tu dois faire un affichage sous forme d'une structure <hn> avec un <h1> des <h2> et si besoin des <h3> et <h4> pour les titres. Donne quelques points important en liste pour aider à écrire introduction hors de la structure <hn>. Concentre toi uniquement sur le briefs n'ajoute pas d'autres commentaires ou informations qui ne fait pas partie du brief que ce soit avant ou apres le brief. Voici quelques informations sur ce qu'est un bon brief en 2023, il faudra t'appuyer sur ces dernières pour ta proposition de brief : {Headings}. En adaptant ton brief aux conseils ci-dessus, propose-moi un brief complet pour un texte sur {keyword} pour mon rédacteur en adaptant la longueur de ce dernier en fonction de la longueur du texte que je vais vous demander, en l'occurrence pour celui-ci j'aimerais un texte de {nombre_de_mots_suggérés}, en incluant les titres des parties (en h2), les titres des sous parties (en h3 ou h4 si besoin) et me donnant le nombre de mots de chaque partie. 
Vous devrez essayer d'inclure lorsque c'est logique et pertinent par rapport aux titres et l'intention utilisateur un [tableau] si besoin, des [images], des [listes bullet points], des [listes en etapes], des [boutons], des [vidéos], etc..."
        elif prompt_option == "Géoloc IA":
            prompt_text = "Veuillez insérer ici votre propre texte de prompt pour l'option 2."
        else:
            prompt_text = "Veuillez insérer ici votre propre texte de prompt pour l'option 3."

        messages = [
            {"role": "system", "content": prompt_text},
        ]

        message = "User : "

        if message:
            messages.append(
                {"role": "user", "content": message},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-4", messages=messages
            )
            reply = chat.choices[0].message.content

            result_data.append({
                "keyword": keyword,
                "Nombre de mots suggérés": nombre_de_mots_suggérés,
                "volume de recherche": volume_recherche,
                "Structure Hn suggerée": reply
            })

    df = pd.DataFrame(result_data)
    st.write(df)

    csv = df.to_csv(index=False, encoding="utf-8").encode()
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="resultat.csv">Télécharger les résultats en format CSV</a>'
    st.markdown(href, unsafe_allow_html=True)
