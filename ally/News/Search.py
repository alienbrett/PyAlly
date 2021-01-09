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






class SearchNews ( AuthenticatedEndpoint ):
	_type		= RequestType.Info
	_resource	= 'market/news/search.json'



	def req_body ( self, **kwargs ):
		"""Return get params together with post body data
		"""

		if 'symbols' not in kwargs.keys:
			raise KeyError('Please specify symbols, and pass in list of symbols (or string)')


		symbols = kwargs.get('symbols', [])

		# Correctly format Symbols, also store split up symbols
		if type(symbols) == type(""):
			# We were passed string
			fmt_symbols = symbols
		else:
			# We were passed list
			fmt_symbols = ','.join(symbols)

		params = {
			'symbols':fmt_symbols,
			'maxhits':kwargs.get('limit',10),
			'startdate':kwargs.get('startdate',[]),
			'enddate':kwargs.get('enddate',[])
		}

		return params, None




	def extract ( self, response ):
		"""Extract certain fields from response
		"""
		k = response.json().get('response')['articles']['article']

		return k




	@staticmethod
	def DataFrame ( raw ):
		import pandas as pd

		# Create dataframe from our dataset
		df = pd.DataFrame( raw ).replace({'na':None}).set_index('id')

		return df






def searchNews ( self, symbols, limit=None, startdate:str= '', enddate:str='', dataframe = True, block: bool = True ):
	"""Searches for news on a set of symbols.

	Calls the 'market/news/search.json' endpoint to search for
	news articles related to some set of symbols.

	Args:
		symbols: Specify the stock symbols for which to search

		limit: (int) maximum number of hits (10 default)

		startdate: Earliest date to include in search

		enddate: Last date to include in search

		dataframe: whether to return results as dataframe

		block: Specify whether to block thread if request exceeds rate limit


	Returns:
		Dataframe, or list

	Raises:
		RateLimitException: If block=False, rate limit problems will be raised

	Example:
		.. code-block:: python

		   df = a.searchNews('spy')

		   df.columns
		   # Index(['date', 'headline', 'story'], dtype='object')

		   df.index
		   # Index([...], dtype='object', name='id')

	"""
	result = SearchNews (
		auth		= self.auth,
		account_nbr	= self.account_nbr,
		symbols		= symbols,
		limit		= limit,
		startdate 	= startdate,
		enddate		= enddate,
		block		= block
	).request()

	if dataframe:
		try:
			result = SearchNews.DataFrame ( result )
		except:
			raise

	return result
