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






class LookupNews ( AuthenticatedEndpoint ):
	_type		= RequestType.Info
	_resource	= 'market/news/{}.json'



	def req_body ( self, **kwargs ):
		"""Return get params together with post body data
		"""
		params = {
			'symbols':kwargs.get('symbols'),
			'maxhits':kwargs.get('limit',10)
		}
		return params, None




	def extract ( self, response ):
		"""Extract certain fields from response
		"""
		k = response.json().get('response')['article']

		return k



	def resolve ( self, **kwargs):
		"""Inject the account number into the call
		"""
		return self.url().format(kwargs.get('articleId'))



	@staticmethod
	def DataFrame ( raw ):
		import pandas as pd

		# Create dataframe from our dataset
		df = pd.DataFrame( [raw] ).replace({'na':None}).set_index('id')

		return df







def lookupNews ( self, articleId, dataframe = True, block: bool = True ):
	"""Looks up the news text for a given article.

	Calls the 'market/news/{}.json' endpoint to the news story with a given id.

	Args:
		articleId: Specify the articleID requested

		dataframe: whether to return results as dataframe

		block: Specify whether to block thread if request exceeds rate limit


	Returns:
		Dataframe, or dict

	Raises:
		RateLimitException: If block=False, rate limit problems will be raised

	Example:
		.. code-block:: python

		   a.lookupNews( '2938-A2231367-5OLLNQGI9S29FR694AB4IM0OQ' )

	"""
	result = LookupNews (
		auth		= self.auth,
		account_nbr	= self.account_nbr,
		block		= block,
		articleId	= articleId
	).request()

	if dataframe:
		try:
			result = LookupNews.DataFrame ( result )
		except:
			raise

	return result
