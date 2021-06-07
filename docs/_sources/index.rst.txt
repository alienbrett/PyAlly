PyAlly Trading Library
==================================

Take control of your `Ally Invest`_ finances through Python. Buy stocks and options in an instant, and stay up-to-date with your investments.

Ally Invest's investment platform is perfect for smaller investors who value a mature web/mobile interface, and low brokerage fees. I made this wrapper so that I could more easily integrate the platform with Python, and reduce the need for human oversight on my account.

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
   option
   news
   ratelimit
   watchlist
   info
   support
   maintaining

Version 1.2.0
----------------

We have added more features in this latest minor release! There have also been numerous contribution and pipeline improvements not listed below. See the commit history for details.

* Added News and Options Searching
  * https://github.com/alienbrett/PyAlly/commit/a12bf634dab79284e9f261df77598ac2d330d1fb
* Added Trade Streaming
  * https://github.com/alienbrett/PyAlly/commit/bb98583d26cc03980a8cd365309b60e5ac5a9272
  * https://github.com/alienbrett/PyAlly/commit/1f301692bc0d28a8c94e7c80a53190360a534ecb

Note that parts of the news searching is broken. Ally's contractor who supplies information for news articles has had trouble suppling some information.

Planned Features
-----------------

* Multi-leg orders

Contributors
------------
* `Brett Graves`_
* `Cole Fox`_
* `Rob Valadez`_
* `Julian Traversa`_
* `Tianyu`_
* `Salient`_
* `Matt Margolin`_
* `Alex Kennedy`_

Message me on Github or `send me an email`_ if you enjoyed the project or thought it could be improved. Anyone with an interest, with an eye for detail, is welcome to contribute.

If you're dying to buy me a beer, I accept venmo at @alienbrett. That said, feel no obligation; this is free software and it's here for you to use.

.. _`Ally bank`: https://www.ally.com/api/invest/documentation/getting-started/

.. _`Brett Graves`: https://github.com/alienbrett

.. _`Cole Fox`: https://github.com/coalfocks

.. _`Rob Valadez`: https://github.com/Rob-Valdez

.. _`Julian Traversa`: https://github.com/JTraversa

.. _`Salient`: https://github.com/Salient

.. _`Tianyu`: https://github.com/Tianyu00

.. _`Matt Margolin`: https://github.com/mm0

.. _`Alex Kennedy`: https://github.com/LaikaN57

.. _`send me an email`: mailto:alienbrett648@gmail.com

.. _github: https://github.com/alienbrett/PyAlly

.. _pypi: https://pypi.org/project/pyally/

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
