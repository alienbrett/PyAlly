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





class TopLists ( AuthenticatedEndpoint ):
	_type		= RequestType.Quote
	_resource	= 'market/toplists/{}.json'
	_method		= 'GET'


	def resolve ( self, **kwargs):
		"""Inject the account number into the call
		"""
		return self.url().format(kwargs.get('whichList'))



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

		params = { 'exchange':kwargs.get('exchange') }

		# return params, data
		return params, None





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





def toplists ( self, whichList : str, exchange : str ='Q', dataframe : bool = True, block: bool = True ):
	"""Gets the most recent toplists for a given exchange.

	Args:

		whichList:
			Must be one of {'toplosers', 'toppctlosers', 'topvolume', 'topactive', 'topgainers', 'toppctgainers'}

		exchange:
			string, one of
			'A' (American Stock Exchange)
			'N' (NYSE)
			'Q' (NASDAQ)
			'U' (NASDAQ Bulletin Board)
			'V' (NASDAQ OTC Other)

		dataframe:
			flag, specifies whether to return data in pandas dataframe
			or flat list of dictionaries.

		block:
			Specify whether to block thread if request exceeds rate limit

	Returns:
		Depends on dataframe flag. Will return pandas dataframe, or possibly
		list of dictionaries, each one a single quote.

	Raises:

		RateLimitException:
			If block=False, rate limit problems will be raised

	Example:

.. code-block:: python

	a.toplists('tpopctgainers')

			     chg  chg_sign       last                            name    pchg       pcls  rank        vl
	symbol
	BFRA     21.3700     u        41.6900                  BIOFRONTERA AG  105.17    20.3200     1    279216
	CBMG      5.0100     u        19.2800  CELLULAR BIOMEDICINE GROUP INC   35.11    14.2700     2    793186


	"""

	result = TopLists(
		auth		= self.auth,
		account_nbr	= self.account_nbr,
		exchange	= exchange,
		whichList	= whichList,
		block		= block
	).request()

	if dataframe:
		try:
			result = TopLists.DataFrame ( result )
		except:
			raise


	return result
