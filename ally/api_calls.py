from . import utils, order as order_utils, fixml, instrument, option_info

from requests.exceptions import ConnectionError, HTTPError, Timeout
from requests_oauthlib   import OAuth1
import pyximport; pyximport.install()
import datetime
import requests
import json
import sys
import os





def quote_stream ( self, symbols ):
	print("Got here...")
	try:
		# Send Request
		r	=	requests.Session().post(
			url		=	self.endpoints['stream'] + 'market/quotes.json',
			auth	=	self.create_auth(),
			data	=	{'symbols':symbols},
			stream=True
		)
		print("Sent the request...")
		for line in r.iter_lines(chunk_size=1):
			print("Got one!")
			decoded_line = line.decode('utf-8')
			print(json.loads(decoded_line))
			
	except ConnectionError as e:
		print("ConnectionError:",e)
		raise
	except HTTPError as e:
		print("HTTPError:",e)
		raise
	except Timeout as e:
		print("Timeout:",e)
		raise


##################

def req_sess ( self ):
	"""Fast session reuse"""
	if self.session == None:
		self.session = requests.Session()
	return self.session

##################
		
def call_api ( self, use_post, url_suffix, data=None,
	params=None,
	timeout=3, verbose=False, use_auth=True, delete=False):
	"""Properly handle sending one API request
	"""
	s		= self.req_sess()

	if use_post:
		meth = 'POST'
	elif delete:
		meth = 'DELETE'
	else:
		meth = 'GET'

	# Create a prepped request
	req = s.prepare_request(
		requests.Request(
			meth,
			self.endpoints['base'] + str(url_suffix),
			auth	= self.create_auth() if use_auth else None,
			data	= data,
			params	= params
		)
	)
	
	try:
		# Send Request
		r = s.send(
			req,
			timeout=timeout
		)
		if r:
			r = r.json()
		else:
			r.raise_for_status()
			
	except ConnectionError as e:
		print("ConnectionError:",e)
		raise
	except HTTPError as e:
		print("HTTPError:",e)
		raise
	except Timeout as e:
		print("Timeout:",e)
		raise

	return {
		'response'	: r,
		'request'	: utils.pretty_print_POST(req)
	}



############################################################################
# Frequently used, this makes it easy
def create_auth(self):
	
	# Precalculate current time
	now = datetime.datetime.now()
	
	# If outside time valid range, regenerate auth
	if self.auth == None or self.last_auth_time + self.valid_auth_dt < now:
		
		# Set cached time to now
		self.last_auth_time = now
	
		# Cache
		self.auth = OAuth1(
			self.params['client_key'],
			self.params['client_secret'],
			self.params['resource_owner_key'],
			self.params['resource_owner_secret'],
			signature_type='auth_header'
		)
		
	return self.auth
############################################################################
def get_accounts(self):

	acnts = self.call_api(
		use_post	= False,
		url_suffix	= 'accounts.json',
		data		= None
	)['response']['response']['accounts']['accountsummary']

	# set accounts internally
	self.accounts = {}
	if type(acnts) == type([]):
		for acnt in list(acnts):
			self.accounts[ int(acnt['account']) ] = acnt
	else:
		self.accounts[ int(acnts['account']) ] = acnts
	
	
	return self.accounts
############################################################################
def get_holdings(self,account=None, verbose=False):
	"""Create pie graph PNG of the current account holdings.
	Currently does not correctly format negative USD Cash
	"""
	
	# Imply account
	if account == None:
		account = self.params['account']
	account = int(account)
	
	# Send Requests
	self.holdings = self.call_api(
		use_post	= False,
		url_suffix	= 'accounts/' + str(account) + '/holdings.json',
		data		= None
	)['response']['response']['accountholdings']

	
	# Get accounts (necessary?)
	if self.accounts == []:
		self.get_accounts()
		
	return self.holdings

