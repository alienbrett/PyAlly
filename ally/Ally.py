from os			import environ
from json		import load
from .Auth		import Auth
from .exception	import ApiKeyException
from .Api		import setTimeout




_all_params = ( 
	'ALLY_OAUTH_SECRET',
	'ALLY_OAUTH_TOKEN',
	'ALLY_CONSUMER_SECRET',
	'ALLY_CONSUMER_KEY',
	'ALLY_ACCOUNT_NBR'
)




class Ally:

	# Import all our class methods
	from .Account	import (
		holdings,
		balances,
		history
	)
	from .Info		import clock, status




	auth = None
	account_nbr = None

	def param_load_environ (self):
		"""Try to use environment params
		Account number is now mandatory
		"""
		params = {}
		for t in _all_params:
			params[t] = environ.get(t,None)
		return params


	def param_load_file (self, fname):
		"""Try to load params from a json file
		Account number is now mandatory
		"""
		with open(params, 'r') as f:
			return load(f)





	def __init__ ( self, params = None, timeout=1.0 ):

		"""Provide API keys in the form of:
		- A dictionary: { ALLY_OAUTH_SECRET: ...}
		- A string: (filename to json file containing api keys)
		- None (default): Grab the api keys from environment variables

		For any of the mediums above, be sure to provide all of the keys:
			params = { 
				'ALLY_OAUTH_SECRET'		: ...,
				'ALLY_OAUTH_TOKEN'		: ...,
				'ALLY_CONSUMER_SECRET'	: ...,
				'ALLY_CONSUMER_KEY'		: ...,
				'ALLY_ACCOUNT_NBR'		: ...
			}

		Also optionally specify timeout period for API requests
			Requests will be automatically retried if connection doesn't succeed

		"""



		# We were passed an actual dictionary
		if type(params) == type({}):
			pass



		# We were passed a JSON file
		elif type(params) == type(""):
			params = self.param_load_file(params)


		# Use environment variables
		else:
			params = self.param_load_environ()
			

		# Check that we have all the parameters we need
		for t in _all_params:
			if params.get(t,None) is None:
				raise ApiKeyException ( '{0} parameter not provided'.format(t) )


		# Create the auth that we want
		#  This is the only tidbit that actually
		#   needs these parameters anyways
		self.auth = Auth(params)

		# But keep account number
		self.account_nbr = params['ALLY_ACCOUNT_NBR']

		




