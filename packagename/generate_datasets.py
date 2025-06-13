import random
import csv
from pathlib import Path
from faker import Faker
import json
import os
import pandas as pd
import re

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

#English cities
cities_england = {
    "1": "London",
    "2": "Birmingham",
    "3": "Manchester",
    "4": "Leeds",
    "5": "Liverpool",
    "6": "Sheffield",
    "7": "Bristol",
    "8": "Newcastle upon Tyne",
    "9": "Nottingham",
    "10": "Leicester",
    "11": "Coventry",
    "12": "Kingston upon Hull",
    "13": "Bradford",
    "14": "Southampton",
    "15": "Plymouth",
    "16": "Reading",
    "17": "Stoke-on-Trent",
    "18": "Wolverhampton",
    "19": "Derby",
    "20": "Norwich",
    "21": "Swindon",
    "22": "Portsmouth",
    "23": "Luton",
    "24": "Preston",
    "25": "Milton Keynes",
    "26": "Northampton",
    "27": "Brighton and Hove",
    "28": "Bournemouth",
    "29": "Sunderland",
    "30": "Poole",
    "31": "Warrington",
    "32": "Peterborough",
    "33": "Oldham",
    "34": "Blackpool",
    "35": "Oxford",
    "36": "Stockport",
    "37": "Cambridge",
    "38": "Slough",
    "39": "Gloucester",
    "40": "Rotherham",
    "41": "Bolton",
    "42": "Blackburn",
    "43": "Middlesbrough",
    "44": "Huddersfield",
    "45": "York",
    "46": "Ipswich",
    "47": "West Bromwich",
    "48": "Grimsby",
    "49": "Southend-on-Sea",
    "50": "Birkenhead",
    "51": "Barnsley",
    "52": "Oldbury",
    "53": "Walsall",
    "54": "Telford",
    "55": "Crawley",
    "56": "Mansfield",
    "57": "Bury",
    "58": "High Wycombe",
    "59": "Dudley",
    "60": "Wigan",
    "61": "Doncaster",
    "62": "Exeter",
    "63": "Gillingham",
    "64": "Rochdale",
    "65": "Solihull",
    "66": "Basingstoke",
    "67": "Worcester",
    "68": "Sutton Coldfield",
    "69": "Chesterfield",
    "70": "Colchester",
    "71": "Eastbourne",
    "72": "Redditch",
    "73": "Lincoln",
    "74": "Cheltenham",
    "75": "Dagenham",
    "76": "Watford",
    "77": "Hartlepool",
    "78": "Halifax",
    "79": "Stevenage",
    "80": "St Helens",
    "81": "Stockton-on-Tees",
    "82": "Gateshead",
    "83": "Darlington",
    "84": "Maidstone",
    "85": "Hastings",
    "86": "Bath",
    "87": "Hemel Hempstead",
    "88": "Aylesbury",
    "89": "Scunthorpe",
    "90": "Worthing",
    "91": "Harrogate",
    "92": "Tamworth",
    "93": "Crewe",
    "94": "Chelmsford",
    "95": "Carlisle",
    "96": "Shrewsbury",
    "97": "Nuneaton",
    "98": "Bedford",
    "99": "Chester",
    "100": "Ashton-under-Lyne",
    "101": "Hereford",
    "102": "Weston-super-Mare",
    "103": "Royal Tunbridge Wells",
    "104": "Cannock",
    "105": "Wellingborough",
    "106": "Great Yarmouth",
    "107": "Kidderminster",
    "108": "Chatham",
    "109": "Stafford",
    "110": "Rugby",
    "111": "Corby",
    "112": "Smethwick",
    "113": "Keighley",
    "114": "Sale",
    "115": "Folkestone",
    "116": "Lancaster",
    "117": "Burnley",
    "118": "Taunton",
    "119": "Washington",
    "120": "Lowestoft",
    "121": "Kettering",
    "122": "Paignton",
    "123": "Runcorn",
    "124": "Cheshire West and Chester",
    "125": "Altrincham",
    "126": "Farnborough",
    "127": "Weymouth",
    "128": "Worksop",
    "129": "Boston",
    "130": "Gravesend",
    "131": "Warwick",
    "132": "Bognor Regis",
    "133": "Spalding",
    "134": "Banbury",
    "135": "Yeovil",
    "136": "Bridgwater",
    "137": "Leamington Spa",
    "138": "Margate",
    "139": "Ashford",
    "140": "Woking",
    "141": "Dewsbury",
    "142": "Accrington",
    "143": "Loughborough",
    "144": "Redcar",
    "145": "Torquay",
    "146": "Newbury",
    "147": "Burton upon Trent",
    "148": "Littlehampton",
    "149": "Carlton",
    "150": "Fareham",
    "151": "Bracknell",
    "152": "Stourbridge",
    "153": "Halesowen",
    "154": "Maidenhead",
    "155": "Marlow",
    "156": "Esher",
    "157": "Frome",
    "158": "Horsham",
    "159": "Walton-on-Thames",
    "160": "St Albans",
    "161": "Salisbury",
    "162": "Rickmansworth",
    "163": "Ramsgate",
    "164": "Northwich",
    "165": "Coalville",
    "166": "Ellesmere Port",
    "167": "Hinckley",
    "168": "Christchurch",
    "169": "Wisbech",
    "170": "Epsom",
    "171": "Letchworth",
    "172": "Dunstable",
    "173": "Canvey Island",
    "174": "Huntingdon",
    "175": "Wokingham",
    "176": "Burgess Hill",
    "177": "Kendal",
    "178": "Dorking",
    "179": "Chippenham",
    "180": "Waterlooville",
    "181": "St Neots",
    "182": "Whitstable",
    "183": "Brentwood",
    "184": "Stratford-upon-Avon",
    "185": "Godalming",
    "186": "Witney",
    "187": "Reigate",
    "188": "Ely",
    "189": "Malvern",
    "190": "Trowbridge",
    "191": "Fleet",
    "192": "Rayleigh",
    "193": "Stamford",
    "194": "Lewes",
    "195": "Bicester",
    "196": "Didcot",
    "197": "Crowborough",
    "198": "Chesham",
    "199": "Royston",
    "200": "Hertford"
}

