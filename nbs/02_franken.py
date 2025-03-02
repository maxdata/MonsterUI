import fasthtml.common as fh
from monsterui.foundations import *
from fasthtml.common import Div, P, Span, FT
from enum import Enum, auto
from fasthtml.components import Uk_select,Uk_input_tag,Uk_icon
from functools import partial
from itertools import zip_longest
from typing import Union, Tuple, Optional, Sequence
from fastcore.all import *
import copy, re, httpx, os
from pathlib import Path
from mistletoe.html_renderer import HTMLRenderer
from mistletoe.span_token import Image
from pathlib import Path
import mistletoe
from lxml import html, etree
from fasthtml.components import Uk_input_range
import fasthtml.components as fh_comp


from fasthtml.jupyter import *
from monsterui.core import Theme

if 'server' in globals(): server.stop()
#| export
app,rt = fh.fast_app(pico=False, hdrs=(Theme.violet.headers()),
                  static_path=os.path.abspath('.'), nb_hdrs=False,
                  bodykw={"class":"uk-overflow-auto min-h-screen"})

server = JupyUvi(app)
Show = partial(HTMX, app=app)


# ## Text Style

# In[ ]:


#| export
class TextT(VEnum):
    'Text Styles from https://franken-ui.dev/docs/text'
    def _generate_next_value_(name, start, count, last_values):
        return str2ukcls('text', name)
    
    paragraph = "uk-paragraph"
    # Text Style
    lead,meta, gray, italic= auto(), auto(), 'text-gray-500 dark:text-gray-200', 'italic'
    # Text Size
    xs, sm, lg, xl = 'text-xs', 'text-sm', 'text-lg', 'text-xl'
    # Text Weight
    light, normal, medium, bold, extrabold = 'font-normal','font-light','font-medium','font-bold','font-extrabold'
    # Text Color
    muted,primary,secondary = 'text-gray-500 dark:text-gray-200', 'text-primary', 'text-secondary'
    success,warning, error, info =  'text-success', 'text-warning', 'text-error', 'text-info'
    # Text Alignment
    left, right,center = "text-left","text-right","text-center"
    justify, start, end = "text-justify","text-start","text-end"
    # Vertical Alignment
    top,middle,bottom = 'align-top','align-middle','align-bottom'
    # Text Wrapping
    truncate,break_,nowrap = 'uk-text-truncate','uk-text-break', 'uk-text-nowrap' 
    # other
    underline = 'underline'
    highlight = 'bg-yellow-200 dark:bg-yellow-800 text-black'
class TextPresets(VEnum):
    'Common Typography Presets'
    muted_sm = TextT.muted+TextT.sm
    muted_lg = TextT.muted+TextT.lg
    
    bold_sm = TextT.bold+TextT.sm
    bold_lg = TextT.bold+TextT.lg
    
    md_weight_sm = stringify((TextT.sm, TextT.medium))
    md_weight_muted = stringify((TextT.medium, TextT.muted))


# In[ ]:


#| export
def CodeSpan(*c, # Contents of CodeSpan tag (inline text code snippets)
             cls=(), # Classes in addition to CodeSpan styling
             **kwargs # Additional args for CodeSpan tag
             )->FT: # Code(..., cls='uk-codespan')
    "A CodeSpan with Styling"
    return fh.Code(*c, cls=('uk-codespan', stringify(cls)), **kwargs)


# In[ ]:


#| export
def CodeBlock(*c: str, # Contents of Code tag (often text)
              cls: Enum | str | tuple = (), # Classes for the outer container
              code_cls: Enum | str | tuple = (), # Classes for the code tag
              **kwargs # Additional args for Code tag
              ) -> FT: # Div(Pre(Code(..., cls='uk-codeblock), cls='multiple tailwind styles'), cls='uk-block')
    "CodeBlock with Styling"
    return Div(
        Pre(Code(*c, cls=('uk-codeblock', stringify(code_cls)), **kwargs),
            cls=(f'bg-gray-100 dark:bg-gray-800 {TextT.gray} p-0.4 rounded text-sm font-mono')),
#             cls=('bg-gray-100 dark:bg-gray-800 dark:text-gray-200 p-0.4 rounded text-sm font-mono')),
        cls=('uk-block', stringify(cls)))


# In[ ]:


#| export
def H1(*c:FT|str, # Contents of H1 tag (often text)
       cls:Enum|str|tuple=(), # Classes in addition to H1 styling
       **kwargs # Additional args for H1 tag
       )->FT: # H1(..., cls='uk-h1')
    "H1 with styling and appropriate size"
    return fh.H1(*c, cls=('uk-h1',stringify(cls)), **kwargs)


# In[ ]:


#| export
def H2(*c:FT|str, # Contents of H2 tag (often text)
       cls:Enum|str|tuple=(), # Classes in addition to H2 styling
       **kwargs # Additional args for H2 tag
       )->FT: # H2(..., cls='uk-h2')
    "H2 with styling and appropriate size"
    return fh.H2(*c, cls=('uk-h2',stringify(cls)), **kwargs)


# In[ ]:


#| export
def H3(*c:FT|str, # Contents of H3 tag (often text)
       cls:Enum|str|tuple=(), # Classes in addition to H3 styling
       **kwargs # Additional args for H3 tag
       )->FT: # H3(..., cls='uk-h3')
    "H3 with styling and appropriate size"
    return fh.H3(*c, cls=('uk-h3',stringify(cls)), **kwargs)


# In[ ]:


#| export
def H4(*c:FT|str, # Contents of H4 tag (often text)
       cls:Enum|str|tuple=(), # Classes in addition to H4 styling
       **kwargs # Additional args for H4 tag
       )->FT: # H4(..., cls='uk-h4')
    "H4 with styling and appropriate size"
    return fh.H4(*c, cls=('uk-h4',stringify(cls)), **kwargs)


# In[ ]:


#| export
def H5(*c:FT|str, # Contents of H5 tag (often text)
       cls:Enum|str|tuple=(), # Classes in addition to H5 styling
       **kwargs # Additional args for H5 tag
       )->FT: # H5(..., cls='text-lg font-semibold')
    "H5 with styling and appropriate size"
    return fh.H5(*c, cls=('text-lg font-semibold',stringify(cls)), **kwargs)

def H6(*c:FT|str, # Contents of H6 tag (often text)
       cls:Enum|str|tuple=(), # Classes in addition to H6 styling
       **kwargs # Additional args for H6 tag
       )->FT: # H6(..., cls='text-base font-semibold')
    "H6 with styling and appropriate size"
    return fh.H6(*c, cls=('text-base font-semibold',stringify(cls)), **kwargs)


# In[ ]:


#| export
def Subtitle(*c:FT|str, # Contents of P tag (often text)
         cls:Enum|str|tuple='mt-1.5', # Additional classes
         **kwargs # Additional args for P tag
         )->FT:
    "Styled muted_sm text designed to go under Headings and Titles"
    return fh.P(*c, cls=(TextPresets.muted_sm, stringify(cls)), **kwargs)


# In[ ]:


#| export
def Q(*c:FT|str, # Contents of Q tag (quote)
      cls:Enum|str|tuple=(), # Additional classes
      **kwargs # Additional args for Q tag
      )->FT:
    "Styled quotation mark"
    return fh.Q(*c, cls=(TextT.italic,TextT.lg, stringify(cls)), **kwargs)

def Em(*c:FT|str, # Contents of Em tag (emphasis)
       cls:Enum|str|tuple=(), # Additional classes 
       **kwargs # Additional args for Em tag
       )->FT:
    "Styled emphasis text"
    return fh.Em(*c, cls=(TextT.medium, stringify(cls)), **kwargs)

def Strong(*c:FT|str, # Contents of Strong tag
          cls:Enum|str|tuple=(), # Additional classes
          **kwargs # Additional args for Strong tag
          )->FT:
    "Styled strong text" 
    return fh.Strong(*c, cls=(TextT.bold, stringify(cls)), **kwargs)

def I(*c:FT|str, # Contents of I tag (italics)
      cls:Enum|str|tuple=(), # Additional classes
      **kwargs # Additional args for I tag
      )->FT:
    "Styled italic text"
    return fh.I(*c, cls=(TextT.italic, stringify(cls)), **kwargs)

def Small(*c:FT|str, # Contents of Small tag
         cls:Enum|str|tuple=(), # Additional classes
         **kwargs # Additional args for Small tag
         )->FT:
    "Styled small text"
    return fh.Small(*c, cls=(TextT.sm, stringify(cls)), **kwargs)

def Mark(*c:FT|str, # Contents of Mark tag (highlighted text)
        cls:Enum|str|tuple=(), # Additional classes
        **kwargs # Additional args for Mark tag
        )->FT:
    "Styled highlighted text"
    return fh.Mark(*c, cls=(TextT.highlight, stringify(cls)), **kwargs)


# In[ ]:


#| export
def Del(*c:FT|str, # Contents of Del tag (deleted text)
       cls:Enum|str|tuple=(), # Additional classes
       **kwargs # Additional args for Del tag
       )->FT:
    "Styled deleted text"
    return fh.Del(*c, cls=('line-through', TextT.gray, stringify(cls)), **kwargs)

def Ins(*c:FT|str, # Contents of Ins tag (inserted text)
        cls:Enum|str|tuple=(), # Additional classes
        **kwargs # Additional args for Ins tag
        )->FT:
    "Styled inserted text"
    return fh.Ins(*c, cls=(TextT.underline+' text-green-600', stringify(cls)), **kwargs)

def Sub(*c:FT|str, # Contents of Sub tag (subscript)
       cls:Enum|str|tuple=(), # Additional classes
       **kwargs # Additional args for Sub tag
       )->FT:
    "Styled subscript text"
    return fh.Sub(*c, cls=(TextT.sm+' -bottom-1 relative', stringify(cls)), **kwargs)

def Sup(*c:FT|str, # Contents of Sup tag (superscript) 
        cls:Enum|str|tuple=(), # Additional classes
        **kwargs # Additional args for Sup tag
        )->FT:
    "Styled superscript text"
    return fh.Sup(*c, cls=(TextT.sm+' -top-1 relative', stringify(cls)), **kwargs)


# In[ ]:


#| export
def Blockquote(*c:FT|str, # Contents of Blockquote tag (often text)
               cls:Enum|str|tuple=(), # Classes in addition to Blockquote styling
               **kwargs # Additional args for Blockquote tag
               )->FT: # Blockquote(..., cls='uk-blockquote')
    "Blockquote with Styling"
    return fh.Blockquote(*c, cls=('uk-blockquote',stringify(cls)), **kwargs)


# In[ ]:


#| export
def Caption(*c:FT|str, cls:Enum|str|tuple=(), **kwargs)->FT:
    "Styled caption text"
    return fh.Caption(
        Span(*c, cls=(TextT.gray, TextT.sm, stringify(cls))),
        **kwargs)


# In[ ]:


#| export
def Cite(*c:FT|str, # Contents of Cite tag
         cls:Enum|str|tuple=(), # Additional classes
         **kwargs # Additional args for Cite tag
         )->FT:
    "Styled citation text"
    return fh.Cite(*c, cls=(TextT.italic, TextT.gray, stringify(cls)), **kwargs)

