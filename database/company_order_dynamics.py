import pandas as pd
import plotly.graph_objects as go

from datetime import date
from database.database_connection import engine

from database.data.data_calendar import data_calendar

'''
SELECT date_entered, customer_name, ifsapp.Customer_Order_Line_API.Get_Sale_Price_Total(ORDER_NO, LINE_NO, REL_NO, LINE_ITEM_NO)
FROM IFSAPP.customer_order_join_cfv 
WHERE contract = 'Z01'
AND customer_no LIKE 'E%'
AND objstate <> (SELECT ifsapp.CUSTOMER_ORDER_LINE_API.FINITE_STATE_ENCODE__('Anulowane') from dual) 
AND date_entered <= to_date('20211231', 'YYYYMMDD') 
AND (upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'A%' ) 
OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'B%' ) 
OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'C%' ) 
OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'D%' ) 
OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'E%' ))
AND CF$_NR_RMA IS NULL
'''

def get_company_order_value_from_previous_years_by_year_and_cw(company_name):
    #data_orders = pd.read_parquet('/home/pkulakow/workspace/dash-zetkama/database/data/linie_zamowien_17-20_E_Z01_kod_produktu_anulowane.parquet')
    #data_orders = pd.read_feather('/home/pkulakow/workspace/dash-zetkama/database/data/linie_zamowien_E_Z01_ABCDE_bez_anul_i_rma.feather')
    df = pd.read_feather('/home/pkulakow/workspace/dash-zetkama/database/data/company_orders_by_year_and_cw.feather')
    #company_data = data_orders[data_orders['Nazwa klienta']==company_name].groupby(['year', 'cw'], as_index=False).agg({'Netto – waluta zamówienia': 'sum'})
    #company_data = company_data.drop(company_data[company_data['cw'] == 53].index)
    df = df[df['customer_name']==company_name].groupby(['year', 'cw'], as_index=False)['net_value'].sum()    
    return df


def get_company_order_data_from_2021(company_name):
    current_year = date.today().year
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT date_entered, ifsapp.Customer_Order_Line_API.Get_Sale_Price_Total(ORDER_NO, LINE_NO, REL_NO, LINE_ITEM_NO) \
    FROM IFSAPP.customer_order_join \
    WHERE customer_name = '{company_name}' \
    AND contract = 'Z01' \
    AND objstate <> (SELECT ifsapp.CUSTOMER_ORDER_LINE_API.FINITE_STATE_ENCODE__('Anulowane') from dual) \
    AND date_entered >= to_date('{current_year}0101', 'YYYYMMDD') \
    AND (upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'A%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'B%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'C%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'D%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'E%' ))", engine)
    company_data = pd.DataFrame(sql_query)
    connection.close()
    if not company_data.empty:
        company_data = company_data.rename(columns={'IFSAPP.CUSTOMER_ORDER_LINE_API.GET_SALE_PRICE_TOTAL(ORDER_NO,LINE_NO,REL_NO,LINE_ITEM_NO)':'net_value'})
        company_data['year'] = company_data['date_entered'].dt.year
        company_data['cw'] = company_data['date_entered'].dt.isocalendar().week
        company_data = company_data.groupby(['year', 'cw'], as_index=False)['net_value'].sum().sort_values(by=['year', 'cw'], ascending=True)
    else:
        company_data = pd.DataFrame(columns=['year', 'cw', 'net_value'])
    return company_data





def prepare_company_sales_data(company_name):
    company_data = get_company_order_value_from_previous_years_by_year_and_cw(company_name)
    company_data_2021 = get_company_order_data_from_2021(company_name)
    company_data_total = pd.merge(left=data_calendar, right=company_data, how='outer', on=['year', 'cw'])
    company_data_total_2 = pd.merge(left=company_data_total, right=company_data_2021, how='outer', on=['year', 'cw'])
    company_data_total_2 = company_data_total_2.fillna(0)
    company_data_total_2['net_value'] = company_data_total_2['net_value_x'] + company_data_total_2['net_value_y']
    company_data_total_2 = company_data_total_2.drop(columns=['net_value_x', 'net_value_y'])
    company_data_total_2 = company_data_total_2.sort_values(by=['year', 'cw'], ascending=True).reset_index()
    company_data_total_2 = company_data_total_2.drop(columns=['index'])
    company_data_total_2['cum_value'] = company_data_total_2.groupby(['year'])['net_value'].cumsum()
    return company_data_total_2
    # TODO: ograniczenie danych o linie RMA

#print(prepare_company_sales_data('EL TEMSAH eg'))

def generate_company_order_dynamics_fig(company_name):
    company_data = prepare_company_sales_data(company_name)
    
    # Tworzenie wykresu
    traces = []
    for year in company_data['year'].unique():
            company_data_year = company_data[company_data['year']==year]
            traces.append(go.Scatter(
                x = company_data_year['cw'],
                y = company_data_year['cum_value'],
                name = str(year),
                mode='lines',
            ))

    fig = go.Figure(
        data=traces,
        layout=go.Layout(
            title='Wpływ zamówień',
            template='plotly_white',
            showlegend=True
        )
    )

    fig.update_yaxes(title='Wartość netto w walucie zamówienia')
    fig.update_xaxes(dtick=1, title='Numer tygodnia', range=(1,52))
    fig.update_layout(modebar_add=["v1hovermode", "toggleSpikeLines"])

    return fig


