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
"""Controls the API rate limiting

- Rate limits
	* 40 per minute, order submission (including submit, modify, cancel)
	* 60 per minute, market quotes
	* 180 per minute, user info like balance, summary, etc

"""
from .classes	import RequestType
from datetime	import datetime, timezone, timedelta
import json
import time
import pytz

__all__ = ['query']


nytz = pytz.timezone('America/New_York')
gmtz = pytz.timezone('UTC')



_rl_exp_datetime = {
	RequestType.Order.value: None,
	RequestType.Quote.value: None,
	RequestType.Info.value: None
}
_rl_remaining = {
	RequestType.Order.value: -1,
	RequestType.Quote.value: -1,
	RequestType.Info.value: -1
}
_rl_used = {
	RequestType.Order.value: -1,
	RequestType.Quote.value: -1,
	RequestType.Info.value: -1
}

########### UTILS

def extract_ratelimit ( headers_dict ):
	"""Returns rate limit dict, extracted from full headers.
	"""
	return {
		'used'		: int(headers_dict.get('X-RateLimit-Used',0)),
		'expire'	: float(headers_dict.get('X-RateLimit-Expire',0)),
		'limit'		: int(headers_dict.get('X-RateLimit-Limit', 0)),
		'remain'	: int(headers_dict.get('X-RateLimit-Remaining',0))
	}

def absolute_ally_time ( ally_time):
	"""Returns datetime instance of ally's reported time.

	Args:

		ally_time: float timestamp, the time reported by ally

	Returns:

		datetime object, timezone-aware
	"""
	texp = datetime.fromtimestamp(
		ally_time
	).replace(
		tzinfo=timezone.utc
	)

	# API clock is off by around 1 minute. This corrects
	# TODO: let ally devs know that their api clock is wrong
	return texp + timedelta( seconds=60.2 )




def update_vals ( r, req_type_val ):
	"""Updates the correct records in the right spot.
	"""
	_rl_remaining[req_type_val]		= r['remain']
	_rl_used[req_type_val]			= r['used']



########### METHODS


def wait_until_ally_time ( req_type ):
	"""Blocks thread until certain type's reported expire time.

	Args:
		req_type:
			RequestType

	"""
	# Get our stuff in utc
	now = datetime.now().replace( tzinfo=timezone.utc )

	# Get the time we have stored
	a_time = _rl_exp_datetime[req_type.value]

	# Make sure we have a valid time
	if a_time is None:
		a_time = now + timedelta(seconds=60.5)

	print("Waiting until {}".format(str(a_time)))
	# Block thread
	time.sleep( (a_time - now).total_seconds() )




def check ( req_type: RequestType, block: bool ):
	"""Validates whether rate limit exceeded

	Args:
		req_type:
			RequestType enum value

		block:
			Whether or not to block thread, or raise exception

	Returns:

		waittime: None, or datetime point in time when next call can occur

	"""

	if _rl_remaining.get(req_type.value) == 0:
		if block:
			wait_until_ally_time( req_type )
		else:
			raise RateLimitException ( "Too many attemps." )



def normal_update ( headers_dict, req_type ):
	"""Updates internal rate limit state, so that calls to check() are informed

	Args:
		headers_dict:
			raw headers for a specific request

		req_type:
			one of RequestType enum

	"""
	rl = extract_ratelimit (headers_dict)


	# 1) Identify quote type
	# 2) If new endtime is later than our stored endtime, overwrite
	# 3) conditionally increment

	now = datetime.now()
	our_expire = _rl_exp_datetime[req_type.value]

	a_time = absolute_ally_time (rl['expire'])

	if our_expire is None or our_expire < a_time:

		# Store the new date, and all new values
		_rl_exp_datetime[req_type.value]	= a_time
		update_vals ( rl, req_type.value )

	# Only decrement
	elif _rl_used[req_type.value] < rl['used']:
		update_vals ( rl, req_type.value )




def force_update ( req_type ):
	"""Informs our information that we should halt all requests for the remainder of the period.

	This should be called on HTTP 429 error, so that we cool down for the rest of the period.

	Args:
		req_type:
			RequestType value

	"""
	update_vals (
		{
			'remain': 0,
			'used': 0
		},
		req_type.value
	)


def snapshot ( req_type ):
	"""Returns all relevent rate limit information for a given request type.

	Args:
		req_type:
			one of RequestType.{Order,Quote,Info}

	Returns:
		dictionary, with keys ['used','remaining','expiration']

	Example:

.. code-block:: python

	>>> ally.RateLimit.snapshot(ally.RequestType.Quote)

	{'expiration': datetime.datetime(2020, 6, 22, 17, 5, 42, 55080, tzinfo=datetime.timezone.utc),
	'remaining': 56,
	'used': 4}

	"""

	return {
		'expiration': _rl_exp_datetime.get(req_type.value),
		'remaining': _rl_remaining.get(req_type.value),
		'used': _rl_used.get(req_type.value)
	}

