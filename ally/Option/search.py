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


class Search(AuthenticatedEndpoint):
    _type = RequestType.Info
    _resource = "market/options/search.json"

    def req_body(self, **kwargs):
        """Return get params together with post body data"""
        q = kwargs.get("query", [])
        q = " AND ".join(q)

        params = {
            "symbol": kwargs.get("symbol"),
            "fields": kwargs.get("fields", None),
            "query": q,
        }

        return params, None

    def extract(self, response):
        """Extract certain fields from response"""
        k = response.json().get("response")["quotes"]["quote"]

        return k

    @staticmethod
    def DataFrame(raw):
        import pandas as pd

        # Create dataframe from our dataset
        df = (
            pd.DataFrame(raw)
            .replace({"na": None})
            .apply(
                # And also cast relevent fields to numeric values
                pd.to_numeric,
                errors="ignore",
            )
            .set_index("symbol")
            .drop(columns="basis")
        )

        return df


def search(self, symbol, query=[], fields=[], dataframe=True, block: bool = True):
    """Searches for all option quotes on a symbol that satisfy some set of criteria

    Calls the 'market/options/search.json' endpoint, querying against certain parameters
    provided. Specify a single value or a list of values to expand the size of the search.

    Option queries are composed of three elements:
        1) a condition,
        2) an operator
        3) a value
    in the format field-operator:value (i.e., xyear-eq:2012)

    Queryable Fields:
        strikeprice: possible values: 5 or 7.50, integers or decimals

        xdate: YYYYMMDD

        xmonth: MM

        xyear: YYYY

        put_call: possible values: put, call

        unique: possible values: strikeprice, xdate

    Operators:
        lt: less than

        gt: greater than

        gte: greater than or equal to

        lte: less than or equal to

        eq: equal to

    Visit `the ally website`_ to see the full API behavior.

    Args:
        symbol: Specify the stock symbol against which to query

        fields: (Optional) List of attributes requested for each option contract found. If not specified, will return all applicable fields

        dataframe: (Optional) Return quotes in pandas dataframe

        block: Specify whether to block thread if request exceeds rate limit

    Returns:
        Default: Pandas dataframe

        Otherwise: flat list of dictionaries

    Raises:
        RateLimitException: If block=False, rate limit problems will be raised

    Example:
        .. code-block:: python

            a.search(
                'spy',
                query=[
                    'xdate-eq:20200814',   # Only consider contracts expiring on 2020-08-14
                    'put_call-eq:put',     # Only conside puts
                    'strikeprice-lte:350', # Only consider strikes <= $350
                    'strikeprice-gte:315'  # Only consider strikes >= $315
                ]
            )


        .. _`the ally website`: https://pypi.org/project/pyally/
    """
    result = Search(
        auth=self.auth,
        account_nbr=self.account_nbr,
        symbol=symbol,
        fields=fields,
        query=query,
        block=block,
    ).request()

    if dataframe:
        try:
            result = Search.DataFrame(result)
        except:
            raise

    return result
