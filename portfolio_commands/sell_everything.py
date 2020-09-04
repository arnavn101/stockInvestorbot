import os
import sys
sys.path.insert(0, os.getcwd())  # Resolve Importing errors
from sentiment_analyzer.fetch_sentiments import retrieve_Sentiments
from colorama import init, Fore
from yahoo_fin import stock_info as si
from datetime import datetime
import pickle

# Cool colors
init(convert=True)
GREEN = Fore.LIGHTGREEN_EX
CYAN = Fore.LIGHTCYAN_EX
MAGENTA = Fore.LIGHTMAGENTA_EX
RESET = Fore.RESET

# Open pickle files to read variables
save_variables = open(os.path.join('storage_dir', 'saved_variables.pkl'), 'rb')

# Stock transactions tracking
file_transactions = open(os.path.join('storage_dir', 'list_transactions.txt'), 'a+')

# Keep track of transactions
transactions_list = pickle.load(save_variables)  # {Stock_id:No.Stocks}

# Initial Value in portfolio
portfolio_value = pickle.load(save_variables)

for individual_stock in retrieve_Sentiments.retrieve_contentsFile(os.path.join('config_files', 'stocks_list.txt')):
    # Assign important values to variables
    date_current = datetime.today().strftime('%Y-%m-%d')
    name_stock = str(individual_stock)
    id_stock = retrieve_Sentiments.retrieve_stockSymbol(name_stock)

    # Get data of stock
    current_stockPrice = (si.get_live_price(id_stock.lower())).round(2)

    if id_stock in [*transactions_list]:
        portfolio_value += current_stockPrice * transactions_list[id_stock]

print(f"{MAGENTA}Current Portfolio Value {portfolio_value}{RESET}")

# Open pickle file to write
save_variables.close()
file_transactions.close()
save_variables = open(os.path.join('storage_dir', 'saved_variables.pkl'), 'wb')

# Variables to be saved
transactions_list = {}

# Save variables
pickle.dump(transactions_list, save_variables)
pickle.dump(portfolio_value, save_variables)

# Open 2nd pickle file
load_sentiments = open(os.path.join('storage_dir', 'saved_sentiments.pkl'), 'wb')

# Variables to be saved
previous_sentiments = {}
pickle.dump(previous_sentiments, load_sentiments)

# Open 3rd pickle file
load_numberTrades = open(os.path.join('storage_dir', 'number_trades.pkl'), 'wb')

# Variables to be saved
numberTrades = 0
pickle.dump(numberTrades, load_numberTrades)

# Close the file
load_numberTrades.close()
