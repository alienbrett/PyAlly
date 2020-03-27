#################################################
"""			ALLY				"""
#################################################

from . import 	order as order_utils
from . import 	option_info
from . import	instrument
from . import 	api_calls
from . import	utils
from . import 	fixml

all = ['fixml.FIXML', 'order', 'instrument', 'Ally', 'utils']

from datetime import timedelta
from json import loads
from os import environ


############################################################################
class Ally:
	endpoints={
		'base'					:'https://api.tradeking.com/v1/',
		'request_token'			:'https://developers.tradeking.com/oauth/request_token',
		'user_auth'				:'https://developers.tradeking.com/oauth/authorize',
		'resource_owner_key'	:'https://developers.tradeking.com/oauth/resource_owner_key'
	}
	json_params = {
		'indent':4
	}
	
	# Cache Oauth requests (faster)
	last_auth_time = None
	auth		   = None
	valid_auth_dt  = timedelta(seconds=9.7)

	############################################################################
	# Option calls are stored in option_info.py
	get_strike_prices	=	option_info.get_strike_prices
	get_exp_dates		=	option_info.get_exp_dates
	search_options		=	option_info.search_options
	options_chain		=	option_info.options_chain
	############################################################################
	# Most API calls are stored in api_calls.py
	create_auth			=	api_calls.create_auth
	get_accounts		=	api_calls.get_accounts
	get_holdings		=	api_calls.get_accounts
	holdings_chart		=	api_calls.holdings_chart
	get_quote			=	api_calls.get_quote
	submit_order		=	api_calls.submit_order
	account_history		=	api_calls.account_history
	order_history		=	api_calls.order_history
	timesales			=	api_calls.timesales
	call_api			=	api_calls.call_api
	req_sess			=	api_calls.req_sess
	
	############################################################################
	def __init__(self, params=None ):
		self.holdings_graph	= None
		self.holdings		= None
		self.accounts		= []
		self.session		= None
		
		
		try:
			
			# We were passed a JSON file
			if type(params) == type(""):
				with open(params, 'r') as f:
					params = load(f)
					
			# SET paramS
			if type(params) == type({}):
				self.params = params

			else:
				# Try to use environment params
				self.params = {
					'resource_owner_secret'	:	environ['ALLY_OAUTH_SECRET'],
					'resource_owner_key'	:	environ['ALLY_OAUTH_TOKEN'],
					'client_secret'			:	environ['ALLY_CONSUMER_SECRET'],
					'client_key'			:	environ['ALLY_CONSUMER_KEY'],
				}
				
				if 'ALLY_ACCOUNT_NBR' in environ:
					self.params['account'] = environ['ALLY_ACCOUNT_NBR']

			## Check that we have all the parameters we need
			for t in ( 
				'resource_owner_secret',
				'resource_owner_key',
				'client_secret',
				'client_key'
			):
				if t not in self.params.keys():
					raise
				
		except:
			print(
				"""Didn't specify parameters or environment variables not set!
				Go to https://github.com/alienbrett/PyAlly.git for help"""
			)
			raise Exception("Didn't specify Ally API environment varialbles!")
			
