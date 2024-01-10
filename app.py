import base64
import datetime
import dash
import dash_auth
import dash_bootstrap_components as dbc

from dash import dcc
from dash import html
from dash_iconify import DashIconify
import dash_mantine_components as dmc

from dash import dash_table
import plotly.graph_objects as go
import time

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate



from datetime import date
from datetime import datetime
from datetime import timedelta

# Main Page imports
from database.general_main import generate_total_new_orders_from_current_week, \
                                  generate_sales_data_bar_fig, \
                                  generate_order_data_line_fig, \
                                  generate_detailed_order_data_fig, \
                                  generate_current_sales_wallet_situation 
                                  

from database.offers_main import generate_offers_total_fig, \
                                 generate_offers_map_fig, \
                                 generate_offers_activitity_fig, \
                                 prepare_offers_data_by_iso_country

# company page
from database.company_list import generate_company_list_for_dropdown
from database.company_sales import generate_company_sales_data_bar_fig, generate_company_sales_data_heatmap_fig
from database.company_activities import get_company_all_activities
from database.company_order_dynamics import generate_company_order_dynamics_fig
from database.company_open_orders import get_company_open_orders

# offers page
from database.offers import prepare_offers_data
from database.offers_problems import get_offers_from_2021_without_district_code, \
                                     get_offers_from_2021_without_salesman_code, \
                                     get_offers_from_2021_without_expiration_date

# leads page
from database.leads_statistics import generate_total_leads_by_year_fig, \
                                      generate_data_for_last_contact_leads_table, \
                                      generate_number_of_leads_by_region, \
                                      generate_of_leads_by_stage_region_contact, \
                                      generate_number_of_potential_clients_by_region, \
                                      generate_of_potential_clients_by_stage_region_contact, \
                                      generate_active_leads_details, \
                                      generate_active_potential_clients_details, \
                                      generate_of_lost_clients_by_stage_region_contact, \
                                      generate_active_lost_clients_details, \
                                      get_activities_by_lead_number, \
                                      get_activities_by_potential_client_number, \
                                      generate_funnel_graph

from database.leads import prepare_leads_data, \
                           get_countries_from_clients_and_leads_for_dropdown, \
                           get_companies_from_clients_and_leads_by_country_data, \
                           get_activities_by_company_lead_number

# leads and activities page
from database.leads2 import get_last_ten_leads

# delivery page
from database.general_delivery_time import generate_delivery_data_fig



# report page
from database.user_weekly_report import get_all_activities

# Conditions page
from database.conditions import prepare_data_for_conditions_table, get_unique_regions

# new sales page by region
from database.new_sales_by_region import generate_new_sales_and_products_from_current_year_by_region_graph, generetate_total_new_sales_and_products_from_current_year, generate_graphs_for_region_view

# Order book page
from database.order_book import generate_order_book_in_time_fig, \
                                generate_order_book_in_time_with_options_fig, \
                                generate_order_book_by_month_fig, \
                                testtest

# Orders
from database.orders import generate_orders_by_year_fig, \
                            generate_orders_by_quarter_fig, \
                            generate_orders_by_month_fig


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",}

VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'world'}

zetkama_logo = 'assets/zetkama.png'
encoded_zetkama_logo = base64.b64encode(open(zetkama_logo, 'rb').read())

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div(
    [
        html.Div(
            style=SIDEBAR_STYLE, 
            children=[
                dbc.Navbar([
                    dbc.Nav([
                        html.Img(src=f'data:image/png;base64,{encoded_zetkama_logo.decode()}', width='180px'),
                        dbc.NavItem(dbc.NavLink('Dane ogólne', href='/')),
                        dbc.NavItem(dbc.NavLink('Klienci', href='/client')),
                        dbc.NavItem(dbc.NavLink('--umowy handlowe', href='/conditions')),
                        dbc.NavItem(dbc.NavLink('Zarządzanie ofertami', href='/offers')),
                        dbc.NavItem(dbc.NavLink('Zarządzanie relacjami', href='/leads')),
                        dbc.NavItem(dbc.NavLink('Raport tygodniowy', href='/report')),
                        html.Br(),
                        dbc.NavItem(dbc.NavLink('Terminy dostaw', href='/timing')),
                        dbc.NavItem(dbc.NavLink('Nowe sprzedaże - test', href='/new_sales_by_region')),
                        dbc.NavItem(dbc.NavLink('Oferty pulpit - test', href='/offers_main')),
                        dbc.NavItem(dbc.NavLink('Portfel - test', href='/order_book')),
                        dbc.NavItem(dbc.NavLink('Zamówienia - test', href='/orders'))
                        ],
                        vertical=True,
                        pills=True)])]),
        html.Div(
            id='page-content',
            style=CONTENT_STYLE
            ),
        dcc.Location(
            id='url'
            )
    ])


page_main = html.Div([
    html.Div(id='home-trigger-1'),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader('Sprzedaż'),
            dbc.CardBody(dbc.Spinner(html.Div(id='home-div-0a'), color='primary'))
            ]),
            width=3
        ),
        dbc.Col(dbc.Card([
                dbc.CardHeader('Zamówienia z tego tygodnia'),
                dbc.CardBody(dbc.Spinner(html.Div(id='home-div-0b'), color='primary'))
            ]),
            width=3
        ),
        dbc.Col(dbc.Card([
                dbc.CardHeader('Statusy ofert'),
                dbc.CardBody(dbc.Spinner(html.Div(id='home-div-0c'), color='primary'))
            ]),
            width=3
        ),
        dbc.Col(dbc.Card([
                dbc.CardHeader('Nowe zamówienia'),
                dbc.CardBody(dbc.Spinner(html.Div(id='home-div-0d'), color='primary'))
            ]),
            width=3
        )
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader('Sprzedaż w poszczególnych latach'),
            dbc.CardBody(dbc.Spinner(html.Div(id='home-div-1a'), color='primary'))
            ]),
            width=6
        ),
        dbc.Col(dbc.Card([
            dbc.CardHeader('Portfel'),
            dbc.CardBody(dbc.Spinner(html.Div(id='home-div-1b'), color='primary'))
            ]),
            width=6
        )
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(
                    dbc.Row([
                    dbc.Col(
                        children='Wpływ zamówień'
                    ),
                    dbc.Col(
                        dbc.RadioItems(
                            options=[
                                {'label': 'Tygodniowo', 'value':1},
                                {'label':'Narastająco', 'value':2}
                            ],
                            value=1,
                            id='home-radio-1',
                            inline=True
                        )
                    )
                ])
                ),
                dbc.CardBody(
                    dbc.Spinner(html.Div(id='home-div-2'), color='primary')
                )
            ]),
            width=8
        ),
        dbc.Col(dbc.Spinner(html.Div(id='home-div-3'), color='primary'),
        width=4
        ),
            
    ]),
    html.Br(),
    dbc.Row(
        dbc.Col(dbc.Card([
            dbc.CardHeader('Aktywność ofertowa'),
            dbc.CardBody(dbc.Spinner(html.Div(id='home-div-4'), color='primary'))
        ]),
        width=12
        )
    )
])

page_company = html.Div([
    dcc.Dropdown(
        id='company-dropdown-1',
        options = generate_company_list_for_dropdown(),
        className = 'w-50'
    ),
    html.Br(),
    dbc.Row([
        dbc.Col(
            dcc.Loading(html.Div(id='company-div-1'), type='default'),
            width=7,
        ),
        dbc.Col(
            dcc.Loading(html.Div(id='company-div-3'), type='default'),
            width=5,
        ),
          
    ], className='h-25')
    ,
    html.Br(),
    dbc.Tabs([
        dbc.Tab(label='Wpływ zamówień', tab_id='company-tab-1'),
        dbc.Tab(label='Sprzedaż po produktach', tab_id='company-tab-2'),
        dbc.Tab(label='Otwarte zamówienia', tab_id='company-tab-3')
    ],
    active_tab='company-tab-1',
    id = 'company-tabs'),
    html.Hr(),
    html.Br(),
    dcc.Loading(html.Div(id='company-div-2'),type='default')
])

page_offers = html.Div([
    dbc.Tabs(
        [dbc.Tab(label='Oferty', tab_id='offers-tab-1'),
        dbc.Tab(label='Problemy', tab_id='offers-tab-2'),
        dbc.Tab(label='Statystyka', tab_id='offers-tab-3')],
        id='offers-tabs-1',
        active_tab='offers-tab-1'
    ),
    dbc.CardBody([
        html.Div(
        id='offers-div-1'
    ),
    html.Div(
        id='offers-div-2'
    )])
])



