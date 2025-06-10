import csv
import json
import random
import os

# Function to generate a tailored mission statement in English
def generate_mission_statement(row):
    sector = row['main_sector']
    skills = row['top3_skills'].split('|')[:2]  # Use first two skills for brevity
    name = row['name']
    tone = row['preferred_tone']

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
    # Validate required columns
    required_columns = {'freelance_id', 'name', 'title', 'main_sector', 'top3_skills','city', 'daily_rate', 'mission_statement', 'preferred_tone', 'preferred_style', 'remote'}
    if not required_columns.issubset(reader.fieldnames):
        missing = required_columns - set(reader.fieldnames)
        raise ValueError(f"Missing required columns: {missing}")

    for row in reader:
        new_mission = generate_mission_statement(row)
        freelancers.append({
            'freelance_id': row['freelance_id'],
            'nom': row['name'],
            'titre': row['title'],
            'secteur_principal': row['main_sector'],
            'skills_top3': row['top3_skills'],
            'ville': row['city'],
            'tjm': row['daily_rate'],
            'mission_statement': new_mission,
            'tonalite_preferee': row['preferred_tone'],
            'style_prefere': row['preferred_style']
})

# Write to JSON file
with open(output_json, 'w', encoding='utf-8') as jsonfile:
    json.dump(freelancers, jsonfile, ensure_ascii=False, indent=4)

# Write to new CSV file
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['freelance_id', 'nom', 'titre', 'secteur_principal', 'skills_top3', 'ville', 'tjm', 'mission_statement', 'tonalite_preferee', 'style_prefere']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(freelancers)

print(f"Files '{output_json}' and '{output_csv}' have been created successfully.")
