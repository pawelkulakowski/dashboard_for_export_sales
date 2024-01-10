import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.express as px
from database.database_connection import engine

def get_leads_data():
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT ifsapp.business_lead.lead_id, ifsapp.business_lead.name, ifsapp.business_lead.creation_date, ifsapp.business_lead.stage_id, ifsapp.business_lead.main_representative_id \
    FROM ifsapp.business_lead \
    WHERE main_representative_id IN ('DSTUKUS', 'AOLSZEWS', 'DSUJEWIC', 'ALINKIEW', 'PKULAKOW', 'ADUDKA', 'AGOLEBIO')", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df

def get_last_lead_contact():
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT MAX(ifsapp.business_activity.start_date), ifsapp.business_activity.connection_id \
    FROM ifsapp.business_activity \
    WHERE ifsapp.business_activity.main_representative_id IN ('DSTUKUS', 'HGLADYSZ', 'AOLSZEWS', 'OMARCHEN', 'DSUJEWIC', 'MBIEZYNS', 'PILNICKI', 'PKULAKOW', 'ALINKIEW', 'ADUDKA', 'AGOLEBIO') \
    AND ifsapp.business_activity.connection_id <> 'Z01' \
    AND ifsapp.business_activity.connection_id NOT LIKE 'E%' \
    GROUP BY ifsapp.business_activity.connection_id ", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df



# Getting number of leads by region from database
def get_number_of_leads_by_region():
    current_year = datetime.datetime.today().year
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT * FROM \
    (SELECT \
    CASE \
        WHEN ifsapp.business_lead.main_representative_id = 'DSUJEWIC' THEN 'DE' \
        WHEN ifsapp.business_lead.main_representative_id = 'AGOLEBIO' THEN 'HU' \
        WHEN ifsapp.business_lead.main_representative_id = 'PKULAKOW' THEN 'IT' \
        WHEN ifsapp.business_lead.main_representative_id = 'ADUDKA' THEN 'NL' \
        WHEN ifsapp.business_lead.main_representative_id = 'ALINKIEW' THEN 'PE' \
        WHEN ifsapp.business_lead.main_representative_id = 'AOLSZEWS' THEN 'RU' \
        WHEN ifsapp.business_lead.main_representative_id = 'DSTUKUS' THEN 'VN' \
    END AS REGION, \
    TO_CHAR(ifsapp.business_lead.creation_date, 'Q') AS QUARTER, \
    COUNT(ifsapp.business_lead.lead_id) AS TOTAL \
    FROM ifsapp.business_lead \
    WHERE TO_CHAR(ifsapp.business_lead.creation_date, 'YYYY') = {current_year} \
    GROUP BY ifsapp.business_lead.main_representative_id, TO_CHAR(ifsapp.business_lead.creation_date, 'Q')) \
    WHERE REGION IS NOT NULL \
    ORDER BY REGION, QUARTER", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df

# Getting number of potential clients by region from database
def get_number_of_potential_clients_by_region():
    current_year = datetime.datetime.today().year
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT \
    CASE \
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-DE' THEN 'DE'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-HU' THEN 'HU'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-IT' THEN 'IT'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-NL' THEN 'NL'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-PE' THEN 'PE'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-RU' THEN 'RU'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-VN' THEN 'VN'\
    END \
    AS REGION, \
    TO_CHAR(ifsapp.customer_info_cfv.creation_date, 'Q') AS QUARTER, \
    COUNT(ifsapp.cust_ord_customer_address_ent.customer_id) AS TOTAL \
    FROM ifsapp.cust_ord_customer_address_ent \
    LEFT JOIN ifsapp.customer_info_cfv \
    ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.customer_info_cfv.customer_id \
    WHERE \
    ifsapp.cust_ord_customer_address_ent.district_code IN ('ME-DE', 'ME-HU', 'ME-NL', 'ME-IT', 'ME-PE', 'ME-RU', 'ME-VN') \
    AND ifsapp.customer_info_cfv.customer_category = 'Potencjalny klient' \
    AND TO_CHAR(ifsapp.customer_info_cfv.creation_date, 'YYYY') = {current_year} \
    GROUP BY ifsapp.cust_ord_customer_address_ent.district_code, \
    TO_CHAR(ifsapp.customer_info_cfv.creation_date, 'Q') \
    ORDER BY REGION, QUARTER", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df

# Getting leads by stage, region and last contact
def get_of_leads_by_stage_region_contact():
    current_year = datetime.datetime.today().year
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT \
    CASE WHEN ifsapp.business_lead.stage_id IS NULL THEN 'Poziom zero' ELSE ifsapp.business_lead.stage_id END AS STAGE_ID, \
    CASE \
        WHEN ifsapp.business_lead.main_representative_id = 'DSUJEWIC' THEN 'DE' \
       WHEN ifsapp.business_lead.main_representative_id = 'AGOLEBIO' THEN 'HU' \
        WHEN ifsapp.business_lead.main_representative_id = 'PKULAKOW' THEN 'IT' \
        WHEN ifsapp.business_lead.main_representative_id = 'ADUDKA' THEN 'NL' \
        WHEN ifsapp.business_lead.main_representative_id = 'ALINKIEW' THEN 'PE' \
        WHEN ifsapp.business_lead.main_representative_id = 'AOLSZEWS' THEN 'RU' \
        WHEN ifsapp.business_lead.main_representative_id = 'DSTUKUS' THEN 'VN' \
    END AS REGION, \
    ifsapp.business_lead.name, \
    MAX(ifsapp.business_activity.start_date) AS LAST_CONTACT \
    FROM ifsapp.business_lead \
    LEFT JOIN ifsapp.business_activity \
    ON ifsapp.business_lead.lead_id = ifsapp.business_activity.connection_id \
    WHERE ifsapp.business_lead.main_representative_id IN ('DSTUKUS', 'AOLSZEWS', 'DSUJEWIC', 'ALINKIEW', 'PKULAKOW', 'ADUDKA', 'AGOLEBIO') \
    GROUP BY ifsapp.business_lead.stage_id, ifsapp.business_lead.main_representative_id, ifsapp.business_lead.name", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df

# Getting potential clients by stage, region and last contact
def get_potential_clients_by_stage_region_contact():
    current_year = datetime.datetime.today().year
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT \
    CASE WHEN ifsapp.customer_info_cfv.cf$_etap IS NULL THEN 'Poziom zero' ELSE ifsapp.customer_info_cfv.cf$_etap END AS STAGE_ID, \
    CASE \
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-DE' THEN 'DE'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-HU' THEN 'HU'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-IT' THEN 'IT'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-NL' THEN 'NL'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-PE' THEN 'PE'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-RU' THEN 'RU'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-VN' THEN 'VN'\
    END AS REGION, \
    ifsapp.cust_ord_customer_address_ent.customer_id, \
    ifsapp.customer_info_cfv.name, \
    MAX(ifsapp.business_activity.start_date) AS LAST_CONTACT \
    FROM ifsapp.cust_ord_customer_address_ent \
    LEFT JOIN ifsapp.customer_info_cfv \
    ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.customer_info_cfv.customer_id \
    LEFT JOIN ifsapp.business_activity \
    ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.business_activity.connection_id \
    WHERE ifsapp.cust_ord_customer_address_ent.district_code IN ('ME-DE', 'ME-HU', 'ME-NL', 'ME-IT', 'ME-PE', 'ME-RU', 'ME-VN') \
    AND ifsapp.customer_info_cfv.customer_category = 'Potencjalny klient' \
    GROUP BY ifsapp.customer_info_cfv.cf$_etap, ifsapp.cust_ord_customer_address_ent.district_code, ifsapp.cust_ord_customer_address_ent.customer_id, ifsapp.customer_info_cfv.name", engine)


    df = pd.DataFrame(sql_query)
    connection.close()
    return df

# Getting lost clients by stage, region and last contact
def get_lost_clients_by_stage_region_contact():
    one_year_from_today = (datetime.datetime.today() -  datetime.timedelta(days=365)).date().strftime('%Y%m%d')
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT \
    CASE WHEN ifsapp.customer_info_cfv.cf$_etap IS NULL THEN 'Poziom zero' ELSE ifsapp.customer_info_cfv.cf$_etap END AS STAGE_ID, \
    CASE \
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-DE' THEN 'DE'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-HU' THEN 'HU'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-IT' THEN 'IT'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-NL' THEN 'NL'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-PE' THEN 'PE'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-RU' THEN 'RU'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-VN' THEN 'VN'\
        END AS REGION, \
        ifsapp.cust_ord_customer_address_ent.customer_id, \
        ifsapp.customer_info_cfv.name, \
        MAX(ifsapp.business_activity.start_date) AS LAST_CONTACT \
        FROM ifsapp.cust_ord_customer_address_ent \
        LEFT JOIN ifsapp.customer_info_cfv \
        ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.customer_info_cfv.customer_id \
        LEFT JOIN ifsapp.business_activity \
        ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.business_activity.connection_id \
        WHERE ifsapp.cust_ord_customer_address_ent.district_code IN ('ME-DE', 'ME-HU', 'ME-NL', 'ME-IT', 'ME-PE', 'ME-RU', 'ME-VN') \
        AND ifsapp.customer_info_cfv.customer_id IN (\
            SELECT IDENTITY FROM (\
                SELECT\
                ifsapp.customer_order_inv_item_join.identity\
                ,MAX(ifsapp.customer_order_inv_item_join.invoice_date) AS LAST_INVOICED_DATE\
                FROM ifsapp.customer_order_inv_item_join\
                WHERE\
                ifsapp.customer_order_inv_item_join.identity LIKE 'E%'\
                GROUP BY \
                ifsapp.customer_order_inv_item_join.identity)\
                WHERE LAST_INVOICED_DATE <= to_date( '{one_year_from_today}', 'YYYYMMDD' )\
        )\
    GROUP BY ifsapp.customer_info_cfv.cf$_etap, ifsapp.cust_ord_customer_address_ent.district_code, ifsapp.cust_ord_customer_address_ent.customer_id, ifsapp.customer_info_cfv.name", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df

