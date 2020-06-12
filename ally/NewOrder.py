from enum		import Enum
from .utils		import (
	option_format,
	option_symbol,
	option_strike,
	option_maturity,
	option_callput,
)

import xml.etree.ElementTree as ET
from .FIXML.utils	import transposeTree, parseTree
import unittest


class OType(Enum):
	Order	= 1
	Modify	= 2
	Cancel	= 3


class Side(Enum):
	Buy			= 1
	Sell		= 2
	BuyCover	= 3
	SellShort	= 4


class SubmitStatus(Enum):
	NotSubmitted	= 1
	Submitted		= 2
	Pending			= 3
	Open			= 4
	Paritial		= 5
	Filled			= 6




class TimeInForce(Enum):
	Day		= 0
	GTC		= 1
	OnClose	= 7



class Instrument:
	"""Handle all the bullshit around an instrument
	"""
	pass






### Pricing information

class PriceType(Enum):
	Market			= 1
	Limit			= 2
	Stop			= 3
	StopLimit		= 4
	StopLoss		= 5
	TrailingStop	= 6


class Pricing:
	_tag = {}

	@property
	def attributes(self):
		return self._data


	@property
	def fixml(self):
		return self._tag
		


class Market(Pricing):
	type_	= PriceType.Market
	_data	= { 'Typ': '1' }
	


class Limit(Pricing):
	type_	= PriceType.Limit
	_data	= { 'Typ': '2' }

	def __init__ ( self, limpx ):
		self.px = round(float(limpx),2)
		self._data['Px'] = str(self.px)



class Stop(Pricing):
	type_	= PriceType.Stop
	_data	= { 'Typ': '3' }

	def __init__ ( self, stoppx ):
		self.stoppx = round(float(stoppx),2)	
		self._data['StopPx'] = str(self.stoppx)



class StopLimit(Pricing):
	type_	= PriceType.StopLimit
	_data	= { 'Typ': '4' }

	def __init__ ( self, limpx, stoppx ):
		self.px		= round(float(limpx),2)
		self.stoppx	= round(float(stoppx),2)
		self._data['Px']		= str(self.px)
		self._data['StopPx']	= str(self.stoppx)



class TrailingStop(Pricing):
	type_	= PriceType.TrailingStop
	_data	= { 'Typ': 'P' }

	def __init__ ( self, use_pct, offset ):
		"""Create trailing stop order
		use_pct:
			- True	# Interpret 1.0 offset as 1%
			- False	# Interpret 1.0 offset as $1.00
		"""
		self._tag = {'PegInstr': {
			'OfstTyp': 1 if use_pct else 0,
			'PegPxTyp': 1,
			'OfstVal': offset
		}}






class Option(Instrument):
	type_='OPTION'
	def __init__(self, underlying, exp_date, strike, direction ):
		self.underlying = underlying.upper()
		self.exp_date	= exp_date
		self.strike		= strike
		self.direction	= 'CALL' if 'c' in direction.lower() else 'PUT'

		# Also get the option
		self.symbol		= option_format (
			symbol		= self.underlying,
			exp_date	= self.exp_date,
			strike		= self.strike,
			direction	= self.direction
		)
	
	@property
	def fixml ( self ):
		return {
			'Instrmt': {
				'CFI'	: 'O' + self.direction[0],
				'SecTyp': 'OPT',
				'MatDt'	: self.exp_date + "T00:00:00.000-05:00",
				'StrkPx': self.strike,
				'Sym'	: self.underlying
			}
		}

class Stock(Instrument):
	type_='STOCK'
	def __init__(self,symbol):
		self.symbol = symbol.upper()

	@property
	def fixml ( self ):
		return {'Instrmt': { 'SecTyp': 'CS', 'Sym': self.symbol}}







	






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


##### TESTS






