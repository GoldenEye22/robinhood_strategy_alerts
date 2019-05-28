# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 23:04:29 2018

@author: Andy
"""
from Robinhood import Robinhood
import time
import calendar
import datetime
import sqlite3
import robinhood_functions as rp
#Setup
trader = Robinhood()
path = 'robinhood_database/robinhood.db'
loginstr = open('usrpw.txt','r').read().split(',')
trader.login(username=loginstr[0],password=loginstr[1],qr_code=loginstr[2])
#Initialize parameters when code in executed
todaystr = time.strftime('%Y%m%d %H:%M:%S')
tick_notify = {}
#Main Parameters to Set
ref_time = 300    
loss_trig = 0.05
gain_trig = 0.25
trade_days = 25
decline = 0.95
skew = 2
#Endless loop, need to find better way to do this.
while True: 
    #Get the current time, clear the notification flags, setup parameters
    today = datetime.datetime.today()
    nine30am = today.replace(hour=9, minute=30, second=0, microsecond=0)
    fourpm = today.replace(hour=16, minute=0, second=0, microsecond=0)
    four30pm = today.replace(hour=16, minute=30, second=0, microsecond=0)
    dayofweek = calendar.day_name[datetime.datetime.today().weekday()]   
    print (str(today) + ' ' + str(dayofweek))
    #Reset the daily parameters to perpare for next day
    if fourpm <= today <= four30pm:
        tick_notify = {}
        if dayofweek == 'Friday':
            #Sleep 48hrs over weekend
            print ('Weekend - Sleep 48 hrs')
            time.sleep(172800)  
        else:
            #Sleep 8hrs before database load
            print ('Week Day - Sleep 16 hrs')
            time.sleep(57600)
    #Lets find out if Robinhood has updated yesterday closing data
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()       
    c.execute('''
          SELECT * FROM stocks 
          ORDER BY previous_close_date DESC''')
    row_verify = c.fetchone()
    conn.close()
    #login
    working = False 
    while not working:
        try: 
            quote_data = trader.quote_data(row_verify['symbol'])
            working = True 
        except:
            print ('Failed to Get Quote')    
            try:
                time.sleep(ref_time)
                trader = Robinhood()
                trader.login(username=loginstr[0],password=loginstr[1],qr_code=loginstr[2])
                print ('Login')
            except:
                print ('Cant Login')
                time.sleep(ref_time)
                pass
            pass
    #Load database once daily with current securities and watchlist data
    if quote_data['previous_close_date'] > row_verify['previous_close_date']:
        #Calculate all current securty weights and send alert, return security tick list
        working = False
        while not working:
            try:              
                securities_tick = rp.rhpw.portfolio_weight(trader)
                working = True
            except:
                print ('Failed to get Portfolio Weight')
                try:
                    time.sleep(ref_time)
                    trader = Robinhood()
                    trader.login(username=loginstr[0],password=loginstr[1],qr_code=loginstr[2])
                    print ('Login')
                except:
                    print ('Cant Login')
                    time.sleep(ref_time)
                    pass
                pass
        #Generate current watchlist ticks
        working = False
        while not working:
            try:
                watchlist = trader.watchlists()
                watchlist_tick = []
                for watch in watchlist['results']:
                    #Collect data for each quote to be stored
                    tick_check = trader.security_tick(watch['instrument'])
                    if tick_check not in securities_tick:
                        watchlist_tick.append(tick_check)
                all_tick = securities_tick + watchlist_tick
                working = True
            except:
                print ('Failed to get Watchlists')
                try:
                    time.sleep(ref_time)
                    trader = Robinhood()
                    trader.login(username=loginstr[0],password=loginstr[1],qr_code=loginstr[2])
                    print ('Login')
                except:
                    print ('Cant Login')
                    time.sleep(ref_time)
                    pass
                pass
        #Insert current securities and watchlist into the database
        working = False
        while not working:
            try:
                rp.rhdbi.database_insert(trader,path,all_tick)   
                working = True
            except:
                print ('Failed to Database Insert')
                try:
                    time.sleep(ref_time)
                    trader = Robinhood()
                    trader.login(username=loginstr[0],password=loginstr[1],qr_code=loginstr[2])
                    print ('Login')
                except:
                    print ('Cant Login')
                    time.sleep(ref_time)
                    pass
                pass
        #Analyze the database over specified number of trading days
        working = False
        while not working:
            try:
                rp.rhdba.database_analysis(path,all_tick,trade_days,decline,skew)
                working = True
            except:
                print ('Failed to do Database Analysis')
                try:
                    time.sleep(ref_time)
                    trader = Robinhood()
                    trader.login(username=loginstr[0],password=loginstr[1],qr_code=loginstr[2])
                    print ('Login')
                except:
                    print ('Cant Login')
                    time.sleep(ref_time)
                    pass
                pass
    #Main daily stock market analyzer 
    while (nine30am <= today < fourpm) & (dayofweek != 'Saturday') & (dayofweek != 'Sunday'):
        #Analyze live stock data based on current securities and watchlist
        working = False
        while not working:
            try:
                rp.rhma.market_analysis(trader,tick_notify,loss_trig,gain_trig)
                working = True
            except:
                print ('Failed to do Market Analysis')
                try:
                    time.sleep(ref_time)
                    trader = Robinhood()
                    trader.login(username=loginstr[0],password=loginstr[1],qr_code=loginstr[2])
                    print ('Login')
                except:
                    print ('Cant Login')
                    time.sleep(ref_time)
                    pass
                pass                                          
        print ('Market Open Stock Analyzer - Sleep 5 min')
        time.sleep(ref_time)
        #Get the current time and keep looping while market is open    
        today = datetime.datetime.today()
        print (str(today)+' '+str(dayofweek))
    #Wait time until refresh check
    print ('Out of Time Window - Sleep 5 min ')
    time.sleep(ref_time)