import streamlit as st 
from streamlit_option_menu import option_menu

# import Pages.home as home, Pages.tool as tool, Pages.about as about
from Pages import home, tool, about

import base64
from pathlib import Path


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid' style='width:100%;'>".format(
      img_to_bytes(img_path)
    )
    return img_html

logo_image = "../Images/logo.jpg"  # Provide the correct path to your logo

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
    
    .logo{
        width:30%;
        position:relative;
        margin-left:-25rem;
        top:-2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

class MultiApp:
    
    def __init__(self):
        self.apps={}
        
    def add_app(self,title, function):
        self.apps.append({
            'title':title,
            'function':function
        })
        
    def run():
        # app = st.sidebar(
        app = option_menu(
        
                menu_title=None,
                options=['الرئيسية',"الاداة",'من نحن'],
                icons=['house-fill'],
                # menu_icon='chat-text-fill',
                menu_icon='cast',
                default_index=0,
                styles={
                    "container": {"background-color":'#f2f2f2',"direction": "rtl"},
                    # "icon": {"color": "white", "font-size": "23px"}, 
                    # "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#ee5b4d"}
                    },
                
                
                orientation= 'horizontal'
            )

        if app == 'الرئيسية':
                home.app()
        if app == 'الاداة':
                tool.app()
        if app == "من نحن":
            about.app()
            
    run()

    footer="""<style>


    .footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    height:7%;
    background-color: #f2f2f2;
    color: black;
    text-align: center;
    }
    .icon{
        width:1.3rem;
        position:relative;
        left:41.2rem;
        bottom:-0.7rem;
    }
    .footer-text{
        font-size:0.7rem;
        position:relative;
        top:2.1rem;
    }
    .email-text{
        align-items: center;
         position:relative;
        left:43rem;
        bottom:0.8rem;
       
        
        
    }
    .email-div{
        position:fixed;
        padding:0%;
        
    }
    </style>
    
    """
    st.markdown(footer,unsafe_allow_html=True)
    st.write(f"""   <div class="footer">
    <div class="email-div">
    <div class='icon'>{img_to_html("../Images/iconsemail.png")} </div>
    <p class='email-text'>ArabMindGuard@gmail.com</p> 
    </div>
    <p class='footer-text'> Arab Mind Guard @ 2023</p>
    </div>""", unsafe_allow_html=True)

    

