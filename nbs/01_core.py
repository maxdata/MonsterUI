from fasthtml.common import *
import fasthtml.common as fh
from monsterui.foundations import *
from fasthtml.common import FastHTML, fast_app
from enum import Enum, auto
from fastcore.all import *
import httpx
from pathlib import Path

from fasthtml.jupyter import *
from functools import partial


@delegates(fh.fast_app, but=['pico'])
def fast_app(*args, pico=False, **kwargs):
    "Create a FastHTML or FastHTMLWithLiveReload app with `bg-background text-foreground` to bodykw for frankenui themes"
    if 'bodykw' not in kwargs: kwargs['bodykw'] = {}
    if 'class' not in kwargs['bodykw']: kwargs['bodykw']['class'] = ''
    kwargs['bodykw']['class'] = stringify((kwargs['bodykw']['class'],'bg-background text-foreground'))
    return fh.fast_app(*args, pico=pico, **kwargs)

@delegates(fh.FastHTML, but=['pico'])
def FastHTML(*args, pico=False, **kwargs):
    "Create a FastHTML app and adds `bg-background text-foreground` to bodykw for frankenui themes"
    if 'bodykw' not in kwargs: kwargs['bodykw'] = {}
    if 'class' not in kwargs['bodykw']: kwargs['bodykw']['class'] = ''
    kwargs['bodykw']['class'] = stringify((kwargs['bodykw']['class'],'bg-background text-foreground'))
    bodykw = kwargs.pop('bodykw',{})
    return fh.FastHTML(*args, pico=pico, **bodykw, **kwargs)


class ThemeRadii(VEnum):
    none = 'uk-radii-none'
    sm = 'uk-radii-sm'
    md = 'uk-radii-md'
    lg = 'uk-radii-lg'

class ThemeShadows:
    none = 'uk-shadows-none'
    sm = 'uk-shadows-sm'
    md = 'uk-shadows-md'
    lg = 'uk-shadows-lg'

class ThemeFont:
    sm = 'uk-font-sm'
    default = 'uk-font-base'

def _headers_theme(color, mode='auto', radii=ThemeRadii.sm, shadows=ThemeShadows.sm, font=ThemeFont.sm):
    franken_init = '''
          const __FRANKEN__ = JSON.parse(localStorage.getItem("__FRANKEN__") || "{}");
    '''
    
    mode_script = {
        'auto': f'''
          {franken_init}
          if (
            __FRANKEN__.mode === "dark" ||
            (!__FRANKEN__.mode &&
              window.matchMedia("(prefers-color-scheme: dark)").matches)
          ) {{
            htmlElement.classList.add("dark");
          }} else {{
            htmlElement.classList.remove("dark");
          }}
        ''',
        'light': f'{franken_init}\nhtmlElement.classList.remove("dark");',
        'dark': f'{franken_init}\nhtmlElement.classList.add("dark");'
    }
    
    return fh.Script(f'''
        const htmlElement = document.documentElement;
        {mode_script[mode]}
          htmlElement.classList.add("uk-theme-{color}");
          htmlElement.classList.add(__FRANKEN__.theme || "uk-theme-{color}");
          htmlElement.classList.add(__FRANKEN__.radii || "{radii}");
          htmlElement.classList.add(__FRANKEN__.shadows || "{shadows}");
          htmlElement.classList.add(__FRANKEN__.font || "{font}");
    ''')

HEADER_URLS = {
        'franken_css': "https://unpkg.com/franken-ui@2.0.0-internal.45/dist/css/core.min.css",
        'franken_js_core': "https://unpkg.com/franken-ui@2.0.0-internal.45/dist/js/core.iife.js",
        'franken_icons': "https://unpkg.com/franken-ui@2.0.0-internal.45/dist/js/icon.iife.js",
        'tailwind': "https://cdn.tailwindcss.com",
        'daisyui': "https://cdn.jsdelivr.net/npm/daisyui@4.12.22/dist/full.min.css",
        'highlight_js': "https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js",
        'highlight_python': "https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/languages/python.min.js",
        'highlight_light_css': "https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/atom-one-light.css",
        'highlight_dark_css': "https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/atom-one-dark.css",
        'highlight_copy': "https://cdn.jsdelivr.net/gh/arronhunt/highlightjs-copy/dist/highlightjs-copy.min.js",
        'highlight_copy_css': "https://cdn.jsdelivr.net/gh/arronhunt/highlightjs-copy/dist/highlightjs-copy.min.css",
}

def _download_resource(url, static_dir):
    "Download a single resource and return its local path"
    static = Path(static_dir)
    fname = static/f"{url[0]}.{'js' if 'js' in url[1] else 'css'}"
    content = httpx.get(url[1], follow_redirects=True).content
    fname.write_bytes(content)
    return (url[0], f"/{static_dir}/{fname.name}")

daisy_styles = Style("""
:root {
  --b1: from hsl(var(--background)) l c h;
  --bc: from hsl(var(--foreground)) l c h;
  --m: from hsl(var(--muted)) l c h;
  --mc: from hsl(var(--muted-foreground)) l c h;
  --po: from hsl(var(--popover)) l c h;
  --poc: from hsl(var(--popover-foreground)) l c h;
  --b2: from hsl(var(--card)) l c h;
  --b2c: from hsl(var(--card-foreground)) l c h;
  --br: from hsl(var(--border)) l c h;
  --in: from hsl(var(--input)) l c h;
  --p: from hsl(var(--primary)) l c h;
  --pc: from hsl(var(--primary-foreground)) l c h;
  --s: from hsl(var(--secondary)) l c h;
  --sc: from hsl(var(--secondary-foreground)) l c h;
  --a: from hsl(var(--accent)) l c h;
  --ac: from hsl(var(--accent-foreground)) l c h;
  --er: from hsl(var(--destructive)) l c h;
  --erc: from hsl(var(--destructive-foreground)) l c h;
  --b3: from hsl(var(--ring)) l c h;
  --ch1: from hsl(var(--chart-1)) l c h;
  --ch2: from hsl(var(--chart-2)) l c h;
  --ch3: from hsl(var(--chart-3)) l c h;
  --ch4: from hsl(var(--chart-4)) l c h;
  --ch5: from hsl(var(--chart-5)) l c h;
  --rd: var(--radius);
}
""")

