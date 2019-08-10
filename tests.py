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
            ally.order.Long('TSLA',100,timespan='GFD'),
            ally.order.Long('TSLA',-100,timespan='GFD'),
            ally.order.Long(None,100),
        ]

        for order in orders:
            a.submit_order(order, verbose=True)
        

        
        
        
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
    
