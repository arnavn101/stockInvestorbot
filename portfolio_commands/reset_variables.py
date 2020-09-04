import os
import pickle
import sys
sys.path.insert(0, os.getcwd())  # Resolve Importing errors

# Create Directory
if 'storage_dir' not in os.listdir(os.getcwd()):
    os.mkdir('storage_dir')

# Create transactions file
open(os.path.join('storage_dir', 'list_transactions.txt'), 'w+').close()

# Open the pickle file
save_variables = open(os.path.join('storage_dir', 'saved_variables.pkl'), 'wb')

# Variables to be saved
transactions_list = {}
portfolio_value = 10000
empty_sentiments = {}

# Save variables
pickle.dump(transactions_list, save_variables)
pickle.dump(portfolio_value, save_variables)

# Close the file
save_variables.close()

# Open 2nd pickle file
load_sentiments = open(os.path.join('storage_dir', 'saved_sentiments.pkl'), 'wb')

# Variables to be saved
pickle.dump(empty_sentiments, load_sentiments)

# Close the file
load_sentiments.close()

# Open 3rd pickle file
load_numberTrades = open(os.path.join('storage_dir', 'number_trades.pkl'), 'wb')

# Variables to be saved
numberTrades = 0
pickle.dump(numberTrades, load_numberTrades)

# Close the file
load_numberTrades.close()


