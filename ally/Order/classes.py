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
from ..utils		import (
	option_format,
	option_symbol,
	option_strike,
	option_maturity,
	option_callput,
)



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
	def __str__(self):
		return self.symbol






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
	
	def __eq__(self, other):
		if isinstance(other, Pricing):
			return \
			(other.type_ == self.type_) and \
			(other._data == self._data) and \
			(other._tag == self._tag)
		return False

		


class Market(Pricing):
	type_	= PriceType.Market
	_data	= { 'Typ': '1' }
	def __str__(self):
		"""Creates market price object.

		"""
		return 'Market'
	


class Limit(Pricing):
	type_	= PriceType.Limit
	_data	= { 'Typ': '2' }

	def __init__ ( self, limpx ):
		"""Creates a limit price object.

		Args:
			
			limpx: the stop price

		"""
		self.px = round(float(limpx),2)
		self._data['Px'] = str(self.px)
	def __str__(self):
		return 'Limit ${:.3f}'.format(self.px)



class Stop(Pricing):
	type_	= PriceType.Stop
	_data	= { 'Typ': '3' }

	def __init__ ( self, stoppx ):
		"""Creates a stop price object.

		Args:
			
			stoppx: the stop price

		"""

		self.stoppx = round(float(stoppx),2)	
		self._data['StopPx'] = str(self.stoppx)
	def __str__(self):
		return 'Stop ${:.3f}'.format(self.stoppx)



class StopLimit(Pricing):
	type_	= PriceType.StopLimit
	_data	= { 'Typ': '4' }

	def __init__ ( self, limpx, stoppx ):
		"""Stop-limit price object.

		Args:

			limpx: limit price, to be used once stop price was reached
			stoppx: stop price, to trigger limit price
		"""
		self.px		= round(float(limpx),2)
		self.stoppx	= round(float(stoppx),2)
		self._data['Px']		= str(self.px)
		self._data['StopPx']	= str(self.stoppx)
	def __str__ ( self ):
		return 'StopLimit (Stop ${0:.3f}, Limit ${1:.3f})'.format(self.px,self.stoppx)



class TrailingStop(Pricing):
	type_	= PriceType.TrailingStop
	_data	= { 'Typ': 'P' }

	def __init__ ( self, use_pct, offset ):
		"""Trailing stop price object.

		Args:
			
			use_pct: if true, treat offset as percent. Otherwise, treat it as a dollar quantity
			offset: the trailing stop offset

		"""
		self.use_pct 	= use_pct
		self.offset		= offset
		self._tag = {'PegInstr': {
			'OfstTyp': 1 if self.use_pct else 0,
			'PegPxTyp': 1,
			'OfstVal': self.offset
		}}

	def __str__ ( self ):
		return 'Trailing Stop {0}{1}{2}'.format(
			'$' if not self.use_pct else '',
			('{:.1f}' if self.use_pct else '{:.3f}').format(self.offset),
			'%' if self.use_pct else '',
		)






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
