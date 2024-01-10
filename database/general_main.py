import pandas as pd
import datetime

import time
import plotly.graph_objects as go
import plotly.express as px

from database.database_connection import engine

def getDateRangeFromWeek(year,cw):
    if year in (2019, 2020):
        cw -= 1
    firstdayofweek = datetime.datetime.strptime(f'{year}-W{int(cw)}-1', "%Y-W%W-%w").date()
    lastdayofweek = firstdayofweek + datetime.timedelta(days=6.9)
    firstdayofweek = firstdayofweek.strftime('%Y%m%d')
    lastdayofweek = lastdayofweek.strftime('%Y%m%d')
    return firstdayofweek, lastdayofweek


# Sales / Wallet
def get_total_sales_data_from_current_year():
       current_year = datetime.datetime.today().year
       connection = engine.connect()
       sql_query = pd.read_sql_query(f"SELECT SUM(net_curr_amount) \
       FROM ifsapp.CUSTOMER_ORDER_INV_JOIN_cfv \
       WHERE invoice_date >=to_date( '{current_year}0101', 'YYYYMMDD' ) \
       AND client_state <> 'Anulowana' \
       AND contract = 'Z01' \
       AND identity like upper('E%') \
       AND rma_no is null \
       AND (upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'A%' ) \
       OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'B%' ) \
       OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'C%' ) \
       OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'D%' ) \
       OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'E%' ))", engine)
       
       df = pd.DataFrame(sql_query)
       connection.close()
       df = df.rename(columns={'SUM(NET_CURR_AMOUNT)':'net_value'})
       return df

def get_sales_data_from_current_year():
       current_year = datetime.datetime.today().year
       connection = engine.connect()
       sql_query = pd.read_sql_query(f"SELECT invoice_date, SUM(net_curr_amount) \
       FROM ifsapp.CUSTOMER_ORDER_INV_JOIN_cfv \
       WHERE invoice_date >=to_date( '{current_year}0101', 'YYYYMMDD' ) \
       AND client_state <> 'Anulowana' \
       AND contract = 'Z01' \
       AND identity like upper('E%') \
       AND rma_no is null \
       AND (upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'A%' ) \
       OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'B%' ) \
       OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'C%' ) \
       OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'D%' ) \
       OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'E%' )) \
       GROUP BY invoice_date \
       ORDER BY invoice_date", engine)
       
       df = pd.DataFrame(sql_query)
       connection.close()
       df = df.rename(columns={'SUM(NET_CURR_AMOUNT)':'net_value'})
       df = df.set_index('invoice_date')
       df = df.resample('W').sum()
       df['year'] = df.index.year
       df['cw'] = df.index.isocalendar().week
       df = df.reset_index()
       df = df[['year', 'cw', 'net_value']]
       df['year'] = df['year'].astype('category')
       df['cw'] = df['cw'].astype('category')
       return df

def get_sales_data_from_current_year_by_month():
       current_year = datetime.datetime.today().year
       connection = engine.connect()
       sql_query = pd.read_sql_query(f"SELECT invoice_date, SUM(net_curr_amount) \
       FROM ifsapp.CUSTOMER_ORDER_INV_JOIN_cfv \
       WHERE invoice_date >=to_date( '{current_year}0101', 'YYYYMMDD' ) \
       AND client_state <> 'Anulowana' \
       AND contract = 'Z01' \
       AND identity like upper('E%') \
       AND rma_no is null \
       AND (upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'A%' ) \
       OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'B%' ) \
       OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'C%' ) \
       OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'D%' ) \
       OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'E%' )) \
       GROUP BY invoice_date \
       ORDER BY invoice_date", engine)
       
       df = pd.DataFrame(sql_query)
       connection.close()
       df = df.rename(columns={'SUM(NET_CURR_AMOUNT)':'net_value'})
       df = df.set_index('invoice_date')
       df = df.resample('M').sum()
       df['year'] = df.index.year
       df['month'] = df.index.month
       df = df.reset_index()
       df = df[['year', 'month', 'net_value']]
       df['year'] = df['year'].astype('category')
       df['month'] = df['month'].astype('category')
       return df

