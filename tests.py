import sys
import ally

<<<<<<< HEAD
n_tests = 3
=======
n_tests = 5
>>>>>>> updates
tests = range(n_tests)

def Test(t):
    t = int(t)
<<<<<<< HEAD
    print("TEST " + str(t))
=======
#     print("TEST " + str(t))
>>>>>>> updates
    a = ally.Ally()
    
    
    if t == 1:
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
        orders = [
            ally.order.Order(
                timespan=ally.order.Timespan('GTC'),
                price=ally.order.Market(),
                type=ally.order.Buy()
            ),
            ally.order.Order(
                timespan=ally.order.Timespan('day'),
                price=ally.order.Stop(100.0),
                type=ally.order.Sell(False)
            )
>>>>>>> updates
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
            
            
=======
             
>>>>>>> updates

        print(ally.utils.option_format("ibm", "2014-01-18", 200.00, "call"))
        print(ally.utils.option_format())
        print(a.account_history())


    elif t == 3:

<<<<<<< HEAD
        a.holdings_chart('graph.png')
=======
        print(a.holdings_chart('graph.png'))
>>>>>>> updates

            
            
            
            

    elif t == 4:
<<<<<<< HEAD
        a.get_quote('nvda','bid,ask')
        a.get_quote('nvda,chk,brk.b','bid,ask,vol')
        a.get_quote('','')
        a.get_quote()


=======
        print(a.get_quote('nvda','bid,ask'))
        print(a.get_quote('nvda,chk,brk.b','bid,ask,vol'))
        print(a.get_quote(['nvda','chk,brk.b'],['bid','ask','vol']))
        a.get_quote('','')

    
    elif t == 5:
#         print(a.get_strike_prices('nvda'))
#         print(a.get_strike_prices('chk'))
#         print(a.get_exp_dates('aapl'))
#         print(a.get_exp_dates('nvda'))

        print("CALLS")
        op_chain = a.options_chain(
            symbol="spy",
            exp_date="20191018",
            direction="c"
        )
        for op in op_chain:
            print(op['issue_desc'] +  "\t( $" + str(op['ask']).rjust(5,' ') + " )" \
                  + ("(ITM)" if op['in_the_money'] else "")\
                 )
            
        print("PUTS")
        op_chain = a.options_chain(
            symbol="spy",
            exp_date="20191018",
            direction="p"
        )
        for op in op_chain:
            print(op['issue_desc'] +  "\t( $" + str(op['ask']).rjust(5,' ') + " )" \
                  + ("(ITM)" if op['in_the_money'] else "".rjust(4,' ')) \
                 )
        
        ops = a.search_options(
            symbol="spy",
            query="xdate-eq:20191018 AND put_call-eq:call",
            fields="bid,ask,vol"
        )
        
        
        
        
        
    elif t == 6:
        
        
        
        
        dates = a.get_exp_dates("spy")
        print(dates)
            
            
            
            
            
            
            
    elif t == 7:
        
        
        instrument = ally.instrument.Equity('SPY')
        op = ally.instrument.Put(instrument, "2019-10-18", 291)
        
        
        order = ally.order.Order(
            timespan=ally.order.Timespan('day'),
            price=ally.order.Market(),
            type=ally.order.Buy(),
            instrument=instrument,
            quantity=ally.order.Quantity(1)
        )

        print(
            a.submit_order(
                order=order,
                verbose=True,
                preview=True
            )['response']
        )
                   
        
>>>>>>> updates

if len(sys.argv) < 2:
    print("Running all tests:")
    for i in tests:
        Test(i)
else:
    Test(int(sys.argv[1]))
    
