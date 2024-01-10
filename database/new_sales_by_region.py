import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.express as px

from database.database_connection import engine


def get_new_sales_and_new_products_from_current_year():
    current_year = datetime.datetime.today().year
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT cf$_typ_sprzedazy, date_entered, order_no, district_code, customer_no, customer_name, line_no, buy_qty_due, part_price, discount, cf$_cena_po_rabacie_zam, currency_rate, cost, state \
    FROM IFSAPP.customer_order_join_cfv \
    WHERE contract = 'Z01' \
    AND customer_no like upper('E%') \
    AND cf$_typ_sprzedazy in ('Nowy klient', 'Rozszerzenie oferty') \
    AND objstate <> (SELECT ifsapp.CUSTOMER_ORDER_LINE_API.FINITE_STATE_ENCODE__('Anulowane') from dual) \
    AND date_entered >= to_date('{current_year}0101', 'YYYYMMDD') \
    AND (upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'A%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'B%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'C%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'D%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'E%' ))", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df



def get_total_new_sales_and_new_products_from_current_year():
    current_year = datetime.datetime.today().year
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT cf$_typ_sprzedazy, SUM(ifsapp.Customer_Order_Line_API.Get_Sale_Price_Total(ORDER_NO, LINE_NO, REL_NO, LINE_ITEM_NO)) \
    FROM IFSAPP.customer_order_join_cfv \
    WHERE contract = 'Z01' \
    AND customer_no like upper('E%') \
    AND cf$_typ_sprzedazy in ('Nowy klient', 'Rozszerzenie oferty') \
    AND objstate <> (SELECT ifsapp.CUSTOMER_ORDER_LINE_API.FINITE_STATE_ENCODE__('Anulowane') from dual) \
    AND date_entered >= to_date('{current_year}0101', 'YYYYMMDD') \
    AND (upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'A%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'B%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'C%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'D%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'E%' )) \
    GROUP BY cf$_typ_sprzedazy", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    df = df.rename(columns={'SUM(IFSAPP.CUSTOMER_ORDER_LINE_API.GET_SALE_PRICE_TOTAL(ORDER_NO,LINE_NO,REL_NO,LINE_ITEM_NO))':'net_value',
                            'cf$_typ_sprzedazy':'sales_type'})
    return df

