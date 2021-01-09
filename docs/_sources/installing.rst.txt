Installing
===============


Overview
--------

A new API project needs to be created through the account page on Ally's website,
and the project keys imported so that they can be used with the module.



Get the Library
---------------

To install the library, just use pip

.. code-block:: console

   $ pip install pyally


Log into `Ally Invest`_, go to the specific account page, click Tools->API

.. image:: https://github.com/alienbrett/PyAlly/blob/master/resources/tools.PNG?raw=true

Fill out the API token application as a Personal Application

.. image:: https://github.com/alienbrett/PyAlly/blob/master/resources/new_application.PNG?raw=true

It's **strongly recommended** to store the keys in environment variables.


.. image:: https://github.com/alienbrett/PyAlly/blob/master/resources/details.PNG?raw=true

To do this, insert the following into ``~/.bashrc``:

.. code-block:: console

   export ALLY_CONSUMER_KEY=XXXXXXXXXXXXXXXXXXXXXXXX
   export ALLY_CONSUMER_SECRET=XXXXXXXXXXXXXXXXXXXXX
   export ALLY_OAUTH_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXX
   export ALLY_OAUTH_SECRET=XXXXXXXXXXXXXXXXXXXXXXXX
   export ALLY_ACCOUNT_NBR=12345678



First Steps
-----------


To import the library, just run

.. code-block:: python

   import ally


We need to pass the API keys to the pyally object on instantiation. This can be done in a few ways:



Keys: Environment Variables
---------------------------

It's **strongly recommended** that the API keys be stored as environment variables.
This is more secure than other methods, as it conceals the credentials of ally account if
the code is leaked or distributed. If the account variables are specified as recommended this way,
instantiation is easy:

.. code-block:: python

   a = ally.Ally()


**And you're done!**



Keys: JSON file
---------------

The object creator also accepts a json file holding the dict keys, and 
this is about as secure as the environment variable method.
Place the API keys into a JSON file (this looks very similar to a python dict):

.. code-block:: python

   {
       'ALLY_CONSUMER_SECRET':XXXX,
       'ALLY_CONSUMER_KEY':XXXX,
       'ALLY_OAUTH_SECRET':XXXX,
       'ALLY_OAUTH_TOKEN':XXXX,
       'ALLY_ACCOUNT_NBR':XXXX
   }



Then the object can be instantiated like:

.. code-block:: python

   a = ally.Ally('/path/to/params.json')



Keys: Passing Directly
----------------------

Variables can be passed in on instantiation. This way, no account variables need to be set.
Keep in mind that this is much less secure for distributable applications, since anyone with these keys
will have access to the account with which they're associated.



.. code-block:: python

   params = {
       'ALLY_CONSUMER_SECRET':XXXX,
       'ALLY_CONSUMER_KEY':XXXX,
       'ALLY_OAUTH_SECRET':XXXX,
       'ALLY_OAUTH_TOKEN':XXXX,
       'ALLY_ACCOUNT_NBR':XXXX
   }
   a = ally.Ally(params)



Now you're ready to make API calls with your new object and start trading.


.. _`Ally Invest`: https://secure.ally.com
