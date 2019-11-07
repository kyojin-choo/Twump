# extract.py -*- scraping twitter -*-
#
# Author: Daniel Choo
# Date:   10/28/19

import os
import sys
import time
import json
import tweepy
import threading
import itertools


def authorize():
    """ authorize(): Reads in credentials JSON; verifies login.
        Return:      N/A (throws error)
    """
    with open("credentials.json") as cred:
        data = json.load(cred)
        

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
        creds = authorize()
        extract()
        print("Done.\n")
        return 0

    # This should not be possible.
    else:
        raise Exception('This is not possible. How did you get here.')

main()
