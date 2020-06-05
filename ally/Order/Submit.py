from ..Api			import AccountEndpoint, RequestType
from .order			import orderReqType, injectAccount
from ..exception	import OrderException
from ..FIXML		import FIXML




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

		return self.url().format(
			kwargs.get('account_nbr'),
			"/preview" if kwargs.get('preview',True) else ''
		)
	





	def extract ( self, response ):
		"""Extract certain fields from response
		"""
		response = response.json()['response']

		return response







	def req_body ( self, **kwargs ):
		"""Return get params together with post body data
		"""

		order = kwargs['order']


		# Must insert account info
		#  this helps us handle modify operations
		orderReqTyp		= orderReqType( order )
		# order[]['Acct']	= kwargs.get( 'account_nbr' )

		# Create FIXML formatted request body
		# Except key errors and the like,
		#  hopefully in the future we can offer more granular exceptions
		try:
			data = FIXML( order )
		except:
			raise OrderException("Incorrectly formatted order")

		return None, data
















def submit ( self, order, **kwargs ):
	"""Use self.auth to query for current account holdings
	"""

	# Add the account number to this order
	order = injectAccount ( order, self.account_nbr )


	# Throw order into the right place
	kwargs['order'] = order
	

	result = Submission(
		auth		= self.auth,
		account_nbr = self.account_nbr,
		**kwargs
	).request()

	return result