def Time(*c:FT|str, # Contents of Time tag
         cls:Enum|str|tuple=(), # Additional classes
         datetime:str=None, # datetime attribute
         **kwargs # Additional args for Time tag
         )->FT:
    "Styled time element"
    if datetime: kwargs['datetime'] = datetime
    return fh.Time(*c, cls=(TextT.gray, stringify(cls)), **kwargs)

def Address(*c:FT|str, # Contents of Address tag
           cls:Enum|str|tuple=(), # Additional classes
           **kwargs # Additional args for Address tag
           )->FT:
    "Styled address element"
    return fh.Address(*c, cls=(TextT.italic, stringify(cls)), **kwargs)


# In[ ]:


demo = Div(
            H1("MonsterUI's Semantic Text"),
            P(
                Strong("MonsterUI"), " brings the power of semantic HTML to life with ",
                Em("beautiful styling"), " and ", Mark("zero configuration"), "."
            ),
            Blockquote(
                P("Write semantic HTML in pure Python, get modern styling for free."),
                Cite("MonsterUI Team")
            ),
            footer=Meta("Released February 2025"),
        )

Show(demo)


# In[ ]:


#| export
def Abbr(*c:FT|str, # Contents of Abbr tag
         cls:Enum|str|tuple=(), # Additional classes
         title:str=None, # Title attribute for abbreviation
         **kwargs # Additional args for Abbr tag
         )->FT:
    "Styled abbreviation with dotted underline"
    if title: kwargs['title'] = title
    return fh.Abbr(*c, cls=('border-b border-dotted border-secondary hover:cursor-help', stringify(cls)), **kwargs)

def Dfn(*c:FT|str, # Contents of Dfn tag (definition)
        cls:Enum|str|tuple=(), # Additional classes
        **kwargs # Additional args for Dfn tag
        )->FT:
    "Styled definition term with italic and medium weight"
    return fh.Dfn(*c, cls=(TextT.medium + TextT.italic + TextT.gray, stringify(cls)), **kwargs)

def Kbd(*c:FT|str, # Contents of Kbd tag (keyboard input)
        cls:Enum|str|tuple=(), # Additional classes
        **kwargs # Additional args for Kbd tag
        )->FT:
    "Styled keyboard input with subtle background"
    return fh.Kbd(*c, cls=('font-mono px-1.5 py-0.5 text-sm bg-secondary border border-gray-300 dark:border-gray-600 rounded shadow-sm', stringify(cls)), **kwargs)


# In[ ]:


#| export
def Samp(*c:FT|str, # Contents of Samp tag (sample output)
         cls:Enum|str|tuple=(), # Additional classes
         **kwargs # Additional args for Samp tag
         )->FT:
    "Styled sample output with subtle background"
    return fh.Samp(*c, cls=('font-mono bg-secondary px-1 rounded', TextT.gray, stringify(cls)), **kwargs)

def Var(*c:FT|str, # Contents of Var tag (variable)
        cls:Enum|str|tuple=(), # Additional classes
        **kwargs # Additional args for Var tag
        )->FT:
    "Styled variable with italic monospace"
    return fh.Var(*c, cls=('font-mono',TextT.italic + TextT.gray, stringify(cls)), **kwargs)


# In[ ]:


#| export
def Figure(*c:FT|str, # Contents of Figure tag
          cls:Enum|str|tuple=(), # Additional classes 
          **kwargs # Additional args for Figure tag
          )->FT:
    "Styled figure container with card-like appearance"
    return fh.Figure(*c, cls=('p-4 my-4 border border-gray-200 dark:border-gray-800 rounded-lg shadow-sm bg-card', stringify(cls)), **kwargs)


# In[ ]:


#| export
def Details(*c:FT|str, # Contents of Details tag
           cls:Enum|str|tuple=(), # Additional classes
           **kwargs # Additional args for Details tag
           )->FT:
    "Styled details element"
    return fh.Details(*c, cls=('border border-secondary rounded-lg', stringify(cls)), **kwargs)

def Summary(*c:FT|str, # Contents of Summary tag
           cls:Enum|str|tuple=(), # Additional classes
           **kwargs # Additional args for Summary tag
           )->FT:
    "Styled summary element"
    return fh.Summary(*c, cls=(TextT.medium + ' p-3 hover:bg-secondary cursor-pointer', stringify(cls)), **kwargs)

def Data(*c:FT|str, # Contents of Data tag
         value:str=None, # Value attribute
         cls:Enum|str|tuple=(), # Additional classes
         **kwargs # Additional args for Data tag
         )->FT:
    "Styled data element"
    if value: kwargs['value'] = value
    return fh.Data(*c, cls=('font-mono text-sm bg-secondary px-1 rounded', stringify(cls)), **kwargs)

def Meter(*c:FT|str, # Contents of Meter tag
          value:float=None, # Current value
          min:float=None, # Minimum value
          max:float=None, # Maximum value
          cls:Enum|str|tuple=(), # Additional classes
          **kwargs # Additional args for Meter tag
          )->FT:
    "Styled meter element"
    if value is not None: kwargs['value'] = value
    if min is not None: kwargs['min'] = min
    if max is not None: kwargs['max'] = max
    return fh.Meter(*c, cls=('w-full h-2 bg-secondary rounded', stringify(cls)), **kwargs)


# In[ ]:


#| export
def S(*c:FT|str, # Contents of S tag (strikethrough)
      cls:Enum|str|tuple=(), # Additional classes
      **kwargs # Additional args for S tag
      )->FT:
    "Styled strikethrough text (different semantic meaning from Del)"
    return fh.S(*c, cls=('line-through', TextT.gray, stringify(cls)), **kwargs)

def U(*c:FT|str, # Contents of U tag (unarticulated annotation)
      cls:Enum|str|tuple=(), # Additional classes
      **kwargs # Additional args for U tag
      )->FT:
    "Styled underline (for proper names in Chinese, proper spelling etc)"
    return fh.U(*c, cls=(TextT.underline, stringify(cls)), **kwargs)

def Output(*c:FT|str, # Contents of Output tag
          form:str=None, # ID of form this output belongs to
          for_:str=None, # IDs of elements this output is for
          cls:Enum|str|tuple=(), # Additional classes
          **kwargs # Additional args for Output tag
          )->FT:
    "Styled output element for form results"
    if form: kwargs['form'] = form
    if for_: kwargs['for'] = for_  # Note: 'for' is reserved in Python
    return fh.Output(*c, cls=('font-mono bg-secondary px-2 py-1 rounded', 
                             stringify(cls)), **kwargs)


# In[ ]:


#| export
def PicSumImg(h:int=200,           # Height in pixels
              w:int=200,           # Width in pixels
              id:int=None,        # Optional specific image ID to use
              grayscale:bool=False, # Whether to return grayscale version
              blur:int=None,       # Optional blur amount (1-10)
              **kwargs             # Additional args for Img tag
              )->FT:              # Img tag with picsum image
    "Creates a placeholder image using https://picsum.photos/"
    url = f"https://picsum.photos"
    if id is not None: url = f"{url}/id/{id}"
    url = f"{url}/{w}/{h}"
    if grayscale: url = f"{url}?grayscale"
    if blur is not None: 
        url = f"{url}{'?' if not grayscale else '&'}blur={max(1,min(10,blur))}"
    return fh.Img(src=url, loading="lazy", **kwargs)


# ## Button

# In[ ]:


#| export
class ButtonT(VEnum):
    "Options for styling Buttons"
    def _generate_next_value_(name, start, count, last_values): return str2ukcls('btn', name)
    default, ghost, primary = auto(),auto(),auto()
    secondary, destructive = auto(), auto()
    text, link = auto(), auto()
    xs, sm, lg, xl = auto(), auto(), auto(), auto()
    icon = auto()


# In[ ]:


#| export
def Button(*c: Union[str, FT], # Contents of `Button` tag (often text)
           cls: Union[str, Enum]=ButtonT.default, # Classes in addition to `Button` styling (use `ButtonT` for built in styles)
           submit=True, # Whether the button should submit a form
           **kwargs # Additional args for `Button` tag
           ) -> FT: # Button(..., cls='uk-btn')
    "Button with Styling (defaults to `submit` for form submission)"
    if 'type' not in kwargs: kwargs['type'] = 'submit' if submit else 'button'
    return fh.Button(*c, cls=('uk-btn', stringify(cls)), **kwargs)


# ## Headings

# In[ ]:


#| export
class ContainerT(VEnum):
    'Max width container sizes from https://franken-ui.dev/docs/container'
    def _generate_next_value_(name, start, count, last_values): return str2ukcls('container', name)
    xs = auto()
    sm = auto()
    lg = auto()
    xl = auto()
    expand = auto()


# In[ ]:


#| export
class BackgroundT(VEnum):
    def _generate_next_value_(name, start, count, last_values): return str2ukcls('background', name)
    muted = auto()
    primary = auto()
    secondary = auto()
    default = auto()


# In[ ]:


#| export
def Container(*c, # Contents of Container tag (often other FT Components)
              cls=('mt-5', ContainerT.xl), # Classes in addition to Container styling
              **kwargs # Additional args for Container (`Div` tag)
              )->FT: # Container(..., cls='uk-container')
    "Div to be used as a container that often wraps large sections or a page of content"
    return Div(*c, cls=('uk-container',stringify(cls)), **kwargs)


# In[ ]:


#| export
def Titled(title:str="FastHTML app", # Title of the page
           *c, # Contents of the page (often other tags)
           cls=ContainerT.xl, # Classes in addition to Container styling
           **kwargs # Additional args for Container (`Div` tag)
           )->FT: # Title, Main(Container(H1(title), content))
    "Creates a standard page structure for titled page.  Main(Container(title, content))"
    return fh.Title(title), fh.Main(Container(H1(title), *c, cls=cls, **kwargs))


# In[ ]:





# ## Dividers

# In[ ]:


#| export
class DividerT(VEnum):
    "Divider Styles from https://franken-ui.dev/docs/divider"
    def _generate_next_value_(name, start, count, last_values): return str2ukcls('divider', name)
    icon=auto()
    sm=auto()
    vertical=auto()


# In[ ]:


#| export
def Divider(*c, # contents of Divider tag (often nothing)
            cls=('my-4', DividerT.icon), # Classes in addition to Divider styling
            **kwargs # Additional args for Divider tag
            )->FT: #  Hr(..., cls='uk-divider-icon') or Div(..., cls='uk-divider-vertical')
    "Divider with default styling and margin"
    cls = stringify(cls)
    container = Div if 'uk-divider-vertical' in cls else Hr
    return container(*c, cls=cls, **kwargs)


# In[ ]:


#| export
def DividerSplit(*c, cls=(), line_cls=(), text_cls=()):
    "Creates a simple horizontal line divider with configurable thickness and vertical spacing"
    cls, line_cls, text_cls = map(stringify,(cls, line_cls, text_cls))
    return Div(cls='relative ' + cls)(
        Div(cls="absolute inset-0 flex items-center " + line_cls)(Span(cls="w-full border-t border-border")),
        Div(cls="relative flex justify-center " + text_cls)(Span(cls="bg-background px-2 ")(*c)))


# In[ ]:


#| export
def DividerLine(lwidth=2, y_space=4): return Hr(cls=f"my-{y_space} h-[{lwidth}px] w-full bg-secondary")


