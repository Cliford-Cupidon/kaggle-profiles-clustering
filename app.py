
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from matplotlib.patches import Patch

import re 

df_old = pd.read_csv("kaggle_survey_2020_responses.csv", low_memory=False)
df = pd.read_csv("Final.csv", low_memory=False)

# ----------------------------
# 1️⃣ Fonctions globales
# ----------------------------
def afficher_auteurs_sidebar():
    """Fonction pour afficher les auteurs dans la sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👥 Auteur")
    st.sidebar.markdown("""
    - **Cliford CUPIDON**
    """)

# ----------------------------
# Interface Streamlit
# ----------------------------
st.title("Analyse des profils techniques au sein de la data" )
st.sidebar.title("Sommaire")
pages=["Introduction et Contexte", 
       "Présentation du Dataset", 
       "DataVizualization", 
       "Les profils techniques", 
       "Les tâches et les outils",
       "Clustering des profils", 
       "Conclusion",
       "Remerciements"]

page=st.sidebar.radio("Aller vers", pages)

# ----------------------------
# 4️⃣ Pages 0 : Intro
# ----------------------------

if page == pages[0] :
    st.title("🏠 Introduction")
    st.markdown("""
        Ce projet vise à analyser les résultats du sondage **Kaggle 2020** pour :
        - 🔍 Identifier les **profils techniques** les plus représentés
        - 🛠️ Comprendre les **outils et plateformes** utilisés
        - 📆 Explorer les **activités quotidiennes** des professionnels de la donnée
        """)

    st.markdown("""
    <div style='background-color:#f9f9f9; padding: 10px; border-left: 6px solid #FF4B4B'>
    <b>Problématique</b> 🧠<br>
    <em>Comment les tâches et outils utilisés permettent-ils de mieux comprendre les différents profils dans l’industrie de la donnée ?</em>
    </div>
    """, unsafe_allow_html=True)

    afficher_auteurs_sidebar()

# ----------------------------
# 4️⃣ Pages 1 : Données
# ----------------------------

if page == pages[1] :
    st.header("Présentation du Dataset")
    st.markdown("""
Le Dataset utilisé est tiré du sondage "2020 Kaggle Machine Learning & Data Science Survey"
    réalisé par Kaggle et présent en accès libre via l’adresse suivante :
    https://www.kaggle.com/c/kaggle-survey-2020/overview
    Cette enquête regroupe les réponses de plus de 20 000 professionnels du monde entier.
    Les participants partagent des informations sur leurs rôles, les outils et les langages
    qu'ils utilisent, les plateformes sur lesquelles ils travaillent, ainsi que leurs
    formations et pratiques professionnelles""")

    st.header("Exploration")
    st.write("""
    Pour explorer et analyser le dataset, nous avons chargé les données dans un environnement
    python.

    Voici ci-dessous un extrait du Dataframe avant transformation des données
""")

    st.subheader("Avant transformation")
    st.dataframe(df_old.head(10))
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Nombre de lignes", df_old.shape[0])
    with col2:
        st.metric("Nombre de colonnes", df_old.shape[1])

    st.header("Nettoyage")
    st.write("""
    Un nettoyage des données a été effectué pour réduire la taille du DataFrame de 355 à 25
    colonnes :
    - Regroupement des questions à choix multiples.
    - Traitement des valeurs manquantes en supprimant les colonnes avec plus de 80% de valeurs manquantes.
    - Traitement des doublons.
    - Colonnes renommées avec des noms explicites pour faciliter la lecture et l’analyse

    Voici ci-dessous un extrait du Dataframe après transformation des données