# Getting value of open offers of all potential clients
def get_value_of_open_offers_for_potential_clients():
    current_year = datetime.datetime.today().year
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT ifsapp.order_quotation.customer_no, SUM(ifsapp.Order_Quotation_API.Get_Total_Sale_Price__(QUOTATION_NO)) AS OPEN_OFFER \
    FROM ifsapp.order_quotation \
    WHERE ifsapp.order_quotation.customer_no IN (SELECT \
        ifsapp.cust_ord_customer_address_ent.customer_id \
        FROM ifsapp.cust_ord_customer_address_ent \
        LEFT JOIN ifsapp.customer_info_cfv \
        ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.customer_info_cfv.customer_id \
        WHERE ifsapp.cust_ord_customer_address_ent.district_code IN ('ME-DE', 'ME-HU', 'ME-NL', 'ME-IT', 'ME-PE', 'ME-RU', 'ME-VN') \
        AND ifsapp.customer_info_cfv.customer_category = 'Potencjalny klient') \
    AND ifsapp.order_quotation.state = 'Aktywowane' \
    GROUP BY ifsapp.order_quotation.customer_no", engine)
    
    df = pd.DataFrame(sql_query)
    connection.close()
    return df

# Getting activities based on click
def get_activities_by_company_lead_number_two(company_id):
    if company_id is None:
        df = pd.DataFrame(columns=['start_date', 'description', 'calendar_activity_type', 'note', 'completed_date'])
    else:
        connection = engine.connect()
        sql_query = pd.read_sql_query(f"SELECT start_date, description, calendar_activity_type, note, completed_date FROM ifsapp.business_activity \
        WHERE ifsapp.business_activity.connection_id = '{company_id}' \
        ORDER BY start_date DESC", engine)
        df = pd.DataFrame(sql_query)
        connection.close()
        if not df.empty:
            df['start_date'] = df['start_date'].dt.date
            df['completed_date'] = pd.to_datetime(df['completed_date'], errors='coerce').dt.date
            #df['completed_date'] = df['completed_date'].dt.date
    
    return df

def generate_total_leads_by_year_fig():
    df = get_leads_data()
    df['year'] = df['creation_date'].dt.year
    df.loc[df['main_representative_id'] == 'DSUJEWIC', 'region' ] = 'ME-DE'
    df.loc[df['main_representative_id'] == 'AGOLEBIO', 'region' ] = 'ME-HU'
    df.loc[df['main_representative_id'] == 'PKULAKOW', 'region' ] = 'ME-IT'
    df.loc[df['main_representative_id'] == 'ADUDKA', 'region' ] = 'ME-NL'
    df.loc[df['main_representative_id'] == 'ALINKIEW', 'region' ] = 'ME-PE'
    df.loc[df['main_representative_id'] == 'AOLSZEWS', 'region' ] = 'ME-RU'
    df.loc[df['main_representative_id'] == 'DSTUKUS', 'region' ] = 'ME-VN'
    df['stage_id'] = df['stage_id'].fillna('Brak')
    
    # Prepare general graph with leads set by year

    colors = ['lightgray',] * 6
    colors[4] = 'darkblue'
    colors[5] = 'orange'

    zz = df.groupby('year', as_index=False)['name'].count()
    fig = go.Figure(data=[go.Bar(
                x=zz['year'], y=zz['name'],
                text=zz['name'],
                textposition='outside',
                marker_color=colors,
            )])
    fig.update_layout(template='plotly_white', title="Liczba dodanych lead'ów")
    fig.update_xaxes(showgrid=False, dtick=1)
    fig.update_yaxes(showgrid=False, visible=False)
    fig.update_layout(title_font=dict(color='gray'), height=600, width=600)

    # Prepare graph for leads by region in years - dynamic

    leads_by_regions_in_years = df.groupby(['region', 'year'], as_index=False)['name'].count()
    grouping = leads_by_regions_in_years.groupby(['region'])['name']
    leads_by_regions_in_years['cumsum'] = grouping.cumsum()
    leads_by_regions_in_years = leads_by_regions_in_years.pivot_table(index='region', columns='year', values='cumsum').fillna(0).reset_index()
    leads_by_regions_in_years = pd.melt(leads_by_regions_in_years, id_vars=['region']).sort_values(by=['region','year'], ascending=True)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        y=leads_by_regions_in_years[leads_by_regions_in_years['region']=='ME-DE']['value'], 
        x=leads_by_regions_in_years[leads_by_regions_in_years['region']=='ME-DE']['year'],
        mode='lines',
        name='ME-DE',
        marker_color='#000814'))
    fig2.add_trace(go.Scatter(
        y=leads_by_regions_in_years[leads_by_regions_in_years['region']=='ME-HU']['value'], 
        x=leads_by_regions_in_years[leads_by_regions_in_years['region']=='ME-HU']['year'],
        mode='lines',
        name='ME-HU'))
    fig2.add_trace(go.Scatter(
        y=leads_by_regions_in_years[leads_by_regions_in_years['region']=='ME-IT']['value'], 
        x=leads_by_regions_in_years[leads_by_regions_in_years['region']=='ME-IT']['year'],
        mode='lines',
        name='ME-IT'))
    fig2.add_trace(go.Scatter(
        y=leads_by_regions_in_years[leads_by_regions_in_years['region']=='ME-NL']['value'], 
        x=leads_by_regions_in_years[leads_by_regions_in_years['region']=='ME-NL']['year'],
        mode='lines',
        name='ME-NL'))
    fig2.add_trace(go.Scatter(
        y=leads_by_regions_in_years[leads_by_regions_in_years['region']=='ME-PE']['value'], 
        x=leads_by_regions_in_years[leads_by_regions_in_years['region']=='ME-PE']['year'],
        mode='lines',
        name='ME-PE'))
    fig2.add_trace(go.Scatter(
        y=leads_by_regions_in_years[leads_by_regions_in_years['region']=='ME-RU']['value'], 
        x=leads_by_regions_in_years[leads_by_regions_in_years['region']=='ME-RU']['year'],
        mode='lines',
        name='ME-RU'))
    fig2.add_trace(go.Scatter(
        y=leads_by_regions_in_years[leads_by_regions_in_years['region']=='ME-VN']['value'], 
        x=leads_by_regions_in_years[leads_by_regions_in_years['region']=='ME-VN']['year'],
        mode='lines',
        name='ME-VN'))

    fig2.update_xaxes(showgrid=False, dtick=1)
    fig2.update_yaxes(showgrid=False)
    fig2.update_layout(template='plotly_white',height=600, width=600)

    # Prepare DF with statuses of leads
    # statusofleads = df.pivot_table(index='region', columns='stage_id', values='name', aggfunc='count').fillna(0)
    #statusofleads = statusofleads[['Brak', 'Akcja zaczepna', 'Wstępny', 'Zainteresowany', 'Niezainteresowany', 'Wstrzymany', 'Zamknięty']]
    #statusofleads = statusofleads.astype(int)
    #statusofleads = statusofleads.reset_index()
    
    return fig, fig2

def generate_data_for_last_contact_leads_table():
    df = get_leads_data()
    df.loc[df['main_representative_id'] == 'DSUJEWIC', 'region' ] = 'ME-DE'
    df.loc[df['main_representative_id'] == 'AGOLEBIO', 'region' ] = 'ME-HU'
    df.loc[df['main_representative_id'] == 'PKULAKOW', 'region' ] = 'ME-IT'
    df.loc[df['main_representative_id'] == 'ADUDKA', 'region' ] = 'ME-NL'
    df.loc[df['main_representative_id'] == 'ALINKIEW', 'region' ] = 'ME-PE'
    df.loc[df['main_representative_id'] == 'AOLSZEWS', 'region' ] = 'ME-RU'
    df.loc[df['main_representative_id'] == 'DSTUKUS', 'region' ] = 'ME-VN'
    df['stage_id'] = df['stage_id'].fillna('Brak działań')
    
    df_last = get_last_lead_contact()
    df_last = df_last.rename(columns={'connection_id':'lead_id', 'MAX(IFSAPP.BUSINESS_ACTIVITY.START_DATE)':'last_contact'})
    df = pd.merge(left=df, right=df_last, on='lead_id', how='left')
    df['year'] = df['last_contact'].dt.year
    df['year'] = df['year'].fillna(0)
    
    totalleadsbyregion = df[df['stage_id']!='Zamknięty'].groupby('region', as_index=False)['name'].count()
    whenlastcontacted = df.pivot_table(index='region', columns=df['last_contact'].dt.year, values='name', aggfunc='count').fillna(0)
    whenlastcontacted = pd.merge(left=whenlastcontacted, right=totalleadsbyregion, on='region', how='left')
    whenlastcontacted = whenlastcontacted.rename(columns={'name':'total'})
    whenlastcontactedfull = pd.DataFrame(columns=['region', 2018.0, 2019.0, 2020.0, 2021.0, 2022.0])
    whenlastcontacted = whenlastcontactedfull.append(whenlastcontacted).fillna(0.0)
    whenlastcontacted['without_any'] = whenlastcontacted['total'] - whenlastcontacted[2022.0] - whenlastcontacted[2021.0] - whenlastcontacted[2020.0] - whenlastcontacted[2019.0] - whenlastcontacted[2018.0]
    whenlastcontacted['used'] = round(whenlastcontacted[2022.0] / whenlastcontacted['total']*100,2)
    whenlastcontacted = whenlastcontacted.rename(columns={2018.0:2018, 2019.0:2019, 2020.0:2020, 2021.0:2021, 2022.0:2022, 'without_any':'Bez działań', 'used':'Wykorzystanie'})
    whenlastcontacted['Bez działań w 2022 roku'] = whenlastcontacted['total'] - whenlastcontacted[2022]
    whenlastcontacted = whenlastcontacted[['region','Bez działań', 2018, 2019, 2020, 2021, 2022, 'Bez działań w 2022 roku', 'Wykorzystanie']]
    whenlastcontacted[whenlastcontacted.columns[1:-1]] = whenlastcontacted[whenlastcontacted.columns[1:-1]].astype(int)
    
    leadstocontact = pd.pivot_table(df[df['year']!=2022], index=['region'], columns='year', values=['name'], aggfunc=lambda x:list(x))
    leadstocontact = leadstocontact.droplevel(0,axis=1).reset_index().rename_axis(columns=None)
    leadstocontact = leadstocontact.rename(columns={0.0:'Bez działań', 2018.0:2018, 2019.0:2019, 2020.0:2020, 2021.0:2021})
    return whenlastcontacted, leadstocontact


