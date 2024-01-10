import pandas as pd
from database.database_connection import engine


def get_unique_companies_from_orders():
    connection = engine.connect()
    sql_query = pd.read_sql_query("SELECT DISTINCT customer_name, customer_no FROM IFSAPP.customer_order_join \
    WHERE customer_no LIKE 'E%' \
    AND objstate <> (SELECT ifsapp.CUSTOMER_ORDER_LINE_API.FINITE_STATE_ENCODE__('Anulowane') from dual) \
    AND (upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'A%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'B%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'C%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'D%' ) \
    OR upper(ifsapp.INVENTORY_PART_API.Get_Part_Product_Code(CONTRACT, CATALOG_NO)) like upper( 'E%' )) \
    ORDER BY customer_name", engine)
    companies = pd.DataFrame(sql_query)
    connection.close()
    return companies

def generate_company_list_for_dropdown():
    companies = get_unique_companies_from_orders()
    companies = companies.drop_duplicates(subset=['customer_name'], keep='first')
    companies_drop = [{'label':company, 'value':company} for company in companies['customer_name']]
    return companies_drop


def get_company_name_from_clients(company_no):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT name, customer_category \
    FROM IFSAPP.customer_info \
    WHERE customer_id = '{company_no}'", engine)
    companies = pd.DataFrame(sql_query)
    connection.close()
    return companies['name']

def get_companies_numbers_and_names():
    connection = engine.connect()
    sql_query = pd.read_sql_query("SELECT customer_id, name FROM IFSAPP.customer_info \
    WHERE customer_id like 'E%'", engine)
    companies = pd.DataFrame(sql_query)
    connection.close()
    return companies



