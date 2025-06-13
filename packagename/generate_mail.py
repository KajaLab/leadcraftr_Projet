# Imports
import pandas as pd
import numpy as np
from langchain.chat_models import init_chat_model


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
