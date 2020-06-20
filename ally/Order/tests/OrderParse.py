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


class TestOrderParse(XMLTestCase):

	def test_parse1(self):


		fixml = '<?xml version="1.0" encoding="utf-8"?>\r\n<FIXML xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2">\r\n  <ExecRpt OrdID="SVI-6111492151" ID="SVI-6111492151" Stat="2" Acct="12345678" AcctTyp="2" Side="2" Typ="2" Px="31.5" TmInForce="1" LastQty="1" LastPx="31.5" LeavesQty="0" TrdDt="2020-06-12T12:12:00.000-04:00" TxnTm="2020-06-12T12:12:00.000-04:00" PosEfct="C">\r\n	<Instrmt Sym="TSLA" CFI="OP" SecTyp="OPT" MMY="202006" MatDt="2020-06-19T00:00:00.000-04:00" StrkPx="935" Mult="100" Desc="TSLA Jun 19 2020 935.00 Put" />\r\n	<Undly Sym="TSLA" />\r\n	<OrdQty Qty="1" />\r\n	<Comm Comm="0.50" />\r\n  </ExecRpt>\r\n</FIXML>'


		o = Order(fixml=fixml)
		
		self.assertEqual ( o.quantity, 1, "quantity of one" )
		self.assertEqual ( o.time, TimeInForce.GTC, "Good Til Cancelled order" )
		self.assertEqual ( o.buysell, Side.Sell, "Sell order" )
		self.assertEqual ( o.account, 12345678, "account number" )
		self.assertEqual ( o.orderid, 'SVI-6111492151', "Order number" )
		self.assertEqual ( o.pricing, Limit(31.50), "Limit order @ $31.50")
	




