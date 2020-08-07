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

class DateRelation:


	def __init__ (self):
		self._rel = None

	def __gt__ ( self, date ):

		import datetime
		if isinstance ( date, datetime.datetime ):
			date = date.strftime('%Y-%m-%d')

		self._rel = ('>', date)
		return self

	def __lt__ ( self, date ):

		import datetime
		if isinstance ( date, datetime.datetime ):
			date = date.strftime('%Y-%m-%d')

		self._rel = ('<', date)
		return self

	def __str__ ( self ):
		return str(self._rel)




class DateAgg:
	def __init__( self ):

		self._dates = []

	def __add__ (self, relation):

		self._dates.append ( relation )
		return self

	def __str__ ( self ):
		return str(self._dates)
