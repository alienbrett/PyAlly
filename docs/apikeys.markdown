---
Title: Getting API Keys
---
## Getting API Keys

Log into [Ally Invest](https://secure.ally.com), go to the specific account page, click Tools->API

![Tools](https://github.com/alienbrett/PyAlly/blob/master/resources/tools.PNG?raw=true)

Fill out the API token application as a Personal Application

![New Application](https://github.com/alienbrett/PyAlly/blob/master/resources/new_application.PNG?raw=true)


![Details](https://github.com/alienbrett/PyAlly/blob/master/resources/details.PNG?raw=true)

It's ***strongly recommended*** to store the keys in environment variables.
To do this, insert the following into `~/.bashrc`:

```bash
export ALLY_CONSUMER_KEY=XXXXXXXXXXXXXXXXXXXXXXXX
export ALLY_CONSUMER_SECRET=XXXXXXXXXXXXXXXXXXXXX
export ALLY_OAUTH_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXX
export ALLY_OAUTH_SECRET=XXXXXXXXXXXXXXXXXXXXXXXX
export ALLY_ACCOUNT_NBR=12345678
```

Now you can [start an account instance](https://alienbrett.github.io/PyAlly/starting.html) in your python project.


