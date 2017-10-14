"""A twitter bot that reads direct message hashes and responds with pizza"""

__version__ = "0.7"

import hashlib
import os
import tempfile
import time
from collections import deque

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


def _file_to_list(filename):
    """turn a file with one item to a line into a python list"""

    return [line.rstrip() for line in open(filename) if not None]


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

    # set up D.O.U.G.H.

    dsystem = dough.Dough(
        _file_to_list("premium.txt"),
        _file_to_list("premiummod.txt"),
        _file_to_list("free.txt"),
        _file_to_list("freemod.txt"),
        _file_to_list("responses.txt"))

    # might not be needed by why not be scalable
    messagequeue = deque()
    basicoven = oven.Oven(os.path.join("recipes", "basic"))

    # main program loop
    while 1:

        if not messagequeue:
            messagequeue = deque(api.GetDirectMessages())

        if messagequeue:
            message = messagequeue.pop()
            api.DestroyDirectMessage(message.id)

            seed = _convert_text_to_data(message.text)

            # Use the DOUGH system on input data to get a pizza back. Yum.
            pizza = dsystem.generate_pizza(seed)
            responsetext = dsystem.generate_response(
                pizza, "@" + message.sender.screen_name)

            # * workaround: temprary file... I would rather do this in-memory but the API complains
            filed, filepath = tempfile.mkstemp(suffix=".png", dir=".")
            try:
                with os.fdopen(filed, "rb+") as imgfile:
                    basicoven.bake(pizza).save(imgfile, format="PNG")
                    api.PostUpdate(status=responsetext, media=filepath)
            finally:
                os.remove(filepath)
            message = None

        # wait for some time, if the pizza generation gets intensive, this time can be used to build
        # up a queue of processed messages from the backlog
        time.sleep(_LOOP_TIMEOUT)


main()