def get_total_order_book():   
    connection = engine.connect()    
    sql_query = pd.read_sql_query("SELECT sum((BUY_QTY_DUE - QTY_INVOICED)*ifsapp.Customer_Order_Line_API.Get_Sale_Price_Total(ORDER_NO, LINE_NO, REL_NO, LINE_ITEM_NO)/BUY_QTY_DUE) \
    FROM IFSAPP.customer_order_join \
    WHERE contract = 'Z01' \
    AND ORDER_NO like 'S%' \
    AND customer_no like upper('E%') \
    AND objstate <> (SELECT ifsapp.CUSTOMER_ORDER_LINE_API.FINITE_STATE_ENCODE__('Anulowane') from dual) \
    AND objstate <> (SELECT ifsapp.CUSTOMER_ORDER_LINE_API.FINITE_STATE_ENCODE__('Zafakturowane/Zamknięte') from dual) \
    AND objstate <> (SELECT ifsapp.CUSTOMER_ORDER_LINE_API.FINITE_STATE_ENCODE__('Dostarczone') from dual) \
    AND (upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'A%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'B%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'C%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'D%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'E%' ))", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df.iloc[0,0]

'''def get_wallet_from_current_year_by_month():
       current_year = datetime.datetime.today().year   
       connection = engine.connect()    
       sql_query = pd.read_sql_query(f"SELECT date_entered, (BUY_QTY_DUE - QTY_INVOICED)*ifsapp.Customer_Order_Line_API.Get_Sale_Price_Total(ORDER_NO, LINE_NO, REL_NO, LINE_ITEM_NO)/BUY_QTY_DUE \
       FROM IFSAPP.customer_order_join \
       WHERE contract = 'Z01' \
       AND ORDER_NO like 'S%' \
       AND customer_no like upper('E%') \
       AND objstate <> (SELECT ifsapp.CUSTOMER_ORDER_LINE_API.FINITE_STATE_ENCODE__('Anulowane') from dual) \
       AND date_entered >= to_date('{current_year}0101', 'YYYYMMDD') \
       AND (upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'A%' ) \
       OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'B%' ) \
       OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'C%' ) \
       OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'D%' ) \
       OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'E%' ))", engine)
       df = pd.DataFrame(sql_query)
       connection.close()
       df = df.rename(columns={'(BUY_QTY_DUE-QTY_INVOICED)*IFSAPP.CUSTOMER_ORDER_LINE_API.GET_SALE_PRICE_TOTAL(ORDER_NO,LINE_NO,REL_NO,LINE_ITEM_NO)/BUY_QTY_DUE':'net_value'})
       df = df.set_index('date_entered')
       df = df.resample('M').sum()
       df['year'] = df.index.year
       df['month'] = df.index.month
       df = df.reset_index()
       df = df[['year', 'month', 'net_value']]
       df['year'] = df['year'].astype('category')
       df['month'] = df['month'].astype('category')
       
       return df'''



# Orders
def get_weekly_order_data_from_current_year():
    current_year = datetime.datetime.today().year
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
        df['cw'] = df['date_entered'].dt.isocalendar().week
        df = df.groupby(['year', 'cw'], as_index=False)['net_value'].sum().sort_values(by=['year', 'cw'], ascending=True)
        df_final = pd.DataFrame(data={'year':[datetime.datetime.today().year for i in range(0,datetime.datetime.today().isocalendar()[1]+1)], 'cw':[i for i in range(0,datetime.datetime.today().isocalendar()[1]+1)]})
        df = pd.merge(left=df_final, right=df, on=['year', 'cw'], how='left')
    else:
        df = pd.DataFrame(columns=['year', 'cw', 'net_value'])
    
    return df

def get_weekly_order_data_from_current_year_incrementing():
    current_year = datetime.datetime.today().year
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
        df['cw'] = df['date_entered'].dt.isocalendar().week
        df = df.groupby(['year', 'cw'], as_index=False)['net_value'].sum().sort_values(by=['year', 'cw'], ascending=True)
        
    else:
        df = pd.DataFrame(columns=['year', 'cw', 'net_value'])
    
    return df


def get_detailed_weekly_orders_by_cw_and_year(year, cw):
    
    firstdayofweek, lastdayofweek = getDateRangeFromWeek(year, cw)

    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT customer_name, SUM(ifsapp.Customer_Order_Line_API.Get_Sale_Price_Total(ORDER_NO, LINE_NO, REL_NO, LINE_ITEM_NO)) \
    FROM IFSAPP.customer_order_join_cfv \
    WHERE contract = 'Z01' \
    AND customer_no LIKE 'E%' \
    AND objstate <> (SELECT ifsapp.CUSTOMER_ORDER_LINE_API.FINITE_STATE_ENCODE__('Anulowane') from dual) \
    AND date_entered >= to_date('{firstdayofweek}', 'YYYYMMDD') \
    AND date_entered <= to_date('{lastdayofweek}', 'YYYYMMDD') \
    AND (upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'A%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'B%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'C%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'D%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'E%' )) \
    AND CF$_NR_RMA IS NULL \
    GROUP BY customer_name", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    df = df.rename(columns={'SUM(IFSAPP.CUSTOMER_ORDER_LINE_API.GET_SALE_PRICE_TOTAL(ORDER_NO,LINE_NO,REL_NO,LINE_ITEM_NO))':'net_value'})
    return df

