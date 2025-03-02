#!/usr/bin/env python
# coding: utf-8

# ## Daisy UI
# 
# > Helpers and components for DaisyUI style stuff

# In[ ]:


#| default_exp daisy


# In[ ]:


#| export
import fasthtml.common as fh
from monsterui.foundations import *
from fasthtml.common import Div, Span, FT
from fasthtml.svg import *
from enum import auto
from fastcore.all import *


# ## Alerts

# In[ ]:


#| export
class AlertT(VEnum):
    "Alert styles from DaisyUI"
    def _generate_next_value_(name, start, count, last_values): return f"alert-{name}"
    info = auto()
    success = auto()
    warning = auto()
    error = auto()


# In[ ]:


#| export
def Alert(*c, # Content for Alert (often text and/or icon)
          cls='',  # Class for the alert (often an `AlertT` option)
          **kwargs # Additional arguments for outer Div
         )->FT: # Div(Span(...), cls='alert', role='alert')
    "Alert informs users about important events."
    return Div(Span(*c), cls=('alert', stringify(cls)), role='alert', **kwargs)


# The simplest alert is a div wrapped with a span:

# In[ ]:


Alert("Hi")


# Alert colors are defined by the alert styles:

# In[ ]:


Alert("Hi", cls=AlertT.info)


# ## Steps

# In[ ]:


#| export
class StepsT(VEnum):
    "Options for Steps"
    def _generate_next_value_(name, start, count, last_values): return f'steps-{name}'
    vertical = auto()
    horizonal = auto()


# In[ ]:


#| export 
class StepT(VEnum):
    'Step styles for LiStep'
    def _generate_next_value_(name, start, count, last_values): return f'step-{name}'
    primary = auto()
    secondary = auto()
    accent = auto() 
    info = auto()
    success = auto()
    warning = auto()
    error = auto()
    neutral = auto()


# In[ ]:


#| export
def Steps(*li, # Each `Li` represent a step (generally use `LiStep`)
          cls='', # class for Steps (generally a `StepsT` option)
          **kwargs # Additional args for outer wrapper (`Ul` component)
         )->FT: # Ul(..., cls='steps')
    "Creates a steps container"
    return Ul(*li, cls=('steps',stringify(cls)), **kwargs)

def LiStep(*c, # Description for Step that goes next to bubble (often text)
           cls='', # Additional step classes (generally a `StepT` component)
           data_content=None, # Content for inside bubble (defaults to number, often an emoji)
           **kwargs # Aditional arguments for the step (`Li` component)
          )->FT: # Li(..., cls='step')
    "Creates a step list item"
    return Li(*c, cls=('step', stringify(cls)), data_content=data_content, **kwargs)


# To create a list of steps in a process:

# In[ ]:


Steps(
    *[LiStep(o, cls="primary") for o in ("Register", "Choose Plan")],
    *[LiStep(o) for o in ("Purchase", "Receive Product")]
)


# # Loading

# In[ ]:


#| export
class LoadingT(VEnum):
    def _generate_next_value_(name, start, count, last_values): return f'loading-{name}'
    spinner = auto()
    dots = auto()
    ring = auto()
    ball = auto()
    bars = auto()
    infinity = auto()
    
    xs = 'loading-xsmall'
    sm = 'loading-small'
    md = 'loading-medium'
    lg = 'loading-large'


# In[ ]:


#| export
def Loading(cls=(LoadingT.bars, LoadingT.lg), # Classes for indicator (generally `LoadingT` options)
            htmx_indicator=False, # Add htmx-indicator class
            **kwargs # additional args for outer conainter (`Span`)
           )->FT: # Span(cls=...)
    "Creates a loading animation component"
    classes = ['loading', stringify(cls)]
    if htmx_indicator: classes.append('htmx-indicator')
    return Span(cls=classes, **kwargs)


# ## Toasts

# In[ ]:


#| export
class ToastHT(VEnum):
    "Horizontal position for Toast"
    def _generate_next_value_(name, start, count, last_values): return f'toast-{name}'
    start = auto()
    center = auto()
    end = auto()

class ToastVT(VEnum):
    "Vertical position for Toast"
    def _generate_next_value_(name, start, count, last_values): return f'toast-{name}'
    top = auto()
    middle = auto()
    bottom = auto()


# In[ ]:


#| export
def Toast(*c, # Content for toast (often test)
          cls='', # Classes for toast (often `ToastHT` and `ToastVT` options)
          alert_cls='', # classes for altert (often `AlertT` options)
          **kwargs # Additional args for outer container (`Div` tag)
         )->FT: # Div(Alert(...), cls='toast')
    "Toasts are stacked announcements, positioned on the corner of page."
    a = Alert(*c, cls=alert_cls)
    return Div(a, cls=('toast', stringify(cls)), **kwargs)


# To define a toast with a particular location, add horizontal or vertical toast type classes:

# In[ ]:


Toast("New message arrived.", cls=(ToastHT.start, ToastVT.middle))


# To define toast colors, set the class of the alert wrapped by the toast:

# In[ ]:


Toast("New message arrived.", alert_cls=AlertT.info)


# In[ ]:


#| hide
import nbdev; nbdev.nbdev_export()


# In[ ]:




