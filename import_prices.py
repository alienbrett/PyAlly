import yfinance as yf
import pandas as pd
import mysql.connector
import datetime

spy_file = '/home/alienbrett/python_finance/data/spy500.txt'

def load_spy500_5d(host, user, password, db, table):
    with open(spy_file, 'r') as f:
        load_intraday(host, user, password, db, table, f.read())

def load_intraday(host, user, password, db, table, symbols):
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=password,
        database=db
    )
    sql = "insert ignore into " + table + " (open, high, low, close, volume, sym, datetime) values (%s,%s,%s,%s,%s,%s,%s)"
    mycursor = mydb.cursor()
    
    for sym in symbols.split(' '):
        sym = sym.upper()
        try:
            df = yf.download(
                tickers=sym,
                period='5d',
                interval='1m',
                auto_adjust=True
            )
        except:
            pass
        f = '%Y-%m-%d %H:%M:%S'
        df['sym'] = sym
        df['date'] = df.index.strftime(f)
        
        print(df.tail())
        tuples = [tuple(x) for x in df.values]
        print(tuples[:5])
        
        mycursor.executemany(sql,tuples)
        mydb.commit()
        print(mycursor.rowcount, "was inserted")
