from requests_oauthlib   import OAuth1
import datetime
import requests
import json
import sys
import os


##################
class Cache:
	"""Wrap calls to get something, for faster results grabbing
	"""
	cache={}
	f=None

	def find_bin(self, x):
		return x

	def eval(self, x, **kwargs):
		z = self.find_bin(x)
		if z not in self.cache.keys():
			self.cache[z] = self.f(z,**kwargs)
		return self.cache[z]




class Auth:
	##############################	
	# Header is valid for 10 seconds,
	#  but this seems safer
	valid_dt	= datetime.timedelta(seconds=9.7)
	params		= None
	header 		= None
	exp   		= None
	##############################	
	def __init__(self, params):
		self.params = {
			k.lower():v
			for k,v in params.items()
			if k.lower() in (
				'client_key',
				'client_secret',
				'resource_owner_key',
				'resource_owner_secret'
			)
		}
		if len(self.params.keys()) < 4:
			raise ValueError
	##############################	
	def use_cached(self,time):
		if self.header == None:
			return False
		else:
			return self.time['last'] < time
	##############################	
	def auth(self):
		# Precalculate current time
		now = datetime.datetime.now()
		# If outside time valid range, regenerate auth
		if self.use_cached(now):
			# Set exp
			self.exp = now + valid_dt
			# Cache
			self.auth = OAuth1(
				self.params['client_key'],
				self.params['client_secret'],
				self.params['resource_owner_key'],
				self.params['resource_owner_secret'],
				signature_type='auth_header'
			)
		return self.auth




class APICALL:

	def __init__( self, account ):

	def clean ( self, *args, **kwargs ):
		"""Ensure all input parameters are well-formatted"""
		pass

	def gen_req ( self, auth, account, *args, **kwargs ):
		"""Use auth and account information to generate request object"""
		pass

	def send_req ( self, *args, **kwargs ):
		"""Just send our request"""
		pass

	def handle_req ( self, *args, **kwargs ):
		"""Handle whatever Ally decides to send us"""
		pass


def validate( validator_dict, k, v )
	"""Give me dict, in the form
	validator_dict = {
		'some_arg': ( type(""), set('possibility_one',...) ),
	}
	And I'll return whether each argument satisfies
	"""
	t = validator_dict[k]
	# Check types
	if type(v) != t[0]:
		raise TypeError(str(k) + " should have type " + str(t[0]))
	# Check values
	if type(v) == type(''):
		v = v.lower()
	if v not in t[1]:
		raise ValueError(str(k) + " = " + str(v) + " not in acceptable values " \
			+ str(list(t[1]))
		)
	


def Account_History( APICALL ):
	url =   common.endpoints['base']	+\
			'accounts/'			   +\
			str(account)			  +\
			'/history.json'

	validator_dict = {
		'type_' : (type(''), set([
			'all',
			'bookkeeping',
			'trade'
		]),
		'range_': (type(''), set([
			'all',
			'today',
			'current_week',
			'current_month',
			'last_month'
		]))
	}
	def clean( type_='all', range_='all' ):
		validate ( Account_History.validator_dict, 'type_', type_ )
		validate ( Account_History.validator_dict, 'range_', range_ )
		
		


		

def account_history(self, account=None, type='all', range="all"):
	if not (utils.check(type) and utils.check(range)):
		return {}
	
	# Imply account
	if account == None:
		account = self.params['account']
		
	# Assemble URL
	url =   self.endpoints['base']	+\
			'accounts/'			   +\
			str(account)			  +\
			'/history.json'
	# Add parameters
	data = {
		'range':range,
		'transactions':type
	}
	
	# Create HTTP Request objects
	session = requests.Session()
	auth	= self.create_auth()
	req	 = requests.Request('GET',url,params=data,auth=auth).prepare()
	
	results			= {'response':session.send(req).json()}
	results['request'] = utils.pretty_print_POST(req)
	
	return results['response']['response']['transactions']['transaction']
