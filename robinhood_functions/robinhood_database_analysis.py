# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 22:54:35 2018

@author: Andy
"""
import time
import sqlite3
#Import functions as abbreviations
import robinhood_send_email as rhse
def database_analysis(path,all_tick,trade_days,decline):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    # Analyze data in database to see changes in owned securities and watchlist
    for itick in range(len(all_tick)):
        c.execute('''
                  SELECT * FROM stocks
                  WHERE symbol = ?
                  ORDER BY previous_close_date DESC''',(all_tick[itick],))
        row = c.fetchmany(trade_days)
        #print securities_tick[itick]
        #row.keys()
        msg2 = ''
        send = 0
        # Do we have x trading days of data for the current ticker?
        if len(row) >= trade_days:
            # Has the ticker dropped more the 5% in 30 trading days
            if float(row[0]['previous_close'])/float(row[trade_days-1]['previous_close']) < decline:
                msg2 += '%s Trading Close @ %s Down %s%% Over %s tdays\n'\
                %(all_tick[itick], row[0]['previous_close'],
                str((1-float(row[0]['previous_close'])
                /float(row[trade_days-1]['previous_close']))*100)[:4],str(trade_days))
                # Has the ticker traded up the past 5 trading days
                if float(row[0]['previous_close'])/float(row[4]['previous_close']) > 1:
                    msg2 += 'Trading Close Up %s%% Pass 5 tdays\n'\
                    %(str((float(row[0]['previous_close'])
                    /float(row[4]['previous_close'])-1)*100)[:4])
                send = 1
            # Has the ticker reached a new 52 week low
            if float(row[0]['low_52_weeks']) < float(row[1]['low_52_weeks']):
                msg2 += '%s Trading @ %s near a 52 Week Low\n'\
                %(all_tick[itick], row[0]['previous_close'])
                send = 1
            # Is there a message to send?
            if send == 1:
                rhse.send_email(msg2,2)
                send = 0
                time.sleep(5)
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
    print 'Finish Database Analysis'