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

from ..Api		import AccountEndpoint, RequestType
from .order		import Order




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

		orders = [ Order(fixml=x['fixmlmessage']) for x in raworders]

		return orders





def orders ( self, block: bool = True ):
	"""View all recent orders in the last 24 hours.

	Calls accounts/./orders.json from the Ally API.

	Args:
		block: Specify whether to block thread if request exceeds rate limit

	Returns:
		A list of Order objects. Attributes can be viewed in the
		same way as orders created by the user.

	Raises:
		RateLimitException: If block=False, rate limit problems will be raised

	"""
	result = OutstandingOrders(
		auth		= self.auth,
		account_nbr = self.account_nbr,
		block		= block
	).request()

	return result
