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
import math
from .utils import *

############################################################################
def option_format(symbol="", exp_date="1970-01-01", strike=0, direction=""):
    """Returns the OCC standardized option name.

    Args:

            symbol: the underlying symbol, case insensitive
            exp_date: date of expiration, in string-form.
            strike: strike price of the option
            direction: 'C' or 'call' or the like, for call, otherwise 'p' or 'Put' for put

    Returns:

            OCC string, like 'IBM201231C00301000'


    .. code-block:: python

            # Construct the option's OCC symbol
            >>> ibm_call = ally.utils.option_format(
                    exp_date = '2020-12-31',
                    symbol = 'IBM', # case insensitive
                    direction = 'call',
                    strike = 301
            )

            >>> ibm_call
            'IBM201231C00301000'


    """
    if not (
        check(symbol) and check(exp_date) and check(str(strike)) and check(direction)
    ):
        return ""

    # direction into C or P
    direction = "C" if "C" in direction.upper() else "P"

    # Pad strike with zeros
    def format_strike(strike):
        x = str(math.floor(float(strike) * 1000))
        return "0" * (8 - len(x)) + x

    # Assemble
    return (
        str(symbol).upper()
        + datetime.datetime.strptime(exp_date, "%Y-%m-%d").strftime("%y%m%d")
        + direction
        + format_strike(strike)
    )


def option_strike(name):
    """Pull apart an OCC standardized option name and
    retreive the strike price, in integer form"""
    return int(name[-8:]) / 1000.0


def option_maturity(name):
    """Given OCC standardized option name,
    return the date of maturity"""
    return datetime.datetime.strptime(name[-15:-9], "%y%m%d").strftime("%Y-%m-%d")


def option_callput(name):
    """Given OCC standardized option name,
    return whether its a call or a put"""
    return "call" if name.upper()[-9] == "C" else "put"


def option_symbol(name):
    """Given OCC standardized option name, return option ticker"""
    return name[:-15]
