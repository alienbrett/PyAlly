from ..Api				import (
	Endpoint,
	AuthenticatedEndpoint,
	RequestType
)





class WatchlistEndpoint ( AuthenticatedEndpoint ):
	"""Also automatically resolve url to include account number
	"""
	def resolve ( self, **kwargs):
		"""Inject the account number into the call
		"""
		return self.url().format(kwargs.get('watchlist_name'))










class GetWatchlists ( Endpoint ):
	_type		= RequestType.Info
	_resource	= 'watchlists.json'

	def extract ( self, response ):
		"""Extract certain fields from response
		"""
		response = response.json()['response']
		return [
			v['id'] for v in
				response['watchlists']['watchlist']
		]







class CreateWatchlist ( Endpoint ):
	"""Create a watchlist, and add symbols to it (optionally)
	"""
	_type		= RequestType.Info
	_resource	= 'watchlists.json'
	_method		= 'POST'


	def req_body ( self, **kwargs ):
		"""Return get params together with post body data
		"""

		name = kwargs.get('watchlist_name')
		symbols = ','.join( kwargs.get('watchlist_symbols') )

		data = {
			'id': name,
			'symbols': symbols
		}
		return None, data






class DeleteWatchlist ( Endpoint ):
	"""Outright delete an entire watchlist
	"""
	_type		= RequestType.Info
	_resource	= 'watchlists/{0}.json'
	_method		= 'DELETE'

	

class DeleteFromWatchlist ( WatchlistEndpoint ):
	"""Delete selected symbols from a watchlist
	"""
	_type		= RequestType.Info
	_resource	= 'watchlists/{0}/symbols/{1}.json'
	_method		= 'DELETE'

	def resolve ( self, **kwargs):
		"""Inject the account number into the call
		"""
		return self.url().format(
			kwargs.get( 'watchlist_name' ),
			kwargs.get( 'watchlist_symbol' )
		)







class GetWatchlist ( WatchlistEndpoint ):
	"""Get the symbols from some watchlist
	"""
	_type		= RequestType.Info
	_resource	= 'watchlists/{0}.json'


	def resolve ( self, **kwargs):
		"""Inject the account number into the call
		"""
		watchlist_name = kwargs.get( 'watchlist_name' ).replace('/',r"%2F")
		# print(watchlist_name)
		return self.url().format(
			watchlist_name,
		)

	def extract ( self, response ):
		"""Extract certain fields from response
		"""
		response = response.json()['response']
		syms = response['watchlists']['watchlist']['watchlistitem']
		syms = list ( map (
			lambda d: d['instrument']['sym'],
			syms
		) )
		return syms






class AppendWatchlist ( WatchlistEndpoint ):
	"""Append some symbols to a watchlist
	"""
	_type		= RequestType.Info
	_resource	= 'watchlists/{0}.json'

	def req_body ( self, **kwargs ):
		"""Return get params together with post body data
		"""
		symbols = ','.join( kwargs.get('watchlist_symbols') )
		data = { 'symbols': symbols }
		return None, data