import sys
import ally
import json

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
			print(a.submit_order(order,verbose=True))
		

		
		
		
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

	elif t == 5:

		print(a.get_quote('ally'))
		help(a.get_holdings)

	elif t == 6:



		orders = [
			ally.order.Order(
				instrument=ally.instrument.Equity('nflx'),
				quantity=ally.order.Quantity(20),
				timespan=ally.order.Timespan('day'),
				type=ally.order.Sell(),
				price=ally.order.Limit(400)
			)
		]
		ids = [ a.submit_order(order, preview=True, verbose=False) for order in orders ]
		
		for i in ids:
			# ensure we're only considering 200's
			if i['response']:
				print(json.dumps(i['response'], indent=4, sort_keys=True))

	elif t == 7:


		# View prior orders
		o = ally.order.Cancel(sys.argv[2])
		print(json.dumps(o, indent=4))
		x = a.submit_order(o,verbose=True)
		print(json.dumps(x, indent=4))


	elif t == 8:
		ts = a.timesales('spy',interval='1min',startdate='2020-03-26')
		print(
			json.dumps( ts, indent=4, sort_keys=True)
		)
		

if len(sys.argv) < 2:
	print("Running all tests:")
	for i in tests:
		Test(i)
else:
	Test(int(sys.argv[1]))
	
