"""A twitter bot that reads direct message hashes and responds with pizza"""

__version__ = "0.5"

import hashlib
import tempfile
import time

# lib includes
import twitter

# local includes
import dough
import oven

_NOTICE = """
	(c) 2017 Henry Webster

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    The author of this program is not to be held liable for putting pineapple
    on any pizzas.  
"""

_KEY_FILE = "keys.secret"
_LOOP_TIMEOUT = 60


def _convert_text_to_data(text):
    """
    Turns the input string into a hash digest for the RNG.
    Current implementation uses MD5.

    Should look more into how the python RNG implements arbitrary length input to seeds.
    Hashing is not required but in the future images or meta-data could be read in and
    digested to a single seed value here.
    """

    return hashlib.md5(text.encode("utf_8")).digest()


def main():
    """main program loop"""

    # TODO 
    # * move into seperate helper?
    print(_NOTICE)
    print("Starting DOUGHBot ver {}".format(__version__), flush=True)
    print("*this is considered an alpha version and not complete...*")

    # set up twitter-python
    with open(_KEY_FILE) as _f:
        _consumer_key = _f.readline().strip()
        _consumer_secret = _f.readline().strip()
        _access_key = _f.readline().strip()
        _access_secret = _f.readline().strip()

    api = twitter.Api(
        consumer_key=_consumer_key,
        consumer_secret=_consumer_secret,
        access_token_key=_access_key,
        access_token_secret=_access_secret)


    oven.stock_kitchen()

    messagequeue = []

    # main program loop
    while 1:

        if not messagequeue:
            messagequeue = api.GetDirectMessages()

        if messagequeue:
            message = messagequeue.pop()
            api.DestroyDirectMessage(message.id)

            seed = _convert_text_to_data(message.text)

            # Use the DOUGH system on input data to get a pizza back. Yum.
            pizza = dough.generate_pizza(seed)
            responsetext = dough.generate_response(pizza, "@" + message.sender.screen_name)

            # TODO
            # * workaround: temprary file... I would rather do this in-memory but the API complains
            # * verify it is closing

            filed, filepath = tempfile.mkstemp(suffix=".png", dir=".")
            with open(filed, "rb+") as imgfile:
                oven.bake_pizza(pizza).save(imgfile, format="PNG")
                api.PostUpdate(status=responsetext, media=filepath)

            message = None

        # wait for some time, if the pizza generation gets intensive, this time can be used to build
        # up a queue of processed messages from the backlog
        time.sleep(_LOOP_TIMEOUT)


main()
