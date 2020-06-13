To import the library, just run
```python
import ally
```

Then, we can create an an API object a couple different ways:

### Environment Variables (Easy)
It's **strongly recommended** that the [API keys](https://alienbrett.github.io/PyAlly/apikeys) be stored as environment variables. If the account variables are specified as recommended, instantiation is easy:
```python
a = ally.Ally()
```
**And you're done!**

***

### As Parameters (Insecure)

However, variables can be passed in on instantiation. This way, no account variables need to be set.
Keep in mind that this is much less secure for distributable applications, since anyone with these keys
will have access to the account with which they're associated.
```python
params = {
  'ALLY_OAUTH_SECRET'     : ...,
  'ALLY_OAUTH_TOKEN'      : ...,
  'ALLY_CONSUMER_SECRET'  : ...,
  'ALLY_CONSUMER_KEY'     : ...,
  'ALLY_ACCOUNT_NBR'      : ...
}

a = ally.Ally(params)
```
### From File

Parameters can also be read from a JSON file:
`params.json`
```
{
  'ALLY_OAUTH_SECRET'     : ...,
  'ALLY_OAUTH_TOKEN'      : ...,
  'ALLY_CONSUMER_SECRET'  : ...,
  'ALLY_CONSUMER_KEY'     : ...,
  'ALLY_ACCOUNT_NBR'      : ...
}
```
Now you're ready to make API calls with your new object.
