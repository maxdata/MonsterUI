"MonsterUI Scrollspy Example application" 

from fasthtml.common import *
from monsterui.all import *
import random

# Using the "slate" theme with Highlight.js enabled
hdrs = Theme.slate.headers(highlightjs=True)
app, rt = fast_app(hdrs=hdrs)

################################
### Example Data and Content ###
################################
products = [
    {"name": "Laptop", "price": "$999"},
    {"name": "Smartphone", "price": "$599"}
]

code_example = """
# Python Code Example
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))
"""
testimonials = [
    {"name": "Alice", "feedback": "Great products and excellent customer service!"},
    {"name": "Bob", "feedback": "Fast shipping and amazing quality!"},
    {"name": "Charlie", "feedback": "Amazing experience! Will definitely buy again."},
    {"name": "Diana", "feedback": "Affordable prices and great variety!"},
    {"name": "Edward", "feedback": "Customer support was very helpful."},
    {"name": "Fiona", "feedback": "Loved the design and quality!"}
]

# Team members
team = [
    {"name": "Isaac Flath", "role": "CEO"},
    {"name": "Benjamin Clavié", "role": "AI Researcher"},
    {"name": "Alexis Gallagher", "role": "ML Engineer"},
    {"name": "Hamel Husain", "role": "Data Scientist"},
    {"name": "Austin Huang", "role": "Software Engineer"},
    {"name": "Benjamin Warner", "role": "Product Manager"},
    {"name": "Jonathan Whitaker", "role": "UX Designer"},
    {"name": "Kerem Turgutlu", "role": "DevOps Engineer"},
    {"name": "Curtis Allan", "role": "DevOps Engineer"},
    {"name": "Audrey Roy Greenfeld", "role": "Security Analyst"},
    {"name": "Nathan Cooper", "role": "Full Stack Developer"},
    {"name": "Jeremy Howard", "role": "CTO"},
    {"name": "Wayde Gilliam", "role": "Cloud Architect"},
    {"name": "Daniel Roy Greenfeld", "role": "Blockchain Expert"},
    {"name": "Tommy Collins", "role": "AI Ethics Researcher"}
]


def ProductCard(p,img_id=1):
    return Card(
        PicSumImg(w=500, height=100, id=img_id),
        DivFullySpaced(H4(p["name"]), P(Strong(p["price"], cls=TextT.sm))), 
        Button("Details", cls=(ButtonT.primary, "w-full")))

def TestimonialCard(t,img_id=1):
    return Card(
        DivLAligned(PicSumImg(w=50, h=50, cls='rounded-full', id=img_id), H4(t["name"])), 
        P(Q((t["feedback"]))))


def TeamCard(m,img_id=1): 
    return Card(
        DivLAligned(
            PicSumImg(w=50, h=50, cls='rounded-full', id=img_id), 
            Div(H4(m["name"]), P(m["role"]))),
        DivRAligned(
            UkIcon('twitter', cls='w-5 h-5'), 
            UkIcon('linkedin', cls='w-5 h-5'),
            UkIcon('github', cls='w-5 h-5'),
            cls=TextT.gray+'space-x-2'
        ),
        cls='p-3')

################################
### Navigation and Scrollspy ###
################################

scrollspy_links = (
                A("Welcome",      href="#welcome-section"),
                A("Products",     href="#products-section"),
                A("Testimonials", href="#testimonials-section"), 
                A("Team",         href="#team-section"),
                A("Code Example", href="#code-section"))
@rt
def index():
    def _Section(*c, **kwargs): return Section(*c, cls='space-y-3 my-48',**kwargs)
    return Container(
        NavBar(
            *scrollspy_links,
            brand=DivLAligned(H3("Scrollspy Demo!"),UkIcon('rocket',height=30,width=30)),
            sticky=True, uk_scrollspy_nav=True,
            scrollspy_cls=ScrollspyT.bold),
        NavContainer(
            *map(Li, scrollspy_links),
            uk_scrollspy_nav=True,
            sticky=True,
            cls=(NavT.primary,'pt-20 px-5 pr-10')),
        Container(
            # Notice the ID of each section corresponds to the `scrollspy_links` dictionary
            # So in scollspy `NavContainer` the `href` of each `Li` is the ID of the section
            DivCentered(
                H1("Welcome to the Store!"), 
                Subtitle("Explore our products and enjoy dynamic code examples."), 
                id="welcome-section"),
            _Section(H2("Products"),
                     Grid(*[ProductCard(p,img_id=i) for i,p in enumerate(products)], cols_lg=2),                   
                     id="products-section"),
            _Section(H2("Testimonials"), 
                     Slider(*[TestimonialCard(t,img_id=i) for i,t in enumerate(testimonials)]),       
                     id="testimonials-section"),
            _Section(H2("Our Team"), 
                     Grid(*[TeamCard(m,img_id=i) for i,m in enumerate(team)], cols_lg=2, cols_max=3),                          
                     id="team-section"),
            _Section(H2("Code Example"), 
                     CodeBlock(code_example, lang="python"),                             
                     id="code-section")), 
            cls=(ContainerT.xl,'uk-container-expand'))

serve()
