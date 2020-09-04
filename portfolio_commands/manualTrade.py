import os
import pickle
import sys
from datetime import datetime
from colorama import init, Fore
from yahoo_fin import stock_info as si
sys.path.insert(0, os.getcwd())  # Resolve Importing errors
from sentiment_analyzer.fetch_sentiments import retrieve_Sentiments

# Cool colors
init(convert=True)
GREEN = Fore.LIGHTGREEN_EX
CYAN = Fore.LIGHTCYAN_EX
MAGENTA = Fore.LIGHTMAGENTA_EX
RESET = Fore.RESET

# Open number_trades pickle file
load_numberTrades = open(os.path.join('storage_dir', 'number_trades.pkl'), 'rb')

# Open pickle files to read variables
save_variables = open(os.path.join('storage_dir', 'saved_variables.pkl'), 'rb')

# Stock transactions tracking
file_transactions = open(os.path.join('storage_dir', 'list_transactions.txt'), 'a+')

# Keep track of transactions
transactions_list = pickle.load(save_variables)  # {Stock_id:No.Stocks}

# Initial Value in portfolio
portfolio_value = pickle.load(save_variables)

# Number of Trades
numberTrades = pickle.load(load_numberTrades)

# Buy or sell specific no. shares
portion_portfolio = 1000
print(f"{MAGENTA}Initial Portfolio Value: {portfolio_value}{RESET}")

""" Initialize Variables to Trade Here"""

action = "sell"
name_stock = "Netflix"
id_stock = retrieve_Sentiments.retrieve_stockSymbol(name_stock)

""" Start Trading Process"""

if action == "buy":
    current_stockPrice = (si.get_live_price(id_stock.lower())).round(2)
    date_current = datetime.today().strftime('%Y-%m-%d')
    if numberTrades < 4:
        print("Execute Buy Trade")

        if portfolio_value < portion_portfolio:
            print("No money remaining for buying stocks")
        elif id_stock in [*transactions_list]:
            current_shares = transactions_list[id_stock]
            increase_shares = round(portion_portfolio / current_stockPrice, 2)
            portfolio_value -= current_stockPrice * increase_shares
            transactions_list[id_stock] += increase_shares
            file_transactions.write(
                f"\nBought {increase_shares} of {name_stock} on {date_current} at a price of {current_stockPrice}")
        else:
            increase_shares = round(portion_portfolio / current_stockPrice, 2)
            portfolio_value -= current_stockPrice * increase_shares
            transactions_list[id_stock] = increase_shares
            file_transactions.write(
                f"\nBought {increase_shares} of {name_stock} shares on {date_current} at a price of {current_stockPrice}")
            numberTrades += 1

elif action == "sell":
    current_stockPrice = (si.get_live_price(id_stock.lower())).round(2)
    date_current = datetime.today().strftime('%Y-%m-%d')
    if numberTrades < 4:
        print("Execute Sell Trade")

        if id_stock in [*transactions_list]:
            current_shares = transactions_list[id_stock]
            portfolio_value += current_stockPrice * portion_portfolio
            decrease_shares = round(portion_portfolio / current_stockPrice, 2)

            if current_shares <= portion_portfolio:
                del transactions_list[id_stock]
            else:
                transactions_list[id_stock] -= portion_portfolio

            file_transactions.write(
                f"\nSold {decrease_shares} of {name_stock} shares on {date_current} at a price of {current_stockPrice}")
            numberTrades += 1
        else:
            print("Stock does not exist in portfolio")

print(f"{MAGENTA}Final Portfolio Value {portfolio_value}{RESET}")

# Open pickle file to write
save_variables.close()
file_transactions.close()
save_variables = open(os.path.join('storage_dir', 'saved_variables.pkl'), 'wb')

# Save variables for next day
pickle.dump(transactions_list, save_variables)
pickle.dump(portfolio_value, save_variables)

# Close both opened files
save_variables.close()

# Open pickle file for writing
load_numberTrades.close()
write_numberTrades = open(os.path.join('storage_dir', 'number_trades.pkl'), 'wb')

# Variables to be saved
pickle.dump(numberTrades, write_numberTrades)
