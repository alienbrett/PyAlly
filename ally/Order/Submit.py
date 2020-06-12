from ..Api			import AccountEndpoint, RequestType
# from .order			import orderReqType, injectAccount
from ..exception	import OrderException, ExecutionException
from .order			import Order




class Submission ( AccountEndpoint ):
	"""Send an order off
	"""
	_type		= RequestType.Order
	_resource	= 'accounts/{0}/orders{1}.json'
	_method		= 'POST'






	def resolve ( self, **kwargs):
		"""Inject the account number into the call
		Also controls whether or not this is a preview.

		To submit a real order, specify 'preview'=False
		in the constructer arguments
		"""
		self._preview = kwargs.get('preview',True)

		return self.url().format(
			kwargs.get('account_nbr'),
			"/preview" if self._preview else ''
		)
	





	def extract ( self, response ):
		"""Extract certain fields from response
		"""
		response = response.json()['response']
		
		if response['error'] != 'Success':
			raise ExecutionException(response['error'])


		if not self._preview:
			# Get the ID we were promissed
			self._order._id = response['clientorderid']
			return self._order._id

		else:
			return response







	def req_body ( self, **kwargs ):
		"""Return get params together with post body data
		"""

		# Get our order
		self._order = kwargs['order']

		# Update account info
		self._acct	= kwargs['account']
		self._order.set_account(self._acct)

		# Let FIXML handle this bullshit
		data = self._order.fixml

		# Return what we have
		return None, data
















def submit ( self, order, **kwargs ):
	"""Use self.auth to query for current account holdings
	"""

	# Add the account number to this order
	order.set_account(self.account_nbr)

	# Throw order into the right place
	kwargs['order'] = order
	

	result = Submission(
		auth		= self.auth,
		account_nbr = self.account_nbr,
		**kwargs
	).request()

	return result
