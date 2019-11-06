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

def extract():
    for c in itertools.cycle([".", "..", "..."]):
        print("Extracting" + c, flush=True)
        time.sleep(0.5)

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

    if usr_input == "n" or usr_input == "no":
        print("\nSee ya!")
        sys.exit(0)
    elif usr_input == "y" or usr_input == "":
        extract()
        return 0


main()
