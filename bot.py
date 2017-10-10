import hashlib
import io
import tempfile
import time

# lib includes
import twitter

# local includes
import dough
import oven
import validate

VERSION_MAJOR = 0
VERSION_MINOR = 4

KEY_FILE = "keys.secret"

_LICENSE = """
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
"""

LOOP_TIMEOUT = 60


def convert_text_to_data(text):
    """
    Turns the input string into a hash digest for the RNG.
    Current implementation uses MD5.

    Should look more into how the python RNG implements arbitrary length input to seeds.
    Hashing is not required but in the future images or meta-data could be read in and
    digested to a single seed value here.
    """

    return hashlib.md5(text.encode('utf_8')).digest()


def main():
    """
        Sets up twitter api and loops checking for twitter messages
    """

    print(_LICENSE)
    print("Starting DOUGHBot ver {}.{}".format(
        VERSION_MAJOR, VERSION_MINOR), flush=True)
    print("\tThis is considered an alpha version and not complete...")

    # set up twitter-python
    with open(KEY_FILE) as _f:
        _consumer_key = _f.readline().strip()
        _consumer_secret = _f.readline().strip()
        _access_key = _f.readline().strip()
        _access_secret = _f.readline().strip()

    api = twitter.Api(
        consumer_key=_consumer_key,
        consumer_secret=_consumer_secret,
        access_token_key=_access_key,
        access_token_secret=_access_secret)

    # validate the image packs (recipes) are OK
    validate.validateRecipeDir(validate.RECIPE_DIR)

    oven.stock_kitchen()

    messagequeue = []

    # main program loop
    while 1:

        if not messagequeue:
            # if local queue is empty, make a request to twitter for message inbox contents
            messagequeue = api.GetDirectMessages()

        if messagequeue:
            # there is a message in the queue, take it for processing
            message = messagequeue.pop()
            api.DestroyDirectMessage(message.id)

            # convert the text component to a seed for the RNG
            seed = convert_text_to_data(message.text)

            # Use the DOUGH system on input data to get a pizza back. Yum.
            pizza = dough.generatePizza(seed)

            # build and send a response
            responsetext = "For @{}, one {} pizza with {} coming right up!".format(
                message.sender.screen_name, dough.listToSentance(pizza[0]), dough.listToSentance(pizza[1]))

            # TODO
            # workaround: temprary file... I would rather do this in-memory but the API complains

            with tempfile.TemporaryFile(mode="rb+") as imgfile:
                oven.bake_pizza(pizza).save(imgfile, format="PNG")
                api.PostUpdate(status=responsetext, media=imgfile)

            # clear current message
            message = None

        # wait for some time, if the pizza generation gets intensive, this time can be used to build
        # up a queue of processed messages from the backlog
        time.sleep(LOOP_TIMEOUT)


main()
