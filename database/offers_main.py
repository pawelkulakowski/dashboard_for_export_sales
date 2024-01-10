import pandas as pd
import datetime

import time
import plotly.graph_objects as go
import plotly.express as px

from database.database_connection import engine

def get_active_offers_by_customer_name():
    current_year = datetime.datetime.today().year
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT ifsapp.customer_info.name, ifsapp.order_quotation.quotation_no, ifsapp.Order_Quotation_API.Get_Total_Sale_Price__(QUOTATION_NO) \
    FROM ifsapp.order_quotation \
    INNER JOIN ifsapp.customer_info \
    ON ifsapp.order_quotation.customer_no = ifsapp.customer_info.customer_id \
    WHERE ifsapp.order_quotation.customer_no like 'E%' \
    AND ifsapp.order_quotation.state = 'Aktywowane' \
    AND ifsapp.order_quotation.contract = 'Z01' \
    AND ifsapp.order_quotation.date_entered >= to_date('{current_year}0101', 'YYYYMMDD')", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    df = df.rename(columns={'IFSAPP.ORDER_QUOTATION_API.GET_TOTAL_SALE_PRICE__(QUOTATION_NO)':'net_value',
                            'name':'customer_name'})
    df['country'] = df['customer_name'].str[-2:].str.upper()
    return df




def get_countries():
    countries = pd.read_html('https://pl.wikipedia.org/wiki/ISO_3166-1')[0]
    countries = countries[['kod alfa-2', 'kod alfa-3']]
    countries.columns = ['country', 'iso_alpha']
    return countries

def prepare_offers_data_by_iso_country():
    offers = get_active_offers_by_customer_name()
    countries = get_countries()
    df = pd.merge(left=offers, right=countries, how='left', on='country')
    df = df.groupby('iso_alpha', as_index=False).agg({'net_value':'sum'})
    return df


# Offers
def get_total_offer_by_statuses_from_current_year():
    current_year = datetime.datetime.today().year
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT state, SUM(ifsapp.Order_Quotation_API.Get_Total_Sale_Price__(QUOTATION_NO)) \
    FROM IFSAPP.order_quotation \
    WHERE customer_no like 'E%' \
    AND contract = 'Z01' \
    AND date_entered >= to_date('20220101', 'YYYYMMDD') \
    AND state NOT IN ('Zamknięte', 'Anulowane') \
    GROUP by state \
    ORDER by state", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    df = df.rename(columns={'SUM(IFSAPP.ORDER_QUOTATION_API.GET_TOTAL_SALE_PRICE__(QUOTATION_NO))':'net_value'})
    return df

def get_total_win_lost_offers_from_current_year():
    current_year = datetime.datetime.today().year
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT closed_status, SUM(ifsapp.Order_Quotation_API.Get_Total_Sale_Price__(QUOTATION_NO)) \
    FROM IFSAPP.order_quotation \
    WHERE customer_no like 'E%' \
    AND contract = 'Z01' \
    AND date_entered >= to_date('{current_year}0101', 'YYYYMMDD') \
    AND closed_status IS NOT NULL \
    AND closed_status <> 'Brak decyzji' \
    GROUP BY closed_status", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    df = df.rename(columns={'SUM(IFSAPP.ORDER_QUOTATION_API.GET_TOTAL_SALE_PRICE__(QUOTATION_NO))':'net_value'})
    return df

# Ograniczeni do sales agentow
def get_offers_by_date_from_current_year():
    current_year = datetime.datetime.today().year
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT date_entered, ifsapp.Order_Quotation_API.Get_Total_Sale_Price__(QUOTATION_NO) \
    FROM  IFSAPP.order_quotation \
    WHERE customer_no like 'E%' \
    AND contract = 'Z01' \
    AND quotation_no like 'S%' \
    AND date_entered >= to_date('{current_year}0101', 'YYYYMMDD') \
    AND state <> 'Anulowane' \
    AND salesman_code in ('AOLSZEWS', 'HGLADYSZ', 'DSTUKUS', 'DSUJEWIC', 'OMARCHEN', 'MBIEZYNS', 'PILNICKI', 'PKULAKOW', 'ADUDKA', 'AGOLEBIO')", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    df = df.rename(columns={'IFSAPP.ORDER_QUOTATION_API.GET_TOTAL_SALE_PRICE__(QUOTATION_NO)':'net_value'})
    df['date_entered'] = df['date_entered'].dt.date 
    df = df.groupby('date_entered', as_index=False).agg({'net_value':'sum'}).sort_values(by='date_entered')
    return df

