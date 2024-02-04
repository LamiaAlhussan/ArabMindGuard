# tool.py
import streamlit as st
import joblib
import Logistic_regression as model
import gather_user_tweets as gather_user_tweets
import base64
from pathlib import Path


# Load the logistic regression model
best_model = joblib.load("Extras/LR_Model.pkl")
vectorizer = joblib.load("Extras/vectorizer.pkl")


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

    st.markdown(
        """
                            <style>
                                /* Align text input to the right */
                                .stTextInput {
                                    text-align: right;
                                }
                                
                                 .parent {
        padding-bottom: 2rem;
        text-align: center;
        display: flex;
        width:130%;
        height:100%;
        margin-left:-6.5rem;

    }

    /* Style for the container-like effect */
    .container-like {
        background-color:#fbfbfb;
        position: relative;
        float: right;
        padding: 1rem 1rem;
        border-radius:10px;
        box-shadow:2px 2px 2px 2px lightgrey;
        vertical-align: middle;
        display: inline-block; /* Display child div in line */
        width:50%;
        
        
    }
    .stTextInput input {
        background-color:#f2f2f2;
    }
        @font-face {
      font-family: myFirstFont;
      src: url(NotoNaskhArabic-Medium.ttf);
      font-weight: bold;
    }
    .titles{
        font-family: myFirstFont;
        color:#373d3f;
        
        
    }
    .percentage{
        font-family: myFirstFont;
        margin-top:3rem;
        font-size:5rem;
        
    }

    /* Style for the image container */
    .image-container {
        float: left;
        box-shadow:2px 2px 2px 2px lightgrey;
        background-color:#fbfbfb;
        padding: 1rem 1rem;
        border-radius:10px;
        vertical-align: middle;
        display: inline-block; /* Display child div in line */
        width:50%;
        margin-right:2rem;
                                }
                              
                              
        .warning-message {
        background-color: #fbf8e3;
        border: 1px solid #fbf8e3;
        border-radius: 5px;
        padding: 0px;
        margin: 10%;
        margin-left: 6rem;
        text-align: center;
        color: #ad6c05;
        height:10%;
        width:50%;
        display:block;
    }
    .error-message {
        font-family:myFirstFont;
        background-color: #fbe8e8;
        border: 1px solid #fbe8e8;
        border-radius: 5px;
        color:#7d353b;
        height:2rem;
        width:90%;
        text-align: center;
        margin-left:2.5rem;
        padding:0.5%;

    }
    .parent-clinic{
        width:130%;
        border: 0px solid black;
        margin-right:500px;
        
        
    }
    .clinics{
        font-family:myFirstFont;
        color:#373d3f;
        width:100%;
        height:8rem;
        border: 0px solid black;
        background-color:#fbfbfb;
        display:block;
        box-shadow:2px 2px 2px 2px lightgrey;
        margin-bottom:2%;
        margin-left:-11%;
        border-radius: 10px;
        

    }
    .clinics h2{
        position: relative;
        bottom:8.5rem;
        left:-1rem;
        

    }
    .clinics p{
        position: relative;
        bottom:9rem;
        text-align:right;
        left:1rem;
        width:90%;

    }
    .red-box{
        border: 1px solid #ee5b4d;
        background-color:#ee5b4d;
        width:5%;
        border-radius: 0 10px    10px 0;
        position: relative;
        right:-95.5%;
        height:8rem;
        opacity:0.9;

        
    }
   
                            </style>
                            """,
        unsafe_allow_html=True,
    )
    error_message = ""
    twitter_account = ""
    pressed = False

    st.markdown(
        "<h1 align='center' style='font-family:myFirstFont; color:#373d3f;'>اداة تحديد الاكتئاب</h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <style>
            .text-above-input {{
                font-size: 1.5em;  /* Set the font size to h4 equivalent */
                text-align: center; /* Set the alignment to center (you can change it to 'left' or 'right' as needed) */
                margin-bottom:-2%;
                font-family:myFirstFont;
                color:#373d3f;
                
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Display styled text above the input
    st.markdown('<p class="text-above-input"> ادخل حسابك</p>', unsafe_allow_html=True)

    instr = ""

    # Create two columns; adjust the ratio to your liking
    col1, col2, cl = st.columns([5, 13, 2])

    # Use the first column for text input
    with col2:
        twitter_account = st.text_input(
            instr,
            value=instr,
            placeholder=instr,
            label_visibility="collapsed",
        )
    # Use the second column for the submit button
    with col1:
        buff, col, buff2 = st.columns([4, 1, 4])
        button_style = """
                    <style>
                    .stButton > button {
                        width: 120%;
                        height: 50%;
                        background-color:#fbfbfb;
                        font-weight:bold;
                        font-family:myFirstFont; 
                        color:#373d3f;
                    }
                    </style>
                    """
        st.markdown(button_style, unsafe_allow_html=True)
        if buff2.button("جرب"):
            pressed = True

    if pressed:
        if twitter_account:
            col1, col2 = st.columns(2)
            user_file = twitter_account + ".csv"
            user_found, tweets_length = gather_user_tweets.fetch_and_save_tweets(
                twitter_account, user_file
            )
            if not user_found:
                error_message = "الحساب غير صحيح"

            else:
                if not tweets_length:
                    error_message = "عدد التغريدات غير كافي"

            if error_message:
                st.markdown(
                    f"""
                                    <div class="error-message">{error_message}
                                    </div> 
                                   
                                    """,
                    unsafe_allow_html=True,
                )
            else:

                tweets_length, Percentage = model.analyze_user_tweets(
                    user_file, vectorizer, best_model
                )
                if not tweets_length:
                    error_message = "عدد التغريدات غير كافي"

                    if error_message:
                        st.markdown(
                            f"""
                                            <div class="error-message">{error_message}
                                            </div> 
                                        
                                            """,
                            unsafe_allow_html=True,
                        )

                else:
                    warning_message = ""
                    if Percentage >= 60:
                        warning_message = "تحذير : احتمالية اكتئاب عالية."

                    imagePath = "../Images/" + user_file + ".png"
                    st.markdown(
                        f"""
                                        <div class='parent'>
                                    <div class="image-container"> <h4 class='titles'>ابرز العلامات</h4>
                                        {img_to_html(imagePath)}</div> 
                                        <div class="container-like"><h4 class='titles'> احتمالية الاكتئاب </h4>
                                        <h1 class='percentage'>{Percentage:.2f}%</h1> 
                                        <div>{f"<div class='warning-message'>{warning_message}</div>" if warning_message else ""}</div>
                                        </div>
                                        </div>
                                        """,
                        unsafe_allow_html=True,
                    )

                    # Check if the probability is higher than 60%
                    if Percentage >= 60:
                        st.markdown(
                            """<div style="text-align: center; align-items:center font-family:myFirstFont; color:#373d3f;;">
                                                <h2>عيادات قد تفيدك
                                                </h2></div>""",
                            unsafe_allow_html=True,
                        )
                        clinics = [
                            {
                                "name": "لبيه",
                                "link": "https://labayh.net/ar/",
                                "description": """تطبيق لبيه هو الحل المتكامل لتقديم خدمات الرعاية والرفاهية النفسية عن بعد، عبر الجلسات والمحاضرات ومجموعات الدعم المقدمة من المختصين المرخصين. حمل تطبيق لبيه و ابدأ رحلة التعافي الآن""",
                            },
                            {
                                "name": "عناية",
                                "link": "https://academicadvising.imamu.edu.sa/Enaya",
                                "description": "خدمة متخصصة لتقديم خدمات علاجية وارشادية لدعم وتحقيق الصحة النفسية لدى طلاب وطالبات ومنسوبي جامعة الامام محمد بن سعود الإسلامية",
                            },
                        ]
                        for i, clinic in enumerate(clinics, start=1):
                            st.markdown(
                                f"""
                                        <div class="parent-clinic">
                                        <a href="{clinic['link']}" style="text-decoration:none;">
                                        <div class="clinics">
                                        <div class='red-box'>
                                        </div>

                                        <h2 style="direction: rtl;">{str(i)}.{clinic['name']}</h2>
                                        <p>{clinic['description']}</p>
                                        </div>
                                        </a>
                                        </div>
                                        """,
                                unsafe_allow_html=True,
                            )
