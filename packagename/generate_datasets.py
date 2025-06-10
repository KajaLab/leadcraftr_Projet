import random, csv
from pathlib import Path
from faker import Faker

# Global parameters
N_FREELANCES = 300
N_PROSPECTS = 3000

# Sectors
SECTORS = [
    "Tech/SaaS", "Marketing", "Design", "FinTech", "Wellness",
    "Retail/E-commerce", "GreenTech", "Education/Ed-Tech"
]

# Freelance titles by sector
TITLE_POOL = {
    "Tech/SaaS": [
        "Software Development",
        "Product Management",
        "UI/UX Design",
        "Data Analysis",
        "Cloud Management"
    ],
    "Marketing": [
        "Digital Marketing",
        "Content Creation",
        "Marketing Data Analysis",
        "Social Media Management",
        "Brand Strategy"
    ],
    "Design": [
        "Graphic Design",
        "UI/UX Design",
        "Prototyping",
        "Creative Direction",
        "Interaction Design"
    ],
    "FinTech": [
        "Secure System Development",
        "Financial Analysis",
        "Regulatory Compliance",
        "Blockchain Expertise",
        "Risk Management"
    ],
    "Wellness": [
        "Health & Wellness Coaching",
        "Wellness Content Creation",
        "Community Management",
        "Digital Marketing",
        "Nutrition Expertise"
    ],
    "Retail/E-commerce": [
        "E-commerce Platform Management",
        "Digital Marketing",
        "Supply Chain Management",
        "Sales Data Analysis",
        "Customer Service"
    ],
    "GreenTech": [
        "Renewable Energy Expertise",
        "Environmental Impact Analysis",
        "Project Management",
        "Sustainable Engineering",
        "ESG Standards Knowledge"
    ],
    "Education/Ed-Tech": [
        "Instructional Design",
        "LMS Platform Management",
        "E-learning Content Development",
        "Educational Data Analysis",
        "Ed-Tech Integration"
    ]
}

# Skills by sector
SKILLS = {
    "Tech/SaaS": ["Python", "Docker", "AWS", "CI/CD", "PostgreSQL", "FastAPI"],
    "Marketing": ["SEO", "Google Ads", "Analytics", "Copywriting", "Email Marketing"],
    "Design": ["Figma", "User Research", "Prototyping", "AdobeXD", "Design Systems"],
    "FinTech": ["SQL", "Risk Modeling", "AML/KYC", "Python", "PowerBI"],
    "Wellness": ["Yoga", "Pilates", "Community Management", "Nutrition", "Copywriting"],
    "Retail/E-commerce": ["Shopify", "Facebook Ads", "Supply-Chain", "Data Analytics", "Customer Support"],
    "GreenTech": ["LCA", "Carbon Accounting", "IoT", "Energy Modeling", "Project Management"],
    "Education/Ed-Tech": ["Pedagogy", "Storyline360", "Python", "HTML5", "Learning Analytics"]
}

# Tone and style options
TONE_OPTIONS = ["Professional", "Friendly", "Energetic", "Creative", "Serious", "Premium"]
STYLE_OPTIONS = ["Formal", "Warm", "Storytelling"]

# Financial proxies
COMPANY_SIZE = ["Startup (1-20)", "SME (21-200)", "Mid-size (201-1000)", "Enterprise (1000+)"]
FUNDING_STAGES = ["Pre-Seed", "Seed", "Series A", "Series B", "Series C+"]

def ticket_size_class(size: str, stage: str):
    if size.startswith("Enterprise") or stage in ["Series B", "Series C+"]:
        return "High"
    elif size.startswith("Startup") and stage in ["Pre-Seed", "Seed"]:
        return "Low"
    else:
        return "Medium"



def main():
    fake = Faker("en_US")
    Faker.seed(42)
    random.seed(42)

    Path("generate_datasets").mkdir(exist_ok=True)

    # Freelance dataset
    with open("generate_datasets/freelances_dataset.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "freelance_id", "name", "title", "main_sector",
            "top3_skills", "city", "daily_rate", "mission_statement",
            "preferred_tone", "preferred_style", "remote"
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
                random.choice(STYLE_OPTIONS),
                random.choice(["Yes", "No"])
            ])

    # Prospect dataset
    with open("generate_datasets/prospects_dataset.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "prospect_id", "company", "sector", "main_contact",
            "contact_role", "city", "mission_statement",
            "company_size", "funding_stage", "ticket_size_class",
            "target_tone", "remote"
        ])
        for pid in range(1, N_PROSPECTS + 1):
            sec = random.choice(SECTORS)
            size = random.choice(COMPANY_SIZE)
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
                random.choice(TONE_OPTIONS),
                random.choice(["Yes", "No"])
            ])

        print("✅  CSVs generated in /generate_datasets")

if __name__ == "__main__":
    main()