page_leads = html.Div([
    html.Div([
        dbc.Tabs([
            dbc.Tab(label='Dane ogólne', tab_id='leads-tab-1'),
            dbc.Tab(label='Zarządzanie', tab_id='leads-tab-2'),
            dbc.Tab(label='Wykresy', tab_id='leads-tab-3'),
            dbc.Tab(label='Lejek', tab_id='leads-tab-4')
        ],
        id='leads-tabs',
        active_tab='leads-tab-1')
    ]),
    html.Div(id='leads-main-1'),
    
])

page_leads_one = html.Div([dbc.Card([
        dmc.Accordion(
            children=[
                dmc.AccordionItem(
                    icon=[DashIconify(icon="carbon:radio-button-checked", color="grey", width=30)],
                    label="Namiary handlowe",
                    children=[html.Div(id="accordion-contents-1", className="mt-3")]
                    
                ),
                dmc.AccordionItem(
                    icon=[DashIconify(icon="carbon:radio-button-checked", color="grey", width=30)],
                    label="Klienci potencjalni",
                    children=[html.Div(id="accordion-contents-2", className="mt-3")]
                    
                ),
                dmc.AccordionItem(
                    icon=[DashIconify(icon="carbon:radio-button-checked", color="grey", width=30)],
                    label="Klienci utraceni",
                    children=[html.Div(id="accordion-contents-3", className="mt-3")]
                    
                )],
            id="accordion",
            state={'0':False, '1':False, '2':False},
        )
])])


    

page_leads_one_accordion_one = dbc.Row(
            [
                # Left
                dbc.Col(children=[
                    html.Div(
                        id='leads-page-one-3',
                        className="h-15 py-2",
                    ),
                    html.Div(
                        id='leads-page-one-4',
                        className="h-15 py-2",
                    ),
                    html.Div(
                        id='leads-page-one-5',
                        className="h-15 py-2",
                    ),
                    html.Div(
                        id='leads-page-one-6',
                        className="h-15 py-2",
                    ),
                    html.Div(
                        id='leads-page-one-7',
                        className="h-15 py-2",
                    ),
                    html.Div(
                        id='leads-page-one-8',
                        className="h-15 py-2",
                    ),
                    html.Div(
                        id='leads-page-one-8a',
                        className="h-15 py-2",
                    ),
                    
                ], width=6),
                # Right
                dbc.Col(
                    [
                        # Top
                        html.Div(
                            id = 'leads-page-one-16',
                            className="h-50 py-2",
                        ),
                        # Bottom
                        html.Div(
                            id = 'leads-page-one-16b',
                            className="h-50 py-2",
                        ),
                    ],
                    width=6,
                ),
            ],
            className="h-80",
        )

page_leads_one_accordion_two = dbc.Row(
            [
                # Left
                dbc.Col(children=[
                    html.Div(
                        id='leads-page-one-9',
                        className="h-15 py-2",
                    ),
                    html.Div(
                        id='leads-page-one-10',
                        className="h-15 py-2",
                    ),
                    html.Div(
                        id='leads-page-one-11',
                        className="h-15 py-2",
                    ),
                    html.Div(
                        id='leads-page-one-12',
                        className="h-15 py-2",
                    ),
                    html.Div(
                        id='leads-page-one-13',
                        className="h-15 py-2",
                    ),
                    html.Div(
                        id='leads-page-one-14',
                        className="h-15 py-2",
                    ),
                    html.Div(
                        id='leads-page-one-14a',
                        className="h-15 py-2",
                    ),
                    html.Div(
                        id='leads-page-one-15',
                        className="h-15 py-2",
                    ),
                    
                ], width=6),
                # Right
                dbc.Col(
                    [
                        # Top
                        html.Div(
                            id = 'leads-page-one-18',
                            className="h-50 py-2",
                        ),
                        # Bottom
                        html.Div(
                            id = 'leads-page-one-18b',
                            className="h-50 py-2",
                        ),
                    ],
                    width=6,
                ),
            ],
            className="h-80",
        )

page_leads_one_accordion_three = dbc.Row(
            [
                # Left
                dbc.Col(children=[
                    html.Div(
                        id='leads-page-one-30',
                        className="h-15 py-2",
                    ),
                    html.Div(
                        id='leads-page-one-31',
                        className="h-15 py-2",
                    ),
                    html.Div(
                        id='leads-page-one-32',
                        className="h-15 py-2",
                    ),
                    html.Div(
                        id='leads-page-one-33',
                        className="h-15 py-2",
                    ),
                    html.Div(
                        id='leads-page-one-34',
                        className="h-15 py-2",
                    ),
                    html.Div(
                        id='leads-page-one-34a',
                        className="h-15 py-2",
                    ),
                    
                ], width=6),
                # Right
                dbc.Col(
                    [
                        # Top
                        html.Div(
                            id = 'leads-page-one-38',
                            className="h-50 py-2",
                        ),
                        # Bottom
                        html.Div(
                            id = 'leads-page-one-39',
                            className="h-50 py-2",
                            
                        ),
                    ],
                    width=6,
                ),
            ],
            className="h-80",
        )


page_leads_two = html.Div([

    dbc.Card(children=[ #style={'margin-top': '-1.7rem'},
        dbc.CardHeader(children=[
             dbc.Row([
                dbc.Col(
                    dbc.RadioItems(
                        id='leads-radio-1',
                        options = [{'label':i, 'value':i} for i in ['ADUDKA', 'AGOLEBIO', 'ALINKIEW', 'AOLSZEWS', 'DSUJEWIC', 'DSTUKUS', 'PKULAKOW']],
                        value = None,
                        
                    ),
                ),
                

                dbc.Col([
                    dbc.Row(dbc.Col(
                        dbc.Checklist(
                        options=[
                            {'label':'Klient', 'value':'klient'},
                            {'label':'Potencjalny klient', 'value':'potencjalny_klient'},
                            {'label':'Lead', 'value':'lead'},
                            
                        ],
                        value=['klient', 'potencjalny_klient', 'lead'],
                        id='leads-switches-1',
                        ),
                        width=12
                    )),
                    html.Br(),
                    dbc.Row(dbc.Col(html.Div(id='leads-drop-1'),width=12)
                        
                    )
                ]),
                dbc.Col(
                    html.Div(id='leads-div-1')
                ),
                dbc.Col(
                    html.Div(id='leads-div-2')
                ),
                dbc.Col(
                    html.Div(id='leads-div-3')
                )
            ])
        ]),
        dbc.CardBody([
            dbc.Row(
                dbc.Col(style={'margin-top': '-1.3rem', 'height': '350px'}, children=(dcc.Loading(html.Div(id='leads-div-4'))))
            ),
        ]),
        dbc.CardFooter(style={'height': '250px'},children=[
            dbc.Row(
                dbc.Col(style={'margin-top': '-0.8rem'}, children=(html.Div(id='leads-div-5')))
            ),
            
        ])
    ]),
    html.Br(),
    html.Br(),
    html.Hr(),
    html.Br(),
    html.Br(),
    html.Div(
        id='leads-div-6'
    )
])

page_leads_three = html.Div([
    dbc.Card(
        dbc.Row([
            dbc.Col(html.Div(id='leads-page-three-1')),
            dbc.Col(html.Div(id='leads-page-three-2'))
        ])
    )
])


page_leads_four = html.Div([
    dbc.RadioItems(
        id='leads-page-four-radio-1',
        options = [{'label':i, 'value':i} for i in ['ALL', 'DE', 'HU', 'IT', 'NL', 'PE', 'RU', 'VN']],
        value = 'ALL',
        inline=True
    ),
    html.Div(id='leads-page-four-div-1')
])


page_timing = html.Div([
    html.Div(id='timing-trigger-1'),
    dbc.Spinner(html.Div(id='timing-div-1'))   
])

