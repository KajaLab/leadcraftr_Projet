import random
import csv
import json
import os
import pandas as pd

def update_freelance_mission_statements():
    """
    Updates freelancer mission statements with enriched templates, aligned tone adjectives, and proper punctuation.
    """
    def generate_mission_statement(row):
        sector = row['main_sector']
        skills = row['top3_skills'].split('|')[:2]  # Use first two skills
        name = row['name']
        tone = row['preferred_tone']  # Changed from 'tone' to 'preferred_tone'

        # Sector-specific tone adjectives, aligned with dataset tones
        tone_adjectives = {
            'Marketing': {
                'Professional': ['trusted', 'strategic', 'reliable', 'insightful', 'impactful'],
                'Serious': ['results-driven', 'disciplined', 'focused', 'analytical', 'precise'],
                'Friendly': ['approachable', 'engaging', 'warm', 'collaborative', 'supportive'],
                'Creative': ['innovative', 'visionary', 'original', 'imaginative', 'artistic'],
                'Premium': ['high-quality', 'exclusive', 'sophisticated', 'elite', 'prestigious'],
                'Energetic': ['vibrant', 'dynamic', 'passionate', 'bold', 'enthusiastic']
            },
            'Tech/SaaS': {
                'Professional': ['reliable', 'technical', 'scalable', 'robust', 'efficient'],
                'Serious': ['data-driven', 'methodical', 'structured', 'secure', 'precise'],
                'Friendly': ['approachable', 'user-friendly', 'collaborative', 'supportive', 'accessible'],
                'Creative': ['pioneering', 'visionary', 'inventive', 'forward-thinking', 'innovative'],
                'Premium': ['elite', 'high-performance', 'exclusive', 'advanced', 'sophisticated'],
                'Energetic': ['dynamic', 'agile', 'cutting-edge', 'proactive', 'energetic']
            },
            'Retail/E-commerce': {
                'Professional': ['trusted', 'strategic', 'customer-focused', 'reliable', 'efficient'],
                'Serious': ['results-driven', 'analytical', 'disciplined', 'focused', 'optimized'],
                'Friendly': ['approachable', 'customer-centric', 'engaging', 'supportive', 'warm'],
                'Creative': ['innovative', 'stylish', 'trendy', 'imaginative', 'creative'],
                'Premium': ['luxury', 'exclusive', 'high-quality', 'sophisticated', 'premium'],
                'Energetic': ['vibrant', 'dynamic', 'engaging', 'bold', 'enthusiastic']
            },
            'FinTech': {
                'Professional': ['secure', 'compliant', 'trusted', 'strategic', 'reliable'],
                'Serious': ['data-driven', 'disciplined', 'analytical', 'focused', 'rigorous'],
                'Friendly': ['accessible', 'trustworthy', 'approachable', 'supportive', 'transparent'],
                'Creative': ['innovative', 'visionary', 'forward-thinking', 'pioneering', 'creative'],
                'Premium': ['elite', 'high-security', 'exclusive', 'sophisticated', 'prestigious'],
                'Energetic': ['dynamic', 'proactive', 'bold', 'agile', 'innovative']
            },
            'Education/Ed-Tech': {
                'Professional': ['reliable', 'structured', 'educational', 'insightful', 'effective'],
                'Serious': ['focused', 'analytical', 'results-driven', 'disciplined', 'methodical'],
                'Friendly': ['approachable', 'engaging', 'supportive', 'accessible', 'warm'],
                'Creative': ['innovative', 'imaginative', 'inspiring', 'visionary', 'creative'],
                'Premium': ['high-quality', 'exclusive', 'sophisticated', 'elite', 'prestigious'],
                'Energetic': ['dynamic', 'inspiring', 'motivational', 'engaging', 'enthusiastic']
            },
            'GreenTech': {
                'Professional': ['sustainable', 'reliable', 'strategic', 'efficient', 'impactful'],
                'Serious': ['data-driven', 'focused', 'analytical', 'disciplined', 'rigorous'],
                'Friendly': ['approachable', 'eco-friendly', 'supportive', 'collaborative', 'ethical'],
                'Creative': ['innovative', 'visionary', 'pioneering', 'eco-innovative', 'creative'],
                'Premium': ['high-impact', 'exclusive', 'sophisticated', 'elite', 'prestigious'],
                'Energetic': ['dynamic', 'proactive', 'passionate', 'bold', 'inspiring']
            },
            'Design': {
                'Professional': ['polished', 'reliable', 'user-centric', 'strategic', 'effective'],
                'Serious': ['focused', 'disciplined', 'analytical', 'precise', 'structured'],
                'Friendly': ['approachable', 'engaging', 'user-friendly', 'collaborative', 'warm'],
                'Creative': ['innovative', 'visionary', 'artistic', 'imaginative', 'creative'],
                'Premium': ['luxury', 'exclusive', 'high-quality', 'sophisticated', 'elite'],
                'Energetic': ['vibrant', 'dynamic', 'bold', 'inspiring', 'enthusiastic']
            },
            'Wellness': {
                'Professional': ['trusted', 'structured', 'health-focused', 'reliable', 'effective'],
                'Serious': ['focused', 'disciplined', 'results-driven', 'analytical', 'methodical'],
                'Friendly': ['approachable', 'supportive', 'engaging', 'warm', 'holistic'],
                'Creative': ['innovative', 'inspiring', 'holistic', 'visionary', 'creative'],
                'Premium': ['high-quality', 'exclusive', 'sophisticated', 'elite', 'prestigious'],
                'Energetic': ['vibrant', 'inspiring', 'motivational', 'dynamic', 'enthusiastic']
            }
        }

        # Sector-specific actions
        sector_actions = {
            'Marketing': ['amplify', 'engage', 'elevate', 'optimize', 'captivate', 'promote', 'convert', 'inspire'],
            'Tech/SaaS': ['streamline', 'innovate', 'scale', 'automate', 'enhance', 'secure', 'develop', 'integrate'],
            'Retail/E-commerce': ['boost', 'optimize', 'convert', 'engage', 'personalize', 'grow', 'streamline', 'attract'],
            'FinTech': ['secure', 'optimize', 'innovate', 'streamline', 'protect', 'enhance', 'comply', 'empower'],
            'Education/Ed-Tech': ['inspire', 'enhance', 'engage', 'simplify', 'personalize', 'empower', 'transform', 'educate'],
            'GreenTech': ['sustain', 'innovate', 'reduce', 'enhance', 'promote', 'optimize', 'preserve', 'empower'],
            'Design': ['create', 'inspire', 'enhance', 'craft', 'visualize', 'transform', 'refine', 'innovate'],
            'Wellness': ['inspire', 'nurture', 'empower', 'enhance', 'promote', 'balance', 'transform', 'engage']
        }

        # Dictionary of English templates by sector (6 templates per sector)
        templates = {
            'Marketing': [
                f"{name} delivers {random.choice(tone_adjectives[sector][tone])} strategies using {skills[0]} and {skills[1]} to {random.choice(sector_actions[sector])} your brand's reach and impact.",
                f"With {name}, {random.choice(tone_adjectives[sector][tone])} expertise in {skills[0]} and {skills[1]} {random.choice(sector_actions[sector])}s your marketing for measurable growth.",
                f"{name} crafts {random.choice(tone_adjectives[sector][tone])} campaigns with {skills[0]} and {skills[1]} to {random.choice(sector_actions[sector])} audiences and drive success.",
                f"Partner with {name} for {random.choice(tone_adjectives[sector][tone])} {skills[0]} and {skills[1]} solutions that {random.choice(sector_actions[sector])} your brand's visibility.",
                f"{name} transforms marketing with {random.choice(tone_adjectives[sector][tone])} {skills[0]} and {skills[1]}, {random.choice(sector_actions[sector])}ing engagement and results.",
                f"With {name}'s {random.choice(tone_adjectives[sector][tone])} approach to {skills[0]} and {skills[1]}, I {random.choice(sector_actions[sector])} your brand for lasting impact."
            ],
            'Tech/SaaS': [
                f"{name} builds {random.choice(tone_adjectives[sector][tone])} solutions with {skills[0]} and {skills[1]} to {random.choice(sector_actions[sector])} your tech operations efficiently.",
                f"With {name}, {random.choice(tone_adjectives[sector][tone])} expertise in {skills[0]} and {skills[1]} {random.choice(sector_actions[sector])}s your digital infrastructure.",
                f"{name} drives {random.choice(tone_adjectives[sector][tone])} innovation using {skills[0]} and {skills[1]} to {random.choice(sector_actions[sector])} scalable tech solutions.",
                f"Partner with {name} for {random.choice(tone_adjectives[sector][tone])} {skills[0]} and {skills[1]} solutions that {random.choice(sector_actions[sector])} your tech growth.",
                f"{name} empowers your business with {random.choice(tone_adjectives[sector][tone])} {skills[0]} and {skills[1]}, {random.choice(sector_actions[sector])}ing efficiency.",
                f"With {name}'s {random.choice(tone_adjectives[sector][tone])} approach to {skills[0]} and {skills[1]}, I {random.choice(sector_actions[sector])} robust systems."
            ],
            'Retail/E-commerce': [
                f"{name} boosts {random.choice(tone_adjectives[sector][tone])} e-commerce with {skills[0]} and {skills[1]} to {random.choice(sector_actions[sector])} sales and engagement.",
                f"With {name}, {random.choice(tone_adjectives[sector][tone])} expertise in {skills[0]} and {skills[1]} {random.choice(sector_actions[sector])}s your retail success.",
                f"{name} creates {random.choice(tone_adjectives[sector][tone])} shopping experiences using {skills[0]} and {skills[1]} to {random.choice(sector_actions[sector])} revenue.",
                f"Partner with {name} for {random.choice(tone_adjectives[sector][tone])} {skills[0]} and {skills[1]} solutions that {random.choice(sector_actions[sector])} customer loyalty.",
                f"{name} drives {random.choice(tone_adjectives[sector][tone])} growth with {skills[0]} and {skills[1]}, {random.choice(sector_actions[sector])}ing e-commerce performance.",
                f"With {name}'s {random.choice(tone_adjectives[sector][tone])} approach to {skills[0]} and {skills[1]}, I {random.choice(sector_actions[sector])} your online sales."
            ],
            'FinTech': [
                f"{name} delivers {random.choice(tone_adjectives[sector][tone])} FinTech solutions with {skills[0]} and {skills[1]} to {random.choice(sector_actions[sector])} financial security.",
                f"With {name}, {random.choice(tone_adjectives[sector][tone])} expertise in {skills[0]} and {skills[1]} {random.choice(sector_actions[sector])}s your FinTech goals.",
                f"{name} builds {random.choice(tone_adjectives[sector][tone])} platforms using {skills[0]} and {skills[1]} to {random.choice(sector_actions[sector])} trust and compliance.",
                f"Partner with {name} for {random.choice(tone_adjectives[sector][tone])} {skills[0]} and {skills[1]} solutions that {random.choice(sector_actions[sector])} financial innovation.",
                f"{name} empowers {random.choice(tone_adjectives[sector][tone])} FinTech ventures with {skills[0]} and {skills[1]}, {random.choice(sector_actions[sector])}ing efficiency.",
                f"With {name}'s {random.choice(tone_adjectives[sector][tone])} approach to {skills[0]} and {skills[1]}, I {random.choice(sector_actions[sector])} secure systems."
            ],
            'Education/Ed-Tech': [
                f"{name} creates {random.choice(tone_adjectives[sector][tone])} learning platforms with {skills[0]} and {skills[1]} to {random.choice(sector_actions[sector])} educational outcomes.",
                f"With {name}, {random.choice(tone_adjectives[sector][tone])} expertise in {skills[0]} and {skills[1]} {random.choice(sector_actions[sector])}s student success.",
                f"{name} designs {random.choice(tone_adjectives[sector][tone])} EdTech solutions using {skills[0]} and {skills[1]} to {random.choice(sector_actions[sector])} engagement.",
                f"Partner with {name} for {random.choice(tone_adjectives[sector][tone])} {skills[0]} and {skills[1]} solutions that {random.choice(sector_actions[sector])} learning experiences.",
                f"{name} inspires {random.choice(tone_adjectives[sector][tone])} education with {skills[0]} and {skills[1]}, {random.choice(sector_actions[sector])}ing academic growth.",
                f"With {name}'s {random.choice(tone_adjectives[sector][tone])} approach to {skills[0]} and {skills[1]}, I {random.choice(sector_actions[sector])} innovative education."
            ],
            'GreenTech': [
                f"{name} advances {random.choice(tone_adjectives[sector][tone])} sustainability with {skills[0]} and {skills[1]} to {random.choice(sector_actions[sector])} environmental impact.",
                f"With {name}, {random.choice(tone_adjectives[sector][tone])} expertise in {skills[0]} and {skills[1]} {random.choice(sector_actions[sector])}s green innovation.",
                f"{name} drives {random.choice(tone_adjectives[sector][tone])} eco-solutions using {skills[0]} and {skills[1]} to {random.choice(sector_actions[sector])} sustainability.",
                f"Partner with {name} for {random.choice(tone_adjectives[sector][tone])} {skills[0]} and {skills[1]} solutions that {random.choice(sector_actions[sector])} eco-impact.",
                f"{name} promotes {random.choice(tone_adjectives[sector][tone])} GreenTech with {skills[0]} and {skills[1]}, {random.choice(sector_actions[sector])}ing sustainability.",
                f"With {name}'s {random.choice(tone_adjectives[sector][tone])} approach to {skills[0]} and {skills[1]}, I {random.choice(sector_actions[sector])} green progress."
            ],
            'Design': [
                f"{name} crafts {random.choice(tone_adjectives[sector][tone])} visuals with {skills[0]} and {skills[1]} to {random.choice(sector_actions[sector])} your brand identity.",
                f"With {name}, {random.choice(tone_adjectives[sector][tone])} expertise in {skills[0]} and {skills[1]} {random.choice(sector_actions[sector])}s your design impact.",
                f"{name} creates {random.choice(tone_adjectives[sector][tone])} designs using {skills[0]} and {skills[1]} to {random.choice(sector_actions[sector])} user engagement.",
                f"Partner with {name} for {random.choice(tone_adjectives[sector][tone])} {skills[0]} and {skills[1]} solutions that {random.choice(sector_actions[sector])} visual appeal.",
                f"{name} transforms brands with {random.choice(tone_adjectives[sector][tone])} {skills[0]} and {skills[1]}, {random.choice(sector_actions[sector])}ing design excellence.",
                f"With {name}'s {random.choice(tone_adjectives[sector][tone])} approach to {skills[0]} and {skills[1]}, I {random.choice(sector_actions[sector])} stunning visuals."
            ],
            'Wellness': [
                f"{name} promotes {random.choice(tone_adjectives[sector][tone])} wellness with {skills[0]} and {skills[1]} to {random.choice(sector_actions[sector])} health and balance.",
                f"With {name}, {random.choice(tone_adjectives[sector][tone])} expertise in {skills[0]} and {skills[1]} {random.choice(sector_actions[sector])}s well-being.",
                f"{name} creates {random.choice(tone_adjectives[sector][tone])} wellness programs using {skills[0]} and {skills[1]} to {random.choice(sector_actions[sector])} engagement.",
                f"Partner with {name} for {random.choice(tone_adjectives[sector][tone])} {skills[0]} and {skills[1]} solutions that {random.choice(sector_actions[sector])} health outcomes.",
                f"{name} inspires {random.choice(tone_adjectives[sector][tone])} well-being with {skills[0]} and {skills[1]}, {random.choice(sector_actions[sector])}ing vitality.",
                f"With {name}'s {random.choice(tone_adjectives[sector][tone])} approach to {skills[0]} and {skills[1]}, I {random.choice(sector_actions[sector])} holistic wellness."
            ]
        }

        # Select a random template for the sector
        mission = random.choice(templates.get(sector, templates['Marketing']))

        # Ensure 30–40 words
        words = mission.split()
        if len(words) > 40:
            mission = ' '.join(words[:40]) + '.'
        elif len(words) < 30:
            mission = mission.rstrip('.') + ', with tailored, impactful strategies.'

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
        essential_columns = {'name', 'main_sector', 'top3_skills', 'preferred_tone'}
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

    print("✅ Freelancer mission statements updated successfully.")

