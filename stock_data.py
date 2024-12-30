from finviz.screener import Screener
import requests as re
import pandas as pd
import json
import datetime as dt

# Fetch stock overview
#stock_data = Screener(tickers=["AAPL"], table="Overview")
#for stock in stock_data.data:
#    print(stock)





# Define the ticker and URL
#ticker = "TSLA"
#url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1=1609459200&period2=1672444800&interval=1d&events=history"

# Fetch data
#response = re.get(url)
#print(response.json())

# Save to a CSV file
#with open(f"{ticker}_historical_prices.csv", "wb") as f:
#    f.write(response.content)

# Load into a DataFrame
#df = pd.read_csv(f"{ticker}_historical_prices.csv")
#print(df.head())


import yfinance as yf

def last_quot_stock_data(ticker):
    # Define the stock ticker (e.g., "AAPL" for Apple)
    #ticker = "AAPL"

    # Fetch stock data
    try:
        stock = yf.Ticker(ticker)

    # Current price
        current_price = stock.history(period="1d")['Close'].iloc[-1]
    #curr_price = f"Current Price of {ticker}: ${current_price:.2f}"
        return current_price
    except Exception:
        print(f"Error fetching stock data for {ticker}")
        return None

def history_stock_data(ticker,start_date="2000-01-01",end_date = "2024-12-01"):
    # Fetch stock data
    stock = yf.Ticker(ticker)
    # Historical data
    #start_date = "2022-01-01"
    #end_date = "2023-01-01"
    historical_data = stock.history(start=start_date, end=end_date)
    historical_data = historical_data.reset_index()
    historical_data['Date'] = pd.to_datetime(historical_data['Date'] ,format='%Y-%m-%d') # change the date format
    # setting up new collumns in order to display the stock price on a certain date
    historical_data['year'] = historical_data['Date'].dt.year
    historical_data['month'] = historical_data['Date'].dt.month
    historical_data['day'] = historical_data['Date'].dt.day


    # Display historical data
    return historical_data
    #print(historical_data)
    #print(type(historical_data))
    #print(historical_data.columns)

# Save historical data to CSV
#historical_data.to_csv(f"{ticker}_historical_prices.csv")
ticker = "AAPL"

# Fetch stock data
stock = yf.Ticker(ticker)



# Historical data
start_date = "2022-01-01"
end_date = "2023-01-01"
historical_data = stock.history(start=start_date, end=end_date)
historical_data = historical_data.reset_index()

# Display historical data
print(historical_data.columns)