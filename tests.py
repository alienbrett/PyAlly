import sys
import ally

n_tests = 5
tests = range(n_tests)

def Test(t):
    t = int(t)
    print("TEST " + str(t))
    a = ally.Ally()
    
    
    if t == 1:
        
        instrument = ally.instrument.Equity('TSLA')
        print(instrument)
        op = ally.instrument.Put(instrument, "2019-10-18", 55)
        print(op)
        
        
        
        orders = [
            ally.order.Order(
                instrument=ally.instrument.Equity('spy'),
                quantity=ally.order.Quantity(100),
                timespan=ally.order.Timespan('day'),
                type=ally.order.Buy(),
                price=ally.order.Market()
            )
        ]

        for order in orders:
            print(a.submit_order(order))
        

        
        
        
    elif t == 2:

        print(ally.utils.option_format("ibm", "2014-01-18", 200.00, "call"))
        print(ally.utils.option_format())
        print(a.account_history())


    elif t == 3:

        print(a.holdings_chart('graph.png'))

            
            
            
            

    elif t == 4:
        print(a.get_quote('nvda','bid,ask'))
        print(a.get_quote('nvda,chk,brk.b','bid,ask,vol'))
        print(a.get_quote(['nvda','chk,brk.b'],['bid','ask','vol']))


        

if len(sys.argv) < 2:
    print("Running all tests:")
    for i in tests:
        Test(i)
else:
    Test(int(sys.argv[1]))
    
