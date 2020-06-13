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

import datetime
import json
import re
nonspace = re.compile(r'\S')

############################################################################
def option_format(symbol="", exp_date="1970-01-01", strike=0, direction=""):
	"""Given some parameters, return the OCC standardized option name
	direction should contain 'C' for a call, or 'P' for a put (lowercase is fine)
	"""
	if not (check(symbol) and check(exp_date) and check(str(strike)) and check(direction)):
		return ""
	
	# direction into C or P
	direction = 'C' if 'C' in direction.upper() else'P'

	# Pad strike with zeros
	def format_strike (strike):
		x	= str(int(strike)) + "000"
		return "0" * (8-len(x)) + x
	# Assemble
	return str(symbol).upper() +\
		datetime.datetime.strptime(exp_date,"%Y-%m-%d").strftime("%y%m%d") +\
		direction + format_strike(strike)

def option_strike(name):
	"""Pull apart an OCC standardized option name and
	retreive the strike price, in integer form"""
	return int(name[-8:])/1000

def option_maturity(name):
	"""Given OCC standardized option name,
	return the date of maturity"""
	return datetime.datetime.strptime(name[-15:-9],"%y%m%d").strftime("%Y-%m-%d")

def option_callput(name):
	"""Given OCC standardized option name,
	return whether its a call or a put"""
	return 'call' if name.upper()[-9] == 'C' else 'put'

def option_symbol(name):
	"""Given OCC standardized option name, return option ticker"""
	return name[:-15]




############################################################################
def pretty_print_POST(req):
	"""Not my code, 
	I stole this function off Stackexchange or something. Thanks Anon!
	"""
	return '{}\n{}\n{}\n\n{}'.format(
		'-----------START-----------',
		req.method + ' ' + req.url,
		'\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
		req.body,
	)
############################################################################
# string typecheck
def check(s):
	return type(s) == type("") and len(s) > 0


def sanitize_input ( s ):
	"""Given an arbitrary string,
	escape '/' characters
	"""
	return s.replace('/',r"%2F")



class JSONStreamParser:
	"""Iteratively decode a JSON string into an object.
	Adapted from solution on page:
		https://stackoverflow.com/questions/21059466/python-json-parser
	"""

	s = ""

	def __init__ ( self, s="" ):
		self.s = s
		self.decoder = json.JSONDecoder()
		self.pos = 0
	
	
	def stream_one ( self ):
		"""Parse one iteration of our currently-held string
		"""
		# Search a bit
		matched = nonspace.search(
			self.s,
			self.pos
		)

		# If we haven't encountered anything,
		#  there's nothing to return
		if not matched:
			return None

		# Otherwise, read through this little bit
		self.pos			= matched.start()
		try:
			decoded, self.pos	= self.decoder.raw_decode(
				self.s,
				self.pos
			)
		except:
			return None

		# Return what we were able to find
		return decoded


	def stream ( self,  new_dat="" ):
		"""Given a single piece of data,
		Yield objects until there's nothing left to do
		"""
		# Append this data into our string queue
		self.s += new_dat

		while True:
			x = self.stream_one()
			if x is None:
				raise StopIteration
			else:
				yield x
