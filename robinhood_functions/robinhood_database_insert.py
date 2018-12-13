# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 23:15:20 2018

@author: Andy
"""
import sqlite3
def database_insert(trader,path,all_tick):
    #Connect to database
    print 'Connect DB'
    conn = sqlite3.connect(path)
    c = conn.cursor()
    #Loop through securities and watchlish to insert into database
    for itick in range(len(all_tick)):
        #Collect data for each quote to be stored
        quote_data = trader.quote_data(all_tick[itick])
        fundamentals = trader.fundamentals(all_tick[itick])
        popularity = trader.get_popularity(all_tick[itick])
        news = trader.get_news(all_tick[itick])
        opinion = 1
        for story in news['results']:
            #Do we have new stories added since the previous day
            if story['published_at'][:10] > quote_data['previous_close_date']:
                #Analyze news to extablish a compounded opinion parameter
                full_article = story['title'].lower() + story['summary'].lower()
                #Ultra-positive keyword searchs    
                if ('upgrade' in full_article) or\
                   ('beat' in full_article) or\
                   ('boost' in full_article) or\
                   ('raise' in full_article) or\
                   ('exceed' in full_article) or\
                   ('soar' in full_article) or\
                   ('propel' in full_article) or\
                   ('shine' in full_article) or\
                   ('lift' in full_article) or\
                   ('blast' in full_article) or\
                   ('bull' in full_article) or\
                   ('victory' in full_article):
                       opinion = opinion*1.15
                #Ultra-negative keyword searchs
                if ('downgrade' in full_article) or\
                   ('miss' in full_article) or\
                   ('plunge' in full_article) or\
                   ('dip' in full_article) or\
                   ('tumble' in full_article) or\
                   ('disappoint' in full_article) or\
                   ('slide' in full_article) or\
                   ('cut' in full_article) or\
                   ('suspend' in full_article) or\
                   ('bear' in full_article) or\
                   ('defeat' in full_article):
                       opinion = opinion*0.85
                #Semi-positive keyword searchs       
                if ('poise' in full_article) or\
                   ('urge' in full_article) or\
                   ('buyback' in full_article) or\
                   ('in-line' in full_article) or\
                   ('perk' in full_article) or\
                   ('approval' in full_article) or\
                   ('positive' in full_article) or\
                   ('long' in full_article):
                       opinion = opinion*1.05
                #Semi-negative keyword searchs
                if ('linger' in full_article) or\
                   ('warning' in full_article) or\
                   ('softness' in full_article) or\
                   ('worr' in full_article) or\
                   ('trim' in full_article) or\
                   ('weak' in full_article) or\
                   ('in the red' in full_article) or\
                   ('fear' in full_article) or\
                   ('negative' in full_article) or\
                   ('short' in full_article) or\
                   ('vioatil' in full_article):
                       opinion = opinion*0.95
        #Create row to be inserted
        enterticks = (quote_data['previous_close_date'],all_tick[itick],
                     quote_data['previous_close'],fundamentals['low_52_weeks'],
                     fundamentals['high_52_weeks'],fundamentals['average_volume'],
                     fundamentals['dividend_yield'],fundamentals['pe_ratio'],
                     popularity, opinion)   
        # Insert a row of data
        c.execute('INSERT INTO stocks VALUES (?,?,?,?,?,?,?,?,?,?)', enterticks)
    # Save (commit) the changes and close
    print 'Committ DB'
    conn.commit()
    conn.close()
    return all_tick