def get_total_orders_from_current_week():
    cw = datetime.date.today().isocalendar()[1]
    year = datetime.date.today().year
    firstdayofweek, lastdayofweek = getDateRangeFromWeek(year, cw)

    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT SUM(ifsapp.Customer_Order_Line_API.Get_Sale_Price_Total(ORDER_NO, LINE_NO, REL_NO, LINE_ITEM_NO)) \
    FROM IFSAPP.customer_order_join_cfv \
    WHERE contract = 'Z01' \
    AND customer_no LIKE 'E%' \
    AND objstate <> (SELECT ifsapp.CUSTOMER_ORDER_LINE_API.FINITE_STATE_ENCODE__('Anulowane') from dual) \
    AND date_entered >= to_date('{firstdayofweek}', 'YYYYMMDD') \
    AND date_entered <= to_date('{lastdayofweek}', 'YYYYMMDD') \
    AND (upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'A%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'B%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'C%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'D%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'E%' )) \
    AND CF$_NR_RMA IS NULL", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    df = df.rename(columns={'SUM(IFSAPP.CUSTOMER_ORDER_LINE_API.GET_SALE_PRICE_TOTAL(ORDER_NO,LINE_NO,REL_NO,LINE_ITEM_NO))':'net_value'})
    return df

def get_total_orders_from_current_week_previous_day():
    cw = datetime.date.today().isocalendar()[1]
    year = datetime.date.today().year
    firstdayofweek, lastdayofweek = getDateRangeFromWeek(year, cw)

    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT SUM(ifsapp.Customer_Order_Line_API.Get_Sale_Price_Total(ORDER_NO, LINE_NO, REL_NO, LINE_ITEM_NO)) \
    FROM IFSAPP.customer_order_join_cfv \
    WHERE contract = 'Z01' \
    AND customer_no LIKE 'E%' \
    AND objstate <> (SELECT ifsapp.CUSTOMER_ORDER_LINE_API.FINITE_STATE_ENCODE__('Anulowane') from dual) \
    AND date_entered >= to_date('{firstdayofweek}', 'YYYYMMDD') \
    AND date_entered <= to_date('{lastdayofweek}', 'YYYYMMDD') \
    AND (upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'A%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'B%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'C%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'D%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'E%' )) \
    AND CF$_NR_RMA IS NULL", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    df = df.rename(columns={'SUM(IFSAPP.CUSTOMER_ORDER_LINE_API.GET_SALE_PRICE_TOTAL(ORDER_NO,LINE_NO,REL_NO,LINE_ITEM_NO))':'net_value'})
    return df





def prepare_weekly_order_data():
    df_1 = pd.read_feather('database/data/orders_by_year_and_cw_till_2021_end.feather')
    df_2 = get_weekly_order_data_from_current_year()
    df = df_1.append(df_2)
    
    return df

def prepare_weekly_order_data_incrementing():
    df_1 = pd.read_feather('database/data/orders_by_year_and_cw_till_2021_end.feather')
    df_2 = get_weekly_order_data_from_current_year_incrementing()
    df = df_1.append(df_2)
    
    return df

