from os			import environ
from json		import load
from .Auth		import Auth
from .exception	import ApiKeyException




__all_params = ( 
	'ALLY_OAUTH_SECRET'	
	'ALLY_OAUTH_TOKEN'
	'ALLY_CONSUMER_SECRET'
	'ALLY_CONSUMER_KEY'
	'ALLY_ACCOUNT_NBR'
)





class Ally:

	# Import all our class methods
	# from . import Account	as account
	from . import Info		as info




	auth = None

	def param_load_environ (self):
		"""Try to use environment params
		Account number is now mandatory
		"""
		params = {}
		for t in __all_params:
			params[t] = environ.get(t,None)
		return params


	def param_load_file (self, fname):
		"""Try to load params from a json file
		Account number is now mandatory
		"""
		with open(params, 'r') as f:
			return load(f)





	def __init__ ( self, params = None ):

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
		for t in __all_params:
			if params.get(t,None) is None:
				raise ApiKeyException ( '{0} parameter not provided'.format(t) )


		# Create the auth that we want
		#  This is the only tidbit that actually
		#   needs these parameters anyways
		self._auth = Auth(params)



