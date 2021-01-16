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

############################################################################
def pretty_print_POST(req):
    """Not my code,
    I stole this function off Stackexchange or something. Thanks Anon!
    """
    return "{}\n{}\n{}\n\n{}".format(
        "-----------START-----------",
        req.method + " " + req.url,
        "\n".join("{}: {}".format(k, v) for k, v in req.headers.items()),
        req.body,
    )


############################################################################
# string typecheck
def check(s):
    return type(s) == type("") and len(s) > 0


def sanitize_input(s):
    """Given an arbitrary string,
    escape '/' characters
    """
    return s.replace("/", r"%2F")
