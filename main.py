import streamlit as st 
from streamlit_option_menu import option_menu
from st_pages import Page, show_pages, hide_pages

import home, tool


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
                options=['Home','Tool'],
                icons=['house-fill'],
                # menu_icon='chat-text-fill',
                menu_icon='cast',
                default_index=0,
                # styles={
                #     "container": {"padding": "5!important","background-color":'black'},
                #     "icon": {"color": "white", "font-size": "23px"}, 
                #     "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
                #     "nav-link-selected": {"background-color": "#02ab21"},}
                
                # )
                orientation= 'horizontal'
            )
        hide_pages([Page("tool.py","Tool")
    ])

        if app == 'Home':
                home.app()
        if app == 'Tool':
                tool.app()
            
    run()
