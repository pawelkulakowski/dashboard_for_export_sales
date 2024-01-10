import pandas as pd
from datetime import date, timedelta
from database.database_connection import engine
from database.company_list import get_company_name_from_clients

def get_offers_data_from_2021(district):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT quotation_no, date_entered, expiration_date, customer_no, district_code, salesman_code, state, closed_status, reason_id, ifsapp.Order_Quotation_API.Get_Total_Sale_Price__(QUOTATION_NO) \
    FROM IFSAPP.order_quotation \
    WHERE customer_no like 'E%' \
    AND district_code = '{district}'\
    AND contract = 'Z01' \
    AND date_entered >= to_date('20210101', 'YYYYMMDD')", engine)
    offers_data = pd.DataFrame(sql_query)
    connection.close()
    offers_data = offers_data.rename(columns={'IFSAPP.ORDER_QUOTATION_API.GET_TOTAL_SALE_PRICE__(QUOTATION_NO)':'net_value'})
    return offers_data

def prepare_offers_data(district):
    df = get_offers_data_from_2021(district)

    today = date.today()
    start_of_current_cw = today - timedelta(days=today.weekday())
    end_of_current_cw = start_of_current_cw + timedelta(days=6)
    start_of_previous_cw = start_of_current_cw - timedelta(weeks=1)
    end_of_previous_cw = start_of_previous_cw + timedelta(days=6)
    
    start_of_current_cw_dt = pd.to_datetime(start_of_current_cw)
    start_of_previous_cw_dt = pd.to_datetime(start_of_previous_cw)
    end_of_previous_cw_dt = pd.to_datetime(end_of_previous_cw)
    today_dt = pd.to_datetime(today)

    # oferty z tego tygodnia
    df_this_week = df[(df['date_entered']>=start_of_current_cw_dt)&(df['state']=='Aktywowane')][['customer_no', 'quotation_no', 'net_value', 'expiration_date']].sort_values(by=['net_value'], ascending=False)
    df_this_week['expiration_date'] = df_this_week['expiration_date'].dt.date
    df_this_week['net_value'] = df_this_week['net_value'].map('{:,.2f}'.format)
    df_this_week['customer_no'] = df_this_week['customer_no'].apply(lambda x: get_company_name_from_clients(x))
    df_this_week = df_this_week.rename(columns={'customer_no':'customer_name'})
    # oferty z ostatniego tygodnia
    df_previous_week = df[(df['date_entered']>=start_of_previous_cw_dt)&(df['date_entered']<=end_of_previous_cw_dt)&(df['state']=='Aktywowane')][['customer_no', 'quotation_no', 'net_value', 'expiration_date']].sort_values(by=['net_value'], ascending=False)
    df_previous_week['expiration_date'] = df_previous_week['expiration_date'].dt.date
    df_previous_week['net_value'] = df_previous_week['net_value'].map('{:,.2f}'.format)
    df_previous_week['customer_no'] = df_previous_week['customer_no'].apply(lambda x: get_company_name_from_clients(x))
    df_previous_week = df_previous_week.rename(columns={'customer_no':'customer_name'})
    # oferty przeterminowe
    df_expired = df[(df['expiration_date']<today_dt)&(df['state']=='Aktywowane')][['customer_no', 'quotation_no', 'net_value', 'expiration_date']].sort_values(by=['expiration_date', 'net_value'], ascending=[True, False])
    df_expired['expiration_date'] = df_expired['expiration_date'].dt.date
    df_expired['net_value'] = df_expired['net_value'].map('{:,.2f}'.format)
    df_expired['customer_no'] = df_expired['customer_no'].apply(lambda x: get_company_name_from_clients(x))
    df_expired = df_expired.rename(columns={'customer_no':'customer_name'})    
    # oferty aktywowane
    df_active = df[(df['expiration_date']>today_dt)&(df['state']=='Aktywowane')][['customer_no', 'quotation_no', 'net_value', 'expiration_date']].sort_values(by=['net_value'], ascending=False)
    df_active['expiration_date'] = df_active['expiration_date'].dt.date
    df_active['net_value'] = df_active['net_value'].map('{:,.2f}'.format)
    df_active['customer_no'] = df_active['customer_no'].apply(lambda x: get_company_name_from_clients(x))
    df_active = df_active.rename(columns={'customer_no':'customer_name'})

    df_summary = pd.DataFrame(columns=['quantity'])
    df_summary.loc['Total'] = [len(df.index)]
    df_summary.loc['Aktywowane'] = [len(df_active.index)]
    df_summary.loc['Wygrane'] = [len(df[(df['closed_status']=='Wygrane')&(df['state']=='Zamknięte')]['quotation_no'].tolist())]
    df_summary.loc['Przegrane'] = [len(df[df['closed_status']=='Przegrane']['quotation_no'].tolist())]
    df_summary.loc['Anulowane'] = [len(df[df['state']=='Anulowane']['quotation_no'].tolist())]
    df_summary = df_summary.reset_index()
    df_summary = df_summary.rename(columns={'index':'status'})
    
    df_problems = pd.DataFrame(columns=['quantity', 'offers_no'])
    df_problems.loc['Skorygowane'] = [len(df[df['state']=='Skorygowane']['quotation_no'].tolist()), [str(i)+', ' for i in df[df['state']=='Skorygowane']['quotation_no'].tolist()]]
    df_problems.loc['Zaplanowane'] = [len(df[df['state']=='Zaplanowane']['quotation_no'].tolist()), [str(i)+', ' for i in df[df['state']=='Zaplanowane']['quotation_no'].tolist()]]
    df_problems.loc['Brak daty ważności'] = [len(df[(df['expiration_date'].isna())&(df['state']=='Aktywowane')]['quotation_no'].tolist()), [str(i)+', ' for i in df[(df['expiration_date'].isna())&(df['state']=='Aktywowane')]['quotation_no'].tolist()]]
    df_problems.loc['Wygrane - niezamknięte'] = [len(df[(df['closed_status']=='Wygrane')&(df['state']!='Zamknięte')]['quotation_no'].tolist()), [str(i)+', ' for i in df[(df['closed_status']=='Wygrane')&(df['state']!='Zamknięte')]['quotation_no'].tolist()]]
    df_problems.loc['Przeterminowane'] = [len(df_expired.index), '']
    df_problems = df_problems.reset_index()
    df_problems = df_problems.rename(columns={'index':'status'})

    return df_this_week, df_previous_week, df_expired, df_active, df_summary, df_problems




