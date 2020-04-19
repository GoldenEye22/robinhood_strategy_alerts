# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 21:57:08 2018

@author: Andy
"""
import time
import numpy as np
#Import functions as abbreviations
import robinhood_functions.robinhood_send_email as rhse
def portfolio_weight(trader):      
    #Grab current securities, positions, and portfolio info
    securities = trader.securities_owned()
    portfolios = trader.portfolios()
    account = trader.get_account()
    avg_pe = 0
    securities_tick = []
    weight = {}  
    total_return = {}
    dividend_yield = {}
    #Cyle though securities and grab quote date
    for itick, security in enumerate(securities['results']):                       
        #Request current stock info
        securities_tick.append(trader.security_tick(security['instrument']))
        try:
            quote_data = trader.quote_data(securities_tick[itick])
            fundamentals = trader.fundamentals(securities_tick[itick])
            last_trade_price = quote_data['last_trade_price']
            quantity = security['quantity']
            average_buy_price = security['average_buy_price']
            #Calculate percentage of porfolio
            weight[securities_tick[itick]] = np.around((float(quantity)*float(last_trade_price))\
                                             /float(portfolios['last_core_equity'])*100,1)
            #Calculate Total Return of Profolio
            if float(average_buy_price) == 0:
                total_return[securities_tick[itick]] = 0
            else:
                total_return[securities_tick[itick]] = np.around((float(last_trade_price)\
                                                       /float(average_buy_price) - 1)*100,1)                                                  
            #Calculate average price to earning ratio of porfolio
            if fundamentals['pe_ratio'] is None:
                avg_pe += 0
            else:
                avg_pe += float(fundamentals['pe_ratio'])/float(len(securities['results']))
            #Grab Dividend Yields 
            if fundamentals['dividend_yield'] is None:
                dividend_yield[securities_tick[itick]] = 0
            else:
                dividend_yield[securities_tick[itick]] = np.around(\
                                                         float(fundamentals['dividend_yield']),1)
        except:
            print (securities_tick[itick] + ' Quote Does Not Exist')
            securities_tick.remove(trader.security_tick(security['instrument']))
            pass
    #Add addtional amount of cash
    weight['Cash'] = np.around((float(account['cash'])\
                     +float(account['uncleared_deposits'])\
                     +float(account['unsettled_funds']))\
                     /float(portfolios['last_core_equity'])*100,1)
    total_return['Cash'] = ''
    dividend_yield['Cash'] = ''
    msg1 = ''
    #Send current profolio weighting
    for itick,percent in [(k, weight[k]) for k in sorted(weight, key=weight.get, reverse=True)]:
        if itick != 'Cash':
            msg1 += '%s %s%%, TR: %s%%, D/Y: %s%%\n'\
            %(itick,str(percent),str(total_return[itick]),str(dividend_yield[itick]))
        else:
            msg1 += '%s %s%%\n'\
            %(itick,str(percent))
        #Txt message can only be so long     
        if len(msg1) > 1000:
            rhse.send_email(msg1,1)
            time.sleep(5)
            msg1 = ''
    msg1 += 'Avg. P/E %s'\
    %(str(avg_pe)[:4])
    rhse.send_email(msg1,1)
    time.sleep(5)    
    return securities_tick