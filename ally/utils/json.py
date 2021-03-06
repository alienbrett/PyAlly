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

import json
import re

nonspace = re.compile(r"\S")

############################################################################
class JSONStreamParser:
    """Iteratively decode a JSON string into an object.
    Adapted from solution on page:
            https://stackoverflow.com/questions/21059466/python-json-parser
    """

    s = ""

    def __init__(self, s=""):
        self.s = s
        self.decoder = json.JSONDecoder()
        self.pos = 0

    def stream_one(self):
        """Parse one iteration of our currently-held string"""
        # Search a bit
        matched = nonspace.search(self.s, self.pos)

        # If we haven't encountered anything,
        #  there's nothing to return
        if not matched:
            return None

        # Otherwise, read through this little bit
        self.pos = matched.start()
        try:
            decoded, self.pos = self.decoder.raw_decode(self.s, self.pos)
        except:
            return None

        # Return what we were able to find
        return decoded

    def stream(self, new_dat=""):
        """Given a single piece of data,
        Yield objects until there's nothing left to do
        """
        # Append this data into our string queue
        self.s += new_dat

        while True:
            x = self.stream_one()
            if x is None:
                raise StopIteration
            else:
                yield x