page_report = html.Div([
    dbc.Card(children=(dbc.CardBody([
    dbc.Row([
        dbc.Col(
        dcc.DatePickerRange(
            id='report-date_picker-1',
            min_date_allowed=date(2017, 6, 1),
            # max_date_allowed=date.today(),
            #start_date=datetime.now().date() - timedelta(weeks=4),
            #end_date=date.today(),
            display_format ='DD-MM-YYYY'
    ), width=4),
        dbc.Col([
        dbc.RadioItems(
            id='report-radio-1',
            options = [{'label':i, 'value':i} for i in ['ADUDKA', 'AGOLEBIO', 'ALINKIEW', 'AOLSZEWS', 'DSUJEWIC', 'DSTUKUS', 'PKULAKOW']],
            value = None,
            inline=True
        )], width=8)]),
    dbc.Row([
        dbc.Col(width=4),
        dbc.Col([
            dbc.Checklist(
                options=[
                    {'label':'Zadania', 'value':'zadania'},
                    {'label':'Spotkania', 'value':'spotkania'},
                    {'label':'Klienci', 'value':'klienci'},
                    {'label':'Potencjalni klienci', 'value':'potencjalni_klienci'},
                    {'label':'Lead\'y', 'value':'leady'},
                    {'label':'Oferty', 'value':'oferty'}
                ],
                value=['zadania', 'spotkania', 'klienci', 'potencjalni_klienci', 'leady', 'oferty'],
                id='report-switches-1',
                switch=True,
                inline= True
            )

        ], width=8)
    ])]))),

    html.Hr(),
    dbc.Card(
        dbc.CardBody(
            html.Div(id='report-div-1')
        )
    ),
    html.Div(id='test')
])

page_conditions = html.Div([
    html.Div(id='conditions-1-trigger'),
    html.Div(id='conditions-1-div'),
    html.Hr(),
    html.Div(id='conditions-2-div'),
    html.Hr(),
    html.Div(id='conditions-3-div')
])

page_new_sales_by_region = html.Div([
    html.Div(id='new-sales-by-region-trigger'),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader('Nowe zamówienia'),
                dbc.CardBody(dcc.Loading(html.Div(id='new-sales-by-region-div-1')))
            ]),
            width=3,
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader('Nowe zamówienia w podziale na powiaty'),
                dbc.CardBody(dcc.Loading(html.Div(id='new-sales-by-region-div-2')))
            ]),
            width=9,
        )
    ]),
    html.Br(),
    dbc.Row(
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.Div(id='new-sales-by-region-div-3')),
            ])
        )
    ),
    html.Br(),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader('Nowi klienci'),
                dbc.CardBody(dcc.Graph(id='new-sales-fig-1'))
            ]),
            width=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader('Nowe rozszerzenia'),
                dbc.CardBody(dcc.Graph(id='new-sales-fig-2'))
            ]),
            width=6
        )
    ])
])

page_offers_main = html.Div([
    html.Div(id='offers-main-trigger-1'),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader('Otwarte oferty'),
            dbc.CardBody(dbc.Spinner(html.Div(id='offers-main-div-1'), color='primary'))
        ]),
        width=8
        ),
        dbc.Col(dbc.Card([
            dbc.CardHeader('Top rynki'),
            dbc.CardBody(dbc.Spinner(html.Div(id='offers-main-div-2'), color='primary'))
        ]),
        width=4)
        ]),
    html.Div(id='offers-main-div-3'),
    dbc.Row(
        dbc.Col(dbc.Card([
            dbc.CardHeader('Aktywność ofertowa'),
            dbc.CardBody(dbc.Spinner(html.Div(id='offers-main-div-4'), color='primary'))
        ]),
        width=12
        )
    )
])

page_order_book = html.Div([
    html.Div(id='order-book-trigger'),
    dbc.Card([
        dbc.CardHeader('Portfel'),
        dbc.CardBody(dbc.Spinner(html.Div(id='order-book-div-1'), color='primary'))
    ]),
    dbc.Card([
        dbc.CardHeader('Różnica pomiędzy portfelami'),
        dbc.CardBody(dbc.Spinner(html.Div(id='order-book-div-2'), color='primary'))
    ]),
    html.Div(dcc.Graph(figure=testtest()))
])

page_orders = html.Div([
    html.Div(id='orders-trigger'),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(
                    dbc.Row([
                    dbc.Col(
                        children='Wpływ zamówień'
                    ),
                    dbc.Col(
                        dbc.RadioItems(
                            options=[
                                {'label':'Y/y', 'value':1},
                                {'label':'Q/q', 'value':2},
                                {'label':'M/m', 'value':3}
                            ],
                            value=3,
                            id='orders-radio-1',
                            inline=True
                        )
                    )
                ])
                ),
                dbc.CardBody(
                    dbc.Spinner(html.Div(id='orders-div-1'), color='primary')
                )
            ]),
            width=12)
        ]),
])

@app.callback(
    Output('orders-div-1', 'children'),
    Input('orders-trigger', 'children'),
    Input('orders-radio-1', 'value')
)
def orders_graph(trigger, period):
    if trigger is None:
        if period == 1:
            fig = generate_orders_by_year_fig()
        if period == 2:
            fig = generate_orders_by_quarter_fig()
        if period == 3:
            fig = generate_orders_by_month_fig()

        return dcc.Graph(figure=fig)
            

'''CALLBACKS SECTION'''

# Layout callbacks
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return page_main
    if pathname == '/client':
        return page_company
    if pathname == '/offers':
        return page_offers
    if pathname == '/leads':
        return page_leads
    if pathname == '/timing':
        return page_timing
    if pathname == '/report':
        return page_report
    if pathname == '/conditions':
        return page_conditions
    if pathname == '/test':
        return page_test
    if pathname == '/new_sales_by_region':
        return page_new_sales_by_region
    if pathname == '/offers_main':
        return page_offers_main
    if pathname == '/order_book':
        return page_order_book
    if pathname == '/orders':
        return page_orders
        

# Main page callbacks
@app.callback(
    Output('home-div-0a', 'children'),
    Input('home-trigger-1', 'children'))
def generate_current_sales_and_wallet_situation_graph(trigger):
    if trigger == None:
        return dcc.Graph(figure=generate_current_sales_wallet_situation())
            

@app.callback(
    Output('home-div-0b', 'children'),
    Input('home-trigger-1', 'children'))
def generate_sales_data_graph(trigger):
    if trigger == None:
        return dcc.Graph(figure=generate_total_new_orders_from_current_week())

@app.callback(
    Output('home-div-0c', 'children'),
    Input('home-trigger-1', 'children'))
def generate_sales_data_graph(trigger):
    if trigger == None:
        return dcc.Graph(figure=generate_offers_total_fig())

@app.callback(
    Output('home-div-0d', 'children'),
    Input('home-trigger-1', 'children'))
def generate_sales_data_graph(trigger):
    if trigger == None:
        return dcc.Graph(figure=generetate_total_new_sales_and_products_from_current_year())


@app.callback(
    Output('home-div-1a', 'children'),
    Input('home-trigger-1', 'children'))
def generate_sales_data_graph(trigger):
    if trigger == None:
        return dcc.Graph(figure=generate_sales_data_bar_fig())

@app.callback(
    Output('home-div-1b', 'children'),
    Input('home-trigger-1', 'children'))
def generate_order_book_graph(trigger):
    if trigger == None:
        return dcc.Graph(figure=generate_order_book_in_time_fig())
        
@app.callback(
    Output('home-div-2', 'children'),
    Input('home-trigger-1', 'children'),
    Input('home-radio-1', 'value'))
def generate_order_data_graph(trigger, value):
    fig1, fig2 = generate_order_data_line_fig()
    if trigger == None:
        if value == 1:
            fig = fig1
        elif value == 2:
            fig = fig2
    return dcc.Graph(id='home-graph-2', figure=fig)

@app.callback(
    Output('home-div-3', 'children'),
    Input('home-graph-2', 'clickData'))
def display_click_data(clickData):
    if clickData is None:
        cw = date.today().isocalendar()[1]
        year = date.today().year
    else:
        cw = clickData['points'][0]['customdata']
        years = {
            0:2018,
            1:2019,
            2:2020,
            3:2021,
            4:2022}
        year = years[clickData['points'][0]['curveNumber']]
    return dbc.Card([
        dbc.CardHeader('Szczegółowy wpływ tygodniowy'),
        dbc.CardBody(
            dcc.Graph(figure=generate_detailed_order_data_fig(year, cw))
        )
    ])

@app.callback(
    Output('home-div-4', 'children'),
    Input('home-trigger-1', 'children'))
def show_offers_activity_graph(trigger):
    if trigger == None:
        return dcc.Graph(figure=generate_offers_activitity_fig())


# Company page callbacks
@app.callback(
    Output('company-div-1', 'children'),
    Input('company-dropdown-1', 'value'))
def show_company_sales(company_name):
    if company_name is None:
        raise PreventUpdate
    else:
        return dbc.Card([
            dbc.CardBody([
                html.Label('Wartość sprzedaży'),
                dcc.Graph(
                    figure=generate_company_sales_data_bar_fig(company_name)
                )], style={'height':'100%'}
            )
        ])

@app.callback(
    Output('company-div-3', 'children'),
    Input('company-dropdown-1', 'value'))
