from fasthtml.common import *
from monsterui.all import *
import time
from fasthtml.components import Uk_theme_switcher

app, rt = fast_app(hdrs=Theme.blue.headers())

@rt
def index(): 
    return Titled("Loading Demo", 
        Button("Load", id='load', 
               hx_get=load, hx_target='#content', hx_swap='beforeend',
               hx_indicator='#loading'), 
        Div(id='content'), 
        Loading(id='loading', htmx_indicator=True)) 

@rt
def load(): 
    time.sleep(1)
    return P("Loading Demo")

@rt
def theme(): return Uk_theme_switcher()

serve()
