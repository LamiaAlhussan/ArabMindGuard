import streamlit as st
import joblib
from PIL import Image



def app():
    # Load your model and vectorizer
    model_filename = 'Saudi_percentage.pkl'
    logistic_regression_model = joblib.load(model_filename)
        


    # Streamlit UI
    st.title("Depression Detection Statistics")

    # Display accuracy
    st.write(f"Model Accuracy: {logistic_regression_model:.2f}%")
    image = Image.open('dataset_wordcloud.png')
    st.image(image, caption='',use_column_width=True)

    # "Try Our Tool" button
#     if st.button("Try Our Tool"):
#         switch_page("Tool")

# # Register this page with the st_pages extension
# show_pages([Page("home.py", "App")])
