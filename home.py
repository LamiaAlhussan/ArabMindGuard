# # streamlit_app.py
# import streamlit as st
# import joblib
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# from streamlit_extras.switch_page_button import switch_page
# from st_pages import Page, show_pages, hide_pages
# import tool


# def app():

#     hide_pages([
#         Page('tool.py','Tool')
#     ])

# # Load your model and vectorizer
#     model_filename = 'logistic_regression_model.pkl'
#     logistic_regression_model = joblib.load(model_filename)

#     # Streamlit UI
#     st.title("Depression Detection Statistics")

#     # Display accuracy
#     st.write(f"Model Accuracy: {logistic_regression_model*100:.2f}%")

#     # "Try Our Tool" button
#     if st.button("Try Our Tool"):
#         switch_page("Tool")
        



import streamlit as st
import joblib
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages
import tool

def app():
    # Load your model and vectorizer
    model_filename = 'logistic_regression_model.pkl'
    logistic_regression_model = joblib.load(model_filename)

    # Streamlit UI
    st.title("Depression Detection Statistics")

    # Display accuracy
    st.write(f"Model Accuracy: {logistic_regression_model*100:.2f}%")

    # "Try Our Tool" button
#     if st.button("Try Our Tool"):
#         switch_page("Tool")

# # Register this page with the st_pages extension
# show_pages([Page("home.py", "App")])