# ## Articles & Containers & Sections

# In[ ]:


#| export
def Article(*c, # contents of Article tag (often other tags)
            cls=(), # Classes in addition to Article styling
            **kwargs # Additional args for Article tag
            )->FT: # Article(..., cls='uk-article')
    "A styled article container for blog posts or similar content"
    return fh.Article(*c, cls=('uk-article',stringify(cls)), **kwargs)

def ArticleTitle(*c, # contents of ArticleTitle tag (often other tags)
                 cls=(), # Classes in addition to ArticleTitle styling
                 **kwargs # Additional args for ArticleTitle tag
                 )->FT: # H1(..., cls='uk-article-title')
    "A title component for use within an Article"
    return H1(*c, cls=('uk-article-title',stringify(cls)), **kwargs)

def ArticleMeta(*c, # contents of ArticleMeta tag (often other tags)
                cls=(), # Classes in addition to ArticleMeta styling
                **kwargs # Additional args for ArticleMeta tag
                )->FT: # P(..., cls='uk-article-meta')
    "A metadata component for use within an Article showing things like date, author etc"
    return P(*c, cls=('uk-article-meta',stringify(cls)), **kwargs)


# In[ ]:


# Article(ArticleTitle("Article Title"), ArticleMeta("By: John Doe"))


# In[ ]:


#| export
class SectionT(VEnum):
    'Section styles from https://franken-ui.dev/docs/section'
    def _generate_next_value_(name, start, count, last_values): return str2ukcls('section', name)
    default = auto()
    muted = auto()
    primary = auto()
    secondary = auto()
    xs = 'uk-section-xsmall'
    sm = 'uk-section-small'
    lg = 'uk-section-large'
    xl = 'uk-section-xlarge'
    remove_vertical = auto()


# In[ ]:


# Markdown(enum_to_markdown_table(SectionT))


# In[ ]:


#| export
def Section(*c, # contents of Section tag (often other tags)
            cls=(), # Classes in addition to Section styling
            **kwargs # Additional args for Section tag
            )->FT: # Div(..., cls='uk-section')
    "Section with styling and margins"
    return fh.Div(*c, cls=('uk-section',stringify(cls)), **kwargs)


# ## Forms & Inputs

# In[ ]:


#| export
def Form(*c, # contents of Form tag (often Buttons, FormLabels, and LabelInputs)
          cls='space-y-3', # Classes in addition to Form styling (default is 'space-y-3' to prevent scrunched up form elements)
          **kwargs # Additional args for Form tag
          )->FT: # Form(..., cls='space-y-3')
    "A Form with default spacing between form elements"
    return fh.Form(*c, cls=stringify(cls), **kwargs)


# In[ ]:


#|export
def Fieldset(*c, # contents of Fieldset tag (often other tags)
             cls=(), # Classes in addition to Fieldset styling
             **kwargs # Additional args for Fieldset tag
             )->FT: # Fieldset(..., cls='uk-fieldset')
    "A Fieldset with default styling"
    return fh.Fieldset(*c, cls=('uk-fieldset',stringify(cls)), **kwargs)

def Legend(*c, # contents of Legend tag (often other tags)
           cls=(), # Classes in addition to Legend styling
           **kwargs # Additional args for Legend tag
           )->FT: # Legend(..., cls='uk-legend')
    "A Legend with default styling"
    return fh.Legend(*c, cls=('uk-legend',stringify(cls)), **kwargs)


# In[ ]:


#| export
def Input(*c, # contents of Input tag (often nothing)
          cls=(), # Classes in addition to Input styling
          **kwargs # Additional args for Input tag
          )->FT: # Input(..., cls='uk-input')
    "An Input with default styling"
    return fh.Input(*c, cls=('uk-input',stringify(cls)), **kwargs)

def Radio(*c, # contents of Radio tag (often nothing)
           cls=(), # Classes in addition to Radio styling
           **kwargs # Additional args for Radio tag
           )->FT: # Input(..., cls='uk-radio', type='radio')
    "A Radio with default styling"
    return fh.Input(*c, cls=('uk-radio',stringify(cls)), type='radio', **kwargs)
def CheckboxX(*c, # contents of CheckboxX tag (often nothing)
               cls=(), # Classes in addition to CheckboxX styling
               **kwargs # Additional args for CheckboxX tag
               )->FT: # Input(..., cls='uk-checkbox', type='checkbox')
    "A Checkbox with default styling"
    return fh.Input(*c, cls=('uk-checkbox',stringify(cls)), type='checkbox', **kwargs)


# In[ ]:





# In[ ]:


#| export
def Range(*c, # contents of Range tag (often nothing)
          value='',
          label=True,
          min=None,
          max=None,
          step=None,
           cls=(), # Classes in addition to Range styling
           **kwargs # Additional args for Range tag
           )->FT: # Input(..., cls='uk-range', type='range')
    "A Range with default styling"
    return Uk_input_range(*c, min=min, label=label, max=max, value=value, multiple=len(value.split(','))>1, cls=('uk-range',stringify(cls)), **kwargs)


# In[ ]:


Range(label='kg', value="25,75")


# In[ ]:


Show(Range(label='kg', value="25,75"), link=True)


# In[ ]:


#| export
def TextArea(*c, # contents of TextArea tag (often text)
             cls=(), # Classes in addition to TextArea styling
             **kwargs # Additional args for TextArea tag
             )->FT: # TextArea(..., cls='uk-textarea')
    "A Textarea with default styling"
    return fh.Textarea(*c, cls=('uk-textarea',stringify(cls)), **kwargs)
def Switch(*c, # contents of Switch tag (often nothing)
           cls=(), # Classes in addition to Switch styling
           **kwargs # Additional args for Switch tag
           )->FT: # Input(..., cls='uk-toggle-switch uk-toggle-switch-primary min-w-9', type='checkbox')
    "A Switch with default styling"
    return fh.Input(*c, cls=('uk-toggle-switch uk-toggle-switch-primary min-w-9',stringify(cls)), type='checkbox', **kwargs)


# In[ ]:


#| export
def Upload(*c, # Contents of Upload tag button (often text)
          cls=(), # Classes in addition to Upload styling
          multiple=False, # Whether to allow multiple file selection
          accept=None, # File types to accept (e.g. 'image/*')
          button_cls=ButtonT.default, # Classes for the button
          id=None, # ID for the file input
          name=None, # Name for the file input
          **kwargs # Additional args for the outer div
          )->FT: # Div(Input(type='file'), Button(...))
    "A file upload component with default styling"
    input_kwargs = {'type': 'file', 'multiple': multiple}
    if accept: input_kwargs['accept'] = accept
    if id: input_kwargs['id'] = id
    if name: input_kwargs['name'] = name
    return Div(
        fh.Input(**input_kwargs),
        Button(*c, cls=button_cls, submit=False, tabindex="-1"),
        cls=('w-full js-upload', stringify(cls)),
        uk_form_custom=True)

def UploadZone(*c, # Contents of UploadZone tag (often text or other tags)
               cls=(), # Classes in addition to UploadZone styling
               multiple=False, # Whether to allow multiple file selection
               accept=None, # File types to accept (e.g. 'image/*')
               id=None, # ID for the file input
               name=None, # Name for the file input
               **kwargs # Additional args for the outer div
               )->FT:
    "A file drop zone component with default styling"
    input_kwargs = {'type': 'file', 'multiple': multiple}
    if accept: input_kwargs['accept'] = accept 
    if id: input_kwargs['id'] = id
    if name: input_kwargs['name'] = name
    return Div(
        Div(fh.Input(**input_kwargs),
            Span(*c),
            uk_form_custom=True, 
            cls='w-full'),
        cls=('js-upload uk-placeholder uk-text-center', stringify(cls)),
        **kwargs)


# In[ ]:


#|export
def FormLabel(*c, # contents of FormLabel tag (often text)
               cls=(), # Classes in addition to FormLabel styling
               **kwargs # Additional args for FormLabel tag
               )->FT: # Label(..., cls='uk-form-label')
    "A Label with default styling"
    return fh.Label(*c, cls=('uk-form-label',stringify(cls)), **kwargs)


# In[ ]:


#| export
class LabelT(VEnum):
    def _generate_next_value_(name, start, count, last_values): return str2ukcls('label', name)
    primary = auto()
    secondary = auto()
    danger = auto()


# In[ ]:


#| export
def Label(*c, # contents of Label tag (often text)
           cls=(), # Classes in addition to Label styling
           **kwargs # Additional args for Label tag
           )->FT: # Label(..., cls='uk-label')
    "FrankenUI labels, which look like pills"
    return fh.Label(*c, cls=('uk-label',stringify(cls)), **kwargs)


# In[ ]:


#| export
def UkFormSection(title, description, *c, button_txt='Update', outer_margin=6, inner_margin=6):
    "A form section with a title, description and optional button"
    return Div(cls=f'space-y-{inner_margin} py-{outer_margin}')(
        Div(H3(title), P(description, cls=TextPresets.muted_sm)),
        DividerSplit(), *c,
        Div(Button(button_txt, cls=ButtonT.primary)) if button_txt else None)


# ## Labeled Inputs

# Inputs of various types often go with a label.  Because of this we created functions to do this for you along with properly linking the `for` attribute from the lable to the input.  We also have some nice defaults, such as putting a little spacing between the label and the input

# In[ ]:


#| export
def GenericLabelInput(
               label:str|FT, # FormLabel content (often text)
               lbl_cls='', # Additional classes for FormLabel
               input_cls='', # Additional classes for user input (Input, Select, etc)
               container=Div, # Container to wrap label and input in (default is Div)
               cls='', # Classes on container (default is '')
               id=None, # id for label and input (`id`, `name` and `for` attributes are set to this value).  If `label` is str, this defaults to `label.lower()`
               input_fn=noop, # User input FT component 
                **kwargs # Additional args for user input
                ): 
    "`Div(Label,Input)` component with Uk styling injected appropriately. Generally you should higher level API, such as `LabelInput` which is created for you in this library"
    if not id and isinstance(label, str): id = label.lower()
    if isinstance(label, str) or label.tag != 'label': 
        label = FormLabel(cls=stringify(lbl_cls), fr=id)(label)
    inp = input_fn(id=id, cls=stringify(input_cls), **kwargs)        
    if container: return container(label, inp, cls=stringify(cls))
    return label, inp


# In[ ]:


#| export
def LabelInput(label:str|FT, # FormLabel content (often text)
               lbl_cls='', # Additional classes for `FormLabel`
               input_cls='', # Additional classes for `Input`
               cls='space-y-2', # Classes on container (default is `'space-y-2'` to prevent scrunched up form elements)
               id='', # id for `FormLabel` and `Input` (`id`, `name` and `for` attributes are set to this value)
                **kwargs # Additional args for `Input`
               )->FT:  # Div(cls='space-y-2')(`FormLabel`, `Input`)
    "A `FormLabel` and `Input` pair that provides default spacing and links/names them based on id"
    return GenericLabelInput(label=label, lbl_cls=lbl_cls, input_cls=input_cls,
                             container=Div, cls=cls, id=id, input_fn=Input, **kwargs)


# In[ ]:


