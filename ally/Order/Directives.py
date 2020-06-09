from ..exception	import (
	TimeInForceException,
	PriceException
)
from ..FIXML		import FIXML, OrderType
from .instrument	import implySymbol
from .order			import *




def Order ( buysell, symbol, price, qty, time ):
	"""Easy function to create an order encapsulation.


	buysell:
		Specify the postion desired.

		- 'buy' 		Buy to open a long position
		- 'sell'		Sell to close a long position
		- 'sellshort'	Sell to open a short position
		- 'buycover'	Buy to close a short position
	

	symbol:
		Enter the symbol of the instrument to be traded.
		  You can use ally.utils.option_format(...)
		    to generate the OCC-standard option symbol

		- 'spy'					Equivalent to 'SPY'
		- 'SPY200529C00305000'	SPY 2020-05-29 Call @ $305.00


	price:
		Specify the pricing options for execution.

		- Market()					Market (whatever price the market gives you)
		- Limit(123.45)				Limit (execute trade no less-favorably than value)
		- Stop(123.45)				Stop (execute a market order once the price passes this value)
		- StopLimit (				Stop Limit (Once the stop price is reached, submit a limit order)
			Stop ( 123.45 ),
			Limit ( 120.00 )
		)
		- StopLoss (				Stop Loss order (same as trailing stop)
			pct = True, [default]		specify whether to treat stop as percent or dollar value
			stop=5.0
		)

	
	qty:
		Specify the number of shares (or contracts, for options)
			to be purchased.

		- 10	Accepts integers, no fractions though


	time:
		Specify the time-in-force of the order.

		- 'day'				# Good-For-Day
		- 'gtc'				# Good-'till-Cancelled
		- 'marketonclose'	# Market-On-Close

	"""

	# Quantity
	qty		= str(int(qty))


	# Side
	side	= Side(buysell)
	isBuy	= side['Side'] == '1'

	



	try:
		# Price
		if price['__execution'] == 'stop limit':
			price['OfstVal'] = price.get('__stop') * (-1 if isBuy else 1)
	except:
		raise PriceException(
			"""Price {0} is invalid.
			Use a wrapper like Market(), etc.  Look in ally.Order.order for available constructors.
			""".format(str(price))
		)



	x = {
		**Timespan ( time ),
		**side,
		**price,
		'Instrmt':{
			**implySymbol(symbol)
		},
		'OrdQty':{
			'__quantity' : qty,
			'Qty'		: qty
		}
	}



	if x['Instrmt']['SecTyp'] == 'OPT':
		x['OrdQty']['Qty'] = str(round(float(x['Order']['OrdQty']['Qty'])))

	return FIXML(order=x)











def Cancel ( order):
	"""Give me an order, and I'll cancel it for you
	"""
	
	return FIXML (
		order	= order,
		orderid	= order._id,
		otype	= OrderType.Cancel
	)


def Modify ( order ):
	"""If the order you gave me was just made,
	"""
	pass
