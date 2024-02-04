import streamlit as st
import base64
from pathlib import Path


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid' style='width:101%; height:70%;'>".format(
        img_to_bytes(img_path)
    )
    return img_html


def app():

    # style
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
        width:150%;
        height:130%;
        margin-left:-11.5rem;
      
        

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
        width:80%;
        height:25rem;
        left:7.5rem;
     
        
        
    }
    .image{
        position: relative;
        bottom:5.3rem;
        right:0rem;
        width:45%;
        height:140%;
    }

    @font-face {
      font-family: myFirstFont;
      src: url(NotoNaskhArabic-Medium.ttf);
      font-weight: bold;
    }
    .title{
        font-family: sans-serif;
        color:#373d3f;
        font-size:2.5rem;
        position: relative;
        left:4.5em;
        
       
        
    }
    .about-text{
        font-family: sans-serif;
        color:#373d3f;
        font-size:1.2rem;
        font-weight:bold;
        position: relative;
        bottom:33rem;
        text-align:right;
        margin-right:3.5%;
    }

                                



                            </style>
                            """,
        unsafe_allow_html=True,
    )

    # Streamlit UI
    st.markdown(
        "<h1 style='text-align:center;'class='titles'> </h1>", unsafe_allow_html=True
    )

    # Display accuracy

    st.markdown(
        f"""
                                <div class='parent'>
                                <div class="container-like">
                               <h2 class='title'> من نحن؟ </h2>
                               <div class='image'>
                               {img_to_html('../Images/logo2.jpg')}
                               </div>
                               <p class="about-text">أداة تهدف لاكتشاف الحالات المحتملة وعلامات الإكتئاب في  <br> المملكة العربية السعودية من خلال تحليل التغريدات العربية<br> وإظهار مدى انتشار هذه العلامات كاستجابة للمخاوف المتعلقة<br> بالصحة العقلية</p>
                               </div>
                                </div>
                        """,
        unsafe_allow_html=True,
    )
