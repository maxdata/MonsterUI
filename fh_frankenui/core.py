"""The building blocks to the UI"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../lib_nbs/00_core.ipynb.

# %% auto 0
__all__ = ['UkInput', 'UkSwitch', 'UkTextArea', 'UkFormLabel', 'UkH1', 'UkH2', 'UkH3', 'UkH4', 'UkH5', 'UkH6', 'stringify',
           'VEnum', 'Theme', 'TextB', 'TextT', 'UkIcon', 'DiceBearAvatar', 'Grid', 'ResponsiveGrid', 'FullySpacedDiv',
           'CenteredDiv', 'LAlignedDiv', 'RAlignedDiv', 'VStackedDiv', 'HStackedDiv', 'UkGenericInput', 'Options',
           'UkSelect', 'UkButtonT', 'process_options', 'UkDropdownButton', 'UkButton', 'UkGenericComponent', 'UkHSplit',
           'UkHLine', 'UkNavDivider', 'UkNavbarDropdown', 'UkNavbar', 'NavTab', 'UkTab', 'UkSidebarItem', 'UkSidebarUl',
           'UkSidebarSection', 'UkSidebar', 'Card', 'UkModalTitle', 'Modal', 'default_header', 'default_cell',
           'header_row', 'data_row', 'UkTable', 'UkFormSection']

# %% ../lib_nbs/00_core.ipynb
from fasthtml.common import *
from fasthtml.svg import Svg
from enum import Enum, EnumType
from fasthtml.components import Uk_select,Uk_input_tag
from functools import partial
from itertools import zip_longest
from typing import Union, Tuple, Optional
from fastcore.all import L

# %% ../lib_nbs/00_core.ipynb
# need a better name, stringify might be too general for what it does 
def stringify(o # String, Tuple, or Enum options we want stringified
             ): # String that can be passed FT comp args (such as `cls=`)
    "Converts input types into strings that can be passed to FT components"  
    if is_listy(o): return ' '.join(map(str,o)) if o else ""
    return o.__str__()

# %% ../lib_nbs/00_core.ipynb
class VEnum(Enum):
    def __add__(self, other):
        "Add other enums, listy, or strings"
        return stringify((self, other))

    def __radd__(self, other):
        "Add other enums, listy, or strings"
        return stringify((other, self))
    
    def __str__(self):
        "Stringifies with uk-{attr}-{value} format"
        base = self.__class__.__name__       
        if isinstance(self.__class__, EnumType):
            base = base.lstrip('Uk').rstrip('T')
        return f"uk-{base.lower()}-{self.value}".strip('-')

# %% ../lib_nbs/00_core.ipynb
class Theme(Enum):
    slate = "slate"
    stone = "stone"
    gray = "gray"
    neutral = "neutral"
    red = "red"
    rose = "rose"
    orange = "orange"
    green = "green"
    blue = "blue"
    yellow = "yellow"
    violet = "violet"
    zinc = "zinc"

    def headers(self):
        js = (Script(src="https://cdn.tailwindcss.com"),
              Script(src="https://cdn.jsdelivr.net/npm/uikit@3.21.6/dist/js/uikit.min.js"),
              Script(src="https://cdn.jsdelivr.net/npm/uikit@3.21.6/dist/js/uikit-icons.min.js"),
              Script(type="module", src="https://unpkg.com/franken-wc@0.0.6/dist/js/wc.iife.js")
              )
        _url = f"https://unpkg.com/franken-wc@0.0.6/dist/css/{self.value}.min.css"
        return (*js, Link(rel="stylesheet", href=_url))

# %% ../lib_nbs/00_core.ipynb
class TextB(Enum):
    sz_xsmall = 'text-xs'
    sz_small = 'text-sm'
    sz_medium = 'text-base'
    sz_large = 'text-lg'
    cl_muted = 'uk-text-muted'
    
    wt_light = 'font-light'
    wt_normal = 'font-normal'
    wt_medium = 'font-medium'
    wt_bold = 'font-bold'
# font-thin	font-weight: 100;
# font-extralight	font-weight: 200;
# font-light	font-weight: 300;
# font-normal	font-weight: 400;
# 
# font-semibold	font-weight: 600;
# font-bold	font-weight: 700;
# font-extrabold	font-weight: 800;
# font-black    
    
    
# font-medium text-sm
    def __str__(self):
        return self.value

# %% ../lib_nbs/00_core.ipynb
class TextT(Enum):
    muted_xs = TextB.sz_xsmall, TextB.cl_muted 
    muted_sm = TextB.sz_small, TextB.cl_muted # Text below card headings
    muted_med = TextB.sz_medium, TextB.cl_muted 
    muted_lg = TextB.sz_large, TextB.cl_muted 
    medium_sm = TextB.sz_small, TextB.wt_medium
    medium_xs = TextB.sz_xsmall, TextB.wt_medium

    def __str__(self):
        if is_listy(self.value): return ' '.join(map(str,self.value))
        return self.value

# %% ../lib_nbs/00_core.ipynb
def UkIcon(icon, ratio=1,cls=()):
    return Span(uk_icon=f"icon: {icon}; ratio: {ratio}",cls='z-[-1] '+stringify(cls))

# %% ../lib_nbs/00_core.ipynb
def DiceBearAvatar(seed_name, h, w):
    url = 'https://api.dicebear.com/8.x/lorelei/svg?seed='
    return Span(cls=f"relative flex h-{h} w-{w} shrink-0 overflow-hidden rounded-full bg-accent")(
            Img(cls="aspect-square h-full w-full", alt="Avatar", src=f"{url}{seed_name}"))

# %% ../lib_nbs/00_core.ipynb
def Grid(*c, cols=3, gap=2, cls=(), **kwargs):
    cls = stringify(cls)
    return Div(cls=f'grid grid-cols-{cols} gap-{gap} '+cls, **kwargs)(*c)

# %% ../lib_nbs/00_core.ipynb
def ResponsiveGrid(*c, sm=1, md=2, lg=3, xl=4, gap=2, cls='', **kwargs):
    return Div(cls=f'grid grid-cols-{sm} md:grid-cols-{md} lg:grid-cols-{lg} xl:grid-cols-{xl} gap-{gap} ' + stringify(cls), **kwargs)(*c)

# %% ../lib_nbs/00_core.ipynb
def FullySpacedDiv(*c,wrap_tag=None, cls='', **kwargs):
    wrap_fn = ifnone(wrap_tag, noop)
    cls = stringify(cls)
    return Div(cls='uk-flex uk-flex-between uk-flex-middle uk-width-1-1 '+cls, **kwargs)(*(map(wrap_fn,c)))

# %% ../lib_nbs/00_core.ipynb
def CenteredDiv(*c,cls=(), **kwargs):
    cls=stringify(cls)
    return Div(cls='flex flex-col items-center justify-center '+cls,**kwargs)(*c)

# %% ../lib_nbs/00_core.ipynb
def LAlignedDiv(*c, gap=2, cls='', **kwargs):
    cls=stringify(cls)
    return Div(cls=f'flex items-center space-x-{gap} '+stringify(cls), **kwargs)(*c)

# %% ../lib_nbs/00_core.ipynb
def RAlignedDiv(*c, gap=2, cls='', **kwargs):
    cls=stringify(cls)
    return Div(cls=f'flex items-center justify-end space-x-{gap} '+stringify(cls), **kwargs)(*c)

# %% ../lib_nbs/00_core.ipynb
def VStackedDiv(*c, gap=2, cls='', **kwargs):
    cls=stringify(cls)
    return Div(cls=f'flex flex-col space-y-{gap} ' + stringify(cls), **kwargs)(*c)

# %% ../lib_nbs/00_core.ipynb
def HStackedDiv(*c, gap=2, cls='', **kwargs):
    cls=stringify(cls)
    return Div(cls=f'flex flex-row space-x-{gap} ' + stringify(cls), **kwargs)(*c)

# %% ../lib_nbs/00_core.ipynb
def UkGenericInput(input_fn: FT, # FT Components that generates a user input (e.g. `TextArea`)
                    label:str|FT=(), # String or FT component that goes in `Label`
                    lbl_cls:str|Enum=(), # Additional classes that goes in `Label`
                    inp_cls:str|Enum=(), # Additional classes that go in user input (e.g. `TextArea`)
                    cls:str|Enum=('space-y-2',), # Div cls
#                     id: str="", # ID of the user input (e.g. `TextArea`)
                   **kwargs # Passed to `input_fn` (e.g. ` TextArea`)
                  ) -> FT: # FT component in structure `(Div(label,input))`
    "`Div(Label,Input)` component with Uk styling injected appropriately. Generally you should higher level API, such as `UKTextArea` which is created for you in this library"
    lbl_cls, inp_cls, cls = map(stringify,(lbl_cls, inp_cls, cls))
    if label:  label = Label(cls='uk-form-label '+lbl_cls)(label)
    if label and id: label.attrs['for'] = id
    res = input_fn(**kwargs)
    if inp_cls: res.attrs['class'] += inp_cls
    return Div(cls=cls)(label, res)

# %% ../lib_nbs/00_core.ipynb
UkInput =     partial(UkGenericInput, partial(Input, cls='uk-input'))
UkSwitch =    partial(UkGenericInput, partial(CheckboxX,    cls='uk-toggle-switch uk-toggle-switch-primary')) 
UkTextArea =  partial(UkGenericInput, partial(Textarea,     cls='uk-textarea'))
UkFormLabel = partial(UkGenericInput, partial(Uk_input_tag, cls='uk-form-label'))


# %% ../lib_nbs/00_core.ipynb
def Options(*c, # Content for an `Option`
            selected_idx:int=None, # Index location of selected `Option`
            disabled_idxs:set=None
           ):
    "Generates list of `Option`s with the proper `selected_idx`"
    return [Option(o,selected=i==selected_idx, disabled=disabled_idxs and i in disabled_idxs) for i,o in enumerate(c)]

# %% ../lib_nbs/00_core.ipynb
def UkSelect(*options,
             label=(),
             lbl_cls=(),
             inp_cls=(),
             cls=('space-y-2',),
             id="",
             name="",
             placeholder="",
             searchable=False,
             **kwargs):
    lbl_cls, inp_cls, cls = map(stringify, (lbl_cls, inp_cls, cls))
    if label:
        lbl = Label(cls=f'uk-form-label {lbl_cls}', fr=id)(label) if id else Label(cls=f'uk-form-label {lbl_cls}')(label)
    select = Uk_select(cls=inp_cls, uk_cloak=True, id=id, name=name, placeholder=placeholder, searchable=searchable, **kwargs)
    select = select(*options)
    return Div(cls=cls)(lbl, select) if label else Div(cls=cls)(select)

# %% ../lib_nbs/00_core.ipynb
class UkButtonT(VEnum):
    default = 'default'
    primary = 'primary'
    secondary = 'secondary'
    danger = 'danger'
    ghost = 'ghost'
    text = 'text'
    link = 'link'

# %% ../lib_nbs/00_core.ipynb
def process_options(opts, hdrs):
    for i, (opt, hdr) in enumerate(zip_longest(opts, hdrs or [])):
        if hdr and len(hdr) > 0: yield Li(cls="uk-nav-header")(hdr if isinstance(hdr, FT) else Div(hdr))
        if isinstance(opt, (list, tuple)): yield from list(map(Li, opt))
        else: yield Li(opt)
        if i < len(opts) - 1:
            next_hdr = hdrs[i+1] if hdrs and i+1 < len(hdrs) else None
            if not next_hdr or len(next_hdr) == 0: yield Li(cls='uk-nav-divider')

def UkDropdownButton(
    options,        # List of options to be displayed in the dropdown
    option_hdrs=None,  # List of headers for each option group, or None
    label=None,     # String, FT component, or None for the `Button`
    btn_cls=UkButtonT.default,  # Button class(es)
    cls=(),         # Parent div class
    dd_cls=(),      # Class that goes on the dropdown container
    icon='triangle-down',  # Icon to use for the dropdown
    icon_cls='',    # Additional classes for the icon
    icon_position='right'  # Position of the icon: 'left' or 'right'
    ):
    dd_cls, btn_cls, cls, icon_cls = map(stringify, (dd_cls, btn_cls, cls, icon_cls))
    icon_component = UkIcon(icon, cls=icon_cls) if icon else None
    btn_content = [] if label is None else [label]
    if icon_component: btn_content.insert(0 if icon_position == 'left' else len(btn_content), icon_component)
    btn = Button(type='button', cls='uk-button ' + btn_cls)(*btn_content)
    dd = Div(uk_drop='mode: click; pos: bottom-right', cls='uk-dropdown uk-drop ' + dd_cls)(
        Ul(cls='uk-dropdown-nav')(*process_options(options, option_hdrs))
    )
    return Div(cls=cls)(Div(cls='flex items-center space-x-4')(btn, dd))

# %% ../lib_nbs/00_core.ipynb
def UkButton(*c, 
            cls=UkButtonT.default, # Use UkButtonT or styles 
            **kwargs):    
    return Button(type='button', cls='uk-button ' + stringify(cls), **kwargs)(*c)

# %% ../lib_nbs/00_core.ipynb
def UkGenericComponent(component_fn, *c, cls=(), **kwargs):
    res = component_fn(**kwargs)(*c)
    if cls: res.attrs['class'] += ' ' + cls
    return res

UkH1 = partial(UkGenericComponent, partial(H1,cls='uk-h1'))
UkH2 = partial(UkGenericComponent, partial(H2,cls='uk-h2'))
UkH3 = partial(UkGenericComponent, partial(H3,cls='uk-h3'))
UkH4 = partial(UkGenericComponent, partial(H4,cls='uk-h4'))
UkH5 = partial(UkGenericComponent, partial(H5,cls='uk-h5'))
UkH6 = partial(UkGenericComponent, partial(H6,cls='uk-h6'))


# %% ../lib_nbs/00_core.ipynb
def UkHSplit(*c, cls=(), line_cls=(), text_cls=()):
    cls, line_cls, text_cls = map(stringify,(cls, line_cls, text_cls))
    return Div(cls='relative ' + cls)(
        Div(cls="absolute inset-0 flex items-center " + line_cls)(Span(cls="w-full border-t border-border")),
        Div(cls="relative flex justify-center " + text_cls)(Span(cls="bg-background px-2 ")(*c)))

def UkHLine(lwidth=2, y_space=4): return Div(cls=f"my-{y_space} h-[{lwidth}px] w-full bg-secondary")

# %% ../lib_nbs/00_core.ipynb
def UkNavDivider(): return Li(cls="uk-nav-divider")

# %% ../lib_nbs/00_core.ipynb
def UkNavbarDropdown(*c, label, href='#', cls='', has_header=False, **kwargs):
    fn = lambda x: Li(item, cls='uk-drop-close', href='#demo', uk_toggle=True)
    flattened = []
    for i, item in enumerate(c):
        if i > 0: flattened.append(Li(cls="uk-nav-divider"))
        if isinstance(item, (list,tuple)): flattened.extend(map(Li, item))
        else: flattened.append(Li(item, cls="uk-nav-header" if i == 0 and has_header else None, uk_toggle=True))
    return (Li(cls=cls, **kwargs)(
                A(label, cls='uk-drop-close', href='#', uk_toggle=True), 
                Div(cls='uk-navbar-dropdown', uk_dropdown="mode: click; pos: bottom-left")(Ul(cls='uk-nav uk-dropdown-nav')(*flattened))))

# %% ../lib_nbs/00_core.ipynb
def _NavBarSide(n, s):
    def add_class(item):
        if isinstance(item, str): return Li(cls='uk-navbar-item')(item)
        else: item.attrs['class'] = f"{item.attrs.get('class', '')} uk-navbar-item".strip()
        return item
    return Div(cls=f'uk-navbar-{s}')(Ul(cls='uk-navbar-nav')(*map(add_class, tuplify(n))))

# %% ../lib_nbs/00_core.ipynb
def UkNavbar(lnav: Sequence[Union[str, FT]]=None, 
             rnav: Sequence[Union[str, FT]]=None, 
             cls='') -> FT:
    return Div(cls='uk-navbar-container uk-width-1-1 relative'+ stringify(cls), uk_navbar=True)(
             _NavBarSide(lnav,'left') if lnav else '',
             _NavBarSide(rnav,'right') if rnav else '')

# %% ../lib_nbs/00_core.ipynb
def NavTab(text, active=False):
    return Li(cls="uk-active" if active else " ")(A(text, href="#demo", uk_toggle=True))

def UkTab(*items):
    return Ul(cls="uk-tab-alt max-w-96")(*[NavTab(item, active=i==0) for i, item in enumerate(items)])

# %% ../lib_nbs/00_core.ipynb
def UkSidebarItem(item, is_header=False): return UkH4(item) if is_header else A(role='button')(item)

def UkSidebarUl(*lis, cls='', **kwargs): 
    return Ul(cls=f"uk-nav uk-nav-secondary space-y-2 {cls}", **kwargs)(*map(Li,lis))

def UkSidebarSection(items, header=None, cls='', **kwargs):
    section = [UkSidebarItem(item) for item in items]
    if header: section.insert(0, UkSidebarItem(header, is_header=True))
    return UkSidebarUl(*section, cls=cls, **kwargs)

def UkSidebar(sections, headers=None, outer_margin=4, inner_margin=4, cls=(), **kwargs):
    headers = headers or [None] * len(sections)
    sidebar_content = map(lambda s_h: UkSidebarSection(*s_h, **kwargs), zip(sections, headers))
    return Div(cls=f"space-y-{inner_margin} p-{outer_margin} {cls}")(*sidebar_content)

# %% ../lib_nbs/00_core.ipynb
def Card(*c, # Components that go in the body
        header=None, # Components that go in the header
        footer=None,  # Components that go in the footer
        body_cls='space-y-6', # classes for the body
        header_cls=(), # classes for the header
        footer_cls=(), # classes for the footer
        cls=(), #class for outermost component
        **kwargs # classes that for the card itself
        ):
    header_cls, footer_cls, body_cls, cls = map(stringify, (header_cls, footer_cls, body_cls, cls))
    res = []
    if header: res += [Div(cls='uk-card-header ' + header_cls)(header),]
    res += [Div(cls='uk-card-body ' + body_cls)(*c),]
    if footer: res += [Div(cls='uk-card-footer ' + footer_cls)(footer),]
    return Div(cls='uk-card '+cls, **kwargs)(*res)

# %% ../lib_nbs/00_core.ipynb
def UkModalTitle(*c, cls=()): return Div(cls='uk-modal-title ' + stringify(cls))(*c)

def Modal(*c,
        header=None, # Components that go in the header
        footer=None,  # Components that go in the footer
        body_cls='space-y-6', # classes for the body
        header_cls='p-6', # classes for the header
        footer_cls=(), # classes for the footer
        cls=(), #class for outermost component
        **kwargs # classes that for the card itself
        ):
    header_cls, footer_cls, body_cls, cls = map(stringify, (header_cls, footer_cls, body_cls, cls))
    res = []
    if header: res += [Div(cls='uk-modal-header ' + header_cls)(header),]
    res += [Div(cls='uk-modal-body uk-modal-dialog ' + body_cls)(*c),]
    if footer: res += [Div(cls='uk-modal-footer ' + footer_cls)(footer),]
    return Div(cls='uk-modal uk-modal-container' + cls, uk_modal=True, **kwargs)(*res)


# %% ../lib_nbs/00_core.ipynb
def default_header(col): return Th(cls='p-2')(col)
def default_cell(col, row): return Td(row[col], cls='p-2')

def header_row(columns, header_render):
    rndr = header_render or default_header
    return Tr(*map(rndr, columns))

def data_row(row, columns, cell_render):
    rndr = cell_render or default_cell
    return Tr(*[rndr(col, row) for col in columns])

def UkTable(columns, data, *args, cls=(), footer=None, cell_render=None, header_render=None, **kwargs):
    table_cls = 'uk-table uk-table-middle uk-table-divider uk-table-hover uk-table-small ' + stringify(cls)
    table_content = [
        Thead(header_row(columns, header_render)),
        Tbody(*map(lambda d: data_row(d, columns, cell_render), data))
    ]
    if footer: table_content.append(Tfoot(footer))
    return Table(cls=table_cls, *args, **kwargs)(*table_content)

# %% ../lib_nbs/00_core.ipynb
def UkFormSection(title, description, *c, button_txt='Update', outer_margin=6, inner_margin=6):
    return Div(cls=f'space-y-{inner_margin} py-{outer_margin}')(
        Div(UkH3(title), P(description, cls=TextT.medium_sm)),
        UkHSplit(), *c,
        Div(UkButton(button_txt, cls=UkButtonT.primary)) if button_txt else None
    )
