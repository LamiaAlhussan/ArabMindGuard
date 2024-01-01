# tool.py
import streamlit as st
import joblib
import LR_model as model
import gather_user_tweets 
import numpy as np
from PIL import Image


# import main


# Load the logistic regression model
model_filename = 'logistic_regression_model.pkl'
logistic_regression_model = joblib.load(model_filename)
best_model= joblib.load('LR_Model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

def app():
    # show_pages([Page("tool.py","Tool"),
    #             Page("home.py","Home")
    # ])
    # hide_pages(['Tool','Home'])
    
    st.title("اداة تحديد الاكتئاب")

    # Get user input
    twitter_account = st.text_input(":ادخل حسابك")

    
    # Display entered Twitter account
    if st.button("جرب"):
        if twitter_account:
            st.write(f"@{twitter_account} :حسابك هو ")
            user_file = twitter_account+'.csv'
            # gather_user_tweets.fetch_and_save_tweets(twitter_account,user_file)
            Percentage = model.analyze_user_tweets("sah_khail.csv",vectorizer,best_model)
            # Predict depression probability
                # Predict depression probability
            st.write(f"{Percentage:.2f}% : احتمالية الاكتئاب ")

            image = Image.open('depression_wordcloud.png')
            st.image(image, caption='3 marla plot',use_column_width=True)

                    # Check if the probability is higher than 60%
            if Percentage >= 70:
                st.warning("تحذير : احتمالية اكتئاب عالية.")
                st.write("هنا بعض العيادات الي ممكن تساعدك:")
                st.markdown("[1-لبيه](https://labayh.net/ar/)")
                st.markdown("[2-عناية](https://academicadvising.imamu.edu.sa/Enaya)")

