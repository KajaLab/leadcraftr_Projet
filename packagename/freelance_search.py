import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import string
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from math import radians, sin, cos, sqrt, atan2

# Ensure necessary NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')

city_coord = {
  "london": {"lat": 51.5072, "lon": -0.1275},
  "birmingham": {"lat": 52.48, "lon": -1.9025},
  "manchester": {"lat": 53.479, "lon": -2.2452},
  "liverpool": {"lat": 53.4094, "lon": -2.9785},
  "bristol": {"lat": 51.4536, "lon": -2.5975},
  "leeds": {"lat": 53.8, "lon": -1.75},
  "glasgow": {"lat": 55.86, "lon": -4.25},
  "edinburgh": {"lat": 55.9533, "lon": -3.1883},
  "cardiff": {"lat": 51.4816, "lon": -3.1791},
  "newcastle upon tyne": {"lat": 54.978, "lon": -1.6178},
  "sheffield": {"lat": 53.3811, "lon": -1.4701},
  "nottingham": {"lat": 52.9561, "lon": -1.1512},
  "portsmouth": {"lat": 50.8058, "lon": -1.0872},
  "southampton": {"lat": 50.9025, "lon": -1.4042},
  "leicester": {"lat": 52.6344, "lon": -1.1319},
  "worcester": {"lat": 52.1911, "lon": -2.2206},
  "altrincham": {"lat": 53.3879, "lon": -2.3475},
  "lewes": {"lat": 50.8736, "lon": 0.0076},
  "carlton": {"lat": 52.965, "lon": -1.056},
  "scunthorpe": {"lat": 53.585, "lon": -0.65},
  "christchurch": {"lat": 50.73, "lon": -1.777},
  "lancaster": {"lat": 54.048, "lon": -2.793},
  "whitstable": {"lat": 51.359, "lon": 1.026},
  "hinckley": {"lat": 52.539, "lon": -1.371},
  "carlisle": {"lat": 54.89, "lon": -2.93},
  "rickmansworth": {"lat": 51.64, "lon": -0.47},
  "chesterfield": {"lat": 53.236, "lon": -1.433},
  "sutton coldfield": {"lat": 52.569, "lon": -1.825},
  "dorking": {"lat": 51.23, "lon": -0.33},
  "smethwick": {"lat": 52.502, "lon": -1.978},
  "coalville": {"lat": 52.715, "lon": -1.373},
  "burgess hill": {"lat": 50.957, "lon": -0.133},
  "luton": {"lat": 51.8783, "lon": -0.4147},
  "canvey island": {"lat": 51.536, "lon": 0.589},
  "loughborough": {"lat": 52.766, "lon": -1.206},
  "hemel hempstead": {"lat": 51.7526, "lon": -0.4692},
  "boston": {"lat": 52.978, "lon": -0.026},
  "sunderland": {"lat": 54.906, "lon": -1.383},
  "basingstoke": {"lat": 51.2667, "lon": -1.0876},
  "grimsby": {"lat": 53.568, "lon": -0.089},
  "bognor regis": {"lat": 50.787, "lon": -0.675},
  "royston": {"lat": 52.072, "lon": -0.024},
  "shrewsbury": {"lat": 52.711, "lon": -2.756},
  "reigate": {"lat": 51.237, "lon": -0.207},
  "accrington": {"lat": 53.753, "lon": -2.364},
  "wisbech": {"lat": 52.664, "lon": 0.163},
  "didcot": {"lat": 51.605, "lon": -1.242},
  "royal tunbridge wells": {"lat": 51.132, "lon": 0.264},
  "halifax": {"lat": 53.722, "lon": -1.86},
  "keighley": {"lat": 53.867, "lon": -1.905},
  "epsom": {"lat": 51.332, "lon": -0.269},
  "nuneaton": {"lat": 52.525, "lon": -1.464},
  "oldbury": {"lat": 52.492, "lon": -2.012},
  "stratford-upon-avon": {"lat": 52.191, "lon": -1.706},
  "warwick": {"lat": 52.284, "lon": -1.583},
  "stockport": {"lat": 53.4083, "lon": -2.1494},
  "walton-on-thames": {"lat": 51.396, "lon": -0.412},
  "witney": {"lat": 51.785, "lon": -1.486},
  "huddersfield": {"lat": 53.645, "lon": -1.782},
  "wigan": {"lat": 53.545, "lon": -2.636},
  "stourbridge": {"lat": 52.457, "lon": -2.14},
  "chatham": {"lat": 51.378, "lon": 0.528},
  "lakenheath": {"lat": 52.404, "lon": 0.54},
  "huntingdon": {"lat": 52.327, "lon": -0.198},
  "waterlooville": {"lat": 50.898, "lon": -1.031},
  "solihull": {"lat": 52.413, "lon": -1.778},
  "farnborough": {"lat": 51.288, "lon": -0.75},
  "godalming": {"lat": 51.189, "lon": -0.606},
  "stafford": {"lat": 52.809, "lon": -2.116},
  "redditch": {"lat": 52.308, "lon": -1.942},
  "dewsbury": {"lat": 53.687, "lon": -1.631},
  "esher": {"lat": 51.378, "lon": -0.374},
  "milton keynes": {"lat": 52.04, "lon": -0.759},
  "stevenage": {"lat": 51.905, "lon": -0.203},
  "kingston upon hull": {"lat": 53.746, "lon": -0.336},
  "tamworth": {"lat": 52.637, "lon": -1.688},
  "northampton": {"lat": 52.2304, "lon": -0.8938},
  "west bromwich": {"lat": 52.519, "lon": -1.995},
  "kidderminster": {"lat": 52.388, "lon": -2.24},
  "rugby": {"lat": 52.37, "lon": -1.26},
  "lowestoft": {"lat": 52.478, "lon": 1.748},
  "blackburn": {"lat": 53.748, "lon": -2.482},
  "bicester": {"lat": 51.902, "lon": -1.14},
  "northwich": {"lat": 53.257, "lon": -2.518},
  "brentwood": {"lat": 51.623, "lon": 0.304},
  "hereford": {"lat": 52.057, "lon": -2.716},
  "gloucester": {"lat": 51.8667, "lon": -2.25},
  "littlehampton": {"lat": 50.803, "lon": -0.543},
  "bridgwater": {"lat": 51.127, "lon": -2.994},
  "ipswich": {"lat": 52.059, "lon": 1.155},
  "hastings": {"lat": 50.852, "lon": 0.573},
  "worthing": {"lat": 50.8147, "lon": -0.3714},
  "bracknell": {"lat": 51.411, "lon": -0.752},
  "colchester": {"lat": 51.8917, "lon": 0.903},
  "dudley": {"lat": 52.508, "lon": -2.088},
  "st helens": {"lat": 53.454, "lon": -2.748},
  "crewe": {"lat": 53.096, "lon": -2.441},
  "halesowen": {"lat": 52.455, "lon": -2.073},
  "spalding": {"lat": 52.787, "lon": -0.154},
  "st albans": {"lat": 51.755, "lon": -0.339},
  "poole": {"lat": 50.718, "lon": -1.989},
  "slough": {"lat": 51.5084, "lon": -0.5881},
  "cheshire west and chester": {"lat": 53.208, "lon": -2.704},
  "ashton-under-lyne": {"lat": 53.488, "lon": -2.096},
  "burnley": {"lat": 53.789, "lon": -2.235},
  "hartlepool": {"lat": 54.678, "lon": -1.21},
  "leamington spa": {"lat": 52.287, "lon": -1.533},
  "runcorn": {"lat": 53.342, "lon": -2.729},
  "harrogate": {"lat": 54.004, "lon": -1.54},
  "corby": {"lat": 52.484, "lon": -0.686},
  "torquay": {"lat": 50.46, "lon": -3.525},
  "warrington": {"lat": 53.39, "lon": -2.59},
  "cannock": {"lat": 52.684, "lon": -2.028},
  "norwich": {"lat": 52.6286, "lon": 1.2928},
  "york": {"lat": 53.96, "lon": -1.08},
  "oldham": {"lat": 53.541, "lon": -2.115},
  "mansfield": {"lat": 53.144, "lon": -1.201},
  "ashford": {"lat": 51.146, "lon": 0.869},
  "stamford": {"lat": 52.653, "lon": -0.478},
  "lincoln": {"lat": 53.23, "lon": -0.536},
  "watford": {"lat": 51.656, "lon": -0.395},
  "gravesend": {"lat": 51.442, "lon": 0.368},
  "frome": {"lat": 51.229, "lon": -2.321},
  "kendal": {"lat": 54.329, "lon": -2.746},
  "aylesbury": {"lat": 51.815, "lon": -0.81},
  "cheltenham": {"lat": 51.9, "lon": -2.07},
  "ely": {"lat": 52.399, "lon": 0.258},
  "salisbury": {"lat": 51.071, "lon": -1.795},
  "stockton-on-tees": {"lat": 54.567, "lon": -1.321},
  "taunton": {"lat": 51.018, "lon": -3.102},
  "bolton": {"lat": 53.579, "lon": -2.433},
  "malvern": {"lat": 52.109, "lon": -2.322},
  "trowbridge": {"lat": 51.324, "lon": -2.213},
  "maidenhead": {"lat": 51.522, "lon": -0.718},
  "chippenham": {"lat": 51.46, "lon": -2.115},
  "eastbourne": {"lat": 50.771, "lon": 0.279},
  "paignton": {"lat": 50.435, "lon": -3.565},
  "ellesmere port": {"lat": 53.284, "lon": -2.898},
  "yeovil": {"lat": 50.941, "lon": -2.632},
  "peterborough": {"lat": 52.576, "lon": -0.245},
  "dagenham": {"lat": 51.545, "lon": 0.165},
  "bournemouth": {"lat": 50.72, "lon": -1.88},
  "crawley": {"lat": 51.109, "lon": -0.187},
  "doncaster": {"lat": 53.523, "lon": -1.135},
  "brighton and hove": {"lat": 50.822, "lon": -0.137},
  "southend-on-sea": {"lat": 51.536, "lon": 0.711},
  "weston-super-mare": {"lat": 51.353, "lon": -2.981},
  "bedford": {"lat": 52.137, "lon": -0.468},
  "birkenhead": {"lat": 53.393, "lon": -3.018},
  "fareham": {"lat": 50.852, "lon": -1.176},
  "reading": {"lat": 51.455, "lon": -0.97},
  "middlesbrough": {"lat": 54.58, "lon": -1.235},
  "rochdale": {"lat": 53.61, "lon": -2.16},
  "gateshead": {"lat": 54.9556, "lon": -1.6},
  "marlow": {"lat": 51.572, "lon": -0.775},
  "wolverhampton": {"lat": 52.5833, "lon": -2.1333},
  "wellingborough": {"lat": 52.316, "lon": -0.697},
  "cambridge": {"lat": 52.2053, "lon": 0.1192},
  "bury": {"lat": 53.593, "lon": -2.302},
  "blackpool": {"lat": 53.8142, "lon": -3.0503},
  "chelmsford": {"lat": 51.73, "lon": 0.48},
  "newbury": {"lat": 51.404, "lon": -1.32},
  "margate": {"lat": 51.387, "lon": 1.385},
  "chesham": {"lat": 51.706, "lon": -0.612},
  "exeter": {"lat": 50.718, "lon": -3.532},
  "swindon": {"lat": 51.558, "lon": -1.782},
  "washington": {"lat": 54.893, "lon": -1.506},
  "telford": {"lat": 52.678, "lon": -2.449},
  "horsham": {"lat": 51.063, "lon": -0.329},
  "burton upon trent": {"lat": 52.801, "lon": -1.637},
  "folkestone": {"lat": 51.082, "lon": 1.176},
  "walsall": {"lat": 52.585, "lon": -1.977},
  "weymouth": {"lat": 50.617, "lon": -2.457},
  "fleet": {"lat": 51.278, "lon": -0.835},
  "coventry": {"lat": 52.4081, "lon": -1.5106},
  "high wycombe": {"lat": 51.6287, "lon": -0.7482},
  "barnsley": {"lat": 53.553, "lon": -1.488},
  "gillingham": {"lat": 51.388, "lon": 0.551},
  "derby": {"lat": 52.9247, "lon": -1.478},
  "preston": {"lat": 53.759, "lon": -2.703},
  "ramsgate": {"lat": 51.338, "lon": 1.418},
  "chester": {"lat": 53.197, "lon": -2.89},
  "crowborough": {"lat": 51.056, "lon": 0.163},
  "kettering": {"lat": 52.395, "lon": -0.72},
  "maidstone": {"lat": 51.272, "lon": 0.529},
  "sale": {"lat": 53.424, "lon": -2.322},
  "worksop": {"lat": 53.303, "lon": -1.124},
  "banbury": {"lat": 52.062, "lon": -1.341},
  "hertford": {"lat": 51.802, "lon": -0.081},
  "redcar": {"lat": 54.619, "lon": -1.066},
  "st neots": {"lat": 52.222, "lon": -0.27},
  "plymouth": {"lat": 50.3714, "lon": -4.1422},
  "oxford": {"lat": 51.75, "lon": -1.25},
  "great yarmouth": {"lat": 52.607, "lon": 1.73},
  "stoke-on-trent": {"lat": 53.003, "lon": -2.181},
  "woking": {"lat": 51.319, "lon": -0.556},
  "dunstable": {"lat": 51.876, "lon": -0.524},
  "wokingham": {"lat": 51.411, "lon": -0.835}
}

