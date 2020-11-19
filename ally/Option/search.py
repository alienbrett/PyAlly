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




class OptionSearchQuery:

	_queryable_fields = [
		'strikeprice',
		'xdate',
		'xmonth',
		'xyear',
		'put_call',
		'unique'
	]
	_query_operators = [
		'lt',
		'gt',
		'gte',
		'lte',
		'eq'
	]

	_condition:str = ''
	_operator:str = ''
	_value = None

	def __init__(self, **kwargs ):
		if 'condition' not in kwargs.keys():
			raise KeyError('Please specify a condition as a string')
		if 'operator' not in kwargs.keys():
			raise KeyError('Please specify an operator as a string')
		if 'value' not in kwargs.keys():
			raise KeyError('Please specify a value as a string')
		self._condition = kwargs.get('condition',[])
		self._operator = kwargs.get('operator',[])
		self._value = kwargs.get('value',[])


	def is_query_valid(self):
		return (self._condition in self._queryable_fields) and (self._operator in self._query_operators)

	def get_formatted_query_str(self):
		if(self.is_query_valid()):
			if(self._condition and self._operator and self._value):
				return f'{self._condition}-{self._operator}:{self._value}'
		return ''




class Search ( AuthenticatedEndpoint ):
	_type		= RequestType.Info
	_resource	= 'market/options/search.json'
	_method		= 'POST'
	_symbol:str	= ''
	_queries:List[OptionSearchQuery] = []





	def extract ( self, response ):
		"""Extract certain fields from response
		"""
		response = response.json()['response']
		quotes = response['quotes']['quote']

		if type(quotes) != type ([]):
			quotes = [quotes]

		# and return it to the world
		return quotes




	def req_body ( self, **kwargs ):
		"""Return get params together with post body data
		"""

		if 'symbol' not in kwargs.keys():
			raise KeyError('Please specify a symbol as a string')
		symbol	= kwargs.get('symbol',[])
		fields	= kwargs.get('fields',[])
		queries= kwargs.get('queries',[])

		# print(kwargs)

		# Correctly format Fields, also store split up fields
		if type(fields) == type(""):
			# We were passed string
			fmt_fields = fields
			fields = fmt_fields.split(',')
		else:
			# We were passed list
			fmt_fields = ','.join(fields)


		# For aesthetics...
		self._symbol = symbol.upper()

		# Create request paramters according to how we need them
		params = { 'symbol': self._symbol}

		if fields != []:
			params['fids'] = fmt_fields

		if queries != []:
			params['query']=" AND ".join([x.get_formatted_query_str() for x in queries])


		# print(params)
		data = None
		# return params, data
		return data, params



def search (self, symbol: str='', queries:List[OptionSearchQuery] = [], fields: list =[], block: bool = True):
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
		symbol		= symbol,
		fields		= fields,
		queries		= queries,
		block		= block
	).request()




	return result
