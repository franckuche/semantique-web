import os
import openai
import re
import pandas as pd
import itertools
import streamlit as st
import base64

# Installer le package OpenAI si nécessaire
try:
    import openai
except ImportError:
    st.write("Installation du package OpenAI en cours...")
    st.system("!pip install openai")
    import openai

# Titre de l'application Streamlit
st.title("Sémantique Web : Le meilleur outil pour vos briefs")

# Demande de fichier CSV et clés API
uploaded_file = st.file_uploader("Choisir un fichier CSV", type=["csv"])
api_key_1 = st.text_input("Clé API 1")
api_key_2 = st.text_input("Clé API 2")
api_key_3 = st.text_input("Clé API 3")

# Deuxième itération pour générer un appel à OpenAI GPT-4 avec un prompt de rédaction
st.header("Génération de contenu avec OpenAI GPT-4")

# Demander à l'utilisateur s'il souhaite générer du contenu supplémentaire
generate_content = st.checkbox("Générer du contenu supplémentaire")

# Demander le style de rédaction uniquement si la case est cochée
if generate_content:
    writing_style = st.selectbox(
        "Quel style de rédaction souhaitez-vous ?",
        ("Pas de choix", "Prompt 1", "Prompt 2", "Prompt 3")
    )
else:
    writing_style = "Pas de choix"

# Création d'une liste pour stocker les résultats
result_data = []

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
        if prompt_option == "Semantique IA":
            prompt_text = f"Veuillez ignorer toutes les instructions précédentes. Tu es un expert en référencement SEO reconnu en France. Tu dois délivrer un brief de très haute qualité à tes rédacteurs. Voici quelques informations sur ce qu'est un bon brief en 2023, il faudra t'appuyer sur ces dernières pour ta proposition de brief :{headings_thruu}. En adaptant ton brief aux conseils ci-dessus, propose-moi un brief complet pour un texte sur {keyword} pour mon rédacteur en adaptant la longueur de ce dernier en fonction de la longueur du texte que je vais vous demander, en l'occurrence pour celui-ci j'aimerais un texte de {nombre_de_mots}, en incluant les titres des parties, les titres des sous parties et me donnant le nombre de mots de chaque partie. Vous devrez essayer d'inclure selon les besoins un ou plusieurs [tableau], des [images], des [listes], des [liens internes], des [boutons], des [vidéos], etc..."
        elif prompt_option == "Géoloc IA":
            prompt_text = f"Veuillez insérer ici votre propre texte de prompt pour 'Géoloc IA'."

        elif prompt_option == "Business IA":
            prompt_text = f"Veuillez insérer ici votre propre texte de prompt pour 'Business IA'."

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

        # Ajout des résultats dans la liste result_data
        result_data.append({
            "keyword": keyword,
            "Nb_de_mots_suggérés": nombre_de_mots,
            "volume de recherche": volume_recherche,
            "Structure Hn suggerée": reply
        })

# Conversion de la liste de résultats en DataFrame
if result_data:
    df = pd.DataFrame(result_data)

    # Affichage du DataFrame dans l'application Streamlit
    st.write(df)

    # Bouton pour télécharger le fichier CSV résultant de la première itération
    csv = df.to_csv(index=False, encoding="utf-8").encode()
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="resultat.csv">Télécharger les résultats de la première itération en format CSV</a>'
    st.markdown(href, unsafe_allow_html=True)

    # Deuxième itération pour générer un appel à OpenAI GPT-4 avec un prompt de rédaction
    if generate_content and writing_style != "Pas de choix":
        st.header("Génération de contenu avec OpenAI GPT-4")

        # Création d'une nouvelle liste pour stocker les résultats de la deuxième itération
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

                # Ajout des résultats dans la liste result_data_2
                result_data_2.append({
                    "Structure Hn": structure_hn,
                    "Article généré": reply_2
                })

        # Conversion de la liste de résultats en DataFrame
        df= pd.DataFrame(result_data_2)

        # Affichage du DataFrame de la deuxième itération dans l'application Streamlit
        st.write(df_2)

        # Bouton pour télécharger le fichier CSV résultant de la deuxième itération
        csv_2 = df_2.to_csv(index=False, encoding="utf-8").encode()
        b64_2 = base64.b64encode(csv_2).decode()
        href_2 = f'<a href="data:file/csv;base64,{b64_2}" download="resultat_2.csv">Télécharger les résultats de la deuxième itération en format CSV</a>'
        st.markdown(href_2, unsafe_allow_html=True)

    else:
        st.warning("Aucune donnée à afficher. Veuillez fournir un fichier CSV et les clés API pour continuer.")

    else:
        st.warning("Veuillez fournir un fichier CSV et les clés API pour continuer.")



