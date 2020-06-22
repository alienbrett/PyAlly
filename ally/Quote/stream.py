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

from ..Api		import StreamEndpoint, RequestType
import json





class Stream ( StreamEndpoint ):
	_type		= RequestType.Quote
	_resource	= 'market/quotes.json'
	_method		= 'POST'
	_symbols	= []



	def req_body ( self, **kwargs ):
		"""Return get params together with post body data
		"""

		symbols	= kwargs.get('symbols',[])


		# Correctly format Symbols, also store split up symbols
		if type(symbols) == type(""):
			# We were passed string
			fmt_symbols = symbols
			symbols = symbols.split(',')
		else:
			# We were passed list
			fmt_symbols = ','.join(symbols)



		# Store symbols, so we can zip them back up with
		#  the response object
		symbols = [ s.upper() for s in symbols ]
		self._symbols = symbols

		# For aesthetics...
		fmt_symbols = fmt_symbols.upper()

		# Create request POST data
		data = { 'symbols':fmt_symbols }

		params = None
		return params, data








# stream = template(Stream)
def stream ( self, symbols: list =[] ):
	"""Live-streams market quotes for up to 256 stock and options.

	The stream generator that yields dictionaries. Specify one or more
	symbols, and the stream object establishes a connection with the API servers,
	then starts returning symbol-keyed quote objects in real-time.

	Args:
		symbols:
			string or list of strings, each string a symbol to be queried.
			Notice symbols=['spy'], symbols='spy both work.

	Returns:
		A generator

	Example:

.. code-block:: python

		for quote in a.stream('tsla'):
			print(quote)

	"""

	result = Stream(
		auth		= self.auth,
		account_nbr	= self.account_nbr,
		symbols		= symbols
	).request()

	return result