def show_company_activities(company_name):
    if company_name is None:
        raise PreventUpdate
    else:
        df = get_company_all_activities(company_name)
        return dbc.Card([
            dbc.CardBody([
                html.Label('Aktywności'),
                dash_table.DataTable(
                columns=[{'name':i, 'id':i} for i in df.columns],
                data = df.to_dict('records'),
                style_cell={
                'fontSize': 12,    
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth': 10,
                },
                tooltip_data=[
                    {
                        column: {'value': str(value), 'type': 'markdown'}
                        for column, value in row.items()
                    } for row in df.to_dict('records')
                ],
                tooltip_duration=None,
                page_action='native',
                page_current= 0,
                page_size= 12,
            )
                
        ], style={'height':'100%'})
        ])

@app.callback(
    Output('company-div-2', 'children'),
    [Input('company-dropdown-1', 'value'),
    Input('company-tabs', 'active_tab')])
def show_company_data(company_name, active_tab):
    if company_name is None:
        raise PreventUpdate()
    if active_tab == 'company-tab-1':
        return dbc.Card([
            dbc.CardBody(
                dcc.Graph(
                    figure=generate_company_order_dynamics_fig(company_name)
                )
            )
        ])
    if active_tab == 'company-tab-2':
        return dbc.Card([
            dbc.CardBody(
                dcc.Graph(
                    figure=generate_company_sales_data_heatmap_fig(company_name)
                )
            )
        ])
    if active_tab == 'company-tab-3':
        company_open_orders = get_company_open_orders(company_name)
        return html.Div(
            dash_table.DataTable(
                    columns=[{'name':i, 'id':i} for i in company_open_orders.columns],
                    data = company_open_orders.to_dict('records'),
                    style_as_list_view=True,
                    style_cell={'textAlign': 'left'},
                    style_header = {'backgroundColor': 'rgb(230, 230, 230)',
                                    'fontWeight': 'bold'},
                )
        )


# Offers page callbacks
@app.callback(
    Output('offers-div-1', 'children'),
    Input('offers-tabs-1', 'active_tab'))
def show_radio(active_tab):
    if active_tab == 'offers-tab-1':
        return dbc.RadioItems(
            id='offers-radio-1',
            options = [{'label':i, 'value':i} for i in ['ME-DE', 'ME-HU', 'ME-IT', 'ME-NL', 'ME-PE', 'ME-RU','ME-VN']],
            value = 'ME-DE',
            inline=True
        )
    if active_tab == 'offers-tab-2':
        df = get_offers_from_2021_without_district_code()
        df2 = get_offers_from_2021_without_salesman_code()
        df3 = get_offers_from_2021_without_expiration_date()
        return html.Div([
            dbc.Alert('Bez przypisanego powiatu', color='danger'),
            dash_table.DataTable(
                columns=[{'name':i, 'id':i} for i in df.columns],
                data = df.to_dict('records'),
                style_as_list_view=True,
                editable=True
            ),
            html.Br(),
            dbc.Alert('Bez przypisanego sprzedawcy', color='danger'),
            dash_table.DataTable(
                columns=[{'name':i, 'id':i} for i in df2.columns],
                data = df2.to_dict('records'),
                style_as_list_view=True,
                editable=True
            ),
            html.Br(),
            dbc.Alert('Bez daty ważności', color='danger'),
            dash_table.DataTable(
                columns=[{'name':i, 'id':i} for i in df3.columns],
                data = df3.to_dict('records'),
                style_as_list_view=True,
                editable=True
            )

        ])
    

@app.callback(
    Output('offers-div-2', 'children'),
    Input('offers-tabs-1', 'active_tab'), 
    Input('offers-radio-1', 'value'))
def show_offers(active_tab, district):
    if active_tab == 'offers-tab-1':
        df_this_week, df_previous_week, df_expired, df_active, df_summary, df_problems = prepare_offers_data(district)
        return html.Div([
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Alert('Podsumowanie', color='primary'),
                    dash_table.DataTable(
                        columns=[{'name':i, 'id':i} for i in df_summary.columns],
                        data = df_summary.to_dict('records'),
                        style_as_list_view=True,
                        style_cell={'textAlign': 'left'},
                        style_header = {'backgroundColor': 'rgb(230, 230, 230)',
                                        'fontWeight': 'bold'},
                    )],
                    width=6
                ),
                dbc.Col([
                    dbc.Alert('Problemy', color='danger'),
                    dash_table.DataTable(
                        columns=[{'name':i, 'id':i} for i in df_problems.columns],
                        data = df_problems.to_dict('records'),
                        style_as_list_view=True,
                        style_cell={'textAlign': 'left', 'whiteSpace':'normal', 'height':'auto'},
                        style_header = {'backgroundColor': 'rgb(230, 230, 230)',
                                        'fontWeight': 'bold'},
                        editable=True
                    )],
                    width=6
                )
            ]),
            html.Br(),
            dbc.Alert('Oferty z tego tygodnia', color='warning'),
            dash_table.DataTable(
                columns=[{'name':i, 'id':i} for i in df_this_week.columns],
                data = df_this_week.to_dict('records'),
                style_as_list_view=True,
                editable=True
            ),
            html.Br(),
            dbc.Alert('Oferty z poprzedniego tygodnia', color='secondary'),
            dash_table.DataTable(
                columns=[{'name':i, 'id':i} for i in df_previous_week.columns],
                data = df_previous_week.to_dict('records'),
                style_as_list_view=True,
                editable=True
            ),
            html.Br(),
            dbc.Alert('Oferty przeterminowane',color='danger'),
            dash_table.DataTable(
                columns=[{'name':i, 'id':i} for i in df_expired.columns],
                data = df_expired.to_dict('records'),
                style_as_list_view=True,
                editable=True,
            ),
            html.Br(),
            dbc.Alert('Oferty aktywowane', color='success'),
            dash_table.DataTable(
                columns=[{'name':i, 'id':i} for i in df_active.columns],
                data = df_active.to_dict('records'),
                style_as_list_view=True,
                editable=True
            ),
        ])




# Leads page callbacks

@app.callback(
    Output('leads-main-1', 'children'),
    Input('leads-tabs', 'active_tab'))
def show_pages(tab):
    if tab is None:
        raise PreventUpdate
    if tab == 'leads-tab-1':
        return page_leads_one
    if tab =='leads-tab-2':
        return page_leads_two
    if tab =='leads-tab-3':
        return page_leads_three
    if tab == 'leads-tab-4':
        return page_leads_four


@app.callback(Output("accordion-contents-1", "children"), Input("accordion", "state"))
def show_state(state):
    if state is None:
        raise PreventUpdate
    if state['0'] == True:
        return page_leads_one_accordion_one


@app.callback(Output("accordion-contents-2", "children"), Input("accordion", "state"))
def show_state(state):
    if state is None:
        raise PreventUpdate
    if state['1'] == True:
        return page_leads_one_accordion_two


@app.callback(Output("accordion-contents-3", "children"), Input("accordion", "state"))
def show_state(state):
    if state is None:
        raise PreventUpdate
    if state['2'] == True:
        return page_leads_one_accordion_three





@app.callback(
    Output('leads-page-one-3', 'children'),
    Output('leads-page-one-4', 'children'),
    Output('leads-page-one-5', 'children'),
    Output('leads-page-one-6', 'children'),
    Output('leads-page-one-7', 'children'),
    Output('leads-page-one-8', 'children'),
    Output('leads-page-one-8a', 'children'),
    Input('leads-tabs', 'active_tab'))
