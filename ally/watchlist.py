# Pure python, how about that!
import pyximport; pyximport.install()

############################################################################
def get_watchlists ( self ):
	"""Grab a list of watchlist ID's
	"""
	url_suffix	=	'watchlists.json'

	results = self.call_api (
		use_post	= False,
		url_suffix	= url_suffix,
		use_auth	= True
	)['response']['response']
	if results['error'] != 'Success':
		raise  ValueError

	results = results['watchlists']['watchlist']
	if type(results) != type([]):
		results = [results]

	results = [ entry['id'] for entry in results ]

	return results
############################################################################
def new_watchlist ( self, name, symbols=[] ):
	"""Create a new watchlist, with symbols specified
	"""
	url_suffix	=	'watchlists.json'

	results = self.call_api (
		use_post	= True,
		url_suffix	= url_suffix,
		use_auth	= True,
		data		= {
			'id'		: str(name),
			'symbols'	: ','.join(symbols)
		}
	)['response']['response']
	if results['error'] != 'Success':
		raise  ValueError

	results = [ entry['id'] for entry in results['watchlists']['watchlist'] ]

	return results
############################################################################
def add_symbol ( self, name, symbols=[] ):
	"""Add symbols to watchlist
	"""
	url_suffix	=	'watchlists/' + str(name) + '/symbols.json'

	results = self.call_api (
		use_post	= True,
		url_suffix	= url_suffix,
		use_auth	= True,
		data		= { 'symbols' : ','.join(symbols) }
	)['response']['response']
	if results['error'] != 'Success':
		raise  ValueError

	results = [ entry['id'] for entry in results['watchlists']['watchlist'] ]

	return results
############################################################################
def watchlist ( self, name ):
	"""View instruments in watchlist
	"""
	url_suffix	=	'watchlists/' + str(name) + '.json'

	results = self.call_api (
		use_post	= False,
		url_suffix	= url_suffix,
		use_auth	= True,
	)['response']['response']

	if results['error'] != 'Success':
		raise  ValueError

	results = [
		entry['instrument']['sym']
		for entry in results['watchlists']['watchlist']['watchlistitem']
	]

	return results
############################################################################
def delete_watchlist ( self, name ):
	"""Delete a watchlist given a name
	"""
	url_suffix	=	'watchlists/' + str(name) + '.json'

	results = self.call_api (
		use_post	= False,
		url_suffix	= url_suffix,
		use_auth	= True,
		delete		= True
	)['response']['response']

	if results['error'] != 'Success':
		raise  ValueError

	results = [ entry['id'] for entry in results['watchlists']['watchlist'] ]

	return results
############################################################################
def delete_symbol ( self, name, symbol ):
	"""Delete an instrument from a watchlist
	"""
	url_suffix	=	'watchlists/' + str(name) + '/symbols/' + str(symbol) + '.json'

	results = self.call_api (
		use_post	= False,
		delete		= True,
		url_suffix	= url_suffix,
		use_auth	= True
	)['response']['response']

	if results['error'] != 'Success':
		raise  ValueError

	results = [ entry['id'] for entry in results['watchlists']['watchlist'] ]

	return results
