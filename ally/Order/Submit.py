# MIT License
#
# Copyright (c) 2020 Brett Graves
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from ..Api			import AccountEndpoint, RequestType
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
			self._order.orderid = response['clientorderid']
			return self._order.orderid

		else:
			return response







	def req_body ( self, order, **kwargs ):
		"""Return get params together with post body data
		"""

		# Get our order
		self._order = order

		# Let FIXML handle this bullshit
		data = self._order.fixml

		# Return what we have
		return None, data
















def submit ( self, order, preview: bool = True, type_ = None, block: bool = True ):
	"""Submits an order object to Ally's servers for execution.

	Given an instantiated ally object, send an order up
	to the API for execution right now. The original order passed
	in to this function will have a new attribute, order.orderid
	(if preview=False), which will encode the order's ID in Ally's system.
	Modifying or cancelling this order will affect this orderid unless it was
	otherwise modified.

	Args:
		order:
			An ally.Order.Order instance

		preview:
			Specify whether to actually submit the order for execution,
			or just to see mock execution info including quotes, from Ally.

		type_:
			Cancels or modifies the order, if not None

		block:
			Specify whether to block thread if request exceeds rate limit

	Returns:
		An order ID string, the same added to the order object (if preview=False)
		or a dictionary with contingent market execution data (if preview=True)


	Raises:
		ExecutionException: Will return verbatim error from Ally's API if a problem with
			the order is encountered.
		RateLimitException: If block=False, rate limit problems will be raised

	"""

	if type_ is not None:
		order.otype = type_

	# Add the account number to this order
	order.set_account(self.account_nbr)

	result = Submission(
		auth		= self.auth,
		account_nbr = self.account_nbr,
		preview		= preview,
		order		= order,
		block		= block
	).request()

	return result