#| export
def LabelTextArea(label:str|FT, # FormLabel content (often text)
                  value='', # Value for the textarea
                  lbl_cls='', # Additional classes for `FormLabel`
                  input_cls='', # Additional classes for `TextArea`
                  cls='space-y-2', # Classes on container (default is `'space-y-2'` to prevent scrunched up form elements)
                  id='', # id for `FormLabel` and `TextArea` (`id`, `name` and `for` attributes are set to this value)
                  **kwargs # Additional args for `TextArea`
                  )->FT:  # Div(cls='space-y-2')(`FormLabel`, `TextArea`)
    def text_area_with_value(**kw): return TextArea(value, **kw)
    return GenericLabelInput(label=label, lbl_cls=lbl_cls, input_cls=input_cls,
                             container=Div, cls=cls, id=id, input_fn=text_area_with_value, **kwargs)


# In[ ]:


#| export
@delegates(GenericLabelInput, but=['input_fn','cls'])
def LabelSwitch(label:str|FT, # FormLabel content (often text)
               lbl_cls='', # Additional classes for `FormLabel`
               input_cls='', # Additional classes for `Switch`
               cls='space-x-2', # Classes on container (default is `'space-x-2'` to prevent scrunched up form elements)
               id='', # id for `FormLabel` and `Switch` (`id`, `name` and `for` attributes are set to this value)
                **kwargs # Additional args for `Switch`
               )->FT:  # Div(cls='space-y-2')(`FormLabel`, `Switch`)
    return GenericLabelInput(label=label, lbl_cls=lbl_cls, input_cls=input_cls,
                             container=Div, cls=cls, id=id, input_fn=Switch, **kwargs)


# In[ ]:


#| export
def LabelRadio(label:str|FT, # FormLabel content (often text)
               lbl_cls='', # Additional classes for `FormLabel`
               input_cls='', # Additional classes for `Radio`
               container=Div, # Container to wrap label and input in (default is Div)
               cls='flex items-center space-x-2', # Classes on container (default is 'flex items-center space-x-2')
               id='', # id for `FormLabel` and `Radio` (`id`, `name` and `for` attributes are set to this value)
                **kwargs # Additional args for `Radio`
               )->FT:  # Div(cls='flex items-center space-x-2')(`FormLabel`, `Radio`)
    "A FormLabel and Radio pair that provides default spacing and links/names them based on id"
    if isinstance(label, str) or label.tag != 'label': 
        label = FormLabel(cls=stringify(lbl_cls), fr=id)(label)
    inp = Radio(id=id, cls=stringify(input_cls), **kwargs)        
    if container: return container(inp, label, cls=stringify(cls))
    return inp, label


# In[ ]:


#| export
def LabelCheckboxX(label:str|FT, # FormLabel content (often text)
               lbl_cls='', # Additional classes for `FormLabel`
               input_cls='', # Additional classes for `CheckboxX`
               container=Div, # Container to wrap label and input in (default is Div)
               cls='flex items-center space-x-2', # Classes on container (default is 'flex items-center space-x-2')
               id='', # id for `FormLabel` and `CheckboxX` (`id`, `name` and `for` attributes are set to this value)
                **kwargs # Additional args for `CheckboxX`
               )->FT:  # Div(cls='flex items-center space-x-2')(`FormLabel`, `CheckboxX`)
    "A FormLabel and CheckboxX pair that provides default spacing and links/names them based on id"
    id = kwargs.pop('id', fh.unqid())
    if isinstance(label, str) or label.tag != 'label': 
        label = FormLabel(cls=stringify(lbl_cls), fr=id)(label)
    inp = CheckboxX(id=id, cls=stringify(input_cls), **kwargs)        
    if container: return container(inp, label, cls=stringify(cls))
    return inp, label


# In[ ]:


#| export
def LabelSelect(*option, # Options for the select dropdown (can use `Options` helper function to create)
               label:str|FT, # FormLabel content (often text)
               lbl_cls='', # Additional classes for `FormLabel`
               input_cls='', # Additional classes for `Select`
               container=Div, # Container to wrap label and input in (default is Div)
               cls='space-y-2', # Classes on container (default is 'space-y-2')
               id='', # id for `FormLabel` and `Select` (`id`, `name` and `for` attributes are set to this value)
                **kwargs # Additional args for `Select`
                ):
    "A FormLabel and Select pair that provides default spacing and links/names them based on id (usually UkLabelSelect is a better choice)"
    if isinstance(label, str) or label.tag != 'label': 
        label = FormLabel(lbl_cls=stringify(lbl_cls), fr=id)(label)
    inp = Select(*option, id=id, cls=stringify(input_cls), **kwargs)        
    if container: return container(label, inp, cls=stringify(cls))
    return label, inp


# In[ ]:


#| export
def Options(*c,                    # Content for an `Option`
            selected_idx:int=None, # Index location of selected `Option`
            disabled_idxs:set=None # Idex locations of disabled `Options`
           ):
    "Helper function to wrap things into `Option`s for use in `Select`"
    return [fh.Option(o,selected=i==selected_idx, disabled=disabled_idxs and i in disabled_idxs) for i,o in enumerate(c)]


# In[ ]:


#| export
def Select(*option,            # Options for the select dropdown (can use `Options` helper function to create)
          inp_cls=(),         # Additional classes for the select input
          cls=('h-10',),      # Classes for the outer div (default h-10 for consistent height)
          cls_custom='button: uk-input-fake dropdown: w-full', # Classes for the Uk_Select web component
          id="",              # ID for the select input
          name="",            # Name attribute for the select input
          placeholder="",     # Placeholder text for the select input
          searchable=False,   # Whether the select should be searchable
          insertable=False,   # Whether to allow user-defined options to be added
          select_kwargs=None, # Additional Arguments passed to Select
           **kwargs           # Additional arguments passed to Uk_select
          ):          
    "Creates a select dropdown with uk styling and option for adding a search box"
    inp_cls, cls, cls_custom= map(stringify, (inp_cls, cls, cls_custom))
    select_kwargs = ifnone(select_kwargs, {})
    uk_select = Uk_select(fh.Select(*option, hidden=True, id=id, name=name, **select_kwargs),
                         cls_custom=cls_custom,
                         searchable=searchable,
                         placeholder=placeholder,
                         insertable=insertable,
                         cls=inp_cls,
                         id=id, 
                         name=name,
                         **kwargs)
    
    return Div(cls=cls)(uk_select)


# In[ ]:


Show(
 Div(cls='h-48')(LabelSelect(
                      Option("Select a verified email to display", value="", selected=True, disabled=True),
                     *[Option(o, value=o) for o in ('m@example.com', 'm@yahoo.com', 'm@cloud.com')],  
                     label="Email", id="email",
 searchable=True)))


# In[ ]:


def LabelSelect(*option,            # Options for the select dropdown (can use `Options` helper function to create) 
             label=(),           # String or FT component for the label
             lbl_cls=(),         # Additional classes for the label
             inp_cls=(),         # Additional classes for the select input
             cls=('space-y-2',), # Classes for the outer div
             id="",              # ID for the select input
             name="",            # Name attribute for the select input
             placeholder="",     # Placeholder text for the select input
             searchable=False,   # Whether the select should be searchable
             select_kwargs=None, # Additional Arguments passed to Select
             **kwargs):          # Additional arguments passed to Select
    "A FormLabel and Select pair that provides default spacing and links/names them based on id"
    lbl_cls, inp_cls, cls = map(stringify, (lbl_cls, inp_cls, cls))
    select_kwargs = ifnone(select_kwargs, {})
    if label:
        lbl = FormLabel(cls=f'{lbl_cls}', fr=id)(label)
    select = Select(*option, inp_cls=inp_cls, id=id, name=name if name else id, 
                   placeholder=placeholder, searchable=searchable, select_kwargs=select_kwargs, **kwargs)
    return Div(cls=cls)(lbl, select) if label else Div(cls=cls)(select)


# In[ ]:


#| export
@delegates(GenericLabelInput, but=['input_fn','cls'])
def LabelRange(label:str|FT, # FormLabel content (often text)
               lbl_cls='', # Additional classes for `FormLabel`
               input_cls='', # Additional classes for `Range`
               cls='space-y-6', # Classes on container (default is `'space-y-2'` to prevent scrunched up form elements)
               id='', # id for `FormLabel` and `Range` (`id`, `name` and `for` attributes are set to this value)
               value='', # Value for the range input
               min=None, # Minimum value
               max=None, # Maximum value
               step=None, # Step size
               label_range=True, # Whether to show the range value label (label for the `Range` component)
               **kwargs # Additional args for `Range`
               )->FT:  # Div(cls='space-y-2')(`FormLabel`, `Range`)
    "A FormLabel and Range pair that provides default spacing and links/names them based on id"
    def range_with_value(**kw): 
        return Div(Range(value=value, min=min, max=max, step=step, label=label_range, **kw))
    return GenericLabelInput(label=label, lbl_cls=lbl_cls, input_cls=input_cls,
                           container=Div, cls=cls, id=id, input_fn=range_with_value, **kwargs)


# In[ ]:


# Show(Div(cls='space-y-6')(
#     LabelRange('Basic Range', value='50', min=0, max=100, step=1),
#     LabelRange('Range with Label', value='75', min=0, max=100, step=5, label_range=True),
#     LabelRange('Multiple Values', value='25,75', min=0, max=100, step=5, label_range=True),
#     LabelRange('Custom Range', value='500', min=0, max=1000, step=100, label_range=True)
# ))


# ## Links

# In[ ]:


#| export
class AT(VEnum):
    'Link styles from https://franken-ui.dev/docs/link'
    def _generate_next_value_(name, start, count, last_values): return str2ukcls('link', name)
    muted = auto()
    text = auto()
    reset = auto()
    primary = 'uk-link text-primary hover:text-primary-focus underline'
    classic = 'text-blue-600 hover:text-blue-800 underline'


# ## Lists

# In[ ]:


#| export
class ListT(VEnum):
    'List styles using Tailwind CSS'
    disc = 'list-disc list-inside'
    circle = 'list-[circle] list-inside' 
    square = 'list-[square] list-inside'
    decimal = 'uk-list uk-list-decimal'
    hyphen = 'uk-list uk-list-hyphen'
    bullet = 'uk-list uk-list-bullet'
    divider = 'uk-list uk-list-divider'
    striped = 'uk-list uk-list-striped'


# ## Modal

# In[ ]:


#| export
def ModalContainer(*c, # Components to put in the modal (often `ModalDialog`)
                     cls=(), # Additional classes on the `ModalContainer`
                     **kwargs # Additional args for `Div` tag
                     )->FT: # Div(..., cls='uk-modal uk-modal-container')
    "Creates a modal container that components go in"
    return fh.Div(*c, cls=('uk-modal uk-modal-container',stringify(cls)), uk_modal=True, **kwargs)
def ModalDialog(*c, # Components to put in the `ModalDialog` (often `ModalBody`, `ModalHeader`, etc)
                  cls=(), # Additional classes on the `ModalDialog`
                  **kwargs # Additional args for `Div` tag
                  )->FT: # Div(..., cls='uk-modal-dialog')
    "Creates a modal dialog"
    return fh.Div(*c, cls=('uk-modal-dialog',   stringify(cls)),                **kwargs)
