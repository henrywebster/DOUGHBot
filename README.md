# DOUGHBot
DOUGH stands for Digitally Optimized Utility for inGredient Hacking

## Overview

### Twitter bot
The DOUGH bot is at <https://twitter.com/_DOUGHBot>. It will read incoming direct messages and send a response message back 
with a pizza order and message.

It uses [python-twitter](https://github.com/bear/python-twitter) to interact with the Twitter API in Python.

[Pillow](https://github.com/python-pillow/Pillow) is the image processing library used for generating the images.

### DOUGH (secret sauce)
The DOUGH module takes in ingredient and modifer lists and enables randomized pizza orders based on those ingredients.
There are two kinds of ingredients:

* Premium (something you might expect to cost more or be the *main* topping)
* Free (something extra that is usually gratis at a pie shop)

Each category has its own *modifier list*, which is an attribute that might be expected to customize an order

## Future
* Pizza image generator
* Put the bot on a server so it's always running.
* Change format to *premium list* pizza *modifier premium list* etc... as in "Sausage pizza extra sausage". It sounds better.
