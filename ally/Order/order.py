# MIT License
#
# Copyright (c) 2020 Brett Graves
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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



	def __init__ ( self,
		buysell: str =None,
		symbol: str =None,
		price=None,
		qty: int =None,
		time: int =None,
		account=None,
		type_=OType.Order,
		orderid=None,
		fixml=None
	):
		"""Creates an order.

		Args:

			buysell:
				Specify the postion desired.


			symbol:
				Enter the symbol of the instrument to be traded.
				You can use ally.utils.option_format(...) to generate the OCC-standard option symbol.


			price:
				Specify the pricing options for execution.


			qty:
				Specify the number of shares (or contracts, for options) to be purchased.
				Accepts integers, not fractions.


			time
				Specify the time-in-force of the order.


		"""
		self.otype		= type_
		self.account	= None
		self.orderid	= None
		self._status	= None

		self.instrument	= None
		self.pricing	= None
		self.buysell	= None
		self.time		= None
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
		"""Turns buysell type into string.
		"""
		x = {}


		if self.buysell is not None:
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
		"""Compiles the object into FIXML string.

		Does not affect internal state of object
		"""

		d = {}

		# Store account information for this call
		if self.account is not None:
			d['Acct'] = self.account

		# Store order ID for this call
		if self.orderid is not None:
			d['OrigID'] = self.orderid

		# Get instrument data
		if self.instrument is not None:
			d.update(self.instrument.fixml)

		# Get fixml fields from our pricing object
		if self.pricing is not None:
			d.update(self.pricing.fixml)
			d.update(self.pricing.attributes)

		# Perform logic to transform our buy-sell into fixml fields
		d.update(self.convert_buysell)

		# Include Time fields
		if self.time is not None:
			# For cancel requests, tminforce = 0
			if self.otype.value == OType.Cancel.value:
				d['TmInForce'] = '0'
			else:
				d['TmInForce'] = self.time.value

		# Include order quantity
		if self.quantity != 0:
			d['OrdQty'] = { 'Qty': self.quantity }



		# Properly format our order
		order = {
			'xmlns': "http://www.fixprotocol.org/FIXML-5-0-SP2",
			Order._otype_dict_reverse[self.otype.value]: d
		}

		# Rework our tree
		return transposeTree (
			order,			# The tree structure to turn into FIXML
			name='FIXML',	# Name of root tag
			stringify=True	# Please give us a string
		)




	@property
	def status ( self ):
		"""Execution status of this order.

		None implies that this order hasn't been submitted for execution yet.

		"""
		return self._status






	def set_buysell ( self, buysell ):
		"""Specify the side of this order.

		Can be viewed at obj.buysell

		Args:

			buysell:
				one of ('buy','sell','sellshort','buycover'),
				or the corresponding enum types.

		"""

		if isinstance(buysell, str):
			buysell	= Order._side_dict[buysell.lower()]

		self.buysell	= buysell





	def set_orderid ( self, orderid ):
		"""Specifies the order's ID.

		Can be viewed at obj.orderid

		"""
		self.orderid = orderid





	def set_account ( self, account ):
		"""Specifies the account used to execute an order.

		Users shouldn't really need to use this under normal circumstances, this
		is handled by the ally object.

		Can be viewed at obj.account

		"""
		self.account = int(str(account)[:8])






	def set_symbol ( self, symbol: str ):
		"""Sets the order's instrument.

		Can be viewed at obj.instrument

		"""
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
		"""Sets the order's time-in-force.

		Can be viewed at obj.time

		Args:

			time:
				must be one of ('day','gtc','onclose'), or the corresponding enums instances.

		"""

		# Handle strings
		if isinstance(time, str):
			time = Order._time_dict[time.lower()]
		self.time = time





	def set_quantity ( self, qty ):
		"""Sets the order quantity.

		Can be viewed at obj.quantity

		"""

		self.quantity		= int(qty)




	def set_pricing ( self, priceobj ):
		"""Sets the pricing information of an order.

		Can be viewed at obj.pricing

		Args:

			priceobj:
				Must be one of
				ally.Order.Market(),
				ally.Order.Limit(x),
				ally.Order.Stop(x),
				ally.Order.StopLimit(x,y),
				ally.Order.TrailingStop(x,y)

		"""

		self.pricing = priceobj





	def imply_fixml_instrument( self, instrmt ):

		sectyp = instrmt['SecTyp']
		sym = instrmt.pop('Sym')

		if sectyp == 'OPT':
			# Option
			exp_date	= instrmt.pop('MatDt')[:10]
			strike		= instrmt.pop('StrkPx')
			direction	= 'put' if instrmt.pop('CFI') == 'OP' else 'call'
			sym = option_format(
				symbol		= sym,
				exp_date	= exp_date,
				strike		= strike,
				direction	= direction
			)

		self.set_symbol ( sym )






	def __str__(self):
		return '({0}) {1} {2} units of "{3}" {4}, {5}'.format(
			self.otype,
			self.buysell,
			self.quantity,
			self.instrument,
			self.time,
			self.pricing
		)






	def _from_str ( self, fixml ):
		"""Constructer 1)
		Read FIXML string into this object
		"""
		xml = parseTree(fixml)['FIXML']
		xml['Order'] = xml.pop('ExecRpt')

		o = xml['Order']

		o.pop('ID')
		self.set_orderid ( o.pop('OrdID') )

		self.set_account ( o.pop('Acct') )

		self.set_quantity ( o.get('OrdQty').pop('Qty') )


		# Set self.buysell
		side = o.pop('Side',None)
		actp = o.pop('AcctTyp',None)

		if side == '1':
			if actp is None:
				self.set_buysell('buy')
			else:
				self.set_buysell('buycover')
		elif side == '2':
			self.set_buysell('sell')
		elif side == '5':
			self.set_buysell('sellshort')


		# Time In Force (Day, GTC, OnClose)
		tminforce = o.pop('TmInForce')
		if tminforce == '0':
			self.set_time('day')
		elif tminforce == '1':
			self.set_time('gtc')
		elif tminforce == '7':
			self.set_time('onclose')


		# Parse the pricing type of order
		typ = o.pop('Typ')
		px  = o.pop('Px',None)
		stoppx = o.pop('StopPx',None)
		p = None
		# Market
		if typ == '1':
		 	p = Market()
		# Limit
		elif typ == '2':
			p = Limit(px)
		# Simple Stop
		elif typ == '3':
			p = Stop(stoppx)
		# Stop limit
		elif typ == '4':
			p = StopLimit ( limpx=px, stoppx=stoppx )

		# Trailing Stop
		elif typ == 'P':
			tag		= o.pop('PegInstr')
			use_pct = ( tag.pop('OfstTyp') == 1 ) # Cast to boolean
			offset	= tag.pop('OfstVal')
			p		= TrailingStop ( use_pct=use_pct, offset=offset )

		self.set_pricing ( p )




		instrmt = o.pop('Instrmt')
		self.imply_fixml_instrument(instrmt)

		self._status = o






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