def ModalHeader(*c, # Components to put in the `ModalHeader`
                  cls=(), # Additional classes on the `ModalHeader`
                  **kwargs # Additional args for `Div` tag
                  )->FT: # Div(..., cls='uk-modal-header')
    "Creates a modal header"
    return fh.Div(*c, cls=('uk-modal-header',   stringify(cls)),                **kwargs)
def ModalBody(*c, # Components to put in the `ModalBody` (often forms, sign in buttons, images, etc.)
               cls=(), # Additional classes on the `ModalBody`
               **kwargs # Additional args for `Div` tag
               )->FT: # Div(..., cls='uk-modal-body')
    "Creates a modal body"
    return fh.Div(*c, cls=('uk-modal-body',     stringify(cls)),                **kwargs)
def ModalFooter(*c, # Components to put in the `ModalFooter` (often buttons)
                 cls=(), # Additional classes on the `ModalFooter`
                 **kwargs # Additional args for `Div` tag
                 )->FT: # Div(..., cls='uk-modal-footer')
    "Creates a modal footer"
    return fh.Div(*c, cls=('uk-modal-footer',   stringify(cls)),                **kwargs)
def ModalTitle(*c, # Components to put in the `ModalTitle` (often text)
                cls=(), # Additional classes on the `ModalTitle`
                **kwargs # Additional args for `H2` tag
                )->FT: # H2(..., cls='uk-modal-title')
    "Creates a modal title"
    return fh.H2(*c,  cls=('uk-modal-title',  stringify(cls)),  **kwargs)
def ModalCloseButton(*c, # Components to put in the button (often text and/or an icon)
                      cls=(), # Additional classes on the button
                      htmx=False, # Whether to use HTMX to close the modal (must add hx_get to a route that closes the modal)
                      **kwargs # Additional args for `Button` tag
                      )->FT: # Button(..., cls='uk-modal-close') + `hx_target` and `hx_swap` if htmx is True
    "Creates a button that closes a modal with js"
    if htmx: kwargs['onclick'] = 'this.closest(".uk-modal").remove()'
    return Button(*c, cls=('uk-modal-close', stringify(cls)), **kwargs)


# In[ ]:


#| export
def Modal(*c,                 # Components to put in the `ModalBody` (often forms, sign in buttons, images, etc.)
        header=None,          # Components that go in the `ModalHeader` (often a `ModalTitle`)
        footer=None,          # Components that go in the `ModalFooter` (often a `ModalCloseButton`)
        cls=(),               # Additional classes on the outermost `ModalContainer` 
        dialog_cls=(),        # Additional classes on the `ModalDialog` 
        header_cls='p-6',     # Additional classes on the `ModalHeader`
        body_cls='space-y-6', # Additional classes on the `ModalBody`
        footer_cls=(),        # Additional classes on the `ModalFooter`
        id='',                # id for the outermost container
        open=False,           # Whether the modal is open (typically used for HTMX controlled modals)
        **kwargs              # Additional args for the outermost `Div` tag
        )->FT: # Fully styled modal FT Component
    "Creates a modal with the appropriate classes to put the boilerplate in the appropriate places for you"
    if open:
        cls = stringify((cls, 'uk-open'))
        kwargs['style'] = stringify((kwargs.get('style',''), 'display: block;'))
    cls, dialog_cls, header_cls, body_cls, footer_cls = map(stringify, (cls, dialog_cls, header_cls, body_cls, footer_cls))
    res = []
    if header: res.append(ModalHeader(cls=header_cls)(header))
    res.append(ModalBody(cls=body_cls)(*c))
    if footer: res.append(ModalFooter(cls=footer_cls)(footer))
    return ModalContainer(ModalDialog(*res, cls=dialog_cls), cls=cls, id=id, **kwargs)


# ## Other

# In[ ]:


#| export
def Placeholder(*c, # Components to put in the placeholder
                  cls=(), # Additional classes on the placeholder
                  **kwargs # Additional args for `Div` tag
                  )->FT: # Div(..., cls='uk-placeholder')
    "Creates a placeholder"
    return fh.Div(*c, cls=('uk-placeholder',stringify(cls)), **kwargs)


# In[ ]:


#| export
def Progress(*c, # Components to put in the progress bar (often nothing)
             cls=(), # Additional classes on the progress bar
             value="", # Value of the progress bar
             max="100", # Max value of the progress bar (defaults to 100 for percentage)
             **kwargs # Additional args for `Progress` tag
             )->FT: # Progress(..., cls='uk-progress')
    "Creates a progress bar"
    return fh.Progress(*c, value=value, max=max, cls=('uk-progress',stringify(cls)), **kwargs)


# ## Icons and Avatars

# In[ ]:


#| export
def UkIcon(icon:str, # Icon name from [lucide icons](https://lucide.dev/icons/)
           height:int=None, 
           width:int=None, 
           stroke_width:int=None, # Thickness of lines
           cls=(), # Additional classes on the `Uk_icon` tag
           **kwargs # Additional args for `Uk_icon` tag
           )->FT: # a lucide icon of the specified size 
    "Creates an icon using lucide icons"
    return Uk_icon(icon=icon, height=height, width=width, stroke_width=stroke_width, cls=cls, **kwargs)


# In[ ]:


#| export
def UkIconLink(icon:str,  # Icon name from [lucide icons](https://lucide.dev/icons/)
           height:int=None, 
           width:int=None, 
           stroke_width:int=None, # Thickness of lines
           cls=(), # Additional classes on the icon
           button:bool=False, # Whether to use a button (defaults to a link)
           **kwargs # Additional args for `A` or `Button` tag
           )->FT: # a lucide icon  button or link of the specified size
    "Creates an icon link using lucide icons"
    fn = fh.Button if button else fh.A
    return fn(cls=(f"uk-icon-{'button' if button else 'link'}", stringify(cls)), **kwargs)(
        UkIcon(icon=icon, height=height, width=width, stroke_width=stroke_width))


# In[ ]:


class IconButtonT(VEnum):
    xs = 'uk-icon-button-xsmall'
    sm = 'uk-icon-button-small'
    outline= 'uk-icon-button-outline'


# In[ ]:


#| export
def DiceBearAvatar(seed_name:str, # Seed name (ie 'Isaac Flath')
                   h:int=20,         # Height 
                   w:int=20,          # Width
                  ):          # Span with Avatar
    "Creates an Avatar using https://dicebear.com/"
    url = 'https://api.dicebear.com/8.x/lorelei/svg?seed='
    return Span(cls=f"relative flex h-{h} w-{w} shrink-0 overflow-hidden rounded-full bg-secondary")(
            fh.Img(cls=f"aspect-square h-{h} w-{w}", alt="Avatar", loading="lazy", src=f"{url}{seed_name}"))


# ## Flexbox | Grid

# The most common pattern for spacing it to organize the general high level page layout with a `Grid`, and smaller components with `Flex`.
# 
# :::{.callout-tip}
# Play [Flex Box Froggy](https://flexboxfroggy.com/) to get an understanding of flex box.
# :::

# In[ ]:


#| export
def Center(*c, # Components to center
          vertical:bool=True, # Whether to center vertically
          horizontal:bool=True, # Whether to center horizontally 
          cls=(), # Additional classes
          **kwargs # Additional args for container div
          )->FT: # Div with centered contents
    "Centers contents both vertically and horizontally by default"
    classes = ['flex']
    if vertical: classes.append('items-center min-h-full') 
    if horizontal: classes.append('justify-center min-w-full')
    return fh_comp.Center(*c, cls=(stringify(classes), stringify(cls)), **kwargs)


# In[ ]:


# Show(Div(
#     H2("All centered (default)"),
#     Div(cls='h-48')(Center(H1("Center()"), cls='bg-secondary')),
#     H2("Only vertically centered"),
#     Div(cls='h-48')(Center(H1("Center(horizontal=False)"), horizontal=False, cls='bg-secondary')),
#     H2("Only horizontally centered"),
#     Div(cls='h-48')(Center(H1("Center(vertical=False)"), vertical=False, cls='bg-secondary')),
#     H2("Not centered"),
#     Div(cls='h-48')(Center(H1("Center(vertical=False, horizontal=False)"), vertical=False, horizontal=False, cls='bg-secondary')),
#     cls='space-y-4'
# ))


# In[ ]:


from fasthtml.jupyter import *
from monsterui.all import *
from functools import partial
app, rt = fast_app(hdrs=Theme.blue.headers())
server = JupyUvi(app, port=8008)


# In[ ]:


Show = partial(HTMX, app=app, port = 8008)


# In[ ]:


#| export
class FlexT(VEnum):
    'Flexbox modifiers using Tailwind CSS'
    def _generate_next_value_(name, start, count, last_values): return name
    
    # Display
    block = 'flex'
    inline = 'inline-flex'
    
    # Horizontal Alignment
    left = 'justify-start' 
    center = 'justify-center'
    right = 'justify-end'
    between = 'justify-between'
    around = 'justify-around'
    
    # Vertical Alignment
    stretch = 'items-stretch'
    top = 'items-start'
    middle = 'items-center' 
    bottom = 'items-end'
    
    # Direction
    row = 'flex-row'
    row_reverse = 'flex-row-reverse'
    column = 'flex-col'
    column_reverse = 'flex-col-reverse'
    
    # Wrap
    nowrap = 'flex-nowrap'
    wrap = 'flex-wrap'
    wrap_reverse = 'flex-wrap-reverse'


# In[ ]:





# In[ ]:


#|export
def Grid(*div, # `Div` components to put in the grid
         cols_min:int=1, # Minimum number of columns at any screen size
         cols_max:int=4, # Maximum number of columns allowed at any screen size
         cols_sm:int=None, # Number of columns on small screens
         cols_md:int=None, # Number of columns on medium screens
         cols_lg:int=None, # Number of columns on large screens
         cols_xl:int=None, # Number of columns on extra large screens
         cols:int=None, # Number of columns on all screens
         cls='gap-4', # Additional classes on the grid (tip: `gap` provides spacing for grids)
         **kwargs # Additional args for `Div` tag
         )->FT: # Responsive grid component
    "Creates a responsive grid layout with smart defaults based on content"
    if cols: cols_min = cols_sm = cols_md = cols_lg = cols_xl = cols
    else:
        n = len(div)
        cols_max = min(n, cols_max)
        cols_sm = cols_sm or min(n, cols_min, cols_max)
        cols_md = cols_md or min(n, cols_min+1, cols_max) 
        cols_lg = cols_lg or min(n, cols_min+2, cols_max) 
        cols_xl = cols_xl or cols_max
    return Div(cls=(f'grid grid-cols-{cols_min} sm:grid-cols-{cols_sm} md:grid-cols-{cols_md} lg:grid-cols-{cols_lg} xl:grid-cols-{cols_xl}', stringify(cls)), **kwargs)(*div)


# In[ ]:


#| export
def DivFullySpaced(*c,                # Components
                   cls='w-full',# Classes for outer div (`w-full` makes it use all available width)
                   **kwargs           # Additional args for outer div
                  ):                  # Div with spaced components via flex classes
    "Creates a flex div with it's components having as much space between them as possible"
    cls = stringify(cls)
    return Div(cls=(FlexT.block,FlexT.between,FlexT.middle,cls), **kwargs)(*c)


