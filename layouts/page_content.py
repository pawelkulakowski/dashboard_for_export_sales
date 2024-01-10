import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


page_content = html.Div(
    id='page-content',
    style=CONTENT_STYLE
)