def show_leads_statistics(tab):
    if tab=='leads-tab-1':
        overall_leads = generate_number_of_leads_by_region()
        active_leads, leads_usage, action_leads, initial_leads, interested_leads, leftovers = generate_of_leads_by_stage_region_contact()
        
        overall_leads_tbl = dash_table.DataTable(
            id='overall-leads-tbl',
            columns=[{'name':i, 'id':i} for i in overall_leads.columns if i != 'id'],
            data = overall_leads.to_dict('records'),
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'borderBottom': '1px solid black'},
            style_as_list_view=True,
            style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'border':'0px'},
            style_cell_conditional=[
            {'if': {'column_id': '2022'},
             'minWidth': '120px', 'width': '120px', 'maxWidth': '120px', 'fontWeight': 'bold'}])

        active_leads_tbl = dash_table.DataTable(
            id='active-leads-tbl',
            columns=[{'name':i, 'id':i} for i in active_leads.columns if i != 'id'],
            data = active_leads.to_dict('records'),
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'borderBottom': '1px solid black'},
            style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'border':'0px'},
            style_cell_conditional=[
            {'if': {'column_id': 'stage_id'},
             'minWidth': '120px', 'width': '120px', 'maxWidth': '120px', 'fontWeight': 'bold'}
        ])

        leads_usage_tbl = dash_table.DataTable(
            id='leads-usage-tbl',
            columns=[{'name':i, 'id':i} for i in leads_usage.columns if i != 'id'],
            data = leads_usage.to_dict('records'),
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'borderBottom': '1px solid black'},
            style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'border':'0px'},
            style_cell_conditional=[
            {'if': {'column_id': 'period'},
             'minWidth': '120px', 'width': '120px', 'maxWidth': '120px', 'fontWeight': 'bold'}])
        
        action_leads_tbl = dash_table.DataTable(
            id='action-leads-tbl',
            columns=[{'name':i, 'id':i} for i in action_leads.columns if i != 'id'],
            data = action_leads.to_dict('records'),
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'borderBottom': '1px solid black'},
            style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'border':'0px'},
            style_cell_conditional=[
            {'if': {'column_id': 'Akcja zaczepna'},
             'minWidth': '120px', 'width': '120px', 'maxWidth': '120px', 'fontWeight': 'bold'}])

        initial_leads_tbl = dash_table.DataTable(
            id='initial-leads-tbl',
            columns=[{'name':i, 'id':i} for i in initial_leads.columns if i != 'id'],
            data = initial_leads.to_dict('records'),
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'borderBottom': '1px solid black'},
            style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'border':'0px'},
            style_cell_conditional=[
            {'if': {'column_id': 'Wstępny'},
             'minWidth': '100px', 'width': '100px', 'maxWidth': '100px', 'fontWeight': 'bold'}])
        
        interested_leads_tbl = dash_table.DataTable(
            id='interested-leads-tbl',
            columns=[{'name':i, 'id':i} for i in interested_leads.columns if i != 'id'],
            data = interested_leads.to_dict('records'),
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'borderBottom': '1px solid black'},
            style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'border':'0px'},
            style_cell_conditional=[
            {'if': {'column_id': 'Zainteresowany'},
             'minWidth': '120px', 'width': '120px', 'maxWidth': '120px', 'fontWeight': 'bold'}])
    
        leftovers_tbl = dash_table.DataTable(
            id='leftovers-leads-tbl',
            columns=[{'name':i, 'id':i} for i in leftovers.columns if i != 'id'],
            data = leftovers.to_dict('records'),
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'color': 'lightgrey',
                'borderBottom': '1px solid lightgrey'},
            style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'border':'0px', 'color':'lightgrey'},
            style_cell_conditional=[
            {'if': {'column_id': 'stage_id'},
             'minWidth': '120px', 'width': '120px', 'maxWidth': '120px', 'fontWeight': 'bold'}])

        return overall_leads_tbl, active_leads_tbl, leads_usage_tbl, action_leads_tbl, initial_leads_tbl, interested_leads_tbl, leftovers_tbl

@app.callback(
    Output('leads-page-one-16', 'children'),
    Input('active-leads-tbl', 'active_cell'))
def show_active_leads_details(active_cell):
    if active_cell is None:
        raise PreventUpdate
    else:
        col = active_cell['column']
        row = active_cell['row']
        regions = {
            0: None,
            1: 'ME-DE',
            2: 'ME-HU',
            3: 'ME-IT',
            4: 'ME-NL',
            5: 'ME-PE',
            6: 'ME-RU',
            7: 'ME-VN'}
        stages = {
            0: 'TOTAL',
            1: 'Poziom zero',
            2: 'Akcja zaczepna',
            3: 'Wstępny',
            4: 'Zainteresowany'
        }
        
        df = generate_active_leads_details(regions[col], stages[row])
        return dash_table.DataTable(
            id='active-leads-details-tbl',
            columns=[{'name':i, 'id':i} for i in df.columns if i != 'id'],
            data = df.to_dict('records'),
            page_action="native",
            page_current= 0,
            page_size= 10,
            sort_action="native",
            style_as_list_view=True,
            #style_table={'height': '325px'},
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'borderBottom': '1px solid black'},
             style_cell={'border':'0px', 'textAlign': 'left'},
             style_cell_conditional=[
            {'if': {'column_id': 'name'},
             'fontWeight': 'bold',
             'maxWidth':'120px'},
             {'if': {'column_id': 'last_contact'},
             'maxWidth':'60px'},
            {'if': {'column_id': 'note'},
             'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth':'120px'}],
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in df.to_dict('records')
            ],
            tooltip_duration=None)


@app.callback(
    Output('leads-page-one-16b', 'children'),
    Input('active-leads-details-tbl', 'active_cell'))
def show_active_leads_actions(active_cell):
    if active_cell is None:
        raise PreventUpdate
    lead_id = active_cell['row_id']
    df = get_activities_by_lead_number(lead_id)
    return dash_table.DataTable(
            id='22',
            columns=[{'name':i, 'id':i} for i in df.columns if i != 'id'],
            data = df.to_dict('records'),
            page_action="native",
            page_current= 0,
            page_size= 10,
            style_as_list_view=True,
            style_header={
                    'backgroundColor': 'rgb(247, 247, 247)',
                    'fontWeight': 'bold'
                },
            style_cell={
                'textAlign': 'left',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth': 5,
                'fontSize': 14,
                },
            style_data={
                'backgroundColor':'rgb(247, 247, 247)'
            },
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in df.to_dict('records')
            ],
            tooltip_duration=None,
        )           

@app.callback(
    Output('leads-page-one-9', 'children'),
    Output('leads-page-one-10', 'children'),
    Output('leads-page-one-11', 'children'),
    Output('leads-page-one-12', 'children'),
    Output('leads-page-one-13', 'children'),
    Output('leads-page-one-14', 'children'),
    Output('leads-page-one-14a', 'children'),
    Input('leads-tabs', 'active_tab'))
def show_potential_clients_statistics(tab):
    if tab=='leads-tab-1':
        overall_potential_clients = generate_number_of_potential_clients_by_region()
        active_potential_clients, potential_clients_usage, open_offer_potential_clients, action_potential_clients, initial_potential_clients, interested_potential_clients, leftovers = generate_of_potential_clients_by_stage_region_contact()
        
        
        overall_potential_clients_tbl = dash_table.DataTable(
            id='overall-potential-clients-tbl',
            columns=[{'name':i, 'id':i} for i in overall_potential_clients.columns if i != 'id'],
            data = overall_potential_clients.to_dict('records'),
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'borderBottom': '1px solid black'},
            style_as_list_view=True,
            style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'border':'0px'},
            style_cell_conditional=[
            {'if': {'column_id': '2022'},
             'minWidth': '120px', 'width': '120px', 'maxWidth': '120px', 'fontWeight': 'bold'}])

        active_potential_clients_tbl = dash_table.DataTable(
            id='active-potential-clients-tbl',
            columns=[{'name':i, 'id':i} for i in active_potential_clients.columns if i != 'id'],
            data = active_potential_clients.to_dict('records'),
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'borderBottom': '1px solid black'},
            style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'border':'0px'},
            style_cell_conditional=[
            {'if': {'column_id': 'stage_id'},
             'minWidth': '120px', 'width': '120px', 'maxWidth': '120px', 'fontWeight': 'bold'}
        ])

        potential_clients_usage_tbl = dash_table.DataTable(
            id='potential-clients-usage-tbl',
            columns=[{'name':i, 'id':i} for i in potential_clients_usage.columns if i != 'id'],
            data = potential_clients_usage.to_dict('records'),
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'borderBottom': '1px solid black'},
            style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'border':'0px'},
            style_cell_conditional=[
            {'if': {'column_id': 'period'},
             'minWidth': '120px', 'width': '120px', 'maxWidth': '120px', 'fontWeight': 'bold'}])
        
        

        action_potential_clients_tbl = dash_table.DataTable(
            id='action-potential-clients-tbl',
            columns=[{'name':i, 'id':i} for i in action_potential_clients.columns if i != 'id'],
            data = action_potential_clients.to_dict('records'),
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'borderBottom': '1px solid black'},
            style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'border':'0px'},
            style_cell_conditional=[
            {'if': {'column_id': 'Akcja zaczepna'},
             'minWidth': '120px', 'width': '120px', 'maxWidth': '120px', 'fontWeight': 'bold'}])

        initial_potential_clients_tbl = dash_table.DataTable(
            id='initial-potential-clients-tbl',
            columns=[{'name':i, 'id':i} for i in initial_potential_clients.columns if i != 'id'],
            data = initial_potential_clients.to_dict('records'),
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'borderBottom': '1px solid black'},
            style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'border':'0px'},
            style_cell_conditional=[
            {'if': {'column_id': 'Wstępny'},
             'minWidth': '120px', 'width': '120px', 'maxWidth': '120px', 'fontWeight': 'bold'}])
        
        interested_potential_clients_tbl = dash_table.DataTable(
            id='interested-potential-clients-tbl',
            columns=[{'name':i, 'id':i} for i in interested_potential_clients.columns if i != 'id'],
            data = interested_potential_clients.to_dict('records'),
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'borderBottom': '1px solid black'},
            style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'border':'0px'},
            style_cell_conditional=[
            {'if': {'column_id': 'Zainteresowany'},
             'minWidth': '120px', 'width': '120px', 'maxWidth': '120px', 'fontWeight': 'bold'}])
    
        leftovers_potential_clients_tbl = dash_table.DataTable(
            id='leftovers-potential-clients-tbl',
            columns=[{'name':i, 'id':i} for i in leftovers.columns if i != 'id'],
            data = leftovers.to_dict('records'),
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'color': 'lightgrey',
                'borderBottom': '1px solid lightgrey'},
            style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'border':'0px', 'color':'lightgrey'},
            style_cell_conditional=[
            {'if': {'column_id': 'stage_id'},
             'minWidth': '120px', 'width': '120px', 'maxWidth': '120px', 'fontWeight': 'bold'}])

        return overall_potential_clients_tbl, active_potential_clients_tbl, potential_clients_usage_tbl, action_potential_clients_tbl, initial_potential_clients_tbl, interested_potential_clients_tbl, leftovers_potential_clients_tbl


