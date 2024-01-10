import pandas as pd
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import datetime

from database.data.data_sales import data_sales
from database.company_list import get_unique_companies_from_orders
from database.database_connection import engine



#sales_total = sales_total.rename(columns={'customer_name':'Klient Nazwa'})
#sales_by_company = data_sales.groupby(['Klient Nazwa', 'year', 'cw'], as_index=False).agg({'Netto – waluta zamówienia': 'sum'})

def get_company_ids(company_name):
      companies_from_orders = get_unique_companies_from_orders()
      company_numbers = companies_from_orders[companies_from_orders['customer_name']==f'{company_name}']['customer_no'].to_list()
      company_number_tuple = str(tuple(company_numbers))
      if company_number_tuple[-2] == ',':
           company_number_tuple = company_number_tuple.replace(company_number_tuple[-2],"")
      return company_number_tuple


def get_company_sales_data_2021(company_number_tuple):
      connection = engine.connect()
      sql_query = pd.read_sql_query(f"SELECT invoice_date, catalog_no, net_curr_amount \
      FROM ifsapp.CUSTOMER_ORDER_INV_JOIN_cfv \
      WHERE identity IN {company_number_tuple} \
      AND invoice_date >=to_date( '20210101', 'YYYYMMDD' ) \
      AND client_state <> 'Anulowana' \
      AND contract = 'Z01' \
      AND (upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'A%' ) \
      OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'B%' ) \
      OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'C%' ) \
      OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'D%' ) \
      OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'E%' ))", engine)
      company_sales_data_2021 = pd.DataFrame(sql_query)
      connection.close()
      return company_sales_data_2021

def get_wallet_total_sum_2021(company_number_tuple):   
       connection = engine.connect()    
       sql_query = pd.read_sql_query(f"SELECT catalog_no, (BUY_QTY_DUE - QTY_INVOICED)*ifsapp.Customer_Order_Line_API.Get_Sale_Price_Total(ORDER_NO, LINE_NO, REL_NO, LINE_ITEM_NO)/BUY_QTY_DUE \
       FROM IFSAPP.customer_order_join \
       WHERE customer_no IN {company_number_tuple} \
       AND contract = 'Z01' \
       AND ORDER_NO like 'S%' \
       AND objstate <> (SELECT ifsapp.CUSTOMER_ORDER_LINE_API.FINITE_STATE_ENCODE__('Anulowane') from dual) \
       AND date_entered >= to_date('20210101', 'YYYYMMDD') \
       AND (upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'A%' ) \
       OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'B%' ) \
       OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'C%' ) \
       OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'D%' ) \
       OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'E%' ))", engine)
       order_data = pd.DataFrame(sql_query)
       connection.close()
       order_data = order_data.rename(columns={'(BUY_QTY_DUE-QTY_INVOICED)*IFSAPP.CUSTOMER_ORDER_LINE_API.GET_SALE_PRICE_TOTAL(ORDER_NO,LINE_NO,REL_NO,LINE_ITEM_NO)/BUY_QTY_DUE':'wallet'})
       return order_data


def prepare_company_sales_data(company_name):
      company_sales_by_year = data_sales[data_sales['Klient Nazwa']==company_name].groupby(['year', 'cw'], as_index=False).agg({'Netto – waluta zamówienia': 'sum'})
      company_number_tuple = get_company_ids(company_name)
      company_sales_data_2021 = get_company_sales_data_2021(company_number_tuple)
      
      # Preparing data for first general sales graph
      if not company_sales_data_2021.empty:
        company_sales_data_2021['invoice_date'] = pd.to_datetime(company_sales_data_2021['invoice_date'])
        company_sales_data_2021['year'] = company_sales_data_2021['invoice_date'].dt.year
        company_sales_data_2021['cw'] = company_sales_data_2021['invoice_date'].dt.isocalendar().week
        
        company_sales_data_2021 = company_sales_data_2021.groupby(['year', 'cw'], as_index=False).agg({'net_curr_amount': 'sum'})
        company_sales_data_2021 = company_sales_data_2021.rename(columns={'net_curr_amount':'Netto – waluta zamówienia'})
        company_sales_by_year = company_sales_by_year.append(company_sales_data_2021)
      
      # Adding empty data for missing years to avoid problems
      for year in [2017, 2018, 2019, 2020, 2021]:
            if not year in company_sales_by_year['year'].values:
                  new_row = {'year': year, 'cw':1, 'Netto – waluta zamówienia':0}
                  company_sales_by_year = company_sales_by_year.append(new_row, ignore_index=True)
      company_sales_by_year = company_sales_by_year.sort_values(by=['year', 'cw'], ascending=True)
      wallet = get_wallet_total_sum_2021(company_number_tuple)['wallet'].sum()
      return company_sales_by_year, wallet