scrollspy_style= Style('''
.monster-navbar.navbar-bold a {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.monster-navbar.navbar-bold a.uk-active {
    transform: scale(1.15) ;
    font-weight: bold;
    text-shadow: 0 0 12px rgba(var(--p-rgb), 0.4);
    letter-spacing: 0.02em;
    color: hsl(var(--p) / 1);
}
.monster-navbar.navbar-underline a.uk-active { position: relative; }
.monster-navbar.navbar-underline a.uk-active::after {
    content: '';
    position: absolute;
    left: 0;
    bottom: -2px;
    width: 100%;
    height: 2px;
    background: currentColor;
    animation: slideIn 0.3s ease forwards;
}
@keyframes slideIn {
    from { transform: scaleX(0); }
    to { transform: scaleX(1); }
}
''')

#| export
class Theme(Enum):
    "Selector to choose theme and get all headers needed for app.  Includes frankenui + tailwind + daisyui + highlight.js options"
    def _generate_next_value_(name, start, count, last_values): return name
    slate = auto()
    stone = auto()
    gray = auto()
    neutral = auto()
    red = auto()
    rose = auto()
    orange = auto()
    green = auto()
    blue = auto()
    yellow = auto()
    violet = auto()
    zinc = auto()

    def _create_headers(self, urls, mode='auto', daisy=True, highlightjs=False, katex=True, radii=ThemeRadii.sm, shadows=ThemeShadows.sm, font=ThemeFont.sm):
        "Create header elements with given URLs"
        hdrs = [
            fh.Link(rel="stylesheet", href=urls['franken_css']),
            fh.Script(type="module", src=urls['franken_js_core']),
            fh.Script(type="module", src=urls['franken_icons']),
            fh.Script(src=urls['tailwind']),
            fh.Script("""
    tailwind.config = {
        darkMode: 'selector',
    }
    """),
            _headers_theme(self.value, mode=mode, radii=radii, shadows=shadows, font=font),
            scrollspy_style]

        if daisy:
            hdrs += [fh.Link(rel="stylesheet", href=urls['daisyui']), daisy_styles]
            
        if highlightjs:
            hdrs += [
                fh.Script(src=urls['highlight_js']),
                fh.Script(src=urls['highlight_python']),
                fh.Link(rel="stylesheet", href=urls['highlight_light_css'], id='hljs-light'),
                fh.Link(rel="stylesheet", href=urls['highlight_dark_css'], id='hljs-dark'),
                fh.Script(src=urls['highlight_copy']),
                fh.Link(rel="stylesheet", href=urls['highlight_copy_css']),
                fh.Script('''
                    hljs.addPlugin(new CopyButtonPlugin());
                    hljs.configure({
                        cssSelector: 'pre code',
                        languages: ['python'],
                        ignoreUnescapedHTML: true
                    });
                    function updateTheme() {
                        const isDark = document.documentElement.classList.contains('dark');
                        document.getElementById('hljs-dark').disabled = !isDark;
                        document.getElementById('hljs-light').disabled = isDark;
                    }
                    new MutationObserver(mutations =>
                        mutations.forEach(m => m.target.tagName === 'HTML' &&
                            m.attributeName === 'class' && updateTheme())
                    ).observe(document.documentElement, { attributes: true });
                    updateTheme();
                    htmx.onLoad(hljs.highlightAll);
                ''', type='module'),
            ]

        if katex:
            hdrs += [
                fh.Link(rel="stylesheet",
                        href="https://cdn.jsdelivr.net/npm/katex@0.16.21/dist/katex.min.css"),
                fh.Script("""
                import katex from 'https://cdn.jsdelivr.net/npm/katex@0.16.21/dist/katex.mjs';
                import autoRender from 'https://cdn.jsdelivr.net/npm/katex@0.16.21/dist/contrib/auto-render.mjs';
                const options = {
                  delimiters: [
                    {left: '$$', right: '$$', display: true},
                    {left: '$', right: '$', display: false}
                  ],
                  ignoredClasses: ['nomath']
                };

                document.addEventListener('htmx:load', evt => {
                  const element = evt.detail.elt || document.body;
                  autoRender(element,options);
                });
                """,type="module"),
                ]
        return hdrs

    def headers(self, mode='auto', daisy=True, highlightjs=False, katex=True, radii=ThemeRadii.sm, shadows=ThemeShadows.sm, font=ThemeFont.sm ):
        "Create frankenui and tailwind cdns"
        return self._create_headers(HEADER_URLS, mode=mode, daisy=daisy, highlightjs=highlightjs, katex=katex, radii=radii, shadows=shadows, font=font)    
    
    def local_headers(self, mode='auto', static_dir='static', daisy=True, highlightjs=False, katex=True, radii='md', shadows='sm', font='sm'):
        "Create headers using local files downloaded from CDNs"
        Path(static_dir).mkdir(exist_ok=True)
        local_urls = dict([_download_resource(url, static_dir) for url in HEADER_URLS.items()])
        return self._create_headers(local_urls, mode=mode, daisy=daisy, highlightjs=highlightjs, katex=katex, radii=radii, shadows=shadows, font=font)

serve()


