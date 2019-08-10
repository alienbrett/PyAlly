import requests

############################################################################
# Convert option information into OCC-name format
def option_format(symbol="", exp_date="1970-01-01", strike=0, direction=""):
    if not (check(symbol) and check(range) and check(strike) and check(direction)):
        return ""
    # direction into C or P
    direction = 'C' if 'C' in direction.upper() else'P'

    # Pad strike with zeros
    def format_strike (strike):
        x    = str(int(strike)) + "000"
        return "0" * (8-len(x)) + x
    # Assemble
    return str(symbol).upper() +\
        datetime.datetime.strptime(exp_date,"%Y-%m-%d").strftime("%y%m%d") +\
        direction + format_strike(strike)
############################################################################
# I stole this function off Stackexchange or something. Thanks Anon!
def pretty_print_POST(req):
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