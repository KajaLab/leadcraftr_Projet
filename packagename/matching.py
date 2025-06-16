# Imports
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import vstack

def get_top_20_leads(freelance_vec, prospect_df):
    """
    Retourne les 20 prospects les plus proches du vecteur freelance donné.
    """
    prospect_matrix = vstack(prospect_df["tfidf_vector"].values)
    similarities = cosine_similarity(freelance_vec, prospect_matrix).flatten()
    top_20_idx = similarities.argsort()[-20:][::-1]
    return prospect_df.iloc[top_20_idx].assign(similarity=similarities[top_20_idx])

def get_top_20_freelances(prospect_vec, freelance_df):
    """
    Retourne les 20 freelances les plus proches du vecteur prospect donné.
    """
    prospect_matrix = vstack(freelance_df["tfidf_vector"].values)
    similarities = cosine_similarity(prospect_vec, prospect_matrix).flatten()
    top_20_idx = similarities.argsort()[-20:][::-1]
    return freelance_df.iloc[top_20_idx].assign(similarity=similarities[top_20_idx])
