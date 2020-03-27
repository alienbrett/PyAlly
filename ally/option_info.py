from . import utils

from requests_oauthlib   import OAuth1
import pyximport; pyximport.install()
import requests
import json

############################################################################
def get_strike_prices(self,symbol=""):
	"""return list of float strike prices for specific symbol"""
	
	# Safety first!
	if not utils.check(symbol):
		return []
	
	# Format
	symbol = symbol.upper()
	
	# Assemble URL
	url =   self.endpoints['base']	+ 'market/options/strikes.json'
	data = { 'symbol':symbol }
	
	# Create HTTP Request objects
	auth			   = self.create_auth()
	results			= requests.get(url,params=data,auth=auth).json()
	
	# Convert to floats
	return [float(x) for x in results['response']['prices']['price']]
############################################################################
def get_exp_dates(self,symbol=""):
	"""return list of float strike prices for specific symbol"""
	
	# Safety first!
	if not utils.check(symbol):
		return []
	
	# Format
	symbol = symbol.upper()
	
	# Assemble URL
	url =   self.endpoints['base']	+ 'market/options/expirations.json'
	data = { 'symbol':symbol }
	
	# Create HTTP Request objects
	auth			   = self.create_auth()
	results			= requests.get(url,params=data,auth=auth).json()
	
	return results['response']['expirationdates']['date']
	
############################################################################
def search_options(self,symbol="", query="", fields=""):
	"""return list of float strike prices for specific symbol
	QUERYABLE FIELDS:
		strikeprice  #  possible values: 5 or 7.50, integers or decimals		 
		xdate		#  YYYYMMDD
		xmonth	   #  MM
		xyear		#  YYYY 
		put_call	 #  'put' or 'call'  
		unique	   #  'strikeprice', 'xdate'
	OPERATORS:
		LT  # <
		GT  # >
		LTE # <=
		GTE # >=
		EQ  # ==

	For complete list of Field values, and query help
	 https://www.ally.com/api/invest/documentation/market-options-search-get-post/
	"""
	
	# Safety first!
	if not utils.check(symbol):
		print("failed check?")
		return []
	
	# Format
	symbol	= symbol.upper()
	if type(query) == type([]):
		fmt_query = ' AND '.join([str(q) for q in query])
	else:
		fmt_query = query
	
	# Assemble URL
	url =   self.endpoints['base']	+ 'market/options/search.json'
	data = {
		'symbol':symbol,
		'query':fmt_query,
		'fids':','.join(fields)
	}
	
	# Create HTTP Request objects
	auth			   = self.create_auth()
	results			= requests.post(url,params=data,auth=auth).json()\
		['response']['quotes']['quote']
	
	return results
############################################################################
def options_chain(self, symbol="", direction="c", within_pct=4.0, exp_date=""):
	"""Return options with a strike price within a certain percentage of the 
	last price on the market, on a given exp_date, with a specified direction.
	"""
	
	# Safety first!
	if not utils.check(symbol) or not utils.check(direction) or not utils.check(exp_date):
		return []
	
	cur_price = self.get_quote(symbol, 'last')['last']
	
	# Format
	direction = "call" if "c" in direction else "put"
	symbol	= symbol.upper()
	fmt_query = "xdate-eq:" + str(exp_date) + \
		" AND " + "strikeprice-gte:" + str(float(cur_price)*(1.0-within_pct/100.0)) + \
		" AND " + "strikeprice-lte:" + str(float(cur_price)*(1.0+within_pct/100.0)) + \
		" AND " + "put_call-eq:" + direction
	
	# Assemble URL
	url =   self.endpoints['base']	+ 'market/options/search.json'
	data = {
		'symbol':symbol,
		'query':fmt_query
	}
	
	# Create HTTP Request objects
	auth			   = self.create_auth()
	results			= requests.post(url,params=data,auth=auth).json()\
		['response']['quotes']['quote']
	
	for op in results:
		if direction == "call":
			op['in_the_money'] = op['strikeprice'] <= cur_price
		else:
			op['in_the_money'] = op['strikeprice'] >= cur_price
	return results
	
