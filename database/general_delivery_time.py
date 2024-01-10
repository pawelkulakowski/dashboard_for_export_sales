import pandas as pd
import datetime
import plotly.graph_objects as go

from database.database_connection import engine

def q1(x):
    return x.quantile(0.25)

def median(x):
    return x.quantile(0.5)

def q3(x):
    return x.quantile(0.75)

def get_delivery_data_from_previous_years():
    df = pd.read_feather('database/data/delivery_dates.feather')
    df = df.set_index('date_entered')
    return df

def get_delivery_data_from_current_year():
    current_year = datetime.datetime.today().year
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT date_entered, promised_delivery_date \
    FROM IFSAPP.customer_order_join_cfv \
    WHERE contract = 'Z01' \
    AND customer_no like upper('E%') \
    AND order_no like upper('S%') \
    AND objstate <> (SELECT ifsapp.CUSTOMER_ORDER_LINE_API.FINITE_STATE_ENCODE__('Anulowane') from dual) \
    AND date_entered >= to_date('{current_year}0101', 'YYYYMMDD') \
    AND (upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'A%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'B%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'C%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'D%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'E%' )) \
    AND CF$_NR_RMA IS NULL \
    ORDER BY date_entered", engine)
    delivery_data = pd.DataFrame(sql_query)
    connection.close()
    delivery_data['date_entered'] = delivery_data['date_entered'].dt.date
    delivery_data = delivery_data.set_index('date_entered')
    delivery_data.index = pd.to_datetime(delivery_data.index)
    return delivery_data

def prepare_delivery_data():
    x = get_delivery_data_from_previous_years()
    y = get_delivery_data_from_current_year()
    z = x.append(y)
    z['time'] = abs(((z['promised_delivery_date'] - z.index).dt.days)/7)
    z = z[['time']]
    z = z.resample('M').agg([q1, median, q3, 'mean'])
    z.columns = z.columns.get_level_values(1)
    return z

def generate_delivery_data_fig():
    test3 = prepare_delivery_data()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=test3.index, 
                            y=test3['q1'],
                            mode='lines',
                            name='Kwartyl 25%',
                            
                            opacity=0.25,
                            line=dict(color='blue', width=0.5),
                            ))
    fig.add_trace(go.Scatter(x=test3.index, 
                            y=test3['median'],
                            mode='lines',
                            name='Mediana',
                            fill="tonexty",
                            line=dict(color='blue', width=2)
                            ))

    fig.add_trace(go.Scatter(x=test3.index, 
                            y=test3['q3'],
                            mode='lines',
                            name='Kwartyl 75%',
                            opacity=0.25,
                            fill="tonexty",
                            line=dict(color='blue', width=0.5),
                            ))

    fig.add_trace(go.Scatter(x=test3.index, 
                            y=test3['mean'],
                            mode='lines',
                            name='Średnia',
                            opacity=0.25,
                            line=dict(color='blue', width=2, dash='dash'),
                            ))

    fig.add_trace(go.Scatter(x=test3.index, 
                            y=[3 for i in range(0, len(test3.index))],
                            mode='lines',
                            name='Cel',
                            line=dict(color='orange', width=2, dash='dash'),
                            ))


    fig.update_yaxes(title='Ilość tygodni', range=(1,15), dtick=1, showgrid=False,
                    tickfont=dict(color='gray'),
                    title_font=dict(color='gray'))
    fig.update_xaxes(title='',
                    tickfont=dict(color='gray'),
                    title_font=dict(color='gray'))
    fig.update_layout(template='plotly_white', title='', title_font={'color':'gray'}, modebar_add=["v1hovermode", "toggleSpikeLines"])

    return fig
