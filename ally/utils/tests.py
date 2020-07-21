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

import unittest
from .option	import *



class TestOptionFormat(unittest.TestCase):

	def test_option_format1(self):
		sym = option_format (
			symbol="iBm",
			exp_date="2014-01-18",
			strike=200,
			direction="c"
		)

		self.assertEqual(
			sym,
			"IBM140118C00200000",
			"From ally website, https://www.ally.com/api/invest/documentation/market-ext-quotes-get-post/"
		)

	def test_option_format2(self):
		sym = option_format (
			symbol="f",
			exp_date="2020-07-24",
			strike=1,
			direction="c"
		)

		self.assertEqual(
			sym,
			"F200724C00001000",
			"Snagged from yahoo finance (God bless yahoo finance)"
		)

	def test_option_format3(self):
		sym = option_format (
			symbol="f",
			exp_date="2020-07-24",
			strike=4.5,
			direction="c"
		)

		self.assertEqual(
			sym,
			"F200724C00004500",
			"Snagged from yahoo finance (God bless yahoo finance)"
		)

	def test_option_format3(self):
		sym = option_format (
			symbol="TSLA",
			exp_date="2022-09-16",
			strike="2950.0",
			direction="Put" # Should work, try to break the function
		)

		self.assertEqual(
			sym,
			"TSLA220916P02950000",
			"Snagged from yahoo finance (God bless yahoo finance)"
		)

	############### Test option parameter extraction #####
	def test_option_extraction1(self):
		sym = 'TSLA220916P02950000'
		self.assertEqual(
			option_strike ( sym ),
			2950,
			"Strike price of $2950.00"
		)

	def test_option_extraction2(self):
		sym = 'TSLA220916P02950000'
		self.assertEqual(
			option_symbol ( sym ),
			'TSLA',
			"It is a TSLA option"
		)

	def test_option_extraction3(self):
		sym = "F200724C00004500"
		self.assertEqual(
			option_strike ( sym ),
			4.5,
			"Make sure we can extract non-integer strikes"
		)

	def test_option_extraction4(self):
		sym = "F200724C00004500"
		self.assertEqual(
			option_maturity ( sym ),
			"2020-07-24",
			"Extract the expiration date"
		)
