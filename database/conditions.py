# 02.02.2022 wersja
import pandas as pd
from database.database_connection import engine


# Downloading 
def get_conditions_with_2201():
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"select ifsapp.customer_agreement.agreement_id, ifsapp.customer_agreement.valid_from, ifsapp.customer_agreement.description, \
    ifsapp.customer_agreement.customer_no, ifsapp.customer_agreement.delivery_terms, ifsapp.customer_agreement.del_terms_location, \
    ifsapp.agreement_sales_group_deal.catalog_group, ifsapp.agreement_sales_group_deal.discount \
    FROM ifsapp.customer_agreement \
    INNER JOIN ifsapp.agreement_sales_group_deal \
    ON ifsapp.customer_agreement.agreement_id = ifsapp.agreement_sales_group_deal.agreement_id \
    WHERE ifsapp.customer_agreement.description like '%2201%'", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df

def get_list_of_export_clients():
    connection = engine.connect()
    sql_query = pd.read_sql_query("SELECT ifsapp.customer_info.customer_id, ifsapp.customer_info.name, ifsapp.customer_info.country, ifsapp.cust_ord_customer_address.district_code \
    FROM ifsapp.customer_info \
    INNER JOIN ifsapp.cust_ord_customer_address \
    ON ifsapp.customer_info.customer_id = ifsapp.cust_ord_customer_address.customer_no \
    WHERE ifsapp.customer_info.customer_id LIKE 'E%' \
    AND ifsapp.customer_info.party_type  = 'Klient'", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df

def get_unique_regions():
    connection = engine.connect()
    sql_query = pd.read_sql_query("SELECT DISTINCT ifsapp.cust_ord_customer_address.district_code \
    FROM ifsapp.cust_ord_customer_address \
    WHERE ifsapp.cust_ord_customer_address.district_code LIKE 'ME%'", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df

def prepare_data_for_conditions_table(region):
    df1 = get_conditions_with_2201()
    df2 = get_list_of_export_clients()
    df1 = df1.rename(columns={'customer_no':'customer_id'})
    df = pd.merge(left=df1, right=df2, on='customer_id', how='left')
    df['catalog_group'] = df['catalog_group'].str.split('-').str[1]

    df = df.pivot_table(index=['name', 'country', 'district_code'], columns='catalog_group', values='discount').fillna('').reset_index()
    if region != 'All':
        df = df[df['district_code']==region]
    return df
