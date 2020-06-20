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

import xml.etree.ElementTree as ET
import unittest
from ..classes		import *
from .classes		import *
from ..order		import Order


class TestOrderConstruction(XMLTestCase):


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

