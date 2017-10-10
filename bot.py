import twitter
import hashlib
import time

# local includes
import dough
import validate

VERSION_MAJOR = 0
VERSION_MINOR = 3

KEY_FILE = "keys.secret"

"""
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

def convertTextToData(text):
	"""
	Turns the input string into a hash digest for the RNG.
	Current implementation uses MD5.
	
	Should look more into how the python RNG implements arbitrary length input to seeds.
	Hashing is not required but in the future images or meta-data could be read in and
	digested to a single seed value here.
	"""
	
	return hashlib.md5(text.encode('utf_8')).digest()


def main():

	print("Starting DOUGHBot ver {}.{}".format(VERSION_MAJOR,  VERSION_MINOR), flush=True)
	
	# set up twitter-python
	with open(KEY_FILE) as f:
	    CONSUMER_KEY = f.readline().strip()
	    CONSUMER_SECRET = f.readline().strip()
	    ACCESS_KEY = f.readline().strip()
	    ACCESS_SECRET = f.readline().strip()

	api = twitter.Api(
		consumer_key=CONSUMER_KEY,
		consumer_secret=CONSUMER_SECRET,
		access_token_key=ACCESS_KEY,
		access_token_secret=ACCESS_SECRET)
	
	# validate the image packs (recipes) are OK
	validate.validateRecipeDir(validate.RECIPE_DIR)
	
	messageQueue = []
	
	# main program loop
	while 1:

		if not messageQueue:
			# if local queue is empty, make a request to twitter for message inbox contents
			messageQueue = api.GetDirectMessages()
		
		if messageQueue:
			# there is a message in the queue, take it for processing
			message = messageQueue.pop()
			api.DestroyDirectMessage(message.id)
			
			# convert the text component to a seed for the RNG
			seed = convertTextToData(message.text)

			# Use the DOUGH system on input data to get a pizza back. Yum.
			pizza = dough.generatePizza(seed)
			
			# build and send a response
			responseText = "One {} pizza with {} coming right up!".format(
				dough.listToSentance(pizza[0]), dough.listToSentance(pizza[1]))
	
			api.PostDirectMessage(text=responseText, user_id=message.sender_id)
			
			# clear current message
			message = None
	
		# wait for some time, if the pizza generation gets intensive, this time can be used to build
		# up a queue of processed messages from the backlog
		time.sleep(LOOP_TIMEOUT)
	
main()