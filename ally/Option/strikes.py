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

from ..Api import AuthenticatedEndpoint, RequestType


class Strikes(AuthenticatedEndpoint):
    _type = RequestType.Info
    _resource = "market/options/strikes.json"

    def req_body(self, **kwargs):
        """Return get params together with post body data"""
        params = {"symbol": kwargs.get("symbol")}
        return params, None

    def extract(self, response):
        """Extract certain fields from response"""
        k = response.json().get("response")["prices"]["price"]

        if k is None:
            k = []

        return list(map(float, k))


def strikes(self, symbol, block: bool = True):
    """Gets list of available strike prices for a symbol.

    Calls the 'market/options/strikes.json' endpoint to get list of all
    strikes available for some given equity.

    Args:
            symbol: Specify the stock symbol against which to query
            block: Specify whether to block thread if request exceeds rate limit

    Returns:
            List of strikes (float)

    Raises:
            RateLimitException: If block=False, rate limit problems will be raised

    Example:
            .. code-block:: python

               a.strikes('spy')
               # [ 5.0, 10.0, ... ]

    """
    result = Strikes(
        auth=self.auth, account_nbr=self.account_nbr, block=block, symbol=symbol
    ).request()

    return result