############################################################################
def holdings_chart(self, graph_file="./graph.png", account=None, regen=False):
	"""Create graph of current holdings, by dollar value"""

	# This suppresses warnings and errors, idk just go with it
	import matplotlib
	matplotlib.use('Agg') 
	import matplotlib.pyplot
	matplotlib.use('Agg') 

	
	# Imply account
	if account == None:
		account = self.params['account']
		
	# Int-ify account
	account = int(account)
	
	# Ensure we have holdings
	if self.holdings == None:
		self.get_holdings(account = account)
	
	self.holdings['holding'].sort(key=lambda h: abs(float(h['marketvalue'])))
	
	# If no cache or ignore cache:
	if self.holdings_graph == None or regen:
		
		# Create lists of position names and USD size
		labels  = [h['instrument']['sym']	   for h in self.holdings['holding']]
		sizes   = [abs(float(h['marketvalue'])) for h in self.holdings['holding']]

		# Create Pie
		fig, ax = matplotlib.pyplot.subplots()
		ax.pie(sizes, labels=labels, autopct='%1.2f%%', startangle=90)
		ax.axis('equal')
		matplotlib.pyplot.savefig(graph_file, bbox_inches='tight')
		
		# Store name (cache)
		self.holdings_graph = graph_file
		
	# return filename
	return self.holdings_graph
############################################################################
# Return JSON of quote
def get_quote (self, symbols, fields=[]):
	"""For a full list of fields options,
	visit https://www.ally.com/api/invest/documentation/market-ext-quotes-get-post/
	"""
	
	# Ensure correctly-typed input
	if not utils.check(symbols):
		return {}
	
	# Correctly format Symbols, also store split up symbols
	if type(symbols) == type([]):
		# We were passed list
		fmt_symbols = ','.join(symbols)
	else:
		# We were passed string
		fmt_symbols = symbols
		symbols = symbols.split(',')
		
		
	# Correctly format Fields, also store split up fields
	if type(fields) == type([]):
		# We were passed list
		fmt_fields = ','.join(fields)
	else:
		# We were passed string
		fmt_fields = fields
		fields = fmt_fields.split(',')
		
	# For aesthetics...
	fmt_symbols = fmt_symbols.upper()
	
	# Create request paramters according to how we need them
	req_params = { 'symbols':symbols }
	if fields != None:
		req_params['fids'] = fmt_fields
		

	results = self.call_api (
		use_post	= True,
		url_suffix	= 'market/ext/quotes.json',
		data		= req_params
	)['response']['response']['quotes']['quote']
	
	
	# Add symbols to output
	# ...why tf doesn't Ally include this in the quote? they usually send way too much
	if len(symbols) > 1:
		for i,sym in enumerate(symbols):
			results[i]['symbol'] = sym
	else:
		results['symbol'] = symbols[0]
		
		
	return results

############################################################################
def submit_order (self,order,preview=True, append_order=True,
	account=None, verbose=False, discard_quotes=True):

	"""Handle an order request. This ones a little complicated with a few options:
	order		   - Must submit an order constructed with ally.Order.Order(...)
					  Or, submit a cancel request, using an order object and negating
					  ( ally.Order.Cancel(order) will produce a cancel request)
	preview		 - If True, just submit dummy order with some extra information.
					  Set to true by default, to prevent accidental orders by n00bs
	append_order	- If True, return the order information in the response.
					  If disabled, the user must keep track of the original order in case
					  a cancel is needed later.
	account		 - Optionally specify account
	verbose		 - True or False
	discard_quotes  - If disabled, more information is returned, including tick bars
					  of the instrument in question, and extra greeks and metrics.
					  True by default
	"""

	# utils.check input
	if order == None:
		return {}
	

	# Imply account
	if account == None:
		account = self.params['account']
		

	# Must insert account info
	order[order_utils.orderReqType(order)]['Acct'] = str(int(account))


	# Create FIXML formatted request body
	data = fixml.FIXML(order)
	if verbose:
		print(data)

	
	# Assemble URL
	url_suffix = 'accounts/' + str(account) + '/orders'
	if preview:
		url_suffix += '/preview'
	url_suffix += '.json'
	print(url_suffix)


	results = self.call_api (
		use_post	= True,
		url_suffix	= url_suffix,
		data		= data
	)

	
	# Optionally print request
	if verbose:
		print(results['request'])
		print(results['response'])


	results['response'] = results['response']['response']
	
	# optionally throw away unsightly extra bullshit
	if discard_quotes:
		del results['response']['quotes']



	# Optionally send the original order back to the user
	if append_order:
		results['order_submission'] = order

	return results
