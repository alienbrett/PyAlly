from enum		import Enum
from ..utils	import (
	option_format,
	option_symbol,
	option_strike,
	option_maturity,
	option_callput,
)
from .classes	import *
from .utils		import transposeTree, parseTree











class Order:
	
	_otype_dict_reverse = {
		OType.Order.value	: "Order",
		OType.Modify.value	: "OrdCxlRplcReq",
		OType.Cancel.value	: "OrdCxlReq"
	}

	_side_dict = {
		'buy':			Side.Buy,
		'sell':			Side.Sell,
		'sellshort':	Side.SellShort,
		'buycover':		Side.BuyCover
	}

	_time_dict = {
		'day':			TimeInForce.Day,
		'gtc':			TimeInForce.GTC,
		'onclose':		TimeInForce.OnClose
	}


	
	def __init__ ( self, fixml=None, buysell=None, symbol=None,
		price=None, qty=None, time=None, account=None, type_=OType.Order, orderid=None):
		"""Create an order
		Should be able to handle 2 different constructors:

		1) FIXML string input
		2) User-supplied information
		"""
		self.otype		= type_
		self.account	= None
		self.orderid	= None

		self.instrument	= None
		self.pricing	= None
		self.buysell	= None
		self.quantity	= 0


		if fixml is not None:
			# Constructor 1
			self._from_str ( fixml=fixml )

		else:
			# Constructor 2
			self._from_user (
				buysell=buysell,
				symbol=symbol,
				price=price,
				qty=qty,
				time=time,
				account=account,
				orderid=orderid
			)





	@property
	def convert_buysell ( self ):
		# Process buysell a wee bit
		x = None
		v = self.buysell.value

		if v == Side.Buy.value:
			x = { 'Side'	:'1' }

		elif v == Side.Sell.value:
			x = { 'Side'	:'2' }

		elif v == Side.BuyCover.value:
			x = { 'Side'	: '1', 'AcctTyp'  : '5' }

		elif v == Side.SellShort.value:
			x = { 'Side'	: '5' }

		return x





	

	@property
	def fixml ( self ):
		"""Compile the object into FIXML string
		Should not affect internal state of object
		"""

		# Store account information for this call
		account_info = {}
		if self.account is not None:
			account_info['Acct'] = self.account

		# Store order ID for this call
		orderid_info = {}
		if self.orderid is not None:
			account_info['OrigID'] = self.orderid



		# Properly format our order
		order = {
			'xmlns': "http://www.fixprotocol.org/FIXML-5-0-SP2",
			Order._otype_dict_reverse[self.otype.value]:	{
				**self.instrument.fixml,
				**self.price.attributes,
				**self.price.fixml,
				**self.convert_buysell,
				**account_info,
				**orderid_info,
				'TmInForce': self.time.value,
				'OrdQty': { 'Qty': self.quantity }
			}
		}

		# Rework our tree
		return transposeTree (
			order,			# The tree structure to turn into FIXML
			name='FIXML',	# Name of root tag
			stringify=True	# Please give us a string
		)
	



	@property
	def status ( self ):
		"""Return information about the execution state of this order
		"""
		pass






	def set_buysell ( self, buysell ):
		## Accept buysell information from string or enum
		if isinstance(buysell, str):
			buysell	= Order._side_dict[buysell.lower()]

		self.buysell	= buysell





	def set_orderid ( self, orderid ):
		"""Install this orderid
		Can be viewed at obj.orderid
		"""
		self.orderid = orderid





	def set_account ( self, account ):
		"""Set the account number for an order, so that orders
		are accepted properly
		"""
		self.account = int(account)






	def set_symbol ( self, symbol ):
		if len(symbol) > 15:
			# Almost certainly an option, if not unintelligible

			try:

				# Extract the symbol
				underlying	= option_symbol( symbol )

				# Extract strike price
				strike		= option_strike( symbol )

				# Extract expiration date
				exp_date	= option_maturity( symbol )

				# Extract 
				callput		= option_callput( symbol )

				# Wrap it up and spank it on the bottom!
				self.instrument = Option (
					direction	= callput,
					underlying	= underlying,
					exp_date	= exp_date,
					strike		= strike
				)

			except:
				raise
	
		self.instrument = Stock(symbol=symbol)
	





	def set_time ( self, time ):
		# Handle strings
		if isinstance(time, str):
			time = Order._time_dict[time.lower()]
		self.time = time





	def set_quantity ( self, qty ):
		self.quantity		= int(qty)




	def set_pricing ( self, priceobj ):
		self.price = priceobj



	
	def _from_str ( self, fixml ):
		"""Constructer 1)
		Read FIXML string into this object
		"""
		pass
	





	def _from_user ( self, buysell, symbol, price, qty, time, account, orderid ):
		"""Constructer 2) Read multiple inputs from user

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
				limpx = 123.45,
				stoppx = 120.00
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
	

		# BUYSELL INFO
		if buysell is not None:
			self.set_buysell(buysell)


		# TIME INFO
		if qty is not None:
			self.set_quantity(qty)


		# TIME INFO
		if time is not None:
			self.set_time ( time )


		# INSTRUMENT INFO
		if symbol is not None:
			self.set_symbol ( symbol )


		# TIME INFO
		if price is not None:
			self.set_pricing ( price )


		if account is not None:
			self.set_account ( account )


		if orderid is not None:
			self.set_orderid ( orderid )


