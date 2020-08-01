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
from typing import List





class Search ( AuthenticatedEndpoint ):
	_type		= RequestType.Info
	_resource	= 'market/news/search.json'
	_method		= 'GET'
	_symbols	= []





	def extract ( self, response ):
		"""Extract certain fields from response
		"""
		import pprint
		pprint.pprint(response.json())
		response = response.json()['response']
		articles = response['articles']['article']

		if type(articles) != type ([]):
			articles = [articles]

		# Zip symbols up with the response
		# for i,d in enumerate(articles):
		# 	d[''] = self._symbols[i]

		# and return it to the world
		return articles




	def req_body ( self, **kwargs ):
		"""Return get params together with post body data
		"""

		if 'symbols' not in kwargs.keys():
			raise KeyError('Please specify symbols, and pass in list of symbols (or string)')
		symbols = kwargs.get('symbols',[])
		maxhits = kwargs.get('maxhits',10)
		if 'startdate' not in kwargs.keys():
			raise KeyError('Please specify startdate')
		startdate = kwargs.get('startdate',[])
		if 'enddate' not in kwargs.keys():
			raise KeyError('Please specify enddate')
		enddate = kwargs.get('enddate',[])

		print(kwargs)

		# Correctly format Symbols, also store split up symbols
		if type(symbols) == type(""):
			# We were passed string
			fmt_symbols = symbols
			symbols = symbols.split(',')
		else:
			# We were passed list
			fmt_symbols = ','.join(symbols)

		# Store symbols, so we can zip them back up with
		#  the response object
		symbols = [ s.upper() for s in symbols ]
		self._symbols = symbols


		# For aesthetics...
		fmt_symbols = fmt_symbols.upper()

		# Create request paramters according to how we need them
		params = {
			'symbols':fmt_symbols,
			'maxhits':maxhits,
			'startdate': startdate,
			'enddate': enddate
		}


		print(params)
		data = None
		# return params, data
		return params,data



def newssearch (self, symbols: list=[], maxhits:int = 10, startdate:str= '', enddate:str='',block: bool = True):
	"""Gets the most current market data on the price of a symbol.

	Args:
		symbols:

			string or list of strings, each string a symbol to be queried.
			Notice symbols=['spy'], symbols='spy both work

		fields:

			string or list of strings, each string a field to be grabbed.
			By default, get all fields


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

	result = Search(
		auth		= self.auth,
		account_nbr	= self.account_nbr,
		symbols		= symbols,
		maxhits		= maxhits,
		startdate	= startdate,
		enddate		= enddate,
		block		= block
	).request()




	return result
