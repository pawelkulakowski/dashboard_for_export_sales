
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

from database.database_connection import engine


def get_orders_by_year_quarter_month_from_current_year():
    current_year = datetime.today().year
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT date_entered, ifsapp.Customer_Order_Line_API.Get_Sale_Price_Total(ORDER_NO, LINE_NO, REL_NO, LINE_ITEM_NO) \
    FROM IFSAPP.customer_order_join_cfv \
    WHERE contract = 'Z01' \
    AND customer_no LIKE 'E%' \
    AND objstate <> (SELECT ifsapp.CUSTOMER_ORDER_LINE_API.FINITE_STATE_ENCODE__('Anulowane') from dual) \
    AND date_entered >= to_date('{current_year}0101', 'YYYYMMDD') \
    AND (upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'A%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'B%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'C%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'D%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'E%' )) \
    AND CF$_NR_RMA IS NULL", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    if not df.empty:
        df = df.rename(columns={'IFSAPP.CUSTOMER_ORDER_LINE_API.GET_SALE_PRICE_TOTAL(ORDER_NO,LINE_NO,REL_NO,LINE_ITEM_NO)':'net_value'})
        df['year'] = df['date_entered'].dt.year
        df['quarter'] = df['date_entered'].dt.quarter
        df['month'] = df['date_entered'].dt.month
        df = df.groupby(['year', 'quarter', 'month'], as_index=False)['net_value'].sum().sort_values(by=['year', 'quarter', 'month'], ascending=True)
    else:
        df = pd.DataFrame(columns=['year', 'quarter', 'month', 'net_value'])
    return df

def prepare_orders_by_year_quarter_month():
    df_1 = pd.read_feather('database/data/orders_by_year_quarter_month_till_2021_end.feather')
    df_1 = df_1.drop(columns=['index'])
    df_2 = get_orders_by_year_quarter_month_from_current_year()
    df = df_1.append(df_2)
    return df
    
def generate_orders_by_year_fig():
    df = prepare_orders_by_year_quarter_month()
    years = [i for i in df['year'].unique()]

    df = df.groupby(['year'], as_index=False)['net_value'].sum().sort_values(by=['year'], ascending=True)
    colors = ['lightgray', 'lightgray', 'lightgray', 'lightgray', 'orange']
    fig = go.Figure()
    
    x = 0
    for year in years:
        fig.add_trace(go.Bar(
            x = df[df['year']==year]['year'],
            y = df[df['year']==year]['net_value'],
            name=str(year),
            marker_color = colors[x],
            text = df[df['year']==year]['net_value'],
            textposition = 'outside',
            texttemplate='%{text:.2s}'
        ))
        x +=1
    
    fig.update_layout(template='plotly_white')
    fig.update_xaxes(dtick=1)

    

    return fig


def generate_orders_by_quarter_fig():
    df = prepare_orders_by_year_quarter_month()
    years = [i for i in df['year'].unique()]

    df = df.groupby(['year', 'quarter'], as_index=False)['net_value'].sum().sort_values(by=['year', 'quarter'], ascending=True)
    colors = ['lightgray', 'lightgray', 'lightgray', 'lightgray', 'orange']
    fig = go.Figure()
    
    x = 0
    for year in years:
        fig.add_trace(go.Bar(
            x = df[df['year']==year]['quarter'],
            y = df[df['year']==year]['net_value'],
            name=str(year),
            marker_color = colors[x],
            text = df[df['year']==year]['net_value'],
            textposition = 'outside',
            texttemplate='%{text:.2s}'
        ))
        x +=1
    
    fig.update_layout(template='plotly_white')
    fig.update_xaxes(dtick=1)

    return fig

def generate_orders_by_month_fig():
    df = prepare_orders_by_year_quarter_month()
    years = [i for i in df['year'].unique()]

    df = df.groupby(['year', 'month'], as_index=False)['net_value'].sum().sort_values(by=['year', 'month'], ascending=True)
    colors = ['lightgray', 'lightgray', 'lightgray', 'lightgray', 'orange']
    fig = go.Figure()
    
    x = 0
    for year in years:
        fig.add_trace(go.Bar(
            x = df[df['year']==year]['month'],
            y = df[df['year']==year]['net_value'],
            name=str(year),
            marker_color = colors[x],
            text = df[df['year']==year]['net_value'],
            textposition = 'outside',
            texttemplate='%{text:.2s}'
        ))
        x +=1
    
    fig.update_layout(template='plotly_white')
    fig.update_xaxes(dtick=1)

    return fig


'''df = prepare_orders_by_year_quarter_month()
df = df.groupby(['year', 'quarter'], as_index=False)['net_value'].sum().sort_values(by=['year', 'quarter'], ascending=True)
df = df[df['quarter']==1]
#df['color'] = df['net_value'] < df.iloc[-1,-1]
df.loc[(df['net_value'] < df.iloc[-1,-1]), 'color'] = 'green'
df.loc[(df['net_value'] > df.iloc[-1,-1]), 'color'] = 'red'

#eksport.loc[(eksport['Nr zam./Nr zlec.']=='S2100422') & (eksport['short_index']=='630A'), 'typ_sprzedazy'] = 'Rozszerzenie oferty'

print(df)'''