# In[ ]:


#| export
def DivCentered(*c,      # Components
                cls='space-y-4',  # Classes for outer div (`space-y-4` provides spacing between components)
                vstack=True, # Whether to stack the components vertically
                **kwargs # Additional args for outer div
               )->FT: # Div with components centered in it
    "Creates a flex div with it's components centered in it"
    cls=stringify(cls)
    return Div(cls=(FlexT.block,(FlexT.column if vstack else FlexT.row),FlexT.middle,FlexT.center,cls),**kwargs)(*c)


# In[ ]:


#| export
def DivLAligned(*c, # Components
                cls='space-x-4',  # Classes for outer div
                **kwargs # Additional args for outer div
               )->FT: # Div with components aligned to the left
    "Creates a flex div with it's components aligned to the left"
    cls=stringify(cls)
    return Div(cls=(FlexT.block,FlexT.left,FlexT.middle,cls), **kwargs)(*c)


# In[ ]:


#| export
def DivRAligned(*c, # Components
                cls='space-x-4',  # Classes for outer div
                **kwargs # Additional args for outer div
               )->FT: # Div with components aligned to the right
    "Creates a flex div with it's components aligned to the right"
    cls=stringify(cls)
    return Div(cls=(FlexT.block,FlexT.right,FlexT.middle,cls), **kwargs)(*c)


# In[ ]:


#| export
def DivVStacked(*c, # Components
                cls='space-y-4', # Additional classes on the div  (tip: `space-y-4` provides spacing between components)
                **kwargs # Additional args for the div
               )->FT: # Div with components stacked vertically
    "Creates a flex div with it's components stacked vertically"
    cls=stringify(cls)
    return Div(cls=(FlexT.block,FlexT.column,FlexT.middle,cls), **kwargs)(*c)


# In[ ]:


#| export
def DivHStacked(*c, # Components
                cls='space-x-4', # Additional classes on the div (`space-x-4` provides spacing between components)
                **kwargs # Additional args for the div
               )->FT: # Div with components stacked horizontally
    "Creates a flex div with it's components stacked horizontally"
    cls=stringify(cls)
    return Div(cls=(FlexT.block,FlexT.row,FlexT.middle,cls), **kwargs)(*c)


# ## Nav

# In[ ]:


#| export
class NavT(VEnum):
    def _generate_next_value_(name, start, count, last_values): return str2ukcls('nav', name)
    default = auto()
    primary = auto()
    secondary = auto()


# In[ ]:


#| export
def NavContainer(*li, # List items are navigation elements (Special `Li` such as `NavParentLi`, `NavDividerLi`, `NavHeaderLi`, `NavSubtitle`, `NavCloseLi` can also be used)
                 cls=NavT.primary, # Additional classes on the nav
                 parent=True, # Whether this nav is a *parent* or *sub* nav
                 uk_nav=False, #True for default collapsible behavior, see [frankenui docs](https://franken-ui.dev/docs/nav#component-options) for more advanced options
                 uk_scrollspy_nav=False, # Activates scrollspy linking each item `A` tags `href` to content's `id` attribute
                 sticky=False, # Whether to stick to the top of the page while scrolling
                 **kwargs # Additional args
                 )->FT: # FT Component that is a list of `Li` styled for a sidebar navigation menu
    "Creates a navigation container (useful for creating a sidebar navigation).  A Nav is a list (NavBar is something different)"
    _uk_scrollspy_nav = False
    if uk_scrollspy_nav:
        if isinstance(uk_scrollspy_nav, bool):  _uk_scrollspy_nav = 'closest: li; scroll: true' if uk_scrollspy_nav else False
        else:  _uk_scrollspy_nav = uk_scrollspy_nav
    _sticky = 'float-left sticky top-4 hidden md:block' if sticky else ''
    return fh.Ul(*li, uk_nav=uk_nav, cls=(f"uk-nav{'' if parent else '-sub'}", stringify(cls), _sticky), uk_scrollspy_nav=_uk_scrollspy_nav, **kwargs)


# In[ ]:


#| export
def NavParentLi(*nav_container, # `NavContainer` container for a nested nav with `parent=False`)
                cls=(), # Additional classes on the li
                **kwargs # Additional args for the li
               )->FT: # Navigation list item
    "Creates a navigation list item with a parent nav for nesting"
    return fh.Li(*nav_container,  cls=('uk-parent',  stringify(cls)),**kwargs)
def NavDividerLi(*c, # Components
                 cls=(), # Additional classes on the li
                 **kwargs # Additional args for the li
                )->FT: # Navigation list item with a divider
    "Creates a navigation list item with a divider"
    return fh.Li(*c, cls=('uk-nav-divider', stringify(cls)),**kwargs)
def NavHeaderLi(*c, # Components
                cls=(), # Additional classes on the li
                **kwargs # Additional args for the li
               )->FT: # Navigation list item with a header
    "Creates a navigation list item with a header"
    return fh.Li(*c, cls=('uk-nav-header', stringify(cls)),**kwargs)
def NavSubtitle(*c, # Components
                 cls=TextPresets.muted_sm, # Additional classes on the div
                 **kwargs # Additional args for the div
                )->FT: # Navigation subtitle
    "Creates a navigation subtitle"
    return fh.Div(*c, cls=('uk-nav-subtitle', stringify(cls)),**kwargs)
def NavCloseLi(*c, # Components
               cls=(), # Additional classes on the li
               **kwargs # Additional args for the li
              )->FT: # Navigation list item with a close button
    "Creates a navigation list item with a close button"
    return fh.Li(*c, cls=('uk-drop-close', stringify(cls)),**kwargs)


# In[ ]:


def NavParentIcon(): return Span(uk_nav_parent_icon=True)


# ## Navbar

# In[ ]:


#| export
class ScrollspyT(VEnum):
    underline = 'navbar-underline'
    bold = 'navbar-bold'


# In[ ]:


#| export
def NavBar(*c, # Component for right side of navbar (Often A tag links)
           brand=H3("Title"), # Brand/logo component for left side
           right_cls='items-center space-x-4', # Spacing for desktop links
           mobile_cls='space-y-4', # Spacing for mobile links
           sticky:bool=False, # Whether to stick to the top of the page while scrolling
           uk_scrollspy_nav:bool|str=False, # Whether to use scrollspy for navigation
           cls='p-4', # Classes for navbar
           scrollspy_cls=ScrollspyT.underline, # Scrollspy class (usually ScrollspyT.*)
           menu_id=None, # ID for menu container (used for mobile toggle)
           )->FT: # Responsive NavBar
    "Creates a responsive navigation bar with mobile menu support"
    if menu_id is None: menu_id = fh.unqid()
    sticky_cls = 'sticky top-4 bg-base-100/80 backdrop-blur-sm z-50' if sticky else ''
    if uk_scrollspy_nav == True: uk_scrollspy_nav = 'closest: a; scroll: true'

    mobile_icon = A(UkIcon("menu", width=30, height=30), cls="md:hidden", data_uk_toggle=f"target: #{menu_id}; cls: hidden")
    return Div(
        Div(
            DivFullySpaced(
                brand, # Brand/logo component for left side
                mobile_icon, # Hamburger menu icon
                Div(*c,cls=(stringify(right_cls),'hidden md:flex'), uk_scrollspy_nav=uk_scrollspy_nav)),# Desktop Navbar (right side)
            cls=('monster-navbar', stringify(cls), stringify(scrollspy_cls))
            ),
        DivCentered(*c, 
                    cls=(stringify(mobile_cls),stringify(cls), stringify(scrollspy_cls),
                         'hidden md:hidden monster-navbar'), 
                    id=menu_id, uk_scrollspy_nav=uk_scrollspy_nav),
        cls=sticky_cls)


# ## Slider

# In[ ]:


#| export
def SliderContainer(
        *c, # Components
        cls='', # Additional classes on the container
        uk_slider=True, # See FrankenUI Slider docs for more options
        **kwargs # Additional args for the container
    ) -> FT: # Div(..., cls='relative', uk_slider=True, ...)
    "Creates a slider container"
    return Div(*c, cls=('relative', stringify(cls)), uk_slider=uk_slider, **kwargs)


# In[ ]:


#| export
def SliderItems(
        *c, # Components
        cls='', # Additional classes for the items
        **kwargs # Additional args for the items
    ) -> FT: # Div(..., cls='uk-slider-items uk-grid', ...)
    "Creates a slider items container"
    return Div(*c, cls=('uk-slider-items uk-grid', stringify(cls)), **kwargs)


# In[ ]:


# Show(SliderContainer(SliderItems(*[Img(src=f'https://picsum.photos/200/200?random={i}', style='width:200px') for i in range(5)])))


# In[ ]:


#| export
def SliderNav(
        cls='uk-position-small uk-hidden-hover', # Additional classes for the navigation
        prev_cls='absolute left-0 top-1/2 -translate-y-1/2', # Additional classes for the previous navigation
        next_cls='absolute right-0 top-1/2 -translate-y-1/2', # Additional classes for the next navigation
        **kwargs # Additional args for the navigation
    ) -> FT: # Left and right navigation arrows for Slider component
    "Navigation arrows for Slider component"
    return (
        fh.A(cls=(prev_cls, stringify(cls)), href='',
             uk_slidenav_previous=True, uk_slider_item='previous', **kwargs),
        fh.A(cls=(next_cls, stringify(cls)), href='',
             uk_slidenav_next=True, uk_slider_item='next', **kwargs)
    )


# In[ ]:


#| export
def Slider(*c, # Items to show in slider
           cls='', # Classes for slider container
           items_cls='gap-4', # Classes for items container
           nav=True, # Whether to show navigation arrows
           nav_cls='', # Classes for navigation arrows
           **kwargs # Additional args for slider container
    ) -> FT: # SliderContainer(SliderItems(..., cls='gap-4'), SliderNav?)
    "Creates a slider with optional navigation arrows"
    nav_comp = SliderNav(cls=nav_cls) if nav else ()
    return SliderContainer(
        SliderItems(*c, cls=items_cls),
        *nav_comp,
        cls=cls,
        **kwargs
    )


# In[ ]:


# Show(Slider(*[Div(Img(src=f'https://picsum.photos/200/200?random={i}'))
#               for i in range(5)]), link=True)


# ## DropDown

# In[ ]:


#| export
def DropDownNavContainer(*li, # Components
                         cls=NavT.primary, # Additional classes on the nav
                         parent=True, # Whether to use a parent nav
                         uk_nav=False, #True for default collapsible behavior, see https://franken-ui.dev/docs/nav#component-options for more advanced options
                         uk_dropdown=True, # Whether to use a dropdown
                         **kwargs # Additional args for the nav
                        )->FT: # DropDown nav container
    "A Nav that is part of a DropDown"
    return Div(cls = 'uk-drop w-full uk-dropdown',uk_dropdown=uk_dropdown)(NavContainer(*li, cls=('uk-dropdown-nav',stringify(cls)), uk_nav=uk_nav, parent=parent, **kwargs))


# ## Tabs

# In[ ]:


