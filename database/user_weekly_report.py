import pandas as pd
from database.database_connection import engine

# Lista utworzonych klientów
def get_created_clients(main_representative, start_date, end_date):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT ifsapp.customer_info.creation_date, ifsapp.customer_info.customer_category, ifsapp.cust_ord_customer_ent.name \
    FROM ifsapp.customer_info \
    LEFT JOIN ifsapp.cust_ord_customer_ent \
    ON ifsapp.cust_ord_customer_ent.customer_id = ifsapp.customer_info.customer_id \
    WHERE ifsapp.cust_ord_customer_ent.salesman_code = '{main_representative}' \
    AND ifsapp.customer_info.creation_date >= to_date('{start_date}', 'YYYYMMDD') \
    AND ifsapp.customer_info.creation_date <= to_date('{end_date}', 'YYYYMMDD') \
    AND ifsapp.customer_info.customer_category = 'Klient'", engine) 
    created_clients = pd.DataFrame(sql_query)
    connection.close()
    if not created_clients.empty:
        created_clients['creation_date'] = created_clients['creation_date'].dt.date
        created_clients = created_clients.rename(columns={'creation_date': 'date_entered', 'customer_category':'task_type'})
    else:
        created_clients = pd.DataFrame(columns=['date_entered', 'task_type', 'name', 'additional_info', 'note'])
    return created_clients

# Lista utworzonych potencjalnych klientów
def get_created_potential_clients(main_representative, start_date, end_date):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT ifsapp.customer_info.creation_date, ifsapp.customer_info.customer_category, ifsapp.cust_ord_customer_ent.name \
    FROM ifsapp.customer_info \
    LEFT JOIN ifsapp.cust_ord_customer_ent \
    ON ifsapp.cust_ord_customer_ent.customer_id = ifsapp.customer_info.customer_id \
    WHERE ifsapp.cust_ord_customer_ent.salesman_code = '{main_representative}' \
    AND ifsapp.customer_info.creation_date >= to_date('{start_date}', 'YYYYMMDD') \
    AND ifsapp.customer_info.creation_date <= to_date('{end_date}', 'YYYYMMDD') \
    AND ifsapp.customer_info.customer_category = 'Potencjalny klient'", engine) 
    created_potential_clients = pd.DataFrame(sql_query)
    connection.close()
    if not created_potential_clients.empty:
        created_potential_clients['creation_date'] = created_potential_clients['creation_date'].dt.date
        created_potential_clients = created_potential_clients.rename(columns={'creation_date': 'date_entered', 'customer_category':'task_type'})
    else:
        created_potential_clients = pd.DataFrame(columns=['date_entered', 'task_type', 'name', 'additional_info', 'note'])
    return created_potential_clients

# Lista utworzonych ofert
def get_created_offers(main_representative, start_date, end_date):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT ifsapp.order_quotation.date_entered, ifsapp.order_quotation.quotation_no, ifsapp.customer_info.name, ifsapp.Order_Quotation_API.Get_Total_Sale_Price__(QUOTATION_NO) \
    FROM ifsapp.order_quotation \
    LEFT JOIN ifsapp.customer_info \
    ON ifsapp.order_quotation.customer_no  = ifsapp.customer_info.customer_id \
    WHERE ifsapp.order_quotation.state != 'Anulowane' \
    AND ifsapp.order_quotation.salesman_code = '{main_representative}' \
    AND ifsapp.order_quotation.date_entered >= to_date('{start_date}', 'YYYYMMDD') \
    AND ifsapp.order_quotation.date_entered <= to_date('{end_date}', 'YYYYMMDD')", engine) 
    created_offers = pd.DataFrame(sql_query)
    connection.close()
    if not created_offers.empty:
        created_offers['date_entered'] = created_offers['date_entered'].dt.date
        created_offers = created_offers.rename(columns={'quotation_no':'additional_info', 'IFSAPP.ORDER_QUOTATION_API.GET_TOTAL_SALE_PRICE__(QUOTATION_NO)':'note'})
        created_offers['task_type'] = 'Oferta'
    else:
        created_offers = pd.DataFrame(columns=['date_entered', 'task_type', 'name', 'additional_info', 'note'])
    return created_offers

