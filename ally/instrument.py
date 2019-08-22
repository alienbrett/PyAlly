#################################################
"""            INSTRUMENT                """
#################################################
def Instrument(symbol):
    symbol = str(symbol).upper()
    return {
        '__symbol' : symbol,
        'Sym'      : symbol,
        'SecTyp'   : 'CS'
    }

#################################################
def Equity(symbol):
    return Instrument(symbol)

#################################################
def Option (instrument, maturity_date, strike):
    return {
        **instrument,
        **{
            'MatDt'   : str(maturity_date) + 'T00:00:00.000-05:00',
            'StrkPx'  : str(int(strike)),
            'SecTyp' : 'OPT'
        }
    }

#################################################
def Call (instrument, maturity_date, strike):
    # Let Option do some lifting
    return {
        **{
        'CFI':'OC'
        },
        **Option(instrument, maturity_date, strike)
    }
        
#################################################
def Put (instrument, maturity_date, strike):
    # Let Option do some lifting
    return {
        **{
        'CFI':'OP'
        },
        **Option(instrument, maturity_date, strike)
    }