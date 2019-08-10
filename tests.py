from ally import *


print("TEST 1:")
a = Ally()
long = order.Long('TSLA',100,timespan='GFD')
short = order.Long('TSLA',-100,timespan='GFD')

print("LONG")
a.submit_order(long, verbose=True)

print("short")
a.submit_order(short, verbose=True)




print("TEST 2:")
print(Ally.option_format("ibm", "2014-01-18", 200.00, "call"))

a = Ally()
print(a.account_history())



print("TEST 3:")
a = Ally()
a.holdings_chart('graph.png')