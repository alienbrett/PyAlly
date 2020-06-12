# from requests.exceptions import ConnectionError, HTTPError, Timeout
from enum					import Enum
from retry					import retry
from requests				import Request, Session
from requests.exceptions	import HTTPError,Timeout
from .utils					import (
	pretty_print_POST,
	JSONStreamParser
)
import datetime
import logging





"""
- Auth-less request,
	* (market clock, etc)
	* should be a class method

- Auth-ed request
	* get information
	* submit order
	* etc
	* should be object method


- Rate limits
	* 40 per minute, order submission (including submit, modify, cancel)
	* 60 per minute, market quotes
	* 180 per minute, user info like balance, summary, etc

"""



# Global timeout variable
_timeout = 1.0



class RequestType(Enum):
	Order	= 1
	Quote	= 2
	Info	= 3




class Endpoint:

	# Host
	_host = 'https://api.tradeking.com/v1/'
	
	# One of RequestType
	_type = None

	# Extension
	_resource = ''

	# GET, POST, etc.
	_method	= 'GET'

	# results
	_results = None

	req = None
	




	@classmethod
	def url ( cls ):
		return cls._host + cls._resource
	




	@classmethod
	def resolve ( cls, **kwargs):
		"""Can insert account information into the url
		This is just a placeholder
		"""
		return cls.url()






	def extract ( self, response ):
		"""Extract certain fields from response
		"""
		return response.json().get('response')






	def req_body ( self, **kwargs ):
		"""Return get params together with post body data
		"""
		return None, None







	def _fetch_raw ( self, stream=False ):
		return self.s.send(
			self.req,
			stream=stream
		)



	def request ( self=None ):
		"""Execute an entire loop, and aggregate results
		"""
		x = self._fetch_raw()

		# print(x.status)
		x.raise_for_status()

		return self.extract ( x )




	

	def __init__ ( self, auth = None, **kwargs ):
		"""Create and send request
		Return the processed result
		"""

		# Get post and get data
		send_params, send_data = self.req_body (**kwargs)


		# Get the session
		if auth is not None:
			self.s = auth.sess
		else:
			self.s = Session()


		req_auth = None if auth is None else auth.auth
		
		# Create a prepped request
		self.req = self.s.prepare_request(
			Request(
				self._method,
				self.resolve( **kwargs ),
				auth	= req_auth,
				params	= send_params,
				data	= send_data
			)
		)
		print(pretty_print_POST(self.req))









class AuthenticatedEndpoint ( Endpoint ):
	"""Simple class, just require auth. Non-auth is non-optional
	"""
	def __init__ ( self, auth, **kwargs ):
		"""Create and send request
		Return the processed result
		"""
		super().__init__(auth,**kwargs)







class AccountEndpoint ( AuthenticatedEndpoint ):
	"""Also automatically resolve url to include account number
	"""
	def resolve ( self, **kwargs):
		"""Inject the account number into the call
		"""
		return self.url().format(kwargs.get('account_nbr'))






class StreamEndpoint ( AuthenticatedEndpoint ):
	"""Stream an endpoint
	"""
	_host		= 'https://stream.tradeking.com/v1/'
	def request ( self=None ):
		"""Execute an entire loop, and aggregate results
		"""

		x = self._fetch_raw(stream=True)

		x.raise_for_status()

		p = JSONStreamParser()

		for chunk in x.iter_content( chunk_size=1 ):
			it = p.stream(chunk.decode('utf-8'))
			while True:
				try:
					row = next(it)
				except StopIteration:
					pass
				else:
					quote = row.get('quote')
					if quote is not None:
						yield quote
				finally:
					del it
					break







def setTimeout ( t ):
	"""Used to set the global request response timeout variable
	"""
	if t is not None:
		_timeout = float(t)
