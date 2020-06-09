from ..Api		import AuthenticatedEndpoint, RequestType
from .template	import template






class Timesales ( AuthenticatedEndpoint ):
	_type		= RequestType.Quote
	_resource	= 'market/timesales.json'
	_method		= 'GET'
	_symbols	= []





	def extract ( self, response ):
		"""Extract certain fields from response
		"""
		response = response.json()['response']
		quotes = response['quotes']['quote']

		# and return it to the world
		return quotes




	def req_body ( self, **kwargs ):
		"""Return get params together with post body data
		"""

		if 'symbols' not in kwargs.keys():
			raise KeyError('Please specify a symbol. Use symbols="sym"')
		symbols	= kwargs.get('symbols',"")

		# Interval
		interval = kwargs.get('interval','5min')	

		# Start date
		startdate = kwargs.get('startdate')

		# End date
		enddate = kwargs.get('enddate')

		params = {
			'symbols':symbols,
			'interval':interval,
			'startdate':startdate,
			'enddate':enddate
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
		# df = df.set_index('symbol')
		return df





timesales = template(Timesales)
