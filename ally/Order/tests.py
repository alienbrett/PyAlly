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
from .classes	import *
from .order		import Order

__all__ = ['TestOrderManual','TestInstrumentConstruction','TestPricingConstruction', 'TestOrderConstruction', 'TestOrderParse']


class XMLTestCase(unittest.TestCase):
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




class TestOrderParse(XMLTestCase):

	def test_parse1(self):


		fixml = '<?xml version="1.0" encoding="utf-8"?>\r\n<FIXML xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2">\r\n  <ExecRpt OrdID="SVI-6111492151" ID="SVI-6111492151" Stat="2" Acct="12345678" AcctTyp="2" Side="2" Typ="2" Px="31.5" TmInForce="1" LastQty="1" LastPx="31.5" LeavesQty="0" TrdDt="2020-06-12T12:12:00.000-04:00" TxnTm="2020-06-12T12:12:00.000-04:00" PosEfct="C">\r\n    <Instrmt Sym="TSLA" CFI="OP" SecTyp="OPT" MMY="202006" MatDt="2020-06-19T00:00:00.000-04:00" StrkPx="935" Mult="100" Desc="TSLA Jun 19 2020 935.00 Put" />\r\n    <Undly Sym="TSLA" />\r\n    <OrdQty Qty="1" />\r\n    <Comm Comm="0.50" />\r\n  </ExecRpt>\r\n</FIXML>'


		o = Order(fixml=fixml)
		
		self.assertEqual ( o.quantity, 1, "quantity of one" )
		self.assertEqual ( o.time, TimeInForce.GTC, "Good Til Cancelled order" )
		self.assertEqual ( o.buysell, Side.Sell, "Sell order" )
		self.assertEqual ( o.account, 12345678, "account number" )
		self.assertEqual ( o.orderid, 'SVI-6111492151', "Order number" )
		self.assertEqual ( o.pricing, Limit(31.50), "Limit order @ $31.50")
