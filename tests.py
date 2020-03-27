import sys
import ally
import json
import pandas as pd

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
		print(json.dumps(a.account_history(),indent=4))


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

	elif t == 9:
		print("Attempting market streaming")
		print(
			a.quote_stream(
				symbols='SPY'
			)
		)
	elif t == 10:
		print("market info:",
			json.dumps(
				a.market_clock(),
				indent=4
			)
		)
		print("api server info:",
			json.dumps(
				a.api_status(),
				indent=4
			)
		)

	elif t == 11:
		print("timesales")
		n_pages = 10
		for i in range(n_pages):
			print(i)
			x = a.timesales(
				symbols='spy',
				rpp=str(n_pages),
				interval='1min',
				index=str(i),
				startdate='2020-03-26'
			)

			print("Found ",len(x),"ticks")
			print(json.dumps(x,indent=4))
			df = pd.DataFrame(x)
			df['datetime'] = pd.to_datetime(df['datetime'])
			df = df.set_index('datetime')
			df.to_csv('/tmp/df.csv'+str(i))

	elif t == 12:
		print("Get member information:")
		print(
			json.dumps(
				a.get_member(),
				indent=4
			)

		)
		

if len(sys.argv) < 2:
	print("Running all tests:")
	for i in tests:
		Test(i)
else:
	Test(int(sys.argv[1]))
	
