import pandas as pd
from database.database_connection import engine



def get_countries_from_clients_and_leads_for_dropdown(main_representative):
    df = pd.DataFrame(columns=['country'])
    
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT DISTINCT ifsapp.customer_info.country FROM ifsapp.customer_info \
    INNER JOIN ifsapp.cust_ord_customer \
    ON ifsapp.customer_info.customer_id = ifsapp.cust_ord_customer.customer_no \
    WHERE ifsapp.cust_ord_customer.salesman_code = '{main_representative}' \
    AND ifsapp.customer_info.customer_category = 'Klient'", engine)
    df2 = pd.DataFrame(sql_query)
    connection.close()
    df = df.append(df2)

    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT DISTINCT ifsapp.customer_info.country FROM ifsapp.customer_info \
    INNER JOIN ifsapp.cust_ord_customer \
    ON ifsapp.customer_info.customer_id = ifsapp.cust_ord_customer.customer_no \
    WHERE ifsapp.cust_ord_customer.salesman_code = '{main_representative}' \
    AND ifsapp.customer_info.customer_category = 'Potencjalny klient'", engine)
    df2 = pd.DataFrame(sql_query)
    connection.close()
    df = df.append(df2)

    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT DISTINCT ifsapp.business_lead.country \
    FROM ifsapp.business_lead \
    WHERE ifsapp.business_lead.main_representative_id = '{main_representative}'", engine)
    df2 = pd.DataFrame(sql_query)
    connection.close()
    df = df.append(df2)
    df = df.drop_duplicates().sort_values(by='country')
    df = df.reset_index()
    df = df.drop(columns=['index'])
    return df

def get_last_activity_date(company_id):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT start_date FROM (SELECT start_date FROM ifsapp.business_activity \
    WHERE ifsapp.business_activity.connection_id = '{company_id}' \
    ORDER BY start_date DESC) \
    WHERE ROWNUM = 1", engine)
    df = pd.DataFrame(sql_query)
    connection.close()
    if df.empty:
        return 'brak'
    else:
        df = df.rename(columns={'start_date':'last_contact'})
        return df['last_contact'].values[0]