############################################################################
def account_history(self, account=None, type='all', range="all"):
	"""type must be in "all, bookkeeping, trade"
	range must be in "all, today, current_week, current_month, last_month"
	"""
	
	if not (utils.check(type) and utils.check(range)):
		return {}
	
	# Imply account
	if account == None:
		account = self.params['account']
	# Add parameters
	data = {
		'range':range,
		'transactions':type
	}
	
	results = self.call_api (
		url_suffix	= 'accounts/' + str(account) + '/history.json',
		use_post	= False,
		params		= data
	)
	
	return results['response']['response']['transactions']['transaction']
############################################################################
def order_history(self, account=None, verbose=False):
	"""View most recent orders"""
	if not (utils.check(account)):
		return {}
	
	# Imply account
	if account == None:
		account = self.params['account']
		
	results	= self.call_api(
		url_prefix	= 'accounts/' + str(account) + '/orders.json',
		use_post	= False,
		params		= {}
	)

	# Clean this up a bit, un-nest one layer
	if 'response' in results['response'].keys():
		results['response'] = results['response']['response']

	return results
############################################################################
def timesales( self, symbols="", interval="5min", rpp="10", index="0", startdate="", enddate="", starttime=""):
	"""return time and sales quote data based on a symbol passed as a query parameter
	   see https://www.ally.com/api/invest/documentation/market-timesales-get/ for parameter explanations
	"""

	# Safety first!
	if not utils.check(symbols) or not utils.check(startdate):
		return []

	symbols = symbols.upper()

	# Assemble URL
	url_suffix	= 'market/timesales.json'
	data = {
		'symbols': symbols,
		'interval': interval,
		'rpp': rpp,
		'index': index,
		'startdate': startdate,
		'enddate': enddate,
		'starttime': starttime
	}

	results = self.call_api (
		use_post	= False,
		url_suffix	= url_suffix,
		params		= data
	)

	return results['response']['response']['quotes']['quote']

############################################################################
def market_clock ( self ):
	"""Receive information about the state of the exchange
	"""
	url_suffix = 'market/clock.json'

	results = self.call_api (
		use_post	= False,
		url_suffix	= url_suffix,
		use_auth	= False
	)

	x = { k:v
		for k,v in results['response']['response'].items()
		if k in (
			'date','message','unixtime','error'
		)
	}
	for k,v in results['response']['response']['status'].items():
		x[k] = v
	return x
############################################################################
def api_status ( self ):
	"""Receive information about the Ally servers right now
	"""
	url_suffix	=	'utility/status.json'

	results = self.call_api (
		use_post	= False,
		url_suffix	= url_suffix,
		use_auth	= False
	)

	return { k:v
		for k,v in results['response']['response'].items()
		if k in ( 'time','error')
	}
############################################################################
def get_member ( self ):
	"""Receive some information about the owner of this account
	"""
	results	= self.call_api (
		use_post	= False,
		url_suffix	= 'member/profile.json'
	)['response']['response']['userdata']
	
	x = {
		entry['name']:entry['value']
		for entry in results['userprofile']['entry']
		if entry['name'] not in ('defaultAccount')
	}
	return {**x, **{
		k:v
		for k,v in results['account'].items()
		}
	}

