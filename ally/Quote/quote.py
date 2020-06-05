from ..Api		import AuthenticatedEndpoint, RequestType
from .template	import template






class Quote ( AuthenticatedEndpoint ):
	_type		= RequestType.Quote
	_resource	= 'market/ext/quotes.json'
	_method		= 'POST'
	_symbols	= []





	def extract ( self, response ):
		"""Extract certain fields from response
		"""
		response = response.json()['response']
		quotes = response['quotes']['quote']

		if type(quotes) != type ([]):
			quotes = [quotes]
		
		# Zip symbols up with the response
		for i,d in enumerate(quotes):
			d['symbol'] = self._symbols[i]
		
		# and return it to the world
		return quotes




	def req_body ( self, **kwargs ):
		"""Return get params together with post body data
		"""

		symbols	= kwargs.get('symbols',[])
		fields	= kwargs.get('fields',[])


		# Correctly format Symbols, also store split up symbols
		if type(symbols) == type(""):
			# We were passed string
			fmt_symbols = symbols
			symbols = symbols.split(',')
		else:
			# We were passed list
			fmt_symbols = ','.join(symbols)
			

			
		# Correctly format Fields, also store split up fields
		if type(fields) == type(""):
			# We were passed string
			fmt_fields = fields
			fields = fmt_fields.split(',')
		else:
			# We were passed list
			fmt_fields = ','.join(fields)
			
		
		# Store symbols, so we can zip them back up with
		#  the response object
		symbols = [ s.upper() for s in symbols ]
		self._symbols = symbols


		# For aesthetics...
		fmt_symbols = fmt_symbols.upper()

		# Create request paramters according to how we need them
		params = { 'symbols':fmt_symbols }
		
		if fields != []:
			params['fids'] = fmt_fields

			
		
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
		df.set_index('symbol')
		return df





quote = template(Quote)
