#################################################
"""            ORDER                """
#################################################



#################################################
# ORDER CONSTRUCTOR
def Order(timespan,type,price,instrument, quantity):
    x = {
       'Order':{
            **timespan,
            **type,
            **price,
            'Instrmt':{
                **instrument
            },
            'OrdQty':{
                **quantity
            }
        }
    }
    if x['Order']['Instrmt']['SecTyp'] == 'OPT':
        x['Order']['OrdQty']['Qty'] = str(round(float(x['Order']['OrdQty']['Qty'])))
#     if x['Instrmt']['SecTyp'] == 'OP':
#         x['Order']['PosEfct'] = 'O' if x['
    return x
        

"""
# Timespans
Timespan('day')
Timespan('gtc')
Timespan('marketonclose')



# Types
Buy()              # Buy to open (default)
Buy(to_open=False) # Buy to cover

Sell()              # Sell short (default)
Sell(to_open=False) # Sell to close



# Pricing
Market ()         # Give me anything
Limit (69)        # Execute at least as favorably as $69.00
Stop (4.20)       # Stop order at $4.20
StopLimit (
    Stop  (10),   # Stop at $10.00
    Limit (9.50)  # No worse than $9.50
)
StopLoss (
    isBuy=False,  # Interpret stop as less than current price
    pct=True,     # Treat 'stop' as pct
    stop=5.0      # Stop at 5% from highest achieved after order placed
)
StopLoss (
    isBuy=True,   # Interpret stop as less than current price
    pct=False,     # Treat 'stop' as pct
    stop=5.0      # Stop at $5.00 above lowest price
)


# Quantity
Quantity ( 15 )

"""







# Order Lifetime constructors
#################################################
def Timespan(type='Day'):
    type = type.lower()
    
    # for the day
    if type == 'day' or type == 'gfd':
        return {
            '__timeframe':'GFD',
            'TmInForce':'0'
        }
    
    # Market on close (wtf ???)
    elif type == 'marketonclose':
         return {
            '__timeframe':'MarketOnClose',
            'TmInForce':'7'
         }
        
    # GTC order
    elif type == 'gtc':
        return {
            '__timeframe':'GTC',
            'TmInForce':'1'
         }
    
    #Something went wrong
    else:
        return {
            '__timeframe':'invalid'
        }



# Order Type constructors
#################################################
# Buy() --------> Buy
# Buy(False) ----> Buy to cover
def Buy(to_open=True):
    if to_open:
        return {
            '__side'  :'buy',
            'Side'    :'1'
        }
    else:
        return {
            '__side'  : 'buy_to_cover',
            'Side'    : '1',
            'AccTyp'  : '5'
        }

# Sell() --------> Sell
# Sell(False) ----> Sell short
def Sell(to_open=True):
    if to_open:
        return {
            '__side'  :'sell_short',
            'Side'    :'2'
        }
    else:
        return {
            '__side'  : 'sell',
            'Side'    : '5'
        }




# Order Pricing constructors
#################################################
def StopLoss( isBuy=False, pct=True, stop=5 ):
    # If pct == true?
    #  treat stop as percent
    # if pct == false?
    #  treat stop as dollar amnt
    return {
            '__execution'  : 'stop limit',
            'Typ'           : 'P',
            'ExecInst'      : 'a',
            'PegPxTyp'      : '1',
            'OfstTyp'       : '0' if pct else '1',
            'OfstVal'       : str(float(stop) * (-1 if isBuy else 1))
        }
    
    
# Pass in sub-orders
def StopLimit(stopOrder, limitOrder):
    return {
        '__execution' : 'stop limit',
        'Typ'    : '4',
        'Px'     : limitOrder['Px'],
        'StopPx' : stopOrder['StopPX'],
    }
    
    
def Market():
    return {
        '__execution' :'market',
        'Typ'    :'1'
    }
    

def Limit(limit):
    return {
        '__execution' :'limit',
        'Typ'    :'2',
        'Px'     :str(float(limit))
    }
    

def Stop(stop):
    return {
        '__execution' :'stop',
        'Typ'    :'3',
        'StopPX' : str(float(stop))
    }



# Quantity
#################################################
def Quantity(n):
    n = str(float(n))
    return {
        '__quantity' : n,
        'Qty'        : n
    }