def ticket_size_class(size: str, stage: str):
    if size.startswith("Enterprise") or stage in ["Series B", "Series C+"]:
        return "High"
    elif size.startswith("Startup") and stage in ["Pre-Seed", "Seed"]:
        return "Low"
    else:
        return "Medium"

def generate_email(first_last_name, company_or_sector, is_freelancer=False):
    try:
        name_parts = first_last_name.strip().split()
        if not name_parts:
            raise ValueError("Name cannot be empty")
        if len(name_parts) < 2:
            first = name_parts[0].lower()
            last = ""
        else:
            first = name_parts[0].lower()
            last = name_parts[-1].lower()

        first = re.sub(r'[^a-z0-9]', '', first)
        last = re.sub(r'[^a-z0-9]', '', last)
        username = f"{first}.{last}" if last else first

        if not company_or_sector:
            raise ValueError("Company or sector cannot be empty")
        domain_base = company_or_sector.lower()
        domain_base = re.sub(r'[,\s&]+', '', domain_base)
        domain_base = re.sub(r'[^a-z0-9]', '', domain_base)
        domain = f"{domain_base}freelance.com" if is_freelancer else f"{domain_base}.com"

        return f"{username}@{domain}"
    except Exception as e:
        print(f"Error generating email for {first_last_name}: {e}")
        return "error@invalid.com"

def clean_csv_in_memory(input_file):
    """
    Clean CSV file in memory and return a DataFrame, excluding malformed lines.
    """
    try:
        # Read CSV with pandas, handling quoting and bad lines
        df = pd.read_csv(
            input_file,
            encoding='utf-8',
            quoting=csv.QUOTE_NONNUMERIC,
            quotechar='"',
            on_bad_lines='warn',  # Log bad lines instead of raising error
            engine='python'  # Use python engine for robust parsing
        )

        # Debug: Print columns to diagnose
        print(f"DataFrame columns: {list(df.columns)}")

        # Validate prospect_id column
        if 'prospect_id' not in df.columns:
            raise KeyError(f"'prospect_id' column not found in {input_file}. Available columns: {list(df.columns)}")

        # Convert prospect_id to numeric
        df['prospect_id'] = pd.to_numeric(df['prospect_id'], errors='coerce')

        # Log rows with invalid prospect_id
        invalid_ids = df[df['prospect_id'].isna()]
        if not invalid_ids.empty:
            print(f"Found {len(invalid_ids)} rows with invalid prospect_id:")
            for idx, row in invalid_ids.iterrows():
                print(f"Row {idx}: {row.to_dict()}")
            # Remove invalid rows
            df = df.dropna(subset=['prospect_id'])

        print(f"Cleaned DataFrame contains {len(df)} data lines")
        if len(df) < 2987:
            print(f"Warning: Got {len(df)} lines, fewer than expected (~3000). Check CSV for issues.")

        # Log malformed lines to file
        with open('generate_datasets/malformed_lines.log', 'w', encoding='utf-8') as f:
            if not invalid_ids.empty:
                f.write(f"Found {len(invalid_ids)} rows with invalid prospect_id:\n")
                for idx, row in invalid_ids.iterrows():
                    f.write(f"Row {idx}: {row.to_dict()}\n")

        return df

    except Exception as e:
        print(f"Error cleaning CSV {input_file}: {e}")
        # Debug: Read first few lines manually
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:5]
            print("First 5 lines of CSV:")
            for i, line in enumerate(lines, 1):
                print(f"Line {i}: {line.strip()}")
        raise

