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
import itertools


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
        print("Logged in as: " + str(api.me().screen_name))
        return api

    # If the file does not exist...
    else:
        # If the credentials.json is missing and the template exists, typo?
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


def print_tweet(status):
    """ print_tweet(status): just prints the tweet text (void function)
        Return:              N/A (void)
    """
    if 'retweeted_status' in status._json:
        print("\n" + str(status.created_at) + ": " + status._json['retweeted_status']['full_text'])
    else:
        print("\n" + str(status.created_at) + ": " + status.full_text)


def getUser(api):
    """ getUser(username): retrieves user input from the user and 
        Return:            user (API object)
    """
    # Attempt to see if the user exists on Twitter.
    while True:
        user_input = -1
        username = input("\nEnter the Twitter Account to scrape: ")
        try:
            # Use streaming API on my own Twitter feed
            if username == "self":
                print("myself")
                sys.exit(0)
            # Use REST API on user's twitter timeline
            else:
                user = api.get_user(username)

        # If username does not exist, retry or exit.
        except tweepy.TweepError:
            print("\nThat user does not exist.")
            while user_input not in range(0, 2):
                user_input = int(input("0 to exit, 1 to retry: "))

            if user_input == 1:
                continue
            else:
                print("\nGoodbye!")
                sys.exit(-1)
        # If we successfully retrieve a user, leave the loop.
        else:
            break

    return user


def extract(api, username):
    """ extract(): Extracting data from Twitter (REST API)
                   It will print out the messages it scrapes and append
                   them into a JSON file.
        Return:    N/A [None]
    """
    # Formatting file path; initializing variables.
    filename = username + ".json"
    path = "data/" + filename
    print("\nThis is the path: " + path)
    print("Retreiving Tweets from " + str(username) + "...\n")

    """  parser=JSONParser()" currently still faces a bug. It will demonstrate this
         error code. 'JSONParser' object has no attribute 'model_factory.'
         Read more about it here: https://github.com/tweepy/tweepy/issues/538
         Thus, I've elected to design the JSON similarly to Twitter's format.
         However, I want to keep what I think is necessary. Trimming fat.

         Note: This has been resolved via a private variable: status._json.
               I may come back and work on my own Twitter JSON parser, but that
               is now indefinitly postponed.
    """
    check = False
    counter = 0
    tweet = ""
    # Printing message, but also boolean value flips if the file exists. Required for loading JSON.
    if os.path.exists(path):
        print("Path already exists.")
        with open(path, "r") as file:
            for line in file:
                if "full_text" in line:
                    line = line.strip()                       # Strips whitespace
                    line = line.replace('"full_text": ', "")  # Removes "full_text: "
                    tweet = line[:-1]                         # Removes comma at the end
                    tweet = tweet[1:-1]                       # Removes the quotes
                    break
                else:
                    counter+=1
        check = True
        counter = 0
    else:
        print("Creating a new file.")

    # Automatically creates a new file!
    with open(path, "a+") as file:
        # Iterating through user' tweets (REST)
        for status in tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode="extended").items():
            # If the Tweet exists in our JSON file. No need to reappend it in. Break!
            if check is True:
                if status.full_text in tweet:
                    print("Tweet already exists in JSON. Breaking.")
                    break
            print_tweet(status)

            # Unfortunately, we have to set ensure_ascii to False because it does 
            # not encode Emojis properly--which is a problem when comparing strings.
            file.write(json.dumps(status._json, indent=4, ensure_ascii=False))
            if counter >= 30:
                break
            else:
                counter+=1

#            counter = 0
#            print("Extracting", end="")
#            for c in itertools.cycle(["."]):
#                print(c, flush=True, end="")
#                time.sleep(0.5)
#                if counter >= 3:
#                     break
#                counter+=1


def main():
    """ main(): the bootstrapper
        Return: sys.exit(0)
    """
    # Initializing variables.
    valid = {"": "", "y": "y", "n": "n", "yes": "yes", "no": "no"}
    usr_input = "abc"
    logo = """.   . .    .  .    .  .    .  .    .  .    .  .    .  .    .  .
 .     .    .  .    .  .    .  .    ..S88888X88t. .    . . .      . .
  .    .   .  ;;   .       .       . .XX88888X8@@88@t%..:%88%   . .
     .   .   :@8t;   .  .    .  .   X888888X8X88S8X88888@88888:.      .  .
  .    .    .X888:X   .   .   .   .%888888888888888888888 @@8@  .     .
    .     .  88S888.X:  .   .   . :X88888%8 888888S@888%88888t    . .
  .   .     .S@8 88888 8t.        X8888@8S8888S8888S88 8 88@t . .      .
    .   . .  ;888 8888888@8@..  . 88888888S88 8 @888%X8888X.      .  .
  .          :8 8888 888888@8 S88@8X8888888888888888888%88S .. .         .
     . .  .  %X@888888S888 8S@888888888S8 888 888 @ @8XS8S: .   .  . .
  .         .XX88888S8888X888 8S8 888888888888@888888S8888S    .   .    .
    .  . .   ;8S8 8 @88 8 88X8%888%8S888888888 88888888888. . .  .    . 
  .        . :S @88888888888 888888888XS888888 8888 888 @      .    .
    . .  .   .:%8888888888S8888 888S88S8888 88888888888:    .  .     . .
  .        .   ;%8888 @8888 888888S888 8888888888888 S     .   . .
     . .        .888888S8888%8 888888S88888888S8 888:.  .    .      .
  .      .  . . .888 888 @88888 8S8888888S888@888 8   .   .    .  .
    .  .        ..@8888888888 8888S88S8 88888X8888      .   .        .
  .      .  .  .  : X8%8S8 888888S8888888%8S8888:        .   . .  .
    . .       .  .   . ;8@8 888 88888888 @88 8St     .     .
  .     . .      .   ;888888S888S@88 8888 888t         .     .  .  .
     .     .t%%SS@88 88888888 88888 @88X8888.  .  .  .   .    .     .
  .    .    ;8X@888%88888 @88888 8S@8@ 888..           .   .     .
    .    . . :S@888 888888 888S88888888 .    . .  . .    .   .  .   .
  .   .      ...%t   .t88888888; S.%::  .  .     .    .    .      .
    .   .  .  .        :t.:;;.. .  .         .      .   .    .  .
  .      .   . .  . .  ...   ..      . . .     .  .   .   .   .    .  """
    print(logo + "\n")

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
#            print("Type 'self' to scrape your Twitter feed in live time.")
            username = getUser(api).screen_name
            extract(api, username)                  # Extract information wanted information
            print("\nDone.\n")
            return 0                                 # Fini
        # This should not be possible. Literally. I think.
        else:
            raise Exception('This is not possible. How did you get here.')


main()
