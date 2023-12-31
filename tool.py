# tool.py
import streamlit as st
import joblib
import subprocess
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages
# import main


# Load the logistic regression model
model_filename = 'logistic_regression_model.pkl'
logistic_regression_model = joblib.load(model_filename)

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

            # Predict depression probability
                # Predict depression probability
            probability=logistic_regression_model
            st.write(f"{probability*100:.2f}% : احتمالية الاكتئاب ")

                    # Check if the probability is higher than 60%
            if probability >= 0.6:
                st.warning("تحذير : احتمالية اكتئاب عالية.")
                st.write("هنا بعض العيادات الي ممكن تساعدك:")
                st.markdown("[1-لبيه](https://labayh.net/ar/)")
                st.markdown("[2-عناية](https://academicadvising.imamu.edu.sa/Enaya)")

