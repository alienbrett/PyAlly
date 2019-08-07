from ally import *


a = Ally('keyfile.json')
long = order.Long('TSLA',100,timespan='GFD')
short = order.Long('TSLA',-100,timespan='GFD')

print("LONG")
a.submit_order(long, verbose=True)

print("short")
a.submit_order(short, verbose=True)