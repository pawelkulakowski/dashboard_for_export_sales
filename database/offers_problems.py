import pandas as pd
from datetime import date
from database.database_connection import engine


def get_offers_from_2021_without_district_code():
    previous_year = date.today().year-1 
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT quotation_no, date_entered, expiration_date, customer_no, district_code, salesman_code, state, closed_status, ifsapp.Order_Quotation_API.Get_Total_Sale_Price__(QUOTATION_NO) \
    FROM IFSAPP.order_quotation \
    WHERE customer_no like 'E%' \
    AND district_code IS NULL \
    AND contract = 'Z01' \
    AND date_entered >= to_date('{previous_year}0101', 'YYYYMMDD') \
    AND state NOT IN ('Anulowane', 'Zamknięte')", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    df = df.rename(columns={'IFSAPP.ORDER_QUOTATION_API.GET_TOTAL_SALE_PRICE__(QUOTATION_NO)':'net_value'})
    df['date_entered'] = pd.to_datetime(df['date_entered']).dt.date
    df['expiration_date'] = pd.to_datetime(df['expiration_date']).dt.date    
    return df

def get_offers_from_2021_without_salesman_code():
    previous_year = date.today().year-1 
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT quotation_no, date_entered, expiration_date, customer_no, district_code, salesman_code, state, closed_status, ifsapp.Order_Quotation_API.Get_Total_Sale_Price__(QUOTATION_NO) \
    FROM IFSAPP.order_quotation \
    WHERE customer_no like 'E%' \
    AND salesman_code IS NULL \
    AND contract = 'Z01' \
    AND date_entered >= to_date('{previous_year}0101', 'YYYYMMDD') \
    AND state NOT iN ('Anulowane', 'Zamknięte')", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    df = df.rename(columns={'IFSAPP.ORDER_QUOTATION_API.GET_TOTAL_SALE_PRICE__(QUOTATION_NO)':'net_value'})
    df['date_entered'] = pd.to_datetime(df['date_entered']).dt.date
    df['expiration_date'] = pd.to_datetime(df['expiration_date']).dt.date    
    return df

def get_offers_from_2021_without_expiration_date():
    previous_year = date.today().year-1 
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT quotation_no, date_entered, expiration_date, customer_no, district_code, salesman_code, state, closed_status, ifsapp.Order_Quotation_API.Get_Total_Sale_Price__(QUOTATION_NO) \
    FROM IFSAPP.order_quotation \
    WHERE customer_no like 'E%' \
    AND expiration_date IS NULL \
    AND contract = 'Z01' \
    AND date_entered >= to_date('{previous_year}0101', 'YYYYMMDD') \
    AND state NOT iN ('Anulowane', 'Zamknięte')", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    df = df.rename(columns={'IFSAPP.ORDER_QUOTATION_API.GET_TOTAL_SALE_PRICE__(QUOTATION_NO)':'net_value'})
    df['date_entered'] = pd.to_datetime(df['date_entered']).dt.date
    df['expiration_date'] = pd.to_datetime(df['expiration_date']).dt.date    
    return df

