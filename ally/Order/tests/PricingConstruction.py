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