#df_coords = pd.read_csv('../generate_datasets/city_coordinates.csv',sep=",")
city_coordinates_df = pd.DataFrame.from_dict(city_coord, orient='index').reset_index()
city_coordinates_df = city_coordinates_df.rename(columns={'index': 'city'})

def get_wordnet_pos(word):
    """Map POS tag to first character for WordNetLemmatizer"""
    tag = pos_tag([word])[0][1][0].lower()  # Get first letter of POS tag
    return{'n': 'n', 'v': 'v', 'a': 'a', 'r': 'r'}.get(tag, 'n')

def cleaning(sentence):
    # Basic cleaning
    sentence = sentence.strip().lower()
    sentence = ''.join(char for char in sentence if not char.isdigit())
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))

    # Tokenization
    tokenized_sentence = word_tokenize(sentence)

    # Stopwords removal
    stop_words = set(stopwords.words('english'))
    tokenized_sentence_cleaned = [w for w in tokenized_sentence if w not in stop_words]

    # Lemmatization with correct POS tagging
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in tokenized_sentence_cleaned]

    return ' '.join(lemmatized)

def prepare_data(freelance_df, prospect_df):
    """Prepares combined text and skills list for freelancers and prospects."""
    freelance_df['combined_text'] = freelance_df.apply(
        lambda row: cleaning(row['mission_statement'] + " " +
                             row['title'] + " " +
                             row['main_sector']), axis=1
    )

    prospect_df['combined_text'] = prospect_df.apply(
        lambda row: cleaning(row['mission_statement'] + " " +
                             row['contact_role'] + " " +
                             row['sector']), axis=1
    )
    return freelance_df, prospect_df

