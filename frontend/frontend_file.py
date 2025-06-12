import streamlit as st
import requests

# UI setup
st.set_page_config(page_title="LEADCRAFT® | Freelance Matching", layout="centered")

# Theme and Header
st.markdown("""
    <style>
        .main { background-color: #ffffff; }
        .css-1d391kg, .css-1cpxqw2 { background: #f5f7fa !important; }
        div[role="listitem"] div {
            background: #f9fbfc;
            border-radius: 12px;
            padding: 16px 20px;
            margin: 10px 0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
            font-size: 15px;
            color: #1c1c1c;
        }
        b {
            font-size: 16px;
            color: #0d47a1;
        }
        a.email-link {
            display: inline-block;
            margin-top: 8px;
            padding: 6px 12px;
            background-color: #0d47a1;
            color: white;
            border-radius: 6px;
            text-decoration: none;
        }
        a.email-link:hover {
            background-color: #093170;
        }
    </style>
""", unsafe_allow_html=True)

st.title("LEADCRAFT®")
st.markdown("### 🤝 Match Freelancers & Companies")
st.write("Connect top freelancers with companies. Start by selecting your profile:")

# Profile selection (default to Freelancer)
user_type = st.radio("You are:", ("A Freelancer looking for a Company", "A Company looking for a Freelancer"))

st.markdown("---")

skills_options = [
    "Python", "Data Analysis", "Data Engineering", "Machine Learning", "Deep Learning", "Web Development",
    "Mobile App", "UI/UX", "DevOps", "Cybersecurity", "Product Management", "Project Management",
    "Digital Marketing", "Content Writing", "AI Engineering", "Data Visualization", "Cloud Architecture"
]

locations = ["Europe", "North America", "South America", "Asia", "Africa", "Oceania", "Remote"]
company_sizes = ["Startup", "SME", "Large Enterprise"]

if user_type == "A Company looking for a Freelancer":
    st.subheader("🔍 Company Search Form")
    company_name = st.text_input("Company Name", max_chars=40)
    company_size = st.selectbox('Company Size', company_sizes)
    location = st.selectbox('Preferred Location', locations)
    work_mode = st.selectbox('Work Mode', ['Remote', 'On-site', 'Hybrid'])
    budget = st.slider('Budget per day (€)', min_value=100, max_value=2000, value=500, step=50)
    job_title = st.text_input("Job Title", max_chars=60)
    mission_statement = st.text_area("Mission Statement", max_chars=300)
    skills = st.multiselect('Required Skills (max 3)', skills_options, max_selections=3)
    experience = st.slider('Minimum Experience (years)', min_value=0, max_value=20, value=3)

    if st.button('Find Freelancers'):
        params = {
            'company_name': company_name,
            'company_size': company_size,
            'location': location,
            'work_mode': work_mode,
            'budget': budget,
            'job_title': job_title,
            'mission_statement': mission_statement,
            'skills': ",".join(skills),
            'experience': experience,
        }
        response = {
            "matches": [
                {"name": "Alice", "skills": ["Python", "Data Science"], "tjm": 600, "experience": 5, "location": "Europe", "work_mode": "Remote", "email": "alice.freelance@example.com"},
                {"name": "Bob", "skills": ["Web Development"], "tjm": 450, "experience": 7, "location": "Remote", "work_mode": "Hybrid", "email": "bob.dev@example.com"},
            ]
        }
        if response and response["matches"]:
            st.success(f"Found {len(response['matches'])} matching freelancers:")
            for match in response['matches']:
                st.markdown(
                    f"""
                    <div>
                        <b>{match['name']}</b> | {', '.join(match['skills'])}<br>
                        💰 <b>{match['tjm']}€/day</b> | 🏆 {match['experience']}y exp | 📍 {match['location']} | {match['work_mode']}<br>
                        <a class='email-link' href='mailto:{match['email']}?subject=Freelance%20Opportunity&body=Hello%20{match['name']},%20test%20contenu%20du%20mail' target='_blank'>📧 Generate Email</a>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No matching freelancers found.")

elif user_type == "A Freelancer looking for a Company":
    st.subheader("🔍 Freelancer Search Form")
    freelancer_name = st.text_input("Your Name", max_chars=40)
    job_title = st.text_input("Desired Job Title", max_chars=60)
    mission_statement = st.text_area("Personal Statement", max_chars=300)
    experience = st.slider('Your Experience (years)', min_value=0, max_value=20, value=3)
    tjm = st.slider('Your Day Rate (TJM, €)', min_value=100, max_value=2000, value=500, step=50)
    skills = st.multiselect('Your Skills (max 3)', skills_options, max_selections=3)
    preferred_company_size = st.selectbox('Preferred Company Size', company_sizes + ['No preference'])
    location = st.selectbox('Preferred Location', locations)
    work_mode = st.selectbox('Preferred Work Mode', ['Remote', 'On-site', 'Hybrid'])

    if st.button('Find Companies'):
        params = {
            'freelancer_name': freelancer_name,
            'experience': experience,
            'tjm': tjm,
            'job_title': job_title,
            'mission_statement': mission_statement,
            'skills': ",".join(skills),
            'preferred_company_size': preferred_company_size,
            'location': location,
            'work_mode': work_mode,
        }
        response = {
            "matches": [
                {"company": "Acme Corp", "industry": "Tech", "budget": 800, "location": "Europe", "size": "SME", "work_mode": "Remote", "email": "hr@acme.com"},
                {"company": "Beta Startup", "industry": "Marketing", "budget": 500, "location": "Remote", "size": "Startup", "work_mode": "Hybrid", "email": "jobs@betastartup.com"},
            ]
        }
        if response and response["matches"]:
            st.success(f"Found {len(response['matches'])} matching companies:")
            for match in response['matches']:
                st.markdown(
                    f"""
                    <div>
                        <b>{match['company']}</b> | {match['industry']}<br>
                        💰 <b>{match['budget']}€/day</b> | 🏢 {match['size']} | 📍 {match['location']} | {match['work_mode']}<br>
                        <a class='email-link' href='mailto:{match['email']}?subject=Freelance%20Collaboration&body=Hello,%20test%20contenu%20du%20mail' target='_blank'>📧 Generate Email</a>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No matching companies found.")

st.markdown("---")
st.caption("Built with LeadCraftr — Empowering smarter freelance matchmaking 🚀")
