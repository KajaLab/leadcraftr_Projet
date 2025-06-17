from .utils_rework import *
from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.oauth2 import service_account
from google.cloud import bigquery
from .config import config
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#credentials = service_account.Credentials.from_service_account_file(config["CREDENTIALS_PATH"])     ==> A SUPPRIMER CAR IMPORT DEPUIS .utils_rework
#client = bigquery.Client(project=config["PROJECT_ID"], credentials=credentials)
# Modèles Pydantic pour valider les données d'entrée
class FreelanceInput(BaseModel):
    mission_statement: str
    title: str
    main_sector: str
    city: str
    remote: str
    preferred_tone: str
    preferred_style: str
    name: str
    daily_rate: float
    top3_skills: str

class ProspectInput(BaseModel):
    mission_statement: str
    contact_role: str
    sector: str
    city: str
    remote: str
    target_tone: str
    company: str
    main_contact: str
    company_size: str
    funding_stage: str

class MailRequest(BaseModel):
    freelance: dict
    prospect: dict
    basic_mail_content: str = ""

@app.get("/")
def root():
    return {'message': "Hi, The API is running!"}

####################################################################################################
###                                           Freelance                                         ####
####################################################################################################

#@app.get("/match_freelance")
@app.post("/match_freelance")
async def match_freelance(freelance: FreelanceInput):
    try:
        # Charger les données des prospects
        prospect_df = load_prospect_data()
        freelance_df = pd.DataFrame({"name": [freelance.name], "mission_statement": [freelance.mission_statement],
                                     "title": [freelance.title], "main_sector": [freelance.main_sector],
                                     "city": [freelance.city], "remote": [freelance.remote],
                                     "preferred_tone": [freelance.preferred_tone],
                                     "preferred_style": [freelance.preferred_style],
                                     "daily_rate": [freelance.daily_rate], "top3_skills": [freelance.top3_skills]})

        # Prétraiter les données
        freelance_df, prospect_df = prepare_data(freelance_df, prospect_df)
        freelance_df, prospect_df = prepare_categorical_features(freelance_df, prospect_df)

        # Trouver les 20 meilleurs prospects
        top_prospects = get_top_20_prospects(freelance_df.iloc[0], prospect_df)

        if top_prospects.empty:
            return {"message": "No prospects found within the 40km radius or fulfilling remote criteria."}

        # Convertir en format JSON pour le frontend
        return top_prospects.to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during matching: {str(e)}")

@app.post("/generate_mail_freelance")
async def generate_mail_freelance(request: MailRequest):
    try:
        freelance = request.freelance
        prospect = request.prospect
        previous_mail_content = request.basic_mail_content

        # Valider les champs requis
        required_freelance_fields = ["name", "title", "main_sector", "city", "remote", "preferred_tone", "preferred_style", "daily_rate", "top3_skills"]
        required_prospect_fields = ["main_contact", "contact_role", "sector", "city", "remote", "target_tone", "company", "company_size", "funding_stage"]

        if not all(field in freelance for field in required_freelance_fields):
                raise HTTPException(status_code=400, detail="Missing required freelance fields")
        if not all(field in prospect for field in required_prospect_fields):
            raise HTTPException(status_code=400, detail="Missing required prospect fields")

        mail = freelance_mail_generator(freelance, prospect, previous_mail_content)
        return JSONResponse(content={"email": mail})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating email: {str(e)}")

####################################################################################################
###                                           Prospect                                          ####
####################################################################################################

#@app.get("/match_prospect")
@app.post("/match_prospect")
async def match_prospect(prospect: ProspectInput):
    try:
        # Charger les données des freelances
        freelance_df = load_freelance_data()
        prospect_df = pd.DataFrame({"main_contact": [prospect.main_contact], "mission_statement": [prospect.mission_statement],
                                    "contact_role": [prospect.contact_role], "sector": [prospect.sector],
                                    "city": [prospect.city], "remote": [prospect.remote],
                                    "target_tone": [prospect.target_tone], "company": [prospect.company],
                                    "company_size": [prospect.company_size], "funding_stage": [prospect.funding_stage]})

        # Prétraiter les données
        freelance_df, prospect_df = prepare_data(freelance_df, prospect_df)
        freelance_df, prospect_df = prepare_categorical_features(freelance_df, prospect_df)

        # Trouver les 20 meilleurs freelances
        top_freelances = get_top_20_freelances(prospect_df.iloc[0], freelance_df)

        if top_freelances.empty:
            return {"message": "No freelances found within the 40km radius or fulfilling remote criteria."}

        # Convertir en format JSON pour le frontend
        return top_freelances.to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during matching: {str(e)}")

@app.post("/generate_mail_prospect")
async def generate_mail_prospect(request: MailRequest):
    try:
        freelance = request.freelance
        prospect = request.prospect
        previous_mail_content = request.basic_mail_content

        # Valider les champs requis
        required_freelance_fields = ["name", "title", "main_sector", "city", "remote", "preferred_tone", "daily_rate", "top3_skills"]
        required_prospect_fields = ["main_contact", "contact_role", "sector", "city", "remote", "target_tone", "company", "company_size", "funding_stage"]

        if not all(field in freelance for field in required_freelance_fields):
            raise HTTPException(status_code=400, detail="Missing required freelance fields")
        if not all(field in prospect for field in required_prospect_fields):
            raise HTTPException(status_code=400, detail="Missing required prospect fields")

        mail = prospect_mail_generator(prospect, freelance, previous_mail_content)
        return JSONResponse(content={"email": mail})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating email: {str(e)}")
