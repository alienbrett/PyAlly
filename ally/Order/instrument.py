from ..utils import (
	option_format,
	option_symbol,
	option_strike,
	option_maturity,
	option_callput
)
#################################################
"""			INSTRUMENT				"""
#################################################
def Instrument(symbol):
	"""Turn a symbol into an Instrument equity object
	"""
	symbol = str(symbol).upper()
	return {
		'__symbol'	: symbol,
		'__type'	: 'equity',
		'Sym'		: symbol,
		'SecTyp'	: 'CS'
	}

#################################################
def Equity(symbol):
	"""Turn a symbol into an Instrument equity object
	(Equivalent to Instrument(symbol))
	"""
	return Instrument(symbol)

#################################################
def Option (instrument, maturity_date, strike):
	"""Create Option object for option information specified
	"""
	return {
		**{
			'MatDt'			: str(maturity_date) + 'T00:00:00.000-05:00',
			'StrkPx'		: str(int(strike)),
			'SecTyp'		: 'OPT',
			'__maturity'	: str(maturity_date),
			'__strike'		: str(int(strike))
		},
		**instrument
	}

#################################################
def Call (instrument, maturity_date, strike):
	"""Create Call object for option information specified
	"""
	# Let Option do some lifting
	x = {
		**{ 'CFI':'OC' },
		**Option(instrument, maturity_date, strike)
	}
	x['__underlying']	= x['Sym']
	x['__type']			= 'call'
	x['__symbol']		= option_format(
		symbol			= x['Sym'],
		exp_date		= x['__maturity'],
		strike			= x['__strike'],
		direction		= 'C'
	)
	return x
		
#################################################
def Put (instrument, maturity_date, strike):
	"""Create Put object for option information specified
	"""
	# Let Option do some lifting
	x = {
		**{ 'CFI':'OP' },
		**Option(instrument, maturity_date, strike)
	}
	x['__underlying']	= x['Sym']
	x['__type']			= 'put'
	x['__symbol']		= option_format(
		symbol			= x['Sym'],
		exp_date		= x['__maturity'],
		strike			= x['__strike'],
		direction		= 'P'
	)
	return x


def implySymbol ( symbol ):
	"""Given a symbol string, create and return
	the symbol object created correctly

	In other words,
		'SYM'			=> Equity('sym')
		'SPYXXXXXXXXXX'	=> Call (...)
	"""
	if len(symbol) > 15:
		# Almost certainly an option, if not unintelligible

		try:

			# Extract the symbol
			underlying	= Instrument (
				option_symbol( symbol )
			)

			# Extract strike price
			strike		= option_strike( symbol )

			# Extract expiration date
			exp_date	= option_maturity( symbol )

			# Extract 
			callput		= option_callput( symbol )

			op = Call if callput == 'call' else Put

			# Wrap it up and spank it on the bottom!
			return op (
				instrument		= underlying,
				maturity_date	= exp_date,
				strike			= strike
			)

		except:
			raise
	
	return Equity ( symbol )
