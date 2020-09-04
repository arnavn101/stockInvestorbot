# stockInvestorbot - v1.0

********
***Overview***
********

This repository provides a sentiment-based stock trader bot that relies on reddit, twitter, and news articles
for trading decisions. It also uses a very simple "rectangular" trading strategy.

- ``stockInvestorbot``: a NLP-Based Stock Trader
 

Functionality
=====

Fundamentally, ``stockInvestorbot`` is capable of 
    
    1) Parsing Reddit, Twitter, and News Data 
  
    2) Producing Sentiment values for pieces of text
    
    3) Trading virtually on the PC, using pickle files as storage
    
    4) Executing trades only on specific timeframes or days
    
    5) Other Misc commands (manual trade, sell all 
                shares of stock, reset portfolio...)


************
Installation/Configuration
************

Linux Environments
==========================

On any Linux OS, clone this repository and setup the config file
and other stock trading information within the ``config_files`` directory

      vim config_files/auth.cfg # API Keys
      vim config_files/stocks_list.txt # Stocks avalable to the bot for trading
      vim config_files/subreddits_list.txt # Allowed Subreddits for parsing
      

Install requirements of Python
    
     python3 -m venv stockInvestorEnv
     source stockInvestorEnv/bin/activate
     pip install -r requirements.txt
     
Setup PreProcessing Directories

     python3 portfolio_commands/reset_variables.py

Run the Main File: 
     
     python3 initialize_tradingProcess.py

APIs and Resources Used
===============
      nltk
      tweepy
      praw
      APScheduler
      # For more, refer to the requirements.txt file


