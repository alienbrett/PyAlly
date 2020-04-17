# Pure python, how about that!
import pyximport; pyximport.install()

############################################################################
def news_search ( self, symbols, maxhits=None, startdate=None, enddate=None ):
	"""Search for news relavent to some symbols
	Optionally, define some maximum hits (integer).
	Also optional, specify date range
	"""
	url_suffix	=	'market/news/search.json'
	data = {
		'symbols'	: ','.join(symbols)
	}

	# Maybe add hits
	if maxhits != None:
		data['maxhits'] = str(int(maxhits))

	# Maybe add start & end date
	if startdate != None and enddate != None:
		print("adding dates...")
		data['startdate']	= startdate
		data['enddate']		= enddate


	# Create call
	results = self.call_api (
		method		= 'GET',
		url_suffix	= url_suffix,
		use_auth	= True,
		data		= data
	)['articles']['article']

	if type(results) != type([]):
		results = [results]

	results = [ {k:v for k,v in entry.items() if k != 'story'} for entry in results ]

	return results
