import pandas as pd
from database.database_connection import engine

def get_name_from_connection_id(connection_id):
    connection = engine.connect()
    if str(connection_id).startswith('E'):
        sql_query = pd.read_sql_query(f"SELECT ifsapp.customer_info.name FROM ifsapp.customer_info \
        WHERE ifsapp.customer_info.customer_id = '{connection_id}'", engine) 
    else: 
        sql_query = pd.read_sql_query(f"SELECT ifsapp.business_lead.name from ifsapp.business_lead \
        where ifsapp.business_lead.lead_id = {connection_id}", engine) 
    name = pd.DataFrame(sql_query)
    connection.close()
    return name.iloc[0,0]


def get_last_ten_leads(main_representative):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT * FROM (SELECT ifsapp.business_lead.creation_date, ifsapp.business_lead.name FROM ifsapp.business_lead \
    where ifsapp.business_lead.main_representative_id = '{main_representative}' \
    ORDER BY ifsapp.business_lead.creation_date DESC) \
    WHERE ROWNUM <= 10", engine) 
    last_ten_leads = pd.DataFrame(sql_query)
    connection.close()
    last_ten_leads['creation_date'] = last_ten_leads['creation_date'].dt.date
    return last_ten_leads

def get_last_ten_activities(main_representative):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT * FROM ( \
    SELECT ifsapp.business_activity.date_entered, ifsapp.business_activity.connection_id, ifsapp.business_activity.description, ifsapp.business_activity.calendar_activity_type, ifsapp.business_activity.note FROM ifsapp.business_activity \
    WHERE ifsapp.business_activity.main_representative_id = '{main_representative}' \
    ORDER BY ifsapp.business_activity.date_entered DESC) \
    WHERE ROWNUM <= 10", engine) 
    last_ten_activities = pd.DataFrame(sql_query)
    connection.close()
    last_ten_activities['date_entered'] = last_ten_activities['date_entered'].dt.date
    last_ten_activities['connection_id'] = last_ten_activities['connection_id'].apply(lambda x: get_name_from_connection_id(x))
    return last_ten_activities
