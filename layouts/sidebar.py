import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import base64
import datetime


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",

}

zetkama_logo = '/home/pkulakow/workspace/dash-zetkama/assets/zetkama.png'
encoded_zetkama_logo = base64.b64encode(open(zetkama_logo, 'rb').read())


sidebar = html.Div(style=SIDEBAR_STYLE, children=[
    dbc.Navbar([
        dbc.Nav([
            html.Img(src=f'data:image/png;base64,{encoded_zetkama_logo.decode()}', width='180px'),
            dbc.NavItem(dbc.NavLink('Dane ogólne', href='/general')),
            dbc.NavItem(dbc.NavLink('Dynamika wpływu zamówień', href='/dynamics')),
            dbc.NavItem(dbc.NavLink('Klienci', href='/clients')),
            dbc.NavItem(dbc.NavLink('Kraje', href='/countries')),
            dbc.NavItem(dbc.NavLink('Rynki', href='/markets'))
        ],
        vertical=True,
        pills=True)
    ]),
    html.Div(f'{datetime.date.today()}, CW:{datetime.date.today().isocalendar()[1]}', style={'position':'fixed', 'bottom':0})
]
)