def prepare_sales_data():
       sales_data_from_current_year = get_sales_data_from_current_year()
       sales_data_from_previous_years = pd.read_feather('database/data/sales_by_year_and_cw_till_2021_end.feather')
       sales_data_from_previous_years = sales_data_from_previous_years[sales_data_from_previous_years['year']!=2017]
       df = sales_data_from_previous_years.append(sales_data_from_current_year)
       return df




def generate_current_sales_wallet_situation():
    df_sales = get_total_sales_data_from_current_year()
    sales_value = df_sales['net_value'].values[0]
    wallet_value = get_total_order_book()
    plan = 23800000 - sales_value - wallet_value

    fig = go.Figure(
        data=go.Pie(
            labels=['Sprzedaż', 'Portfel', 'Plan', ],
            values=[sales_value, wallet_value, plan],
            hole=.7,
            marker_colors=['darkblue', 'orange', 'lightgray'],
            textposition = 'inside'

        ),
        layout=go.Layout(
                annotations=[{'text': "&#8364;"+str(round(sales_value/1000000,3))+"M", 'x':0.50, 'y':0.5, 'font_size':14, 'showarrow':False}],
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

    return fig

def generate_total_new_orders_from_current_week():
    df = get_total_orders_from_current_week()

    fig = go.Figure(
        go.Indicator(
            mode = "number+delta",
            value = round(df['net_value'].values[0]/1000,2),
            number = {'prefix': "&#8364;"},
            delta = {'position': "top", 'reference': 320},
            domain = {'x': [0, 1], 'y': [0, 1]}))

    fig.update_layout(
        margin=dict(
        l=10,
        r=10,
        b=10,
        t=10    
        ),
        height=150)

    return fig




def generate_sales_data_bar_fig():
       sales_by_year = prepare_sales_data()
       today_cw = datetime.date.today().isocalendar()[1]
       current_year = datetime.datetime.today().year   


       sales_by_year_to = sales_by_year[sales_by_year['cw'] <= today_cw]
       sales_by_year_to = sales_by_year_to.groupby('year').agg({'net_value':'sum'})
       sales_by_year_to = sales_by_year_to.fillna(0)
    
       sales_by_year_from = sales_by_year[sales_by_year['cw'] > today_cw]
       sales_by_year_from = sales_by_year_from.groupby('year').agg({'net_value':'sum'})
       sales_by_year_from = sales_by_year_from.fillna(0)

       wallet = get_total_order_book()
       wallet_pd = pd.DataFrame(data={'year':[current_year], 'wallet_value':[wallet]})

       sales_2021 = sales_by_year[sales_by_year['year']==current_year]['net_value'].sum()

       plan = 23800000 - sales_2021 - wallet
       plan_pd = pd.DataFrame(data={'year':[current_year], 'plan_value':[plan]})

       sales_total = sales_by_year.groupby('year')['net_value'].sum().reset_index()
       sales_total = pd.merge(left=sales_total, right=wallet_pd, on='year', how='outer')
       sales_total = sales_total.fillna(0)
       sales_total = sales_total.set_index('year')
       sales_total['total'] = sales_total.sum(axis=1)
       

       fig = go.Figure(data=[
              go.Bar(name=f'Sprzedaż do {today_cw} tygodnia', y=sales_by_year_to['net_value'], x=sales_by_year_to.index,
               marker_color='darkblue'),
              go.Bar(name=f'Sprzedaż po {today_cw} tygodniach', y=sales_by_year_from['net_value'], x=sales_by_year_from.index, opacity=0.6,
               marker_color='darkgray'),
              go.Bar(name='Portfel', x=wallet_pd['year'], y=wallet_pd['wallet_value'], marker_color='orange'),
              go.Bar(name='Plan', x=plan_pd['year'], y=plan_pd['plan_value'], opacity=0.1, marker_color='gray'),
              go.Scatter(name='Razem', x=sales_total.index, y=sales_total['total'], mode='text', text=sales_total['total'], textposition='top center', texttemplate='%{text:.4s}',
              showlegend=False)
               ])
       fig.update_layout(barmode='stack', template='plotly_white', showlegend=True)
       fig.update_xaxes(dtick=1)
       fig.update_layout(modebar_add=["v1hovermode", "toggleSpikeLines"], modebar_remove=['zoom', 'pan', 'zoomIn', 'zoomOut', 'resetScale', 'select2d', 'lasso2d'])
       fig.update_layout(template='plotly_white',
                        height=300,
                        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        x=0),
                        margin=dict(
        l=1,
        r=1,
        b=10,
        t=5,
    ))
       return fig

def generate_order_data_line_fig():
    current_year = datetime.datetime.today().year
    previous_year = current_year - 1
    df = prepare_weekly_order_data()
    #df['cum_value'] = df.groupby('year')['net_value'].cumsum()
    
    fig1 = go.Figure()

    for year in range(2018, current_year+1):
        df_year = df[df['year']==year].groupby('cw', as_index=False).agg({'net_value':'sum'})
        
        if year == current_year:
            color = 'orange'
        elif year == previous_year:
            color = 'darkblue'
        else:
            color = 'lightgray'

        if year == current_year:
            fig1.add_trace(
                go.Scatter(
                    x = df_year['cw'],
                    y = df_year['net_value'],
                    name = year,
                    marker_color = color,
                    customdata = df_year['cw'],
                )
            )

        else:
            fig1.add_trace(
                go.Scatter(
                    x = df_year['cw'],
                    y = df_year['net_value'],
                    name = year,
                    marker_color = color,
                    customdata = df_year['cw'],
                )
            )

    fig1.update_layout(template='plotly_white', title_font_color='gray', modebar_add=["v1hovermode", "toggleSpikeLines"])
    fig1.update_xaxes(title='Tygodnie', dtick=1, title_font_color='gray', tickfont=dict(color='gray'), range=[0.5,52], showgrid=False, )
    fig1.update_yaxes(title='', tickfont=dict(color='gray'))

    fig1.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1),
        margin=dict(
        l=10,
        r=10,
        b=50,
        t=80,
        pad=4
    ),)

    df = prepare_weekly_order_data_incrementing()
    df['cum_value'] = df.groupby('year')['net_value'].cumsum()


    fig2 = go.Figure()

    for year in range(2018, current_year+1):
        df_year = df[df['year']==year].groupby('cw', as_index=False).agg({'cum_value':'sum'})
        
        if year == current_year:
            color = 'orange'
        elif year == previous_year:
            color = 'darkblue'
        else:
            color = 'lightgray'

        if year == current_year:
            fig2.add_trace(
                go.Scatter(
                    x = df_year['cw'],
                    y = df_year['cum_value'],
                    name = year,
                    marker_color = color,
                    customdata = df_year['cw'],
                )
            )

        else:
            fig2.add_trace(
                go.Scatter(
                    x = df_year['cw'],
                    y = df_year['cum_value'],
                    name = year,
                    marker_color = color,
                    customdata = df_year['cw'],
                )
            )

    fig2.update_layout(template='plotly_white', title_font_color='gray', modebar_add=["v1hovermode", "toggleSpikeLines"])
    fig2.update_xaxes(title='Tygodnie', dtick=1, title_font_color='gray', tickfont=dict(color='gray'), range=[0.5,52], showgrid=False, )
    fig2.update_yaxes(title='', tickfont=dict(color='gray'))

    fig2.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1),
        margin=dict(
        l=10,
        r=10,
        b=50,
        t=80,
        pad=4
    ),)
    
    return fig1, fig2

def generate_detailed_order_data_fig(year, cw):
    df = get_detailed_weekly_orders_by_cw_and_year(year, cw)
    df = df.sort_values(by='net_value', ascending=True)
    
    fig = go.Figure(data=[
        go.Bar(
            y=df['customer_name'],
            x=df['net_value'],
            marker_color = 'orange',
            text = round(df['net_value']/1000,2),
            textposition = 'outside',
            orientation='h'),
    ])

    fig.update_layout(template='plotly_white', title='', title_font_color='gray', showlegend=False)
    fig.update_yaxes(title='', title_font_color='gray', tickfont=dict(color='gray'), showgrid=False)
    fig.update_xaxes(title='', tickfont=dict(color='gray'), showgrid=False, showticklabels=False)

    fig.update_layout(
        margin=dict(
        l=1,
        r=1,
        b=10,
        t=20,
    ))

    return fig

