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

"""Gets information from the API service not directly tied to a particular account.

"""


from .Api import Endpoint, RequestType



class Clock ( Endpoint ):
	_type		= RequestType.Info
	_resource	= 'market/clock.json'



class Status ( Endpoint ):
	_type		= RequestType.Info
	_resource	= 'utility/status.json'







def clock ( block: bool = True):
	"""Return the current market clock.

	Gets a simple dict with timestamp and the status of the market (pre-market, post-market, etc.),
	including the next time that the market clock changes status.

	Args:
		block:
			Specify whether to block thread if request exceeds rate limit


	Returns:
		A dictionary with timestamp, current market status, and any error information.

	Raises:
		RateLimitException: If block=False, rate limit problems will be raised

	Example:

.. code-block:: python


	# Equivalent to the static function
	#   ally.Info.clock()
	a.clock()

	# => {
		'date': '2020-06-14 18:03:58.0-04:00',
		'unixtime': '1592172240.069',
		'status': {
			'current': 'close',
			'next': 'pre',
			'change_at': '08:00:00'
		},
		'error': 'Success',
	}

	"""
	return Clock().request(block=block)

def status ( block: bool = True ):
	"""Return the status of the API service.

	Gets a simple dict with timestamp and the current status (up, down, etc.) of the service.

	Args:
		block:
			Specify whether to block thread if request exceeds rate limit

	Returns:
		A dictionary with current time, and the status of the API service.

	Raises:
		RateLimitException: If block=False, rate limit problems will be raised

	Example:

.. code-block:: python

	# Equivalent to the static function
	#   ally.Info.status()
	a.status()

	# => {
		'time': 'Sun, 14, Jun 2020 18:17:06 GMT',
		'error': 'Success'
	}

	"""
	return Status().request(block=block)

