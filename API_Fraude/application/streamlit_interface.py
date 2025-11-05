import streamlit as st
import pandas as pd
import requests
import json
from sklearn.metrics import accuracy_score, classification_report
from io import BytesIO, StringIO
from API_Fraude.domain import fraud_rules


st.set_page_config(page_title="FraudShield - Détection de Fraude", layout="wide")
st.title("FraudShield - Analyse des Transactions")


# Uploader un fichier JSON
uploaded_file = st.file_uploader("Uploadez un fichier JSON à analyser", type=["json"])
# Input utilisateur pour choisir le seuil
cutoff_threshold = st.slider("Seuil de détection de fraude (cutoff)", 0.0, 1.0, round(fraud_rules.FRAUD_RATE_THRESHOLD, 3), step=0.001)

if uploaded_file:
    with st.spinner("Envoi à l'API et analyse en cours..."):
        try:
            # Envoyer le fichier JSON tel quel (comme un fichier, pas du texte)
            files = {"file": (uploaded_file.name, uploaded_file, "application/json")}
            #url = f"http://0.0.0.0:8000/predict/?cutoff_threshold={cutoff_threshold}"
            url = f"http://127.0.0.2:8000/predict/?cutoff_threshold={cutoff_threshold}"
            response = requests.post(url, files=files)

            if response.status_code == 200:
                data = response.json()  # <- JSON retourné par l’API
                df_result = pd.DataFrame(data)

                st.success("Analyse terminée avec succès !")
                st.subheader("Résultats")
                st.dataframe(df_result, use_container_width=True)

                # Télécharger les résultats en JSON
                json_str = json.dumps(data, indent=2)
                st.download_button(
                    label="Télécharger les résultats JSON",
                    data=json_str,
                    file_name="resultats_fraude.json",
                    mime="application/json"
                )
                # Affichage des métriques
                y_true = df_result["fraude"]
                y_pred = df_result["is_fraud"]

                acc = accuracy_score(y_true, y_pred)
                report = classification_report(y_true, y_pred, output_dict=True)

                st.subheader("📈 Évaluation des Prédictions")
                st.markdown(f"**🎯 Taux de Bonne Prédiction (Accuracy)** : `{acc:.2%}`")

                st.markdown("**📋 Rapport de Classification :**")
                st.dataframe(pd.DataFrame(report).transpose())
            else:
                st.error(f"Erreur de l'API : {response.status_code}\n{response.text}")

        except Exception as e:
            st.error(f"Une erreur est survenue : {str(e)}")

# streamlit run "C:\Users\dsonne\OneDrive - Micropole\Documents\Projet Python\Fraud detector\API_Fraude\API_Fraude\application\streamlit_interface.py"