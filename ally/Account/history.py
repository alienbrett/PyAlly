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






class History ( AccountEndpoint ):
	_type		= RequestType.Info
	_resource	= 'accounts/{0}/history.json'


	@staticmethod
	def _process ( entry ):
		"""Process a single transaction, into
		the format that's most useful
		"""

		t = entry['transaction']



		# Get the consistent trading symbol
		x = { }
		x['sectyp'] = t['security']['sectyp']

		if x['sectyp'] == 'OPT':
			# Process this option
			x['symbol'] = t['security']['id']


		elif x['sectyp'] == 'CS':
			# Process stock
			x['symbol'] = t['security']['sym']


		else:
			# Something else, cash transfer or dividend likely
			x['symbol'] = None


		x['cusip'] = t['security']['cusip']


		# Register the human-readable transaction type
		#  buy, sell, short or cover
		side	= t['side']
		accttyp	= t['accounttype']

		if entry['activity'] == 'Trade':
			if side == '1':
				if accttyp == '5':
					x['transactiontype']	= 'buy'
				else:
					x['transactiontype']	= 'buy to cover'

			elif side == '2':
				x['transactiontype']		= 'sell'

			elif side == '5':
				x['transactiontype']		 = 'short sell'



		# Modify the trade date to something actually useful
		entry['date'] = entry['date'][:10]


		# Pull some of these values out of transaction
		for i in (
			'source','settlementdate',
			'transactionid','security',
			'tradedate'
		):
			entry['transaction'].pop( i )


		# Now plop them down into the root
		entry = { ** entry, ** entry['transaction'] }


		# Now delete transaction
		entry.pop('transaction')


		# Now combine our values with entry's values
		return { **entry, **x }










	def extract ( self, response ):
		"""Extract certain fields from response
		"""
		response = response.json()['response']
		history = response['transactions']['transaction']

		# print(response.status)
		
		return [ History._process ( x ) for x in history ]
		# return history




	def req_body ( self, **kwargs ):
		"""Return get params together with post body data
		"""
		params = {
			'range': kwargs.get('range_'),
			'transactions':kwargs.get('type_')
		}
		data = None
		return params, data







	@staticmethod
	def DataFrame ( raw ):
		import pandas as pd

		# Create dataframe from our dataset
		df = pd.DataFrame( raw ).apply(
			# And also cast relevent fields to numeric values
			pd.to_numeric,
			errors='ignore'
		)
		return df






def history ( self, dataframe: bool = True, block: bool = True ):
	"""Gets the transaction history for the account.

	Calls the 'accounts/./history.json' endpoint to get list of all trade
	and cash  movement history for an account. This includes dividends, cash
	deposits and withdrawals, and all trades, including pricing information about
	each trade.

	Args:
		dataframe: Specify an output format
		block: Specify whether to block thread if request exceeds rate limit

	Returns:
		Pandas dataframe by default, otherwise a flat list of dictionaries.

	Raises:
		RateLimitException: If block=False, rate limit problems will be raised

	"""
	result = History(
		auth		= self.auth,
		account_nbr	= self.account_nbr,
		block		= block
	).request()


	if dataframe:
		try:
			result = History.DataFrame ( result )
		except:
			pass

	return result
