#################################################
"""            ALLY                """
#################################################

from . import fixml
from . import order

all = ['fixml.FIXML', 'order.Long', 'Ally']


from requests_oauthlib import OAuth1Session, OAuth1
import requests
import json
import xml.dom.minidom
import datetime
import os
import sys

import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot
matplotlib.use('Agg') 

############################################################################
class Ally:
    endpoints={
        'base':'https://api.tradeking.com/v1/',
        'request_token':'https://developers.tradeking.com/oauth/request_token',
        'user_auth':'https://developers.tradeking.com/oauth/authorize',
        'resource_owner_key':'https://developers.tradeking.com/oauth/resource_owner_key'
    }
    json_params = {
        'indent':4
    }
    
    ############################################################################
    def __init__(self, params=None ):
        
        
        self.session = None
        self.accounts = []
        self.holdings = None
        self.holdings_graph = None
        
        
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
                    'client_key':            os.environ['ALLY_CONSUMER_KEY'],
                    'client_secret':         os.environ['ALLY_CONSUMER_KEY'],
                    'resource_owner_key':    os.environ['ALLY_OATH_TOKEN'],
                    'resource_owner_secret': os.environ['ALLY_OAUTH_SECRET'],
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
    def get_holdings(self,outfile=None,account=None):
        
        print("getting holdings...")
        if account == None:
            account = self.params['account']
            
        account = int(account)
        url = self.endpoints['base'] + 'accounts/' + str(account) + '/holdings.json'
        x = self.session.get(url).json()['response']['accountholdings']
        
        
        if self.accounts == []:
            self.get_accounts()
            
        
        self.holdings = []
        
        for h in x['holding']:
            x = {}
            x['sym'] = h['instrument']['sym']
            x['qty'] = float(h['qty'])
            x['price'] = float(h['price'])
            self.holdings.append(x)
            
        print('Account: ' + str(account))
        self.holdings.append({
            'sym':'USD',
            'price':1.0,
            'qty':float(self.accounts[account]['accountbalance']['money']['cash'])
        })
        
        self.holdings[-1]['qty'] += sum(
            [x['qty'] * x['price']
             for x in self.holdings
             if x['qty'] < 0.0]
        )
        for hld in self.holdings:
            hld['qty'] = abs(hld['qty'])
            
        self.holdings.sort(key=lambda x: x['qty'] * x['price'])
        
        if outfile != None:
            with open(outfile, 'w') as f:
                json.dump(
                    x,
                    f,
                    indent=self.json_params['indent']
                )
        return self.holdings
    ############################################################################
    def holdings_chart(self, graph_file="./graph.png", account=None, regen=False):
        
        if account == None:
            account = self.params['account']
            
        account = int(account)
        
        if self.holdings == None:
            self.get_holdings(account = account)
        
        if self.holdings_graph == None or regen:
            
            labels = [h['sym'] for h in self.holdings]
            sizes = [h['qty'] * h['price'] for h in self.holdings]
            explode = None

            fig, ax = matplotlib.pyplot.subplots()
            ax.pie(sizes, labels=labels, explode=explode, autopct='%1.2f%%', startangle=90)
            ax.axis('equal')
            matplotlib.pyplot.savefig(graph_file, bbox_inches='tight')
            
            self.holdings_graph = graph_file
        
        return self.holdings_graph
    ############################################################################
    def get_quote (self, symbols, fields=None):
        url = self.endpoints['base'] + 'market/ext/quotes' + ('.json' if json else '')
        req_params = {
            'symbols':symbols
        }
        if fields != None:
            req_params['fids'] = fields
            
        auth = OAuth1(self.params['client_key'],
                      self.params['client_secret'],
                      self.params['resource_owner_key'],
                      self.params['resource_owner_secret'],
                      signature_type='auth_header'
                     )
        
        results = requests.post(url, data=req_params, auth=auth).json()
        return results['response']['quotes']['quote']
    
    ############################################################################
    def submit_order (self, order, preview=True, account = None, verbose=False):
        
        if account == None:
            account = self.params['account']
            
        url = self.endpoints['base'] + 'accounts/' + str(account) + '/orders'\
            + ('/preview' if preview else '') + ('.json' if json else '')
        data = fixml.FIXML(order,account)
        
#         if verbose:
#             dom = xml.dom.minidom.parseString(data)
#             data = dom.toprettyxml(data)
        
        auth = OAuth1(self.params['client_key'],
                      self.params['client_secret'],
                      self.params['resource_owner_key'],
                      self.params['resource_owner_secret'],
                      signature_type='auth_header'
                     )
        s = requests.Session()
        req = requests.Request('POST',url, data=data, auth=auth)
        prepped = req.prepare()
        
        results = {'response':s.send(prepped)}
        results['request'] = fixml.pretty_print_POST(prepped)
        
        if verbose:
            print(results['request'])
            
        if json and not preview:
            results['response'] = results['response'].json()
            
        return results
    ############################################################################
    def option_format(symbol, exp_date, strike, direction):
        direction = 'C' if 'C' in direction.upper() else'P'
        def format_strike (strike):
            x = str(int(strike)) + "000"
            return "0" * (8-len(x)) + x
        return str(symbol).upper() +\
            datetime.datetime.strptime(exp_date,"%Y-%m-%d").strftime("%y%m%d") +\
            direction + format_strike(strike)
    ############################################################################
    def account_history(self, account=None, type='all', range="all"):
        # type must be in "all, bookkeeping, trade"
        # range must be in "all, today, current_week, current_month, last_month"
        if account == None:
            account = self.params['account']
            
        url = self.endpoints['base'] + 'accounts/' + str(account) + '/history'\
            + ('.json' if json else '')
        
        auth = OAuth1(self.params['client_key'],
                      self.params['client_secret'],
                      self.params['resource_owner_key'],
                      self.params['resource_owner_secret'],
                      signature_type='auth_header'
                     )
        data = {
            'range':range,
            'transactions':type
        }
        s = requests.Session()
        req = requests.Request('GET',url,params=data,auth=auth)
        prepped = req.prepare()
        
        results = {'response':s.send(prepped).json()}
        results['request'] = fixml.pretty_print_POST(prepped)
        
        return results['response']['response']['transactions']['transaction']
            