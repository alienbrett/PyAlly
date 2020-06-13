from requests_oauthlib	import OAuth1
from datetime			import datetime, timedelta
from requests			import Session


class Auth:

	_session		= None
	_auth			= None

	_auth_expire	= None
	_valid_auth_dt	= None

	_params			= {}



	@property
	def sess ( self ):
		if self._session is None:
			self._session = Session()
		return self._session


	@property
	def _get_auth ( self ):
		# Compute the auth, without caching
		return OAuth1(
			self._params.get('ALLY_CONSUMER_KEY'),
			self._params.get('ALLY_CONSUMER_SECRET'),
			self._params.get('ALLY_OAUTH_TOKEN'),
			self._params.get('ALLY_OAUTH_SECRET'),
			signature_type='auth_header'
		)

	
	@property
	def auth ( self ):
			
		# Precalculate current time
		now = datetime.now()
		
		# If outside time valid range, regenerate auth
		if self._auth is None or self._auth_expire < now:
			
			# Set the max auth valid range
			self._auth_expire = now + self._valid_auth_dt

			# Actually generate the auth request
			self._auth = self._get_auth
		
			
		return self._auth





	def __init__ ( self, params, dt = None ):
		"""Given well-formatted parameters
		and (optionally) a time interval,
		create an auth object
		"""
		
		# make sure DT is good
		if dt is None:
			dt = timedelta(seconds=9.7)

		# Keep track of the cache invalidation time
		self._valid_auth_dt = dt

		# Store what we need
		self._params = params

		# Precompute some stuff
		self.sess
		self.auth
