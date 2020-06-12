import xml.etree.cElementTree as ET
import xml.dom.minidom
from enum		import Enum
from .utils		import transposeTree, parseTree

from pytz		import timezone
from datetime	import datetime


nytz = timezone('US/Eastern')



class OrderType(Enum):
	Order	= 1
	Modify	= 2
	Cancel	= 3

class OrderSubmitStatus(Enum):
	Local		= 1
	Submitted	= 2
	Pending		= 3
	Open		= 4
	Paritial	= 5
	Filled		= 6




# Used to translate our type into the FIXML order prefix needed
OType = {
	OrderType.Order.value	: "Order",
	OrderType.Modify.value	: "OrdCxlRplcReq",
	OrderType.Cancel.value	: "OrdCxlReq"
}








class FIXML:

	@property
	def otype ( self ):
		"""Return self's otype
		otype represents the type of this order, one of:

		- Order (Create new order)
		- Modify (change existing, if given an ID)
		- Cancel (remove existing, given an ID)
		"""
		return self._type
	

	
	@property
	def price ( self ):
		"""Return self's pricing
		"""
		return self._data['__execution']


	@property
	def quantity ( self ):
		"""Return self's quantity
		"""
		return int(self._data['OrdQty']['__quantity'])



	@property
	def symbol ( self ):
		"""Return self's symbol
		"""
		return self._data['Instrmt']['__symbol']
	




	def fixml ( self ):
		"""Cast this object to fixml
		"""
		# print(self._data)

		# Insert the order ID if we need to
		if self._type != OrderType.Order:
			self._data['OrigID'] = self._id

			
		# Properly format our order
		order = {
			'xmlns': "http://www.fixprotocol.org/FIXML-5-0-SP2",
			OType[self._type.value]:	self._data
		}

		# Rework our tree
		return transposeTree (
			order,			# The tree structure to turn into FIXML
			name='FIXML',	# Name of root tag
			stringify=True	# Please give us a string
		)
	





	def cancel ( self ):
		"""Modify this order so that when submitted, this order
		overwrites and cancels the older order.
		Calling this function alone is not enough to cancel the order upstream,
		it must be submitted next
		"""
		self._type = OrderType.Cancel





	def from_str ( self, orderstring ):
		"""Parse an XML object into FIXML object
		"""
		# print( orderstring )
		data = parseTree ( ET.fromstring ( orderstring ) )
		data = data['FIXML']['ExecRpt']
		# print(data)

		# print(data)
		data.pop('ID')

		self._id = data.pop('OrdID')


		# Trade datetime
		dt = datetime.strptime(
			data.pop('TxnTm')[:19],
			'%Y-%m-%dT%H:%M:%S'
		)

		# Localize
		dt = nytz.localize(dt)
		# Remove unnecessary
		data.pop('TrdDt')
		# Throw in our aggregate
		self._exec_rpt['timestamp'] = dt

		# Order status info
		for key in ('Stat','LastQty','LastPx', 'LeavesQty'):
			if key in data.keys():
				self._exec_rpt[key]		= data.pop(key)
		self._exec_rpt['Commission'] = data.pop('Comm')['Comm']

	
		# Ally actually has a stupid bug where an extra '2' is appended
		#  to each and every account entry on returned orders
		data['Acct'] = data['Acct'][:-1]


		# And throw the rest of the stuff into our order info dict
		self._data.update(data)
		print(self._data)
	






	def from_fixml ( self, order, otype, orderid ):

		# Keep most of the junk
		self._data	= order._data
		self._type	= otype

		# Extract the order ID
		self._id	= orderid







	def __init__ ( self, order={}, otype=OrderType.Order, orderid=None ):
		"""Construct a wrapper class for an object
		Arguments:

		'order': pass in a dict of the order
			- {...} # (You shouldn't need to do this yourself)

		'otype' must be one of

			- OrderType.Order  # (standard submit)
			- OrderType.Modify # (Modify an outstanding order)
			- OrderType.Cancel # (Cancel an outstanding order)

		'orderid' must be the ID string returned by the API for a submit
			- "SV-123456"

		"""

		"""Cases:
		1) String
				=> parse into fixml, offload

		2) FIXML object
				=> Probably a cancel or modify, handle it

		3) Dict
				=> Probably a new order
		"""

		# This helps us encode into the tag at runtime the correct order
		self._type = OrderType.Order

		# Order ID
		self._id = ""

		# This will be formatted as needed during .fixml() call
		self._data = { }


		# Execution receipt
		self._exec_rpt = {}

		if isinstance(order, str):
			# print("Loading from string")
			self.from_str ( order )


		elif isinstance(order, dict):
			# print("We got us a dict")
			self._type = otype
			
			print(self._type)

			if self._type != OrderType.Order:
				# print("Not an order!")
				self._id = orderid


			if self._type != OrderType.Cancel:
				# print("Not a cancel!")
				# Store the order handed to us
				self._data = order
		else:
			# Probably cancel request
			# print("Loading from fixml object")
			self.from_fixml ( order, otype, orderid )