def update_prospect_mission_statements():
    """
    Met à jour les mission statements des prospects
    """
    # Load dataset
    df = pd.read_csv("generate_datasets/prospects_dataset.csv")

    # Define templates by sector
    templates = {
        "FinTech": [
            "We enable {company_size} to {action} financial operations with {adjective} solutions that integrate {focus}.",
            "{company_size} rely on our {adjective} FinTech services to {action} transparency and user empowerment through {focus}.",
            "At the heart of our mission: {action} digital finance with {adjective} tools built on {focus}.",
            "Transforming finance for {company_size} through {adjective} platforms designed to {action} financial decisions via {focus}.",
            "Bringing {adjective} financial clarity to {company_size} by {action} operations with {focus}.",
            "Making finance simpler for {company_size}: we {action} systems with {adjective} technology powered by {focus}."
        ],
        "GreenTech": [
            "Empowering {company_size} to {action} sustainability goals using {adjective} green innovation based on {focus}.",
            "Our {adjective} solutions help {company_size} {action} environmental impact through smart use of {focus}.",
            "{company_size} partner with us to {action} climate action thanks to {adjective} technologies driven by {focus}.",
            "At the intersection of ecology and innovation, we {action} a cleaner future using {adjective} tools powered by {focus}.",
            "From energy to waste, our mission is to help {company_size} {action} better ecological performance through {focus}.",
            "We support {company_size} in {action} green value chains using {adjective} systems and data from {focus}."
        ],
        "Wellness/Bien-Être": [
            "Helping {company_size} {action} wellness outcomes through {adjective} solutions built around {focus}.",
            "We design {adjective} health solutions to help {company_size} {action} mental and physical balance using {focus}.",
            "{company_size} trust our {adjective} platforms to {action} holistic wellness through {focus}.",
            "Supporting better living for {company_size} by {action} self-care habits with {adjective} digital tools based on {focus}.",
            "Empowering health journeys: we help {company_size} {action} well-being with {adjective} methods powered by {focus}.",
            "Wellness made smarter for {company_size}—we {action} care strategies through {focus} and {adjective} innovations."
        ],
        "Marketing": [
            "Helping {company_size} {action} brand visibility with {adjective} marketing tools powered by {focus}.",
            "Our {adjective} strategies enable {company_size} to {action} audience engagement using {focus}.",
            "{company_size} grow their reach by {action} campaigns designed with {adjective} creativity and {focus}.",
            "From insight to impact: we help {company_size} {action} market share through {focus} and {adjective} execution.",
            "We {action} brand presence for {company_size} by mixing {focus} insights with {adjective} storytelling.",
            "Marketing reimagined for {company_size}: we {action} digital growth through {adjective} techniques and {focus}."
        ],
        "Tech/SaaS": [
            "We help {company_size} {action} business operations with {adjective} SaaS platforms driven by {focus}.",
            "Scaling success: our {adjective} software empowers {company_size} to {action} everyday efficiency through {focus}.",
            "{company_size} modernize their infrastructure by {action} scalable solutions built on {adjective} architecture and {focus}.",
            "Reimagining work for {company_size}: we {action} productivity through {adjective} platforms and {focus}.",
            "Powering transformation in {company_size} with {adjective} digital tools that {action} performance through {focus}.",
            "With {adjective} SaaS innovation and smart {focus}, we help {company_size} {action} critical tasks efficiently."
        ],
        "Retail/E-commerce": [
            "Helping {company_size} {action} shopping journeys with {adjective} online experiences built using {focus}.",
            "We support {company_size} in {action} conversion rates through {adjective} e-commerce platforms and {focus}.",
            "Retail made seamless: we {action} user interactions for {company_size} using {adjective} solutions powered by {focus}.",
            "{company_size} boost customer loyalty by {action} purchase experiences with {focus} and {adjective} tech.",
            "Bringing retail online: our {adjective} platforms help {company_size} {action} engagement through {focus}.",
            "We create {adjective} digital storefronts for {company_size}, enabling them to {action} user satisfaction via {focus}."
        ],
        "Éducation/Ed-Tech": [
            "We help {company_size} {action} learning outcomes using {adjective} education platforms based on {focus}.",
            "{company_size} improve learner engagement through our {adjective} digital tools that {action} performance with {focus}.",
            "Education made better: we {action} academic success with {adjective} innovations rooted in {focus}.",
            "Empowering minds: our {adjective} tools help {company_size} {action} learning through {focus}.",
            "Transforming education for {company_size} with {adjective} methods that {action} development through {focus}.",
            "At the core of our mission: to {action} education for {company_size} using {adjective} systems driven by {focus}."
        ],
        "Design": [
            "Helping {company_size} {action} brand storytelling with {adjective} designs powered by {focus}.",
            "We {action} visual experiences for {company_size}, combining {adjective} aesthetics and {focus}.",
            "{company_size} elevate their identity through our {adjective} design systems based on {focus}.",
            "Reimagining digital presence: we help {company_size} {action} with {focus} and {adjective} design.",
            "Shaping how {company_size} are perceived by {action} their interfaces through {adjective} and strategic {focus}.",
            "With {focus} and a {adjective} mindset, we help {company_size} {action} user engagement through design."
        ]
    }

        # Nouveaux dictionnaires dynamiques sectoriels
    dynamic_elements = {
            "FinTech": {
                "actions": ["streamline transactions", "modernise compliance", "democratise finance", "enhance security", "optimise asset flows"],
                "focuses": ["blockchain innovation", "AI-powered risk analysis", "regtech tools", "real-time data", "automated trading platforms"],
                "adjectives": ["secure", "agile", "innovative", "scalable", "intelligent"]
            },
            "GreenTech": {
                "actions": ["accelerate sustainability", "reduce carbon footprint", "promote circular economy", "enhance energy efficiency", "drive environmental impact"],
                "focuses": ["clean energy", "eco-conscious design", "carbon offset platforms", "waste reduction", "smart grids"],
                "adjectives": ["sustainable", "eco-friendly", "impact-driven", "climate-conscious", "resilient"]
            },
            "Wellness/Bien-Être": {
                "actions": ["promote healthy lifestyles", "support mental wellbeing", "enable holistic health", "simplify wellness journeys", "empower daily self-care"],
                "focuses": ["personalised coaching", "mindfulness platforms", "wearable integration", "nutrition tracking", "habit-building tools"],
                "adjectives": ["caring", "supportive", "balanced", "nurturing", "holistic"]
            },
            "Marketing": {
                "actions": ["boost brand visibility", "amplify engagement", "target customer growth", "enhance campaign performance", "optimise brand storytelling"],
                "focuses": ["data-driven strategy", "multichannel outreach", "creative content", "SEO/SEM tools", "influencer activation"],
                "adjectives": ["strategic", "creative", "compelling", "disruptive", "audience-focused"]
            },
            "Tech/SaaS": {
                "actions": ["scale infrastructure", "enable digital transformation", "simplify workflows", "automate processes", "redefine operations"],
                "focuses": ["cloud-native architecture", "DevOps agility", "API-first development", "AI-assisted automation", "scalable frameworks"],
                "adjectives": ["scalable", "intelligent", "modular", "resilient", "future-ready"]
            },
            "Retail/E-commerce": {
                "actions": ["optimise user journeys", "enhance shopping experiences", "streamline logistics", "personalise product discovery", "amplify conversions"],
                "focuses": ["omnichannel commerce", "real-time recommendations", "customer data insights", "mobile-first platforms", "secure checkout systems"],
                "adjectives": ["customer-first", "frictionless", "intuitive", "responsive", "conversion-driven"]
            },
            "Éducation/Ed-Tech": {
                "actions": ["democratise access", "enhance learning outcomes", "empower educators", "support lifelong learning", "simplify content delivery"],
                "focuses": ["adaptive learning", "gamification", "remote classrooms", "AI tutoring", "data-driven assessments"],
                "adjectives": ["accessible", "learner-focused", "interactive", "transformational", "inclusive"]
            },
            "Design": {
                "actions": ["elevate brand aesthetics", "streamline visual identity", "empower user interaction", "redefine storytelling", "enhance UX/UI coherence"],
                "focuses": ["human-centred design", "responsive layouts", "brand narrative", "motion design", "prototyping tools"],
                "adjectives": ["visually striking", "user-centric", "bold", "elegant", "cohesive"]
            }
        }
    def generate_mission(row):
        sector = row["sector"]
        company_size = row["company_size"].split()[0].lower()
        tone = row["target_tone"]
        role = row["contact_role"]

        # Sélection des templates par secteur
        template = random.choice(templates.get(sector, templates["FinTech"]))

        # Élément dynamique sectoriel ou fallback générique
        elements = dynamic_elements.get(sector, dynamic_elements["FinTech"])

        adjective = random.choice(elements["adjectives"])
        action = random.choice(elements["actions"])
        focus = random.choice(elements["focuses"])

        # Ajustement selon le rôle
        if role == "Head of Data":
            focus = "data analytics"
        elif role == "CTO":
            focus = "cutting-edge technology"
        elif role == "Head of Marketing":
            focus = "customer engagement"
        elif role == "CEO":
            action = random.choice(["drive", "pioneer", "transform"])

        mission = template.format(adjective=adjective, action=action, focus=focus, company_size=company_size)

        # Estimer la longueur attendue du template sélectionné
        expected_length = len(template.split())

        # Réajuster la mission en fonction de la longueur attendue
        words = mission.split()
        if len(words) > expected_length + 4:  # autorise un léger débordement
            mission = " ".join(words[:expected_length + 4]) + "."
        elif len(words) < expected_length - 3:  # tolère un léger déficit
            mission += " Our approach ensures measurable results aligned with your goals."

        return mission

    # Générer les mission statements
    mission_dict = {str(row["prospect_id"]): generate_mission(row) for _, row in df.iterrows()}

    with open("generate_datasets/prospects_mission_statements.json", "w", encoding="utf-8") as f:
        json.dump(mission_dict, f, ensure_ascii=False, indent=2)

    df = pd.read_csv("generate_datasets/prospects_dataset.csv")
    with open("generate_datasets/prospects_mission_statements.json", "r") as f:
        mission_data = json.load(f)

    df["mission_statement"] = df["prospect_id"].astype(str).map(mission_data)
    df.to_csv("generate_datasets/updated_prospects_dataset.csv", index=False, encoding="utf-8")

    print("✅ Prospects mission statements updated successfully.")



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
