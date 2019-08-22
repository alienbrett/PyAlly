#################################################
"""            ORDER                """
#################################################
import datetime
from .. import utils

all = ['Long']

# Stores an instrument order. Specify symbol, quantity, price, ...
class Order:
    # Static uninitialized values
    qty = 0.0
    price = 0.0
    sym = ""
    open = True
    timespan = 'GTC'
    side = None
    date={
        'creation':None,
        'completion':None
    }
    ##############################
    def __init__(self, sym, qty, price=None, timespan='GTC', new_position=True,sectype='CS'):
        
        # Safety first!
        self.valid = utils.check(sym)
        if not self.valid:
            return
        
        # boilerplate
        self.date['creation'] = datetime.datetime.now()
        self.sym              = sym.upper()
        self.timespan         = timespan
        self.sectype          = sectype
        self.price            = price
        self.open             = True
        self.qty              = qty
        
        
        # set order position
        # Ally api does not make distinctio between buy to cover and buy to open
        #  However they distinguish between sell short and sell to close
        
        
        # quantity > 0? Buy order
        if self.qty > 0:
            self.side = 'buy'
            
        # if quantity < 0? Sell/Short order
        # don't already have a position? sell to open
        elif new_position:
            self.side = 'short'
        else:
            # already have a position? sell to close
            self.side = 'sell'
            
            
    ##############################
    def print(self):
        return {
            'qty'   : self.qty,
            'price' : self.price,
            'sym'   : self.sym,
            'open'  : self.open,
            'date'  : self.date
        }
    
# Mostly just wraps Order, idk
#  Will be fleshed out more in the future
class Long(Order):
    ##############################
    # unused as of right now
    def fill(self, price, commission=0.0):
        def execute(price):
            self.price = price
            self.date['completion'] = datetime.datetime.now()
            self.open = False
            
        if (self.price == None) or (self.price - price) * self.qty > 0:
            # execute
            execute(price)
        
        return not self.open
            