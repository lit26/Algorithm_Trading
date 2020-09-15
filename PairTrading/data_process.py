import numpy as np
import pandas as pd
import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
import yfinance 
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator
import warnings
warnings.filterwarnings('ignore')
mpl.style.use('default')

RSI_threshold = [20,80]
FIG_SIZE1 = (18, 8)
FIG_SIZE2 = (18, 4)
LATEST = 30
MA_color_list = ['#FFAE42','green','blue','red']

class Stock():
    def __init__(self):
        self.ticker = ""
        self.df = None
        self.n = 0
        self.SMA_list = []

    # Fetch history data from yahoo
    def get_stock_data(self, symbol, start=None, end=None, latest=None):
        try:
            if latest!=None:
                start = datetime.datetime.now() - datetime.timedelta(days=latest)
                end = datetime.datetime.now()
            df_temp = yfinance.download(symbol, start, end)
            df_temp = df_temp.reset_index()
            df_temp['Date'] = pd.to_datetime(df_temp['Date'])
            self.df = df_temp
            self.n = len(self.df)
            self.ticker = symbol
            #print('No. trading dates {}'.format(self.n))
            return df_temp
        except:
            print('No stock is found')

    # Normalize col
    def normalize_col(self, col):
        self.df['Norm_'+col] = self.df[col]/self.df.iloc[0,:][col]
        return self.df

    ##------------------------------------##
    ## Show plots
    ##------------------------------------##
    # Data plots
    def Data_plot(self, latest=LATEST, show_MA=True):
        plot_df = self.df[-latest:]
        ohlc_df = plot_df[['Date', 'Open', 'High', 'Low', 'Close']]
        # Converting dates column to float values
        ohlc_df['Date'] = ohlc_df['Date'].map(mdates.date2num)
        # Making plot
        fig, ax = plt.subplots(figsize=FIG_SIZE1)
        # Converts raw mdate numbers to dates
        ax.xaxis_date()
        plt.xlabel("Date")

        # Making candlestick plot
        candlestick_ohlc(ax, ohlc_df.values, width=0.4,
                         colorup='g', colordown='r', alpha=0.8)
        if show_MA:
            for i in range(len(self.SMA_list)):
                period = self.SMA_list[i]
                plt.plot('Date', 'SMA_{}'.format(period), color=MA_color_list[i],
                         data=plot_df,label='SMA_{}'.format(period))

        plt.ylabel("Price")
        plt.title(self.ticker)
        plt.legend()
        plt.grid()
        plt.show()















