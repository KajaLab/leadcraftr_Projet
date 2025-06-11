# Imports
import pandas as pd
import numpy as np
import time
from langchain.chat_models import init_chat_model


def mail_generator(freelance, prospect):
    """
    Génère un email de prospection personnalisé en anglais à partir des données d’un freelance et d’une entreprise cible.

    Paramètres :
    -----------
    freelance : dict
        Dictionnaire contenant les informations du freelance :
        - 'name' : Nom complet
        - 'title' : Titre ou métier
        - 'main_sector' : Secteur principal d’activité
        - 'city' : Ville
        - 'top3_skills' : Compétences clés (format texte)
        - 'daily_rate' : Tarif journalier
        - 'remote' : "Yes"/"No"
        - 'mission_statement' : Résumé de la proposition de valeur
        - 'preferred_tone' : Ton préféré (ex. : Professional)
        - 'preferred_style' : Style préféré (ex. : Storytelling)

    prospect : pandas.Series ou dict
        Informations sur l’entreprise cible :
        - 'company' : Nom de l’entreprise
        - 'city' : Ville
        - 'sector' : Secteur d’activité
        - 'main_contact' : Nom du contact principal
        - 'contact_role' : Poste du contact
        - 'company_size' : Taille de l’entreprise
        - 'funding_stage' : Stade de financement
        - 'remote' : "Yes"/"No"
        - 'target_tone' : Ton attendu côté entreprise

    Retour :
    --------
    prospect : pandas.Series ou dict
        Le même objet que `prospect` mais avec un champ supplémentaire 'mail' contenant l’email généré.
    """

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

    prospect['mail'] = response.__dict__['content']

    return prospect

