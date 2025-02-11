import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from datetime import timedelta, date
from plotly.subplots import make_subplots


class PlotlyPlot:
    """Plotly Plot

    Plot the stock data as well as indicator data.

    Args:
        df(pd.DataFrame): the whole dataset
        time(str): name of dataset 'Date' column.
        close(str): name of dataset 'Close' column.
        open(str): name of dataset 'Open' column.
        high(str): name of dataset 'High' column.
        low(str): name of dataset 'Low' column.
        main_plot_type(str): type of the main plot. Default: "Candlestick"
        main_plot_legend(bool): if True, show the legend of the main plot. Default: False
        range_slider(bool): if True, show the range slider. Default: True
        rows(int): number of plots. Default: 1
        row_height(list): scale for the plots. Default: [1]
    """
    def __init__(self,
                 df: pd.DataFrame,
                 time: str = 'Date',
                 close: str = 'Close',
                 open: str = 'Open',
                 high: str = 'High',
                 low: str = 'Low',
                 main_plot_type: str = "Candlestick",
                 main_plot_legend: bool = False,
                 range_slider: bool = True,
                 rows: int = 1,
                 row_heights: list = None):
        self._time = df[time]
        self._open = df[open]
        self._high = df[high]
        self._low = df[low]
        self._close = df[close]
        self._df = df
        self._chart_type = main_plot_type
        self._showlegend = main_plot_legend
        self._rangeslider = range_slider
        self._rows = rows
        if not row_heights:
            self._row_heights = [1]
        else:
            self._row_heights = row_heights
        self._init_fig()

    def _init_fig(self):
        self._fig = make_subplots(
            rows=self._rows,
            shared_xaxes=True,
            shared_yaxes=True,
            cols=1,
            print_grid=False,
            vertical_spacing=0.2,
            row_heights=self._row_heights
        )
        self._main_plot()

    def _main_plot(self):
        data = None
        if self._chart_type == "Candlestick":
            data = go.Candlestick(
                    x=self._time,
                    open=self._open,
                    high=self._high,
                    low=self._low,
                    close=self._close,
                    name="Candlestick",
                    showlegend=self._showlegend
                    )
        elif self._chart_type == "Line":
            data = go.Scatter(
                    x=self._time,
                    y=self._close,
                    name="Close",
                    showlegend=self._showlegend
                    )
        elif self._chart_type == "OHLC":
            data = go.Ohlc(
                    x=self._time,
                    open=self._open,
                    high=self._high,
                    low=self._low,
                    close=self._close,
                    name="OHLC",
                    showlegend=self._showlegend
                )
        elif self._chart_type == 'Area':
            data = go.Scatter(
                    x=self._time,
                    y=self._close,
                    name="Close",
                    showlegend=self._showlegend,
                    fill='tozeroy'
            )
        self._fig.add_trace(data, row=1, col=1)

    def addLine(self, ind_data, name, row, showlegend=True, color='black'):
        """Add indicator to the plot.

        Add the indicator plot.
        Args:
            ind_data(pandas.Series): dataset indicator column.
            name(str): name of the indicator
            row(int): position of the plot
            showlegend(bool): if True, show the legend
            color(str): color of the horizontal line
        """
        self._fig.add_trace(go.Scatter(
            x=self._time,
            y=ind_data,
            name=name,
            line=dict(color=color),
            showlegend=showlegend), row=row, col=1)

    def addHorizontalLine(self, y, name, row, showlegend=True, color='black'):
        """Add horizontal line

        Add horizontal line to the plot
        Args:
            y(int): y value of the horizontal line
            name(str): name of the horizontal line
            row(int): position of the horizontal line
            showlegend(bool): if True, show the legend
            color(str): color of the horizontal line
        """
        self._fig.add_trace(go.Scatter(
            x=self._time,
            y=[y] * len(self._time),
            name=name,
            line=dict(dash='dash', width=0.7, color=color),
            showlegend=showlegend), row=row, col=1)

    def addHorizontalArea(self, range, row, color="red"):
        """Add horizontal area

        Add horizontal area to the plot
        Args:
            range(tuple): y range of the horizontal area
            row(int): position of the horizontal area
            color(str): color of the horizontal area
        """
        self._fig.add_trace(go.Scatter(
            x=self._time,
            y=[range[1]] * len(self._time),
            line=dict(width=0, color=color),
            showlegend=False), row=row, col=1)
        self._fig.add_trace(go.Scatter(
            x=self._time,
            y=[range[0]] * len(self._time),
            line=dict(width=0, color=color),
            fill='tonexty',
            showlegend=False), row=row, col=1)

    def addBuySell(self, signal_column, buy_color='yellow', sell_color='blue', marker_size=10):
        """Add buy sell
        Add buy sell signal
        Args:
            signal_column(string): the column name of the buy sell signal
            buy_color(string): the buy signal color
            sell_color(string): the sell signal color
            market_size(int): the size of the marker
        """
        df2 = self._df[self._df[signal_column] == 1]
        df3 = self._df[self._df[signal_column] == -1]
        self._fig.add_trace(go.Scatter(
            x=df2['Date'],
            y=df2['Low'],
            name='buy',
            mode='markers',
            marker_symbol='triangle-up',
            marker=dict(color=buy_color, size=marker_size)
        ))
        self._fig.add_trace(go.Scatter(
            x=df3['Date'],
            y=df3['High'],
            name='sell',
            mode='markers',
            marker_symbol='triangle-down',
            marker=dict(color=sell_color, size=marker_size)
        ))

    def _getExcludeDates(self):
        startDate = self._time.iloc[0]
        endDate = self._time.iloc[-1]
        currentDate = startDate
        dateArray = []
        while currentDate <= endDate:
            dateArray.append(currentDate)
            currentDate += timedelta(days=1)
        dateArray = [i.strftime('%Y-%m-%d') for i in dateArray]
        currentDates = self._time.apply(lambda x: x.strftime('%Y-%m-%d')).values
        dateArray = [i for i in dateArray if i not in currentDates]
        return dateArray

    def show(self):
        """show

        Show the plots
        """
        excludeDates = self._getExcludeDates()
        # excludeDates = [i.strftime("%Y-%m-%d") for i in excludeDates]
        self._fig.update_layout(
            autosize=True,
            width=700,
            height=700,
            margin={
                'l': 50,
                'r': 50,
                'b': 50,
                't': 50,
                'pad': 4
            },
            paper_bgcolor="LightSteelBlue",
        )
        self._fig.update_layout(
            xaxis_rangeslider_visible=self._rangeslider
        )
        self._fig.update_xaxes(
            rangebreaks=[
                dict(values=excludeDates)
            ]
        )
        self._fig.show()