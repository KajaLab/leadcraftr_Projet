# Imports
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import vstack


def vectorize_missions(freelance_df, prospect_df):
    """
    Vectorise les mission statements avec TF-IDF et stocke les vecteurs dans la colonne 'tfidf_vector'.
    """
    # Copie des textes bruts
    all_missions = pd.concat([
        freelance_df["mission_statement"],
        prospect_df["mission_statement"]
    ])

    vectorizer = TfidfVectorizer(stop_words='english')
    vectorizer.fit(all_missions)

    # Ajoute les vecteurs TF-IDF dans une nouvelle colonne
    freelance_df = freelance_df.copy()
    prospect_df = prospect_df.copy()

    freelance_df["tfidf_vector"] = list(vectorizer.transform(freelance_df["mission_statement"]))
    prospect_df["tfidf_vector"] = list(vectorizer.transform(prospect_df["mission_statement"]))
    return freelance_df, prospect_df, vectorizer


def get_top_20_leads(freelance_vec, prospect_df):
    """
    Retourne les 20 prospects les plus proches du vecteur freelance donné.
    """
    prospect_matrix = vstack(prospect_df["tfidf_vector"].values)

    similarities = cosine_similarity(freelance_vec, prospect_matrix).flatten()
    top_20_idx = similarities.argsort()[-20:][::-1]

    return prospect_df.iloc[top_20_idx].assign(similarity=similarities[top_20_idx])
