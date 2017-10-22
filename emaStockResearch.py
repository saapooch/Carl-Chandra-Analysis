import quandl
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

#Quandl API key associated with my account
quandl.ApiConfig.api_key = '2sBoxWDxwXqHmxGQoPys'

#This program takes user input of stock tickers and calculates the returns that would have been generated if a portfolio
#were constructed that invested equally in the stocks input in 2001 and sold in 2010
#
#For example, if PG KO GS (Goldman Sachs, Coca Cola, Proctor and Gamble) is input, the program would calculate the returns on a portfolio that purchased 
#those three stocks with equal weight on January 1st, 2001 and sold them on December 31st, 2010
#
#
#I originally retrieved stock data from Yahoo, but it recently shut down.
#I have swtiched to Qunadl, which only gives access to a limited number of stocks with a free account
#So unfortuantely as of now research can only be performed on the stocks listed when the program runs

#define start and end date parameters
startDate = '2005-01-01'
endDate = '2006-12-31'

print("This program tells you the returns of a hypothetical portfolio starting in 2001 and ending in 2010 consisting of stocks you input equally weighted.")
stocksRawText = input("Please input your list of stock names, seperated by spaces. Stocks avialable for research are: \nUNH - United Health \nPG - Proctor and Gamble \nKO - Coca ColaGS \nWMT - Walmart\nMRK - Merck\nVZ - Verizon\nUTX - United Technologies\nTRV - Travelers Company\nAAPL - Apple\nAfter the program runs, a graph will display. You must close the graph to see the total return.\n")
listOfStocks = stocksRawText.split()

#Start on our portfolio data frame - get all weekdays in the date range as index
portfolioIndex = pd.date_range(start=startDate, end=endDate, freq='B')

#Create a data frame to populate with stock info
portfolioDataFrame = pd.DataFrame(index=portfolioIndex)

for stock in listOfStocks:

	#Quandl stock databases I am accessing follow the format: EOD (for end of day) + /(stock ticker)
	databaseName = "EOD/" + stock

	#Get data from Quandl database
	data = quandl.get(databaseName, start_date=startDate, end_date=endDate)

	#Quandl doesnt have a lot of holes, but this will fill in any NAN entries 
	data = data.fillna(method = 'pad')

	#Get the closing stock price
	closeData = data.ix[:, 'Adj_Close']

	#Get daily % changes of stock prices - relative returns
	percentReturns = closeData.pct_change(1)

	#Get logarithmic returns - this is the data we want
	logReturns = np.log(closeData).diff()

	#Add close data returns to portfolio data frame
	portfolioDataFrame[stock] = pd.Series(closeData, index=portfolioDataFrame.index)

	#Create EMA - exponential moving average
	emaShort = closeData.ewm(span=20, adjust=False).mean()

	#create 20 short moving average
	shortRolling = closeData.rolling(window=20).mean()

	fig = plt.figure(figsize=(15,9))
	ax = fig.add_subplot(1,1,1)

	ax.plot(closeData.index, closeData, label='Price of ' + stock)
	ax.plot(emaShort.index, emaShort, label = 'Span 20 day EMA')
	ax.plot(shortRolling.index, shortRolling, label = '20 day SMA')
	#ax.plot(closeData.ix[startDate:endDate, :].index, closeData.ix[startDate:endDate, stock], label='Price')
	#ax.plot(ema_short.ix[startDate:endDate, :].index, ema_short.ix[startDate:endDate, stock], label = 'Span 20-days EMA')
	#ax.plot(short_rolling.ix[startDate:endDate, :].index, short_rolling.ix[startDate:endDate, stock], label = '20-days SMA')

	ax.legend(loc='best')
	ax.set_ylabel('Price in $')
	ax.grid()
	#ax.xaxis.set_major_formatter(my_year_month_fmt)

	#plt.show()
	
	#Loop will populate the portfolioDataFrame with stock data from all the stoks the user inputs

#After retrieving data from each stock and adding it to our data frame, we now calculate the return of the portfolio
#We will achieve this via a weight matrix with the same indices as the return matrix
#Get the dot product of the two matrices - diagnol of this matrix will be a return for each date in the index
#Then graph this logarithmic data next to relative return data, print out total portfolio return

#Each stock input gets equal weight
numStocksInPortfolio = len(listOfStocks)

#This section calculates returns using a EMA based strategy,
#where you go long or short on a stock depending on whether or not the ema-price is 
#positive or negative

#Create EMA - exponential moving average
emaShort = portfolioDataFrame.ewm(span=20, adjust=False).mean()

#get trading positions: price - ema short average
tradingPositions = portfolioDataFrame - emaShort
tradingPositions = tradingPositions.apply(np.sign) * (1/numStocksInPortfolio)
trading_positions_final = tradingPositions.shift(1)

print(tradingPositions.head(20))

#get log returns
asset_log_returns = np.log(portfolioDataFrame).diff()

print(asset_log_returns.head(20))

#get strategy asset log returns
strategy_asset_log_returns = trading_positions_final* asset_log_returns

print(strategy_asset_log_returns.head(20))

# Get the cumulative log-returns per asset
cum_strategy_asset_log_returns = strategy_asset_log_returns.cumsum()

# Transform the cumulative log returns to relative returns
cum_strategy_asset_relative_returns = np.exp(cum_strategy_asset_log_returns) - 1

#graph results of ema returns
fig = plt.figure(figsize=(15,9))
ax = fig.add_subplot(2,1,1)

for c in asset_log_returns:
    ax.plot(cum_strategy_asset_log_returns.index, cum_strategy_asset_log_returns[c], label=str(c))

ax.set_ylabel('Cumulative log-returns')
ax.legend(loc='best')
ax.grid()

ax = fig.add_subplot(2,1,2)

for c in asset_log_returns:
    ax.plot(cum_strategy_asset_relative_returns.index, 100*cum_strategy_asset_relative_returns[c], label=str(c))

ax.set_ylabel('Total relative returns (%)')
ax.legend(loc='best')
ax.grid()

# Total strategy relative returns. This is the exact calculation.
cum_relative_return_exact = cum_strategy_asset_relative_returns.sum(axis=1)

# Get the cumulative log-returns per asset
cum_strategy_log_return = cum_strategy_asset_log_returns.sum(axis=1)

# Transform the cumulative log returns to relative returns. This is the approximation
cum_relative_return_approx = np.exp(cum_strategy_log_return) - 1

fig = plt.figure(figsize=(15,9))
ax = fig.add_subplot(1,1,1)

ax.plot(cum_relative_return_exact.index, 100*cum_relative_return_exact, label='Exact')
ax.plot(cum_relative_return_approx.index, 100*cum_relative_return_approx, label='Approximation')

ax.set_ylabel('Total cumulative relative returns for EMA(%)')
ax.legend(loc='best')
ax.grid()

def print_portfolio_yearly_statistics(portfolio_cumulative_relative_returns, days_per_year = 52 * 5):

    total_days_in_simulation = portfolio_cumulative_relative_returns.shape[0]
    number_of_years = total_days_in_simulation / days_per_year

    # The last data point will give us the total portfolio return
    total_portfolio_return = portfolio_cumulative_relative_returns[-1]
    # Average portfolio return assuming compunding of returns
    average_yearly_return = (1 + total_portfolio_return)**(1/number_of_years) - 1

    print('Total portfolio EMA return is: ' + '{:5.2f}'.format(100*total_portfolio_return) + '%')
    print('Average yearly return is: ' + '{:5.2f}'.format(100*average_yearly_return) + '%')

print_portfolio_yearly_statistics(cum_relative_return_exact)

#calculate buy and hold returns for comparison

#Make weight matrix
weightDataFrame = pd.DataFrame((1/numStocksInPortfolio), index = portfolioDataFrame.index, columns = portfolioDataFrame.columns)

#make portfolio DataFrame log returns
portfolioDataFrame = np.log(portfolioDataFrame).diff()

#multiply matrices - result we are looking for is in the diagnol
tempDataFrame = weightDataFrame.dot(portfolioDataFrame.transpose())

#retreive diagnol
portfolioLogReturns = pd.Series(np.diag(tempDataFrame), index=portfolioDataFrame.index)

#get relative returns for graphing
portfolioRelativeReturns = (np.exp(portfolioLogReturns.cumsum()) - 1)

#take last cell of relative returns for total relative return
portfolioTotalRelativeReturn = portfolioRelativeReturns[-1]

#print total return
print('Total portfolio buy and hold return is: ' +
      '{:5.2f}'.format(100 * portfolioTotalRelativeReturn) + '%')

#rint('Average buy and hold yearly return is: ' + '{:5.2f}'.format(100*average_yearly_return) + '%')

plt.show()
