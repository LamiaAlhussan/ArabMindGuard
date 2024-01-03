import streamlit as st
import base64
from pathlib import Path

# Simulated user credentials
def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid' style='width:100%;'>".format(
      img_to_bytes(img_path)
    )
    return img_html
def app():

    logo_image = "logo.jpg"  # Provide the correct path to your logo

    st.markdown(
        f"""
    <div class='logo'>{img_to_html(logo_image)} </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        .st-emotion-cache-1r4qj8v {
        background-color:#fbfbfb;
    }
     @font-face {
      font-family: myFirstFont;
      src: url(NotoNaskhArabic-Medium.ttf);
      font-weight: bold;
    }
    
        .logo{
            width:70%;
            position:relative;
            left:7rem;
            margin-top:10%;
            margin-bottom:5%;
        }
        .stButton > button{
            width:7rem;
            margin:2%;
            margin-top:4%;
            position:relative;
            left:18rem;
            
        }
        .stTextInput{
            width:70%;
            position:relative;
            left:6.5rem;
            margin-bottom:-1.5rem;

            
        }
        .sub-title{
            color:#373d3f;
            font-family: myFirstFont;
            position:relative;
            left:-7rem;
            bottom:-2rem;
            
        }
        .title{
        font-family: myFirstFont;
        color:#373d3f;

        }
        
        </style>
        """,
        unsafe_allow_html=True
    )
    valid_username = "user123"
    valid_password = "pass123"

    # Streamlit app title

    st.markdown(
        f"""
    <div class='title' style="text-align:center;"><h2>تسجيل دخول</h2> </div>
        """,
        unsafe_allow_html=True
    )

    # Login form
    st.markdown(
        f"""
    <div class='sub-title' style="text-align:right;"><h5>إسم المستخدم</h5> </div>
        """,
        unsafe_allow_html=True
    )
    username = st.text_input("")
    st.markdown(
        f"""
    <div class='sub-title' style="text-align:right;"><h5>كلمة السر</h5> </div>
        """,
        unsafe_allow_html=True
    )
    password = st.text_input(" ", type="password")

    # Check credentials on button click
    if st.button("دخول"):
        if username == valid_username and password == valid_password:
            st.success("Login Successful!")
        else:
            st.error("Invalid username or password")
app()