# Lista utworzonych lead'ow
def get_created_leads(main_representative, start_date, end_date):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT ifsapp.business_lead.creation_date, ifsapp.business_lead.name FROM ifsapp.business_lead \
    WHERE ifsapp.business_lead.main_representative_id = '{main_representative}' \
    and ifsapp.business_lead.creation_date >= to_date('{start_date}', 'YYYYMMDD') \
    and ifsapp.business_lead.creation_date <= to_date('{end_date}', 'YYYYMMDD')", engine) 
    created_leads = pd.DataFrame(sql_query)
    connection.close()
    if not created_leads.empty:
        created_leads['creation_date'] = created_leads['creation_date'].dt.date
        created_leads = created_leads.rename(columns={'creation_date': 'date_entered'})
        created_leads['task_type'] = 'Nowy lead'
    else:
        created_leads = pd.DataFrame(columns=['date_entered', 'task_type', 'name', 'additional_info', 'note'])
    return created_leads

# Lista aktywności na klientach
def get_activities_on_clients(main_representative, start_date, end_date):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT ifsapp.business_activity.start_date, ifsapp.business_activity.calendar_activity_type, ifsapp.business_activity.description, ifsapp.customer_info.name, ifsapp.business_activity.note \
    FROM ifsapp.business_activity \
    LEFT JOIN ifsapp.customer_info \
    ON ifsapp.business_activity.connection_id = ifsapp.customer_info.customer_id \
    WHERE ifsapp.business_activity.main_representative_id = '{main_representative}' \
    and ifsapp.business_activity.calendar_activity_type = 'Zadanie' \
    and ifsapp.business_activity.start_date >= to_date('{start_date}', 'YYYYMMDD') \
    and ifsapp.business_activity.start_date <= to_date('{end_date}', 'YYYYMMDD') \
    AND ifsapp.business_activity.connection_id like ('E%')", engine) 
    activities_on_clients = pd.DataFrame(sql_query)
    connection.close()
    if not activities_on_clients.empty:
        activities_on_clients['start_date'] = activities_on_clients['start_date'].dt.date
        activities_on_clients = activities_on_clients.rename(columns={'start_date':'date_entered', 'calendar_activity_type':'task_type', 'description':'additional_info'})
    else:
        activities_on_clients = pd.DataFrame(columns=['date_entered', 'task_type', 'name', 'additional_info', 'note'])
    return activities_on_clients

# Lista aktywności na potencjalnych klientach
def get_activities_on_potential_clients(main_representative, start_date, end_date):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT ifsapp.business_activity.start_date, ifsapp.business_activity.calendar_activity_type, ifsapp.business_activity.description, ifsapp.business_lead.name, ifsapp.business_activity.note \
    FROM ifsapp.business_activity \
    LEFT JOIN ifsapp.business_lead \
    ON ifsapp.business_activity.connection_id = ifsapp.business_lead.lead_id \
    WHERE ifsapp.business_activity.main_representative_id = '{main_representative}' \
    and ifsapp.business_activity.calendar_activity_type = 'Zadanie' \
    and ifsapp.business_activity.start_date >= to_date('{start_date}', 'YYYYMMDD') \
    and ifsapp.business_activity.start_date <= to_date('{end_date}', 'YYYYMMDD') \
    AND ifsapp.business_activity.connection_id not like ('E%')", engine) 
    activities_on_potential_clients = pd.DataFrame(sql_query)
    connection.close()
    if not activities_on_potential_clients.empty:
        activities_on_potential_clients['start_date'] = activities_on_potential_clients['start_date'].dt.date
        activities_on_potential_clients = activities_on_potential_clients.rename(columns={'start_date':'date_entered', 'calendar_activity_type':'task_type', 'description':'additional_info'})
    else:
        activities_on_potential_clients = pd.DataFrame(columns=['date_entered', 'task_type', 'name', 'additional_info', 'note'])
    return activities_on_potential_clients

