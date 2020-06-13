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
		# self._acct	= kwargs['account']
		# self._order.set_account(self._acct)

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
