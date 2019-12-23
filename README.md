# PyAlly
Python3 wrapper for [Ally Invest brokerage API](https://www.ally.com/api/invest/documentation/getting-started/ "Ally Invest API")

Ally Bank's investment platform is perfect for smaller investors who value a mature web/mobile interface, and low brokerage fees. I made this wrapper so that I could more easily integrate the platform with Python, and reduce the need for human oversight on my account.

After setting up API keys, PyAlly can provide the basic/essential Ally brokerage transaction functions from a simple python request.

## Supported features
* Stock buy/sell/short/buy-to-cover orders
* Query account transaction history
* Represent account holdings
* Query account holdings
* Orders supported:
    * Market
    * Stop
    * Limit
    * Stop Limit
    * Stop Loss
* Instrument quotes
* Option trading

## Requirements
* requests-oathlib
* matplotlib

## Installation
`pip3 install pyally`

Once the package is downloaded, we recommend setting environment variables to store Ally API credentials.

Log into [Ally Invest](https://secure.ally.com), go to the specific account page, click Tools->API


![Tools](https://github.com/alienbrett/PyAlly/blob/master/resources/tools.PNG?raw=true)


Fill out the API token application as a Personal Application


![New Application](https://github.com/alienbrett/PyAlly/blob/master/resources/new_application.PNG?raw=true)


Enter the API tokens and secrets into your environment variables 


![Details](https://github.com/alienbrett/PyAlly/blob/master/resources/details.PNG?raw=true)


Insert the following into `~/.bashrc`:

```bash
export ALLY_CONSUMER_KEY=XXXXXXXXXXXXXXXXXXXXXXXX
export ALLY_CONSUMER_SECRET=XXXXXXXXXXXXXXXXXXXXX
export ALLY_OAUTH_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXX
export ALLY_OAUTH_SECRET=XXXXXXXXXXXXXXXXXXXXXXXX
```


## Documentation

#### Initialize
```python
import ally
a = ally.Ally()
```


### Account Functions
#### Transaction History
```python
#	Get transaction history in JSON dictionary form
#		- Optionally specify account, if not in set in
#		environment
#		- Optionally specify type of transaction, must be 
#			"all", "bookkeeping", or "trade"
#            [default "all"]
#        - Optionally specify time window for transactions, must be in 
#            "all", "today", "current_week", "current_month", "last_month"
#            [default "all"]
trans_history = a.account_history(
	account=12345678,
	type="all",
    range="current_week"
)
```

#### Current Account Holdings
```python
#    Get current holdings for an account in JSON dict format
#        Uses default account if not specified
#        Optionally dump json to file
current_holdings = a.get_holdings(
    account=12345678,
    outfile="./holdings.json"
)
```

#### Holdings Pie Chart
```python
#    Create pie graph of asset allocations for account, using matplotib
#    Dumps to file ./graph.png by default
#        Specify account optionally
#        - specify regen=True to prevent outputting cached graph [default False]
pie_file = a.holdings_chart(
    account=12345678,
    graph_file="./my_graph_file.png",
    regen=True
)
```


#### Live Quotes
```python
#    Get quote:
#        Go to
#            https://www.ally.com/api/invest/documentation/market-ext-quotes-get-post/
#        to see available fields options
#        [defaults to all fields available]
quote = a.get_quote(
    symbols="spy,ALLY",
    fields="ask,bid,vol"
)
```



### Instruments

#### Equity
```python
Equity("SPY")     # Perfectly equivalent statements
Instrument('spy') # Perfectly equivalent statements
```
#### Option
```python
Call (
    instrument    = Equity("spy"), # Underlying
    maturity_date = "2019-09-30",  # Expiration date
    strike        = 290            # Strike
)

Put (
    instrument    = Instrument("ALLY"), # Underlying
    maturity_date = "2019-10-18",       # Expiration date
    strike        = 300                 # Strike
)
```

### Orders
`Order( timespan, type, price, instrument, quantity)`
```python
market_buy = ally.order.Order(
    
    # Good for day order
    timespan   = ally.order.Timespan('day'),
    
    # Buy order (to_open is True by defaul)
    type       = ally.order.Buy(),
    
    # Market order
    price      = ally.order.Market(),
    
    # Stock, symbol F
    instrument = ally.instrument.Equity('f'),
    
    # 1 share
    quantity   = ally.order.Quantity(1)
)
```

#### TimeInForce (Timespans)
```python
#### Timespans
Timespan('day')
Timespan('gtc')
Timespan('marketonclose')
```



#### Types
```python
Buy()              # Buy to open (default)
Buy(to_open=False) # Buy to cover

Sell()              # Sell short (default)
Sell(to_open=False) # Sell to close
```



#### Pricing
```python
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
    pct=False,    # Treat 'stop' as pct
    stop=5.0      # Stop at $5.00 above lowest price
)
```


#### Quantity
```python
Quantity ( 15 )  # In shares or lots, for an option
```

#### Submitting an Order
```python
exec_status = a.submit_order(
    
    # specify order created, see above
    order=,
    
    # Can dry-run using preview=True, defaults to True
    # Must specify preview=False to actually execute
    preview=True,
    
    # Like always, if not specified in environment, use a specific account
    account=12345678
)

```


## Author
* [Brett Graves](https://github.com/alienbrett)

## Contributing
Please contact me if you enjoyed the project or thought it could be improved. I do my best to code with quality but sometimes it is easier said than done. Anyone with an interest with an eye for detail is welcome to contribute.