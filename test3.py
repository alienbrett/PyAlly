from ally import *

print(Ally.option_format("ibm", "2014-01-18", 200.00, "call"))

a = Ally('keyfile.json')
print(a.account_history())