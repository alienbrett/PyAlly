Trading
=======

Overview
--------

The latest release of the library makes creating, viewing, and modifying orders very simple and intuitive.
Each order object must have a few attributes:

* Buysell
* Pricing
* Quantity
* Time
* Symbol


The parameters can be provided all at once on object instantiation, or any of the orders can be
set or modifed before submitting.


Submit a Stock Order
--------------------------

Buy 8 shares of AAPL at market price, good for the day.

.. code-block:: python
	
	>>> o = ally.Order.Order(
		buysell = 'buy',
		symbol = 'aapl', # case insensitive
		price = ally.Order.Market(),
		time = 'day',
		qty = 8
	)

	# Get a summary of this order in human-readable terms
	>>> print(str(o))
	'Side.Buy 8 units of "AAPL" TimeInForce.Day, Market'

	# See a hypothetical execution info for this order,
	#  without actually submitting the order
	>>> a.submit(o)
	{ ... }

	# Actually submit this order for execution
	#  Returns the ID of this new order, but this parameter
	#  also becomes a parameter of the 'o' object created earlier
	>>> o.orderid
	None

	>>> a.submit(o, preview=False)
	'SVI-12345678'

	>>> o.orderid
	'SVI-12345678'


Order information can be passed to the class on instantiation. Notice that any or all fields can be None, and added later.

.. autoclass:: ally.Order.Order
   :members: __init__


Dealing With Options
--------------------

The only difference between how stocks and options must be handled, is that the option contract
must be changed into its standard OCC symbol first. Then the option can be treated like any other stock, in every other feature.
The ``ally.utils.option_format`` function formats the options's unique OCC symbol from its parameters:

.. autofunction:: ally.utils.option_format


This symbol can now be traded, same as any other stock or option.


Short sell 1 contract (with contract size 100 shares) of the IBM call specified above,
limit at $18, good-til-cancelled.

.. code-block:: python
	

	>>> o = ally.Order.Order(
		buysell = 'sellshort',
		symbol = ibm_call,
		price = ally.Order.Limit( limpx = 18 ),
		time = 'gtc',
		qty = 1
	)



Changing Order Parameters
-------------------------


Modifying orders, outstanding or local orders, is easy as well.

.. code-block:: python

	# Doesn't matter where this order came from
	>>> o
	<ally.Order.order.Order at 0x7f6ae8246278>

	# It turns out that it's a buy-to-open order
	>>> o.buysell
	<Side.Buy: 1>

	# Modify something about it
	>>> o.set_buysell ( 'sellshort' )

	# And now its a sell-to-open
	>>> o.buysell
	<Side.SellShort: 4>


Any of these functions can be used to modify the order's parameters:
	
.. autoclass:: ally.Order.Order
   :members: set_buysell, set_instrument, set_time, set_pricing, set_orderid
   :noindex:


And the order type (Order, Cancel or Modify) can be set as so:

.. code-block:: python

	o.otype = ally.Order.OType.{Order, Modify, Cancel}




Modifying and Cancelling Outstanding Orders
-----------------------------------------------

Cancelling an order is very simple:

.. code-block:: python
	
	>>> a.submit(o, preview = False)
	'SVI-12345678'

	# Oops, now I want to cancel
	>>> cxl = ally.Order.Order(
		orderid = o.orderid,
		type_ = ally.Order.OType.Cancel
	)

	# Submit this new order
	>>> a.submit ( cxl, preview=False )


	# Can also be accomplished by modifying the existing order
	>>> o.otype = ally.Order.OType.Cancel

	>>> a.submit( o, preview=False )



Orders can be revised once submitted but before execution like so:

.. code-block:: python
	
	# Modify an attribute of this order
	>>> o.set_pricing( ally.Order.Limit(8) )

	# Set the order to 'Modify', not 'Order'
	>>> o.otype = ally.Order.OType.Modify

	# Submit to ally for revision
	>>> a.submit ( o, preview=False )



Pricing Types
---------------

The Ally API supports 5 price types in total.

.. autoclass:: ally.Order.Market
   :members: __init__

.. autoclass:: ally.Order.Limit
   :members: __init__

.. autoclass:: ally.Order.Stop
   :members: __init__

.. autoclass:: ally.Order.StopLimit
   :members: __init__


.. autoclass:: ally.Order.TrailingStop
   :members: __init__