""")

    st.subheader("Après transformation (extrait)")
    st.dataframe(df.head(10))

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Nombre de lignes", df.shape[0])
    with col2:
        st.metric("Nombre de colonnes", df.shape[1])

    afficher_auteurs_sidebar()

# ----------------------------
# 4️⃣ Pages 2 : DataViz
# ----------------------------

elif page == pages[2]:
    st.header("DataVizualization")
    st.write("Choisir une visualisation dans la liste ci-dessous pour explorer les données.")

    viz = st.selectbox("Sélectionner une visualisation", [
       "Répartition des rôles (pie)",
       "IDE par profils (barplot)",
       "Outils DataViz par profils",
       "Langages par pays (Data Analyst & Data Scientist)",
       "Expérience de codage par genre et profil",
       "Utilisation des ML frameworks par métier"
    ])

    # --- Répartition des rôles (pie)
    if viz == "Répartition des rôles (pie)":
        st.subheader("Répartition des rôles des répondants")
        role_counts = df['job_title'].value_counts().nlargest(9)
        fig, ax = plt.subplots(figsize=(8,8))
        ax.pie(
            role_counts,
            labels=role_counts.index,
            autopct=lambda x: f"{x:.1f}%",
            startangle=90,
            pctdistance=0.8 # rapproche ou éloigne les %
            )
        ax.axis('equal')
        st.pyplot(fig)

    # --- IDE par profils (barplot)
    elif viz == "IDE par profils (barplot)":
        st.subheader("Environnements de développement les plus utilisés par profil")

        dfnew = df[["job_title", "IDE"]].copy()
        dfnew['IDE'] = dfnew['IDE'].astype(str).str.replace(r'\(.*?\)', '', regex=True).str.split(',')
        dfnew = dfnew.explode('IDE')
        dfnew['IDE'] = dfnew['IDE'].str.strip()

        #  Filtrer pour garder seulement les métiers pertinents
        top_jobs = ['Data Analyst', 'Machine Learning Engineer', 'Data Scientist', 'Software Engineer', 'Student']
        df_filtered = dfnew[dfnew['job_title'].isin(top_jobs)].copy()

        #  Compter les occurrences
        count_data = df_filtered.groupby(['job_title', 'IDE']).size().reset_index(name='counts')

        # Création de la figure
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(
            data=count_data,
            y='counts',
            x='job_title',
            hue='IDE',
            palette = "tab20" ,
            edgecolor='black',
            linewidth=1
            )
        plt.title('Environnements de développement les plus utilisés par profil professionnel(métiers ciblés)', y=1.02)
        plt.xlabel('profil professionnel')
        plt.ylabel('Nombre d\'utilisateurs')

        # Rotation + alignement des ticks
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

        # Légende à l'extérieur
        ax.legend(
        title="IDE",
        bbox_to_anchor=(1.05, 1),  # position horizontale, verticale
        loc='upper left'  # ancrage

        )
        plt.tight_layout()
        st.pyplot(fig)

    # --- Outils DataViz par profils
    elif viz == "Outils DataViz par profils":
        st.subheader("Outils de DataVisualisation les plus utilisés par profils")
        if 'Data_viz_libraries' not in df.columns or 'job_title' not in df.columns:
            st.warning("Colonnes manquantes.")
        else:
            def clean_data_viz(series):
                cleaned = (series.dropna().str.split(',').explode().str.strip().loc[lambda x: x != ''])
                result = cleaned.value_counts().reset_index()
                result.columns = ['Data_viz_libraries', 'count']
                return result

            top_jobs = ['Data Analyst', 'Machine Learning Engineer','Data Scientist','Software Engineer', 'Student']
            fig = plt.figure(figsize=(14, 18))
            i=1
            for job in top_jobs:
                job_series = df[df['job_title'] == job]['Data_viz_libraries'] if 'job_title' in df.columns else pd.Series(dtype='object')
                job_df = clean_data_viz(job_series)
                ax = fig.add_subplot(3,2,i)
                sns.barplot(x='count',
                            y='Data_viz_libraries',
                            data=job_df.head(15),
                            ax=ax,
                            palette='rocket')
                ax.set_title(f'Top outils pour {job}')
                ax.set_xlabel('Nombre d\'utilisateurs')
                ax.set_ylabel('')
                i += 1
            plt.tight_layout()
            st.pyplot(fig)

 # --- Langages par pays (Data Analyst & Data Scientist)
    elif viz == "Langages par pays (Data Analyst & Data Scientist)":
        st.subheader("Langages par pays - Data Analyst & Data Scientist")
        # Nettoyage et préparation
        df_tmp = df[df["programming_languages"].notna()].copy()
        df_tmp["programming_languages"] = df_tmp["programming_languages"].apply(lambda x: [lang.strip() for lang in x.split(",")] if isinstance(x, str) else [])
        df_filtered = df_tmp[df_tmp["job_title"].isin(["Data Analyst", "Data Scientist"])].copy()
        df_exploded = df_filtered.explode("programming_languages").reset_index(drop=True)
        df_exploded = df_exploded[df_exploded["programming_languages"] != ""]

        # Top pays
        top_countries_analyst = df_exploded[df_exploded["job_title"]=="Data Analyst"]["Country_of_residence"].value_counts().nlargest(5).index
        top_countries_scientist = df_exploded[df_exploded["job_title"]=="Data Scientist"]["Country_of_residence"].value_counts().nlargest(5).index
        top_countries = list(set(top_countries_analyst).union(set(top_countries_scientist)))

        df_top = df_exploded[df_exploded["Country_of_residence"].isin(top_countries)].copy()

        # Créer palettes cohérentes, pour avoir le même code couleur pour les pays
        unique_countries = sorted(df_top["Country_of_residence"].unique())
        palette_colors = sns.color_palette("Set2", len(unique_countries))
        country_palette = dict(zip(unique_countries, palette_colors))

        # Séparer les dataframes
        df_analyst = df_top[df_top["job_title"] == "Data Analyst"]
        df_scientist = df_top[df_top["job_title"] == "Data Scientist"]

        top_langs = df_top["programming_languages"].value_counts().index[:10]

        # Plot
        fig, axes = plt.subplots(1, 2, figsize=(22,10), sharey=True)
        sns.countplot(data=df_analyst,
                      x="programming_languages",
                      hue="Country_of_residence",
                      order=top_langs,
                      palette=country_palette,
                      ax=axes[0])
        axes[0].set_title("Langages par pays - Data Analyst", fontsize=30)
        axes[0].set_xlabel("Langages", fontsize=25)
        axes[0].set_ylabel("Nombre de répondants", fontsize=25)
        axes[0].tick_params(axis='x', rotation=45, labelsize=20)
        axes[0].tick_params(axis='y', labelsize=20)

        sns.countplot(data=df_scientist,
                      x="programming_languages",
                      hue="Country_of_residence",
                      order=top_langs,
                      palette=country_palette,
                      ax=axes[1])
        axes[1].set_title("Langages par pays - Data Scientist", fontsize=30)
        axes[1].set_xlabel("Langages", fontsize=25)
        axes[1].set_ylabel("", fontsize=25)
        axes[1].tick_params(axis='x', rotation=45, labelsize=20)
        axes[1].tick_params(axis='y', labelsize=20)

        plt.tight_layout()
        st.pyplot(fig)

    # --- Expérience de codage par genre et profil
    elif viz == "Expérience de codage par genre et profil":
        st.subheader("Expérience de codage selon le genre et le profil technique")
        df_exp = df.dropna(subset=["Coding_experience", "Gender", "job_title"]).copy()

        # Exclure certains profils
        excluded_titles = ["Student", "Other", "Currently not employed"]
        df_exp = df_exp[~df_exp["job_title"].isin(excluded_titles)]

        # Ordre de l’expérience
        experience_order = [
            "Never written code",
            "< 1 year",
            "1-2 years",
            "3-5 years",
            "5-10 years",
            "10-20 years",
            "20+ years"
            ]

        # Convertir en catégorie ordonnée
        df_exp["Coding_experience"] = pd.Categorical(
            df_exp["Coding_experience"],
            categories=experience_order,
            ordered=True)

        # Contexte lisible
        sns.set_context("talk")
        genders = df_exp["Gender"].unique()
        palette = sns.color_palette("Set2", n_colors=len(genders))
        color_map = dict(zip(genders, palette))
        g = sns.catplot(
            data=df_exp,
            x="Coding_experience",
            hue="Gender",
            col="job_title",
            kind="count",
            height=4,
            aspect=1.5,
            palette=color_map,
            col_wrap=2,
            sharey=False,
            legend=False
            )

        #for ax in g.axes.flatten():
            # Rotation + alignement des ticks
            #plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            #ax.margins(y=0.1)  # ajoute de l’espace vertical autour des barres
            #ax.set_xlabel("Expérience en code")
            #ax.set_ylabel("Nombre de répondants")

        #---------------------
        for ax in g.axes.flatten():
            # Rotation + alignement des ticks
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

            # 🔥 Rendre les petites barres visibles
            ax.set_yscale("log")

            # ❌ Supprimer les ticks sur l’axe Y
            ax.tick_params(axis='y', which='both', length=0)

            # Marges et labels
            ax.margins(y=0.1)
            ax.set_xlabel("Expérience en code")
            ax.set_ylabel("Nombre de répondants")

            # 📊 Afficher les valeurs au-dessus des barres
            for container in ax.containers:
                ax.bar_label(container, fmt='%.0f', label_type='edge', fontsize=8, padding=2)

        #-------------
        g.fig.subplots_adjust(top=0.88, right=0.82, wspace=0.35, hspace=0.35)


        # Création manuelle des patches de légende
        from matplotlib.patches import Patch
        legend_handles = [Patch(color=color_map[gender], label=gender) for gender in genders]

        g.fig.legend(
            handles=legend_handles,
            title="Genre",
            loc='center left',
            bbox_to_anchor=(1.05, 0.5),
            frameon=False
            )

        plt.tight_layout()
        g.fig.subplots_adjust(hspace=0.5)  # plus d’espace entre les lignes
        st.pyplot(g.fig)

    # --- ML frameworks par métier
    elif viz == "Utilisation des ML frameworks par métier":
        st.subheader("Utilisation des ML Frameworks selon les métiers")
        if 'Ml_frameworks' not in df.columns or 'job_title' not in df.columns:
            st.warning("Colonnes 'Ml_frameworks' ou 'job_title' manquantes.")
        else:
            step1_3_cleaned = df['Ml_frameworks'].dropna().str.split(',').explode().str.strip()
            framework_mapping = {
                'Tensorflow': 'TensorFlow',
                'Pytorch': 'PyTorch',
                'Xgboost': 'XGBoost',
                'Lightgbm': 'LightGBM',
                'Fast.Ai': 'Fastai',
                'Scikit-Learn': 'Scikit-learn',
                'H2O 3': 'H2O.ai'
            }
            step4_standardized = step1_3_cleaned.replace(framework_mapping)
            df_job_framework = pd.concat([
                df.loc[step4_standardized.index, 'job_title'],
                step4_standardized.rename("Framework")
            ], axis=1).dropna()
            top_frameworks = df_job_framework['Framework'].value_counts().head(5).index
            filtered_df = df_job_framework[df_job_framework['Framework'].isin(top_frameworks)]
            fig, ax = plt.subplots(figsize=(12,6))
            sns.countplot(data=filtered_df,
                          x='Framework',
                          hue='job_title',
                          ax=ax,
                          palette="Paired")
            ax.set_title("Utilisation des ML Frameworks par Titre de Poste")
            ax.set_xlabel("Frameworks de Machine Learning")
            ax.set_ylabel("Nombre d'utilisateurs")
            ax.tick_params(axis='x', rotation=45)
            ax.legend(title='Titre de poste', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            st.pyplot(fig)

    afficher_auteurs_sidebar()

# ----------------------------
# 4️⃣ Pages 3 : Profils Techniques
# ----------------------------

if page == pages[3]:
    st.markdown("Explore les rôles professionnels, les tranches d'âge, les niveaux d'études, le genre et les pays des participants à l'enquête Kaggle 2020.")

    # Filtre pays
    st.sidebar.header("🔎 Filtres")
    pays = st.sidebar.multiselect("Filtrer par pays :", df["Country_of_residence"].dropna().sort_values(ascending=True).unique())

     # Filtre Metier
    metier = st.sidebar.multiselect("Filtrer par Metier :", df["job_title"].sort_values(ascending=True).dropna().unique())

     # Application du filtre
    df_filtered = df.copy()

    # Cas 1: Aucun filtre sélectionné → affiche tout
    if not pays and not metier:
        df_filtered = df.copy()

    # Cas 2: Seulement le pays sélectionné → pays + tous les métiers
    elif pays and not metier:
        df_filtered = df_filtered[df_filtered["Country_of_residence"].isin(pays)]

    # Cas 3: Seulement le métier sélectionné → métier + tous les pays
    elif not pays and metier:
        df_filtered = df_filtered[df_filtered["job_title"].isin(metier)]

    # Cas 4: Les deux filtres sélectionnés → pays ET métier
    elif pays and metier:
        df_filtered = df_filtered[
            df_filtered["Country_of_residence"].isin(pays) &
            df_filtered["job_title"].isin(metier)
        ]

    afficher_auteurs_sidebar()

    # Choix analyse
    profil_option = st.radio("Choisir une caractéristique à visualiser :",
                             ["Rôle professionnel", "Tranche d'âge", "Niveau d'études", "Genre", "Top 10 des pays"])

    if profil_option == "Rôle professionnel":
        st.subheader("💼 Rôle Professionnel")
        counts = df_filtered["job_title"].value_counts().sort_values()
        fig = px.bar(counts, orientation='h',
                     title="Répartition des rôles professionnels",
                     labels={"value": "Nombre", "index": "Rôle"},
                     color_discrete_sequence=["#1B557E"])
        fig.update_layout(showlegend=False, title_x=0.5)
        fig.update_traces(text=counts.values, textposition='outside')
        st.plotly_chart(fig)

    elif profil_option == "Tranche d'âge":
        st.subheader("🕒 Tranche d'âge")
        age_counts = df_filtered["Age"].value_counts().sort_values(ascending=False)
        fig = px.pie(names=age_counts.index, values=age_counts.values,
                     title="Répartition par tranche d'âge",
                     color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_layout( title_x=0.5,legend_title_text='Âge')
        st.plotly_chart(fig)

    elif profil_option == "Niveau d'études":
        st.subheader("🎓 Niveau d'études")
        counts = df_filtered["Education"].value_counts().sort_values()
        fig = px.bar(counts, orientation='h',
                     title="Répartition du niveau d'études",
                     labels={"value": "Nombre", "index": "Niveau"},
                     color_discrete_sequence=["#2ca02c"])
        fig.update_layout(showlegend=False, title_x=0.5)
        fig.update_traces(text=counts.values, textposition='outside')
        st.plotly_chart(fig)

    elif profil_option == "Genre":
        st.subheader("🚻 Genre")
        counts = df_filtered["Gender"].value_counts().sort_values()
        fig = px.bar(counts, orientation='h',
                     title="Répartition par genre",
                     labels={"value": "Nombre", "index": "Genre"},
                     color_discrete_sequence=["#d62728"])
        fig.update_layout(showlegend=False, title_x=0.5)
        fig.update_traces(text=counts.values, textposition='outside')
        st.plotly_chart(fig)

    elif profil_option == "Top 10 des pays":
        st.subheader("🌍 Top 10 des pays")
        top_countries = df["Country_of_residence"].value_counts().nlargest(10).sort_values()
        fig = px.bar(top_countries, orientation='h',
                     title="Top 10 des pays représentés",
                     labels={"value": "Nombre de participants", "index": "Pays"},
                     color_discrete_sequence=["#9467bd"])
        fig.update_layout(showlegend=False, title_x=0.5)
        fig.update_traces(text=top_countries.values, textposition='outside')
        st.plotly_chart(fig)

# ----------------------------
# 4️⃣ Pages 4 : Tâches et outils
# ----------------------------
def multiresponse_counts(series, delimiter=","):
    return (series.dropna()
                  .str.split(delimiter)
                  .explode()
                  .str.strip()
                  .value_counts())

if page == pages[4]:
    st.markdown("Visualisez les langages de programmation, bibliothèques Python, et plateformes ML les plus utilisées par les professionnels de la Data.")

    # Filtre pays
    st.sidebar.header("🔎Filtres")
    pays = st.sidebar.multiselect("Filtrer par pays :", df["Country_of_residence"].dropna().unique())
    df_filtered = df.copy()
    if pays:
        df_filtered = df_filtered[df_filtered["Country_of_residence"].isin(pays)]

    afficher_auteurs_sidebar()

    # Sélection du profil technique
    roles = df_filtered["job_title"].dropna().unique()
    roles_options = ['All'] + sorted(roles)
    #selected_role = st.selectbox("Sélectionner un profil technique :", sorted(roles))
    selected_role = st.selectbox("Sélectionner un profil technique :", roles_options)

    # Si "All" est choisi → on garde tout le df_filtered
    if selected_role == "All":
        df_role = df_filtered.copy()
    else:
        df_role = df_filtered[df_filtered["job_title"] == selected_role]

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Langages", "Outils Dataviz",  "Outils/Plateformes ML", "Les tâches effectuées", "Expérience en programmation","IDE"])

    with tab1:
        st.subheader("💻 Langages de programmation")
        lang_counts = multiresponse_counts(df_role["programming_languages"])
        fig = px.bar(lang_counts, orientation='h',
                     title="Langages les plus populaires",
                     labels={'value': 'Nombre', 'index': 'Langage'},
                     color='value',
                     color_continuous_scale='Plasma')
        fig.update_layout(showlegend=False, title_x=0.5)
        st.plotly_chart(fig)

    with tab2:
        st.subheader("📚 Outils Dataviz")
        lib_counts = multiresponse_counts(df_role["Data_viz_libraries"])
        fig = px.bar(lib_counts, orientation='h',
                     title="Outils Python les plus utilisés",
                     labels={'value': 'Nombre', 'index': 'Bibliothèque'},
                     color='value',
                     color_continuous_scale='Plasma')
        fig.update_layout(showlegend=False, title_x=0.5)
        st.plotly_chart(fig)

    with tab3:
        st.subheader("📦 Outils / plateformes de Machine Learning")
        ml_counts = multiresponse_counts(df_role["Ml_frameworks"])
        fig = px.bar(ml_counts, orientation='h',
                     title="Outils / Plateformes de ML",
                     labels={'value': 'Nombre', 'index': 'Outil'},
                     color='value',
                     color_continuous_scale='Plasma')
        fig.update_layout(showlegend=False, title_x=0.5)
        st.plotly_chart(fig)

    ROLE_OPTIONS = [
        "Analyze and understand data to influence product or business decisions",
        "Build and/or run the data infrastructure that my business uses for storing, analyzing, and operationalizing data",
        "Build prototypes to explore applying machine learning to new areas",
        "Build and/or run a machine learning service that operationally improves my product or workflows",
        "Experimentation and iteration to improve existing ML models",
        "Do research that advances the state of the art of machine learning",
        "None of these activities are an important part of my role at work",
        "Other"
    ]

    def role_counts(series):
        counts = {}
        for response in series.dropna():
            for option in ROLE_OPTIONS:
                if option in response:
                    counts[option] = counts.get(option, 0) + 1
        return pd.Series(counts).sort_values(ascending=False)

    with tab4:
        st.subheader("📈 Tâches effectuées")
        task_counts = role_counts(df_role["Role/Activities"])
        fig = px.bar(task_counts, orientation='h',
                 title="Répartition des tâches effectuées",
                 labels={'value': 'Nombre', 'index': 'Tâche'},
                 color='value',
                 color_continuous_scale='Plasma')
        fig.update_layout(showlegend=False, title_x=0.5)
        st.plotly_chart(fig)

    with tab5:
        st.subheader("👩‍💻Expérience en programmation")
        xp_counts = multiresponse_counts(df_role["Coding_experience"])
        fig = px.bar(xp_counts, orientation='h',
                 title="Expérience en programmation",
                 labels={'value': 'Nombre', 'index': 'Tâche'},
                 color='value',
                 color_continuous_scale='Plasma')
        fig.update_layout(showlegend=False, title_x=0.5)
        st.plotly_chart(fig)

    ##Avec plasma modifié (code moins compliqué)
    import plotly.express as px

    with tab5:
        st.subheader("👩‍💻Expérience en programmation - moins compliqué")

        # Comptage par Age et Expérience
        xp_counts = df_role.groupby(["Age", "Coding_experience"]).size().reset_index(name="count")

        # Graphique avec palette Plasma (déjà intégrée)
        fig = px.bar(
            xp_counts,
            x="count",
            y="Age",
            color="Coding_experience",
            orientation="h",
            title="Expérience en programmation par âge",
            labels={'count': 'Nombre', 'Coding_experience': 'Expérience'},
            color_discrete_sequence=px.colors.sequential.Plasma  # palette prête
        )

        fig.update_layout(
            barmode="stack",   # barres empilées
            title_x=0.5
        )

        st.plotly_chart(fig)

    ##Avec couleur plasma mais code compliqué
    import plotly.express as px
    import plotly.colors as pc

    with tab5:
        st.subheader("👩‍💻Expérience en programmation - code compliqué")

        # Comptage par Age et Expérience
        xp_counts = df_role.groupby(["Age", "Coding_experience"]).size().reset_index(name="count")

        # Générer une palette Plasma discrète (nb de catégories = nb d'expériences uniques)
        n_colors = xp_counts["Coding_experience"].nunique()
        plasma_colors = px.colors.sample_colorscale("Plasma", [i/(n_colors-1) for i in range(n_colors)])

        # Graphique
        fig = px.bar(
            xp_counts,
            x="count",
            y="Age",
            color="Coding_experience",
            orientation="h",
            title="Expérience en programmation par âge",
            labels={'count': 'Nombre', 'Coding_experience': 'Expérience'},
            color_discrete_sequence=plasma_colors  # palette plasma appliquée aux catégories
        )

        fig.update_layout(
            barmode="stack",   # barres empilées
            title_x=0.5
        )

        st.plotly_chart(fig)
    
    with tab6:
        st.subheader("🛠️ IDE les plus utilisés")
        lib_counts = multiresponse_counts(df_role["IDE"])
        fig = px.bar(lib_counts, orientation='h',
                     title="IDE les plus populaires",
                     labels={'value': 'Nombre', 'index': 'Bibliothèque'},
                     color='value',
                     color_continuous_scale='Plasma')
        fig.update_layout(showlegend=False, title_x=0.5)
        st.plotly_chart(fig)

#------------------------------------------------------------------------------------
    
# ==========================================================
# PAGE : Clustering des profils
# ==========================================================
elif page == "Clustering des profils":   # (ou: elif page == pages[5]:)

    st.header("🧠 Clustering des profils (K-Means)")

    # ------------------------------------------------------
    # ✅ Explication (avant les imports)
    # ------------------------------------------------------
    st.markdown("""
    ### ℹ️ Important
    Le **clustering (K-Means)** a été exécuté **dans le notebook** pour :
    - éviter de recalculer le modèle à chaque refresh Streamlit,
    - garantir un résultat stable et reproductible,
    - accélérer l’application.

    Ici, Streamlit **ne refait pas l’entraînement**.
    Il **charge uniquement** le fichier de résultats : `data/clustered_profiles.csv`.
    """)

    # ------------------------------------------------------
    # Imports nécessaires UNIQUEMENT pour afficher les résultats
    # (pas besoin de sklearn ici)
    # ------------------------------------------------------
    import os
    from pathlib import Path
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # ------------------------------------------------------
    # Chemin robuste (évite les erreurs "file not found")
    # ------------------------------------------------------
    BASE_DIR = Path(__file__).resolve().parent
    DATA_PATH = BASE_DIR / "data" / "clustered_profiles.csv"

    @st.cache_data
    def load_clustered_csv(path: Path) -> pd.DataFrame:
        return pd.read_csv(path)

    # Vérification existence du fichier
    if not DATA_PATH.exists():
        st.error("❌ Fichier introuvable : `data/clustered_profiles.csv`")
        st.markdown(f"""
        **Chemin attendu :** `{DATA_PATH}`

        ✅ Solution :
        1) Vérifie que tu as bien un dossier **data** dans le même dossier que `final.py`  
        2) Mets dedans le fichier **clustered_profiles.csv** généré depuis le notebook  
        3) Relance Streamlit
        """)
        st.stop()

    # ------------------------------------------------------
    # Chargement des résultats
    # ------------------------------------------------------
    df_clusters = load_clustered_csv(DATA_PATH)

    if "Cluster" not in df_clusters.columns:
        st.error("❌ La colonne `Cluster` n'existe pas dans le fichier CSV.")
        st.write("Colonnes trouvées :", list(df_clusters.columns))
        st.stop()

    st.success(f"✅ Résultats chargés : {len(df_clusters):,} lignes")
    st.dataframe(df_clusters.head(10))

    # ------------------------------------------------------
    # 1) Répartition des clusters (camembert)
    # ------------------------------------------------------
    st.subheader("📌 Répartition des répondants par cluster")
    counts = df_clusters["Cluster"].value_counts().sort_index()

    fig1, ax1 = plt.subplots()
    ax1.pie(
        counts,
        labels=[f"Cluster {i}" for i in counts.index],
        autopct="%1.1f%%",
        startangle=90
    )
    ax1.axis("equal")
    st.pyplot(fig1)
   
    st.markdown("""
        ### 📊 Interprétation du graphique

        On observe que le **Cluster 0 est majoritaire**, représentant environ 40-45 % des répondants.  
        Cela signifie que la majorité des professionnels ont un profil technique similaire.

        Les **Clusters 1 et 2** représentent des profils intermédiaires, moins fréquents mais significatifs.  
        Le **Cluster 3** est minoritaire, ce qui indique un profil plus spécifique ou spécialisé.

        👉 Conclusion : le clustering permet d’identifier clairement plusieurs types de profils dans l’industrie de la Data.
        """)

    # ------------------------------------------------------
    # 2) Profils dominants par cluster (tableau)
    # ------------------------------------------------------
    st.subheader("🔎 Profils dominants par cluster")

    # Colonnes attendues (celles que tu utilisais pour définir tes profils)
    cluster_cols = [
        "job_title",
        "Coding_experience",
        "programming_languages",
        "IDE",
        "Hosted_notebook",
        "Computing_platform"
    ]

    missing = [c for c in cluster_cols if c not in df_clusters.columns]
    if missing:
        st.warning("⚠️ Certaines colonnes attendues manquent dans le CSV :")
        st.write(missing)
        st.info("➡️ Vérifie que tu as bien sauvegardé ces colonnes dans le notebook.")
        st.stop()

    summary = df_clusters.groupby("Cluster")[cluster_cols].agg(lambda s: s.value_counts().index[0])
    st.dataframe(summary)

    st.markdown("""
        ### 🔎 Analyse des profils dominants

        Le tableau montre les caractéristiques principales de chaque cluster.

        - Le **Cluster 0** correspond souvent à des profils expérimentés (Data Scientist avec plusieurs années d’expérience).
        - Les **Clusters 1 et 2** regroupent plutôt des étudiants ou juniors avec 1-2 ans d’expérience.
        - Le **Cluster 3** représente un profil intermédiaire.

        👉 Conclusion : le clustering distingue bien les niveaux d’expérience et les outils utilisés par les professionnels.
        """)
    st.markdown("""
        ### ✅ Conclusion du clustering
                    
        Le clustering met en évidence plusieurs profils techniques dans l’industrie de la Data.  
        On distingue notamment des profils expérimentés, intermédiaires et débutants, avec des outils et plateformes différents.

        👉 Ces résultats peuvent aider les entreprises à mieux comprendre les compétences présentes sur le marché.
        """)
    # ------------------------------------------------------
    # 3) Radar plot (comparaison des profils)
    # ------------------------------------------------------
    st.subheader("🕸️ Visualisation radar des profils")

    encoded = pd.get_dummies(summary).astype(int)
    normed = encoded.div(encoded.max(axis=0).replace(0, 1))

    labels = list(normed.columns)
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig2, ax2 = plt.subplots(figsize=(8, 6), subplot_kw=dict(polar=True))
    for c_idx, row in normed.iterrows():
        values = row.tolist() + row.tolist()[:1]
        ax2.plot(angles, values, label=f"Cluster {c_idx}")
        ax2.fill(angles, values, alpha=0.1)

    ax2.set_theta_offset(np.pi / 2)
    ax2.set_theta_direction(-1)
    ax2.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=8)
    ax2.set_title("Comparaison des clusters par caractéristiques (échelles normalisées)", pad=20)
    ax2.legend(loc="upper right", bbox_to_anchor=(1.15, 1.1))
    st.pyplot(fig2)

    st.markdown("""
        ### 🧭 Interprétation du radar des profils

        Le radar compare les clusters sur plusieurs caractéristiques.

        On remarque que :
        - Certains clusters utilisent davantage **Kaggle ou Jupyter**,
        - D’autres privilégient **Colab ou Binder**,
        - Les niveaux d’expérience varient selon les groupes.

        """)
    
    
    # ============================================================
# BONUS : Expérience en programmation par cluster
# Graphique SEUL avec titre
# ============================================================

    needed_cols = {"Cluster", "Coding_experience"}

    if not needed_cols.issubset(df_clusters.columns):
        st.warning("⚠️ Colonnes manquantes : Cluster ou Coding_experience")
    else:
        import plotly.express as px

        # Copie du dataframe
        df_plot = df_clusters.copy()

        # Important : Cluster en catégorie pour avoir une vraie légende
        df_plot["Cluster"] = df_plot["Cluster"].astype(str)

        # Comptage
        exp_counts = (
            df_plot.groupby(["Cluster", "Coding_experience"])
            .size()
            .reset_index(name="count")
        )

        # Ordre logique des expériences
        order_exp = [
            "< 1 years",
            "1-2 years",
            "3-5 years",
            "5-10 years",
            "10-20 years",
            "20+ years"
        ]

        fig = px.bar(
            exp_counts,
            x="Coding_experience",
            y="count",
            color="Cluster",
            barmode="group",
            category_orders={"Coding_experience": order_exp},
            title="📊 Répartition des niveaux d’expérience par cluster"
        )

        fig.update_layout(
            xaxis_title="Expérience",
            yaxis_title="Nombre",
            title_x=0.2
        )

        st.plotly_chart(fig, use_container_width=True)
    st.caption("Ce graphique montre la répartition des niveaux d’expérience pour chaque cluster.")
# ----------------------------
# 4️⃣ Pages 5 : Conclusion
# ----------------------------
if page == pages[6] :
    st.title("✅ Conclusion")
    ("""
    Cette étude, basée sur les réponse au sondage Kaggle 2020, met en évidence la grande diversité des profils
    au sein de l'industrie de la Data.

    **Principaux renseignements :**
    - Les outils et plateformes varient fortement selon le niveau d’expérience.
    - plusieurs métiers coexistent : Data Scientist, Data Analyst, Machine Learnind Engineer, etc.
    - Python domine largement les langages utilisés, souvent associé à Jupyter et Colab.

    **Perspectives :**
    - Etendre l'étude à d'autres années pour observer les tendances d'évolution.
    - Expérimenter différents algorithmes de clustering pour affiner la segmentation des profils
    - Mettre en place un modèle prédictif capable d'anticiper le rôle ou le salaire en fonction des outils
    utilisés.
    - Croiser ces résultats avec les données du marché de l'emploi pour mesurer l'adéquation entre compétences
    et besoin du marché.

    """)
    afficher_auteurs_sidebar()

# ----------------------------


# 4️⃣ Pages 6 : Remerciements
# ----------------------------
if page == pages[7] :
    st.title("🙏 Merci pour votre attention")
    st.image(
        "https://images.unsplash.com/photo-1520975922071-a6ef851e39b0",
        caption=" Et d’avoir exploré avec moi 🚀",
        use_container_width =True
    )
    afficher_auteurs_sidebar()

