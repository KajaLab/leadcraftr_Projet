import csv
import json
import random
import os
import pandas as pd


def update_freelance_mission_statements():
    """
    Met à jour les mission statements des freelances
    """
    def generate_mission_statement(row):
        sector = row['secteur_principal']
        skills = row['skills_top3'].split('|')[:2]  # Use first two skills for brevity
        name = row['nom']
        tone = row['tonalite_preferee']

        # Tone-specific adjectives
        tone_adjectives = {
            'Professional': ['trusted', 'reliable', 'strategic'],
            'Benevolent': ['supportive', 'inclusive', 'caring'],
            'Serious': ['results-driven', 'disciplined', 'focused'],
            'Energetic': ['vibrant', 'dynamic', 'passionate'],
            'Premium': ['high-quality', 'exclusive', 'premium'],
            'Creative': ['innovative', 'visionary', 'creative']
        }

        # Dynamic actions
        actions = ['amplify', 'streamline', 'empower', 'enhance', 'transform', 'drive', 'optimize', 'innovate', 'maximize', 'engage']

        # Dictionary of English templates by sector
        templates = {
            'Marketing': [
                f"With {name}, {random.choice(tone_adjectives.get(tone, ['effective']))} marketing strategies {random.choice(actions)} your brand using {skills[0]} and {skills[1]}. I craft campaigns to engage audiences and drive growth.",
                f"{name} delivers {random.choice(tone_adjectives.get(tone, ['effective']))} solutions in {skills[0]} and {skills[1]} to {random.choice(actions)} your marketing. I create tailored strategies for impactful business success.",
                f"{name} excels with {random.choice(tone_adjectives.get(tone, ['effective']))} expertise in {skills[0]} and {skills[1]}. I {random.choice(actions)} brand visibility through innovative, results-focused marketing campaigns."
            ],
            'Tech/SaaS': [
                f"{name} builds {random.choice(tone_adjectives.get(tone, ['effective']))} tech solutions with {skills[0]} and {skills[1]}. I {random.choice(actions)} operations through scalable, innovative platforms for your business.",
                f"With {name}, {random.choice(tone_adjectives.get(tone, ['effective']))} expertise in {skills[0]} and {skills[1]} {random.choice(actions)}s your tech projects. I deliver robust solutions for efficiency and growth.",
                f"{name} transforms ideas with {random.choice(tone_adjectives.get(tone, ['effective']))} skills in {skills[0]} and {skills[1]}. I {random.choice(actions)} digital innovation through reliable, scalable systems."
            ],
            'Retail/E-commerce': [
                f"{name} drives {random.choice(tone_adjectives.get(tone, ['effective']))} e-commerce success with {skills[0]} and {skills[1]}. I {random.choice(actions)} sales through strategic, customer-focused solutions tailored to your business.",
                f"With {name}, {random.choice(tone_adjectives.get(tone, ['effective']))} expertise in {skills[0]} and {skills[1]} {random.choice(actions)}s your retail platform. I optimize sales with innovative strategies.",
                f"{name} excels in {random.choice(tone_adjectives.get(tone, ['effective']))} {skills[0]} and {skills[1]} to {random.choice(actions)} e-commerce growth. I create seamless experiences to boost revenue."
            ],
            'FinTech': [
                f"{name} delivers {random.choice(tone_adjectives.get(tone, ['effective']))} FinTech solutions with {skills[0]} and {skills[1]}. I {random.choice(actions)} financial security through compliant, data-driven platforms.",
                f"With {name}, {random.choice(tone_adjectives.get(tone, ['effective']))} expertise in {skills[0]} and {skills[1]} {random.choice(actions)}s your FinTech goals. I build secure, innovative systems.",
                f"{name} empowers {random.choice(tone_adjectives.get(tone, ['effective']))} FinTech ventures with {skills[0]} and {skills[1]}. I {random.choice(actions)} trust through robust, compliant solutions."
            ],
            'Education/Ed-Tech': [
                f"{name} creates {random.choice(tone_adjectives.get(tone, ['effective']))} educational platforms with {skills[0]} and {skills[1]}. I {random.choice(actions)} learning outcomes through innovative, tech-driven solutions.",
                f"With {name}, {random.choice(tone_adjectives.get(tone, ['effective']))} expertise in {skills[0]} and {skills[1]} {random.choice(actions)}s education. I design engaging, data-driven learning experiences.",
                f"{name} excels in {random.choice(tone_adjectives.get(tone, ['effective']))} {skills[0]} and {skills[1]} to {random.choice(actions)} academic success. I create tailored, tech-enhanced learning tools."
            ],
            'GreenTech': [
                f"{name} advances {random.choice(tone_adjectives.get(tone, ['effective']))} sustainability with {skills[0]} and {skills[1]}. I {random.choice(actions)} environmental impact through innovative, eco-conscious solutions.",
                f"With {name}, {random.choice(tone_adjectives.get(tone, ['effective']))} expertise in {skills[0]} and {skills[1]} {random.choice(actions)}s GreenTech goals. I create efficient, sustainable solutions.",
                f"{name} drives {random.choice(tone_adjectives.get(tone, ['effective']))} eco-innovation with {skills[0]} and {skills[1]}. I {random.choice(actions)} sustainability through data-driven green technologies."
            ],
            'Design': [
                f"{name} crafts {random.choice(tone_adjectives.get(tone, ['effective']))} designs with {skills[0]} and {skills[1]}. I {random.choice(actions)} brand identity through user-centric, visually compelling solutions.",
                f"With {name}, {random.choice(tone_adjectives.get(tone, ['effective']))} expertise in {skills[0]} and {skills[1]} {random.choice(actions)}s your visuals. I create intuitive, striking designs.",
                f"{name} excels in {random.choice(tone_adjectives.get(tone, ['effective']))} {skills[0]} and {skills[1]} to {random.choice(actions)} design impact. I deliver user-focused, creative visuals."
            ],
            'Wellness': [
                f"{name} promotes {random.choice(tone_adjectives.get(tone, ['effective']))} wellness with {skills[0]} and {skills[1]}. I {random.choice(actions)} health through engaging, community-focused programs and content.",
                f"With {name}, {random.choice(tone_adjectives.get(tone, ['effective']))} expertise in {skills[0]} and {skills[1]} {random.choice(actions)}s well-being. I create tailored wellness solutions.",
                f"{name} excels in {random.choice(tone_adjectives.get(tone, ['effective']))} {skills[0]} and {skills[1]} to {random.choice(actions)} wellness. I design inspiring, health-driven experiences."
            ]
        }

        # Select a random template for the sector
        mission = random.choice(templates.get(sector, templates['Marketing']))

        # Ensure 30–40 words
        words = mission.split()
        if len(words) > 40:
            mission = ' '.join(words[:40]) + '.'
        elif len(words) < 30:
            mission += ' with scalable, user-focused strategies.'

        return mission

    # Read CSV and process data
    freelancers = []
    input_file = 'generate_datasets/freelances_dataset.csv'
    output_json = 'generate_datasets/freelances_missions_statements.json'
    output_csv = 'generate_datasets/updated_freelances_dataset.csv'

    # Check if input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file {input_file} not found")

    with open(input_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        # Validate only essential columns for mission generation
        essential_columns = {'nom', 'secteur_principal', 'skills_top3', 'tonalite_preferee'}
        if not essential_columns.issubset(reader.fieldnames):
            missing = essential_columns - set(reader.fieldnames)
            raise ValueError(f"Missing essential columns for mission generation: {missing}")

        # Get all fieldnames from the CSV
        all_fieldnames = reader.fieldnames

        for row in reader:
            new_mission = generate_mission_statement(row)

            # Create a new row dict with all existing columns
            freelancer_data = {}
            for field in all_fieldnames:
                freelancer_data[field] = row[field]

            # Add or update the mission_statement column
            freelancer_data['mission_statement'] = new_mission

            freelancers.append(freelancer_data)

    # Write to JSON file
    with open(output_json, 'w', encoding='utf-8') as jsonfile:
        json.dump(freelancers, jsonfile, ensure_ascii=False, indent=4)

    # Write to new CSV file with all original columns + mission_statement
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        # Create fieldnames list: all original columns + mission_statement if not already present
        fieldnames = list(all_fieldnames)
        if 'mission_statement' not in fieldnames:
            fieldnames.append('mission_statement')

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(freelancers)

    print(f"Files '{output_json}' and '{output_csv}' have been created successfully.")


def update_prospect_mission_statements():
    """
    Met à jour les mission statements des prospects
    """
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

    # Save to JSON
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

    print("Prospects mission statements updated successfully.")


def main():
    """
    Fonction principale qui permet d'exécuter les deux mises à jour
    """
    print("=== Mise à jour des Mission Statements ===")

    choice = input("\nQue souhaitez-vous faire ?\n1. Mettre à jour les freelances\n2. Mettre à jour les prospects\n3. Mettre à jour les deux\nVotre choix (1/2/3): ")

    if choice == "1":
        print("\n--- Mise à jour des freelances ---")
        update_freelance_mission_statements()
    elif choice == "2":
        print("\n--- Mise à jour des prospects ---")
        update_prospect_mission_statements()
    elif choice == "3":
        print("\n--- Mise à jour des freelances ---")
        update_freelance_mission_statements()
        print("\n--- Mise à jour des prospects ---")
        update_prospect_mission_statements()
    else:
        print("Choix invalide. Veuillez relancer le programme.")


if __name__ == "__main__":
    main()
