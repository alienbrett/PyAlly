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






class Quote ( AuthenticatedEndpoint ):
	_type		= RequestType.Quote
	_resource	= 'market/ext/quotes.json'
	_method		= 'POST'
	_symbols	= []





	def extract ( self, response ):
		"""Extract certain fields from response
		"""
		response = response.json()['response']
		quotes = response['quotes']['quote']

		if type(quotes) != type ([]):
			quotes = [quotes]
		
		# Zip symbols up with the response
		for i,d in enumerate(quotes):
			d['symbol'] = self._symbols[i]
		
		# and return it to the world
		return quotes




	def req_body ( self, **kwargs ):
		"""Return get params together with post body data
		"""

		if 'symbols' not in kwargs.keys():
			raise KeyError('Please specify symbols, and pass in list of symbols (or string)')
		symbols	= kwargs.get('symbols',[])
		fields	= kwargs.get('fields',[])


		# Correctly format Symbols, also store split up symbols
		if type(symbols) == type(""):
			# We were passed string
			fmt_symbols = symbols
			symbols = symbols.split(',')
		else:
			# We were passed list
			fmt_symbols = ','.join(symbols)
			

			
		# Correctly format Fields, also store split up fields
		if type(fields) == type(""):
			# We were passed string
			fmt_fields = fields
			fields = fmt_fields.split(',')
		else:
			# We were passed list
			fmt_fields = ','.join(fields)
			
		
		# Store symbols, so we can zip them back up with
		#  the response object
		symbols = [ s.upper() for s in symbols ]
		self._symbols = symbols


		# For aesthetics...
		fmt_symbols = fmt_symbols.upper()

		# Create request paramters according to how we need them
		params = { 'symbols':fmt_symbols }
		
		if fields != []:
			params['fids'] = fmt_fields

			
		
		data = None
		# return params, data
		return data, params





	@staticmethod
	def DataFrame ( raw ):
		import pandas as pd

		# Create dataframe from our dataset
		df = pd.DataFrame( raw ).apply(
			# And also cast relevent fields to numeric values
			pd.to_numeric,
			errors='ignore'
		)
		df = df.set_index('symbol')
		df = df.replace ({'na':None})

		return df





quote = template(Quote)