@app.callback(
    Output('leads-page-one-18', 'children'),
    Input('active-potential-clients-tbl', 'active_cell'))
def show_active_potential_clients_details(active_cell):
    if active_cell is None:
        raise PreventUpdate
    else:
        col = active_cell['column']
        row = active_cell['row']
        regions = {
            0: None,
            1: 'ME-DE',
            2: 'ME-HU',
            3: 'ME-IT',
            4: 'ME-NL',
            5: 'ME-PE',
            6: 'ME-RU',
            7: 'ME-VN'}
        stages = {
            0: 'TOTAL',
            1: 'Poziom zero',
            2: 'Akcja zaczepna',
            3: 'Wstępny',
            4: 'Zainteresowany'
        }
        
        
        df = generate_active_potential_clients_details(regions[col], stages[row])
        return dash_table.DataTable(
            id='active-potential-clients-details-tbl',
            columns=[{'name':i, 'id':i} for i in df.columns if i != 'id'],
            data = df.to_dict('records'),
            page_action="native",
            page_current= 0,
            page_size= 10,
            sort_action="native",
            style_as_list_view=True,
            #style_table={'height': '325px'},
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'borderBottom': '1px solid black'},
            style_cell={'border':'0px', 'textAlign': 'left'},
            style_cell_conditional=[
            {'if': {'column_id': 'name'},
             'fontWeight': 'bold',
             'maxWidth':'120px'},
             {'if': {'column_id': 'last_contact'},
             'maxWidth':'60px'},
            {'if': {'column_id': 'note'},
             'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth':'120px'}],
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in df.to_dict('records')
            ],
            tooltip_duration=None)

@app.callback(
    Output('leads-page-one-18b', 'children'),
    Input('active-potential-clients-details-tbl', 'active_cell'))
def show_active_potential_clients_actions(active_cell):
    if active_cell is None:
        raise PreventUpdate
    customer_id = active_cell['row_id']
    df = get_activities_by_potential_client_number(customer_id)
    return dash_table.DataTable(
            id='22',
            columns=[{'name':i, 'id':i} for i in df.columns if i != 'id'],
            data = df.to_dict('records'),
            page_action="native",
            page_current= 0,
            page_size= 10,
            style_as_list_view=True,
            style_header={
                    'backgroundColor': 'rgb(247, 247, 247)',
                    'fontWeight': 'bold'
                },
            style_cell={
                'textAlign': 'left',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth': 5,
                'fontSize': 14,
                },
            style_data={
                'backgroundColor':'rgb(247, 247, 247)'
            },
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in df.to_dict('records')
            ],
            tooltip_duration=None,
        )           

@app.callback(
    Output('leads-page-one-30', 'children'),
    Output('leads-page-one-31', 'children'),
    Output('leads-page-one-32', 'children'),
    Output('leads-page-one-33', 'children'),
    Output('leads-page-one-34', 'children'),
    Output('leads-page-one-34a', 'children'),
    Input('leads-tabs', 'active_tab'))
def show_lost_clients_statistics(tab):
    if tab=='leads-tab-1':
        
        active_lost_clients, lost_clients_usage, action_lost_clients, initial_lost_clients, interested_lost_clients, leftovers = generate_of_lost_clients_by_stage_region_contact()
        
        
    
        active_lost_clients_tbl = dash_table.DataTable(
            id='active-lost-clients-tbl',
            columns=[{'name':i, 'id':i} for i in active_lost_clients.columns if i != 'id'],
            data = active_lost_clients.to_dict('records'),
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'borderBottom': '1px solid black'},
            style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'border':'0px'},
            style_cell_conditional=[
            {'if': {'column_id': 'stage_id'},
             'minWidth': '120px', 'width': '120px', 'maxWidth': '120px', 'fontWeight': 'bold'}
        ])

        lost_clients_usage_tbl = dash_table.DataTable(
            id='lost-clients-usage-tbl',
            columns=[{'name':i, 'id':i} for i in lost_clients_usage.columns if i != 'id'],
            data = lost_clients_usage.to_dict('records'),
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'borderBottom': '1px solid black'},
            style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'border':'0px'},
            style_cell_conditional=[
            {'if': {'column_id': 'period'},
             'minWidth': '120px', 'width': '120px', 'maxWidth': '120px', 'fontWeight': 'bold'}])
        
        action_lost_clients_tbl = dash_table.DataTable(
            id='action-lost-clients-tbl',
            columns=[{'name':i, 'id':i} for i in action_lost_clients.columns if i != 'id'],
            data = action_lost_clients.to_dict('records'),
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'borderBottom': '1px solid black'},
            style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'border':'0px'},
            style_cell_conditional=[
            {'if': {'column_id': 'Akcja zaczepna'},
             'minWidth': '120px', 'width': '120px', 'maxWidth': '120px', 'fontWeight': 'bold'}])

        initial_lost_clients_tbl = dash_table.DataTable(
            id='initial-lost-clients-tbl',
            columns=[{'name':i, 'id':i} for i in initial_lost_clients.columns if i != 'id'],
            data = initial_lost_clients.to_dict('records'),
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'borderBottom': '1px solid black'},
            style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'border':'0px'},
            style_cell_conditional=[
            {'if': {'column_id': 'Wstępny'},
             'minWidth': '120px', 'width': '120px', 'maxWidth': '120px', 'fontWeight': 'bold'}])

        interested_lost_clients_tbl = dash_table.DataTable(
            id='interested-lost-clients-tbl',
            columns=[{'name':i, 'id':i} for i in interested_lost_clients.columns if i != 'id'],
            data = interested_lost_clients.to_dict('records'),
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'borderBottom': '1px solid black'},
            style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'border':'0px'},
            style_cell_conditional=[
            {'if': {'column_id': 'Zainteresowany'},
             'minWidth': '120px', 'width': '120px', 'maxWidth': '120px', 'fontWeight': 'bold'}])


        leftovers_lost_clients_tbl = dash_table.DataTable(
            id='leftovers-lost-clients-tbl',
            columns=[{'name':i, 'id':i} for i in leftovers.columns if i != 'id'],
            data = leftovers.to_dict('records'),
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'color': 'lightgrey',
                'borderBottom': '1px solid lightgrey'},
            style_cell={'minWidth': '40px', 'width': '40px', 'maxWidth': '40px', 'border':'0px', 'color':'lightgrey'},
            style_cell_conditional=[
            {'if': {'column_id': 'stage_id'},
             'minWidth': '120px', 'width': '120px', 'maxWidth': '120px', 'fontWeight': 'bold'}])
    
    

        return active_lost_clients_tbl, lost_clients_usage_tbl, action_lost_clients_tbl, initial_lost_clients_tbl, interested_lost_clients_tbl, leftovers_lost_clients_tbl


@app.callback(
    Output('leads-page-one-38', 'children'),
    Input('active-lost-clients-tbl', 'active_cell'))
