#################################################
"""            ALLY                """
#################################################

from . import fixml
from . import order

all = ['fixml.FIXML', 'order.Long', 'Ally']


from requests_oauthlib import OAuth1Session, OAuth1
import requests
import json
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
        
        # SET paramS
        if type(params) == type({}):
            self.params = params
        elif type(params) == type(""):
            # LOAD FROM params (file)
            with open(params, 'r') as f:
                self.params = json.load(f)
                
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
    def holdings_chart(self, graph_file=None, account=None):
        
        if account == None:
            account = self.params['account']
            
        account = int(account)
        
        if self.holdings == None:
            self.get_holdings(account = account)
            
        if graph_file == None:
            graph_file = "./graph.png"
        
        if self.holdings_graph == None:
            
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
    def submit_order (self, order, account = None, verbose=False, testXML=False, dry_run=True):
        
        if account == None:
            account = self.params['account']
            
        url = self.endpoints['base'] + 'accounts/' + str(account) + '/orders/preview' + ('.json' if json else '')
        print(url)
        
        data = fixml.FIXML(order,account,testXML)
        
        auth = OAuth1(self.params['client_key'],
                      self.params['client_secret'],
                      self.params['resource_owner_key'],
                      self.params['resource_owner_secret'],
                      signature_type='auth_header'
                     )
        s = requests.Session()
        req = requests.Request('POST',url, data=data, auth=auth)
        prepped = req.prepare()
        
        if dry_run:
            results = {}
        else:
            results = {'response':s.send(prepped)}
        results['request'] = fixml.pretty_print_POST(prepped)
        
        if verbose:
            print(results['request'])
        if json:
            results['response'] = results['response'].json()
            
        return results