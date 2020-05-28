from ..Api import AccountEndpoint, RequestType
from ..utils import option_format
from .template import template






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
		





holdings = template(Holdings)