# Generating table with created leads in current year quarterly
def generate_number_of_leads_by_region():
    current_year = datetime.datetime.today().year
    df = get_number_of_leads_by_region()
    df_quarter = pd.DataFrame(data={f'{current_year}':[1,2,3,4]})
    df = df.pivot_table(index='quarter', columns='region', values='total').reset_index()
    df = pd.concat([df_quarter, df], axis=1).fillna(0).astype(int)
    df = df.drop(columns=['quarter'])
    df.iat[0,0] = 'Q1'
    df.iat[1,0] = 'Q2'
    df.iat[2,0] = 'Q3'
    df.iat[3,0] = 'Q4'
    return df

# Generating table with created potential clients in current year quarterly
def generate_number_of_potential_clients_by_region():
    current_year = datetime.datetime.today().year
    df = get_number_of_potential_clients_by_region()
    df_quarter = pd.DataFrame(data={f'{current_year}':[1,2,3,4]})
    df = df.pivot_table(index='quarter', columns='region', values='total').reset_index()
    df = pd.concat([df_quarter, df], axis=1).fillna(0).astype(int)
    df = df.drop(columns=['quarter'])
    df.iat[0,0] = 'Q1'
    df.iat[1,0] = 'Q2'
    df.iat[2,0] = 'Q3'
    df.iat[3,0] = 'Q4'
    return df

