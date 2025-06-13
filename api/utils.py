from langchain.chat_models import init_chat_model
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import vstack
import pandas as pd
import joblib
from google.cloud import storage, bigquery
from google.oauth2 import service_account
import tempfile
import string
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from .config import config

def get_bq_client():
    credentials = service_account.Credentials.from_service_account_file(
        "/home/yahyaad/code/KajaLab/leadcraftr_Projet/notebooks/bigquery-sa-key.json"
    )
    return bigquery.Client(project=PROJECT_ID, credentials=credentials)


# Loading
def load_vectorizer():
    credentials = service_account.Credentials.from_service_account_file(config["CREDENTIALS_PATH"])
    storage_client = storage.Client(project=config["PROJECT_ID"], credentials=credentials)
    bucket = storage_client.bucket(config["BUCKET_NAME"])
    blob = bucket.blob(config["VECTORIZER_BLOB"])

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        blob.download_to_filename(tmp_file.name)
        vectorizer = joblib.load(tmp_file.name)

    return vectorizer

def load_prospect_data():
    client = get_bq_client()
    query = f"SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}` WHERE mission_statement IS NOT NULL"
    return client.query(query).to_dataframe()

# Preprocessing
def get_wordnet_pos(word):
    """Map POS tag to first character for WordNetLemmatizer"""
    tag = pos_tag([word])[0][1][0].lower()  # Get first letter of POS tag
    return{'n': 'n', 'v': 'v', 'a': 'a', 'r': 'r'}.get(tag, 'n')

def cleaning(sentence):
    # Basic cleaning
    sentence = sentence.strip().lower()
    sentence = ''.join(char for char in sentence if not char.isdigit())
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))

    # Tokenization
    tokenized_sentence = word_tokenize(sentence)

    # Stopwords removal
    stop_words = set(stopwords.words('english'))
    tokenized_sentence_cleaned = [w for w in tokenized_sentence if w not in stop_words]

    # Lemmatization with correct POS tagging
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in tokenized_sentence_cleaned]

    return ' '.join(lemmatized)

# Matching
def get_top_20_leads(freelance_vec, prospect_df):
    prospect_matrix = vstack([v for v in prospect_df["tfidf_vector"]])
    similarities = cosine_similarity(freelance_vec, prospect_matrix).flatten()
    top_20_idx = similarities.argsort()[-20:][::-1]
    return prospect_df.iloc[top_20_idx].assign(similarity=similarities[top_20_idx])

# Mail
def mail_generator(freelance, prospect, previous_mail_content=''):
    model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
    prospect = prospect.copy()

    prompt = f"""
            If there is no previous email, ignore the following instruction.

            Otherwise, based on the content below, rewrite the previous email ('{previous_mail_content}') to better match the desired tone and style, while keeping its intent.

            Write a clear, professional, and personalized cold email in English, addressed to {prospect['main_contact']} ({prospect['contact_role']})
            at {prospect['company']}, located in {prospect['city']} and operating in the {prospect['sector']} sector.

            You are {freelance['name']}, a {freelance['title']} based in {freelance['city']}, specialized in the {freelance['main_sector']} sector.
            You provide services with expertise in {freelance['top3_skills']}, at a daily rate of {freelance['daily_rate']} EUR (remote: {freelance['remote']}).
            Your mission is: {freelance['mission_statement']}.

            The company is a {prospect['company_size']} at the {prospect['funding_stage']} stage, and remote work availability is {prospect['remote']}.

            The email should:
            - Open with a brief and relevant introduction.
            - Present the value you can bring in 2–3 concise sentences.
            - Be business-oriented and adapted to the company's context.
            - Match the company's tone: {prospect['target_tone']}, while also reflecting your preferred tone: {freelance['preferred_tone']} and style: {freelance['preferred_style']}.
            - End with a clear, actionable closing (e.g., propose a short call or ask for availability).
            - Sign the email with your name.

            Ensure the language is polite, direct, and free from repetition or generic phrases. Avoid placeholders or uncertain formulations.
            Return only the body of the email (no subject line or explanation).
            """

    try:
        response = model.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)
    except Exception as e:
        print(f"Error : {e}")
        content = f"ERROR: {e}"

    content = response.__dict__['content']
    return content
