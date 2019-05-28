# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 23:00:57 2018

@author: Andy
"""
import time
import numpy as np
#Import functions as abbreviations
import robinhood_functions.robinhood_send_email as rhse
def market_analysis(trader,tick_notify,loss_trig,gain_trig):
    #Account position section analysis 
    #Grab current securities, positions, and portfolio info
    securities = trader.securities_owned()
    watchlist = trader.watchlists()
    securities_tick = []
    watchlist_tick = []
    #Cyle though securities and grab quote date
    for itick, security in enumerate(securities['results']):                         
        #Request current stock info
        securities_tick.append(trader.security_tick(security['instrument']))
        quote_data = trader.quote_data(securities_tick[itick])
        last_trade_price = quote_data['last_trade_price']
        previous_close = quote_data['previous_close']
        average_buy_price = security['average_buy_price']
        if float(average_buy_price) == 0:
            average_buy_price = '1'
        #Does the library exist for this tick
        if securities_tick[itick] not in tick_notify:
            tick_notify[securities_tick[itick]] = 0
        #Send notification if it hasn't been sent yet               
        if tick_notify[securities_tick[itick]] != 1:
            #Is the stock down by a certain percentage from average buy price
            if float(last_trade_price) < (float(previous_close)*(1-loss_trig)):
                #Number of shares to buy as per strategy
                buy_number_of_shares = np.floor(500/float(last_trade_price))
                #How much has this position lost
                loss_per = 100*(1-float(last_trade_price)/float(previous_close))
                #Message structured for three line text message
                msg0 = '%s, Trading @ %s From Avg %s\nDown %s%% From Prev Close, Buy %s shares'\
                %(securities_tick[itick],last_trade_price[:5],average_buy_price[:5],
                str(loss_per)[:4],str(buy_number_of_shares))
                rhse.send_email(msg0,0)
                time.sleep(5)
                tick_notify[securities_tick[itick]] = 1
            #Is the stock up by a certain percantage from average buy price
            elif float(last_trade_price) > (float(average_buy_price)*(1+gain_trig)):
                #How much has this position gained
                gain_per = 100*(float(last_trade_price)/float(average_buy_price)-1)
                #Message structured for three line text message
                msg0 = '%s, Trading @ %s From Avg %s\nUp: %s%%, Sell shares'\
                %(securities_tick[itick],last_trade_price[:5],average_buy_price[:5],
                str(gain_per)[:4])
                rhse.send_email(msg0,0)
                time.sleep(5)
                tick_notify[securities_tick[itick]] = 1  
    #Cyle though watchlist and grab ticks
    for itick, watch in enumerate(watchlist['results']):
        #Request current stock info
        tick_check = trader.security_tick(watch['instrument'])
        if tick_check not in securities_tick:
            watchlist_tick.append(tick_check)
    #Cyle though watchlist_tick and grab quote date       
    for ticker in watchlist_tick:       
        quote_data = trader.quote_data(ticker)
        last_trade_price = quote_data['last_trade_price']
        previous_close = quote_data['previous_close']
        #Does the library exist for this tick
        if ticker not in tick_notify:
            tick_notify[ticker] = 0
        #Send notification if it hasn't been sent yet               
        if tick_notify[ticker] != 1:
            #Is the stock down by a certain percentage from previous close
            if float(last_trade_price) < (float(previous_close)*(1-loss_trig)):
                #How much has this position lost
                loss_per = 100*(1-float(last_trade_price)/float(previous_close))
                #Message structured for three line text message
                msg0 = '%s, Trading @ %s From Prev Close %s Down %s%%'\
                %(ticker,last_trade_price[:5],previous_close[:5],
                  str(loss_per)[:4])
                rhse.send_email(msg0,0)
                time.sleep(5)
                tick_notify[ticker] = 1
    return None