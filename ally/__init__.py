#################################################
"""            ALLY                """
#################################################

from . import utils
from . import order
from . import fixml
from . import instrument

all = ['fixml.FIXML', 'order', 'instrument', 'Ally', 'utils']

from requests_oauthlib   import OAuth1
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
    
    # Cache Oauth requests (faster)
    last_auth_time = None
    auth           = None
    valid_auth_dt  = datetime.timedelta(seconds=9.7)
    
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
                    'client_secret'          : os.environ['ALLY_CONSUMER_SECRET'],
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
            
    ############################################################################
    # Frequently used, this makes it easy
    def create_auth(self):
        
        # Precalculate current time
        now = datetime.datetime.now()
        
        # If outside time valid range, regenerate auth
        if self.auth == None or self.last_auth_time + self.valid_auth_dt < now:
            
            # Set cached time to now
            self.last_auth_time = now
        
            # Cache
            self.auth = OAuth1(self.params['client_key'],
                          self.params['client_secret'],
                          self.params['resource_owner_key'],
                          self.params['resource_owner_secret'],
                          signature_type='auth_header'
                         )
            
        return self.auth
    ############################################################################
    def dump_params(self, fname='keyfile.json'):
        if fname != None:
            with open(fname,'w') as f:
                json.dump(self.params, f, indent=self.json_params['indent'])
                
        return json.dumps(self.params,indent=self.json_params['indent'])
    ############################################################################
    def get_accounts(self):
        
        # Assemble URL
        url = self.endpoints['base'] + 'accounts.json'
        
        # Authenticate
        auth = self.create_auth()
        
        # Send Requests
        acnts = requests.get(url, auth=auth).json()['response']['accounts']['accountsummary']
        
        # set accounts internally
        self.accounts = {}
        for acnt in acnts:
            self.accounts[int(acnt['account'])] = acnt
        
        
        return self.accounts
    ############################################################################
    def get_holdings(self,account=None, verbose=False):
        """Create pie graph PNG of the current account holdings.
        Currently does not correctly format negative USD Cash
        """
        
        # Imply account
        if account == None:
            account = self.params['account']
        account = int(account)
        
        # Assemble URL
        url = self.endpoints['base'] +\
              'accounts/'            +\
              str(account)           +\
              '/holdings.json'
        
        # Create auth
        session = requests.Session()
        auth    = self.create_auth()
        req     = requests.Request('GET',url,auth=auth).prepare()
        
        # Send Request
        self.holdings = session.send(req).json()\
            ['response']['accountholdings']
        
        # Get accounts (necessary?)
        if self.accounts == []:
            self.get_accounts()
            
        return self.holdings
    
    ############################################################################
    def holdings_chart(self, graph_file="./graph.png", account=None, regen=False):
        """Create graph of current holdings, by dollar value"""
        
        # Imply account
        if account == None:
            account = self.params['account']
            
        # Int-ify account
        account = int(account)
        
        # Ensure we have holdings
        if self.holdings == None:
            self.get_holdings(account = account)
        
        self.holdings['holding'].sort(key=lambda h: abs(float(h['marketvalue'])))
        
        # If no cache or ignore cache:
        if self.holdings_graph == None or regen:
            
            # Create lists of position names and USD size
            labels  = [h['instrument']['sym']       for h in self.holdings['holding']]
            sizes   = [abs(float(h['marketvalue'])) for h in self.holdings['holding']]

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
    def get_quote (self, symbols, fields=[]):
        """For a full list of fields options,
        visit https://www.ally.com/api/invest/documentation/market-ext-quotes-get-post/
        """
        
        # Ensure correctly-typed input
        if not utils.check(symbols):
            return {}
        
        # Correctly format Symbols, also store split up symbols
        if type(symbols) == type([]):
            # We were passed list
            fmt_symbols = ','.join(symbols)
        else:
            # We were passed string
            fmt_symbols = symbols
            symbols = symbols.split(',')
            
            
        # Correctly format Fields, also store split up fields
        if type(fields) == type([]):
            # We were passed list
            fmt_fields = ','.join(fields)
        else:
            # We were passed string
            fmt_fields = fields
            fields = fmt_fields.split(',')
            
        # For aesthetics...
        fmt_symbols = fmt_symbols.upper()
        
        
        # Assemble URL
        url = self.endpoints['base'] + 'market/ext/quotes.json'
        
        # Authenticate
        auth = self.create_auth()
        
        # Create request paramters according to how we need them
        req_params = { 'symbols':symbols }
        if fields != None:
            req_params['fids'] = fmt_fields
            
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
        if len(symbols) > 1:
            for i,sym in enumerate(symbols):
                results[i]['symbol'] = sym
        else:
            results['symbol'] = symbols[0]
            
            
        return results
    
    ############################################################################
    def submit_order (self,orderx,preview=True, append_order=True,
        account=None, verbose=False, discard_quotes=True):

        """Handle an order request. This ones a little complicated with a few options:
        order           - Must submit an order constructed with ally.Order.Order(...)
                          Or, submit a cancel request, using an order object and negating
                          ( ally.Order.Cancel(order) will produce a cancel request)
        preview         - If True, just submit dummy order with some extra information.
                          Set to true by default, to prevent accidental orders by n00bs
        append_order    - If True, return the order information in the response.
                          If disabled, the user must keep track of the original order in case
                          a cancel is needed later.
        account         - Optionally specify account
        verbose         - True or False
        discard_quotes  - If disabled, more information is returned, including tick bars
                          of the instrument in question, and extra greeks and metrics.
                          True by default
        """

        # utils.check input
        if orderx == None:
            return {}
        

        # Imply account
        if account == None:
            account = self.params['account']

            
        # Must insert account info
        orderx[order.orderReqType(orderx)]['Acct'] = str(int(account))


        # Assemble URL
        url = self.endpoints['base']          +\
              'accounts/'                     +\
              str(account)                    +\
              '/orderxs'                       +\
              ('/preview' if preview else '') +\
             '.json'
        
        # Create FIXML formatted request body
        data = fixml.FIXML(orderx)
        if verbose:
            print(data)
        
        # Create Authentication headers
        auth = self.create_auth()
        
        # Create HTTP request objects
        session = requests.Session()
        req     = requests.Request('POST',url, data=data, auth=auth).prepare()
        
        # Submit request to put orderx in as soon as possible
        # results            = {'response':json.loads(session.send(req).text)}
        results            = {'response':session.send(req)}
        results['request'] = utils.pretty_print_POST(req)
        
        # Optionally print request
        if verbose:
            print(results['request'])
            print(results['response'])

        # Clean this up a bit, un-nest one layer
        if 'response' in results.keys():
            if 'response' in results['response'].keys():
                results['response'] = results['response']['response']
        
        # optionally throw away unsightly extra bullshit
        if discard_quotes:
            del results['response']['quotes']

        # Optionally send the original orderx back to the user
        if append_order:
            results['orderx_submission'] = orderx

        return results
    ############################################################################
    def account_history(self, account=None, type='all', range="all"):
        """type must be in "all, bookkeeping, trade"
        range must be in "all, today, current_week, current_month, last_month"
        """
        
        if not (utils.check(type) and utils.check(range)):
            return {}
        
        # Imply account
        if account == None:
            account = self.params['account']
            
        # Assemble URL
        url =   self.endpoints['base']    +\
                'accounts/'               +\
                str(account)              +\
                '/history.json'
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
        results['request'] = utils.pretty_print_POST(req)
        
        return results['response']['response']['transactions']['transaction']
    ############################################################################
    def order_history(self, account=None, verbose=False):
        """View most recent orders"""
        if not (utils.check(account)):
            return {}
        
        # Imply account
        if account == None:
            account = self.params['account']
            
        # Assemble URL
        url =   self.endpoints['base']    +\
                'accounts/'               +\
                str(account)              +\
                '/orders.json'
        # Add parameters
        data = {}
        
        # Create HTTP Request objects
        session = requests.Session()
        auth    = self.create_auth()
        req     = requests.Request('GET',url,params=data,auth=auth).prepare()
        
        
        results            = {'response':session.send(req).json()}
        results['request'] = utils.pretty_print_POST(req)

        # Clean this up a bit, un-nest one layer
        if 'response' in results.keys():
            if 'response' in results['response'].keys():
                results['response'] = results['response']['response']

        return results
    ############################################################################
    def get_strike_prices(self,symbol=""):
        """return list of float strike prices for specific symbol"""
        
        # Safety first!
        if not utils.check(symbol):
            return []
        
        # Format
        symbol = symbol.upper()
        
        # Assemble URL
        url =   self.endpoints['base']    + 'market/options/strikes.json'
        data = { 'symbol':symbol }
        
        # Create HTTP Request objects
        auth               = self.create_auth()
        results            = requests.get(url,params=data,auth=auth).json()
        
        # Convert to floats
        return [float(x) for x in results['response']['prices']['price']]
    ############################################################################
    def get_exp_dates(self,symbol=""):
        """return list of float strike prices for specific symbol"""
        
        # Safety first!
        if not utils.check(symbol):
            return []
        
        # Format
        symbol = symbol.upper()
        
        # Assemble URL
        url =   self.endpoints['base']    + 'market/options/expirations.json'
        data = { 'symbol':symbol }
        
        # Create HTTP Request objects
        auth               = self.create_auth()
        results            = requests.get(url,params=data,auth=auth).json()
        
        return results['response']['expirationdates']['date']
        
    ############################################################################
    def search_options(self,symbol="", query="", fields=""):
        """return list of float strike prices for specific symbol
        QUERYABLE FIELDS:
            strikeprice  #  possible values: 5 or 7.50, integers or decimals         
            xdate        #  YYYYMMDD
            xmonth       #  MM
            xyear        #  YYYY 
            put_call     #  'put' or 'call'  
            unique       #  'strikeprice', 'xdate'
        OPERATORS:
            LT  # <
            GT  # >
            LTE # <=
            GTE # >=
            EQ  # ==

        For complete list of Field values, and query help
         https://www.ally.com/api/invest/documentation/market-options-search-get-post/
        """
        
        # Safety first!
        if not utils.check(symbol):
            print("failed check?")
            return []
        
        # Format
        symbol    = symbol.upper()
        if type(query) == type([]):
            fmt_query = ' AND '.join([str(q) for q in query])
        else:
            fmt_query = query
        
        # Assemble URL
        url =   self.endpoints['base']    + 'market/options/search.json'
        data = {
            'symbol':symbol,
            'query':fmt_query,
            'fids':','.join(fields)
        }
        
        # Create HTTP Request objects
        auth               = self.create_auth()
        results            = requests.post(url,params=data,auth=auth).json()\
            ['response']['quotes']['quote']
        
        return results
    ############################################################################
    def options_chain(self, symbol="", direction="c", within_pct=4.0, exp_date=""):
        """Return options with a strike price within a certain percentage of the 
        last price on the market, on a given exp_date, with a specified direction.
        """
        
        # Safety first!
        if not utils.check(symbol) or not utils.check(direction) or not utils.check(exp_date):
            return []
        
        cur_price = self.get_quote(symbol, 'last')['last']
        
        # Format
        direction = "call" if "c" in direction else "put"
        symbol    = symbol.upper()
        fmt_query = "xdate-eq:" + str(exp_date) + \
            " AND " + "strikeprice-gte:" + str(float(cur_price)*(1.0-within_pct/100.0)) + \
            " AND " + "strikeprice-lte:" + str(float(cur_price)*(1.0+within_pct/100.0)) + \
            " AND " + "put_call-eq:" + direction
        
        # Assemble URL
        url =   self.endpoints['base']    + 'market/options/search.json'
        data = {
            'symbol':symbol,
            'query':fmt_query
        }
        
        # Create HTTP Request objects
        auth               = self.create_auth()
        results            = requests.post(url,params=data,auth=auth).json()\
            ['response']['quotes']['quote']
        
        for op in results:
            if direction == "call":
                op['in_the_money'] = op['strikeprice'] <= cur_price
            else:
                op['in_the_money'] = op['strikeprice'] >= cur_price
        return results
        
