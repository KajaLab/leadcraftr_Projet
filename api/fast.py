from packagename.main import predict
from .utils import *
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from google.oauth2 import service_account
from google.cloud import bigquery
from .config import config
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

credentials = service_account.Credentials.from_service_account_file(config["CREDENTIALS_PATH"])
client = bigquery.Client(project=config["PROJECT_ID"], credentials=credentials)

@app.get("/")
def root():
    return {'message': "Hi, The API is running!"}


@app.get("/match")
def match(mission_statement: str = Query(..., min_length=10)):
    try:
        # Charger le vectorizer et les données
        vectorizer = load_vectorizer()
        prospects = load_prospect_data()

        # Convertir les vecteurs (string → list → sparse)
        if isinstance(prospects["tfidf_vector"].iloc[0], str):
            prospects["tfidf_vector"] = prospects["tfidf_vector"].apply(eval)
        from scipy.sparse import csr_matrix
        prospects["tfidf_vector"] = prospects["tfidf_vector"].apply(lambda x: csr_matrix([x]))

        # Vectoriser la mission
        vec = vectorizer.transform([mission_statement])

        # Matching
        top_leads = get_top_20_leads(vec, prospects)

        # Nettoyage pour le frontend
        return top_leads.drop(columns=["tfidf_vector"]).to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}

@app.post("/generate_mail")
# def generate_mail(request: Request):
#     data = request.json()
#     freelance = data.get("freelance", {})
#     prospect = data.get("prospect", {})
#     return mail_generator(freelance, prospect)

async def generate_mail(request: Request):
    try:
        data = await request.json()
        freelance = data.get("freelance", {})
        prospect = data.get("prospect", {})
        mail = mail_generator(freelance, prospect)
        return JSONResponse(content={"email": mail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
