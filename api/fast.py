from packagename.main import predict
from utils import *
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def root():
    return {'message': "Hi, The API is running!"}

@app.get("/match")
def match(mission_statement: str = Query(..., min_length=10)):
    # Charger les données + vectorizer
    vectorizer = load_vectorizer()
    prospects = load_prospect_data()

    # Convertir les vecteurs de strings en listes (si besoin)
    if isinstance(prospects["tfidf_vector"].iloc[0], str):
        prospects["tfidf_vector"] = prospects["tfidf_vector"].apply(eval)

    # Convertir en sparse
    prospects["tfidf_vector"] = prospects["tfidf_vector"].apply(
        lambda x: vectorizer.transform([""]).__class__((x,))
    )

    # Vectoriser l'entrée
    mission_statement = cleaning(mission_statement)
    vec = vectorizer.transform([mission_statement])

    # Obtenir top 20
    top_leads = get_top_20_leads(vec, prospects)

    # Nettoyer pour réponse JSON
    columns_to_return = [col for col in top_leads.columns if col != "tfidf_vector"]
    return top_leads[columns_to_return].to_dict(orient="records")

@app.post("/generate_mail")
def generate_mail(request: Request):
    data = request.json()
    freelance = data.get("freelance", {})
    prospect = data.get("prospect", {})
    return mail_generator(freelance, prospect)
