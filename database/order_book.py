import pandas as pd
import plotly.graph_objects as go
from datetime import date
import plotly.express as px

def generate_order_book_in_time_with_options_fig():
    eastern = ['ADL ru','AQUATECHING ua','CZYSTYJ BEREG ru','ETNA ua','EUROSTEP ru','KPSR GROUP by',
    'SANTECH ru','TEPLOSILA by','VOGEZENERGO by','LAODON GROUP by','BTM by','CZYSTYJ BIEREG by',  
    'INOXTRADE by','ZETKAMA RUS','LPG TECHNO ua','LAODON by','KOMPENSATOR by','PROMTEHSINTEZ ua']

    df = pd.read_feather('/home/pkulakow/workspace/scheduler-wallet/wallet_value_by_day.feather')
    
    total_wallet = df.groupby('current_time').agg({'net_value':'sum'}).reset_index()
    wallet_without_eastern = df[~df['customer_name'].isin(eastern)].groupby('current_time').agg({'net_value':'sum'}).reset_index()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=total_wallet['current_time'],
        y=total_wallet['net_value'],
        name='Razem',
        marker_color='darkblue'
    ))

    fig.add_trace(go.Scatter(
        x=wallet_without_eastern['current_time'],
        y=wallet_without_eastern['net_value'],
        name='Bez Wschodu',
        marker_color='lightgray'
    ))

    fig.update_layout(template='plotly_white')

    return fig

def generate_order_book_in_time_fig():

    df = pd.read_feather('/home/pkulakow/workspace/scheduler-wallet/wallet_value_by_day.feather')
    total_order_book = df

    #total_order_book = df.groupby('current_time').agg({'net_value':'sum'}).reset_index()
    smax = total_order_book.iloc[total_order_book['net_value'].idxmax(),:].to_frame().T
    smax['text'] = smax['net_value'] / 1000000
    #smax['text'] = smax['text'].round(3)
    smin = total_order_book.iloc[total_order_book['net_value'].idxmin(),:].to_frame().T
    smin['text'] = smin['net_value'] / 1000000
    last = total_order_book.iloc[-1,:].to_frame().T
    #last['text'] = last['net_value'] / 1000000

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=total_order_book['current_time'],
        y=total_order_book['net_value'],
        name='Razem',
        marker_color='darkblue'
    ))
    fig.add_trace(go.Scatter(
        x=smax['current_time'],
        y=smax['net_value'],
        mode='text',
        text = smax['net_value'],
        textposition = 'top center',
        textfont = dict(color='darkblue'),
        texttemplate = '%{text:.2s}'
    ))
    fig.add_trace(go.Scatter(
        x=smin['current_time'],
        y=smin['net_value'],
        mode='text',
        text = smin['net_value'],
        textposition = 'bottom center',
        textfont = dict(color='darkblue'),
        texttemplate = '%{text:.2s}'
    ))
    fig.add_trace(go.Scatter(
        x=last['current_time'],
        y=last['net_value'],
        mode='text',
        text = last['net_value'],
        textposition = 'middle right',
        textfont = dict(color='orange'),
        texttemplate = '%{text:.2s}'
    ))


    fig.update_layout(
        modebar_add=["v1hovermode", "toggleSpikeLines"],
        template='plotly_white',
        height=300,
        margin=dict(l=1, r=1, b=10, t=20),
        showlegend=False
        )
    fig.update_xaxes(tickfont=dict(color='gray'), showgrid=False),
    fig.update_yaxes(tickfont=dict(color='gray'), showgrid=False, showticklabels=False)
  

    return fig

def generate_order_book_by_month_fig():
    
    df = pd.read_feather('/home/pkulakow/workspace/scheduler-wallet/everyday_wallet.feather')

    df = df[df['current_time']==date.today()]

    df_wanted = df[['wanted_delivery_date', 'net_value']]
    df_wanted  = df_wanted.set_index('wanted_delivery_date')
    df_wanted  = df_wanted.resample('M').sum()
    df_wanted  = df_wanted.reset_index()

    df_promised = df[['promised_delivery_date', 'net_value']]
    df_promised = df_promised.set_index('promised_delivery_date')
    df_promised = df_promised.resample('M').sum()
    df_promised = df_promised.reset_index()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_wanted['wanted_delivery_date'],
        y=df_wanted['net_value'],
        marker_color='darkblue',
        name='Wymagane'
    ))

    fig.add_trace(go.Bar(
        x=df_promised['promised_delivery_date'],
        y=df_promised['net_value'],
        marker_color='orange',
        name='Obiecana'
    ))
    
    fig.update_layout(template='plotly_white', barmode='group')
    fig.update_xaxes(showgrid=False, dtick="M1", tickformat="%b\n%Y")

    return fig

def testtest():
    df = pd.read_feather('/home/pkulakow/workspace/scheduler-wallet/everyday_wallet.feather', columns=['customer_name', 'order_no', 'catalog_no', 'net_value', 'date_entered', 'current_time', 'promised_delivery_date'])
    df = df[df['current_time']==date.today()]
    df = df[['customer_name', 'net_value', 'order_no', 'catalog_no', 'date_entered', 'promised_delivery_date']]
    df['date_entered'] = pd.to_datetime(df['date_entered'])
    df['diff'] = df['promised_delivery_date'] - df['date_entered']
    df['diff'] = df['diff'].dt.days
    fig = px.histogram(df, 'diff')
    fig.update_layout(template='plotly_white')
    return fig
