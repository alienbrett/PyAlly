from ..exception import (
	TimeInForceException,
	PriceException
)
from ..FIXML		import FIXML
from .instrument import implySymbol





def orderReqType(order):
	"""Return the string that corresponds to the order's request type"""
	for x in ('Order','OrdCxlRplcReq','OrdCxlReq'):
		if x in order.keys():
			return x

# Order Lifetime constructors
#################################################
def Timespan( type_ = 'day' ):
	type_ = type_.lower()
	
	# for the day
	if type_ == 'day' or type_ == 'gfd':
		return {
			'__timeframe':'GFD',
			'TmInForce':'0'
		}
	
	# Market on close (wtf ???)
	elif type_ == 'marketonclose':
		 return {
			'__timeframe':'MarketOnClose',
			'TmInForce':'7'
		 }
		
	# GTC order
	elif type_ == 'gtc':
		return {
			'__timeframe':'GTC',
			'TmInForce':'1'
		 }
	
	#Something went wrong
	else:
		raise TimeInForceException(
			"""Invalid time: "{0}". Valid times are:
			"day", "gfd", or "marketonclose"
			""".format(type_)
		)






def Side ( buysell ):
	"""Wrap the buy-sell order type.

	buysell:
		- 'buy' 		Buy to open a long position
		- 'sell'		Sell to close a long position

		- 'sellshort'	Sell to open a short position
		- 'buycover'	Buy to close a short position
	
	"""
	try:
		buysell = buysell.lower()
		
		x = None
		if buysell == 'buy':
			x = {
				'__side'  :'buy',
				'Side'	:'1'
			}

		elif buysell == 'sellshort':
			x = {
				'__side'  : 'sell',
				'Side'	:'2'
			}

		elif buysell == 'buycover':
			x = {
				'__side'  : 'buy_to_cover',
				'Side'	: '1',
				'AcctTyp'  : '5'
			}

		elif buysell == 'sell':
			x = {
				'__side'  :'sell_short',
				'Side'	: '5'
			}

		return x

	except:
		raise BuySellException
		
		





# Order Pricing constructors
#################################################
def StopLoss( pct=True, stop=5 ):
	"""If pct == true?
	treat stop as percent
	if pct == false?
	treat stop as dollar amnt
	"""
	return {
			'__execution'	: 'stop limit',
			'Typ'			: 'P',
			'ExecInst'		: 'a',
			'PegPxTyp'		: '1',
			'OfstTyp'		: '0' if pct else '1',
			'__stop'		: str(float(stop))
		}
	
	
# Pass in sub-orders
def StopLimit(stopOrder, limitOrder):
	return {
		'__execution' : 'stop limit',
		'Typ'	: '4',
		'Px'	 : limitOrder['Px'],
		'StopPx' : stopOrder['StopPx'],
	}
	
	
def Market():
	return {
		'__execution' :'market',
		'Typ'	:'1'
	}
	

def Limit(limit):
	return {
		'__execution' :'limit',
		'Typ'	:'2',
		'Px'	 :str(float(limit))
	}
	

def Stop(stop):
	return {
		'__execution' :'stop',
		'Typ'	:'3',
		'StopPx' : str(float(stop))
	}




# Unusual order requests
#################################################


def Cancel(orderid, order=None):
	"""Convert an order into a cancel order
	It's unclear in the Ally Invest API documentation whether or not the order information
	must match the original order request. Maybe a user only needs the order ID?"""

	# make sure order is at least nominally ok
	if order==None:
		order = Order(
			Timespan('gtc'),
			Buy(),
			Market(),
			{},
			Quantity(0)
			)


	# Handle two cases
	if 'Order' in order.keys():
		order['OrdCxlReq'] = order.pop('Order')

	elif 'OrdCxlRplcReq' in order.keys():
		order['OrdCxlReq'] = order.pop('OrdCxlRplcReq')

	else:
		order = {'error':"Don't try to submit this order, it's malformatted. Missing order request type"}
		return order


	order['OrdCxlReq']['OrigID'] = str(orderid)
	return order



def Modify(neworder, orderid):
	"""Given a new order, and a different order ID,
	Cancel the old and replace with some new order in a single step"""

	if 'Order' in neworder.keys():
		neworder['OrdCxlRplcReq'] = neworder.pop('Order')
		neworder['OrdCxlRplcReq']['OrigID'] = str(neworderid)
	elif 'OrdCxlRplcReq' in neworder.keys():
		neworder['OrdCxlRplcReq']['OrigID'] = str(neworderid)
	else:
		order = { 'error':
			"Don't try to submit this order, it's malformatted. Missing order request type, or it looks cancelled already"
		}
		return order











def Order (
	buysell	= 'buy',
	symbol	= '',
	price	= None,
	qty		= 1,
	time	= 'day',
	acct	= None
):
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









def injectAccount ( order, acct ):
	"""Given an order, inject the account information
	"""
	order['Order']['Acct'] = str(int(acct))

	return order
