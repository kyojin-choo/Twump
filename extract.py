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

    if os.path.exists("credentials.json"):
        # Opening file and reading in the json information.
        with open("credentials.json") as cred:
            data = json.load(cred)
            counter = 0
            for key in secret:
                secret[key] = data[values[counter]]
                counter += 1
            auth = tweepy.OAuthHandler(secret["CONSUMER_KEY"], secret["CONSUMER_SECRET"])
            auth.set_access_token(secret["ACCESS_KEY"], secret["ACCESS_SECRET"])
            pass

    else:
        # If the credentials.json is missing and the template exists... typo?
        if os.path.exists("credentials_template.json"):
            print("\nYou have either not properly named your file to 'credentials.json'")
            print("Or there may be a typo in the file name. Else, this error should not be occurring.")
            sys.exit(1)
        else:
            # If the credentials.json and template do not exist, create it!
            with open("credentials_template.json", "w") as file:
                file.write(json.dumps(secret, indent=4))
                print("\nCreated new template.\nHowever, you are missing the necessary file to proceed")
                print("Please fill in the blanks with the necessary information.")
                print("Also, please rename the template file to 'credentials.json'")
                sys.exit(1)


def extract():
    """ extract(): Extracting data from Twitter
                   It will print out the messages it scrapes and append
                   them into a JSON file.
        Return:    N/A [None]
    """
    for c in itertools.cycle([".", "..", "..."]):
        print("Extracting" + c, flush=True)
        time.sleep(0.5)
        if c == "...":
            break


def main():
    """ main(): the bootstrapper
        Return: sys.exit(0)
    """
    # Initializing variables.
    valid = {"": "", "y": "y", "n": "n", "yes": "yes", "no": "no"}
    usr_input = "abc"

    usr_input = input("Would you like to scrape (yes): ")

    # Checking if input is valid.
    while usr_input not in valid:
        usr_input = input("Invalid Input.\nWould you like to scrape (yes): ")

    # Bye :(
    if usr_input == "n" or usr_input == "no":
        print("\nSee ya!")
        sys.exit(0)

    # Lets go!
    elif usr_input == "y" or usr_input == "":
        authorize()
        extract()
        print("Done.\n")
        return 0

    # This should not be possible.
    else:
        raise Exception('This is not possible. How did you get here.')

main()