def prepare_2(company_name):
      company_sales_by_year = data_sales[(data_sales['Klient Nazwa']==company_name)&(data_sales['year']!=2017)].groupby(['year', 'short_index'], as_index=False).agg({'Netto – waluta zamówienia': 'sum'})
      company_number_tuple = get_company_ids(company_name)
      company_sales_data_2021 = get_company_sales_data_2021(company_number_tuple)
      company_wallet_data_2021 = get_wallet_total_sum_2021(company_number_tuple)

      if not company_sales_data_2021.empty:
            company_sales_data_2021['invoice_date'] = pd.to_datetime(company_sales_data_2021['invoice_date'])
            company_sales_data_2021['year'] = company_sales_data_2021['invoice_date'].dt.year
            company_sales_data_2021['short_index'] = company_sales_data_2021['catalog_no'].str[2:6]
            company_sales_data_2021 = company_sales_data_2021.groupby(['year', 'short_index'], as_index=False).agg({'net_curr_amount': 'sum'})
            company_sales_data_2021 = company_sales_data_2021.rename(columns={'net_curr_amount': 'Netto – waluta zamówienia'})
            company_sales_by_year = company_sales_by_year.append(company_sales_data_2021)
    

      if not company_wallet_data_2021.empty and company_wallet_data_2021['wallet'].sum() != 0:
            company_wallet_data_2021['short_index'] = company_wallet_data_2021['catalog_no'].str[2:6]
            company_wallet_data_2021 = company_wallet_data_2021.groupby(['short_index'], as_index=False).agg({'wallet': 'sum'})
            company_wallet_data_2021['year'] = 'wallet'
            company_wallet_data_2021 = company_wallet_data_2021.rename(columns={'wallet': 'Netto – waluta zamówienia'}) 
            company_wallet_data_2021 = company_wallet_data_2021[['year', 'short_index', 'Netto – waluta zamówienia']]
            company_sales_by_year = company_sales_by_year.append(company_wallet_data_2021).fillna(0)
      
      company_sales_by_year['Netto – waluta zamówienia'] = round(company_sales_by_year['Netto – waluta zamówienia']/1000, 2)
      company_sales_by_year = company_sales_by_year.pivot(index='year', columns='short_index', values='Netto – waluta zamówienia').fillna(0)      

      return company_sales_by_year


def generate_company_sales_data_bar_fig(company_name):
      today_cw = datetime.date.today().isocalendar()[1]
      company_data = prepare_company_sales_data(company_name)
      company_sales_by_year = company_data[0]
      company_wallet = company_data[1]
      sales_by_company_to = company_sales_by_year[company_sales_by_year['cw'] <= today_cw].groupby('year', as_index=False)['Netto – waluta zamówienia'].sum()
      sales_by_company_from = company_sales_by_year[company_sales_by_year['cw'] > today_cw].groupby('year', as_index=False)['Netto – waluta zamówienia'].sum()
      fig = go.Figure(data=[
            go.Bar(name=f'Sprzedaż do {today_cw} tygodnia', y=sales_by_company_to['Netto – waluta zamówienia'], x=sales_by_company_to['year'],
               marker_color='#76C893'),
               go.Bar(name=f'Sprzedaż po {today_cw} tygodniach', y=sales_by_company_from['Netto – waluta zamówienia'], x=sales_by_company_from['year'], opacity=0.6,
               marker_color='#B5E48C'),
               go.Bar(name='Portfel', x=[datetime.datetime.today().year], y=[company_wallet], opacity=0.6, marker_color='#168AAD')
      ])
      fig.update_layout(barmode='stack', template='plotly_white', showlegend=False, modebar_add=["v1hovermode", "toggleSpikeLines"])
      fig.update_xaxes(dtick=1)
      
      return fig

def generate_company_sales_data_heatmap_fig(company_name):
      company_data = prepare_2(company_name)
      
      if 'wallet' in company_data.index:
            company_data_sales = company_data.iloc[:-1,:]
            company_data_wallet = company_data.iloc[[-1],:]
      
            if not company_data_sales.empty:

                  fig2 = ff.create_annotated_heatmap(
                        z = company_data_sales.values,
                        x = company_data_sales.columns.tolist(),
                        y = ['|'+str(i)+'|' for i in company_data_sales.index.tolist()],
                        colorscale='greens'
                  )

                  fig1 = ff.create_annotated_heatmap(
                        z = company_data_wallet.values,
                        x = company_data_wallet.columns.tolist(),
                        y = company_data_wallet.index.tolist(),
                        colorscale='blues'
                  )


                  fig = make_subplots(
                        rows=2, cols=1,
                        vertical_spacing=0.0,
                        shared_xaxes=True,
                        row_heights=[4, len(company_data_sales.index.tolist())*4]
                        )
                  fig.add_trace(fig1.data[0], 1, 1)
                  fig.add_trace(fig2.data[0], 2, 1)

                  annot1 = list(fig1.layout.annotations)
                  annot2 = list(fig2.layout.annotations)
                  for k  in range(len(annot2)):
                        annot2[k]['xref'] = 'x2'
                        annot2[k]['yref'] = 'y2'
                  fig.update_layout(annotations=annot1+annot2)
                  fig.update_yaxes(dtick=1)
                  fig.update_xaxes(dtick=1)
                  return fig

            if company_data_sales.empty:

                  fig1 = ff.create_annotated_heatmap(
                              z = company_data_wallet.values,
                              x = company_data_wallet.columns.tolist(),
                              y = company_data_wallet.index.tolist(),
                              colorscale='blues'
                        )
                  return fig1

      fig2 = ff.create_annotated_heatmap(
                        z = company_data.values,
                        x = company_data.columns.tolist(),
                        y = ['|'+str(i)+'|' for i in company_data.index.tolist()],
                        colorscale='greens'
                  )
      return fig2