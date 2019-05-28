# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 23:44:33 2018

@author: Andy
"""
from Robinhood import Robinhood
#Import functions as abbreviations
import robinhood_functions.robinhood_send_email as rhse
import robinhood_functions.robinhood_portfolio_weight as rhpw
import robinhood_functions.robinhood_database_analysis as rhdba
import robinhood_functions.robinhood_database_insert as rhdbi
import robinhood_functions.robinhood_market_analysis as rhma
#Setup
mytrader = Robinhood()
