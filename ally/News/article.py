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





class Article ( AuthenticatedEndpoint ):
	_type		= RequestType.Info
	_resource	= 'market/news/{0}.json'
	_method		= 'GET'
	_symbols	= []


	def extract ( self, response ):
		"""Extract certain fields from response
		"""
		import pprint
		pprint.pprint(response.json())
		response = response.json()['response']
		article = response['article']

		if type(article) != type ([]):
			article = [article]

		# Zip symbols up with the response
		# for i,d in enumerate(article):
		# 	d['symbol'] = self._symbols[i]

		# and return it to the world
		return article

	def resolve ( self, **kwargs):
		"""Inject the account number into the call
		"""
		return self.url().format(
			kwargs.get( 'id' )
		)


	def req_body ( self, **kwargs ):
		"""Return get params together with post body data
		"""

		# if 'id' not in kwargs.keys():
		# 	raise KeyError('Please specify article id')

		# Create request paramters according to how we need them

		params = None


		data = None
		# return params, data
		return params,data



def article (self, id: str= '', block: bool = True):
	"""Gets the most current market data on the price of a symbol.

	Args:
		id:

			string id of the article

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

	result = Article(
		auth		= self.auth,
		account_nbr	= self.account_nbr,
		id			= id,
		block		= block
	).request()




	return result
