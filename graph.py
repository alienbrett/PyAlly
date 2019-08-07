#!/bin/python3
from ally import Ally
import sys

a = Ally(paramfile='keyfile.json')

if len(sys.argv) > 1:
    a.holdings_chart(sys.argv[1])
else:
    a.holdings_chart()
