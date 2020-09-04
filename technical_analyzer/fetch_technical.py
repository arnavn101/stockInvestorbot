import pandas as pd
import pandas_datareader.data as web
from datetime import timedelta, datetime, time
from yahoo_fin import stock_info as si
import pandas_market_calendars as market_calendar
from pandas.tseries.offsets import BDay
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)  # Suppress Warnings


class RetrieveTechnical:
    def __init__(self, stock_name):
        self.stock_name = stock_name
        self.technical_value = None
        self.execute_rectangularStrategy()

    def retrieve_stockPrices(self, start_date, end_date):
        return web.DataReader(self.stock_name, 'yahoo', start_date, end_date)

    def retrieve_currentStockPrice(self):
        return (si.get_live_price(self.stock_name.lower())).round(2)

    @staticmethod
    def retrieve_PastDate(number_days=3):
        difference_dates = BDay(number_days + 1)
        return pd.datetime.today() - difference_dates

    @staticmethod
    def get_current_low(stock_id):
        current_StockData = si.get_quote_table(stock_id, dict_result=True)
        return float(((current_StockData["Day's Range"]).split(" ", 1)[0]).replace(",", ""))

    @staticmethod
    def get_current_high(stock_id):
        current_StockData = si.get_quote_table(stock_id, dict_result=True)
        return float(((current_StockData["Day's Range"]).split("-", 1)[1]).replace(",", ""))

    @staticmethod
    def retrieve_changeValues(stock_dataframe):
        daily_High = stock_dataframe["High"]
        daily_Low = stock_dataframe["Low"]
        change_stockValue = []
        for i in range(len(daily_High)):
            change_stockValue.append(daily_High[i] - daily_Low[i])
        return change_stockValue

    def execute_rectangularStrategy(self):
        stock_dataFrame = self.retrieve_stockPrices(RetrieveTechnical.retrieve_PastDate(), pd.datetime.today() - BDay(1))
        change_stockValues = RetrieveTechnical.retrieve_changeValues(stock_dataFrame)
        if change_stockValues[0] > 0:
            if change_stockValues[1] > change_stockValues[0] / 2:
                if change_stockValues[2] > change_stockValues[1] / 2:
                    self.technical_value = RetrieveTechnical.percent_difference(change_stockValues[2],
                                                                                change_stockValues[0])
        elif change_stockValues[0] < 0:
            if change_stockValues[1] < change_stockValues[0] / 2:
                if change_stockValues[2] < change_stockValues[1] / 2:
                    self.technical_value = RetrieveTechnical.percent_difference(change_stockValues[2],
                                                                                change_stockValues[0])

    def return_technicalValue(self):
        if self.technical_value:
            return self.technical_value
        return 0

    @staticmethod
    def percent_difference(original_value, new_value):
        return (original_value - new_value) / original_value

    @staticmethod
    def is_business_day(date_time):
        date_input = date_time.strftime('%Y-%m-%d')
        list_businessDays = market_calendar.get_calendar('NYSE')
        return len(list_businessDays.schedule(start_date=date_input, end_date=date_input)) != 0

    @staticmethod
    def is_time_between(begin_time, end_time, check_time=None):
        # If check time is not given, default to current UTC time
        check_time = check_time or datetime.now().time()
        if begin_time < end_time:
            return begin_time <= check_time <= end_time
        else:  # crosses midnight
            return check_time >= begin_time or check_time <= end_time