def show_active_lost_clients_details(active_cell):
    if active_cell is None:
        raise PreventUpdate
    else:
        col = active_cell['column']
        row = active_cell['row']
        regions = {
            0: None,
            1: 'ME-DE',
            2: 'ME-HU',
            3: 'ME-IT',
            4: 'ME-NL',
            5: 'ME-PE',
            6: 'ME-RU',
            7: 'ME-VN'}
        stages = {
            0: 'TOTAL',
            1: 'Poziom zero',
            2: 'Akcja zaczepna',
            3: 'Wstępny',
            4: 'Zainteresowany'
        }
        
        
        df = generate_active_lost_clients_details(regions[col], stages[row])
        return dash_table.DataTable(
            id='active-lost-clients-details-tbl',
            columns=[{'name':i, 'id':i} for i in df.columns if i != 'id'],
            data = df.to_dict('records'),
            page_action="native",
            page_current= 0,
            page_size= 10,
            sort_action="native",
            style_as_list_view=True,
            #style_table={'height': '325px'},
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'borderBottom': '1px solid black'},
            style_cell={'border':'0px', 'textAlign': 'left'},
            style_cell_conditional=[
            {'if': {'column_id': 'name'},
             'fontWeight': 'bold',
             'maxWidth':'120px'},
             {'if': {'column_id': 'last_contact'},
             'maxWidth':'60px'},
            {'if': {'column_id': 'note'},
             'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth':'120px'}],
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in df.to_dict('records')
            ],
            tooltip_duration=None)

@app.callback(
    Output('leads-page-one-39', 'children'),
    Input('active-lost-clients-details-tbl', 'active_cell'))
def show_active_lost_clients_actions(active_cell):
    if active_cell is None:
        raise PreventUpdate
    customer_id = active_cell['row_id']
    df = get_activities_by_potential_client_number(customer_id)
    return dash_table.DataTable(
            id='22',
            columns=[{'name':i, 'id':i} for i in df.columns if i != 'id'],
            data = df.to_dict('records'),
            page_action="native",
            page_current= 0,
            page_size= 10,
            style_as_list_view=True,
            style_header={
                    'backgroundColor': 'rgb(247, 247, 247)',
                    'fontWeight': 'bold'
                },
            style_cell={
                'textAlign': 'left',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth': 5,
                'fontSize': 14,
                },
            style_data={
                'backgroundColor':'rgb(247, 247, 247)'
            },
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in df.to_dict('records')
            ],
            tooltip_duration=None,
        )      


@app.callback(
    Output('leads-drop-1', 'children'),
    Input('leads-tabs', 'active_tab'),
    Input('leads-radio-1', 'value'))
def show_dropdown_countries(tab, main_representative):
    if tab =='leads-tab-2':
        df = get_countries_from_clients_and_leads_for_dropdown(main_representative)
        options = [{'label':country, 'value':country} for country in df['country']]
        return dcc.Dropdown(
                    id='leads-dropdown-1',
                    options = options,
                    multi=True,
                    placeholder="Wybierz kraj"
                )


@app.callback(
    Output('leads-page-three-1', 'children'),
    Output('leads-page-three-2', 'children'),
    Input('leads-tabs', 'active_tab'))
def show_leads_statistics(tab):
    if tab=='leads-tab-3':
        fig1, fig2 = generate_total_leads_by_year_fig()
        graph1 = dcc.Graph(figure=fig1)
        graph2 = dcc.Graph(figure=fig2)
        return graph1, graph2

'''
@app.callback(
    Output('leads-div-1', 'children'),
    Output('leads-div-2', 'children'),
    Output('leads-div-3', 'children'),
    Input('leads-trigger-1', 'children'),
    Input('leads-switches-1', 'value'))
def show_options_for_lead(trigger, switch_value):
    if trigger is None:
        if 'lead' in switch_value:
            first = dbc.Checklist(
                    options=[
                        {'label':'Zainteresowani', 'value':'Zainteresowany'},
                        {'label':'Wstępny', 'value':'Wstępny'},
                        {'label':'Akcja zaczepna', 'value':'Akcja zaczepna'},
                        {'label':'Niezainteresowani', 'value':'Niezainteresowani'},
                        {'label':'Wstrzymani', 'value':'Wstrzymany'},
                        {'label':'Zamknięty', 'value':'Zamknięty'}
                    ],
                    value=['Zainteresowany', 'Wstępny', 'Akcja zaczepna', 'Niezainteresowani', 'Wstrzymany', 'Zamknięty'],
                    id='leads-switches-2',
                    switch=True,  
                )
            second = dbc.Checklist(
                options=[
                    {'label':'Wysoki', 'value':'Wysoki'},
                    {'label':'Średni', 'value':'Średni'},
                    {'label':'Niski', 'value':'Niski'},
                    {'label':'Bardzo niski', 'value':'Bardzo niski'},
                    
                ],
                value=['Wysoki', 'Średni', 'Niski', 'Bardzo niski'],
                id='leads-switches-3',
                switch=True,
                
            )
            third = dbc.Checklist(
                options=[
                    {'label':'Dystrybutor', 'value':'DIST'},
                    {'label':'Instalator', 'value':'INST'},
                    {'label':'OEM', 'value':'OEM'},
                    {'label':'Projektant', 'value':'DSGN'},
                    {'label':'Użytkownik końcowy', 'value':'USER'}
                ],
                value=['DIST', 'INST', 'OEM', 'DSGN', 'USER'],
                id='leads-switches-4',
                switch=True,
            )
            return first, second, third
        else:
            first = dbc.Checklist(
                    options=[
                        {'label':'Zainteresowani', 'value':'Zainteresowany', 'disabled':True},
                        {'label':'Wstępny', 'value':'Wstępny', 'disabled':True},
                        {'label':'Akcja zaczepna', 'value':'Akcja zaczepna', 'disabled':True},
                        {'label':'Niezainteresowani', 'value':'Niezainteresowani', 'disabled':True},
                        {'label':'Wstrzymani', 'value':'Wstrzymany', 'disabled':True},
                        {'label':'Zamknięty', 'value':'Zamknięty', 'disabled':True}
                    ],
                    value=[],
                    id='leads-switches-2',
                    switch=True,                    
                )
            second = dbc.Checklist(
                options=[
                    {'label':'Wysoki', 'value':'Wysoki', 'disabled':True},
                    {'label':'Średni', 'value':'Średni', 'disabled':True},
                    {'label':'Niski', 'value':'Niski', 'disabled':True},
                    {'label':'Bardzo niski', 'value':'Bardzo niski', 'disabled':True},
                ],
                value=[],
                id='leads-switches-3',
                switch=True,
            )

            third = dbc.Checklist(
                options=[
                    {'label':'Dystrybutor', 'value':'DIST', 'disabled':True},
                    {'label':'Instalator', 'value':'INST', 'disabled':True},
                    {'label':'OEM', 'value':'OEM', 'disabled':True},
                    {'label':'Projektant', 'value':'DSGN', 'disabled':True},
                    {'label':'Użytkownik końcowy', 'value':'USER', 'disabled':True}
                ],
                value=[],
                id='leads-switches-4',
                switch=True,
            )    
            return first, second, third
'''

@app.callback(
    Output('leads-div-4', 'children'),
    Input('leads-tabs', 'active_tab'),
    Input('leads-radio-1', 'value'),
    Input('leads-switches-1', 'value'),
    Input('leads-dropdown-1', 'value') #Input('leads-switches-2', 'value'),Input('leads-switches-3', 'value'),Input('leads-switches-4', 'value')
    )
def show_data(tab, main_representative, switch_values, countries): #, stages, potentials, corporate_forms
    if tab == 'leads-tab-2':
        df = get_companies_from_clients_and_leads_by_country_data(main_representative, switch_values, countries) # , stages, potentials, corporate_forms
        return dash_table.DataTable(
            id='leads-datatable-1',
            columns=[{'name':i, 'id':i} for i in df.columns if i != 'id'],
            data = df.to_dict('records'),
            page_action="native",
            page_current= 0,
            page_size= 10,
            sort_action="native",
            style_as_list_view=True,
            style_table={'height': '325px'},
            style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                },
            style_cell={'textAlign': 'left',
                        'fontSize': 14},
            style_data_conditional =[{
            'if': {
                'filter_query': '{potential_id} = "Wysoki"'
            },
            'backgroundColor': 'orange', 'opacity':0.5}]
        )
       
@app.callback(
    Output('leads-div-5', 'children'),
    Input('leads-datatable-1', 'active_cell'))