def update_freelance_mission_statements():
    def generate_mission_statement(row):
        sector = row['main_sector']
        skills = row['top3_skills'].split('|')[:2]
        name = row['name']
        tone = row['preferred_tone']

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

        mission = random.choice(templates.get(sector, templates['Marketing']))
        words = mission.split()
        if len(words) > 40:
            mission = ' '.join(words[:40]) + '.'
        elif len(words) < 30:
            mission = mission.rstrip('.') + ', with tailored, impactful strategies.'
        return mission.replace('\n', ' ')

    input_file = 'generate_datasets/freelances_dataset.csv'
    output_json = 'generate_datasets/freelances_missions_statements.json'
    output_csv = input_file

    try:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file {input_file} not found")

        freelancers = []
        with open(input_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
            essential_columns = {'name', 'main_sector', 'top3_skills', 'preferred_tone'}
            if not essential_columns.issubset(reader.fieldnames):
                missing = essential_columns - set(reader.fieldnames)
                raise ValueError(f"Missing essential columns: {missing}")

            all_fieldnames = list(reader.fieldnames)
            if 'email' not in all_fieldnames:
                all_fieldnames.append('email')

            for row in reader:
                new_mission = generate_mission_statement(row)
                email = generate_email(row['name'], row['main_sector'], is_freelancer=True)
                freelancer_data = {field: row[field] for field in reader.fieldnames}
                freelancer_data['mission_statement'] = new_mission
                freelancer_data['email'] = email
                freelancers.append(freelancer_data)

        with open(output_json, 'w', encoding='utf-8') as jsonfile:
            json.dump(freelancers, jsonfile, ensure_ascii=False, indent=4)

        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=all_fieldnames, quoting=csv.QUOTE_NONNUMERIC, quotechar='"', doublequote=True)
            writer.writeheader()
            writer.writerows(freelancers)

        print("✅ Freelancer mission statements and emails updated successfully.")
    except Exception as e:
        print(f"Error updating freelancers: {e}")
        raise

