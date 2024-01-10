import pandas as pd
#from database.data.data_time import today_cw

from datetime import date, timedelta

today_cw = date.today().isocalendar()[1]
today = date.today()
current_year = date.today().year

# Creating new empty data frame with years and cw's
data_calendar = pd.DataFrame(index=pd.date_range(start='20170102', end=f'today'))
data_calendar['year'] = data_calendar.index.year
data_calendar['cw'] = data_calendar.index.isocalendar().week
data_calendar = data_calendar.drop(data_calendar[data_calendar['cw']==53].index)
data_calendar = data_calendar.drop_duplicates().reset_index()
data_calendar = data_calendar.drop(columns=['index'])
data_calendar = data_calendar.drop(data_calendar[(data_calendar['year']==current_year)&(data_calendar['cw']>today_cw)].index)
