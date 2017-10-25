import quandl
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

#Quandl API key associated with my account
quandl.ApiConfig.api_key = '2sBoxWDxwXqHmxGQoPys'

startDate = '2010-01-01'
endDate = '2016-12-31'

stock = ['AAPL']

databaseName = "EOD/AAPL"

#Start on our portfolio data frame - get all weekdays in the date range as index
trainingIndex = pd.date_range(start=startDate, end=endDate, freq='B')

trainingData = pd.DataFrame(index = trainingIndex, columns = ['Close','Volume','Ema','Output Layer - Y'])

#Get data from Quandl database
data = quandl.get(databaseName, start_date=startDate, end_date=endDate)

#Quandl doesnt have a lot of holes, but this will fill in any NAN entries 
data = data.fillna(method = 'pad')

trainingData['Close'] = data.ix[:, 'Adj_Close']
trainingData['Volume'] = data.ix[:, 'Adj_Volume']
trainingData['Ema'] = trainingData['Close'].ewm(span=20, adjust=False).mean()

#put 0's in the output layer
trainingData['Output Layer - Y'] = 0

intermediatePanda = pd.DataFrame(index = trainingIndex, columns = ['One', 'Two'])

intermediatePanda['Two'] = 0;

#get output layer Y
#if return after 14 trading days is greater then 3%, output layer is 1, otherwise it is 0

#first get pct_change for 14 days later
twoWeekShift = trainingData['Close'].pct_change(14)

#then shift data 14 days back to align the data
#because our output layer is the condition "did the stock rise 3% in the next 14 trading days"
#we need to shift back the returns by 14
twoWeekShift = twoWeekShift.shift(-14)

#then we do a boolean condition
#if the two week return is greater than 3%, condition is met, 1 is assigned
#if not, 0 is assigned
#this can be done using the np.where function
trainingData['Output Layer - Y'] = np.where(twoWeekShift>=.03, 1, 0)

print (trainingData.head(150))
