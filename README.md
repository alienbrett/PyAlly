# PyAlly
Python3 wrapper for [Ally Invest brokerage API](https://www.ally.com/api/invest/documentation/getting-started/ "Ally Invest API")

Ally Bank's investment platform is perfect for smaller investors who value a mature web/mobile interface, and low brokerage fees. I made this wrapper so that I could more easily integrate the platform with Python, and reduce the need for human oversight on my account.

After setting up API keys, PyAlly can provide the basic/essential transaction functions from a simple python request.

## Supported features
* Stock buy/sell/short/buy-to-cover orders
* Instrument quotes
* Query account transaction history
* Query account holdings
* Represent account holdings
## Planned Features
* Option trading
* Backtrader integration
* More complex orders
* Advanced portfolio analysis

## Requirements
* requests-oathlib
* matplotlib

## Installation
Currently, the package can only be used from this github library. In the future, it will be available as a PyPi package.

Once the package is downloaded, we recommend setting environment variables to store
Ally API credentials. Insert the following into `~/.bashrc`:

```bash
export ALLY_CONSUMER_KEY=XXXXXXXXXXXXXXXXXXXXXXXX
export ALLY_CONSUMER_SECRET=XXXXXXXXXXXXXXXXXXXXX
export ALLY_OATH_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXX
export ALLY_OATH_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXX
```


## Usage

Once the api keys are configured, your brokerage account can be easily accessed via a few simple pythonic functions:

```python
import ally

#	Create new Ally object, with API credentials specified in environment
a = ally.Ally()


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

#    Get current holdings for an account in JSON dict format
#        Uses default account if not specified
#        Optionally dump json to file
current_holdings = a.get_holdings(
    account=12345678,
    outfile="./holdings.json"
)

#    Create pie graph of asset allocations for account, using matplotib
#    Dumps to file ./graph.png by default
#        Specify account optionally
#        - specify regen=True to prevent outputting cached graph [default False]
pie_file = a.holdings_chart(
    account=12345678,
    graph_file="./my_graph_file.png",
    regen=True
)


#    Get quote:
#        Go to
#            https://www.ally.com/api/invest/documentation/market-ext-quotes-get-post/
#        to see available fields options
#        [defaults to None]
quote = a.get_quote(
    symbols="SPY,ALLY",
    fields="ask,bid,vol"
)




#    Create an Order:

# Market buy order
market_buy = ally.order.Long(
    
    # Symbol
    sym="ALLY",
    
    # Quantity in units of shares
    qty=1.0,
    
    # Execute at Market
    price=None,
    
    # Good For Day
    timespan='GFD'
)

# Limit short-sell order
#    Will only execute if execution price is more favorable than price
#    Limit works for buy and sell
limit_sell = ally.order.Long(
    
    # Symbol
    sym="ALLY",
    
    # Negative quantity indicates sell or short-sell
    qty=-1.0,
    
    # Set limit price. Will only execute at price more favorable than specified price
    #    (less than limit if buy, greater than limit if sell)
    price=29.69,
    
    # Good Till Cancelled
    timespan='GTC',
    
    # new_position defaults to true
    # Negative quantity & new_position==True? Short
    # Negative quantity & new_position==False? Sell
    new_position=True
)


#   Submit Order for an account:

exec_status = a.submit_order(
    
    # specify order created, see above
    order=market_buy,
    
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