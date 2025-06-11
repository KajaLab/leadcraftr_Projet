# Imports
import pandas as pd
import numpy as np
import time
from langchain.chat_models import init_chat_model


def mail_generator(freelance, top_20_df):
    model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

    top_20_df['mail'] = ''
    top_20_df = top_20_df.reset_index(drop=True)

    for prospect_id in range(len(top_20_df)):
        # Pause de 60s toutes les 10 requêtes
        if prospect_id > 0 and prospect_id % 10 == 0:
            print("Waiting 30 seconds to respect rate limits...")
            time.sleep(30)

        prospect = top_20_df.iloc[prospect_id]

        prompt = f"""
        Write a concise and professional cold email in English to offer your mission: {freelance['mission_statement']}
        to a company called {prospect['company']} based in {prospect['city']}, operating in the {prospect['sector']} sector.
        Your contact is {prospect['main_contact']}, who is the {prospect['contact_role']}.

        You are {freelance['name']}, a {freelance['title']} specialized in the {freelance['main_sector']} sector,
        based in {freelance['city']}. You offer services with top skills in {freelance['top3_skills']},
        at a daily rate of {freelance['daily_rate']} (remote: {freelance['remote']}).

        Highlight your main value proposition in 2–3 sentences, adapted to the needs of a company like {prospect['company']}
        (size: {prospect['company_size']}, funding stage: {prospect['funding_stage']}, remote work: {prospect['remote']}).

        Include a clear call to action. Keep the tone {freelance['preferred_tone']} and the style {freelance['preferred_style']},
        while matching the company’s target tone: {prospect['target_tone']}.
        """

        try:
            response = model.invoke(prompt)
            content = response.content if hasattr(response, "content") else str(response)
        except Exception as e:
            print(f"Error at index {prospect_id}: {e}")
            content = f"ERROR: {e}"

        top_20_df.at[prospect_id, 'mail'] = content

    return top_20_df
