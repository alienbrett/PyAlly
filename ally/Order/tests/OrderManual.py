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
from ..order		import Order





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
