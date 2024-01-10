import pandas as pd
from database.database_connection import engine

def get_company_open_orders(company_name):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT date_entered, order_no, line_no, catalog_no, wanted_delivery_date, promised_delivery_date, ifsapp.Customer_Order_Line_API.Get_Sale_Price_Total(ORDER_NO, LINE_NO, REL_NO, LINE_ITEM_NO) \
    FROM IFSAPP.customer_order_join \
    WHERE customer_name = '{company_name}' \
    AND contract = 'Z01' \
    AND objstate not in ('Invoiced', 'Cancelled') \
    AND date_entered >= to_date('20210101', 'YYYYMMDD') \
    AND (upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'A%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'B%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'C%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'D%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'E%' ))", engine)
    company_open_orders = pd.DataFrame(sql_query)
    connection.close()
    company_open_orders['date_entered'] = company_open_orders['date_entered'].dt.date
    company_open_orders['wanted_delivery_date'] = company_open_orders['wanted_delivery_date'].dt.date
    company_open_orders['promised_delivery_date'] = company_open_orders['promised_delivery_date'].dt.date
    company_open_orders = company_open_orders.rename(columns={'IFSAPP.CUSTOMER_ORDER_LINE_API.GET_SALE_PRICE_TOTAL(ORDER_NO,LINE_NO,REL_NO,LINE_ITEM_NO)':'value'})

    return company_open_orders