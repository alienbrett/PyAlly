import pyximport; pyximport.install()

from requests.exceptions import ConnectionError, HTTPError, Timeout
from requests_oauthlib   import OAuth1
import datetime
import requests
import json

from . import utils
from . import order as order_utils
from . import fixml






def quote_stream ( self, symbols ):
	"""Incomplete, don't use this yet
	"""
	"""https://stream.tradeking.com/v1/market/quotes.json?
	symbols=AAPL
	oauth_consumer_key=X9j5GvxuowIiCClw45bXdWLc3UXS3kxMaM68XzxrI9A3
	oauth_token=cmpCWpPq1pjmPA0I4kSamCwuGne8rQBlFjF2ZOUC84U6
	"""
	print("Got here...")
	try:
		# Send Request
		r	=	requests.Session().post(
			url		=	self.endpoints['stream'] + 'market/quotes.json',
			auth	=	self.create_auth(),
			data	=	{
				'symbols':symbols,
				'oauth_consumer_key':self.params['client_key']
			},
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
		
def call_api (
	self, method, url_suffix, data=None, 
	timeout=3, verbose=False, use_auth=True, full_output=False):
	"""Properly handle sending one API request
	"""
	s		= self.req_sess()

	method = method.upper()

	if method == 'GET':
		send_params	= data
		send_data	= None
	else:
		send_data	= data
		send_params = None

	# Create a prepped request
	req = s.prepare_request(
		requests.Request(
			method,
			self.endpoints['base'] + str(url_suffix),
			auth	= self.create_auth() if use_auth else None,
			params	= send_params,
			data	= send_data
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
			r = r['response']

			if r['error'] != 'Success':
				raise ValueError( r['error'] )
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

	if full_output:
		return {
			'response'	: r,
			'request'	: utils.pretty_print_POST(req)
		}
	else:
		return r



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
		method		= 'GET',
		url_suffix	= 'accounts.json'
	)['accounts']['accountsummary']

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
		method		= 'GET',
		url_suffix	= 'accounts/' + str(account) + '/holdings.json'
	)['accountholdings']

	
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
		method		= 'POST',
		url_suffix	= 'market/ext/quotes.json',
		data		= req_params
	)['quotes']['quote']
	
	
	# Add symbols to output
	# ...why tf doesn't Ally include this in the quote? they usually send way too much
	if len(symbols) > 1:
		for i,sym in enumerate(symbols):
			results[i]['symbol'] = sym
	else:
		results['symbol'] = symbols[0]
		
		
	return results

############################################################################
def submit_order (
	self,order,preview=True, append_order=True,
	account=None, verbose=False, discard_quotes=True
):

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


	# Perform our call
	results = self.call_api (
		method		= 'POST',
		url_suffix	= url_suffix,
		data		= data,
		full_output	= verbose # we can change the output dynamically
	)

	
	if verbose:
		# Notice results will have different type, depending on verbose
		print(results['request'])
		print(results['response'])

	else:
		# optionally throw away unsightly extra bullshit
		if discard_quotes:
			del results['quotes']


	# Optionally send the original order back to the user
	if append_order:
		results['order_submission'] = order

	return results
############################################################################
def account_history(self, account=None, type_='all', range_="all"):
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
		'range':range_,
		'transactions':type_
	}
	
	results = self.call_api (
		url_suffix	= 'accounts/' + str(account) + '/history.json',
		method		= 'GET',
		data		= data
	)
	
	return results['transactions']['transaction']
############################################################################
def order_history(self, account=None, verbose=False):
	"""View most recent orders"""
	if not (utils.check(account)):
		return {}
	
	# Imply account
	if account == None:
		account = self.params['account']
		
	results	= self.call_api(
		method		= 'GET',
		url_prefix	= 'accounts/' + str(account) + '/orders.json'
	)

	"""
	# Clean this up a bit, un-nest one layer
	if 'response' in results['response'].keys():
		results['response'] = results['response']['response']
	"""

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
	data = {k:v for k,v in {
			'symbols': symbols,
			'interval': interval,
			'rpp': rpp,
			'index': index,
			'startdate': startdate,
			'enddate': enddate,
			'starttime': starttime
		}.items()
		if v is not None and v != ""
	}

	results = self.call_api (
		method		= 'GET',
		url_suffix	= url_suffix,
		data		= data
	)

	return results['quotes']['quote']

############################################################################
def market_clock ( self ):
	"""Receive information about the state of the exchange
	"""
	url_suffix = 'market/clock.json'

	results = self.call_api (
		method		= 'GET',
		url_suffix	= url_suffix,
		use_auth	= False
	)

	x = { k:v
		for k,v in results.items()
		if k in ( 'message','status')
	}
	return x
############################################################################
def api_status ( self ):
	"""Receive information about the Ally servers right now
	"""
	url_suffix	=	'utility/status.json'

	results = self.call_api (
		method		= 'GET',
		url_suffix	= url_suffix,
		use_auth	= False
	)

	return { k:v
		for k,v in results.items()
		if k in ( 'time','error')
	}
############################################################################
def get_member ( self ):
	"""Receive some information about the owner of this account
	"""
	results	= self.call_api (
		method		= 'GET',
		url_suffix	= 'member/profile.json'
	)['userdata']
	
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
############################################################################
def toplists ( self, list_type='topactive', exchange='N' ):
	"""Return ranked list of stocks during the last trading day, for a specific exchange.
	list_type must be one of (
		'topactive', [default]
		'toplosers',
		'topvolume',
		'topgainers',
		'toppctgainers'
	)
	exchange must be one of (
		'N' => NYSE [default]
		'A' => American Stock exchange
		'Q' => Nasdaq
		'U' => Nasdaq Bulletin Board
		'V' => Nasdaq OTC Other
	)
	"""
	results = self.call_api (
		method		= 'GET',
		url_suffix	= 'market/toplists/' + str(list_type) + '.json',
		data		= { 'exchange' : exchange }
	)
	
	return results
############################################################################
def get_cash(self, account=None):
	# Imply account
	if account == None:
		account = self.params['account']
	account = int(account)

	acnts = self.call_api(
		method='GET',
		url_suffix='accounts.json'
	)['accounts']['accountsummary']

	# set accounts internally
	self.accounts = {}
	if type(acnts) == type([]):
		for acnt in list(acnts):
			self.accounts[int(acnt['account'])] = acnt
	else:
		self.accounts[int(acnts['account'])] = acnts

	cash = self.accounts[account]['accountbalance']['money']
	
	return cash
