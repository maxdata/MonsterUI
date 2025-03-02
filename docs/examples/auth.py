"""FrankenUI Auth Example built with MonsterUI (original design by ShadCN)"""

from fasthtml.common import *
from monsterui.all import *
from fasthtml.svg import *

app, rt = fast_app(hdrs=Theme.blue.headers())

@rt
def index():    
    left = Div(cls="col-span-1 hidden flex-col justify-between bg-zinc-900 p-8 text-white lg:flex")(
        Div(cls=(TextT.bold))("Acme Inc"),
        Blockquote(cls="space-y-2")(
            P(cls=TextT.lg)('"This library has saved me countless hours of work and helped me deliver stunning designs to my clients faster than ever before."'),
            Footer(cls=TextT.sm)("Sofia Davis")))

    right = Div(cls="col-span-2 flex flex-col p-8 lg:col-span-1")(
        DivRAligned(Button("Login", cls=ButtonT.ghost)),
        DivCentered(cls='flex-1')(
            Container(
                DivVStacked(
                    H3("Create an account"),
                    Small("Enter your email below to create your account", cls=TextT.muted)),
                Form(
                    Input(placeholder="name@example.com"),
                    Button(Span(cls="mr-2", uk_spinner="ratio: 0.54"), "Sign in with Email", cls=(ButtonT.primary, "w-full"), disabled=True),
                    DividerSplit(Small("Or continue with"),cls=TextT.muted),
                    Button(UkIcon('github',cls='mr-2'), "Github", cls=(ButtonT.default, "w-full")),
                    cls='space-y-6'),
                DivVStacked(Small(
                        "By clicking continue, you agree to our ",
                        A(cls=AT.muted, href="#demo")("Terms of Service")," and ",
                        A(cls=AT.muted, href="#demo")("Privacy Policy"),".",
                        cls=(TextT.muted,"text-center"))),
                cls="space-y-6")))
    
    return Title("Auth Example"),Grid(left,right,cols=2, gap=0,cls='h-screen')


serve()
