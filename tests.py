import sys
import ally

n_tests = 3
tests = range(n_tests)

def Test(t):
    t = int(t)
    print("TEST " + str(t))
    a = ally.Ally()
    
    
    if t == 1:
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
            print(a.submit_order(
                order,
                quantity=ally.order.Quantity(10),
                instrument=instrument,
                verbose=True,
            ))
        
        for order in orders:
            print(a.submit_order(
                order,
                quantity=ally.order.Quantity(10),
                instrument=op,
                verbose=True,
            ))

        
        
        
    elif t == 2:
            
            

        print(ally.utils.option_format("ibm", "2014-01-18", 200.00, "call"))
        print(ally.utils.option_format())
        print(a.account_history())


    elif t == 3:

        a.holdings_chart('graph.png')

            
            
            
            

    elif t == 4:
        a.get_quote('nvda','bid,ask')
        a.get_quote('nvda,chk,brk.b','bid,ask,vol')
        a.get_quote('','')
        a.get_quote()



if len(sys.argv) < 2:
    print("Running all tests:")
    for i in tests:
        Test(i)
else:
    Test(int(sys.argv[1]))
    
