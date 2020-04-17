import pyximport; pyximport.install()
import datetime

############################################################################
def option_format(symbol="", exp_date="1970-01-01", strike=0, direction=""):
	"""Given some parameters, return the OCC standardized option name
	direction should contain 'C' for a call, or 'P' for a put (lowercase is fine)
	"""
	if not (check(symbol) and check(exp_date) and check(str(strike)) and check(direction)):
		return ""
	
	# direction into C or P
	direction = 'C' if 'C' in direction.upper() else'P'

	# Pad strike with zeros
	def format_strike (strike):
		x	= str(int(strike)) + "000"
		return "0" * (8-len(x)) + x
	# Assemble
	return str(symbol).upper() +\
		datetime.datetime.strptime(exp_date,"%Y-%m-%d").strftime("%y%m%d") +\
		direction + format_strike(strike)

def option_strike(name):
	"""Pull apart an OCC standardized option name and
	retreive the strike price, in integer form"""
	return int(name[-8:])/1000

def option_maturity(name):
	"""Given OCC standardized option name,
	return the date of maturity"""
	return datetime.datetime.strptime(name[-15:-9],"%y%m%d").strftime("%Y-%m-%d")

def option_callput(name):
	"""Given OCC standardized option name,
	return whether its a call or a put"""
	return 'call' if name.upper()[-9] == 'C' else 'put'

def option_symbol(name):
	"""Given OCC standardized option name, return option ticker"""
	return name[:-15]
############################################################################
def pretty_print_POST(req):
	"""Not my code, 
	I stole this function off Stackexchange or something. Thanks Anon!
	"""
	return '{}\n{}\n{}\n\n{}'.format(
		'-----------START-----------',
		req.method + ' ' + req.url,
		'\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
		req.body,
	)
############################################################################
# string typecheck
def check(s):
	return type(s) == type("") and len(s) > 0
