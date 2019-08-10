#################################################
"""            ORDER                """
#################################################
import datetime

all = ['Long']

class Order:
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
        self.qty   = qty
        self.sym   = sym.upper()
        self.price = price
        self.open  = True
        self.timespan = timespan
        self.sectype = sectype
        
        
        if self.qty > 0:
            self.side = 'buy'
        elif new_position:
            self.side = 'short'
        else:
            self.side = 'sell'
            
        self.date['creation'] = datetime.datetime.now()
    ##############################
    def print(self):
        return {
            'qty':self.qty,
            'price':self.price,
            'sym':self.sym,
            'open':self.open,
            'date':self.date
        }
    
class Long(Order):
    ##############################
    def fill(self, price, commission=0.0):
        def execute(price):
            self.price = price
            self.date['completion'] = datetime.datetime.now()
            self.open = False
            
        if (self.price == None) or (self.price - price) * self.qty > 0:
            # execute
            execute(price)
        
        return not self.open
            
