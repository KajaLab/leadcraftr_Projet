import pandas as pd
import random
import json

def update_mission_statement_prospects():
    # Load dataset
    df = pd.read_csv("generate_datasets/prospects_dataset.csv")

    # Define templates by sector
    templates = {
        "FinTech": [
            "Pioneering {adjective} FinTech solutions to {action} financial processes, leveraging {focus} for {company_size} to enhance user experiences and drive innovation.",
            "Delivering {adjective} financial platforms, {action} efficiency with {focus} to empower {company_size} in asset management."
        ],
        "GreenTech": [
            "Advancing {adjective} green technologies to {action} sustainability, leveraging {focus} for {company_size} to reduce environmental impact.",
            "Driving {adjective} eco-innovation, {action} a greener future with {focus} for {company_size}."
        ],
        "Wellness/Bien-Être": [
            "Crafting {adjective} wellness solutions to {action} health, leveraging {focus} for {company_size} to enhance well-being.",
            "Empowering {adjective} health platforms, {action} holistic wellness with {focus} for {company_size}."
        ],
        "Marketing": [
            "Delivering {adjective} marketing strategies to {action} brand growth, leveraging {focus} for {company_size} to engage audiences.",
            "Transforming {adjective} campaigns, {action} visibility with {focus} for {company_size}."
        ],
        "Tech/SaaS": [
            "Innovating {adjective} SaaS platforms to {action} operations, leveraging {focus} for {company_size} to drive efficiency.",
            "Empowering {adjective} digital transformation, {action} success with {focus} for {company_size}."
        ],
        "Retail/E-commerce": [
            "Providing {adjective} e-commerce solutions to {action} shopping experiences, leveraging {focus} for {company_size}.",
            "Transforming {adjective} retail platforms, {action} customer satisfaction with {focus} for {company_size}."
        ],
        "Éducation/Ed-Tech": [
            "Revolutionizing {adjective} education platforms to {action} learning, leveraging {focus} for {company_size}.",
            "Empowering {adjective} academic success, {action} outcomes with {focus} for {company_size}."
        ],
        "Design": [
            "Crafting {adjective} designs to {action} brand identity, leveraging {focus} for {company_size} to engage users.",
            "Transforming {adjective} visuals, {action} experiences with {focus} for {company_size}."
        ]
    }

    # Dynamic elements
    actions = ["streamline", "optimize", "revolutionize", "enhance", "empower", "transform", "drive", "accelerate", "maximize", "innovate"]
    focuses = ["data analytics", "cutting-edge technology", "user-centric design", "sustainability", "customer engagement", "interactive tools", "scalable platforms", "creative visuals"]
    adjectives = {
        "Créatif": ["innovative", "dynamic", "visionary"],
        "Professionnel": ["reliable", "robust", "trusted"],
        "Premium": ["premium", "high-quality", "exclusive"],
        "Bienveillant": ["inclusive", "accessible", "supportive"],
        "Énergique": ["vibrant", "dynamic", "engaging"],
        "Sérieux": ["strategic", "results-driven", "disciplined"]
    }

    def generate_mission(row):
        sector = row["secteur"]
        company_size = row["company_size"].split()[0].lower()
        tone = row["tonalite_cible"]
        role = row["role_contact"]

        # Select random template
        template = random.choice(templates.get(sector, templates["FinTech"]))

        # Select adjective based on tone
        adjective = random.choice(adjectives.get(tone, ["effective"]))

        # Select action and focus
        action = random.choice(actions)
        focus = random.choice(focuses)

        # Adjust focus based on role
        if role == "Head of Data":
            focus = "data analytics" if "data" not in focus else focus
        elif role == "CTO":
            focus = "cutting-edge technology" if "tech" not in focus else focus
        elif role == "Head of Marketing":
            focus = "customer engagement" if "engage" not in focus else focus
        elif role == "CEO":
            action = random.choice(["drive", "pioneer", "transform"])  # Visionary actions

        # Generate mission statement
        mission = template.format(adjective=adjective, action=action, focus=focus, company_size=company_size)

        # Ensure 30–40 words
        words = mission.split()
        if len(words) > 40:
            mission = " ".join(words[:40]) + "."
        elif len(words) < 30:
            mission += " with scalable, user-focused solutions."

        return mission

    # Generate mission statements
    mission_dict = {str(row["prospect_id"]): generate_mission(row) for _, row in df.iterrows()}

    # # Save to JSON
    with open("generate_datasets/prospects_mission_statements.json", "w", encoding="utf-8") as f:
        json.dump(mission_dict, f, ensure_ascii=False, indent=2)

    # Load original CSV
    df = pd.read_csv("generate_datasets/prospects_dataset.csv")

    # Load JSON with new mission statements
    with open("generate_datasets/prospects_mission_statements.json", "r") as f:
        mission_data = json.load(f)

    # Update mission_statement column based on prospect_id
    df["mission_statement"] = df["prospect_id"].astype(str).map(mission_data)

    # Save updated CSV
    df.to_csv("generate_datasets/updated_prospects_dataset.csv", index=False, encoding="utf-8")

if __name__ == "__main__":
    update_mission_statement_prospects()