def prepare_categorical_features(freelance_df, prospect_df):
    """Prepares categorical features for matching, specifically 'remote'."""
    freelance_df['remote_flag'] = freelance_df['remote'].apply(lambda x: 1 if x == 'Yes' else 0)
    prospect_df['remote_flag'] = prospect_df['remote'].apply(lambda x: 1 if x == 'Yes' else 0)
    return freelance_df, prospect_df

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on Earth using the Haversine formula.
    Returns distance in kilometers.
    """
    R = 6371  # Radius of Earth in kilometers

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def calculate_holistic_similarity(freelancer_row, prospect_df, vectorizer=None):
    """
    Calculates a holistic similarity score between a freelancer and all prospects,
    combining text, tone, remote preference, sector, and geographical proximity.
    """

    # load the dictionnary of citiy's coordinates
    city_coordinates_df = pd.DataFrame.from_dict(city_coord, orient='index').reset_index()
    city_coordinates_df = city_coordinates_df.rename(columns={'index': 'city'})

    # Initialize a mask for prospects that meet the distance criteria
    distance_mask = np.ones(len(prospect_df), dtype=bool)

    # Calculate geographical similarity and apply distance filter
    geo_similarities = []
    freelancer_city = cleaning(freelancer_row['city']).lower()
    freelancer_coord_row = city_coordinates_df[city_coordinates_df["city"].str.lower() == freelancer_city]

    freelancer_lat, freelancer_lon = None, None
    if not freelancer_coord_row.empty:
        freelancer_lat = freelancer_coord_row["lat"].values[0]
        freelancer_lon = freelancer_coord_row["lon"].values[0]

    for i, prospect_row in prospect_df.iterrows():
        # If either freelancer or prospect is remote, geographical proximity is not a constraint (distance 1.0)
        if freelancer_row['remote_flag'] == 1 or prospect_row['remote_flag'] == 1:
            geo_similarities.append(1.0)
        else:
            # Both are not remote, so geographical proximity matters
            prospect_city = cleaning(prospect_row['city']).lower()
            prospect_coord_row = city_coordinates_df[city_coordinates_df["city"].str.lower() == prospect_city]

            if not prospect_coord_row.empty and freelancer_lat is not None:
                prospect_lat = prospect_coord_row["lat"].values[0]
                prospect_lon = prospect_coord_row["lon"].values[0]

                dist = haversine_distance(freelancer_lat, freelancer_lon, prospect_lat, prospect_lon)
                if dist <= 40:
                    geo_similarities.append(1.0)
                else:
                    geo_similarities.append(0.0)
                    distance_mask[i] = False  # Mark this prospect for exclusion
            else:
                geo_similarities.append(0.0)
                distance_mask[i] = False # Mark for exclusion if coordinates are missing

    geo_similarities = np.array(geo_similarities)

    # Filter prospect_df based on distance_mask BEFORE other calculations
    filtered_prospect_df = prospect_df[distance_mask].copy()

    if filtered_prospect_df.empty:
        return np.array([]) # No prospects left after distance filtering

    # Recalculate other similarities for the filtered prospects
    # 1. Text Similarity
    if vectorizer:
        freelancer_text_vec = vectorizer.transform([freelancer_row['combined_text']])
        prospect_text_vectors = vectorizer.transform(filtered_prospect_df['combined_text'])
        text_similarities = cosine_similarity(freelancer_text_vec, prospect_text_vectors).flatten()
    else:
        text_similarities = np.zeros(len(filtered_prospect_df)) # Placeholder

    # 2. Tone Similarity
    tone_similarities = np.array([
        1 if freelancer_row['preferred_tone'].lower() == prospect_tone.lower() else 0
        for prospect_tone in filtered_prospect_df['target_tone']
    ])

    # 3. Remote Preference Similarity
    remote_similarities = np.array([
        1 if freelancer_row['remote_flag'] == prospect_remote_flag else 0
        for prospect_remote_flag in filtered_prospect_df['remote_flag']
    ])

    # # 4. Sector Similarity
    sector_similarities = np.array([
        1 if cleaning(freelancer_row['main_sector']) == cleaning(prospect_sector) else 0
        for prospect_sector in filtered_prospect_df['sector']
    ])

    # Apply the geo_similarities calculated *before* filtering to the filtered_prospect_df
    # We need to ensure that geo_similarities aligns with filtered_prospect_df.
    # The simplest way is to re-extract the relevant geo_similarities for the filtered rows.
    # Since `distance_mask` was used to filter `prospect_df`, the `geo_similarities` array
    # already has zeros for the excluded rows. We just need to take the elements corresponding
    # to the `True` values in `distance_mask`.
    filtered_geo_similarities = geo_similarities[distance_mask]

    # Combine all similarities with weights
    weights = {
        'text': 0.3,
        'tone': 0.1,
        'remote': 0.4,
        'sector': 0.4,
        'geo': 0.4
    }

    final_similarities = (
        weights['text'] * text_similarities +
        weights['tone'] * tone_similarities +
        weights['remote'] * remote_similarities +
        weights['sector'] * sector_similarities +
        weights['geo'] * filtered_geo_similarities
    )

    return final_similarities, filtered_prospect_df


def get_top_20_leads_prospect(freelancer_row, prospect_df, vectorizer=None):

    city_coordinates_df = pd.DataFrame.from_dict(city_coord, orient='index').reset_index()
    city_coordinates_df = city_coordinates_df.rename(columns={'index': 'city'})

    final_similarities, filtered_prospect_df = calculate_holistic_similarity(freelancer_row, prospect_df, vectorizer)

    if filtered_prospect_df.empty:
        print("No prospects found within the 40km radius or fulfilling remote criteria.")
        return pd.DataFrame() # Return an empty DataFrame if no prospects meet the criteria

    # Ensure we don't try to get more leads than available after filtering
    num_leads = min(20, len(filtered_prospect_df))
    top_leads_idx = final_similarities.argsort()[-num_leads:][::-1]
    return filtered_prospect_df.iloc[top_leads_idx].assign(similarity=final_similarities[top_leads_idx])
