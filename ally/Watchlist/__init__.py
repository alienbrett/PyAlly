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

from collections.abc	import MutableMapping, MutableSet
from datetime			import datetime, timedelta
import weakref

from .methods import (
	GetWatchlist,
	GetWatchlists,
	CreateWatchlist,
	AppendWatchlist,
	DeleteWatchlist,
	DeleteFromWatchlist
)



class WatchlistWrapper ( MutableSet ):
	_name = ""
	_syms = set()

	def __init__ ( self, parent, name, symbols ):
		self._name = name
		self._syms = set(symbols)
		self._auth = weakref.ref(parent._auth())


	def __str__( self ):
		return str(self._syms)


	def __iter__ ( self ):
		return self._syms.__iter__()
	

	def __contains__ ( self, x ):
		return self._syms.contains(x)
	

	def __len__ ( self ):
		return self._syms.__len__()
	

	def add ( self, x ):
		if x not in self._syms:
			result = AppendWatchlist(
				auth				= self._auth(),
				watchlist_symbols	= x
			).request()

			
	def discard ( self, x ):
		if x in self._syms:
			result = DeleteFromWatchlist(
				auth				= self._auth(),
				watchlist_name		= self._name,
				watchlist_symbol	= x
			).request()
		






class Watchlist ( MutableMapping ):
	"""Handle an accounts watchlists and symbols in a pythonic way.

	The Watchlist account object wraps ally's watchlist
	functionality and mimics python datatypes.

	Examples:
		
.. code-block:: python
	
	# See all of your watchlists
	list(a.watchlists)

	# => ['w-list1', 'my-watchlist',...]


.. code-block:: python

	# See all the symbols associated with a watchlist
	list(a.watchlist['w-list1'])

	# => ['aapl, 'googl',...]

.. code-block:: python
	
	# Create a watchlist, and initialize with symbols
	a.watchlist['new-watchlist'] = ['aapl,'googl',...]

.. code-block:: python
	
	# Remove a symbol from a watchlist
	a.watchlist['new-watchlist'].pop('aapl')

.. code-block:: python
	
	# Delete a watchlist
	a.watchlist.pop('new-watchlist')


	"""
	_auth = None
	_expire = None


	def __getitem__ ( self, name ):
		result = GetWatchlist(
			auth			= self._auth(),
			watchlist_name	= name
		).request()

		return WatchlistWrapper( self, name, result )


	def __setitem__ ( self, name, symbols ):
		if type(symbols) != type([]):
			symbols = [str(symbols)]

		CreateWatchlist(
			auth				= self._auth(),
			watchlist_name		= name,
			watchlist_symbols	= symbols
		).request()


		
	def __delitem__ ( self, name ):
		DeleteWatchlist(
			auth				= self._auth(),
			watchlist_name		= name
		).request()
		

	
	@property
	def _all ( self ):
		"""Reusable way to get all watchlists
		"""
		t = datetime.now()

		if self._expire is None or self._expire < t:

			# Update cache
			self._expire = t + timedelta( seconds=0.75 )

			self._lists = GetWatchlists(
				auth = self._auth(),
			).request()

		return self._lists



	def __str__ ( self ):
		return str(self._all)
		
		

	def __iter__ ( self ):
		"""Return list to run ove
		Must be wrapped in some special iterator stuff
		so that python3 will handle it how we want
		"""
		return self._all.__iter__()
	
	
		

	def __len__ ( self ):
		return len(self._all)




	def __init__ ( self, parent ):
		self._auth = weakref.ref(parent.auth)
		
	
