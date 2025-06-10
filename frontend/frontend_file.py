import streamlit as st
import requests

st.title("Iris Predictor")

sepal_length = st.slider('Sepal length', 0.0, 10.0, 5.0)
sepal_width = st.slider('Sepal width', 0.0, 10.0, 3.0)
petal_length = st.slider('Petal length', 0.0, 10.0, 1.5)
petal_width = st.slider('Petal width', 0.0, 10.0, 0.2)

if st.button("Predict"):
    url = "https://<TON_URL_CLOUD_RUN>/predict"  # Remplace par ton vrai URL Cloud Run
    params = {
        "sepal_length": sepal_length,
        "sepal_width": sepal_width,
        "petal_length": petal_length,
        "petal_width": petal_width
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        st.success(f"Prediction: {response.json()['prediction']}")
    else:
        st.error("Failed to get prediction.")
