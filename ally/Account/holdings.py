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

from ..Api import AccountEndpoint, RequestType
from ..utils import option_format






class Holdings ( AccountEndpoint ):
	_type		= RequestType.Info
	_resource	= 'accounts/{0}/holdings.json'


	@staticmethod
	def _flatten_holding ( holding ):


		# Process options
		if holding['instrument']['sectyp'] == 'OPT':

			op = holding['instrument']

			holding['sym'] = option_format (
				symbol		= op['sym'],
				exp_date	= op['matdt'][:10], # '2020-06-19T00:00:00-04:00'
				strike		= op['strkpx'],
				direction	= 'P' if op['putcall'] == '0' else 'C'
			)

		else:
			holding['sym'] = holding['instrument']['sym']



		holding['lastprice'] = holding['quote']['lastprice']

		holding.pop('instrument')
		holding.pop('quote')

		return holding





	def extract ( self, response ):
		"""Extract certain fields from response
		"""
		response = response.json()['response']
		holdings = response['accountholdings']['holding']

		return list( map( Holdings._flatten_holding, holdings ) )


	@staticmethod
	def DataFrame ( raw ):
		import pandas as pd
		return pd.DataFrame( raw )






def holdings ( self, dataframe: bool = True, block: bool = True ):
	"""Gets all current account holdings.

	Calls the 'accounts/./history.json' endpoint to get list of all current account
	holdings, including stocks and options. This also includes current market value,
	cost of acquisition, etc.

	Args:
		dataframe: Specify an output format
		block: Specify whether to block thread if request exceeds rate limit

	Returns:
		A pandas dataframe by default,
			otherwise a flat list of dictionaries.
	"""
	result = Holdings(
		auth		= self.auth,
		account_nbr	= self.account_nbr,
		block		= block
	).request()


	if dataframe:
		try:
			result = Holdings.DataFrame ( result )
		except:
			pass

	return result
