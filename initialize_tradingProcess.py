import os
import sys
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from technical_analyzer.fetch_technical import RetrieveTechnical
from tradingstrategy import TradingStrategy
sys.path.insert(0, os.getcwd())  # Resolve Importing errors


def execute():
    if RetrieveTechnical.is_business_day(datetime.today()):
        TradingStrategy()
    else:
        print("Invalid Date for Trading")


class InitializeTrading:
    def __init__(self):
        execute()
        self.investing_scheduler = BlockingScheduler()
        self.investing_scheduler.add_job(execute, 'interval', minutes=30)
        self.investing_scheduler.start()


InitializeTrading()
