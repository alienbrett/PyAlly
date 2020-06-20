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
"""Controls the OAuth1 object used for account authentication

"""

from requests_oauthlib	import OAuth1
from datetime			import datetime, timedelta
from requests			import Session


class Auth:
	"""Auth object, caching and creating new sessions as needed
	"""

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
		"""Creates an auth object.

		Args:

			params: set of keys given by Ally API
			dt: time interval for caching. 10 seconds max

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
