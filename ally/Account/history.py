from ..Api		import AccountEndpoint, RequestType
from .template	import template
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
		





history = template(History)