# Lista spotkań z klientami
def get_meetings_with_clients(main_representative, start_date, end_date):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT ifsapp.business_activity.date_entered, ifsapp.business_activity.calendar_activity_type, ifsapp.business_activity.description, ifsapp.customer_info.name, ifsapp.business_activity.note \
    FROM ifsapp.business_activity \
    LEFT JOIN ifsapp.customer_info \
    ON ifsapp.business_activity.connection_id = ifsapp.customer_info.customer_id \
    WHERE ifsapp.business_activity.main_representative_id = '{main_representative}' \
    and ifsapp.business_activity.calendar_activity_type = 'Spotkanie' \
    and ifsapp.business_activity.date_entered >= to_date('{start_date}', 'YYYYMMDD') \
    and ifsapp.business_activity.date_entered <= to_date('{end_date}', 'YYYYMMDD') \
    AND ifsapp.business_activity.connection_id like ('E%')", engine) 
    meetings_with_clients = pd.DataFrame(sql_query)
    connection.close()
    if not meetings_with_clients.empty:
        meetings_with_clients['date_entered'] = meetings_with_clients['date_entered'].dt.date
        meetings_with_clients = meetings_with_clients.rename(columns={'calendar_activity_type':'task_type', 'description':'additional_info'})
    else:
        meetings_with_clients = pd.DataFrame(columns=['date_entered', 'task_type', 'name', 'additional_info', 'note'])
    return meetings_with_clients

# Lista spotkań z potencjalnymi klientami
def get_meetings_with_potential_clients(main_representative, start_date, end_date):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT ifsapp.business_activity.date_entered, ifsapp.business_activity.calendar_activity_type, ifsapp.business_activity.description, ifsapp.business_lead.name, ifsapp.business_activity.note \
    FROM ifsapp.business_activity \
    LEFT JOIN ifsapp.business_lead \
    ON ifsapp.business_activity.connection_id = ifsapp.business_lead.lead_id \
    WHERE ifsapp.business_activity.main_representative_id = '{main_representative}' \
    and ifsapp.business_activity.calendar_activity_type = 'Spotkanie' \
    and ifsapp.business_activity.date_entered >= to_date('{start_date}', 'YYYYMMDD') \
    and ifsapp.business_activity.date_entered <= to_date('{end_date}', 'YYYYMMDD') \
    AND ifsapp.business_activity.connection_id not like ('E%')", engine) 
    meetings_with_potential_clients = pd.DataFrame(sql_query)
    connection.close()
    if not meetings_with_potential_clients.empty:
        meetings_with_potential_clients['date_entered'] = meetings_with_potential_clients['date_entered'].dt.date
        meetings_with_potential_clients = meetings_with_potential_clients.rename(columns={'calendar_activity_type':'task_type', 'description':'additional_info'})
    else:
        meetings_with_potential_clients = pd.DataFrame(columns=['date_entered', 'task_type', 'name', 'additional_info', 'note'])
    return meetings_with_potential_clients



def get_all_activities(main_representative, switches, start_date, end_date):
    
    chosen_switches = []

    if 'klienci' in switches:
        created_clients = get_created_clients(main_representative, start_date, end_date)
        chosen_switches.append(created_clients)
    if 'potencjalni_klienci' in switches:
        created_potential_clients = get_created_potential_clients(main_representative, start_date, end_date)
        chosen_switches.append(created_potential_clients)
    if 'oferty' in switches:
        created_offers = get_created_offers(main_representative, start_date, end_date)
        chosen_switches.append(created_offers)
    if 'leady' in switches:
        created_leads = get_created_leads(main_representative, start_date, end_date)
        chosen_switches.append(created_leads)
    if 'zadania' in switches:
        activities_on_clients = get_activities_on_clients(main_representative, start_date, end_date)
        activities_on_potential_clients = get_activities_on_potential_clients(main_representative, start_date, end_date)
        chosen_switches.append(activities_on_clients)
        chosen_switches.append(activities_on_potential_clients)
    if 'spotkania' in switches:
        meetings_with_clients = get_meetings_with_clients(main_representative, start_date, end_date)
        meetings_with_potential_clients = get_meetings_with_potential_clients(main_representative, start_date, end_date)
        chosen_switches.append(meetings_with_clients)
        chosen_switches.append(meetings_with_potential_clients)

    if len(chosen_switches) > 0:
        all_activities = pd.concat(chosen_switches)
        all_activities = all_activities.sort_values(by='date_entered', ascending=False)
        all_activities = all_activities.rename(columns={'date_entered':'Utworzono', 'task_type':'Rodzaj działania', 'name':'Nazwa klienta', 'additional_info':'Dodatkowe informacje', 'note':'Szczegóły'})
    else:
        all_activities = pd.DataFrame(columns=['date_entered', 'task_type', 'name', 'additional_info', 'note'])
        
    return all_activities

