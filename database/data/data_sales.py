import pandas as pd
   
data_sales = pd.read_parquet('database/data/linie_faktur_sprzedazy_17-20_E_Z01_kodproduktu_anulowane.parquet')

# Pobranie danych ze sprzedażą Z01, E%, kategorie [ABCDE], status != Anulowane, dla 2017,2018,2019,2020
#data_sales = pd.read_csv('/home/pkulakow/workspace/dash-zetkama/database/data/linie_faktur_sprzedazy_17-20_E_Z01_kodproduktu_anulowane.csv', sep=';', decimal=',', low_memory=False, parse_dates=['Data faktury'], dayfirst=True)

# Dodanie dodatkowych pól
'''data_sales = data_sales.set_index('Data faktury')
data_sales['year'] = data_sales.index.year
data_sales['month'] = data_sales.index.month
data_sales['cw'] = data_sales.index.isocalendar().week
data_sales['short_index'] = data_sales['Nr poz. sprzedaży'].str[2:6]'''

# TODO: usunięcie linii reklamacyjnych
# TODO: dodanie nowego powiatu