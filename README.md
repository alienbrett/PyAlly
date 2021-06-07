![PyAlly](https://github.com/alienbrett/pyally/blob/master/img/PYALLY22-small.jpg?raw=true)

# PyAlly Trading Library

![Website](https://img.shields.io/website?up_message=up&url=https%3A%2F%2Falienbrett.github.io%2FPyAlly%2F)![PyPI](https://img.shields.io/pypi/v/pyally)![PyPI - License](https://img.shields.io/pypi/l/pyally)![GitHub issues](https://img.shields.io/github/issues/alienbrett/PyAlly)[![Codacy Badge](https://app.codacy.com/project/badge/Grade/58a4d35357fc4c91b7da1ad723122b0b)](https://www.codacy.com/manual/alienbrett/PyAlly?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=alienbrett/PyAlly&amp;utm_campaign=Badge_Grade)

Take control of your [Ally Invest](https://www.ally.com/api/invest/documentation/getting-started/) finances through Python. Buy stocks and options in an instant, and stay up-to-date with your investments.

Ally Invest's investment platform is perfect for smaller investors who value a mature web/mobile interface, and low brokerage fees. I made this wrapper so that I could more easily integrate the platform with Python, and reduce the need for human oversight on my account.

After setting up API keys, PyAlly can provide the basic/essential Ally brokerage transaction functions from a simple python request.

Make sure to [read the docs](https://alienbrett.github.io/PyAlly)!

## Version 1.2.0

We have added more features in this latest minor release! There have also been numerous contribution and pipeline improvements not listed below. See the commit history for details.

* Added News and Options Searching
  * https://github.com/alienbrett/PyAlly/commit/a12bf634dab79284e9f261df77598ac2d330d1fb
* Added Trade Streaming
  * https://github.com/alienbrett/PyAlly/commit/bb98583d26cc03980a8cd365309b60e5ac5a9272
  * https://github.com/alienbrett/PyAlly/commit/1f301692bc0d28a8c94e7c80a53190360a534ecb

Note that parts of the news searching is broken. Ally's contractor who supplies information for news articles has had trouble suppling some information.

## Planned Features

* Multi-leg orders

## Dev Environment Setup

To setup your dev environment, simply run:

```bash
make venv # run once
source venv/bin/activate # run for every new terminal
```

This will install the library requirements for debugging as well as some useful tools to lint, test, build, document, and deploy. See the `Makefile` for a list of useful targets.

### Dev Environment Teardown

To exit the dev environment, simply run:

```bash
deactivate
```
or `exit` / `logout` your terminal.

### Fixing Your Dev Environment

If your dev environment gets hosed, exit it, remove the `venv` directory, and run the setup above again.

## Contributors

* [Brett Graves](https://github.com/alienbrett)
* [Cole Fox](https://github.com/coalfocks)
* [Rob Valadez](https://github.com/Rob-Valdez)
* [Julian Traversa](https://github.com/JTraversa)
* [Tianyu](https://github.com/Tianyu00)
* [Salient](https://github.com/Salient)
* [Matt Margolin](https://github.com/mm0)
* [Alex Kennedy](https://github.com/LaikaN57)

Message me on Github or [send an email](mailto:alienbrett648@gmail.com) if you enjoyed the project or thought it could be improved. Anyone with an interest, with an eye for detail, is welcome to contribute.

If you're dying to buy me a beer, I accept venmo at @alienbrett. That said, feel no obligation; this is free software and it's here for you to use.
