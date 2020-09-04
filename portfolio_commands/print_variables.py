import os
import pickle
import pprint
import sys
sys.path.insert(0, os.getcwd())  # Resolve Importing errors

# Initialize printer
variable_printer = pprint.PrettyPrinter(indent=2)

# Open pickle files to read variables
load_variables = open(os.path.join('storage_dir', 'saved_variables.pkl'), 'rb')

# Keep track of variables
transactions_list = pickle.load(load_variables)  # {Stock_id:No.Stocks}
portfolio_value = pickle.load(load_variables)

# Load previous sentiments
load_sentiments = open(os.path.join('storage_dir', 'saved_sentiments.pkl'), 'rb')
previous_sentiments = pickle.load(load_sentiments)

# Load no.trades
load_trades = open(os.path.join('storage_dir', 'number_trades.pkl'), 'rb')
numberTrades = pickle.load(load_trades)

# print variables
variable_printer.pprint(transactions_list)
print("\n")
variable_printer.pprint(previous_sentiments)
print("\n")
variable_printer.pprint(f"Portfolio Value {portfolio_value}")
print("\n")
variable_printer.pprint(f"Number of Trades {numberTrades}")