def get_new_sales_and_new_products_from_current_year_by_region(region):
    current_year = datetime.datetime.today().year
    connection = engine.connect()
    if region == 'All':
        sql_query = pd.read_sql_query(f"SELECT cf$_typ_sprzedazy, customer_name, catalog_no, buy_qty_due, part_price, discount, cf$_cena_po_rabacie_zam, currency_rate, cost \
        FROM IFSAPP.customer_order_join_cfv \
        WHERE contract = 'Z01' \
        AND customer_no like upper('E%') \
        AND cf$_typ_sprzedazy in ('Nowy klient', 'Rozszerzenie oferty') \
        AND objstate <> (SELECT ifsapp.CUSTOMER_ORDER_LINE_API.FINITE_STATE_ENCODE__('Anulowane') from dual) \
        AND date_entered >= to_date('{current_year}0101', 'YYYYMMDD') \
        AND (upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'A%' ) \
        OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'B%' ) \
        OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'C%' ) \
        OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'D%' ) \
        OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'E%' ))", engine)
    else:
        sql_query = pd.read_sql_query(f"SELECT cf$_typ_sprzedazy, customer_name, catalog_no, buy_qty_due, part_price, discount, cf$_cena_po_rabacie_zam, currency_rate, cost \
        FROM IFSAPP.customer_order_join_cfv \
        WHERE contract = 'Z01' \
        AND district_code = '{region}' \
        AND customer_no like upper('E%') \
        AND cf$_typ_sprzedazy in ('Nowy klient', 'Rozszerzenie oferty') \
        AND objstate <> (SELECT ifsapp.CUSTOMER_ORDER_LINE_API.FINITE_STATE_ENCODE__('Anulowane') from dual) \
        AND date_entered >= to_date('{current_year}0101', 'YYYYMMDD') \
        AND (upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'A%' ) \
        OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'B%' ) \
        OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'C%' ) \
        OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'D%' ) \
        OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'E%' ))", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df

def prepare_new_sales_and_products_from_current_year_by_region_view(region):
    df = get_new_sales_and_new_products_from_current_year_by_region(region)
    df['net_value'] = df['buy_qty_due'] * df['cf$_cena_po_rabacie_zam']
    df['short_index'] = df['catalog_no'].str[2:6]
    df_new_sales = df[df['cf$_typ_sprzedazy']=='Nowy klient'].groupby(['customer_name', 'short_index'], as_index=False).agg({'net_value':'sum'})
    df_new_products = df[df['cf$_typ_sprzedazy']=='Rozszerzenie oferty'].groupby(['customer_name', 'short_index'], as_index=False).agg({'net_value':'sum'})
    return df_new_sales, df_new_products

def prepare_new_sales_and_products_from_current_year_by_region():
    df = get_new_sales_and_new_products_from_current_year()
    df['net_value'] = df['buy_qty_due'] * df['cf$_cena_po_rabacie_zam']
    df2 = df.groupby(['district_code', 'cf$_typ_sprzedazy'], as_index=False).agg({'net_value':'sum'})
    df2 = df2.rename(columns={'cf$_typ_sprzedazy':'sales_type'})
    return df2

def generetate_total_new_sales_and_products_from_current_year():
    
    df = get_total_new_sales_and_new_products_from_current_year()

    a = df[df['sales_type']=='Rozszerzenie oferty']['net_value'].values[0]
    b = df[df['sales_type']=='Nowy klient']['net_value'].values[0]
    c = 2000000

    fig = go.Figure(
        data=go.Pie(
            labels=['Rozszerzenie oferty', 'Nowy klient', 'Cel'],
            values=[a,b,c-a-b],
            hole=.7,
            marker_colors=['darkblue', 'orange', 'lightgray'],
            textposition = 'inside'
        ),
        layout=go.Layout(
                annotations=[{'text': "&#8364;" + str(round((a+b)/1000,2)), 'x':0.50, 'y':0.5, 'font_size':14, 'showarrow':False}],
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

def generate_new_sales_and_products_from_current_year_by_region_graph():
    df = prepare_new_sales_and_products_from_current_year_by_region()
    df_pivot = df.pivot_table(index='district_code', values='net_value', aggfunc='sum')
    df_pivot = df_pivot.reset_index()
    df_new_sales = df[df['sales_type']=='Nowy klient'].groupby('district_code', as_index=False).agg({'net_value':'sum'})
    df_new_products = df[df['sales_type']=='Rozszerzenie oferty'].groupby('district_code', as_index=False).agg({'net_value':'sum'})
    fig = go.Figure(
        data=[
            go.Bar(
                x = df_new_sales['district_code'],
                y = df_new_sales['net_value'],
                name='Nowe sprzedaże',
                marker_color='orange'
            ),
            go.Bar(
                x = df_new_products['district_code'],
                y = df_new_products['net_value'],
                name='Rozszerzenie oferty',
                marker_color='darkblue'
            ),
            go.Scatter(
                x = df_pivot['district_code'],
                y = df_pivot['net_value'],
                name='Razem',
                mode='text',
                text = df_pivot['net_value'],
                textposition='top center', 
                texttemplate='%{text:.4s}',
                showlegend=False
            )
        ]
    )
    fig.update_layout(barmode='stack', template='plotly_white', height=300)

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0),
        margin=dict(
        l=10,
        r=10,
        b=10,
        t=30,
        pad=4
    ),)
    return fig



def generate_graphs_for_region_view(region):
    df_new_sales, df_new_products = prepare_new_sales_and_products_from_current_year_by_region_view(region)

    fig1 = px.bar(df_new_sales, 
                    y='short_index', 
                    x='net_value', 
                    color='customer_name', 
                    template='plotly_white', 
                    orientation='h',
                    color_discrete_sequence=px.colors.sequential.Cividis)
    fig2 = px.bar(df_new_products, 
                    y='short_index', 
                    x='net_value', 
                    color='customer_name', 
                    template='plotly_white', 
                    orientation='h',
                    color_discrete_sequence=px.colors.sequential.Cividis)

    fig1.update_yaxes(categoryorder='total ascending', title='')
    fig1.update_xaxes(title='')
    fig2.update_yaxes(categoryorder='total ascending', title='')
    fig2.update_xaxes(title='')

    fig1.update_layout(legend=dict(
        orientation="h",
        y=-0.1,
        x=0),
        margin=dict(
        l=10,
        r=10,
        b=10,
        t=30,
        pad=4
        ),
        legend_title_text='')

    fig2.update_layout(legend=dict(
        orientation="h",
        y=-0.1,
        x=0),
        margin=dict(
        l=10,
        r=10,
        b=10,
        t=30,
        pad=4
        ),
        legend_title_text='')

    return fig1, fig2
