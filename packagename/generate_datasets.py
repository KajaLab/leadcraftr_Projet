#On génère un dataset fictif
import random, csv
from pathlib import Path
from faker import Faker

#Paramètres globaux
N_FREELANCES = 300 #Nombre de freelances à générer
N_PROSPECTS = 3000 #Nombre de prospects à générer

#Secteurs d'activité
SECTORS = [
    "Tech/SaaS", "Marketing", "Design", "FinTech", "Wellness/Bien-Être",
    "Retail/E-commerce", "GreenTech", "Éducation/Ed-Tech"
]
#Titre du freelance par secteur
TITLE_POOL = {
    "Tech/SaaS": [
        "Développement logiciel (Python, JavaScript)",
        "Gestion de produit",
        "Conception UI/UX",
        "Analyse de données",
        "Gestion de cloud (AWS, Azure)"
    ],
    "Marketing": [
        "Marketing digital (SEO, SEM)",
        "Création de contenu",
        "Analyse de données marketing",
        "Gestion des réseaux sociaux",
        "Stratégie de marque"
    ],
    "Design": [
        "Design graphique (Adobe Creative Suite)",
        "Conception UI/UX (Figma, Sketch)",
        "Prototypage",
        "Direction créative",
        "Design d’interaction"
    ],
    "FinTech": [
        "Développement de systèmes sécurisés",
        "Analyse financière",
        "Conformité réglementaire (KYC, AML)",
        "Expertise blockchain",
        "Gestion des risques"
    ],
    "Wellness/Bien-Être": [
        "Coaching santé/bien-être",
        "Création de contenu wellness",
        "Gestion de communauté",
        "Marketing digital",
        "Connaissance en nutrition"
    ],
    "Retail/E-commerce": [
        "Gestion de plateformes e-commerce (Shopify)",
        "Marketing digital",
        "Gestion de la chaîne d’approvisionnement",
        "Analyse des données de vente",
        "Service client"
    ],
    "GreenTech": [
        "Expertise en énergies renouvelables",
        "Analyse d’impact environnemental",
        "Gestion de projets",
        "Ingénierie durable",
        "Connaissance des normes ESG"
    ],
    "Éducation/Ed-Tech": [
        "Conception pédagogique",
        "Gestion de plateformes LMS",
        "Développement de contenu e-learning",
        "Analyse des données éducatives",
        "Intégration de technologies éducatives"
    ]
}

#Compétences par secteur
SKILLS =  {
    "Tech/SaaS": [
        "Python", "Docker", "AWS", "CI/CD", "PostgreSQL", "FastAPI"
    ],
    "Marketing": [
        "SEO", "Google Ads", "Analytics", "Copywriting", "Email Marketing"
    ],
    "Design": [
        "Figma", "User Research", "Prototypage", "AdobeXD", "Design Systems"
    ],
    "FinTech": [
        "SQL", "Risk Modeling", "AML/KYC", "Python", "PowerBI"
    ],
    "Wellness/Bien-Être": [
        "Yoga", "Pilates", "Community Management", "Nutrition", "Copywriting"
    ],
    "Retail/E-commerce": [
        "Shopify", "Facebook Ads", "Supply-Chain", "Data Analytics", "Customer Support"
    ],
    "GreenTech": [
        "LCA", "Carbon Accounting", "IoT", "Energy Modeling", "Project Management"
    ],
    "Éducation/Ed-Tech": [
        "Pedagogy", "Storyline360", "Python", "HTML5", "Learning Analytics"
    ],
}


#Listes pour le ton et le style
TONE_OPTIONS = ["Professionnel", "Bienveillant", "Énergique", "Créatif", "Sérieux", "Premium"]
STYLE_OPTIONS = ["Formel", "Chaleureux", "Storytelling"]

#Proxies financiers | Taille de société + Stade de financement
COMPANY_SIZE = ["Startup (1-20)", "PME (21-200", "ETI (201-1000)", "Groupe (1000+)"]
FUNDING_STAGES = ["Pre-Seed", "Seed", "Series A", "Series B", "Series C+"]

def ticket_size_class(size:str, stage:str):
    #Retourne Low / Medium / High selon la capacité de l'entreprise
    if size.startswith("Groupe") or stage in ["Series B", "Series C+"]:
        return "High"
    elif size.startswith("Startup") and stage in ["Pre-Seed", "Seed"]:
        return "Low"
    else:
        return "Medium"


def main():
    #Génère les 2 CSV dans le dossier "data"
    #On instancie Faker en français + seeds pour la reproductibilité
    fake = Faker("fr_FR")
    Faker.seed(42)
    random.seed(42)

    #Je créé le dossier data
    Path("generate_datasets").mkdir(exist_ok=True)

#Génération des freelances
    with open("generate_datasets/freelances_dataset.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "freelance_id", "nom", "titre", "secteur_principal",
            "skills_top3", "ville", "tjm", "mission_statement",
            "tonalite_preferee", "style_prefere"
        ])
        for fid in range(1, N_FREELANCES + 1):
            sec = random.choice(SECTORS)
            writer.writerow([
                fid,
                fake.name(),
                random.choice(TITLE_POOL[sec]),
                sec,
                "|".join(random.sample(SKILLS[sec], 3)),
                fake.city(),
                round(random.uniform(300, 1000), 2),
                fake.catch_phrase(),
                random.choice(TONE_OPTIONS),
                random.choice(STYLE_OPTIONS)
            ])

#Générer des prospects

    with open("generate_datasets/prospects_dataset.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "prospect_id", "societe", "secteur", "contact_principal",
            "role_contact", "ville", "mission_statement",
            "company_size", "funding_stage", "ticket_size_class",
            "tonalite_cible"
        ])
        for pid in range(1, N_PROSPECTS + 1):
            sec   = random.choice(SECTORS)
            size  = random.choice(COMPANY_SIZE)
            stage = random.choice(FUNDING_STAGES)
            writer.writerow([
                pid,
                fake.company(),
                sec,
                fake.name(),
                random.choice(["CEO", "CTO", "Head of Marketing", "Head of Data"]),
                fake.city(),
                fake.bs().capitalize(),
                size,
                stage,
                ticket_size_class(size, stage),
                random.choice(TONE_OPTIONS)
            ])

        print("✅  CSV générés dans le dossier /data")

if __name__ == "__main__":
    main()
