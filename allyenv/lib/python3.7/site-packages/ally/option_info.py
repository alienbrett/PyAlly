import pyximport; pyximport.install()
from . import utils

############################################################################
def get_strike_prices(self,symbol=""):
	"""return list of float strike prices for specific symbol"""
	
	# Safety first!
	if not utils.check(symbol):
		return []

	results	= self.call_api (
		method		= 'GET',
		url_suffix	= 'market/options/strikes.json',
		data		= { 'symbol':symbol }
	)['prices']['price']

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
		data		= { 'symbol':symbol }
	)['expirationdates']['date']

	if type(results) != type([]):
		results = [results]
	
	return results
	
############################################################################
def search_options(self,symbol="", query="", fields=""):
	"""return list of float strike prices for specific symbol
	QUERYABLE FIELDS:
		strikeprice	#  possible values: 5 or 7.50, integers or decimals		 
		xdate		#  YYYYMMDD
		xmonth		#  MM
		xyear		#  YYYY 
		put_call	#  'put' or 'call'  
		unique		#  'strikeprice', 'xdate'
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
	
	query = ' AND '.join(list(query))
	
	data = {
		'symbol':symbol,
		'query':query,
		'fids':','.join(fields)
	}

	results	= self.call_api (
		method		= 'POST',
		url_suffix	= 'market/options/search.json',
		data		= data
	)['quotes']['quote']

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
	
	fmt_query = ' AND '.join([
		"xdate-eq:"			+ str(exp_date),
		"strikeprice-gte:"	+ str(float(cur_price)*(1.0-within_pct/100.0)),
		"strikeprice-lte:"	+ str(float(cur_price)*(1.0+within_pct/100.0)),
		"put_call-eq:"		+ "call" if "c" in direction else "put"
	])
	
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
	