def prepare_offers_data():
    df = pd.read_feather('database/data/offers_by_date_till_2021_end.feather')
    df2 = get_offers_by_date_from_current_year()
    df = df.append(df2)
    df['date_entered'] = pd.to_datetime(df['date_entered'])
    return df


def generate_offers_total_fig():
    df = get_total_offer_by_statuses_from_current_year()
    value_activated = df[df['state']=='Aktywowane']['net_value'].values[0]
    value_corrected = df[df['state']=='Skorygowane']['net_value'].values[0]
    value_planned = df[df['state']=='Zaplanowane']['net_value'].values[0]

    df = get_total_win_lost_offers_from_current_year()
    value_won = df[df['closed_status']=='Wygrane']['net_value'].values[0]
    value_lost = df[df['closed_status']=='Przegrane']['net_value'].values[0]

    fig = go.Figure(
        data=go.Pie(
            labels=['Aktywowane', 'Skorygowane', 'Zaplanowane', 'Wygrane', 'Przegrane'],
            values=[value_activated, value_corrected, value_planned, value_won, value_lost],
            hole=.7,
            marker_colors=['darkblue', 'darkgray', 'lightgray', 'green', 'red' ],
            textposition = 'inside'

        ),
        layout=go.Layout(
                annotations=[{'text': "&#8364;"+str(round(value_activated/1000000,3))+"M", 'x':0.50, 'y':0.5, 'font_size':14, 'showarrow':False}],
                showlegend=False,
                title='',
                height=150
                
            )
    )

    fig.update_layout(
        margin=dict(
        l=2,
        r=2,
        b=2,
        t=2    
        ))

    #fig.update_traces(textinfo='none')

    return fig

def generate_offers_activitity_fig():
    df = prepare_offers_data()
    df = df.set_index('date_entered')
    df = df.resample('W').sum().rolling(9).sum()

    fig = px.line(df, x=df.index, y='net_value', color_discrete_sequence=['darkblue'])

    fig.add_vrect(x0='2019-01-01', x1='2019-07-01', line_width=0, fillcolor="lightgray", opacity=0.2)
    fig.add_vrect(x0='2020-01-01', x1='2020-07-01', line_width=0, fillcolor="lightgray", opacity=0.2)
    fig.add_vrect(x0='2021-01-01', x1='2021-07-01', line_width=0, fillcolor="lightgray", opacity=0.2)
    fig.add_vrect(x0='2022-01-01', x1='2022-07-01', line_width=0, fillcolor="lightgray", opacity=0.2)

    fig.update_layout(legend=dict(
        yanchor="top",
        y=1.1,
        xanchor="left",
        x=-0.04,
        orientation='h'
    ), template='plotly_white')

    fig.update_xaxes(title='', showgrid=False, 
                    tickfont=dict(color='gray'),
                    title_font=dict(color='gray'))
    fig.update_yaxes(title ='', showgrid=False,
                    tickfont=dict(color='gray'),
                    title_font=dict(color='gray'), range=[0,8000000])

    fig.add_annotation(x='2019-01-01', y=8000000,
                text="I półrocze 2019",
                showarrow=False,
                yshift=-10,
                xshift=50,
                font={'color':'gray', 'size':10})

    fig.add_annotation(x='2020-01-01', y=8000000,
                text="I półrocze 2020",
                showarrow=False,
                yshift=-10,
                xshift=50,
                font={'color':'gray', 'size':10})

    fig.add_annotation(x='2021-01-01', y=8000000,
                text="I półrocze 2021",
                showarrow=False,
                yshift=-10,
                xshift=50,
                font={'color':'gray', 'size':10})

    fig.add_annotation(x='2022-01-01', y=8000000,
                text="I półrocze 2022",
                showarrow=False,
                yshift=-10,
                xshift=50,
                font={'color':'gray', 'size':10})

    return fig


def generate_offers_map_fig():
    
    data = prepare_offers_data_by_iso_country()
    fig = go.Figure(data=go.Choropleth(
        locations=data['iso_alpha'],
        z = data['net_value'],
        colorscale = 'Blues',
        autocolorscale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix = '$',
    ))
    fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular',
        
    ))

    fig.update_layout(
        margin=dict(
        l=10,
        r=10,
        b=10,
        t=10,
    ),
    showlegend=False)

    return fig