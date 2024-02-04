import streamlit as st
import base64
from pathlib import Path
import graphics


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
        width:75%;
        height:25rem;
     
        
        
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
        font-size:2rem;
        
        
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
        width:75%;
        margin-right:2rem;
                                }
    .image-container h4{
        padding-bottom:2rem;
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
.caption{
    margin:0.5rem;
    margin-bottom:2rem;
}
.caption p{
    font-family: myFirstFont;
    color:#373d3f;
    text-align:center;
    font-size:1.3rem;
}


                            </style>
                            """,
        unsafe_allow_html=True,
    )

    # Get the Plotly chart
    graphics.chart()
    # Streamlit UI
    st.markdown(
        "<h1 style='text-align:center;'class='titles'>احصائية الاكتئاب في تويتر السعودية</h1>",
        unsafe_allow_html=True,
    )

    # Display accuracy
    st.markdown(
        f"""
                                <div class='caption'>
                                <p>هذة الاحصائيات شهرية بناءً على تغريدات مستخدمي تويتر في منطقة المملكة العربية السعودية</p>
                                </div>
                        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
                                <div class='parent'>
                               <div class="image-container"> <h4 class='titles'>ابرز العلامات</h4>
                                {img_to_html("../Images/dataset.png")}</div> 
                                 <div class="container-like"> <h4 class='titles'>احصائيات سنة 2023</h4>
                                {img_to_html("../Images/chart.png")}</div> 
                           
                                </div>
                        """,
        unsafe_allow_html=True,
    )
