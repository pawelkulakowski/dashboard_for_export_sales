import pandas as pd
from database.database_connection import engine

def get_company_activities(company_name):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT ifsapp.business_activity.date_entered,  ifsapp.business_activity.calendar_activity_type, ifsapp.business_activity.description, ifsapp.business_activity.note \
    from ifsapp.customer_info \
    LEFT JOIN ifsapp.business_activity \
    ON ifsapp.customer_info.customer_id = ifsapp.business_activity.connection_id \
    where ifsapp.customer_info.name = '{company_name}'", engine)
    company_activities = pd.DataFrame(sql_query)
    connection.close()
    if not company_activities.iloc[0,1] == None:
        company_activities['date_entered'] = company_activities['date_entered'].dt.date
        company_activities = company_activities.rename(columns={
            'date_entered':'Data',
            'calendar_activity_type':'Typ',
            'description':'Opis',
            'note':'Notatka'
        })
    else:
        company_activities = pd.DataFrame(columns=['Data', 'Typ', 'Opis', 'Notatka'])
    
    return company_activities


def get_company_activities_in_offers(company_name):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT ifsapp.order_quotation.date_entered, ifsapp.order_quotation.quotation_no, ifsapp.order_quotation.closed_status \
    FROM ifsapp.customer_info \
    LEFT JOIN ifsapp.order_quotation \
    ON ifsapp.customer_info.customer_id = ifsapp.order_quotation.customer_no \
    WHERE ifsapp.customer_info.name = '{company_name}' \
    AND ifsapp.order_quotation.state not in ('Anulowane')", engine)
    company_activities_in_offers = pd.DataFrame(sql_query)
    connection.close()
    if not company_activities_in_offers.empty:
        company_activities_in_offers['date_entered'] = company_activities_in_offers['date_entered'].dt.date
        company_activities_in_offers = company_activities_in_offers.rename(columns={
            'date_entered':'Data',
            'quotation_no':'Opis',
            'closed_status':'Notatka'
        })
        company_activities_in_offers['Typ'] = 'Oferta'
        company_activities_in_offers = company_activities_in_offers[['Data', 'Typ', 'Opis', 'Notatka']]
    else:
        company_activities_in_offers = pd.DataFrame(columns=['Data', 'Typ', 'Opis', 'Notatka'])
    
    return company_activities_in_offers

def get_company_all_activities(company_name):
    company_activities = get_company_activities(company_name)
    company_activities_in_offers = get_company_activities_in_offers(company_name)

    company_all_activities = company_activities.append(company_activities_in_offers)
    
    if not company_all_activities.empty:
        company_all_activities = company_all_activities.sort_values(by='Data', ascending=False)
    return company_all_activities
