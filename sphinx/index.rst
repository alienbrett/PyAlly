PyAlly Trading Library
==================================

Take control of your `Ally bank`_ finances through Python.
Buy stocks and options in an instant, and stay up-to-date with your investments.

Ally Bank's investment platform is perfect for smaller investors who value a mature web/mobile interface, and low brokerage fees. I made this wrapper so that I could more easily integrate the platform with Python, and reduce the need for human oversight on my account.

After setting up API keys, PyAlly can provide the basic/essential Ally brokerage transaction functions from a simple python request.

The project can be cloned from github_ or installed through pip on pypi_.


Contents
--------

.. toctree::
   :maxdepth: 2

   installing
   ally
   account
   trading
   quote
   watchlist
   info
   support


Version 1.0.1
----------------

The lastest redesign preserves many features of the old interface, and incorporates a few new ones.
Version 1.0 has been designed around a simple interface which should make modifying orders easier, and many operations more pythonic.
Please note that this version breaks compatibility with all V0.X.X.

* Added pythonic methods for manipulating account watchlists
* Added quote streaming support
* Simplified account operation methods
* Many new order operations. Orders can now be modified or cancelled in an intuitive way


Planned Features
--------------------

* Intelligent rate limiting
* Option searching
* Toplists
* News




Contributors
------------
* `Brett Graves`_
* `Cole Fox`_
* `Rob Valadez`_
* `Julian Traversa`_
* `Tianyu`_


Message me on Github or `send me an email`_ if you enjoyed the project or thought it could be improved.
I do my best to code with quality but sometimes it is easier said than done.
Anyone with an interest with an eye for detail is welcome to contribute.

If you're dying to buy me a beer, I accept venmo at @alienbrett. That said, feel no obligation; this is free software and it's here for you to use.



.. _`Ally bank`: https://www.ally.com/api/invest/documentation/getting-started/

.. _`Brett Graves`: https://github.com/alienbrett

.. _`Cole Fox`: https://github.com/coalfocks

.. _`Rob Valadez`: https://github.com/Rob-Valdez

.. _`Julian Traversa`: https://github.com/JTraversa

.. _`Tianyu`: https://github.com/Tianyu00

.. _`send me an email`: mailto:alienbrett648@gmail.com

.. _github: https://github.com/alienbrett/PyAlly

.. _pypi: https://pypi.org/project/pyally/
