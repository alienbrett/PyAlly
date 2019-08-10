#################################################
"""            ALLY                """
#################################################

from . import fixml
from . import order

all = ['fixml.FIXML', 'order.Long', 'Ally']


from requests_oauthlib   import OAuth1Session, OAuth1
import xml.dom.minidom
import datetime
import requests
import json
import sys
import os

# This suppresses warnings and errors, idk just go with it
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot
matplotlib.use('Agg') 

############################################################################
class Ally:
    endpoints={
        'base'               :'https://api.tradeking.com/v1/',
        'request_token'      :'https://developers.tradeking.com/oauth/request_token',
        'user_auth'          :'https://developers.tradeking.com/oauth/authorize',
        'resource_owner_key' :'https://developers.tradeking.com/oauth/resource_owner_key'
    }
    json_params = {
        'indent':4
    }
    
    ############################################################################
    def __init__(self, params=None ):
        
        
        self.holdings_graph = None
        self.holdings       = None
        self.accounts       = []
        self.session        = None
        
        
        try:
            
            # SET paramS
            if type(params) == type({}):

                # Take dict
                self.params = params

            elif type(params) == type(""):
                

                # LOAD FROM params (file)
                with open(params, 'r') as f:
                    self.params = json.load(f)
                    

            else:

                # Try to use environment params
                self.params = {
                    'resource_owner_secret'  : os.environ['ALLY_OAUTH_SECRET'],
                    'resource_owner_key'     : os.environ['ALLY_OAUTH_TOKEN'],
                    'client_secret'          : os.environ['ALLY_CONSUMER_KEY'],
                    'client_key'             : os.environ['ALLY_CONSUMER_KEY'],
                }
                
                try:
                    self.params['account'] = os.environ['ALLY_ACCOUNT_NBR']
                except e:
                    pass
                
        except:
            print("Didn't specify parameters or environment variables not set!\n" + 
            "Go to https://github.com/alienbrett/PyAlly.git for help")
            raise Exception("Didn't specify Ally API environment varialbles!")
            
        # ESTABLISH SESSION
        self.session =  OAuth1Session(
            client_key=self.params['client_key'],
            client_secret=self.params['client_secret'],
            resource_owner_key=self.params['resource_owner_key'],
            resource_owner_secret=self.params['resource_owner_secret']
        )
    ############################################################################
    # Frequently used, this makes it easy
    def create_auth(self):
        return OAuth1(self.params['client_key'],
                      self.params['client_secret'],
                      self.params['resource_owner_key'],
                      self.params['resource_owner_secret'],
                      signature_type='auth_header'
                     )
    ############################################################################
    def dump_params(self, fname='keyfile.json'):
        if fname != None:
            with open(fname,'w') as f:
                json.dump(self.params, f, indent=self.json_params['indent'])
                
        return json.dumps(self.params,indent=self.json_params['indent'])
    ############################################################################
    def get_accounts(self,outfile=None):
        
        print('getting accounts...')
        
        url = self.endpoints['base'] + 'accounts.json'
        acnts = self.session.get(url).json()\
            ['response']['accounts']['accountsummary']
        
        
        self.accounts = {}
        for acnt in acnts:
            self.accounts[int(acnt['account'])] = acnt
        
        if outfile != None:
            with open(outfile, 'w') as f:
                json.dump(
                    self.accounts,
                    f,
                    indent=self.json_params['indent']
                )
        return self.accounts
    ############################################################################
    # Create pie graph PNG of the current account holdings.
    #  Currently does not correctly format negative USD Cash
    def get_holdings(self,account=None, verbose=False):
        
        # Imply account
        if account == None:
            account = self.params['account']
        account = int(account)
        
        # Assemble URL
        url = self.endpoints['base'] +\
              'accounts/'            +\
              str(account)           +\
              '/holdings.json'
        print(url)
        
        # Create auth
        session = requests.Session()
        auth    = self.create_auth()
        req     = requests.Request('GET',url,auth=auth).prepare()
        
        # Send Request
        raw_holdings = session.send(req).json()\
            ['response']['accountholdings']
        
        # Get accounts (necessary?)
        if self.accounts == []:
            self.get_accounts()
            
        # Reinit holdings
        self.holdings = []
        
        # Format correct information into self.holdings
        for h in raw_holdings['holding']:
            
            # Precalculate some values
            float_price = float(h['price'])
            float_qty   = float(h['qty'])
            
            # Only grab symbol, price, and quantity
            self.holdings.append({
                'value' : float_qty * float_price,
                'sym'   : h['instrument']['sym'],
                'price' : float_price,
                'qty'   : float_qty
            })
            
        # Precalculate dollar value of account
        usd = float(self.accounts[account]['accountbalance']['money']['cash'])
        
        # Add USD cash as holding
        self.holdings.append({
            'value' : usd,
            'sym'   : 'USD',
            'price' : 1.0,
            'qty'   : usd
        })
        
        # Subtract short positions value from cash
        self.holdings[-1]['qty'] += sum(
            [x['value']
             for x in self.holdings
             if x['qty'] < 0.0]
        )
        
        # Normalize all holding values into positive amount
        for hld in self.holdings:
            hld['qty'] = abs(hld['qty'])
            
        # Sort holdings by market value
        self.holdings.sort(key=lambda x: x['value'])
        
        return self.holdings
    
    ############################################################################
    def holdings_chart(self, graph_file="./graph.png", account=None, regen=False):
        
        # Imply account
        if account == None:
            account = self.params['account']
            
        # Int-ify account
        account = int(account)
        
        # Ensure we have holdings
        if self.holdings == None:
            self.get_holdings(account = account)
        
        # If no cache or ignore cache:
        if self.holdings_graph == None or regen:
            
            # Create lists of position names and USD size
            labels  = [h['sym']              for h in self.holdings]
            sizes   = [h['qty'] * h['price'] for h in self.holdings]

            # Create Pie
            fig, ax = matplotlib.pyplot.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.2f%%', startangle=90)
            ax.axis('equal')
            matplotlib.pyplot.savefig(graph_file, bbox_inches='tight')
            
            # Store name (cache)
            self.holdings_graph = graph_file
            
        # return filename
        return self.holdings_graph
    ############################################################################
    # Return JSON of quote
    def get_quote (self, symbols, fields=None):
        
        # Useful later
        symbols = symbols.upper()
        
        # Assemble URL
        url = self.endpoints['base'] + 'market/ext/quotes' + ('.json' if json else '')
        
        # Create request paramters according to how we need them
        req_params = { 'symbols':symbols }
        if fields != None:
            req_params['fids'] = fields
        
        # Create request    
        auth = self.create_auth()
        results = requests.post(\
                url,
                data=req_params,
                auth=auth
        ).json()\
        ['response']['quotes']['quote']
        
        # Add symbols to output
        # ...why tf doesn't Ally include this in the quote? they usually send way too much
        for i,sym in enumerate(symbols.split(',')):
            results[i]['symbol'] = sym
            
            
        return results
    
    ############################################################################
    def submit_order (self, order, preview=True, account = None, verbose=False):
        
        # Imply account
        if account == None:
            account = self.params['account']
            
        # Assemble URL
        url = self.endpoints['base']          +\
              'accounts/'                     +\
              str(account)                    +\
              '/orders'                       +\
              ('/preview' if preview else '') +\
             '.json'
        
        # Create FIXML formatted request body
        data = fixml.FIXML(order,account)
        
        # Create Authentication headers
        auth = self.create_auth()
        
        # Create HTTP request objects
        session = requests.Session()
        req     = requests.Request('POST',url, data=data, auth=auth).prepare()
        
        # Submit request to put order in as soon as possible
        results            = {'response':session.send(req)}
        results['request'] = fixml.pretty_print_POST(req)
        
        # Optionally print request
        if verbose:
            print(results['request'])
        
        return results
    ############################################################################
    # Convert option information into OCC-name format
    def option_format(symbol, exp_date, strike, direction):
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
    def account_history(self, account=None, type='all', range="all"):
        # type must be in "all, bookkeeping, trade"
        # range must be in "all, today, current_week, current_month, last_month"
        
        # Imply account
        if account == None:
            account = self.params['account']
            
        # Assemble URL
        url =   self.endpoints['base']    +\
                'accounts/'               +\
                str(account)              +\
                '/history'                +\
                ('.json' if json else '')
        # Add parameters
        data = {
            'range':range,
            'transactions':type
        }
        
        # Create HTTP Request objects
        session = requests.Session()
        auth    = self.create_auth()
        req     = requests.Request('GET',url,params=data,auth=auth).prepare()
        
        results            = {'response':session.send(req).json()}
        results['request'] = fixml.pretty_print_POST(req)
        
        return results['response']['response']['transactions']['transaction']
            