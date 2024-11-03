"""Utilities for building the docs page that don't belong anywhere else"""


__all__ = ['hjs', 'HShow', 'create_server']

from IPython.display import display, HTML
from fasthtml.common import *
from fh_frankenui.core import *
from fasthtml.jupyter import *


hjs = (Style('html.dark .hljs-copy-button {background-color: #e0e0e0; color: #2d2b57;}'),
                Link(rel='stylesheet', href='https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/styles/atom-one-dark.css', disabled=True),
                Link(rel='stylesheet', href='https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/styles/atom-one-light.css', disabled=True),
                Script(src='https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/highlight.min.js'),
                Script(src='https://cdn.jsdelivr.net/gh/arronhunt/highlightjs-copy/dist/highlightjs-copy.min.js'),
                Link(rel='stylesheet', href='https://cdn.jsdelivr.net/gh/arronhunt/highlightjs-copy/dist/highlightjs-copy.min.css'),
                Style('.hljs-copy-button {background-color: #2d2b57;}'),
                Script(src='https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/languages/python.min.js'),
                Script("hljs.addPlugin(new CopyButtonPlugin());\r\nhljs.configure({'cssSelector': 'pre code'});\r\nhtmx.onLoad(hljs.highlightAll);", type='module'),
                Script('''htmx.on("htmx:beforeHistorySave", () => {document.querySelectorAll("uk-icon").forEach((elt) => {elt.innerHTML = '';});});'''),
                
                Script('''hljs.configure({
                    ignoreUnescapedHTML: true
                });'''),
                Script('''const observer = new MutationObserver(mutations => {
                          mutations.forEach(mutation => {
                            if (mutation.target.tagName === 'HTML' && mutation.attributeName === 'class') {
                              const isDark = mutation.target.classList.contains('dark');
                              document.querySelector('link[href*="atom-one-dark.css"]').disabled = !isDark;
                              document.querySelector('link[href*="atom-one-light.css"]').disabled = isDark;
                            }
                          });
                        });

                        observer.observe(document.documentElement, { attributes: true });

                        // Initial setup
                        const isDark = document.documentElement.classList.contains('dark');
                        document.querySelector('link[href*="atom-one-dark.css"]').disabled = !isDark;
                        document.querySelector('link[href*="atom-one-light.css"]').disabled = isDark;
                        '''))
