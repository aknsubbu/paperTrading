import requests
from dotenv import load_dotenv
import os
import pandas as pd


class MarketReader:
    def __init__(self, symbol):
        self.symbol = symbol
        load_dotenv()
        self.apikey = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.interval = "1min"
        self.baseUrl = "https://www.alphavantage.co/"

        #live stream
        self.functionLiveStream = "TIME_SERIES_INTRADAY"
        self.urlLiveStream = f"{self.baseUrl}query?function={self.functionLiveStream}&symbol={self.symbol}&interval={self.interval}&apikey={self.apikey}"

        #Daily
        self.functionDaily = "TIME_SERIES_DAILY"
        self.urlDaily = f"{self.baseUrl}query?function={self.functionDaily}&symbol={self.symbol}&apikey={self.apikey}"
        
        #Weekly
        self.functionWeekly = "TIME_SERIES_WEEKLY"
        self.urlWeekly = f"{self.baseUrl}query?function={self.functionWeekly}&symbol={self.symbol}&apikey={self.apikey}"
        
        #Monthly
        self.functionMonthly = "TIME_SERIES_MONTHLY"
        self.urlMonthly = f"{self.baseUrl}query?function={self.functionMonthly}&symbol={self.symbol}&apikey={self.apikey}"
        
        #Market Status
        self.functionMarketStatus ="MARKET_STATUS"
        self.urlMarketStatus = f"{self.baseUrl}query?function={self.functionMarketStatus}&apikey={self.apikey}"
        
        #News Sentiment
        self.functionNewsSentiment = "NEWS_SENTIMENT"
        self.urlNewsSentiment = f"{self.baseUrl}query?function={self.functionNewsSentiment}&tickers={self.symbol}&apikey={self.apikey}"
        
        #Top Gainers Losers
        self.functionTopGainersLosers = "TOP_GAINERS_LOSERS"
        self.urlTopGainersLosers = f"{self.baseUrl}query?function={self.functionTopGainersLosers}&apikey={self.apikey}"
        
        #EMA
        self.functionEMA = "EMA"
        self.EMAInterval = "weekly"
        self.EMATimePeriod = "100"
        self.urlEMA = f"{self.baseUrl}query?function={self.functionEMA}&symbol={self.symbol}&interval={self.interval}&time_period=10&series_type=close&apikey={self.apikey}"
        
        #RSI
        self.functionRSI = "RSI"
        self.RSITimePeriod = "14"
        self.urlRSI = f"{self.baseUrl}query?function={self.functionRSI}&symbol={self.symbol}&interval={self.interval}&time_period={self.RSITimePeriod}&series_type=close&apikey={self.apikey}"


    #symbol needed
    def get_live_stream(self):
        r = requests.get(self.urlLiveStream)
        data = r.json()
        time_series_data = data['Time Series (1min)']
        df = pd.DataFrame.from_dict(time_series_data, orient="index")
        df.index = pd.to_datetime(df.index)
        df.to_csv(f"{self.symbol}_intraday_data.csv")
        return df
    
    #symbol needed
    def get_daily(self):
        r = requests.get(self.urlDaily)
        data = r.json()
        time_series_data = data['Time Series (Daily)']
        df = pd.DataFrame.from_dict(time_series_data, orient="index")
        df.index = pd.to_datetime(df.index)
        df.to_csv(f"{self.symbol}_daily_data.csv")
        return df
    
    #symbol needed
    def get_weekly(self):
        r = requests.get(self.urlWeekly)
        data = r.json()
        time_series_data = data['Weekly Time Series']
        df = pd.DataFrame.from_dict(time_series_data, orient="index")
        df.index = pd.to_datetime(df.index)
        df.to_csv(f"{self.symbol}_weekly_data.csv")
        return df
    
    #symbol needed
    def get_monthly(self):
        r = requests.get(self.urlMonthly)
        data = r.json()
        time_series_data = data['Monthly Time Series']
        df = pd.DataFrame.from_dict(time_series_data, orient="index")
        df.index = pd.to_datetime(df.index)
        df.to_csv(f"{self.symbol}_monthly_data.csv")
        return df
    
    #symbol not needed
    def get_market_status(self):
        r = requests.get(self.urlMarketStatus)
        data = r.json()
        return data
    
    #symbol needed
    def get_news_sentiment(self):
        r = requests.get(self.urlNewsSentiment)
        data = r.json()
        return data
    
    #symbol not needed
    def get_top_gainers_losers(self):
        r = requests.get(self.urlTopGainersLosers)
        data = r.json()
        return data
    
    #symbol needed
    def get_ema(self):
        r = requests.get(self.urlEMA)
        data = r.json()
        return data
    
    #symbol needed
    def get_rsi(self):
        r = requests.get(self.urlRSI)
        data = r.json()
        return data
    


marketInput = MarketReader("AAPL")
print("\n\n\n Live Stream \n\n\n")
print(marketInput.get_live_stream())
print("\n\n\n Daily \n\n\n")
print(marketInput.get_daily())
print("\n\n\n Weekly \n\n\n")
print(marketInput.get_weekly())
print("\n\n\n Monthly \n\n\n")
print(marketInput.get_monthly())
print("\n\n\n Market Status \n\n\n")
print(marketInput.get_market_status())
print("\n\n\n News Sentiment \n\n\n")
print(marketInput.get_news_sentiment())
print("\n\n\n Top Gainers Losers \n\n\n")
print(marketInput.get_top_gainers_losers())
print("\n\n\n EMA \n\n\n")
print(marketInput.get_ema())
print("\n\n\n RSI \n\n\n")
print(marketInput.get_rsi())

