from ..Api		import AccountEndpoint, RequestType
from ..utils	import option_format
from .template	import template
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

		

	
	








balances = template(Balances)
