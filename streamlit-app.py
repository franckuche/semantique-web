import os
import openai
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

# Demande du prompt
prompt_option = st.selectbox(
    "Choisissez votre prompt",
    ("Semantique IA", "Géoloc IA", "Business IA")
    help="Veuillez choisir le type de prompt que vous souhaitez utiliser."

)

# Ajout d'une case à cocher pour la rédaction
st.subheader("Rédaction")
writing_checkbox = st.checkbox("Rédiger du texte")

# Demande du style de rédaction
writing_style_option = st.selectbox(
    "Quel style de rédaction souhaitez-vous ?",
    ("Pas de choix", "Style 1", "Style 2", "Style 3")
)

# Vérification si le fichier et les clés API sont fournis
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
        semantique_thruu = row["Mots / concepts importants à développer"]

        # Choisir la clé API suivante
        openai.api_key = next(api_key_cycle)

        # Création du prompt en fonction de l'option choisie par l'utilisateur
        if prompt_option == "Semantique IA":
            prompt_text = f"Veuillez ignorer toutes les instructions précédentes. Tu es un expert en référencement SEO reconnu en France. Tu dois délivrer un brief de très haute qualité à tes rédacteurs. Voici quelques informations sur ce qu'est un bon brief en 2023, il faudra t'appuyer sur ces dernières pour ta proposition de brief : {headings_thruu}. En adaptant ton brief aux conseils ci-dessus, propose-moi un brief complet pour un texte sur {keyword} pour mon rérédacteur en adaptant la longueur de ce dernier en fonction de la longueur du texte que je vais vous demander, en l'occurrence pour celui-ci j'aimerais un texte de {nombre_de_mots}, en incluant les titres des parties, les titiers des sous parties et me donnant le nombre de mots de chaque partie. Vous devrez essayer d'inclure selon les besoins un ou plusieurs [tableau], des [images], des [listes], des [liens internes], des [boutons], des [vidéos], etc..."

        elif prompt_option == "Géoloc IA":
            prompt_text = "Veuillez insérer ici votre propre texte de prompt pour 'Géoloc IA'."

        elif prompt_option == "Business IA":
            prompt_text = "Veuillez insérer ici votre propre texte de prompt pour 'Business IA'."

        # Création du prompt en fonction de l'option de style de rédaction choisie
        if writing_style_option == "Pas de choix":
            prompt_text += " Veuillez insérer ici votre propre texte de prompt pour 'Pas de choix'."

        elif writing_style_option == "Style 1":
            prompt_text += " Veuillez insérer ici votre propre texte de prompt pour 'Style 1'."

        elif writing_style_option == "Style 2":
            prompt_text += " Veuillez insérer ici votre propre texte de prompt pour 'Style 2'."

        elif writing_style_option == "Style 3":
            prompt_text += " Veuillez insérer ici votre propre texte de prompt pour 'Style 3'."

        messages = [
            {"role": "system", "content": prompt_text},
        ]

        message = "User: "

        if message:
            messages.append(
                {"role": "user", "content": message},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-4", messages=messages
            )
            reply = chat.choices[0].message.content

            # Ajout des résultats dans le DataFrame
            result_data.append({
                "keyword": keyword,
                "Nb_de_mots_suggérés": nombre_de_mots,
                "volume de recherche": volume_recherche,
                "Structure Hn suggerée": reply,
                "Rédaction": reply if writing_checkbox else None
            })

    # Conversion de la liste de résultats en DataFrame
    df = pd.DataFrame(result_data)

    # Affichage du DataFrame dans l'application Streamlit
    st.write(df)

    # Bouton pour télécharger le fichier CSV résultant
    csv = df.to_csv(index=False, encoding="utf-8").encode()
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="resultat.csv">Télécharger les résultats en format CSV</a>'
    st.markdown(href, unsafe_allow_html=True)
