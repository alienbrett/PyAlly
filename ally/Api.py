# from requests.exceptions import ConnectionError, HTTPError, Timeout
from enum		import Enum
from requests	import Request, Session
import datetime
import logging
import json


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





	def fetch ( self ):
		"""Fetch the network resource we manage
		"""
		return self.extract ( self.s.send( self.req ) )




	

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
		
		# response = self.fetch()

		# Create a prepped request
		self.req = self.s.prepare_request(
			Request(
				self._method,
				self.resolve( ),
				params	= send_params,
				data	= send_data
			)
		)



	@classmethod
	def request ( cls ):
		"""Execute an entire loop, and aggregate results
		"""
		return cls().fetch()




class AuthenticatedEndpoint ( Endpoint ):
	pass


