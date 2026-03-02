# 📊 Analyse des profils techniques – Kaggle Survey 2020

Projet Data Science Portfolio réalisé par **Cliford Cupidon**

---

## 🚀 Application en ligne

👉 https://kaggle-profiles-app.streamlit.app/

---

## 📁 Repository GitHub

👉 https://github.com/cliford-cupidon/kaggle-profiles-clustering

---

## 🎯 Objectif du projet

L’objectif de ce projet est d’analyser les profils techniques issus du **Kaggle Survey 2020** afin d’identifier différents types de professionnels de la Data grâce à des méthodes de **Machine Learning non supervisé (Clustering)**.

Ce projet permet de :

* Comprendre la diversité des profils en Data Science
* Identifier les compétences dominantes
* Regrouper les profils similaires
* Visualiser les résultats dans une application interactive

---

## 🧠 Méthodologie

### 1️⃣ Préparation des données

* Nettoyage des données
* Gestion des valeurs manquantes
* Encodage des variables catégorielles
* Normalisation des données

### 2️⃣ Clustering

* Algorithme utilisé : **K-Means**
* Choix du nombre optimal de clusters
* Analyse et interprétation des clusters

### 3️⃣ Visualisation

* Graphiques interactifs
* Analyse des profils dans Streamlit

---

## 📊 Résultats

Le clustering a permis d’identifier plusieurs profils types :

* Débutants en Data Science
* Data Analysts expérimentés
* Machine Learning Engineers
* Profils hybrides polyvalents

Chaque cluster est analysé et expliqué dans l’application Streamlit.

---

## 📂 Structure du projet

data/
│   clustered_profiles.csv
│   kaggle_survey_2020_responses.csv

app.py
requirements.txt
clustering_analysis.ipynb
README.md

---

## ⚙️ Installation en local

1. Cloner le repository

git clone https://github.com/cliford-cupidon/kaggle-profiles-clustering.git
cd kaggle-profiles-clustering

2. Installer les dépendances

pip install -r requirements.txt

3. Lancer l’application

streamlit run app.py

---

## 🛠️ Technologies utilisées

* Python
* Pandas
* NumPy
* Scikit-learn
* Plotly
* Matplotlib
* Seaborn
* Streamlit
* Altair

---

## 📌 Dataset

Dataset : Kaggle Machine Learning & Data Science Survey 2020
https://www.kaggle.com/c/kaggle-survey-2020

---

## 👤 Auteur

Cliford Cupidon
Projet Data Science Portfolio

---

⭐ Si ce projet vous plaît, n’hésitez pas à mettre une étoile sur GitHub !
