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
