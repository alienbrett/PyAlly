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
from ...Ally		import Ally
import warnings


class TestOrderSubmition(XMLTestCase):

	def test_order_submit_cxl ( self ):
		"""Submit an order, then cancel that order.

		Ensure that the orders before and after are equivalent
		"""
		warnings.filterwarnings(
			action="ignore",
			message="unclosed",
			category=ResourceWarning
		)

		a = Ally()

		o = Order (
			buysell = 'buy',
			time = 'gtc',
			symbol = 'gld',
			qty = 10,
			price = Limit(1.0)
		)

		# Log the currently outstanding orders
		js = [ str(j) for j in a.orders() ]

		# Create this new order
		newid = a.submit ( o, preview=False )

		# Cancel this order
		cancelinfo = a.submit ( o, preview=False, type_ = OType.Cancel )

		# Compare the new outstanding orders, sans the other one
		ks = [ str(k) for k in a.orders() if k.orderid != newid ]

		self.assertEqual(js, ks, 'orders excluding the new order should be equal')
