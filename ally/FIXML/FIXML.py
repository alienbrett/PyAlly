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
	OrderType.Order		: "Order",
	OrderType.Modify	: "OrdCxlRplcReq",
	OrderType.Cancel	: "OrdCxlReq"

}








class FIXML:

	# This helps us encode into the tag at runtime the correct order
	_type = None

	# Order ID
	_id = ""

	# This will be formatted as needed during .fixml() call
	_data = { }


	# Execution receipt
	_exec_rpt = {}





	def __init__ ( self, order=None, otype=OrderType.Order, orderid=None ):
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

		if isinstance(order, str):
			self.from_fixml ( order )

		elif isinstance(order, dict):
			# Make sure we have the correct order
			self._type = otype

			
			if self._type != OrderType.Order:
				self._id = orderid


			if self._type != OrderType.Cancel:
				# Store the order handed to us
				self._data = order



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

		# Properly format our order
		order = {
			'xmlns': "http://www.fixprotocol.org/FIXML-5-0-SP2",
			OType[self._type]:	self._data
		}

		# Rework our tree
		return transposeTree (
			order,			# The tree structure to turn into FIXML
			name='FIXML',	# Name of root tag
			stringify=True	# Please give us a string
		)
	




	def from_fixml ( self, orderstring ):
		"""Parse an XML object into FIXML object
		"""
		data = parseTree ( ET.fromstring ( orderstring ) )
		data = data['FIXML']['ExecRpt']

		data.pop('ID')


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
			self._exec_rpt[key]		= data.pop(key)
		self._exec_rpt['Commission'] = data.pop('Comm')['Comm']


		# And throw the rest of the stuff into our order info dict
		self._data.update(data)

