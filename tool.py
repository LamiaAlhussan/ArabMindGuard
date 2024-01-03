# tool.py
import streamlit as st
import joblib
# import LR_model as model
import gather_user_tweets 
import numpy as np
from PIL import Image
from htbuilder.utils import styles
from nltk import probability
import base64
from pathlib import Path


# import main


# Load the logistic regression model
# model_filename = 'logistic_regression_model.pkl'
# logistic_regression_model = joblib.load(model_filename)
# best_model= joblib.load('LR_Model.pkl')
# vectorizer = joblib.load('vectorizer.pkl')

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

        
    }
                            </style>
                            """
                            , unsafe_allow_html=True
                        )
    
    twitter_account=''
    pressed = False
    # show_pages([Page("tool.py","Tool"),
    #             Page("home.py","Home")
    # ])
    # hide_pages(['Tool','Home'])
    
    st.markdown("<h1 align='center' style='font-family:myFirstFont; color:#373d3f;'>اداة تحديد الاكتئاب</h1>", unsafe_allow_html=True)

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

    # Create the text input
    # col1,col2 = st.columns([1,1])
    # with col2:
    #     buff, col = st.columns([1,4])
    #     st.text_input("")
    # with col1:
    #     buff, col = st.columns([1,4])
    #     st.button("اجرب")

    instr = ''

    
        # Create two columns; adjust the ratio to your liking
    col1, col2 ,cl= st.columns([5,13,2]) 

        # Use the first column for text input
    with col2:
            twitter_account = st.text_input(
                instr,
                value=instr,
                placeholder=instr,
                label_visibility='collapsed',
            
            )
        # Use the second column for the submit button
    with col1:
            buff, col ,buff2= st.columns([4,1,4])
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
               # Display entered Twitter account
            if buff2.button('جرب'):
                pressed =True

    if pressed:
        if twitter_account:
                        col1, col2 = st.columns(2) 
                        user_file = twitter_account+'.csv'
                        # gather_user_tweets.fetch_and_save_tweets(twitter_account,user_file)
                        # Percentage = model.analyze_user_tweets("sah_khail.csv",vectorizer,best_model)
                        # Predict depression probability
                            # Predict depression probability



                        col1, col2,col3,col4 = st.columns(4)

# Add custom styling to align the text input to the right

                        # Create two columns; adjust the ratio to your liking

                        # Use the first column for text input
                       
                        

                            # Add a container-like effect for text content with dynamic probability
                        probability = 60  # Replace with your dynamic value
                        warning_message =""
                        if probability >= 60:
                            warning_message= "تحذير : احتمالية اكتئاب عالية."
                        
                        st.markdown(
                                f"""
                                <div class='parent'>
                               <div class="image-container"> <h4 class='titles'>ابرز العلامات</h4>
                                {img_to_html("depression_wordcloud.png")}</div> 
                                <div class="container-like"><h4 class='titles'> احتمالية الاكتئاب </h4>
                                <h1 class='percentage'>{probability}%</h1> 
                                <div class="warning-message">{warning_message}
                                </div> 
                                </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        # Use the second column for the image container
                        
                        # buff, col, buff2 = st.columns([4, 1, 4])
                        #     # image = Image.open('depression_wordcloud.png')
                        # #   st.image(image, caption='3 marla plot',use_column_width=True)
                        #     # Add a container-like effect for the image
                        # st.markdown(
                        #         f"""<div class='parent' < </div>""",
                        #         unsafe_allow_html=True
                        #     )


            
                        # with col2:
                            
                        #     probability = 60
                        #         # write_style = """
                        #         #         <style>
                        #         #         .stWrite {
                        #         #             width: 120%;
                        #         #             height: 50%;
                        #         #             font-size:10px;
                        #         #         }
                        #         #         </style>
                        #         #         """
                        #         # st.markdown(write_style, unsafe_allow_html=True)
                        #         # st.markdown("<h4 align='center'>نسبة الاكتئاب       </h4>", unsafe_allow_html=True)
                                
                        #     st.write(f"{probability}%: احتمالية الاكتئاب ")
                

                        # with col1:
                            
                        #     image = Image.open('depression_wordcloud.png')
                        #     st.image(image, caption='3 marla plot',use_column_width=True)

                                # Check if the probability is higher than 60%
                        if 60 >= 60:
                            st.markdown("""<div style="text-align: center; align-items:center font-family:myFirstFont; color:#373d3f;;">
                                        <h2>عيادات قد تفيدك
                                        </h2></div>""",unsafe_allow_html=True)
                            clinics = [
                            {"name": "لبيه", "link": "https://labayh.net/ar/", "description": """تطبيق لبيه هو الحل المتكامل لتقديم خدمات الرعاية والرفاهية النفسية عن بعد،
                             عبر الجلسات والمحاضرات ومجموعات الدعم المقدمة من المختصين المرخصين. حمل تطبيق لبيه و ابدأ رحلة التعافي الآن"""},
                            {"name": "عناية", "link": "https://academicadvising.imamu.edu.sa/Enaya", "description": "خدمة متخصصة لتقديم خدمات علاجية وارشادية لدعم وتحقيق الصحة النفسية لدى طلاب وطالبات ومنسوبي جامعة الامام محمد بن سعود الإسلامية"},
                            # Add more clinics as needed
                        ]
                            for i, clinic in enumerate(clinics, start=1):
                                st.markdown( f'''
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
                                ''',unsafe_allow_html=True)

                            # List of clinics

                        # Display the creative list
             
                            
                                # st.markdown(
                                #     f"""
                                #         <div style="direction: rtl; text-align: right; align-items:right; font-family:myFirstFont; color:#373d3f;">
                                #             <p style="font-size:2rem; font-weight:bold; ">{str(i)}.{clinic['name']}</p>
                                #             <a href="{clinic['link']}">تصفح العيادة</a>
                                #             <p>{clinic['description']}</p>
                                #         </div>
                                #         """,unsafe_allow_html=True
                                # )
                                # # st.image("clinic_image_placeholder.png", caption=f"Image for {clinic['name']}", use_column_width=True)
                                # st.write("---") 
                            # st.write("هنا بعض العيادات الي ممكن تساعدك")
                            # st.markdown("[1-لبيه](https://labayh.net/ar/)")
                            # st.markdown("[2-عناية](https://academicadvising.imamu.edu.sa/Enaya)")  
            
# Set the width explicitly (e.g., 300 pixels)
    # st.markdown(
    #     """
    #     <style>
    #         div[data-baseweb="input"] input {
    #             width: 30%;  /* Adjust the width as needed */
    #         }
    #     </style>
    #     """,
    #     unsafe_allow_html=True,
    # )
        
    
 