'''def get_companies_from_clients_and_leads_by_country_data(main_representative, switch_values, countries, stages, potentials, corporate_forms):
    df = pd.DataFrame(columns=['customer_id', 'name', 'country', 'customer_category', 'stage_id', 'potential_id', 'corporate_form'])
    if len(stages) >0:
            stages = tuple(stages) if len(stages) >1 else '(\'' + str(stages[0]) + '\')'
    if len(potentials) >0:
            potentials = tuple(potentials) if len(potentials) >1 else '(\'' + str(potentials[0]) + '\')'
    if len(corporate_forms) >0:
            corporate_forms = tuple(corporate_forms) if len(corporate_forms) >1 else '(\'' + str(corporate_forms[0]) + '\')'
    if not countries:
        if 'klient' in switch_values:
            connection = engine.connect()
            sql_query = pd.read_sql_query(f"SELECT ifsapp.customer_info.customer_id, ifsapp.customer_info.name, ifsapp.customer_info.country, ifsapp.customer_info.customer_category FROM ifsapp.customer_info \
            INNER JOIN ifsapp.cust_ord_customer \
            ON ifsapp.customer_info.customer_id = ifsapp.cust_ord_customer.customer_no \
            WHERE ifsapp.cust_ord_customer.salesman_code = '{main_representative}' \
            AND ifsapp.customer_info.customer_category = 'Klient'", engine)
            df2 = pd.DataFrame(sql_query)
            connection.close()
            df = df.append(df2)
        if 'potencjalny_klient' in switch_values:
            connection = engine.connect()
            sql_query = pd.read_sql_query(f"SELECT ifsapp.customer_info.customer_id, ifsapp.customer_info.name, ifsapp.customer_info.country, ifsapp.customer_info.customer_category FROM ifsapp.customer_info \
            INNER JOIN ifsapp.cust_ord_customer \
            ON ifsapp.customer_info.customer_id = ifsapp.cust_ord_customer.customer_no \
            WHERE ifsapp.cust_ord_customer.salesman_code = '{main_representative}' \
            AND ifsapp.customer_info.customer_category = 'Potencjalny klient'", engine)
            df2 = pd.DataFrame(sql_query)
            connection.close()
            df = df.append(df2)
        if 'lead' in switch_values:
            if len(stages) >0 and len(potentials) >0 and len(corporate_forms) > 0:
                connection = engine.connect()
                sql_query = pd.read_sql_query(f"SELECT ifsapp.business_lead.lead_id, ifsapp.business_lead.name, ifsapp.business_lead.country, ifsapp.business_lead.stage_id, ifsapp.business_lead.potential_id, ifsapp.business_lead.corporate_form \
                FROM ifsapp.business_lead \
                WHERE ifsapp.business_lead.main_representative_id = '{main_representative}' \
                AND ifsapp.business_lead.stage_id IN {stages} \
                AND ifsapp.business_lead.potential_id IN {potentials} \
                AND ifsapp.business_lead.corporate_form IN {corporate_forms}", engine)
                df2 = pd.DataFrame(sql_query)
                df2['customer_category'] = 'Lead'
                df2 = df2.rename(columns={'lead_id':'customer_id'})
                connection.close()
            if len(stages) >0 and len(potentials) >0 and len(corporate_forms) == 0:
                connection = engine.connect()
                sql_query = pd.read_sql_query(f"SELECT ifsapp.business_lead.lead_id, ifsapp.business_lead.name, ifsapp.business_lead.country, ifsapp.business_lead.stage_id, ifsapp.business_lead.potential_id, ifsapp.business_lead.corporate_form \
                FROM ifsapp.business_lead \
                WHERE ifsapp.business_lead.main_representative_id = '{main_representative}' \
                AND ifsapp.business_lead.stage_id IN {stages} \
                AND ifsapp.business_lead.potential_id IN {potentials} \
                AND ifsapp.business_lead.corporate_form IS NULL", engine)
                df2 = pd.DataFrame(sql_query)
                df2['customer_category'] = 'Lead'
                df2 = df2.rename(columns={'lead_id':'customer_id'})
                connection.close()
            if len(stages) >0 and len(corporate_forms) > 0 and len(potentials) == 0:
                connection = engine.connect()
                sql_query = pd.read_sql_query(f"SELECT ifsapp.business_lead.lead_id, ifsapp.business_lead.name, ifsapp.business_lead.country, ifsapp.business_lead.stage_id, ifsapp.business_lead.potential_id, ifsapp.business_lead.corporate_form \
                FROM ifsapp.business_lead \
                WHERE ifsapp.business_lead.main_representative_id = '{main_representative}' \
                AND ifsapp.business_lead.stage_id IN {stages} \
                AND ifsapp.business_lead.potential_id IS NULL \
                AND ifsapp.business_lead.corporate_form IN {corporate_forms}", engine)
                df2 = pd.DataFrame(sql_query)
                df2['customer_category'] = 'Lead'
                df2 = df2.rename(columns={'lead_id':'customer_id'})
                connection.close()
            if len(potentials) >0 and len(corporate_forms) > 0 and len(stages) == 0:
                connection = engine.connect()
                sql_query = pd.read_sql_query(f"SELECT ifsapp.business_lead.lead_id, ifsapp.business_lead.name, ifsapp.business_lead.country, ifsapp.business_lead.stage_id, ifsapp.business_lead.potential_id, ifsapp.business_lead.corporate_form \
                FROM ifsapp.business_lead \
                WHERE ifsapp.business_lead.main_representative_id = '{main_representative}' \
                AND ifsapp.business_lead.stage_id IS NULL \
                AND ifsapp.business_lead.potential_id IN {potentials} \
                AND ifsapp.business_lead.corporate_form IN {corporate_forms}", engine)
                df2 = pd.DataFrame(sql_query)
                df2['customer_category'] = 'Lead'
                df2 = df2.rename(columns={'lead_id':'customer_id'})
                connection.close()
            if len(stages) >0 and len(potentials) == 0 and len(corporate_forms) == 0:
                connection = engine.connect()
                sql_query = pd.read_sql_query(f"SELECT ifsapp.business_lead.lead_id, ifsapp.business_lead.name, ifsapp.business_lead.country, ifsapp.business_lead.stage_id, ifsapp.business_lead.potential_id, ifsapp.business_lead.corporate_form \
                FROM ifsapp.business_lead \
                WHERE ifsapp.business_lead.main_representative_id = '{main_representative}' \
                AND ifsapp.business_lead.stage_id IN {stages} \
                AND ifsapp.business_lead.potential_id IS NULL \
                AND ifsapp.business_lead.corporate_form IS NULL", engine)
                df2 = pd.DataFrame(sql_query)
                df2['customer_category'] = 'Lead'
                df2 = df2.rename(columns={'lead_id':'customer_id'})
                connection.close()
            if len(potentials) >0 and len(stages) == 0 and len(corporate_forms) == 0:
                connection = engine.connect()
                sql_query = pd.read_sql_query(f"SELECT ifsapp.business_lead.lead_id, ifsapp.business_lead.name, ifsapp.business_lead.country, ifsapp.business_lead.stage_id, ifsapp.business_lead.potential_id, ifsapp.business_lead.corporate_form \
                FROM ifsapp.business_lead \
                WHERE ifsapp.business_lead.main_representative_id = '{main_representative}' \
                AND ifsapp.business_lead.stage_id IS NULL \
                AND ifsapp.business_lead.potential_id IN {potentials} \
                AND ifsapp.business_lead.corporate_form IS NULL", engine)
                df2 = pd.DataFrame(sql_query)
                df2['customer_category'] = 'Lead'
                df2 = df2.rename(columns={'lead_id':'customer_id'})
                connection.close()
            if len(corporate_forms) > 0 and len(stages) == 0 and len(potentials) == 0:
                connection = engine.connect()
                sql_query = pd.read_sql_query(f"SELECT ifsapp.business_lead.lead_id, ifsapp.business_lead.name, ifsapp.business_lead.country, ifsapp.business_lead.stage_id, ifsapp.business_lead.potential_id, ifsapp.business_lead.corporate_form \
                FROM ifsapp.business_lead \
                WHERE ifsapp.business_lead.main_representative_id = '{main_representative}' \
                AND ifsapp.business_lead.stage_id IS NULL \
                AND ifsapp.business_lead.potential_id IS NULL \
                AND ifsapp.business_lead.corporate_form IN {corporate_forms}", engine)
                df2 = pd.DataFrame(sql_query)
                df2['customer_category'] = 'Lead'
                df2 = df2.rename(columns={'lead_id':'customer_id'})
                connection.close()
            if len(corporate_forms) == 0 and len(stages) == 0 and len(potentials) == 0:
                connection = engine.connect()
                sql_query = pd.read_sql_query(f"SELECT ifsapp.business_lead.lead_id, ifsapp.business_lead.name, ifsapp.business_lead.country, ifsapp.business_lead.stage_id, ifsapp.business_lead.potential_id, ifsapp.business_lead.corporate_form \
                FROM ifsapp.business_lead \
                WHERE ifsapp.business_lead.main_representative_id = '{main_representative}' \
                AND ifsapp.business_lead.stage_id IS NULL \
                AND ifsapp.business_lead.potential_id IS NULL \
                AND ifsapp.business_lead.corporate_form IS NULL", engine)
                df2 = pd.DataFrame(sql_query)
                df2['customer_category'] = 'Lead'
                df2 = df2.rename(columns={'lead_id':'customer_id'})
                connection.close()
            df = df.append(df2)
    else:
        countries_list = tuple(countries) if len(countries) >1 else '(\'' + str(countries[0]) + '\')'
        if 'klient' in switch_values:
            connection = engine.connect()
            sql_query = pd.read_sql_query(f"SELECT ifsapp.customer_info.customer_id, ifsapp.customer_info.name, ifsapp.customer_info.country, ifsapp.customer_info.customer_category FROM ifsapp.customer_info \
            INNER JOIN ifsapp.cust_ord_customer \
            ON ifsapp.customer_info.customer_id = ifsapp.cust_ord_customer.customer_no \
            WHERE ifsapp.cust_ord_customer.salesman_code = '{main_representative}' \
            AND ifsapp.customer_info.customer_category = 'Klient' \
            AND ifsapp.customer_info.country IN {countries_list}", engine)
            df2 = pd.DataFrame(sql_query)
            connection.close()
            df = df.append(df2)
        if 'potencjalny_klient' in switch_values:
            connection = engine.connect()
            sql_query = pd.read_sql_query(f"SELECT ifsapp.customer_info.customer_id, ifsapp.customer_info.name, ifsapp.customer_info.country, ifsapp.customer_info.customer_category FROM ifsapp.customer_info \
            INNER JOIN ifsapp.cust_ord_customer \
            ON ifsapp.customer_info.customer_id = ifsapp.cust_ord_customer.customer_no \
            WHERE ifsapp.cust_ord_customer.salesman_code = '{main_representative}' \
            AND ifsapp.customer_info.customer_category = 'Potencjalny klient' \
            AND ifsapp.customer_info.country IN {countries_list}", engine)
            df2 = pd.DataFrame(sql_query)
            connection.close()
            df = df.append(df2)
        if 'lead' in switch_values:
            if len(stages) >0 and len(potentials) >0 and len(corporate_forms) > 0:
                connection = engine.connect()
                sql_query = pd.read_sql_query(f"SELECT ifsapp.business_lead.lead_id, ifsapp.business_lead.name, ifsapp.business_lead.country, ifsapp.business_lead.stage_id, ifsapp.business_lead.potential_id, ifsapp.business_lead.corporate_form \
                FROM ifsapp.business_lead \
                WHERE ifsapp.business_lead.main_representative_id = '{main_representative}' \
                AND ifsapp.business_lead.country IN {countries_list} \
                AND ifsapp.business_lead.stage_id IN {stages} \
                AND ifsapp.business_lead.potential_id IN {potentials} \
                AND ifsapp.business_lead.corporate_form IN {corporate_forms}", engine)
                df2 = pd.DataFrame(sql_query)
                df2['customer_category'] = 'Lead'
                df2 = df2.rename(columns={'lead_id':'customer_id'})
                connection.close()
            if len(stages) >0 and len(potentials) >0 and len(corporate_forms) == 0:
                connection = engine.connect()
                sql_query = pd.read_sql_query(f"SELECT ifsapp.business_lead.lead_id, ifsapp.business_lead.name, ifsapp.business_lead.country, ifsapp.business_lead.stage_id, ifsapp.business_lead.potential_id, ifsapp.business_lead.corporate_form \
                FROM ifsapp.business_lead \
                WHERE ifsapp.business_lead.main_representative_id = '{main_representative}' \
                AND ifsapp.business_lead.country IN {countries_list} \
                AND ifsapp.business_lead.stage_id IN {stages} \
                AND ifsapp.business_lead.potential_id IN {potentials} \
                AND ifsapp.business_lead.corporate_form IS NULL", engine)
                df2 = pd.DataFrame(sql_query)
                df2['customer_category'] = 'Lead'
                df2 = df2.rename(columns={'lead_id':'customer_id'})
                connection.close()
            if len(stages) >0 and len(corporate_forms) > 0 and len(potentials) == 0:
                connection = engine.connect()
                sql_query = pd.read_sql_query(f"SELECT ifsapp.business_lead.lead_id, ifsapp.business_lead.name, ifsapp.business_lead.country, ifsapp.business_lead.stage_id, ifsapp.business_lead.potential_id, ifsapp.business_lead.corporate_form \
                FROM ifsapp.business_lead \
                WHERE ifsapp.business_lead.main_representative_id = '{main_representative}' \
                AND ifsapp.business_lead.country IN {countries_list} \
                AND ifsapp.business_lead.stage_id IN {stages} \
                AND ifsapp.business_lead.potential_id IS NULL \
                AND ifsapp.business_lead.corporate_form IN {corporate_forms}", engine)
                df2 = pd.DataFrame(sql_query)
                df2['customer_category'] = 'Lead'
                df2 = df2.rename(columns={'lead_id':'customer_id'})
                connection.close()
            if len(potentials) >0 and len(corporate_forms) > 0 and len(stages) == 0:
                connection = engine.connect()
                sql_query = pd.read_sql_query(f"SELECT ifsapp.business_lead.lead_id, ifsapp.business_lead.name, ifsapp.business_lead.country, ifsapp.business_lead.stage_id, ifsapp.business_lead.potential_id, ifsapp.business_lead.corporate_form \
                FROM ifsapp.business_lead \
                WHERE ifsapp.business_lead.main_representative_id = '{main_representative}' \
                AND ifsapp.business_lead.country IN {countries_list} \
                AND ifsapp.business_lead.stage_id IS NULL \
                AND ifsapp.business_lead.potential_id IN {potentials} \
                AND ifsapp.business_lead.corporate_form IN {corporate_forms}", engine)
                df2 = pd.DataFrame(sql_query)
                df2['customer_category'] = 'Lead'
                df2 = df2.rename(columns={'lead_id':'customer_id'})
                connection.close()
            if len(stages) >0 and len(potentials) == 0 and len(corporate_forms) == 0:
                connection = engine.connect()
                sql_query = pd.read_sql_query(f"SELECT ifsapp.business_lead.lead_id, ifsapp.business_lead.name, ifsapp.business_lead.country, ifsapp.business_lead.stage_id, ifsapp.business_lead.potential_id, ifsapp.business_lead.corporate_form \
                FROM ifsapp.business_lead \
                WHERE ifsapp.business_lead.main_representative_id = '{main_representative}' \
                AND ifsapp.business_lead.country IN {countries_list} \
                AND ifsapp.business_lead.stage_id IN {stages} \
                AND ifsapp.business_lead.potential_id IS NULL \
                AND ifsapp.business_lead.corporate_form IS NULL", engine)
                df2 = pd.DataFrame(sql_query)
                df2['customer_category'] = 'Lead'
                df2 = df2.rename(columns={'lead_id':'customer_id'})
                connection.close()
            if len(potentials) >0 and len(stages) == 0 and len(corporate_forms) == 0:
                connection = engine.connect()
                sql_query = pd.read_sql_query(f"SELECT ifsapp.business_lead.lead_id, ifsapp.business_lead.name, ifsapp.business_lead.country, ifsapp.business_lead.stage_id, ifsapp.business_lead.potential_id, ifsapp.business_lead.corporate_form \
                FROM ifsapp.business_lead \
                WHERE ifsapp.business_lead.main_representative_id = '{main_representative}' \
                AND ifsapp.business_lead.country IN {countries_list} \
                AND ifsapp.business_lead.stage_id IS NULL \
                AND ifsapp.business_lead.potential_id IN {potentials} \
                AND ifsapp.business_lead.corporate_form IS NULL", engine)
                df2 = pd.DataFrame(sql_query)
                df2['customer_category'] = 'Lead'
                df2 = df2.rename(columns={'lead_id':'customer_id'})
                connection.close()
            if len(corporate_forms) > 0 and len(stages) == 0 and len(potentials) == 0:
                connection = engine.connect()
                sql_query = pd.read_sql_query(f"SELECT ifsapp.business_lead.lead_id, ifsapp.business_lead.name, ifsapp.business_lead.country, ifsapp.business_lead.stage_id, ifsapp.business_lead.potential_id, ifsapp.business_lead.corporate_form \
                FROM ifsapp.business_lead \
                WHERE ifsapp.business_lead.main_representative_id = '{main_representative}' \
                AND ifsapp.business_lead.country IN {countries_list} \
                AND ifsapp.business_lead.stage_id IS NULL \
                AND ifsapp.business_lead.potential_id IS NULL \
                AND ifsapp.business_lead.corporate_form IN {corporate_forms}", engine)
                df2 = pd.DataFrame(sql_query)
                df2['customer_category'] = 'Lead'
                df2 = df2.rename(columns={'lead_id':'customer_id'})
                connection.close()
            if len(corporate_forms) == 0 and len(stages) == 0 and len(potentials) == 0:
                connection = engine.connect()
                sql_query = pd.read_sql_query(f"SELECT ifsapp.business_lead.lead_id, ifsapp.business_lead.name, ifsapp.business_lead.country, ifsapp.business_lead.stage_id, ifsapp.business_lead.potential_id, ifsapp.business_lead.corporate_form \
                FROM ifsapp.business_lead \
                WHERE ifsapp.business_lead.main_representative_id = '{main_representative}' \
                AND ifsapp.business_lead.country IN {countries_list} \
                AND ifsapp.business_lead.stage_id IS NULL \
                AND ifsapp.business_lead.potential_id IS NULL \
                AND ifsapp.business_lead.corporate_form IS NULL", engine)
                df2 = pd.DataFrame(sql_query)
                df2['customer_category'] = 'Lead'
                df2 = df2.rename(columns={'lead_id':'customer_id'})
                connection.close()
            df = df.append(df2)
    df['last_contact'] = df['customer_id'].apply(lambda x: get_last_activity_date(x))
    df['last_contact'] = pd.to_datetime(df['last_contact'], errors='coerce').dt.date
    df['id'] = df['customer_id']
    df.set_index('id', inplace=True, drop=False)

    if 'last_contact' in df.columns:
        df = df.sort_values(by='last_contact', ascending=False)
    return df
'''

