README.md

import numpy as np # For Linear Algebra
import pandas as pd # To Work With Data
# for visualizations
import plotly.express as px 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime # Time Series analysis.

df = pd.read_csv("file/Weather.csv")
# df = pd.read_csv("file/Game_Store_Sales.csv",encoding='latin-1')
# print('dff11',df)

df.head() # This will show us top 5 rows of the dataset by default.
df = pd.read_csv("file/Weather.csv", index_col=0)


# print('dff',df)
# df1 = pd.melt(df, id_vars='JAN', value_vars=df.columns[1:]) ## This will melt the data
df1 = pd.melt(df, id_vars='YEAR', value_vars=df.columns[1:]) ## This will melt the data
df1.head() 


# df1['Date'] = df1['variable'] + ' ' + df1['JAN'].astype(str)  
df1['Date'] = df1['variable'] + ' ' + df1['YEAR'].astype(str)  
# print('df1',df1)
df1.loc[:,'Date'] = df1['Date'].apply(lambda x : datetime.strptime(x, '%b %Y')) ## Converting String to datetime object
# print('df11',df1)
df1.head()


df1.columns=['Year', 'Month', 'Temprature', 'Date']
df1.sort_values(by='Date', inplace=True) ## To get the time series right.
# I am using decision tree regressor for prediction as the data does not actually have a linear trend.
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split 
from sklearn.metrics import r2_score 

df2 = df1[['Year', 'Month', 'Temprature']].copy()
print('df1',df1)
df2 = pd.get_dummies(df2)
print('dfget_dummies1',df2)
y = df2[['Temprature']]
x = df2.drop(columns='Temprature')
# print(x)
# print(y)
dtr = DecisionTreeRegressor()
train_x, test_x, train_y, test_y = train_test_split(x,y,test_size=0.3)
dtr.fit(train_x, train_y)
pred = dtr.predict(test_x)
r2_score(test_y, pred)
# print('r2',r2_score(test_y, pred))

next_Year = df1[df1['Year']==2017][['Year', 'Month']]
print('next_Yearss',next_Year)
next_Year.Year.replace(2017,2020, inplace=True)
next_Year= pd.get_dummies(next_Year)
print('next_Year',next_Year)
temp_2018 = dtr.predict(next_Year)
print('temp_2018',temp_2018)

# temp_2018 = {'Month':df1['Month'].unique(), 'Temprature':temp_2018}
# temp_2018=pd.DataFrame(temp_2018)
# temp_2018['Year'] = 2018
# print(temp_2018)

