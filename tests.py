import sys
import ally

<<<<<<< HEAD
<<<<<<< HEAD
n_tests = 3
=======
n_tests = 5
>>>>>>> updates
=======
n_tests = 3
>>>>>>> Option orders working!
tests = range(n_tests)

def Test(t):
    t = int(t)
<<<<<<< HEAD
<<<<<<< HEAD
    print("TEST " + str(t))
=======
#     print("TEST " + str(t))
>>>>>>> updates
=======
    print("TEST " + str(t))
>>>>>>> Option orders working!
    a = ally.Ally()
    
    
    if t == 1:
<<<<<<< HEAD
<<<<<<< HEAD
        orders = [
            ally.order.Order(
                instrument=ally.instrument.Equity('spy'),
                quantity=ally.order.Quantity(100),
                timespan=ally.order.Timespan('day'),
                type=ally.order.Buy(),
                price=ally.order.Market()
            )
            
=======
        instrument = ally.instrument.Equity('TSLA')
        print(instrument)
        op = ally.instrument.Put(instrument, "2019-10-18", 55)
        print(op)
=======
>>>>>>> Option orders working!
        orders = [
            ally.order.Order(
                instrument=ally.instrument.Equity('spy'),
                quantity=ally.order.Quantity(100),
                timespan=ally.order.Timespan('day'),
                type=ally.order.Buy(),
                price=ally.order.Market()
            )
<<<<<<< HEAD
>>>>>>> updates
=======
            
>>>>>>> Option orders working!
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
<<<<<<< HEAD
<<<<<<< HEAD
            
            
=======
             
>>>>>>> updates
=======
            
            
>>>>>>> Option orders working!

        print(ally.utils.option_format("ibm", "2014-01-18", 200.00, "call"))
        print(ally.utils.option_format())
        print(a.account_history())


    elif t == 3:

<<<<<<< HEAD
<<<<<<< HEAD
        a.holdings_chart('graph.png')
=======
        print(a.holdings_chart('graph.png'))
>>>>>>> updates
=======
        a.holdings_chart('graph.png')
>>>>>>> Option orders working!

            
            
            
            

    elif t == 4:
<<<<<<< HEAD
<<<<<<< HEAD
        a.get_quote('nvda','bid,ask')
        a.get_quote('nvda,chk,brk.b','bid,ask,vol')
        a.get_quote('','')
        a.get_quote()


=======
        print(a.get_quote('nvda','bid,ask'))
        print(a.get_quote('nvda,chk,brk.b','bid,ask,vol'))
        print(a.get_quote(['nvda','chk,brk.b'],['bid','ask','vol']))
=======
        a.get_quote('nvda','bid,ask')
        a.get_quote('nvda,chk,brk.b','bid,ask,vol')
>>>>>>> Option orders working!
        a.get_quote('','')
        a.get_quote()


<<<<<<< HEAD
        print(
            a.submit_order(
                order=order,
                verbose=True,
                preview=True
            )['response']
        )
                   
        
>>>>>>> updates
=======
>>>>>>> Option orders working!

if len(sys.argv) < 2:
    print("Running all tests:")
    for i in tests:
        Test(i)
else:
    Test(int(sys.argv[1]))
    