#| export
def TabContainer(*li, # Components
                  cls='', # Additional classes on the `Ul`
                  alt=False, # Whether to use an alternative tab style
                  **kwargs # Additional args for the `Ul`
                 )->FT: # Tab container
    "A TabContainer where children will be different tabs"
    cls = stringify(cls)
    return Ul(cls=(f"uk-tab{'-alt' if alt else ''}",stringify(cls)),**kwargs)(*li)


# ## Cards

# In[ ]:


#| export
class CardT(VEnum):
    'Card styles from UIkit'
    def _generate_next_value_(name, start, count, last_values): return str2ukcls('card', name)
    default = auto()
    primary = auto()
    secondary = auto()
    destructive = auto()
    hover = 'uk-card hover:shadow-lg hover:-translate-y-1 transition-all duration-200'


# In[ ]:


#| export
def CardTitle(*c, # Components (often a string)
              cls=(), # Additional classes on the div
              **kwargs # Additional args for the div
             ): 
    "Creates a card title"
    return fh.Div(*c, cls=('uk-card-title',stringify(cls)), **kwargs)

def CardHeader(*c, # Components that goes in the header (often a `ModalTitle` and description)
               cls=(), # Additional classes on the div
               **kwargs # Additional args for the div
              )->FT: # Container for the header of a card
    "Creates a card header"
    return fh.Div(*c, cls=('uk-card-header',stringify(cls)), **kwargs)

def CardBody(*c, # Components that go in the body (Main content of the card such as a form, and image, a signin form, etc.)
              cls=(), # Additional classes on the div
              **kwargs # Additional args for the div
             )->FT: # Container for the body of a card
    "Creates a card body"
    return fh.Div(*c, cls=('uk-card-body',stringify(cls)), **kwargs)

def CardFooter(*c, # Components that go in the footer (often a `ModalCloseButton`)
               cls=(), # Additional classes on the div
               **kwargs # Additional args for the div
              )->FT: # Container for the footer of a card
    "Creates a card footer"
    return fh.Div(*c, cls=('uk-card-footer',stringify(cls)), **kwargs)

def CardContainer(*c, # Components (typically `CardHeader`, `CardBody`, `CardFooter`)
                   cls=CardT.default, # Additional classes on the div
                   **kwargs # Additional args for the div
                  )->FT: # Container for a card
    "Creates a card container"
    return fh.Div(*c, cls=('uk-card',stringify(cls)), **kwargs)


# In[ ]:


#|export
def Card(*c, # Components that go in the body (Main content of the card such as a form, and image, a signin form, etc.)
        header:FT|Iterable[FT]=None, # Component(s) that goes in the header (often a `ModalTitle` and a subtitle)
        footer:FT|Iterable[FT]=None,  # Component(s) that goes in the footer (often a `ModalCloseButton`)
        body_cls='space-y-6', # classes for the body
        header_cls=(), # classes for the header
        footer_cls=(), # classes for the footer
        cls=(), #class for outermost component
        **kwargs # additional arguments for the `CardContainer`
        )->FT: # Card component
    "Creates a Card with a header, body, and footer"
    header_cls, footer_cls, body_cls, cls = map(stringify, (header_cls, footer_cls, body_cls, cls))
    res = []
    if header: res.append(CardHeader(cls=header_cls)(header))
    res.append(CardBody(cls=body_cls)(*c))
    if footer: res.append(CardFooter(cls=footer_cls)(footer))
    return CardContainer(cls=cls, **kwargs)(*res)


# ## Tables

# In[ ]:


#| export
class TableT(VEnum):
    def _generate_next_value_(name, start, count, last_values): return str2ukcls('table', name)
    divider = auto()
    striped = auto()
    hover = auto()
    sm = auto()
    lg = auto()
    justify = auto()
    middle = auto()
    responsive = auto()


# In[ ]:


#| export
def Table(*c, # Components (typically `Thead`, `Tbody`, `Tfoot`)
          cls=(TableT.middle, TableT.divider, TableT.hover, TableT.sm), # Additional classes on the table
          **kwargs # Additional args for the table
         )->FT: # Table component
    "Creates a table"
    return fh.Table(cls=('uk-table', stringify(cls)), *c, **kwargs)


# In[ ]:


#| export
def _TableCell(Component, 
               *c, # Components that go in the cell
               cls=(), # Additional classes on the cell container
               shrink=False, # Whether to shrink the cell
               expand=False, # Whether to expand the cell
               small=False, # Whether to use a small table
               **kwargs # Additional args for the cell
              )->FT: # Table cell
    "Creates a table cell"
    cls = stringify(cls)
    if shrink: cls += ' uk-table-shrink'
    if expand: cls += ' uk-table-expand'
    if small: cls += ' uk-table-small'
    return Component(*c,cls=cls, **kwargs)

@delegates(_TableCell, but=['Component'])
def Td(*c,**kwargs):  return _TableCell(fh.Td, *c, **kwargs)
@delegates(_TableCell, but=['Component'])
def Th(*c,**kwargs): return _TableCell(fh.Th, *c, **kwargs)

def Tbody(*rows, cls=(), sortable=False, **kwargs): return fh.Tbody(*rows, cls=stringify(cls), uk_sortable=sortable, **kwargs)


# In[ ]:


#|export
def TableFromLists(header_data:Sequence, # List of header data
                   body_data:Sequence[Sequence], # List of lists of body data
                   footer_data=None, # List of footer data
                   header_cell_render=Th, # Function(content) -> FT that renders header cells
                   body_cell_render=Td, # Function(key, content) -> FT that renders body cells
                   footer_cell_render=Td, #  Function(key, content) -> FT that renders footer cells
                   cls=(TableT.middle, TableT.divider, TableT.hover, TableT.sm), # Additional classes on the table
                   sortable=False, # Whether to use sortable table
                   **kwargs # Additional args for the table
                  )->FT: # Table from lists
    "Creates a Table from a list of header data and a list of lists of body data"
    return Table(
                Thead(Tr(*map(header_cell_render, header_data))),
                Tbody(*[Tr(*map(body_cell_render, r)) for r in body_data], sortable=sortable),
                Tfoot(Tr(*map(footer_cell_render, footer_data))) if footer_data else '',
                cls=stringify(cls),    
                **kwargs)


# In[ ]:


#| export
def TableFromDicts(header_data:Sequence, # List of header data
                   body_data:Sequence[dict], # List of dicts of body data
                   footer_data=None, # List of footer data
                   header_cell_render=Th, # Function(content) -> FT that renders header cells
                   body_cell_render=lambda k,v : Td(v), # Function(key, content) -> FT that renders body cells
                   footer_cell_render=lambda k,v : Td(v), #  Function(key, content) -> FT that renders footer cells
                   cls=(TableT.middle, TableT.divider, TableT.hover, TableT.sm), # Additional classes on the table
                   sortable=False, # Whether to use sortable table
                   **kwargs # Additional args for the table
                  )->FT: # Styled Table
    "Creates a Table from a list of header data and a list of dicts of body data"
    return Table(
        Thead(Tr(*[header_cell_render(h) for h in header_data])),
        Tbody(*[Tr(*[body_cell_render(k, r.get(k, '')) for k in header_data]) for r in body_data], sortable=sortable),
        Tfoot(Tr(*[footer_cell_render(k, footer_data.get(k.lower(), '')) for k in header_data])) if footer_data else '',
        cls=stringify(cls),    
        **kwargs
    )


# ## Calendar, Date, Time

# In[ ]:


from datetime import datetime

#| export
def CalendarInput(
    cls = "",  # Additional classes
    today: bool = False,  # Automatically sets today as the active date.
    jumpable: bool = False,  # Allow month and year selection
    starts_with: int = 0,  # First day of the week (0 for Sunday, 1 for Monday)
    disabled_dates: str | list[str] = None,  # A comma-separated list of dates to disable (YYYY-MM-DD)
    marked_dates: str | list[str] = None,  # A comma-separated list of dates to add an indicator (YYYY-MM-DD)
    view_date: str = None,  # Sets the initial view date of the calendar (YYYY-MM-DD)
    min_date: str = None,  # Sets the minimum date that can be selected (YYYY-MM-DD)
    max_date: str = None,  # Sets the maximum date that can be selected (YYYY-MM-DD)
    selected_date: str = None,  # Sets the current value of the calendar (YYYY-MM-DD)
    hidden_name: str = None,  # Sets the hidden name input field
    i18n: str = None,  # Enables internationalization
    **kwargs  # Additional arguments
) -> str:
    """Creates a UIkit calendar component."""
    
    # Validation bits for attributes that require YYYY-MM-DD formats
    def _validate_date(date_value):
        """Validates if a given date string follows the YYYY-MM-DD format."""
        if isinstance(date_value, str):
            try:
                datetime.strptime(date_value, "%Y-%m-%d")
                return True
            except ValueError:
                return False
        return False
    
    validation_errors = []
    date_attrs = {
        "view_date": [view_date] if view_date else [],
        "min_date": [min_date] if min_date else [],
        "max_date": [max_date] if max_date else [],
        "disabled_dates": disabled_dates.split(',') if isinstance(disabled_dates, str) else (disabled_dates if disabled_dates else []),
        "marked_dates": marked_dates.split(',') if isinstance(marked_dates, str) else (marked_dates if marked_dates else []),
    }
    
    for attr_name, attr_values in date_attrs.items():
        if attr_values:
            invalid_dates = [date for date in attr_values if date and not _validate_date(date)]
            if invalid_dates:
                validation_errors.append(f"{attr_name} contains invalid dates: {', '.join(invalid_dates)}")
    
    if validation_errors:
        raise ValueError("\n".join(validation_errors))
    
    # Set the tag attributes
    attrs = {
        "today": today,
        "jumpable": jumpable,
        "starts-with": starts_with,
        "disabled-dates": ",".join(date_attrs["disabled_dates"]) if date_attrs["disabled_dates"] else None,
        "marked-dates": ",".join(date_attrs["marked_dates"]) if date_attrs["marked_dates"] else None,
        "view-date": view_date,
        "min": min_date,
        "max": max_date,
        "value": selected_date,
        "name": hidden_name,
        "i18n": i18n,
    }
    
    attrs = {k: v for k, v in attrs.items() if v is not None}
    
    # Return the fastHTML web component
    return fh.ft_html("uk-calendar", cls=stringify(cls), **{**attrs, **kwargs})


# In[ ]:


ci = CalendarInput(
    today=True, 
    jumpable=True, 
    starts_with=1, 
    min_date='2025-02-01', 
    max_date='2025-02-15',
    disabled_dates='2025-02-10,2025-02-05',
    marked_dates='2025-02-10,2025-02-05',
)
ci


# In[ ]:


Show(ci)


# ## Markdown

# In[ ]:


#| export
franken_class_map = {
    'h1': 'uk-h1 text-4xl font-bold mt-12 mb-6',
    'h2': 'uk-h2 text-3xl font-bold mt-10 mb-5', 
    'h3': 'uk-h3 text-2xl font-semibold mt-8 mb-4',
    'h4': 'uk-h4 text-xl font-semibold mt-6 mb-3',
    
    # Body text and links
    'p': 'text-lg leading-relaxed mb-6',
    'a': 'uk-link text-primary hover:text-primary-focus underline',
    
    # Lists with proper spacing
    'ul': 'uk-list uk-list-bullet space-y-2 mb-6 ml-6 text-lg',
    'ol': 'uk-list uk-list-decimal space-y-2 mb-6 ml-6 text-lg',
    'li': 'leading-relaxed',
    
    # Code and quotes
    'pre': 'bg-base-200 rounded-lg p-4 mb-6',
    'code': 'uk-codespan px-1',
    'pre code': 'uk-codespan px-1 block overflow-x-auto',
    'blockquote': 'uk-blockquote pl-4 border-l-4 border-primary italic mb-6',
    
    # Tables
    'table': 'uk-table uk-table-divider uk-table-hover uk-table-small w-full mb-6',
    'th': '!text-left p-2 font-semibold',
    'td': 'p-2',
    
    # Other elements
    'hr': 'uk-divider-icon my-8',
    'img': 'max-w-full h-auto rounded-lg mb-6'
}


# In[ ]:


#| export
def apply_classes(html_str:str, # Html string
                  class_map=None, # Class map
                  class_map_mods=None # Class map that will modify the class map map (useful for small changes to a base class map)
                 )->str: # Html string with classes applied
    "Apply classes to html string"
    if not html_str: return html_str
    try:
        class_map = ifnone(class_map, franken_class_map)
        if class_map_mods: class_map = {**class_map, **class_map_mods}
        html_str = html.fromstring(html_str)
        for selector, classes in class_map.items():
            # Handle descendant selectors (e.g., 'pre code')
            xpath = '//' + '/descendant::'.join(selector.split())
            for element in html_str.xpath(xpath):
                existing_class = element.get('class', '')
                new_class = f"{existing_class} {classes}".strip()
                element.set('class', new_class)
        return etree.tostring(html_str, encoding='unicode', method='html')
    except etree.ParserError:
        return html_str


# In[ ]:


_test = apply_classes("<div><h1>Hello, world!</h1></div>", class_map_mods={'h1': 'uk-h1 my-4 mb-4'})
assert _test == '<div><h1 class="uk-h1 my-4 mb-4">Hello, world!</h1></div>'


# In[ ]:


_test = apply_classes("", class_map_mods={'h1': 'uk-h1 my-4 mb-4'})
assert _test == ''


# In[ ]:


apply_classes(mistletoe.markdown('<!-- why -->'), franken_class_map, None)


# In[ ]:


#| export
def render_md(md_content:str, # Markdown content
               class_map=None, # Class map
               class_map_mods=None # Additional class map
              )->FT: # Rendered markdown
    "Renders markdown using mistletoe and lxml"
    if md_content=='': return md_content
    # Check for required dependencies        
    html_content = mistletoe.markdown(md_content) #, mcp.PygmentsRenderer)
    return NotStr(apply_classes(html_content, class_map, class_map_mods))


# In[ ]:


render_md('''Look here:
- a
- b

```python
a = "aa"
```''')


# In[ ]:


#| export
def get_franken_renderer(img_dir):
    "Create a renderer class with the specified img_dir"
    class FrankenRenderer(HTMLRenderer):
        "Custom renderer for Franken UI that handles image paths"
        def render_image(self, token):
            "Modify image paths if they're relative and img_dir is specified"
            template = '<img src="{}" alt="{}"{} class="max-w-full h-auto rounded-lg mb-6">'
            title = f' title="{token.title}"' if hasattr(token, 'title') else ''
            src = token.src
            if img_dir and not src.startswith(('http://', 'https://', '/')):
                src = f'{Path(img_dir)}/{src}'
            return template.format(src, token.children[0].content if token.children else '', title)
    return FrankenRenderer


# In[ ]:


#| export
def render_md(md_content:str, # Markdown content
             class_map=None, # Class map
             class_map_mods=None, # Additional class map
             img_dir:str=None # Directory containing images
             )->FT: # Rendered markdown
    "Renders markdown using mistletoe and lxml with custom image handling"
    if md_content=='': return md_content
    renderer = get_franken_renderer(img_dir)
    html_content = mistletoe.markdown(md_content, renderer)
    return NotStr(apply_classes(html_content, class_map, class_map_mods))


# In[ ]:


print(render_md('![test](/users/isaac-flath/my_image.png)', img_dir='static'))
print(render_md('![test](my_image.png)', img_dir='static'))
print(render_md('![test](https://example.com/img.png)', img_dir='static'))


# In[ ]:


#| export
def ThemePicker(color=True, radii=True, shadows=True, font=True, mode=True, cls='p-4', custom_themes=[]):
    "Theme picker component with configurable sections"
    def _opt(val, txt, **kwargs): return Option(txt, value=val, **kwargs)
    def _optgrp(key, lbl, opts): return fh.Optgroup(data_key=key, label=lbl)(*opts)
    
    groups = []
    if color: groups.append(_optgrp('theme', 'Theme', [
        _opt('uk-theme-zinc', 'Zinc', data_hex='#52525b', selected=True),
        *[_opt(f'uk-theme-{c.lower()}', c, data_hex=h) for c,h in 
          [('Slate','#64748b'),('Stone','#78716c'),('Gray','#6b7280'),
           ('Neutral','#737373'),('Red','#dc2626'),('Rose','#e11d48'),
           ('Orange','#f97316'),('Green','#16a34a'),('Blue','#2563eb'),
           ('Yellow','#facc15'),('Violet','#7c3aed'),*custom_themes]]]))
    if radii: groups.append(_optgrp('radii', 'Radii', [
        _opt('uk-radii-none','None'), _opt('uk-radii-sm','Small'),
        _opt('uk-radii-md','Medium',selected=True), _opt('uk-radii-lg','Large')]))
    if shadows: groups.append(_optgrp('shadows', 'Shadows', [
        _opt('uk-shadows-none','None'), _opt('uk-shadows-sm','Small',selected=True),
        _opt('uk-shadows-md','Medium'), _opt('uk-shadows-lg','Large')]))
    if font: groups.append(_optgrp('font', 'Font', [
        _opt('uk-font-sm','Small',selected=True), _opt('uk-font-base','Default')]))
    if mode: groups.append(_optgrp('mode', 'Mode', [
        _opt('light','Light',data_icon='sun'), _opt('dark','Dark',data_icon='moon')]))
    from fasthtml.components import Uk_theme_switcher
    return Div(Uk_theme_switcher(fh.Select(*groups, hidden=True),  id="theme-switcher"), cls=stringify(cls))


# In[ ]:


Show(ThemePicker())


# ### Insertable Select

# > Since the `LabelSelect()` component already exists, we will simply add the `insertable=True` param and test it's viability with htmx:

# In[ ]:


@rt
def test_form(email:str):
    return Span('Server Received: ', Output(email), cls="border-b p-2")


# In[ ]:


select = Form(LabelSelect(
                      Option("Select a verified email to display", value="", selected=True, disabled=True),
                     *[Option(o, value=o) for o in ('m@example.com', 'm@yahoo.com', 'm@cloud.com')],  
                     label="Email", id="email", name="email",
 insertable=True), Button('Submit', cls=ButtonT.primary+' uk-btn'), hx_post=test_form, hx_swap="beforeend", cls='grid gap-3 mx-auto mt-4 w-1/2')


# In[ ]:


Show(select, height=350)


# ### Persist client option on submit

# In[ ]:


@rt
def submit_fruit(sess, fruit:str):
    if not fruit: return
    if fruit not in sess['options']: sess['options'].append(fruit.lower())
    return Span('Server Received: ', Output(fruit.capitalize()))

@rt
def refresh(sess, clear:bool):
    if clear: sess.clear()
    return select2(sess)


# > Using `<optgroup>` for option label

# In[ ]:


@rt
def select2(sess):
    if not sess.get('options', ''):
        sess['options'] = ['apple', 'orange', 'banana', 'mango']
    btns = DivHStacked(cls="w-full justify-between")(
               Button('Clear (Persist)', hx_post=refresh.to(sess=sess, clear=False), hx_target="closest form", hx_swap="outerHTML",  cls=ButtonT.default),
                Button('Clear (Refresh)', hx_post=refresh.to(sess=sess, clear=True), hx_target="closest form", hx_swap="outerHTML", cls=ButtonT.default),
                Button('Submit', cls=ButtonT.primary))
    
    return Form(LabelSelect(
                fh.Optgroup(label="Fruit")(
                    *map(lambda l: Option(l.capitalize(), value=l), sorted(sess['options']))
                    ),
                    label="Fruit picker", id="fruit", name="fruit",
                    icon=True, insertable="true", placeholder="Choose a fruit...",
                    cls_custom="button: uk-input-fake justify-between w-full; dropdown: w-full"),
                   btns,hx_post=submit_fruit, hx_swap="beforeend",
               cls='grid gap-2 mx-auto mt-4 w-1/2')


# In[ ]:


Show(select2, height=350)


# ### Light Box

# In[ ]:


#| export
def LightboxContainer(*lightboxitem, # `LightBoxItem`s that will be inside lightbox
                      data_uk_lightbox='counter: true', # See https://franken-ui.dev/docs/2.0/lightbox for advanced options
                      **kwargs # Additional options for outer container
                     )->FT: # Lightbox
    "Lightbox container that will hold `LightboxItems`"
    return fh.Div(*lightboxitem, data_uk_lightbox=data_uk_lightbox, **kwargs)


# In[ ]:


#| export
def LightboxItem(*c, # Component that when clicked will open the lightbox (often a button)
                 href, # Href to image, youtube video, vimeo, google maps, etc.
                 data_alt=None, # Alt text for the lightbox item/image
                 data_caption=None, # Caption for the item that shows below it
                 cls='', # Class for the A tag (often nothing or `uk-btn`)
                 **kwargs # Additional args for the `A` tag
                )->FT: # A(... href, data_alt, cls., ...)
    "Anchor tag with appropriate structure to go inside a `LightBoxContainer`"
    return fh.A(*c, href=href, data_alt=data_alt, cls=stringify(cls), **kwargs)


# In[ ]:


# Show(
#     LightboxContainer(
#         LightboxItem(Button("Open"), href='https://picsum.photos/id/100/1280/720.webp', data_alt='alt text stuff', data_caption='my caption'),
#     ),
#     height=400
# )


# In[ ]:


# Show(
#     LightboxContainer(
#         LightboxItem(Button("Open"), href='https://picsum.photos/id/100/1280/720.webp', data_alt='alt text stuff', data_caption='my caption'),
#         LightboxItem(href='https://picsum.photos/id/101/1280/720.webp', data_alt='alt text stuff', data_caption='my caption'),
#         LightboxItem(href='https://picsum.photos/id/102/1280/720.webp', data_alt='alt text stuff', data_caption='my caption'),
#     ),
#     height=400
# )


# In[ ]:


# Show(
#     LightboxContainer(
#         LightboxItem(Button("Open"), href='https://yootheme.com/site/images/media/yootheme-pro.mp4'),
#         LightboxItem(Button("Open"), href='https://www.youtube.com/watch?v=c2pz2mlSfXA'),
#         LightboxItem(Button("Open"), href='https://vimeo.com/1084537'),
#         LightboxItem(Button("Open"), data_type='iframe', href='https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d4740.819266853735!2d9.99008871708242!3d53.550454675412404!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x3f9d24afe84a0263!2sRathaus!5e0!3m2!1sde!2sde!4v1499675200938')
# ),
#     height=400
# )