class TestOrderManual(unittest.TestCase):



	def test_buysell_buy (self):

		o = Order(buysell='buy')
		self.assertEqual(o.buysell, Side.Buy, "Should be Side.Buy")
		o = Order(buysell=Side.Buy)
		self.assertEqual(o.buysell, Side.Buy, "Should be Side.Buy")

	def test_buysell_sell (self):

		o = Order(buysell='sell')
		self.assertEqual(o.buysell, Side.Sell, "Should be Side.Sell")
		o = Order(buysell=Side.Sell)
		self.assertEqual(o.buysell, Side.Sell, "Should be Side.Sell")

	def test_buysell_sellshort (self):

		o = Order(buysell='sellshort')
		self.assertEqual(o.buysell, Side.SellShort, "Should be Side.SellShort")
		o = Order(buysell=Side.SellShort)
		self.assertEqual(o.buysell, Side.SellShort, "Should be Side.SellShort")

	def test_buysell_buycover (self):

		o = Order(buysell='buycover')
		self.assertEqual(o.buysell, Side.BuyCover, "Should be Side.BuyCover")
		o = Order(buysell=Side.BuyCover)
		self.assertEqual(o.buysell, Side.BuyCover, "Should be Side.BuyCover")


	def test_quantity ( self ):

		o = Order(qty=10)
		self.assertEqual(o.quantity, 10, "Should be 10")
		o = Order(qty=10.5)
		self.assertEqual(o.quantity, 10, "Should be 10")
		o = Order(qty="10")
		self.assertEqual(o.quantity, 10, "Should be 10")



	def test_price_market ( self ):
		o = Order(time='onclose')
		self.assertEqual(o.time, TimeInForce.OnClose, "Should be TimeInForce.OnClose")
		o = Order(time=TimeInForce.OnClose)
		self.assertEqual(o.time, TimeInForce.OnClose, "Should be TimeInForce.OnClose")






class TestInstrumentConstruction(unittest.TestCase):
	
	def test_option_construction(self):
		op = Option (
			direction='call',
			exp_date = '2011-02-11',
			strike = 16,
			underlying = 'f'
		)
		self.assertEqual(
			op.fixml,
			{
				'Instrmt': {
					'CFI':"OC",
					'SecTyp':"OPT",
					'MatDt':"2011-02-11T00:00:00.000-05:00",
					'StrkPx': 16,
					'Sym':"F"
					}
			},
			'From ally website'
		)

		op = Option (
			direction='PuT',
			exp_date = '2014-01-18',
			strike = 190,
			underlying = 'IbM'
		)
		self.assertEqual(
			op.fixml,
			{
				'Instrmt': {
					'CFI':"OP",
					'SecTyp':"OPT",
					'MatDt':"2014-01-18T00:00:00.000-05:00",
					'StrkPx': 190,
					'Sym':"IBM"
					}
			},
			'From ally website'
		)
	
	def test_stock_construction(self):
		s = Stock (symbol='f')
		self.assertEqual(
			s.fixml,
			{ 'Instrmt': { 'SecTyp':'CS', 'Sym':'F' } },
			"From ally website"
		)





class TestPricingConstruction(unittest.TestCase):
	
	def test_market_construction(self):
		p = Market()
		self.assertEqual(
			p.attributes,
			{'Typ':'1'},
			"Should have type 1"
		)



	def test_limit_construction(self):
		p = Limit(limpx=10.51)
		self.assertEqual(
			p.attributes,
			{'Typ':'2', 'Px':'10.51'},
			"Should have type 2, with Px included"
		)
		p = Limit(limpx=10.51141)
		self.assertEqual(
			p.attributes,
			{'Typ':'2', 'Px':'10.51'},
			"Should have type 2, with Px included"
		)
	


	def test_stop_construction(self):
		p = Stop(stoppx=10.51)
		self.assertEqual(
			p.attributes,
			{ 'Typ':"3", 'StopPx':"10.51"},
			"Should have typ 3, with StopPx included"
		)
		p = Stop(stoppx=10.5112312)
		self.assertEqual(
			p.attributes,
			{ 'Typ':"3", 'StopPx':"10.51"},
			"Should have typ 3, with StopPx included"
		)


	def test_stoplimit_construction(self):
		p = StopLimit(limpx = 10.1, stoppx = 10.51)
		self.assertEqual(
			p.attributes,
			{ 'Typ':"4", 'Px': '10.1', 'StopPx':"10.51" },
			"Should have typ 3, with StopPx included"
		)



	def test_trailingstop_construction(self):
		p = TrailingStop(
			use_pct = True,
			offset = 1.12
		)
		self.assertEqual(
			p.attributes,
			{ 'Typ':"P"},
			"Should have typ P"
		)
		self.assertEqual(
			p.fixml,
			{
				'PegInstr': {
					'OfstTyp': 1,
					'PegPxTyp': 1,
					'OfstVal': 1.12
				}
			},
			"Should include tag with peginstr"
		)



		p = TrailingStop(
			use_pct = False,
			offset = 5.69
		)
		self.assertEqual(
			p.attributes,
			{ 'Typ':"P"},
			"Should have typ P"
		)
		self.assertEqual(
			p.fixml,
			{
				'PegInstr': {
					'OfstTyp': 0,
					'PegPxTyp': 1,
					'OfstVal': 5.69
				}
			},
			"Should include tag with peginstr"
		)



