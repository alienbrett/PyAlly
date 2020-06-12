from ..Api		import AccountEndpoint, RequestType




class OutstandingOrders ( AccountEndpoint ):
	"""Send an order off
	"""
	_type		= RequestType.Order
	_resource	= 'accounts/{0}/orders.json'
	_method		= 'GET'




	def extract ( self, response ):
		"""Extract certain fields from response
		"""
		response = response.json()['response']
		raworders = response['orderstatus']['order']

		if not isinstance(raworders, list):
			raworders = [raworders]

		# orders = [ FIXML ( x ) for x in raworders]

		return raworders





def orders ( self, **kwargs ):
	"""Use self.auth to query for current account holdings
	"""
	result = OutstandingOrders(
		auth		= self.auth,
		account_nbr = self.account_nbr,
		**kwargs
	).request()

	return result
