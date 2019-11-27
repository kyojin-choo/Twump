# extract.py -*- scraping twitter -*-
#
# Author: Daniel Choo
# Date:   10/28/19
# URL:    https://www.github.com/kyoogoo/twump

import os
import sys
import time
import json
import tweepy
import threading
import itertools
from src.twitter_json import Encode

def authorize():
    """ authorize(): Reads in credentials JSON; verifies login.
                     If the credentials files does not exist, create a
                     template for the user.
        Return:      N/A (sys.exit if file is missing)
    """
    secret = {"ACCESS_KEY":      None,
              "ACCESS_SECRET":   None,
              "CONSUMER_KEY":    None,
              "CONSUMER_SECRET": None}

    values = ["ACCESS_KEY", "ACCESS_SECRET", "CONSUMER_KEY", "CONSUMER_SECRET"]

    # If the file (credentials.json) exists...
    if os.path.exists("credentials.json"):
        # Open file and read in the json information.
        with open("credentials.json") as cred:
            data = json.load(cred)
            counter = 0
            # Appending the values into secret dict.
            for key in secret:
                secret[key] = data[values[counter]]
                counter += 1

        # Checking OAuth authentication...
        try:
            auth = tweepy.OAuthHandler(secret["CONSUMER_KEY"], secret["CONSUMER_SECRET"])
        except tweepy.RaiseError:
            print("\nError: Invalid consumer key!\n")
            sys.exit(-1)

        # Checking access_token...
        try:
            auth.set_access_token(secret["ACCESS_KEY"], secret["ACCESS_SECRET"])
        except tweepy.RaiseError:
            print("Error: Invalid access token!\n")
            sys.exit(-1)

        # Success! Ensure we are running a JSON parser.
        api = tweepy.API(auth)
        print("\n✧･ﾟ Authorized! ✧･ﾟ")
        print("Logged in as: " + str(api.me().screen_name + "\n"))
        return api

    # If the file does not exist...
    else:
        # If the credentials.json is missing and the template exists... typo?
        if os.path.exists("credentials_template.json"):
            print("\nYou have either not properly named your file to 'credentials.json'")
            print("Or there may be a typo in the file name. Else, this error should not be occurring.")
            sys.exit(-1)
        else:
            # If the credentials.json and template do not exist, create it!
            with open("credentials_template.json", "w") as file:
                file.write(json.dumps(secret, indent=4))
                print("\nCreated new template.\nHowever, you are missing the necessary file to proceed")
                print("Please fill in the blanks with the necessary information.")
                print("Also, please rename the template file to 'credentials.json'")
                sys.exit(-1)

def extract(api, username):
    """ extract(): Extracting data from Twitter (REST API)
                   It will print out the messages it scrapes and append
                   them into a JSON file.
        Return:    N/A [None]
    """
    # Attempt to see if the user exists on Twitter.
    try:
        # Use streaming API on my own Twitter feed
        if username == "self":
            print("myself")
            sys.exit(0)
        # Use REST API on user's twitter timeline
        else:
            api.get_user(username)
    # If username does not exist...
    except tweepy.TweepError:
        print("\nThat user does not exist. Exiting program.\n")
        sys.exit(-1)

    # Formatting file path; initializing variables.
    counter = 0
    filename = username + ".json"
    path = "data/" + filename
    print("This is the path: " + path)
    print("\nRetreiving Tweets from " + str(username) + "...\n")

    """  parser=JSONParser()" currently still faces a bug. It will demonstrate this
         error code. 'JSONParser' object has no attribute 'model_factory.'
         Read more about it here: https://github.com/tweepy/tweepy/issues/538
         Thus, I've elected to design the JSON similarly to Twitter's format.
         However, I want to keep what I think is necessary. Trimming fat.
    """
    # If the path exists...
    if os.path.exists(path):
        pass
    else:
        with open(path, "w+") as file:
            # Instantiating encode class.
            encode = Encode()

            # Iterating through user' tweets (REST)
            for tweet in tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode="extended").items():
                print(tweet)
	            #            file.write(json.dumps(x, indent=4))
                if counter >= 0:
                    break
                else:
                    counter+=1

            counter = 0
            print("Extracting", end="")
            for c in itertools.cycle(["."]):
                print(c, flush=True, end="")
                time.sleep(0.5)
                if counter >= 3:
                     break
                counter+=1


def main():
    """ main(): the bootstrapper
        Return: sys.exit(0)
    """
    # Initializing variables.
    valid = {"": "", "y": "y", "n": "n", "yes": "yes", "no": "no"}
    usr_input = "abc"

    # While the user would like to keep running the program...
    while usr_input not in valid:
        # Prompt
        usr_input = input("Would you like to scrape (yes): ")

        # Checking if input is valid.
        while usr_input not in valid:
            usr_input = input("Invalid Input.\nWould you like to scrape (yes): ")

        # Bye :(
        if usr_input == "n" or usr_input == "no":
            break
        # Lets go!
        elif usr_input == "y" or usr_input == "":
            api = authorize()                        # Checking users' consumer/api key.
            usr_input = input("Enter the Twitter Account to scrape: ")
            extract(api, usr_input)                  # Extract information wanted information
            print("\n\nDone.\n")
            return 0                                 # Fini
        # This should not be possible. Literally. I think.
        else:
            raise Exception('This is not possible. How did you get here.')


main()
