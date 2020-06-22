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

from ..Api		import AuthenticatedEndpoint, RequestType






class Timesales ( AuthenticatedEndpoint ):
	_type		= RequestType.Quote
	_resource	= 'market/timesales.json'
	_method		= 'GET'
	_symbols	= []





	def extract ( self, response ):
		"""Extract certain fields from response
		"""
		response = response.json()['response']
		quotes = response['quotes']['quote']

		# and return it to the world
		return quotes




	def req_body ( self, **kwargs ):
		"""Return get params together with post body data
		"""

		if 'symbols' not in kwargs.keys():
			raise KeyError('Please specify a symbol. Use symbols="sym"')
		symbols	= kwargs.get('symbols',"")

		# Interval
		interval = kwargs.get('interval','5min')

		# Start date
		startdate = kwargs.get('startdate')

		# End date
		enddate = kwargs.get('enddate')

		params = {
			'symbols':symbols,
			'interval':interval,
			'startdate':startdate,
			'enddate':enddate
		}

		data = None
		return params, data





	@staticmethod
	def DataFrame ( raw ):
		import pandas as pd

		# Create dataframe from our dataset
		df = pd.DataFrame( raw ).apply(
			# And also cast relevent fields to numeric values
			pd.to_numeric,
			errors='ignore'
		)
		return df






def timesales ( self, symbols: str, startdate: str, enddate: str,
	interval: str = '5min', dataframe=True, block: bool = True ):
	"""Gets the most current market data on the price of a symbol.

	Gets a dataset of price points and other information for a symbol.
	Option symbols unfortunately are not accessible from this interface,
	so only stocks can be used.

	Must specify the start and end date on the range requested.
	The API can only return 5 days of intraday prices, the 5 most
	recent trading days, the current day included. Partial data
	will be returned for the current day, if the query occurs
	during the trading hours of a trading day.

	Start and end date should take the form "2019-12-31". This
	interface will be preserved, but datetime instances may be accepted
	in the future as well.

	Args:
		symbols:
			single symbol to query historical quotes on

		startdate:
			string, the start date of interval

		enddate:
			string, end date of the interval

		interval:
			string, specify the size of each time interval.
			Must be one of ('1min','5min','15min')

		dataframe:
			flag, specifies whether to return data in pandas dataframe or flat list of dictionaries.

		block: Specify whether to block thread if request exceeds rate limit

	Returns:
		Depends on dataframe flag. Will return pandas dataframe, or possibly
		list of dictionaries, each one a single quote.

	Raises:
		RateLimitException: If block=False, rate limit problems will be raised

	Examples:

.. code-block:: python

	gld_history = a.timesales (
		symbols = 'gld',
		startdate = '2020-08-21',
		enddate = '2020-08-19',
	)
	print(gld_history.loc[0])

	"""
	result = Timesales(
		auth		= self.auth,
		account_nbr	= self.account_nbr,
		symbols		= symbols,
		interval	= interval,
		startdate	= startdate,
		enddate		= enddate,
		block		= block
	).request()


	if dataframe:
		try:
			result = Timesales.DataFrame ( result )
		except:
			raise
	

	return result
