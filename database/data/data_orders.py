import pandas as pd

data_orders = pd.read_parquet('/home/pkulakow/workspace/dash-zetkama/database/data/linie_zamowien_17-20_E_Z01_kod_produktu_anulowane.parquet')

#Pobranie danych z zamowieniemi Z01, E% dla 2017,2018,2019,2020
#data_orders = pd.read_csv('/home/pkulakow/workspace/dash-zetkama/database/data/linie_zamowien_17-20_E_Z01_kod_produktu_anulowane.csv', sep=';', decimal=',', low_memory=False, parse_dates=['Utworzone', 'Obiecana data/czas dostawy'], dayfirst=True)

# Dodanie dodatkowych pól
'''data_orders = data_orders.set_index('Utworzone')
data_orders['year'] = data_orders.index.year
data_orders['month'] = data_orders.index.month
data_orders['cw'] = data_orders.index.isocalendar().week
data_orders['short_index'] = data_orders['Nr poz. sprzed.'].str[2:6]
data_orders.to_parquet('/home/pkulakow/workspace/dash-zetkama/database/data/linie_zamowien_17-20_E_Z01_kod_produktu_anulowane.parquet')'''

# TODO: usunięcie linii reklamacyjnych
# TODO: dodanie nowego powiatu
