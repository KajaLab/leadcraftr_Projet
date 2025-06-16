import string
import nltk
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer

# Ensure necessary NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger_eng')

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

def vectorize_missions_dataset(freelance_df, prospect_df):
    """
    Vectorise les mission statements avec TF-IDF et stocke les vecteurs dans la colonne 'tfidf_vector'.
    """
    # Copie des textes bruts
    all_missions = pd.concat([
        freelance_df["tfidf_vector"],
        prospect_df["tfidf_vector"]
    ])

    vectorizer = TfidfVectorizer(stop_words='english')
    vectorizer.fit(all_missions)

    # Ajoute les vecteurs TF-IDF dans une nouvelle colonne
    freelance_df = freelance_df.copy()
    prospect_df = prospect_df.copy()

    freelance_df["tfidf_vector"] = list(vectorizer.transform(freelance_df["tfidf_vector"]))
    prospect_df["tfidf_vector"] = list(vectorizer.transform(prospect_df["tfidf_vector"]))
    return freelance_df, prospect_df, vectorizer


# Ouvre les csv
freelance_df = pd.read_csv('generate_datasets/freelances_dataset.csv', index_col='freelance_id').reset_index(drop=True)
prospect_df = pd.read_csv('generate_datasets/prospects_dataset.csv', index_col='prospect_id').reset_index(drop=True)

# Clean les datas
freelance_df['tfidf_vector'] = freelance_df['mission_statement'].apply(cleaning)
prospect_df['tfidf_vector'] = prospect_df['mission_statement'].apply(cleaning)

# Vectorise les datas
freelance_df, prospect_df, vectorizer = vectorize_missions_dataset(freelance_df, prospect_df)

print(f"✅ Data vectorized and preprocessed")

# Sauvegarde des DataFrames nettoyés et vectorisés
freelance_df.to_csv('generate_datasets/freelances_dataset.csv', index=False)
prospect_df.to_csv('generate_datasets/prospects_dataset.csv', index=False)