def update_prospect_mission_statements():
    try:
        input_csv = "generate_datasets/prospects_dataset.csv"

        with open(input_csv, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"Initial CSV contains {len(lines)-1} data lines")

        df = clean_csv_in_memory(input_csv)

        if 'prospect_id' not in df.columns:
            raise KeyError(f"'prospect_id' column missing after cleaning. Columns: {list(df.columns)}")

        df['prospect_id'] = pd.to_numeric(df['prospect_id'], errors='coerce')
        if df['prospect_id'].isna().any():
            raise ValueError("Invalid prospect_id values found")
        if not df['prospect_id'].is_unique:
            raise ValueError("Duplicate prospect_id found in CSV")
        if not df['prospect_id'].equals(pd.Series(range(df['prospect_id'].min(), df['prospect_id'].max() + 1))):
            print("Warning: prospect_id is not continuous")

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
            "Wellness": [
                "Helping {company_size} {action} wellness outcomes through {adjective} solutions built around {focus}.",
                "We design {adjective} health solutions to help {company_size} {action} mental and physical balance using {focus}.",
                "{company_size} trust our {adjective} platforms to {action} holistic wellness through {focus}.",
                "Supporting better living for {company_size} by {action} self-care habits with {adjective} digital tools based on {focus}.",
                "Empowering health journeys: we help {company_size} {action} well-being with {adjective} methods powered by {focus}.",
                "Wellness made smarter for {company_size}: we {action} care strategies through {focus} and {adjective} innovations."
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
            "Education/Ed-Tech": [
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
            "Wellness": {
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
            "Education/Ed-Tech": {
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

            template = random.choice(templates.get(sector, templates["FinTech"]))
            elements = dynamic_elements.get(sector, dynamic_elements["FinTech"])

            adjective = random.choice(elements["adjectives"])
            action = random.choice(elements["actions"])
            focus = random.choice(elements["focuses"])

            if role == "Head of Data":
                focus = "data analytics"
            elif role == "CTO":
                focus = "cutting-edge technology"
            elif role == "Head of Marketing":
                focus = "customer engagement"
            elif role == "CEO":
                action = random.choice(["drive", "pioneer", "transform"])

            mission = template.format(adjective=adjective, action=action, focus=focus, company_size=company_size)

            words = mission.split()
            expected_length = len(template.split())
            if len(words) > expected_length + 4:
                mission = " ".join(words[:expected_length + 4]) + "."
            elif len(words) < expected_length - 3:
                mission += " Our approach ensures measurable results aligned with your goals."

            return mission.replace('\n', ' ')

        mission_dict = {}
        email_dict = {}
        for _, row in df.iterrows():
            prospect_id = str(row["prospect_id"])
            mission_dict[prospect_id] = generate_mission(row)
            try:
                email_dict[prospect_id] = generate_email(
                    row["main_contact"],
                    row["company"],
                    is_freelancer=False
                )
            except Exception as e:
                print(f"Error generating email for prospect_id={prospect_id}: {e}")
                email_dict[prospect_id] = "error@invalid.com"

        with open("generate_datasets/prospects_mission_statements.json", "w", encoding="utf-8") as f:
            json.dump(mission_dict, f, ensure_ascii=False, indent=2)

        with open("generate_datasets/prospects_mission_statements.json", "r", encoding="utf-8") as f:
            mission_data = json.load(f)

        df["mission_statement"] = df["prospect_id"].astype(str).map(mission_data)
        if "email" not in df.columns:
            df["email"] = df["prospect_id"].astype(str).map(email_dict)
        else:
            df["email"] = df["prospect_id"].astype(str).map(email_dict)

        if df["mission_statement"].isna().any() or df["email"].isna().any():
            raise ValueError("Missing mission statements or emails for some prospect_id")

        with open(input_csv, 'w', encoding='utf-8') as f:
            f.write('')
        df.to_csv(
            input_csv,
            index=False,
            encoding='utf-8',
            quoting=csv.QUOTE_NONNUMERIC,
            quotechar='"',
            doublequote=True
        )

        print(f"✅ Prospects mission statements and emails updated successfully. Output contains {len(df)} lines.")
    except Exception as e:
        print(f"Error updating prospects: {e}")
        raise

def main():
    fake = Faker("en_US")
    Faker.seed(0)
    random.seed(0)

    Path("generate_datasets").mkdir(exist_ok=True)

    # Freelance dataset
    with open("generate_datasets/freelances_dataset.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, quotechar='"', doublequote=True)
        writer.writerow([
            "freelance_id", "name", "title", "main_sector",
            "top3_skills", "city", "daily_rate", "mission_statement",
            "preferred_tone", "preferred_style", "remote"
        ])
        for fid in range(1, N_FREELANCES + 1):
            sec = random.choice(SECTORS)
            writer.writerow([
                fid,
                fake.name().replace('\n', ' ').replace(',', ' '),
                random.choice(TITLE_POOL[sec]),
                sec,
                "|".join(random.sample(SKILLS[sec], 3)),
                random.choice(list(cities_england.values())),
                round(random.uniform(300, 1000), 2),
                fake.catch_phrase().replace('\n', ' '),
                random.choice(TONE_OPTIONS),
                random.choice(STYLE_OPTIONS),
                random.choice(["Yes", "No"])
            ])

    # Prospect dataset
    with open("generate_datasets/prospects_dataset.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, quotechar='"', doublequote=True)
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
                str(pid),
                fake.company().replace('\n', ' '),
                sec,
                fake.name().replace('\n', ' ').replace(',', ' '),
                random.choice(["CEO", "CTO", "Head of Marketing", "Head of Data"]),
                random.choice(list(cities_england.values())),
                fake.bs().capitalize().replace('\n', ' '),
                size,
                stage,
                ticket_size_class(size, stage),
                random.choice(TONE_OPTIONS),
                random.choice(["Yes", "No"])
            ])

    print("✅ CSVs generated in /generate_datasets")
    update_freelance_mission_statements()
    update_prospect_mission_statements()

if __name__ == "__main__":
    main()
