import streamlit as st 
from streamlit_option_menu import option_menu

import home, tool,login
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
                options=['Home','Tool',"About Us",'Log In'],
                icons=['house-fill'],
                # menu_icon='chat-text-fill',
                menu_icon='cast',
                default_index=0,
                styles={
                    "container": {"background-color":'#f2f2f2'},
                    # "icon": {"color": "white", "font-size": "23px"}, 
                    # "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#ee5b4d"}
                    },
                
                
                orientation= 'horizontal'
            )

        if app == 'Home':
                home.app()
        if app == 'Tool':
                tool.app()
        if app == 'Log In':
            login.app()

            
    run()
