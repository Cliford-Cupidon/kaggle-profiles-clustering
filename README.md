📊 Analyse des profils techniques – Kaggle Survey 2020
🚀 Application en ligne

👉 Lien Streamlit :
🔗 https://kaggle-profiles-app.streamlit.app/

👉 Code source GitHub :
https://github.com/cliford-cupidon/kaggle-profiles-clustering

🧠 Description du projet

Ce projet analyse les profils techniques issus du Kaggle Machine Learning & Data Science Survey 2020.

L’objectif est de :

Comprendre les différents profils Data

Identifier des groupes similaires grâce au Machine Learning

Visualiser les tendances du marché Data Science

Proposer une application interactive pour explorer les résultats

Une application Streamlit permet d’explorer dynamiquement les analyses.

📂 Dataset

Source : Kaggle Survey 2020

Le dataset contient des informations sur :

Les langages utilisés (Python, R, SQL…)

Les outils Data & ML

L’expérience en Data Science

Les rôles professionnels

Les salaires

Les pays

🔎 Méthodologie
1️⃣ Préparation des données

Nettoyage des données

Sélection des variables pertinentes

Encodage des variables catégorielles

Standardisation des données

2️⃣ Clustering

Algorithme utilisé : K-Means

Objectifs :

Regrouper les profils similaires

Identifier différents types de profils techniques

Analyser les caractéristiques de chaque cluster

Le modèle a été exécuté dans un notebook afin :

d’éviter un recalcul à chaque refresh Streamlit

d’améliorer la performance de l’application

d’assurer la reproductibilité des résultats

3️⃣ Visualisations

Bibliothèques utilisées :

Plotly (graphiques interactifs)

Matplotlib

Seaborn

Altair

🖥️ Application Streamlit

L’application permet :

Navigation par sections

Présentation du dataset

Visualisations interactives

Analyse des profils techniques

Résultats du clustering

Conclusion et interprétation

Elle charge directement le fichier clustered_profiles.csv généré par le notebook.

🛠️ Technologies utilisées

Python

Streamlit

Pandas

NumPy

Scikit-learn

Plotly

Matplotlib

Seaborn

Altair

⚙️ Installation en local
git clone https://github.com/cliford-cupidon/kaggle-profiles-clustering.git
cd kaggle-profiles-clustering
pip install -r requirements.txt
streamlit run app.py
📁 Structure du projet
data/
 └── clustered_profiles.csv
app.py
requirements.txt
clustering_analysis.ipynb
README.md
📈 Résultats

Le clustering met en évidence plusieurs profils types :

Profils débutants en Data Science

Data Analysts expérimentés

Machine Learning Engineers

Profils hybrides polyvalents

Chaque cluster est analysé et interprété dans l’application.

👨‍💻 Auteur

Cliford Cupidon
Projet Data Science – Portfolio
