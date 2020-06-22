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
		df = pd.DataFrame( raw ).replace({'na':None}).apply(
			# And also cast relevent fields to numeric values
			pd.to_numeric,
			errors='ignore'
		).set_index('symbol')

		return df





def quote ( self, symbols: list =[], fields: list =[], dataframe=True, block: bool = True ):
	"""Gets the most current market data on the price of a symbol.

	Args:
		symbols:

			string or list of strings, each string a symbol to be queried.
			Notice symbols=['spy'], symbols='spy both work

		fields:

			string or list of strings, each string a field to be grabbed.
			By default, get all fields

		dataframe:

			flag, specifies whether to return data in pandas dataframe
			or flat list of dictionaries.

		block:
			Specify whether to block thread if request exceeds rate limit

	Returns:
		Depends on dataframe flag. Will return pandas dataframe, or possibly
		list of dictionaries, each one a single quote.

	Raises:
		RateLimitException: If block=False, rate limit problems will be raised

	Examples:

.. code-block:: python

	# Get the quotes in dataframe format
	#  Each row will only have elements bid, ask, and last
	quotes = a.quote(
		symbols=['spy','gLD','F','Ibm'], # not case sensitive
		fields=['bid','ask,'last'],
	)
	# Access a specific symbol by the dataframe
	print(quotes.loc['SPY'])



.. code-block:: python

	# Get the quotes in dataframe format
	quotes = a.quote(
		'AAPL',
		dataframe=False
	)
	# Access a specific symbol in the dict
	print(quotes['AAPL'])

	"""

	result = Quote(
		auth		= self.auth,
		account_nbr	= self.account_nbr,
		symbols		= symbols,
		fields		= fields,
		block		= block
	).request()


	if dataframe:
		try:
			result = Quote.DataFrame ( result )
		except:
			raise


	return result
