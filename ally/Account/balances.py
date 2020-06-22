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

from ..Api		import AccountEndpoint, RequestType
from .utils		import _dot_flatten



class Balances ( AccountEndpoint ):
	_type		= RequestType.Info
	_resource	= 'accounts/{0}/balances.json'




	def extract ( self, response ):
		"""Extract certain fields from response
		"""
		response = response.json()['response']
		balances = response['accountbalance']

		d = {
			k: v
			for k,v in _dot_flatten( balances ).items()
		}
		return d


	@staticmethod
	def DataFrame ( raw ):
		import pandas as pd

		# Wrap these in lists so that they can be read by pandas
		raw = { k: [v] for k,v in raw.items() }

		return pd.DataFrame.from_dict ( raw )







def balances ( self, dataframe: bool = True, block: bool = True ):
	"""Gets current cash and various account metrics.

	Calls the 'accounts/./balances.json' endpoint to get the current list of balances.
	This includes margin amounts, cash, etc.

	Args:

		dataframe: Specify an output format
		block: Specify whether to block thread if request exceeds rate limit


	Returns:

		A pandas dataframe with 1 row by default,
			otherwise a flat dictionary.

	Raises:

		RateLimitException: If block=False, rate limit problems will be raised
	"""
	result = Balances(
		auth = self.auth,
		account_nbr = self.account_nbr,
		block = block
	).request()


	if dataframe:
		try:
			result = Balances.DataFrame ( result )
		except:
			pass

	return result

