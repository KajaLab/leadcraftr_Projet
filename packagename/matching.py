# Imports
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def vectorize_missions(freelance_df, prospect_df):
    """Vectorise les mission statements des freelances et prospects avec TF-IDF."""
    vectorizer = TfidfVectorizer(stop_words='english')
    freelance_tfidf = vectorizer.fit_transform(freelance_df["mission_statement"])
    prospect_tfidf = vectorizer.transform(prospect_df["mission_statement"])
    return freelance_tfidf, prospect_tfidf

def get_top_20_leads(freelance_vec, prospect_tfidf, prospect_df):
    """
    Retourne les 20 prospects les plus similaires pour un vecteur freelance donné.

    Args:
        freelance_vec: Vecteur TF-IDF (1D ou 2D) du freelance (shape: (1, n_features)).
        prospect_tfidf: Matrice TF-IDF des prospects.
        prospect_df: DataFrame des prospects.

    Returns:
        DataFrame des 20 prospects les plus similaires avec score de similarité.
    """
    similarities = cosine_similarity(freelance_vec, prospect_tfidf).flatten()
    top_20_indices = similarities.argsort()[-20:][::-1]

    return prospect_df.iloc[top_20_indices].assign(
        similarity=similarities[top_20_indices]
    )

