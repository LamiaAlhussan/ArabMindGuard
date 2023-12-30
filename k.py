# streamlit_app.py
import streamlit as st
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import subprocess

# Load your model and vectorizer
model_filename = 'logistic_regression_model.pkl'
logistic_regression_model = joblib.load(model_filename)

# Streamlit UI
st.title("Depression Detection Statistics")

# Display accuracy
st.write(f"Model Accuracy: {logistic_regression_model*100:.2f}%")

# "Try Our Tool" button
if st.button("Try Our Tool"):
    subprocess.run(["streamlit", "run", "tool.py"])



