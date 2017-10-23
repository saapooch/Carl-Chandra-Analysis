import quandl
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

#Quandl API key associated with my account
quandl.ApiConfig.api_key = '2sBoxWDxwXqHmxGQoPys'

#Using tutorial http://www.pythonforfinance.net/category/basic-data-analysis/

#define start and end date parameters
startDate = '2010-01-01'
endDate = '2016-12-31'


stocks = ['AAPL', 'MSFT', 'UTX', 'TRV']
#Quandl stock databases I am accessing follow the format: EOD (for end of day) + /(stock ticker)

#Start on our portfolio data frame - get all weekdays in the date range as index
portfolioIndex = pd.date_range(start=startDate, end=endDate, freq='B')

#Create a data frame to populate with stock info
portfolioDataFrame = pd.DataFrame(index=portfolioIndex)

for stock in stocks:

	#get database name
	databaseName = "EOD/" + stock

	#Get data from Quandl database
	data = quandl.get(databaseName, start_date=startDate, end_date=endDate)

	#Quandl doesnt have a lot of holes, but this will fill in any NAN entries 
	data = data.fillna(method = 'pad')

	#make adj_close
	data = data.ix[:, 'Adj_Close']

	#Add close data returns to portfolio data frame
	portfolioDataFrame[stock] = pd.Series(data, index=portfolioDataFrame.index)

print(portfolioDataFrame.head())

#set array holding portfolio weights of each stock
#weights = np.asarray([0.5,0.2,0.3])

#returns
returns =  portfolioDataFrame.pct_change(1)
 
mean_daily_returns = returns.mean()
cov_matrix = returns.cov()

#set number of runs of random portfolio weights
num_portfolios = 25000
 
#set up array to hold results
#We have increased the size of the array to hold the weight values for each stock
results = np.zeros((4+len(stocks)-1,num_portfolios))
 
for i in range(num_portfolios):
    #select random weights for portfolio holdings
    weights = np.array(np.random.random(4))
    #rebalance weights to sum to 1
    weights /= np.sum(weights)
 
    #calculate portfolio return and volatility
    portfolio_return = np.sum(mean_daily_returns * weights) * 252
    portfolio_std_dev = np.sqrt(np.dot(weights.T,np.dot(cov_matrix, weights))) * np.sqrt(252)
 
    #store results in results array
    results[0,i] = portfolio_return
    results[1,i] = portfolio_std_dev
    #store Sharpe Ratio (return / volatility) - risk free rate element excluded for simplicity
    results[2,i] = results[0,i] / results[1,i]
    #iterate through the weight vector and add data to results array
    for j in range(len(weights)):
    	results[j+3,i] = weights[j]
 
#convert results array to Pandas DataFrame
results_frame = pd.DataFrame(results.T,columns=['ret','stdev','sharpe',stocks[0],stocks[1],stocks[2],stocks[3]])
 
#locate position of portfolio with highest Sharpe Ratio
max_sharpe_port = results_frame.iloc[results_frame['sharpe'].idxmax()]
#locate positon of portfolio with minimum standard deviation
min_vol_port = results_frame.iloc[results_frame['stdev'].idxmin()]
 
#create scatter plot coloured by Sharpe Ratio
plt.scatter(results_frame.stdev,results_frame.ret,c=results_frame.sharpe,cmap='RdYlBu')
plt.xlabel('Volatility')
plt.ylabel('Returns')
plt.colorbar()
#plot red star to highlight position of portfolio with highest Sharpe Ratio
plt.scatter(max_sharpe_port[1],max_sharpe_port[0],marker=(5,1,0),color='r',s=1000)
#plot green star to highlight position of minimum variance portfolio
plt.scatter(min_vol_port[1],min_vol_port[0],marker=(5,1,0),color='g',s=1000)

print(max_sharpe_port)
print(min_vol_port)

plt.show()