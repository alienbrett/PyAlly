import pyximport; pyximport.install()
from . import utils

############################################################################
def get_strike_prices(self,symbol=""):
	"""return list of float strike prices for specific symbol"""
	
	# Safety first!
	if not utils.check(symbol):
		return []

	results	= self.call_api (
		use_post	= False,
		url_suffix	= 'market/options/strikes.json',
		params		= { 'symbol':symbol }
	)['response']['response']
	

	if results['error'] != 'Success':
		raise ValueError

	results = results['prices']['price']

	if type(results) != type([]):
		results = [results]
	
	# Convert to floats
	return list(map(float,results))
############################################################################
def get_exp_dates(self,symbol=""):
	"""return list of float strike prices for specific symbol"""
	
	# Safety first!
	if not utils.check(symbol):
		return []
	
	results	= self.call_api (
		use_post	= False,
		url_suffix	= 'market/options/expirations.json',
		params		= { 'symbol':symbol }
	)['response']['response']

	if results['error'] != 'Success':
		raise ValueError

	results = results['expirationdates']['date']

	if type(results) != type([]):
		results = [results]
	
	return results
	
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
	if type(query) == type([]):
		fmt_query = ' AND '.join([str(q) for q in query])
	else:
		fmt_query = query
	
	data = {
		'symbol':symbol,
		'query':fmt_query,
		'fids':','.join(fields)
	}
	results	= self.call_api (
		use_post	= True,
		url_suffix	= 'market/options/search.json',
		data		= data
	)['response']['response']

	if results['error'] != 'Success':
		raise ValueError

	results = results['quotes']['quote']

	if type(results) != type([]):
		results = [results]

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
	fmt_query = "xdate-eq:" + str(exp_date) + \
		" AND " + "strikeprice-gte:" + str(float(cur_price)*(1.0-within_pct/100.0)) + \
		" AND " + "strikeprice-lte:" + str(float(cur_price)*(1.0+within_pct/100.0)) + \
		" AND " + "put_call-eq:" + direction
	
	results = self.search_options(
		symbol=symbol,
		query=fmt_query
	)
	
	for op in results:
		if direction == "call":
			op['in_the_money'] = op['strikeprice'] <= cur_price
		else:
			op['in_the_money'] = op['strikeprice'] >= cur_price
	return results
	
