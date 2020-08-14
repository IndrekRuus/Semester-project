#!/usr/bin/env python
# coding: utf-8

# # Semester Project
# 
# Complete your data collection, data cleaning, and analysis in this notebook!

# In[3]:


#Import ALL the libraries
import plotly.express as px
import plotly.graph_objects as go
from pandas import read_csv
import datetime
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters() 
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")


#read in data
data = pd.read_csv('https://opendata.ecdc.europa.eu/covid19/casedistribution/csv',error_bad_lines=False,index_col='dateRep')

#Determine what the app is used for
pred_or_view=input("""I am an application for visualizing and forecasting COVID-19 cases on a per country bases.
\nFeel free to experiment with me!
\nwould you like me to graph the corona cases for a country(type in: a) 
\nor would you like to forecast future cases for a country(type in: b)?: """)

#check if the user wants to see the data graphed out
if pred_or_view == 'a':

    #ask for country input
    country = input("Enter a country name: ")
    CountryData = data.loc[data['countriesAndTerritories'] == country]

    #turn data arouns so last dates would appear as last collumns
    countryCases = CountryData.loc[::-1]

    countryCases2 = countryCases[['cases']]
    
    # plot the countries data
    plot = px.line(countryCases2, x = countryCases.index, y = 'cases',title = country +" "+ "COVID-19 daily cases history")

    plot.show()
#check if the user wants to forecast
elif pred_or_view =='b':

    #ask for country input
    country = input("Enter a country name: ")
    days_forecast = int(input("Enter number of days to forecast(I work better with fewer days): "))
    CountryData = data.loc[data['countriesAndTerritories'] == country]

    #turn data arouns so last dates would appear as last collumns
    countryCases = CountryData.loc[::-1]

    countryCases2 = countryCases[['cases']]
    
    #Old piece of code to be reused when making predictions and comapring them to the dataset
    #define testing 
    casest = countryCases2[:'31/05/2020']
        #casesf = countryCases2['01/06/2020':]

    #create the models
    modelt = ARIMA(casest,(7,0,0)).fit()
    modelf = modelt.forecast(days_forecast)

    countryCases2['test'] = modelt
    
    # Plot the forecasting model
    fig = go.Figure()

    fig.add_trace(go.Scatter(x = [x for x in range(len(countryCases2))], y = countryCases2['cases'], name='Historic new cases'))

    fig.add_trace(go.Scatter(x = [x for x in range(len(countryCases2), len(countryCases2)+len(modelf[0]))], y = modelf[0], name='Forecasted new cases'))
    
    fig.update_layout(
    title=country+" "+"COVID-19 cases forecast for "+str(days_forecast)+" days",
    xaxis_title="Number of days from 31/12/2019",
    yaxis_title="Number of new daily cases",
    legend_title="Legend")
    
    fig.show()

#Tell user again what to type
else:
    print("Make sure to tye either a or b")


# In[ ]:




