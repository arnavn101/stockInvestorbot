import os
import pickle
from datetime import datetime
from colorama import init, Fore
from yahoo_fin import stock_info as si
from sentiment_analyzer.fetch_sentiments import retrieve_Sentiments
from technical_analyzer.fetch_technical import RetrieveTechnical


class TradingStrategy:
    def __init__(self):
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

        increase_portfolio_value = False  # Initial Variable

        # Initialize Trading Strategy
        for individual_stock in retrieve_Sentiments.retrieve_contentsFile(
                os.path.join('config_files', 'stocks_list.txt')):

            if increase_portfolio_value:
                increase_portfolio_value = False
                portion_portfolio /= 1.4

            # Assign important values to variables
            individual_stock = individual_stock.lower()
            date_current = datetime.today().strftime('%Y-%m-%d')
            name_stock = (str(individual_stock))
            id_stock = retrieve_Sentiments.retrieve_stockSymbol(name_stock)
            print(f"{GREEN}{name_stock}{RESET}", f"{CYAN}{id_stock}{RESET}")

            # Get data of stock
            current_stockPrice = (si.get_live_price(id_stock.lower())).round(2)

            # retrieve previous sentiment
            load_sentiments = open(os.path.join('storage_dir', 'saved_sentiments.pkl'), 'rb')
            previous_sentiments = pickle.load(load_sentiments)

            # (https://www.geeksforgeeks.org/python-sentiment-analysis-using-vader/)
            sentiments_stock = retrieve_Sentiments(name_stock.lower(), 5)
            sentiment_value = sentiments_stock.return_final_sentiment()
            sentiment_value = round(sentiment_value, 2)

            # Retrieve technical value
            technical_analyzer = RetrieveTechnical(id_stock)
            technical_value = technical_analyzer.return_technicalValue()

            print(f"{MAGENTA}Technical Value {individual_stock}: {technical_value}{RESET}")
            if individual_stock not in [*previous_sentiments] and numberTrades < 400:
                # Positive
                if sentiment_value >= 0.4 and technical_value >= 0.25:
                    if portfolio_value > portion_portfolio * 1.4 and not increase_portfolio_value and \
                            RetrieveTechnical.percent_difference(
                            current_stockPrice, RetrieveTechnical.get_current_low(id_stock)) <= 0.25:
                        portion_portfolio *= 1.4
                        increase_portfolio_value = True
                    print("Execute Buy Trade")

                    if portfolio_value < portion_portfolio:
                        print("No money remaining for buying stocks")
                    elif id_stock in sentiments_stock.return_dictKeys(transactions_list):
                        current_shares = transactions_list[id_stock]
                        increase_shares = round(portion_portfolio / current_stockPrice, 2)
                        portfolio_value -= current_stockPrice * increase_shares
                        transactions_list[id_stock] += increase_shares
                        file_transactions.write(
                            f"\nBought {increase_shares} of {name_stock} on {date_current} at a price of {current_stockPrice}")
                        numberTrades += 1
                    else:
                        increase_shares = round(portion_portfolio / current_stockPrice, 2)
                        portfolio_value -= current_stockPrice * increase_shares
                        transactions_list[id_stock] = increase_shares
                        file_transactions.write(
                            f"\nBought {increase_shares} of {name_stock} shares on {date_current} at a price of {current_stockPrice}")
                        numberTrades += 1

                # Negative
                elif sentiment_value <= -0.4 and technical_value <= 0.25:
                    if not increase_portfolio_value and RetrieveTechnical.percent_difference(
                            RetrieveTechnical.get_current_high(id_stock), current_stockPrice) <= 0.25:
                        portion_portfolio *= 1.4
                        increase_portfolio_value = True

                    if id_stock in sentiments_stock.return_dictKeys(transactions_list):
                        print("Execute Sell Trade")
                        current_shares = transactions_list[id_stock]

                        decrease_shares = round(portion_portfolio / current_stockPrice, 2)
                        portfolio_value += current_stockPrice * decrease_shares

                        if current_shares <= portion_portfolio:
                            del transactions_list[id_stock]
                        else:
                            transactions_list[id_stock] -= portion_portfolio

                        file_transactions.write(
                            f"\nSold {decrease_shares} of {name_stock} shares on {date_current} at a price of "
                            f"{current_stockPrice}")
                        numberTrades += 1
                    else:
                        print("Stock does not exist in portfolio")

                # Neutral
                else:
                    print("Neutral Sentiment")

            elif individual_stock in [*previous_sentiments] and numberTrades < 400:
                if portfolio_value > portion_portfolio * 1.4 and not increase_portfolio_value and \
                        RetrieveTechnical.percent_difference(current_stockPrice,
                                                             RetrieveTechnical.get_current_low(id_stock)) <= 0.25:
                    portion_portfolio *= 1.4
                    increase_portfolio_value = True

                specific_previousSentiment = previous_sentiments[individual_stock]

                if sentiment_value == 0:
                    sentiment_value = 10 ** -10

                # Positive
                if ((
                            sentiment_value - specific_previousSentiment) / sentiment_value) > 0.50 and \
                        technical_value >= 0.25:
                    print("Execute Buy Trade")

                    if portfolio_value < portion_portfolio:
                        print("No money remaining for buying stocks")
                    elif id_stock in sentiments_stock.return_dictKeys(transactions_list):
                        increase_shares = round(portion_portfolio / current_stockPrice, 2)
                        portfolio_value -= current_stockPrice * increase_shares
                        transactions_list[id_stock] += increase_shares
                        file_transactions.write(
                            f"\nBought {increase_shares} of {name_stock} on {date_current} at a price of "
                            f"{current_stockPrice}")
                        numberTrades += 1
                    else:
                        increase_shares = round(portion_portfolio / current_stockPrice, 2)
                        portfolio_value -= current_stockPrice * increase_shares
                        transactions_list[id_stock] = increase_shares
                        file_transactions.write(
                            f"\nBought {increase_shares} of {name_stock} shares on {date_current} at a price of "
                            f"{current_stockPrice}")
                        numberTrades += 1

                # Negative
                elif ((
                              sentiment_value - specific_previousSentiment) / sentiment_value) < -0.50 and \
                        technical_value <= 0.25:

                    if not increase_portfolio_value and RetrieveTechnical.percent_difference(
                            RetrieveTechnical.get_current_high(id_stock), current_stockPrice) <= 0.25:
                        portion_portfolio *= 1.4
                        increase_portfolio_value = True
                    if id_stock in sentiments_stock.return_dictKeys(transactions_list):
                        print("Execute Sell Trade")
                        current_shares = transactions_list[id_stock]
                        decrease_shares = round(portion_portfolio / current_stockPrice, 2)
                        portfolio_value += current_stockPrice * decrease_shares
                        if current_shares <= portion_portfolio:
                            del transactions_list[id_stock]
                        else:
                            transactions_list[id_stock] -= portion_portfolio

                        file_transactions.write(
                            f"\nSold {decrease_shares} of {name_stock} shares on {date_current} at a price of "
                            f"{current_stockPrice}")
                        numberTrades += 1
                    else:
                        print("Stock does not exist in portfolio")

                # Neutral
                else:
                    print("No significant change in sentiment")

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
