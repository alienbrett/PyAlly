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

from ..Api		import AuthenticatedEndpoint, RequestType
from .template	import template






class Timesales ( AuthenticatedEndpoint ):
	_type		= RequestType.Quote
	_resource	= 'market/timesales.json'
	_method		= 'GET'
	_symbols	= []





	def extract ( self, response ):
		"""Extract certain fields from response
		"""
		response = response.json()['response']
		quotes = response['quotes']['quote']

		# and return it to the world
		return quotes




	def req_body ( self, **kwargs ):
		"""Return get params together with post body data
		"""

		if 'symbols' not in kwargs.keys():
			raise KeyError('Please specify a symbol. Use symbols="sym"')
		symbols	= kwargs.get('symbols',"")

		# Interval
		interval = kwargs.get('interval','5min')	

		# Start date
		startdate = kwargs.get('startdate')

		# End date
		enddate = kwargs.get('enddate')

		params = {
			'symbols':symbols,
			'interval':interval,
			'startdate':startdate,
			'enddate':enddate
		}
		
		data = None
		return params, data





	@staticmethod
	def DataFrame ( raw ):
		import pandas as pd

		# Create dataframe from our dataset
		df = pd.DataFrame( raw ).apply(
			# And also cast relevent fields to numeric values
			pd.to_numeric,
			errors='ignore'
		)
		# df = df.set_index('symbol')
		return df





timesales = template(Timesales)