def get_companies_from_clients_and_leads_by_country_data(main_representative, switch_values, countries):
    df = pd.DataFrame(columns=['customer_id', 'name', 'country', 'customer_category', 'stage_id', 'potential_id', 'corporate_form'])
    
    if not countries:
        if 'klient' in switch_values:
            connection = engine.connect()
            sql_query = pd.read_sql_query(f"SELECT ifsapp.customer_info.customer_id, ifsapp.customer_info.name, ifsapp.customer_info.country, ifsapp.customer_info.customer_category FROM ifsapp.customer_info \
            INNER JOIN ifsapp.cust_ord_customer \
            ON ifsapp.customer_info.customer_id = ifsapp.cust_ord_customer.customer_no \
            WHERE ifsapp.cust_ord_customer.salesman_code = '{main_representative}' \
            AND ifsapp.customer_info.customer_category = 'Klient'", engine)
            df2 = pd.DataFrame(sql_query)
            connection.close()
            df = df.append(df2)
        if 'potencjalny_klient' in switch_values:
            connection = engine.connect()
            sql_query = pd.read_sql_query(f"SELECT ifsapp.customer_info.customer_id, ifsapp.customer_info.name, ifsapp.customer_info.country, ifsapp.customer_info.customer_category FROM ifsapp.customer_info \
            INNER JOIN ifsapp.cust_ord_customer \
            ON ifsapp.customer_info.customer_id = ifsapp.cust_ord_customer.customer_no \
            WHERE ifsapp.cust_ord_customer.salesman_code = '{main_representative}' \
            AND ifsapp.customer_info.customer_category = 'Potencjalny klient'", engine)
            df2 = pd.DataFrame(sql_query)
            connection.close()
            df = df.append(df2)
        if 'lead' in switch_values:
            connection = engine.connect()
            sql_query = pd.read_sql_query(f"SELECT ifsapp.business_lead.lead_id, ifsapp.business_lead.name, ifsapp.business_lead.country, ifsapp.business_lead.stage_id, ifsapp.business_lead.potential_id, ifsapp.business_lead.corporate_form \
            FROM ifsapp.business_lead \
            WHERE ifsapp.business_lead.main_representative_id = '{main_representative}'", engine)
            df2 = pd.DataFrame(sql_query)
            df2['customer_category'] = 'Lead'
            df2 = df2.rename(columns={'lead_id':'customer_id'})
            connection.close()
            df = df.append(df2)
    else:
        countries_list = tuple(countries) if len(countries) >1 else '(\'' + str(countries[0]) + '\')'
        if 'klient' in switch_values:
            connection = engine.connect()
            sql_query = pd.read_sql_query(f"SELECT ifsapp.customer_info.customer_id, ifsapp.customer_info.name, ifsapp.customer_info.country, ifsapp.customer_info.customer_category FROM ifsapp.customer_info \
            INNER JOIN ifsapp.cust_ord_customer \
            ON ifsapp.customer_info.customer_id = ifsapp.cust_ord_customer.customer_no \
            WHERE ifsapp.cust_ord_customer.salesman_code = '{main_representative}' \
            AND ifsapp.customer_info.customer_category = 'Klient' \
            AND ifsapp.customer_info.country IN {countries_list}", engine)
            df2 = pd.DataFrame(sql_query)
            connection.close()
            df = df.append(df2)
        if 'potencjalny_klient' in switch_values:
            connection = engine.connect()
            sql_query = pd.read_sql_query(f"SELECT ifsapp.customer_info.customer_id, ifsapp.customer_info.name, ifsapp.customer_info.country, ifsapp.customer_info.customer_category FROM ifsapp.customer_info \
            INNER JOIN ifsapp.cust_ord_customer \
            ON ifsapp.customer_info.customer_id = ifsapp.cust_ord_customer.customer_no \
            WHERE ifsapp.cust_ord_customer.salesman_code = '{main_representative}' \
            AND ifsapp.customer_info.customer_category = 'Potencjalny klient' \
            AND ifsapp.customer_info.country IN {countries_list}", engine)
            df2 = pd.DataFrame(sql_query)
            connection.close()
            df = df.append(df2)
        if 'lead' in switch_values:
            connection = engine.connect()
            sql_query = pd.read_sql_query(f"SELECT ifsapp.business_lead.lead_id, ifsapp.business_lead.name, ifsapp.business_lead.country, ifsapp.business_lead.stage_id, ifsapp.business_lead.potential_id, ifsapp.business_lead.corporate_form \
            FROM ifsapp.business_lead \
            WHERE ifsapp.business_lead.main_representative_id = '{main_representative}' \
            AND ifsapp.business_lead.country IN {countries_list}", engine)
            df2 = pd.DataFrame(sql_query)
            df2['customer_category'] = 'Lead'
            df2 = df2.rename(columns={'lead_id':'customer_id'})
            connection.close()
            df = df.append(df2)
    df['last_contact'] = df['customer_id'].apply(lambda x: get_last_activity_date(x))
    df['last_contact'] = pd.to_datetime(df['last_contact'], errors='coerce').dt.date
    df['id'] = df['customer_id']
    df.set_index('id', inplace=True, drop=False)

    if 'last_contact' in df.columns:
        df = df.sort_values(by='last_contact', ascending=False)
    return df




def get_activities_by_company_lead_number(company_id):
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

def get_leads_data(main_representative):
    connection = engine.connect()
    sql_query = pd.read_sql_query(f"SELECT name, creation_date, potential_id, source_id, stage_id FROM ifsapp.business_lead \
    WHERE main_representative_id  = '{main_representative}'", engine, parse_dates=['creation_date'])
    leads_data = pd.DataFrame(sql_query)
    connection.close()
    leads_data['creation_date'] = leads_data['creation_date'].dt.normalize()
    return leads_data


def prepare_leads_data(main_representative):
    df = get_leads_data(main_representative)
    

    df_nan = df[df['stage_id'].isna()]
    list_nan = [i for i in df_nan['name']]
    
    return list_nan


'''def get_actions():
    connection = engine.connect()
    sql_query = pd.read_sql_query("SELECT connection_id, last_modified, activity_type, note \
    FROM IFSAPP.Business_Activity \
    WHERE connection_id not like 'K%'", engine)
    actions_data = pd.DataFrame(sql_query)
    connection.close()
    return actions_data
'''