class TestOrderConstruction(unittest.TestCase):
	
	def assertEqualXML( self, s1, s2, msg, verbose=False ):
		s1 = ET.tostring(ET.fromstring(s1))
		s2 = ET.tostring(ET.fromstring(s2))
		if verbose:
			print()
			print(s1)
			print(s2)
		self.assertEqual(
			s1,
			s2,
			msg
		)


	def test_market_stock_buy_day(self):
		o = Order (
			buysell = 'buy',
			time	= 'day',
			symbol	= 'f',
			qty		= 1,
			price	= Market(),
			account	= '12345678'
		)

		self.assertEqualXML(
			o.fixml,
			'<FIXML xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2"><Order TmInForce="0" Typ="1" Side="1" Acct="12345678"><Instrmt SecTyp="CS" Sym="F"/><OrdQty Qty="1"/></Order></FIXML>',
			"Straight from the ally website"
		)
	

	def test_market_stock_sell_day(self):
		o = Order (
			buysell = 'sell',
			time	= 'day',
			symbol	= 'ibm',
			qty		= 1,
			price	= Market()
		)
		o.set_account(12345678)

		self.assertEqualXML(
			o.fixml,
			'<FIXML xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2"><Order Acct="12345678" TmInForce="0" Typ="1" Side="2"><Instrmt SecTyp="CS" Sym="IBM"/><OrdQty Qty="1"/></Order></FIXML>',
			"Straight from the ally website"
		)




	def test_market_stock_short_day(self):
		o = Order (
			buysell = 'sellshort',
			time	= 'day',
			symbol	= 'f',
			qty		= 1,
			price	= Limit(22),
			account	= '12345678'
		)

		self.assertEqualXML(
			o.fixml,
			'<FIXML xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2"><Order TmInForce="0" Typ="2" Side="5" Px="22.0" Acct="12345678"><Instrmt SecTyp="CS" Sym="F"/><OrdQty Qty="1"/></Order></FIXML>',
			"Straight from the ally website"
		)



	def test_market_stock_cover_day(self):
		o = Order (
			buysell = 'buycover',
			time	= 'day',
			symbol	= 'f',
			qty		= 1,
			price	= Limit(13),
			account	= '12345678'
		)

		self.assertEqualXML(
			o.fixml,
			'<FIXML xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2"><Order TmInForce="0" Typ="2" Side="1" AcctTyp="5" Px="13.0" Acct="12345678"><Instrmt SecTyp="CS" Sym="F"/><OrdQty Qty="1"/></Order></FIXML>',
			"Straight from the ally website"
		)




	def test_modify_market_stock_buy_day(self):
		o = Order (
			type_	= OType.Modify,
			buysell = 'buy',
			time	= 'day',
			symbol	= 'f',
			qty		= 1,
			price	= Limit(15),
			account	= '12345678',
			orderid	= 'SVI-12345678'
		)

		self.assertEqualXML(
			o.fixml,
			'<FIXML xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2"><OrdCxlRplcReq TmInForce="0" Typ="2" Side="1" Px="15.0" Acct="12345678" OrigID="SVI-12345678"><Instrmt SecTyp="CS" Sym="F"/><OrdQty Qty="1"/></OrdCxlRplcReq></FIXML>',
			"Straight from the ally website"
		)
