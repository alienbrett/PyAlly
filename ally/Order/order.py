from ..exception import (
	TimeInForceException,
	PriceException
)
from ..FIXML		import FIXML
from .instrument	import implySymbol





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

		elif buysell == 'sell':
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

		elif buysell == 'sellshort':
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



def injectAccount ( order, acct ):
	"""Given an order, inject the account information
	"""
	order['Acct'] = str(int(acct))

	return order