# Generating tables with leads
def generate_of_leads_by_stage_region_contact():
    df = get_of_leads_by_stage_region_contact()
    current_year = datetime.datetime.today().year
    one_m = datetime.datetime.now() - datetime.timedelta(days=30)
    three_m = datetime.datetime.now() - datetime.timedelta(days=90)
    
    # Creating a table with total leads in different stages
    df_0 = df[df['stage_id'].isin(['Poziom zero', 'Akcja zaczepna', 'Wstępny', 'Zainteresowany'])].pivot_table(index='stage_id', columns='region', values='name', aggfunc='count').fillna(0).astype(int).reset_index()
    df_0 = df_0.set_index('stage_id')
    df_0.loc['TOTAL'] = df_0.sum()
    df_0 = df_0.reset_index()
    stages = ['TOTAL', 'Poziom zero', 'Akcja zaczepna', 'Wstępny', 'Zainteresowany']
    df_0['stage_id'] = pd.Categorical(df_0['stage_id'], categories = stages)
    df_0 = df_0.sort_values(by = 'stage_id')
    
    dff = df[df['stage_id'].isin(['Poziom zero', 'Akcja zaczepna', 'Wstępny', 'Zainteresowany'])]
    dff['this_year'] = dff['last_contact'].dt.year.fillna(0).astype(int)
    df_1 = dff[dff['stage_id'].isin(['Poziom zero', 'Akcja zaczepna', 'Wstępny', 'Zainteresowany'])].groupby('region', as_index=False)['name'].count()
    df_1 = df_1.rename(columns={'name':'total'})
    df_2 = dff[(dff['stage_id'].isin(['Poziom zero', 'Akcja zaczepna', 'Wstępny', 'Zainteresowany']))&(dff['this_year']==current_year)].groupby('region', as_index=False)['name'].count()
    df_2 = df_2.rename(columns={'name':f'{current_year}'})
    df_3 = dff[(dff['stage_id'].isin(['Poziom zero', 'Akcja zaczepna', 'Wstępny', 'Zainteresowany']))&(dff['last_contact']>=one_m)].groupby('region', as_index=False)['name'].count()
    df_3 = df_3.rename(columns={'name':'1M'})
    df_4 = dff[(dff['stage_id'].isin(['Poziom zero', 'Akcja zaczepna', 'Wstępny', 'Zainteresowany']))&(dff['last_contact']>=three_m)].groupby('region', as_index=False)['name'].count()
    df_4 = df_4.rename(columns={'name':'3M'})
    df_1 = pd.merge(left=df_1, right=df_2, on='region', how='outer')
    df_1 = pd.merge(left=df_1, right=df_3, on='region', how='outer')
    df_1 = pd.merge(left=df_1, right=df_4, on='region', how='outer')
    df_1 = df_1.fillna(0)
    df_1['2022_'] = df_1['2022'] / df_1['total']
    df_1['2022_'] = df_1['2022_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_1['3M_'] = df_1['3M'] / df_1['total']
    df_1['3M_'] = df_1['3M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_1['1M_'] = df_1['1M'] / df_1['total']
    df_1['1M_'] = df_1['1M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_1 = df_1[['region', '2022_', '3M_', '1M_']]
    df_1 = df_1.rename(columns={'2022_':'2022', '3M_':'3M', '1M_':'1M'}).set_index('region')
    df_1 = df_1.T.reset_index()
    df_1 = df_1.rename(columns={'index':'period'})

    #Akcja zaczepna
    dff = df[df['stage_id'].isin(['Akcja zaczepna'])]
    df_5 = dff.groupby('region', as_index=False)['name'].count()
    df_5 = df_5.rename(columns={'name':'total'})
    df_6 = dff[(dff['stage_id'].isin(['Akcja zaczepna']))&(dff['last_contact']>=one_m)].groupby('region', as_index=False)['name'].count()
    df_6 = df_6.rename(columns={'name':'1M'})
    df_7 = dff[(dff['stage_id'].isin(['Akcja zaczepna']))&(dff['last_contact']>=three_m)].groupby('region', as_index=False)['name'].count()
    df_7 = df_7.rename(columns={'name':'3M'})
    df_5 = pd.merge(left=df_5, right=df_6, on='region', how='outer')
    df_5 = pd.merge(left=df_5, right=df_7, on='region', how='outer')
    df_5 = df_5.fillna(0)
    df_5['3M_'] = df_5['3M'] / df_5['total']
    df_5['3M_'] = df_5['3M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_5['1M_'] = df_5['1M'] / df_5['total']
    df_5['1M_'] = df_5['1M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_5 = df_5[['region', '3M_', '1M_']]
    df_5 = df_5.rename(columns={'3M_':'3M', '1M_':'1M'}).set_index('region')
    df_5 = df_5.T.reset_index()
    df_5 = df_5.rename(columns={'index':'Akcja zaczepna'})

    #Wstępny
    dff = df[df['stage_id'].isin(['Wstępny'])]
    df_8 = dff.groupby('region', as_index=False)['name'].count()
    df_8 = df_8.rename(columns={'name':'total'})
    df_6 = dff[(dff['stage_id'].isin(['Wstępny']))&(dff['last_contact']>=one_m)].groupby('region', as_index=False)['name'].count()
    df_6 = df_6.rename(columns={'name':'1M'})
    df_7 = dff[(dff['stage_id'].isin(['Wstępny']))&(dff['last_contact']>=three_m)].groupby('region', as_index=False)['name'].count()
    df_7 = df_7.rename(columns={'name':'3M'})
    df_8 = pd.merge(left=df_8, right=df_6, on='region', how='outer')
    df_8 = pd.merge(left=df_8, right=df_7, on='region', how='outer')
    df_8 = df_8.fillna(0)
    df_8['3M_'] = df_8['3M'] / df_8['total']
    df_8['3M_'] = df_8['3M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_8['1M_'] = df_8['1M'] / df_8['total']
    df_8['1M_'] = df_8['1M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_8 = df_8[['region', '3M_', '1M_']]
    df_8 = df_8.rename(columns={'3M_':'3M', '1M_':'1M'}).set_index('region')
    df_8 = df_8.T.reset_index()
    df_8 = df_8.rename(columns={'index':'Wstępny'})

    #Zainteresowany
    dff = df[df['stage_id'].isin(['Zainteresowany'])]
    df_9 = dff.groupby('region', as_index=False)['name'].count()
    df_9 = df_9.rename(columns={'name':'total'})
    df_6 = dff[(dff['stage_id'].isin(['Zainteresowany']))&(dff['last_contact']>=one_m)].groupby('region', as_index=False)['name'].count()
    df_6 = df_6.rename(columns={'name':'1M'})
    df_7 = dff[(dff['stage_id'].isin(['Zainteresowany']))&(dff['last_contact']>=three_m)].groupby('region', as_index=False)['name'].count()
    df_7 = df_7.rename(columns={'name':'3M'})
    df_9 = pd.merge(left=df_9, right=df_6, on='region', how='outer')
    df_9 = pd.merge(left=df_9, right=df_7, on='region', how='outer')
    df_9 = df_9.fillna(0)
    df_9['3M_'] = df_9['3M'] / df_9['total']
    df_9['3M_'] = df_9['3M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_9['1M_'] = df_9['1M'] / df_9['total']
    df_9['1M_'] = df_9['1M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_9 = df_9[['region', '3M_', '1M_']]
    df_9 = df_9.rename(columns={'3M_':'3M', '1M_':'1M'}).set_index('region')
    df_9 = df_9.T.reset_index()
    df_9 = df_9.rename(columns={'index':'Zainteresowany'})

    active_leads = df_0
    leads_usage = df_1
    action_leads = df_5
    initial_leads = df_8
    interested_leads = df_9

    df_off = df[~df['stage_id'].isin(['Poziom zero', 'Akcja zaczepna', 'Wstępny', 'Zainteresowany'])].pivot_table(index='stage_id', columns='region', values='name', aggfunc='count').fillna(0).astype(int).reset_index()
    stages = ['Wstrzymany', 'Niezainteresowany', 'Zamknięty', 'ASME']
    df_off['stage_id'] = pd.Categorical(df_off['stage_id'], categories = stages)
    df_off = df_off.sort_values(by = 'stage_id')
    #df_off = df_off.set_index('stage_id')

    leftovers = df_off

    return active_leads, leads_usage, action_leads, initial_leads, interested_leads, leftovers
    


# Generating tables with potential clients
def generate_of_potential_clients_by_stage_region_contact():
    df = get_potential_clients_by_stage_region_contact()
    df2 = get_value_of_open_offers_for_potential_clients()
    df2 = df2.rename(columns={'customer_no':'customer_id'})
    df = pd.merge(left=df, right=df2, on='customer_id', how='left')
    #df.loc[df['open_offer']>0, 'stage_id'] = 'OTWARTA OFERTA'


    current_year = datetime.datetime.today().year
    one_m = datetime.datetime.now() - datetime.timedelta(days=30)
    three_m = datetime.datetime.now() - datetime.timedelta(days=90)
    
    # Creating a table with total leads in different stages
    df_0 = df[df['stage_id'].isin(['Poziom zero','Akcja zaczepna', 'Wstępny', 'Zainteresowany'])].pivot_table(index='stage_id', columns='region', values='name', aggfunc='count').fillna(0).astype(int).reset_index()
    df_0 = df_0.set_index('stage_id')
    df_0.loc['TOTAL'] = df_0.sum()
    df_0 = df_0.reset_index()
    stages = ['TOTAL', 'Poziom zero', 'Akcja zaczepna', 'Wstępny', 'Zainteresowany']

    df_0['stage_id'] = pd.Categorical(df_0['stage_id'], categories = stages)
    df_0 = df_0.sort_values(by = 'stage_id')        
    
    stages = ['Poziom zero', 'Akcja zaczepna', 'Wstępny', 'Zainteresowany']
    # 'Brak działań', 'Brak kontaktu', Zainteresowany/Wstrzymany', 'Niezainteresowany'
    dff = df[df['stage_id'].isin(stages)]
    dff['this_year'] = dff['last_contact'].dt.year.fillna(0).astype(int)
    df_1 = dff[dff['stage_id'].isin(stages)].groupby('region', as_index=False)['name'].count()
    df_1 = df_1.rename(columns={'name':'total'})
    df_2 = dff[(dff['stage_id'].isin(stages))&(dff['this_year']==current_year)].groupby('region', as_index=False)['name'].count()
    df_2 = df_2.rename(columns={'name':f'{current_year}'})
    df_3 = dff[(dff['stage_id'].isin(stages))&(dff['last_contact']>=one_m)].groupby('region', as_index=False)['name'].count()
    df_3 = df_3.rename(columns={'name':'1M'})
    df_4 = dff[(dff['stage_id'].isin(stages))&(dff['last_contact']>=three_m)].groupby('region', as_index=False)['name'].count()
    df_4 = df_4.rename(columns={'name':'3M'})
    df_1 = pd.merge(left=df_1, right=df_2, on='region', how='outer')
    df_1 = pd.merge(left=df_1, right=df_3, on='region', how='outer')
    df_1 = pd.merge(left=df_1, right=df_4, on='region', how='outer')
    df_1 = df_1.fillna(0)
    df_1['2022_'] = df_1['2022'] / df_1['total']
    df_1['2022_'] = df_1['2022_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_1['3M_'] = df_1['3M'] / df_1['total']
    df_1['3M_'] = df_1['3M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_1['1M_'] = df_1['1M'] / df_1['total']
    df_1['1M_'] = df_1['1M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_1 = df_1[['region', '2022_', '3M_', '1M_']]
    df_1 = df_1.rename(columns={'2022_':'2022', '3M_':'3M', '1M_':'1M'}).set_index('region')
    df_1 = df_1.T.reset_index()
    df_1 = df_1.rename(columns={'index':'period'})

    #Akcja zaczepna
    dff = df[df['stage_id'].isin(['Akcja zaczepna'])]
    df_5 = dff.groupby('region', as_index=False)['name'].count()
    df_5 = df_5.rename(columns={'name':'total'})
    df_6 = dff[(dff['stage_id'].isin(['Akcja zaczepna']))&(dff['last_contact']>=one_m)].groupby('region', as_index=False)['name'].count()
    df_6 = df_6.rename(columns={'name':'1M'})
    df_7 = dff[(dff['stage_id'].isin(['Akcja zaczepna']))&(dff['last_contact']>=three_m)].groupby('region', as_index=False)['name'].count()
    df_7 = df_7.rename(columns={'name':'3M'})
    df_x = pd.DataFrame(data={'region':['DE', 'HU', 'IT', 'NL', 'PE', 'RU', 'VN']}) #to
    df_5 = pd.merge(left=df_x, right=df_5, on='region', how='outer') #to
    df_5 = pd.merge(left=df_5, right=df_6, on='region', how='outer')
    df_5 = pd.merge(left=df_5, right=df_7, on='region', how='outer')
    df_5 = df_5.fillna(0)
    df_5['3M_'] = df_5['3M'] / df_5['total']
    df_5['3M_'] = df_5['3M_'].fillna(0) #to
    df_5['3M_'] = df_5['3M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_5['1M_'] = df_5['1M'] / df_5['total']
    df_5['1M_'] = df_5['1M_'].fillna(0) # to
    df_5['1M_'] = df_5['1M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_5 = df_5[['region', '3M_', '1M_']]
    df_5 = df_5.rename(columns={'3M_':'3M', '1M_':'1M'}).set_index('region')
    df_5 = df_5.T.reset_index()
    df_5 = df_5.rename(columns={'index':'Akcja zaczepna'})

    #Wstępny
    dff = df[df['stage_id'].isin(['Wstępny'])]
    df_8 = dff.groupby('region', as_index=False)['name'].count()
    df_8 = df_8.rename(columns={'name':'total'})
    df_6 = dff[(dff['stage_id'].isin(['Wstępny']))&(dff['last_contact']>=one_m)].groupby('region', as_index=False)['name'].count()
    df_6 = df_6.rename(columns={'name':'1M'})
    df_7 = dff[(dff['stage_id'].isin(['Wstępny']))&(dff['last_contact']>=three_m)].groupby('region', as_index=False)['name'].count()
    df_7 = df_7.rename(columns={'name':'3M'})
    
    df_x = pd.DataFrame(data={'region':['DE', 'HU', 'IT', 'NL', 'PE', 'RU', 'VN']}) #to
    df_8 = pd.merge(left=df_x, right=df_8, on='region', how='outer') #to
    
    df_8 = pd.merge(left=df_8, right=df_6, on='region', how='outer')
    df_8 = pd.merge(left=df_8, right=df_7, on='region', how='outer')
    df_8 = df_8.fillna(0)
    df_8['3M_'] = df_8['3M'] / df_8['total']
    df_8['3M_'] = df_8['3M_'].fillna(0) #to
    df_8['3M_'] = df_8['3M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_8['1M_'] = df_8['1M'] / df_8['total']
    df_8['1M_'] = df_8['1M_'].fillna(0) #to
    df_8['1M_'] = df_8['1M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_8 = df_8[['region', '3M_', '1M_']]
    df_8 = df_8.rename(columns={'3M_':'3M', '1M_':'1M'}).set_index('region')
    df_8 = df_8.T.reset_index()
    df_8 = df_8.rename(columns={'index':'Wstępny'})

    #Zainteresowany
    dff = df[df['stage_id'].isin(['Zainteresowany'])]
    df_9 = dff.groupby('region', as_index=False)['name'].count()
    df_9 = df_9.rename(columns={'name':'total'})
    df_6 = dff[(dff['stage_id'].isin(['Zainteresowany']))&(dff['last_contact']>=one_m)].groupby('region', as_index=False)['name'].count()
    df_6 = df_6.rename(columns={'name':'1M'})
    df_7 = dff[(dff['stage_id'].isin(['Zainteresowany']))&(dff['last_contact']>=three_m)].groupby('region', as_index=False)['name'].count()
    df_7 = df_7.rename(columns={'name':'3M'})
    
    df_x = pd.DataFrame(data={'region':['DE', 'HU', 'IT', 'NL', 'PE', 'RU', 'VN']}) #to
    df_9 = pd.merge(left=df_x, right=df_9, on='region', how='outer') #to
    
    df_9 = pd.merge(left=df_9, right=df_6, on='region', how='outer')
    df_9 = pd.merge(left=df_9, right=df_7, on='region', how='outer')
    df_9 = df_9.fillna(0)
    df_9['3M_'] = df_9['3M'] / df_9['total']
    df_9['3M_'] = df_9['3M_'].fillna(0) #to
    df_9['3M_'] = df_9['3M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_9['1M_'] = df_9['1M'] / df_9['total']
    df_9['1M_'] = df_9['1M_'].fillna(0) #to
    df_9['1M_'] = df_9['1M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_9 = df_9[['region', '3M_', '1M_']]
    df_9 = df_9.rename(columns={'3M_':'3M', '1M_':'1M'}).set_index('region')
    df_9 = df_9.T.reset_index()
    df_9 = df_9.rename(columns={'index':'Zainteresowany'})

    #OTWARTA OFERTA
    dff = df[df['stage_id'].isin(['OTWARTA OFERTA'])]
    df_10 = dff.groupby('region', as_index=False)['name'].count()
    df_10 = df_10.rename(columns={'name':'total'})
    df_6 = dff[(dff['stage_id'].isin(['OTWARTA OFERTA']))&(dff['last_contact']>=one_m)].groupby('region', as_index=False)['name'].count()
    df_6 = df_6.rename(columns={'name':'1M'})
    df_7 = dff[(dff['stage_id'].isin(['OTWARTA OFERTA']))&(dff['last_contact']>=three_m)].groupby('region', as_index=False)['name'].count()
    df_7 = df_7.rename(columns={'name':'3M'})
    
    df_x = pd.DataFrame(data={'region':['DE', 'HU', 'IT', 'NL', 'PE', 'RU', 'VN']}) #to
    df_10 = pd.merge(left=df_x, right=df_10, on='region', how='outer') #to
    
    df_10 = pd.merge(left=df_10, right=df_6, on='region', how='outer')
    df_10 = pd.merge(left=df_10, right=df_7, on='region', how='outer')
    df_10 = df_10.fillna(0)
    df_10['3M_'] = df_10['3M'] / df_10['total']
    df_10['3M_'] = df_10['3M_'].fillna(0) #to
    df_10['3M_'] = df_10['3M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_10['1M_'] = df_10['1M'] / df_10['total']
    df_10['1M_'] = df_10['1M_'].fillna(0) #to
    df_10['1M_'] = df_10['1M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_10 = df_10[['region', '3M_', '1M_']]
    df_10 = df_10.rename(columns={'3M_':'3M', '1M_':'1M'}).set_index('region')
    df_10 = df_10.T.reset_index()
    df_10 = df_10.rename(columns={'index':'OTWARTA OFERTA'})

    active_potential_clients = df_0
    potential_clients_usage = df_1

    open_offer_potential_clients = df_10
    action_potential_clients = df_5
    initial_potential_clients = df_8
    interested_potential_clients = df_9

    df_off = df[~df['stage_id'].isin(['Poziom zero','Akcja zaczepna', 'Wstępny', 'Zainteresowany'])].pivot_table(index='stage_id', columns='region', values='name', aggfunc='count').fillna(0).astype(int).reset_index()
    #stages = ['Brak działań', 'Brak kontaktu', 'Zainteresowany/Wstrzymany', 'Wstrzymany', 'Zamknięty']
    #df_off['stage_id'] = pd.Categorical(df_off['stage_id'], categories = stages)
    #df_off = df_off.sort_values(by = 'stage_id')
    #df_off = df_off.set_index('stage_id')

    leftovers = df_off
    
    return active_potential_clients, potential_clients_usage, open_offer_potential_clients, action_potential_clients, initial_potential_clients, interested_potential_clients, leftovers
    
# Generating tables with lost clients
def generate_of_lost_clients_by_stage_region_contact():
    df = get_lost_clients_by_stage_region_contact()
    current_year = datetime.datetime.today().year
    one_m = datetime.datetime.now() - datetime.timedelta(days=30)
    three_m = datetime.datetime.now() - datetime.timedelta(days=90)
    
    # Creating a table with total leads in different stages
    df_0 = df[df['stage_id'].isin(['Poziom zero','Akcja zaczepna', 'Wstępny', 'Zainteresowany'])].pivot_table(index='stage_id', columns='region', values='name', aggfunc='count').fillna(0).astype(int).reset_index()
    df_0 = df_0.set_index('stage_id')
    df_0.loc['TOTAL'] = df_0.sum()
    df_0 = df_0.reset_index()
    stages = ['TOTAL', 'Poziom zero', 'Akcja zaczepna', 'Wstępny', 'Zainteresowany']

    df_0['stage_id'] = pd.Categorical(df_0['stage_id'], categories = stages)
    df_0 = df_0.sort_values(by = 'stage_id')        
    
    stages = ['Poziom zero', 'Akcja zaczepna', 'Wstępny', 'Zainteresowany']
    # 'Brak działań', 'Brak kontaktu', Zainteresowany/Wstrzymany', 'Niezainteresowany'
    dff = df[df['stage_id'].isin(stages)]
    dff['this_year'] = dff['last_contact'].dt.year.fillna(0).astype(int)
    df_1 = dff[dff['stage_id'].isin(stages)].groupby('region', as_index=False)['name'].count()
    df_1 = df_1.rename(columns={'name':'total'})
    df_2 = dff[(dff['stage_id'].isin(stages))&(dff['this_year']==current_year)].groupby('region', as_index=False)['name'].count()
    df_2 = df_2.rename(columns={'name':f'{current_year}'})
    df_3 = dff[(dff['stage_id'].isin(stages))&(dff['last_contact']>=one_m)].groupby('region', as_index=False)['name'].count()
    df_3 = df_3.rename(columns={'name':'1M'})
    df_4 = dff[(dff['stage_id'].isin(stages))&(dff['last_contact']>=three_m)].groupby('region', as_index=False)['name'].count()
    df_4 = df_4.rename(columns={'name':'3M'})
    df_1 = pd.merge(left=df_1, right=df_2, on='region', how='outer')
    df_1 = pd.merge(left=df_1, right=df_3, on='region', how='outer')
    df_1 = pd.merge(left=df_1, right=df_4, on='region', how='outer')
    df_1 = df_1.fillna(0)
    df_1['2022_'] = df_1['2022'] / df_1['total']
    df_1['2022_'] = df_1['2022_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_1['3M_'] = df_1['3M'] / df_1['total']
    df_1['3M_'] = df_1['3M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_1['1M_'] = df_1['1M'] / df_1['total']
    df_1['1M_'] = df_1['1M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_1 = df_1[['region', '2022_', '3M_', '1M_']]
    df_1 = df_1.rename(columns={'2022_':'2022', '3M_':'3M', '1M_':'1M'}).set_index('region')
    df_1 = df_1.T.reset_index()
    df_1 = df_1.rename(columns={'index':'period'})

    #Akcja zaczepna
    dff = df[df['stage_id'].isin(['Akcja zaczepna'])]
    df_5 = dff.groupby('region', as_index=False)['name'].count()
    df_5 = df_5.rename(columns={'name':'total'})
    df_6 = dff[(dff['stage_id'].isin(['Akcja zaczepna']))&(dff['last_contact']>=one_m)].groupby('region', as_index=False)['name'].count()
    df_6 = df_6.rename(columns={'name':'1M'})
    df_7 = dff[(dff['stage_id'].isin(['Akcja zaczepna']))&(dff['last_contact']>=three_m)].groupby('region', as_index=False)['name'].count()
    df_7 = df_7.rename(columns={'name':'3M'})
    df_x = pd.DataFrame(data={'region':['DE', 'HU', 'IT', 'NL', 'PE', 'RU', 'VN']}) #to
    df_5 = pd.merge(left=df_x, right=df_5, on='region', how='outer') #to
    df_5 = pd.merge(left=df_5, right=df_6, on='region', how='outer')
    df_5 = pd.merge(left=df_5, right=df_7, on='region', how='outer')
    df_5 = df_5.fillna(0)
    df_5['3M_'] = df_5['3M'] / df_5['total']
    df_5['3M_'] = df_5['3M_'].fillna(0) #to
    df_5['3M_'] = df_5['3M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_5['1M_'] = df_5['1M'] / df_5['total']
    df_5['1M_'] = df_5['1M_'].fillna(0) # to
    df_5['1M_'] = df_5['1M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_5 = df_5[['region', '3M_', '1M_']]
    df_5 = df_5.rename(columns={'3M_':'3M', '1M_':'1M'}).set_index('region')
    df_5 = df_5.T.reset_index()
    df_5 = df_5.rename(columns={'index':'Akcja zaczepna'})

    #Wstępny
    dff = df[df['stage_id'].isin(['Wstępny'])]
    df_8 = dff.groupby('region', as_index=False)['name'].count()
    df_8 = df_8.rename(columns={'name':'total'})
    df_6 = dff[(dff['stage_id'].isin(['Wstępny']))&(dff['last_contact']>=one_m)].groupby('region', as_index=False)['name'].count()
    df_6 = df_6.rename(columns={'name':'1M'})
    df_7 = dff[(dff['stage_id'].isin(['Wstępny']))&(dff['last_contact']>=three_m)].groupby('region', as_index=False)['name'].count()
    df_7 = df_7.rename(columns={'name':'3M'})
    
    df_x = pd.DataFrame(data={'region':['DE', 'HU', 'IT', 'NL', 'PE', 'RU', 'VN']}) #to
    df_8 = pd.merge(left=df_x, right=df_8, on='region', how='outer') #to
    
    df_8 = pd.merge(left=df_8, right=df_6, on='region', how='outer')
    df_8 = pd.merge(left=df_8, right=df_7, on='region', how='outer')
    df_8 = df_8.fillna(0)
    df_8['3M_'] = df_8['3M'] / df_8['total']
    df_8['3M_'] = df_8['3M_'].fillna(0) #to
    df_8['3M_'] = df_8['3M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_8['1M_'] = df_8['1M'] / df_8['total']
    df_8['1M_'] = df_8['1M_'].fillna(0) #to
    df_8['1M_'] = df_8['1M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_8 = df_8[['region', '3M_', '1M_']]
    df_8 = df_8.rename(columns={'3M_':'3M', '1M_':'1M'}).set_index('region')
    df_8 = df_8.T.reset_index()
    df_8 = df_8.rename(columns={'index':'Wstępny'})

    #Zainteresowany
    dff = df[df['stage_id'].isin(['Zainteresowany'])]
    df_9 = dff.groupby('region', as_index=False)['name'].count()
    df_9 = df_9.rename(columns={'name':'total'})
    df_6 = dff[(dff['stage_id'].isin(['Zainteresowany']))&(dff['last_contact']>=one_m)].groupby('region', as_index=False)['name'].count()
    df_6 = df_6.rename(columns={'name':'1M'})
    df_7 = dff[(dff['stage_id'].isin(['Zainteresowany']))&(dff['last_contact']>=three_m)].groupby('region', as_index=False)['name'].count()
    df_7 = df_7.rename(columns={'name':'3M'})
    
    df_x = pd.DataFrame(data={'region':['DE', 'HU', 'IT', 'NL', 'PE', 'RU', 'VN']}) #to
    df_9 = pd.merge(left=df_x, right=df_9, on='region', how='outer') #to
    
    df_9 = pd.merge(left=df_9, right=df_6, on='region', how='outer')
    df_9 = pd.merge(left=df_9, right=df_7, on='region', how='outer')
    df_9 = df_9.fillna(0)
    df_9['3M_'] = df_9['3M'] / df_9['total']
    df_9['3M_'] = df_9['3M_'].fillna(0) #to
    df_9['3M_'] = df_9['3M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_9['1M_'] = df_9['1M'] / df_9['total']
    df_9['1M_'] = df_9['1M_'].fillna(0) #to
    df_9['1M_'] = df_9['1M_'].apply(lambda x: "{0:.0f}%".format(x*100))
    df_9 = df_9[['region', '3M_', '1M_']]
    df_9 = df_9.rename(columns={'3M_':'3M', '1M_':'1M'}).set_index('region')
    df_9 = df_9.T.reset_index()
    df_9 = df_9.rename(columns={'index':'Zainteresowany'})

    
   

    active_lost_clients = df_0
    lost_clients_usage = df_1

    
    action_lost_clients = df_5
    initial_lost_clients = df_8
    interested_lost_clients = df_9

    df_off = df[~df['stage_id'].isin(['Poziom zero','Akcja zaczepna', 'Wstępny', 'Zainteresowany'])].pivot_table(index='stage_id', columns='region', values='name', aggfunc='count').fillna(0).astype(int).reset_index()
    
    leftovers = df_off

    return active_lost_clients, lost_clients_usage, action_lost_clients, initial_lost_clients, interested_lost_clients, leftovers
   
# PART RELATED TO UNDER CONSTRCUTIONES

def get_active_leads_details_all(region):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT \
    ifsapp.business_lead.name, \
    ifsapp.business_lead.lead_id, \
    MAX(ifsapp.business_activity.start_date) AS LAST_CONTACT, \
    DBMS_LOB.SUBSTR(ifsapp.business_lead.note,4000,1) AS NOTE \
    FROM ifsapp.business_lead \
    LEFT JOIN ifsapp.business_activity \
    ON ifsapp.business_lead.lead_id = ifsapp.business_activity.connection_id \
    WHERE \
    ifsapp.business_lead.main_representative_id = '{region}' \
    AND (ifsapp.business_lead.stage_id NOT IN ('Niezainteresowany', 'Wstrzymany', 'Zamknięty', 'ASME') OR ifsapp.business_lead.stage_id IS NULL)\
    GROUP BY ifsapp.business_lead.name, ifsapp.business_lead.lead_id, DBMS_LOB.SUBSTR(ifsapp.business_lead.note,4000,1) \
    ORDER BY MAX(ifsapp.business_activity.start_date)", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    
    return df

def get_active_leads_details_null(region):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT \
    ifsapp.business_lead.name, \
    ifsapp.business_lead.lead_id, \
    MAX(ifsapp.business_activity.start_date) AS LAST_CONTACT, \
    DBMS_LOB.SUBSTR(ifsapp.business_lead.note,4000,1) AS NOTE \
    FROM ifsapp.business_lead \
    LEFT JOIN ifsapp.business_activity \
    ON ifsapp.business_lead.lead_id = ifsapp.business_activity.connection_id \
    WHERE \
    ifsapp.business_lead.main_representative_id = '{region}' \
    AND ifsapp.business_lead.stage_id IS NULL \
    GROUP BY ifsapp.business_lead.name, ifsapp.business_lead.lead_id, DBMS_LOB.SUBSTR(ifsapp.business_lead.note,4000,1) \
    ORDER BY MAX(ifsapp.business_activity.start_date)", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df

def get_active_leads_details_by_stage(region, stage):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT \
    ifsapp.business_lead.name, \
    ifsapp.business_lead.lead_id, \
    MAX(ifsapp.business_activity.start_date) AS LAST_CONTACT, \
    DBMS_LOB.SUBSTR(ifsapp.business_lead.note,4000,1) AS NOTE \
    FROM ifsapp.business_lead \
    LEFT JOIN ifsapp.business_activity \
    ON ifsapp.business_lead.lead_id = ifsapp.business_activity.connection_id \
    WHERE \
    ifsapp.business_lead.main_representative_id = '{region}' \
    AND ifsapp.business_lead.stage_id = '{stage}' \
    GROUP BY ifsapp.business_lead.name, ifsapp.business_lead.lead_id, DBMS_LOB.SUBSTR(ifsapp.business_lead.note,4000,1) \
    ORDER BY MAX(ifsapp.business_activity.start_date)", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df

def generate_active_leads_details(region, stage):
    if region is None:
        pass
    else:
        REPRESENTATIVES = {
            'ME-DE': 'DSUJEWIC',
            'ME-HU': 'AGOLEBIO',
            'ME-IT': 'PKULAKOW',
            'ME-NL': 'ADUDKA',
            'ME-PE': 'ALINKIEW',
            'ME-RU': 'AOLSZEWS',
            'ME-VN': 'DSTUKUS'
        }
        representative = REPRESENTATIVES[region]

        if stage == 'TOTAL':
            df = get_active_leads_details_all(representative)
        if stage == 'Poziom zero':
            df = get_active_leads_details_null(representative)
        if stage in ['Akcja zaczepna', 'Wstępny', 'Zainteresowany']:
            df = get_active_leads_details_by_stage(representative, stage)
        if not df.empty:
            try:
                df['last_contact'] = df['last_contact'].dt.date
            except AttributeError:
                pass
            df['id'] = df['lead_id']
            df.set_index('id', inplace=True, drop=False)
            df = df.drop(columns=['lead_id'])
        return df

def get_activities_by_lead_number(lead_id):
    if lead_id is None:
        df = pd.DataFrame(columns=['start_date', 'description', 'calendar_activity_type', 'note'])
    else:
        connection = engine.connect()
        sql_query = pd.read_sql_query(f"SELECT start_date, description, calendar_activity_type, note FROM ifsapp.business_activity \
        WHERE ifsapp.business_activity.connection_id = '{lead_id}' \
        AND ifsapp.business_activity.connection_type = 'Namiar handlowy' \
        ORDER BY start_date DESC", engine)
        df = pd.DataFrame(sql_query)
        connection.close()
        if not df.empty:
            df['start_date'] = df['start_date'].dt.date
    return df

def get_active_potential_clients_details_all(region):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT ifsapp.cust_ord_customer_address_ent.customer_id, \
    ifsapp.customer_info_cfv.name, \
    MAX(ifsapp.business_activity.start_date) AS LAST_CONTACT, \
    DBMS_LOB.SUBSTR(ifsapp.crm_cust_info.note,4000,1) AS NOTE \
    FROM ifsapp.cust_ord_customer_address_ent \
    LEFT JOIN ifsapp.customer_info_cfv \
    ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.customer_info_cfv.customer_id \
    LEFT JOIN ifsapp.business_activity \
    ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.business_activity.connection_id \
    LEFT JOIN ifsapp.crm_cust_info \
    ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.crm_cust_info.customer_id \
    WHERE \
    ifsapp.cust_ord_customer_address_ent.district_code = '{region}' \
    AND ifsapp.customer_info_cfv.customer_category = 'Potencjalny klient'\
    AND (ifsapp.customer_info_cfv.cf$_etap IN ('Akcja zaczepna', 'Wstępny', 'Zainteresowany') OR ifsapp.customer_info_cfv.cf$_etap IS NULL)\
    GROUP BY ifsapp.cust_ord_customer_address_ent.customer_id, ifsapp.customer_info_cfv.name, DBMS_LOB.SUBSTR(ifsapp.crm_cust_info.note,4000,1)", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df

def get_active_potential_clients_details_null(region):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT ifsapp.cust_ord_customer_address_ent.customer_id, \
    ifsapp.customer_info_cfv.name, \
    MAX(ifsapp.business_activity.start_date) AS LAST_CONTACT, \
    DBMS_LOB.SUBSTR(ifsapp.crm_cust_info.note,4000,1) AS NOTE \
    FROM ifsapp.cust_ord_customer_address_ent \
    LEFT JOIN ifsapp.customer_info_cfv \
    ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.customer_info_cfv.customer_id \
    LEFT JOIN ifsapp.business_activity \
    ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.business_activity.connection_id \
    LEFT JOIN ifsapp.crm_cust_info \
    ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.crm_cust_info.customer_id \
    WHERE \
    ifsapp.cust_ord_customer_address_ent.district_code = '{region}' \
    AND ifsapp.customer_info_cfv.customer_category = 'Potencjalny klient'\
    AND ifsapp.customer_info_cfv.cf$_etap IS NULL \
    GROUP BY ifsapp.cust_ord_customer_address_ent.customer_id, ifsapp.customer_info_cfv.name, DBMS_LOB.SUBSTR(ifsapp.crm_cust_info.note,4000,1)", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df

def get_active_potential_clients_details_by_stage(region, stage):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT ifsapp.cust_ord_customer_address_ent.customer_id, \
    ifsapp.customer_info_cfv.name, \
    MAX(ifsapp.business_activity.start_date) AS LAST_CONTACT, \
    DBMS_LOB.SUBSTR(ifsapp.crm_cust_info.note,4000,1) AS NOTE \
    FROM ifsapp.cust_ord_customer_address_ent \
    LEFT JOIN ifsapp.customer_info_cfv \
    ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.customer_info_cfv.customer_id \
    LEFT JOIN ifsapp.business_activity \
    ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.business_activity.connection_id \
    LEFT JOIN ifsapp.crm_cust_info \
    ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.crm_cust_info.customer_id \
    WHERE \
    ifsapp.cust_ord_customer_address_ent.district_code = '{region}' \
    AND ifsapp.customer_info_cfv.customer_category = 'Potencjalny klient'\
    AND ifsapp.customer_info_cfv.cf$_etap = '{stage}'\
    GROUP BY ifsapp.cust_ord_customer_address_ent.customer_id, ifsapp.customer_info_cfv.name, DBMS_LOB.SUBSTR(ifsapp.crm_cust_info.note,4000,1)", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df

def generate_active_potential_clients_details(region, stage):
    if region is None:
        pass
    else:
        if stage == 'TOTAL':
            df = get_active_potential_clients_details_all(region)
        if stage == 'Poziom zero':
            df = get_active_potential_clients_details_null(region)
        if stage in ['Akcja zaczepna', 'Wstępny', 'Zainteresowany']:
            df = get_active_potential_clients_details_by_stage(region, stage)

        if not df.empty:
            df2 = get_value_of_open_offers_for_potential_clients()
            df2 = df2.rename(columns={'customer_no':'customer_id'})
            df = pd.merge(left=df, right=df2, on='customer_id', how='left')
            df['id'] = df['customer_id']
            df.set_index('id', inplace=True, drop=False)
            df = df.drop(columns=['customer_id'])
            try:
                df['last_contact'] = df['last_contact'].dt.date
            except AttributeError:
                pass
            
       
    return df

def get_activities_by_potential_client_number(customer_id):
    if customer_id is None:
        df = pd.DataFrame(columns=['start_date', 'description', 'calendar_activity_type', 'note'])
    else:
        connection = engine.connect()
        sql_query = pd.read_sql_query(f"SELECT start_date, description, calendar_activity_type, note FROM ifsapp.business_activity \
        WHERE ifsapp.business_activity.connection_id = '{customer_id}' \
        ORDER BY start_date DESC", engine)
        df = pd.DataFrame(sql_query)
        connection.close()
        if not df.empty:
            df['start_date'] = df['start_date'].dt.date
    return df

def get_active_lost_clients_details_all(region):
    one_year_from_today = (datetime.datetime.today() -  datetime.timedelta(days=365)).date().strftime('%Y%m%d')
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT \
    ifsapp.cust_ord_customer_address_ent.customer_id,\
    ifsapp.customer_info_cfv.name, \
    MAX(ifsapp.business_activity.start_date) AS LAST_CONTACT, \
    DBMS_LOB.SUBSTR(ifsapp.crm_cust_info.note,4000,1) AS NOTE \
    FROM ifsapp.cust_ord_customer_address_ent \
    LEFT JOIN ifsapp.customer_info_cfv \
    ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.customer_info_cfv.customer_id \
    LEFT JOIN ifsapp.business_activity \
    ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.business_activity.connection_id \
    LEFT JOIN ifsapp.crm_cust_info \
    ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.crm_cust_info.customer_id \
    WHERE ifsapp.cust_ord_customer_address_ent.district_code = '{region}'\
    AND (ifsapp.customer_info_cfv.cf$_etap IN ('Akcja zaczepna', 'Wstępny', 'Zainteresowany') OR ifsapp.customer_info_cfv.cf$_etap IS NULL) \
    AND ifsapp.customer_info_cfv.customer_id IN (\
        SELECT IDENTITY FROM (\
            SELECT\
            ifsapp.customer_order_inv_item_join.identity\
            ,MAX(ifsapp.customer_order_inv_item_join.invoice_date) AS LAST_INVOICED_DATE\
            FROM ifsapp.customer_order_inv_item_join\
            WHERE\
            ifsapp.customer_order_inv_item_join.identity LIKE 'E%'\
            GROUP BY \
            ifsapp.customer_order_inv_item_join.identity)\
            WHERE LAST_INVOICED_DATE <= to_date('{one_year_from_today}', 'YYYYMMDD' )\
    )\
    GROUP BY ifsapp.cust_ord_customer_address_ent.customer_id, ifsapp.customer_info_cfv.name, DBMS_LOB.SUBSTR(ifsapp.crm_cust_info.note,4000,1)", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df

def get_active_lost_clients_details_null(region):
    one_year_from_today = (datetime.datetime.today() -  datetime.timedelta(days=365)).date().strftime('%Y%m%d')
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT \
    ifsapp.cust_ord_customer_address_ent.customer_id,\
    ifsapp.customer_info_cfv.name, \
    MAX(ifsapp.business_activity.start_date) AS LAST_CONTACT, \
    DBMS_LOB.SUBSTR(ifsapp.crm_cust_info.note,4000,1) AS NOTE \
    FROM ifsapp.cust_ord_customer_address_ent \
    LEFT JOIN ifsapp.customer_info_cfv \
    ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.customer_info_cfv.customer_id \
    LEFT JOIN ifsapp.business_activity \
    ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.business_activity.connection_id \
    LEFT JOIN ifsapp.crm_cust_info \
    ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.crm_cust_info.customer_id \
    WHERE ifsapp.cust_ord_customer_address_ent.district_code = '{region}'\
    AND ifsapp.customer_info_cfv.cf$_etap IS NULL \
    AND ifsapp.customer_info_cfv.customer_id IN (\
        SELECT IDENTITY FROM (\
            SELECT\
            ifsapp.customer_order_inv_item_join.identity\
            ,MAX(ifsapp.customer_order_inv_item_join.invoice_date) AS LAST_INVOICED_DATE\
            FROM ifsapp.customer_order_inv_item_join\
            WHERE\
            ifsapp.customer_order_inv_item_join.identity LIKE 'E%'\
            GROUP BY \
            ifsapp.customer_order_inv_item_join.identity)\
            WHERE LAST_INVOICED_DATE <= to_date('{one_year_from_today}', 'YYYYMMDD' )\
    )\
    GROUP BY ifsapp.cust_ord_customer_address_ent.customer_id, ifsapp.customer_info_cfv.name, DBMS_LOB.SUBSTR(ifsapp.crm_cust_info.note,4000,1)", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df

def get_active_lost_clients_details_by_stage(region, stage):
    one_year_from_today = (datetime.datetime.today() -  datetime.timedelta(days=365)).date().strftime('%Y%m%d')
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT ifsapp.cust_ord_customer_address_ent.customer_id, \
    ifsapp.customer_info_cfv.name, \
    MAX(ifsapp.business_activity.start_date) AS LAST_CONTACT, \
    DBMS_LOB.SUBSTR(ifsapp.crm_cust_info.note,4000,1) AS NOTE \
    FROM ifsapp.cust_ord_customer_address_ent \
    LEFT JOIN ifsapp.customer_info_cfv \
    ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.customer_info_cfv.customer_id \
    LEFT JOIN ifsapp.business_activity \
    ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.business_activity.connection_id \
    LEFT JOIN ifsapp.crm_cust_info \
    ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.crm_cust_info.customer_id \
    WHERE ifsapp.cust_ord_customer_address_ent.district_code = '{region}'\
    AND ifsapp.customer_info_cfv.cf$_etap = '{stage}' \
    AND ifsapp.customer_info_cfv.customer_id IN (\
        SELECT IDENTITY FROM (\
            SELECT\
            ifsapp.customer_order_inv_item_join.identity\
            ,MAX(ifsapp.customer_order_inv_item_join.invoice_date) AS LAST_INVOICED_DATE\
            FROM ifsapp.customer_order_inv_item_join\
            WHERE\
            ifsapp.customer_order_inv_item_join.identity LIKE 'E%'\
            GROUP BY \
            ifsapp.customer_order_inv_item_join.identity)\
            WHERE LAST_INVOICED_DATE <= to_date('{one_year_from_today}', 'YYYYMMDD' )\
    )\
    GROUP BY ifsapp.cust_ord_customer_address_ent.customer_id, ifsapp.customer_info_cfv.name, DBMS_LOB.SUBSTR(ifsapp.crm_cust_info.note,4000,1)", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df

def generate_active_lost_clients_details(region, stage):
    if region is None:
        pass
    else:
        if stage == 'TOTAL':
            df = get_active_lost_clients_details_all(region)
        if stage == 'Poziom zero':
            df = get_active_lost_clients_details_null(region)
        if stage in ['Akcja zaczepna', 'Wstępny', 'Zainteresowany']:
            df = get_active_lost_clients_details_by_stage(region, stage)
        if not df.empty:
            df['id'] = df['customer_id']
            df.set_index('id', inplace=True, drop=False)
            df = df.drop(columns=['customer_id'])
            try:
                df['last_contact'] = df['last_contact'].dt.date
            except AttributeError:
                pass
       
    return df




def get_leads_to_funnel():
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT \
    CASE WHEN ifsapp.business_lead.stage_id IS NULL THEN 'Poziom zero' ELSE ifsapp.business_lead.stage_id END AS STAGE_ID, \
    CASE \
        WHEN ifsapp.business_lead.main_representative_id = 'DSUJEWIC' THEN 'DE' \
        WHEN ifsapp.business_lead.main_representative_id = 'AGOLEBIO' THEN 'HU' \
        WHEN ifsapp.business_lead.main_representative_id = 'PKULAKOW' THEN 'IT' \
        WHEN ifsapp.business_lead.main_representative_id = 'ADUDKA' THEN 'NL' \
        WHEN ifsapp.business_lead.main_representative_id = 'ALINKIEW' THEN 'PE' \
        WHEN ifsapp.business_lead.main_representative_id = 'AOLSZEWS' THEN 'RU' \
        WHEN ifsapp.business_lead.main_representative_id = 'DSTUKUS' THEN 'VN' \
    END AS REGION, ifsapp.business_lead.name \
    FROM ifsapp.business_lead \
    WHERE ifsapp.business_lead.main_representative_id IN ('DSTUKUS', 'AOLSZEWS', 'DSUJEWIC', 'ALINKIEW', 'PKULAKOW', 'ADUDKA', 'AGOLEBIO') \
    AND ifsapp.business_lead.stage_id IN ('Akcja zaczepna', 'Wstępny', 'Zainteresowany')", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df

def get_potential_clients_to_funnel():
    
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT \
    CASE WHEN ifsapp.customer_info_cfv.cf$_etap IS NULL THEN 'Poziom zero' ELSE ifsapp.customer_info_cfv.cf$_etap END AS STAGE_ID, \
    CASE \
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-DE' THEN 'DE' \
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-HU' THEN 'HU' \
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-IT' THEN 'IT' \
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-NL' THEN 'NL' \
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-PE' THEN 'PE' \
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-RU' THEN 'RU' \
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-VN' THEN 'VN' \
    END AS REGION, \
    ifsapp.cust_ord_customer_address_ent.customer_id, \
    ifsapp.customer_info_cfv.name \
    FROM ifsapp.cust_ord_customer_address_ent \
    LEFT JOIN ifsapp.customer_info_cfv \
    ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.customer_info_cfv.customer_id \
    WHERE ifsapp.cust_ord_customer_address_ent.district_code IN ('ME-DE', 'ME-HU', 'ME-NL', 'ME-IT', 'ME-PE', 'ME-RU', 'ME-VN') \
    AND ifsapp.customer_info_cfv.customer_category = 'Potencjalny klient' \
    AND ifsapp.customer_info_cfv.cf$_etap IN ('Akcja zaczepna', 'Wstępny', 'Zainteresowany')", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df

def get_value_of_open_offers_for_potential_clients_to_funnel():
    current_year = datetime.datetime.today().year
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT ifsapp.order_quotation.customer_no, SUM(ifsapp.Order_Quotation_API.Get_Total_Sale_Price__(QUOTATION_NO)) AS OPEN_OFFER \
    FROM ifsapp.order_quotation \
    WHERE ifsapp.order_quotation.customer_no IN (SELECT \
        ifsapp.cust_ord_customer_address_ent.customer_id \
        FROM ifsapp.cust_ord_customer_address_ent \
        LEFT JOIN ifsapp.customer_info_cfv \
        ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.customer_info_cfv.customer_id \
        WHERE ifsapp.cust_ord_customer_address_ent.district_code IN ('ME-DE', 'ME-HU', 'ME-NL', 'ME-IT', 'ME-PE', 'ME-RU', 'ME-VN') \
        AND ifsapp.customer_info_cfv.customer_category = 'Potencjalny klient') \
    AND ifsapp.order_quotation.state = 'Aktywowane' \
    GROUP BY ifsapp.order_quotation.customer_no", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df

def get_lost_clients_to_funnel():
    one_year_from_today = (datetime.datetime.today() -  datetime.timedelta(days=365)).date().strftime('%Y%m%d')
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT \
    CASE WHEN ifsapp.customer_info_cfv.cf$_etap IS NULL THEN 'Poziom zero' ELSE ifsapp.customer_info_cfv.cf$_etap END AS STAGE_ID, \
    CASE \
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-DE' THEN 'DE'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-HU' THEN 'HU'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-IT' THEN 'IT'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-NL' THEN 'NL'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-PE' THEN 'PE'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-RU' THEN 'RU'\
        WHEN ifsapp.cust_ord_customer_address_ent.district_code ='ME-VN' THEN 'VN'\
        END AS REGION, \
        ifsapp.cust_ord_customer_address_ent.customer_id, \
        ifsapp.customer_info_cfv.name \
        FROM ifsapp.cust_ord_customer_address_ent \
        LEFT JOIN ifsapp.customer_info_cfv \
        ON ifsapp.cust_ord_customer_address_ent.customer_id = ifsapp.customer_info_cfv.customer_id \
        WHERE ifsapp.cust_ord_customer_address_ent.district_code IN ('ME-DE', 'ME-HU', 'ME-NL', 'ME-IT', 'ME-PE', 'ME-RU', 'ME-VN') \
        AND ifsapp.customer_info_cfv.cf$_etap IN ('Akcja zaczepna', 'Wstępny', 'Zainteresowany') \
        AND ifsapp.customer_info_cfv.customer_id IN (\
            SELECT IDENTITY FROM (\
                SELECT\
                ifsapp.customer_order_inv_item_join.identity\
                ,MAX(ifsapp.customer_order_inv_item_join.invoice_date) AS LAST_INVOICED_DATE\
                FROM ifsapp.customer_order_inv_item_join\
                WHERE\
                ifsapp.customer_order_inv_item_join.identity LIKE 'E%'\
                GROUP BY \
                ifsapp.customer_order_inv_item_join.identity)\
                WHERE LAST_INVOICED_DATE <= to_date( '{one_year_from_today}', 'YYYYMMDD' ))", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df

def get_value_of_open_offers(customer_id):
    current_year = datetime.datetime.today().year
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT SUM(ifsapp.Order_Quotation_API.Get_Total_Sale_Price__(QUOTATION_NO)) AS OPEN_OFFER \
    FROM ifsapp.order_quotation \
    WHERE ifsapp.order_quotation.customer_no = '{customer_id}' \
    AND ifsapp.order_quotation.state = 'Aktywowane'", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    return df['open_offer'].values[0]

def generate_funnel_graph(region):
    leads = get_leads_to_funnel()
    leads['type'] = 'Namiar handlowy'

    potential = get_potential_clients_to_funnel()
    potential['type'] = 'Klienci potencjalni'
    potential['open_offer'] = potential['customer_id'].apply(lambda x: get_value_of_open_offers(x))
    potential = potential.drop(columns=['customer_id'])

    lost = get_lost_clients_to_funnel()
    lost['type'] = 'Klienci utraceni'
    lost = lost.drop_duplicates()
    lost['open_offer'] = lost['customer_id'].apply(lambda x: get_value_of_open_offers(x))
    lost = lost.drop(columns=['customer_id'])

    df = leads.append(potential)
    df = df.append(lost)
    df['open_offer'] = df['open_offer'].fillna(0)
    df.loc[df['open_offer']>0, 'stage_id'] = 'W trakcie ofertowania'

    if region == 'ALL':
        dff = df.groupby(['stage_id', 'type'], as_index=False).agg({'name':'count'})
        stages = ['Akcja zaczepna', 'Wstępny', 'Zainteresowany', 'W trakcie ofertowania']
        types = ['Namiar handlowy', 'Klienci potencjalni', 'Klienci utraceni']
        dff['stage_id'] = pd.Categorical(dff['stage_id'], categories = stages)
        dff['type'] = pd.Categorical(dff['type'], categories = types)
        dff = dff.sort_values(by = ['stage_id', 'type'])
        fig = px.funnel(dff, x='name', y='stage_id', color='type', template='plotly_white', height=600)

    #if region in ['DE', 'HU', 'IT', 'NL', 'PE', 'RU', 'VN']:
        
    return fig
