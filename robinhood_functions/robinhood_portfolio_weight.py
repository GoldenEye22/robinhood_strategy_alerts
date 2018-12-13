# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 21:57:08 2018

@author: Andy
"""
import time
#Import functions as abbreviations
import robinhood_send_email as rhse
def portfolio_weight(trader):      
    #Grab current securities, positions, and portfolio info
    securities = trader.securities_owned()
    portfolios = trader.portfolios()
    account = trader.get_account()
    avg_pe = 0
    securities_tick = []
    weight = {}  
    #Cyle though securities and grab quote date
    for itick, security in enumerate(securities['results']):                       
        #Request current stock info
        securities_tick.append(trader.security_tick(security['instrument']))
        quote_data = trader.quote_data(securities_tick[itick])
        fundamentals = trader.fundamentals(securities_tick[itick])
        last_trade_price = quote_data['last_trade_price']
        quantity = security['quantity']
        #Calculate percentage of porfolio
        weight[securities_tick[itick]] = (float(quantity)*float(last_trade_price))\
                                         /float(portfolios['last_core_equity'])*100
        #Calculate average price to earning ratio of porfolio
        if fundamentals['pe_ratio'] is None:
            avg_pe += 0
        else:
            avg_pe += float(fundamentals['pe_ratio'])/float(len(securities['results'])) 
    #Add addtional amount of cash
    weight['Cash'] = (float(account['cash'])\
                     +float(account['uncleared_deposits'])\
                     +float(account['unsettled_funds']))\
                     /float(portfolios['last_core_equity'])*100      
    msg1 = ''
    #Send current profolio weighting
    for itick,percent in sorted(weight.iteritems(),key=lambda(k,v):(v,k),reverse=True):
        msg1 += '%s %s%%\n'\
        %(itick,str(percent)[:4])
        #Txt message can only be so long     
        if len(msg1) > 95:
            rhse.send_email(msg1,1)
            time.sleep(2)
            msg1 = ''
    msg1 += 'Avg. P/E %s\n'\
    %(str(avg_pe)[:4])
    rhse.send_email(msg1,1)
    time.sleep(2)    
    return securities_tick