def show_activities_by_company_lead_number(active_cell):
    if active_cell is None:
        raise PreventUpdate
    company_id = active_cell['row_id']
    df = get_activities_by_company_lead_number(company_id)
    return dash_table.DataTable(
            id='22',
            columns=[{'name':i, 'id':i} for i in df.columns if i != 'id'],
            data = df.to_dict('records'),
            page_action="native",
            page_current= 0,
            page_size= 5,
            style_as_list_view=True,
            style_header={
                    'backgroundColor': 'rgb(247, 247, 247)',
                    'fontWeight': 'bold'
                },
            style_cell={
                'textAlign': 'left',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth': 5,
                'fontSize': 14,
                },
            style_data={
                'backgroundColor':'rgb(247, 247, 247)'
            },
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in df.to_dict('records')
            ],
            tooltip_duration=None,
        )           
         

@app.callback(
    Output('leads-div-6', 'children'),
    Input('leads-radio-1', 'value'))
def show_leads(main_representative):
    list_nan = prepare_leads_data(main_representative)
    return html.Div([
        html.H3('Lista firm bez przypisanego statusu:'),
        html.Div(list_nan)
    ])


@app.callback(
    Output('leads-page-four-div-1', 'children'),
    Input('leads-tabs', 'active_tab'),
    Input('leads-page-four-radio-1', 'value'))
def show_leads_statistics(tab, value):
    if tab=='leads-tab-4':
        figure = generate_funnel_graph(value)
        return dcc.Graph(figure=figure)


# Timing page callbacks
@app.callback(
    Output('timing-div-1', 'children'),
    Input('timing-trigger-1', 'children'))
def show_timing_graph(trigger):
    if trigger == None:
        return dbc.Card([
            dbc.CardHeader('Potwierdzane terminy'),
            dbc.CardBody(
                dcc.Graph(
                    figure=generate_delivery_data_fig()
                )
            )
        ])







# Report page activities
@app.callback(
    [Output('report-date_picker-1', 'start_date'), 
    Output('report-date_picker-1', 'end_date'),
    Output('report-date_picker-1', 'max_date_allowed')], 
    [Input('test', 'children')])
def updateDataPicker(value):
    if value == None:
        start_date = datetime.now().date() - timedelta(weeks=4)
        end_date = date.today()
        max_date_allowed = date.today()
    return start_date, end_date, max_date_allowed

@app.callback(
    Output('report-div-1', 'children'),
    [Input('report-radio-1', 'value'),
     Input('report-switches-1', 'value'),
     Input('report-date_picker-1', 'start_date'),
     Input('report-date_picker-1', 'end_date')])
def show_report(main_representative, switches, start_date, end_date):
    start_date = start_date.replace('-','')
    end = datetime.fromisoformat(end_date).date() + timedelta(days=1)
    end_date = str(end).replace('-', '')
    df = get_all_activities(main_representative, switches, start_date, end_date)

    return dash_table.DataTable(
        columns=[{'name':i, 'id':i} for i in df.columns],
        data = df.to_dict('records'),
        style_as_list_view=True,
        style_header={
        'backgroundColor': 'black',
        'fontWeight': 'bold',
        'color':'white'},
        style_cell={
                'textAlign': 'left',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth': 5,
                },
        tooltip_data=[
            {
                column: {'value': str(value), 'type': 'markdown'}
                for column, value in row.items()
            } for row in df.to_dict('records')
        ],
        tooltip_duration=None,
        style_data_conditional=[
        {
            'if': {
                'filter_query': '{Rodzaj działania} contains "Oferta"'
            },
            'backgroundColor': '#ced4da',
        },
        {
            'if': {
                'filter_query': '{Rodzaj działania} contains "Nowy lead"'
            },
            'backgroundColor': '#FFC300',
        },
        {
            'if': {
                'filter_query': '{Rodzaj działania} contains "Zadanie"'
            },
            'backgroundColor': '#003566',
            'color':'white'
        },
        {
            'if': {
                'filter_query': '{Rodzaj działania} contains "Klient"'
            },
            'backgroundColor': '#27a300',
        },
        {
            'if': {
                'filter_query': '{Rodzaj działania} contains "Potencjalny klient"'
            },
            'backgroundColor': '#5bba6f',
        },
        {
            'if': {
                'filter_query': '{Rodzaj działania} contains "Spotkanie"'
            },
            'backgroundColor': '#ba0c0c',
        }]
        )
            

# Conditions page callbacks
@app.callback(
    Output('conditions-1-div', 'children'),
    Input('conditions-1-trigger', 'children'))
def generate_radio_with_regions(trigger):
    if trigger == None:
        return dbc.RadioItems(
            options=[{"label": 'All', "value": 'All'}]+[{"label": i, "value": i} for i in get_unique_regions()['district_code']],
            value='All',
            id="conditions-radioitems-input",
            inline=True
        )

@app.callback(
    Output('conditions-2-div', 'children'),
    Input('conditions-radioitems-input', 'value'))
def generate_table_with_conditions(region):
    df = prepare_data_for_conditions_table(region) 
    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'))


# New sales by region callbacks
@app.callback(
    Output('new-sales-by-region-div-1', 'children'),
    Input('new-sales-by-region-trigger', 'children'))
def generate_new_sales_graph_total(trigger):
    if trigger == None:
        fig = generetate_total_new_sales_and_products_from_current_year()
        return dcc.Graph(figure=fig)

@app.callback(
    Output('new-sales-by-region-div-2', 'children'),
    Input('new-sales-by-region-trigger', 'children'))
def generate_new_sales_graph(trigger):
    if trigger == None:
        fig = generate_new_sales_and_products_from_current_year_by_region_graph()
        return dcc.Graph(figure=fig)

@app.callback(
    Output('new-sales-by-region-div-3', 'children'),
    Input('new-sales-by-region-trigger', 'children'))
def generate_radio_with_regions(trigger):
    if trigger == None:
        return dbc.RadioItems(
            options=[{"label": 'All', "value": 'All'}]+[{"label": i, "value": i} for i in get_unique_regions()['district_code']],
            value='All',
            id="new-sales-by-region-radio-1",
            inline=True
        )

@app.callback(
    Output('new-sales-fig-1', 'figure'),
    Output('new-sales-fig-2', 'figure'),
    Input('new-sales-by-region-radio-1', 'value'))
def generate_radio_with_regions(region):
    fig1, fig2 = generate_graphs_for_region_view(region)
    return fig1, fig2
    
    
# Offers main page callbacks
@app.callback(
    Output('offers-main-div-1', 'children'),
    Input('offers-main-trigger-1', 'children'))
def show_offers_map_graph(trigger):
    if trigger == None:
        return dcc.Graph(id='offers-main-fig-1', figure=generate_offers_map_fig()) 



@app.callback(
    Output('offers-main-div-3', 'children'),
    Input('offers-main-fig-1', 'clickData'))
def show_offers_activity_graph(data):
    if data is None:
        raise PreventUpdate
    else:
        print(data['points'][0]['location'])

@app.callback(
    Output('offers-main-div-2', 'children'),
    Input('offers-main-trigger-1', 'children'))
def show_offers_map_graph(trigger):
    if trigger == None:
        df = prepare_offers_data_by_iso_country()
        df = df.sort_values(by='net_value', ascending=False)
        df['net_value'] = round(df['net_value']/1000, 3)
        return html.Div(
            dash_table.DataTable(
                    columns=[{'name':i, 'id':i} for i in df.columns],
                    data = df.to_dict('records'),
                    style_as_list_view=True,
                    style_cell={'textAlign': 'left'},
                    style_header = {'backgroundColor': 'rgb(230, 230, 230)',
                                    'fontWeight': 'bold'},
                    page_action="native",
                    page_current= 0,
                    page_size= 12,
                )
        )



@app.callback(
    Output('offers-main-div-4', 'children'),
    Input('offers-main-trigger-1', 'children'))
def show_offers_activity_graph(trigger):
    if trigger == None:
        return dcc.Graph(figure=generate_offers_activitity_fig())    
    

# Order book page callbacks
@app.callback(
    Output('order-book-div-1', 'children'),
    Input('order-book-trigger', 'children'))
def generate_current_sales_and_wallet_situation_graph(trigger):
    if trigger == None:
        return dcc.Graph(figure=generate_order_book_in_time_with_options_fig())

@app.callback(
    Output('order-book-div-2', 'children'),
    Input('order-book-trigger', 'children'))
def generate_second_graph(trigger):
    if trigger == None:
        return dcc.Graph(figure=generate_order_book_by_month_fig())

if __name__ == '__main__':
    app.run_server(host = '0.0.0.0', port = 8080)