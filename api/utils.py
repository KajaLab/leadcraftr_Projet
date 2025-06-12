from langchain.chat_models import init_chat_model
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import vstack
import pandas as pd
import joblib
from google.cloud import storage, bigquery
import tempfile

def load_vectorizer():
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(VECTORIZER_BLOB)

    with tempfile.NamedTemporaryFile() as tmp_file:
        blob.download_to_filename(tmp_file.name)
        return joblib.load(tmp_file.name)

def load_prospect_data():
    client = bigquery.Client(project=PROJECT_ID)
    query = f"SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}`"
    return client.query(query).to_dataframe()

def get_top_20_leads(freelance_vec, prospect_df):
    prospect_matrix = vstack([v for v in prospect_df["tfidf_vector"]])
    similarities = cosine_similarity(freelance_vec, prospect_matrix).flatten()
    top_20_idx = similarities.argsort()[-20:][::-1]
    return prospect_df.iloc[top_20_idx].assign(similarity=similarities[top_20_idx])

def mail_generator(freelance: dict, prospect: dict) -> dict:
    model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
    prospect = prospect.copy()

    prompt = f"""
    Write a clear, professional, and personalized cold email in English, addressed to {prospect['main_contact']} ({prospect['contact_role']})
    from the company {prospect['company']}, based in {prospect['city']} and operating in the {prospect['sector']} sector.

    You are {freelance['name']}, a {freelance['title']} based in {freelance['city']}, specialized in the {freelance['main_sector']} sector.
    You provide services with expertise in {freelance['top3_skills']}, at a daily rate of {freelance['daily_rate']} EUR (remote: {freelance['remote']}).
    Your mission is: {freelance['mission_statement']}

    The company is a {prospect['company_size']} at the {prospect['funding_stage']} stage, and remote work availability is {prospect['remote']}.

    The email should:
    - Open with a brief and relevant introduction.
    - Present the value you can bring to this company in 2–3 concise sentences.
    - Match the company's tone: {prospect['target_tone']}, while reflecting your preferred tone: {freelance['preferred_tone']} and style: {freelance['preferred_style']}.
    - Be business-oriented and adapted to the company's context.
    - End with a clear, actionable closing (e.g., propose a short call or ask for availability).
    - Sign with your name
    Ensure the language is polite, direct, and free from repetition or generic phrases. Avoid using placeholders or uncertain formulations.
    Return only the body of the email (no subject line or explanation).
    """
    try:
        response = model.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)
    except Exception as e:
        print(f"Error : {e}")
        content = f"ERROR: {e}"

    prospect['mail'] = content
    return content
